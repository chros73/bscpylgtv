import asyncio
import base64
import copy
import functools
import json
import os
from datetime import timedelta

try:
    import numpy as np
except ImportError:
    np = None

import websockets

from . import buttons as btn
from . import endpoints as ep
from .exceptions import PyLGTVPairException, PyLGTVCmdException, PyLGTVCmdError, PyLGTVServiceNotFoundError
from .handshake import REGISTRATION_MESSAGE
from .storage_proto import StorageProto
from .storage_sqlitedict import StorageSqliteDict

if np:
    from . import cal_commands as cal
    from .constants import BT2020_PRIMARIES, CALIBRATION_TYPE_MAP, DEFAULT_CAL_DATA
    from .lut_tools import (
        create_dolby_vision_config,
        read_cal_file,
        read_cube_file,
        unity_lut_1d,
        unity_lut_3d,
    )

SOUND_OUTPUTS_TO_DELAY_CONSECUTIVE_VOLUME_STEPS = {"external_arc"}


class WebOsClient:
    STATIC_STATES = {"system_info", "software_info"}

    def __init__(
        self,
        ip,
        key_file_path=None,
        timeout_connect=2,
        ping_interval=1,
        ping_timeout=20,
        client_key=None,
        volume_step_delay_ms=None,
        get_hello_info=False,
        states=["system_info", "software_info", "power", "current_app", "muted",
                "volume", "apps", "inputs", "sound_output", "picture_settings"],
        storage: StorageProto=None,
    ):
        """Initialize the client."""
        self.ip = ip
        self.port = 3000
        self.key_file_path = key_file_path
        self.client_key = client_key
        self.command_count = 0
        self.timeout_connect = timeout_connect
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.getHelloInfo = get_hello_info
        self.storage = storage
        self.connect_task = None
        self.connect_result = None
        self.connection = None
        self.input_connection = None
        self.handler_tasks = set()
        self.callbacks = {}
        self.futures = {}
        self._power_state = {}
        self._current_appId = None
        self._muted = None
        self._volume = None
        self._current_channel = None
        self._channel_info = None
        self._channels = None
        self._apps = {}
        self._extinputs = {}
        self._system_info = None
        self._software_info = None
        self._hello_info = None
        self._sound_output = None
        self._picture_settings = None
        self.state_update_callbacks = []
        self.doStateUpdate = False
        self._volume_step_lock = asyncio.Lock()
        self._volume_step_delay = (
            timedelta(milliseconds=volume_step_delay_ms)
            if volume_step_delay_ms is not None
            else None
        )
        self.states = (set(states) if isinstance(states, list) else set())

    @classmethod
    async def create(cls, *args, **kwargs):
        client = cls(*args, **kwargs)
        await client.async_init()
        return client

    async def async_init(self):
        """Load client key from storage if it's required."""
        if self.client_key is None:
            if self.storage is None:
                self.storage = await StorageSqliteDict.create(self.key_file_path)
            elif not isinstance(self.storage, StorageProto):
                raise PyLGTVCmdException("Storage is not a StorageProto class.")

            self.client_key = await self.storage.get_key(self.ip)

    async def get_storage(self):
        return self.storage

    async def connect(self):
        if not self.is_connected():
            self.connect_result = asyncio.Future()
            self.connect_task = asyncio.create_task(self.connect_handler(self.connect_result))
        return await self.connect_result

    async def disconnect(self):
        if self.is_connected():
            self.connect_task.cancel()
            try:
                await self.connect_task
            except asyncio.CancelledError:
                pass

    def is_registered(self):
        """Paired with the tv."""
        return self.client_key is not None

    def is_connected(self):
        return self.connect_task is not None and not self.connect_task.done()

    def registration_msg(self):
        handshake = copy.deepcopy(REGISTRATION_MESSAGE)
        handshake["payload"]["client-key"] = self.client_key
        return handshake

    async def connect_handler(self, res):
        ws = None
        try:
            ws = await asyncio.wait_for(
                websockets.connect(
                    f"ws://{self.ip}:{self.port}",
                    ping_interval=None,
                    close_timeout=self.timeout_connect,
                    max_size=None,
                ),
                timeout=self.timeout_connect,
            )

            if self.getHelloInfo:
                # send hello
                await ws.send(json.dumps({"id": "hello", "type": "hello"}))
                raw_response = await ws.recv()
                response = json.loads(raw_response)

                if response["type"] == "hello":
                    self._hello_info = response["payload"]
                else:
                    raise PyLGTVPairException("Unable to say hello")

            # send registration
            await ws.send(json.dumps(self.registration_msg()))
            raw_response = await ws.recv()
            response = json.loads(raw_response)

            if (response["type"] == "response" and response["payload"]["pairingType"] == "PROMPT"):
                raw_response = await ws.recv()
                response = json.loads(raw_response)

                if response["type"] == "registered":
                    self.client_key = response["payload"]["client-key"]
                    await self.storage.set_key(self.ip, self.client_key)

            if not self.client_key:
                raise PyLGTVPairException("Unable to pair")

            self.handler_tasks.add(asyncio.create_task(self.consumer_handler(ws)))

            if self.ping_interval is not None and self.ping_timeout is not None:
                self.handler_tasks.add(asyncio.create_task(self.ping_handler(ws)))

            self.connection = ws

            if self.states:
                selectedStates = self.states
                # set static states, possible values: ["system_info", "software_info"]
                staticStates = selectedStates.intersection(self.STATIC_STATES)
                if staticStates:
                    # e.g.: [self._system_info] = await asyncio.gather(self.get_system_info())
                    for stateElem in staticStates:
                        stateResult = await asyncio.gather(getattr(self, f'get_{stateElem}')())
                        setattr(self, f'_{stateElem}', (stateResult or [None])[0])
                        selectedStates.remove(stateElem)

                # subscribe to state updates, avoid partial updates during initial subscription
                # possible values: ["power", "current_app", "muted", "volume", "apps", "inputs",
                #                   "sound_output", "picture_settings"]
                subscribe_coros = set()
                if selectedStates:
                    # e.g.: subscribe_coros.add(self.subscribe_power(self.set_power_state))
                    for stateElem in selectedStates:
                        subscriber = f'subscribe_{stateElem}'
                        setter = f'set_{stateElem}_state'

                        if callable(getattr(self, subscriber, None)) and callable(getattr(self, setter, None)):
                            subscribe_coros.add(getattr(self, subscriber)(getattr(self, setter)))

                if subscribe_coros:
                    subscribe_tasks = set()

                    for coro in subscribe_coros:
                        subscribe_tasks.add(asyncio.create_task(coro))

                    await asyncio.wait(subscribe_tasks)

                    for task in subscribe_tasks:
                        try:
                            task.result()
                        except (PyLGTVCmdError, PyLGTVServiceNotFoundError):
                            pass

            # set placeholder power state if not available
            if not self._power_state:
                self._power_state = {"state": "Unknown"}

            self.doStateUpdate = True

            if self.state_update_callbacks:
                await self.do_state_update_callbacks()

            res.set_result(True)

            await asyncio.wait(self.handler_tasks, return_when=asyncio.FIRST_COMPLETED)

        except Exception as ex:
            if not res.done():
                res.set_exception(ex)
        finally:
            for task in self.handler_tasks:
                if not task.done():
                    task.cancel()

            for future in self.futures.values():
                future.cancel()

            closeout = set()
            closeout.update(self.handler_tasks)

            if ws is not None:
                closeout.add(asyncio.create_task(ws.close()))

            if self.input_connection is not None:
                closeout.add(asyncio.create_task(self.input_connection.close()))

            for callback in self.state_update_callbacks:
                closeout.add(callback(self))

            if closeout:
                closeout_task = asyncio.create_task(asyncio.wait(closeout))

                while not closeout_task.done():
                    try:
                        await asyncio.shield(closeout_task)
                    except asyncio.CancelledError:
                        pass

            self.connection = None
            self.input_connection = None
            self.connect_task = None
            self.connect_result = None
            self.handler_tasks = set()
            self.callbacks = {}
            self.futures = {}
            self.state_update_callbacks = []
            self.doStateUpdate = False

            self._power_state = {}
            self._current_appId = None
            self._muted = None
            self._volume = None
            self._current_channel = None
            self._channel_info = None
            self._channels = None
            self._apps = {}
            self._extinputs = {}
            self._system_info = None
            self._software_info = None
            self._hello_info = None
            self._sound_output = None
            self._picture_settings = None

    async def ping_handler(self, ws):
        try:
            while True:
                await asyncio.sleep(self.ping_interval)
                if self.is_on:
                    ping_waiter = await ws.ping()
                    await asyncio.wait_for(ping_waiter, timeout=self.ping_timeout)
        except (
            asyncio.TimeoutError,
            asyncio.CancelledError,
            websockets.exceptions.ConnectionClosedError,
            websockets.exceptions.ConnectionClosedOK,
        ):
            pass

    async def callback_handler(self, queue, callback, future):
        try:
            while True:
                msg = await queue.get()
                payload = msg.get("payload")
                await callback(payload)
                if future is not None and not future.done():
                    future.set_result(msg)
        except asyncio.CancelledError:
            pass

    async def consumer_handler(self, ws):
        callback_queues = {}
        callback_tasks = {}

        try:
            async for raw_msg in ws:
                if self.callbacks or self.futures:
                    msg = json.loads(raw_msg)
                    uid = msg.get("id")
                    callback = self.callbacks.get(uid)
                    future = self.futures.get(uid)

                    if callback is not None:
                        if uid not in callback_tasks:
                            queue = asyncio.Queue()
                            callback_queues[uid] = queue
                            callback_tasks[uid] = asyncio.create_task(
                                self.callback_handler(queue, callback, future)
                            )
                        callback_queues[uid].put_nowait(msg)
                    elif future is not None and not future.done():
                        self.futures[uid].set_result(msg)

        except (
            asyncio.CancelledError,
            websockets.exceptions.ConnectionClosedError,
            websockets.exceptions.ConnectionClosedOK,
        ):
            pass
        finally:
            for task in callback_tasks.values():
                if not task.done():
                    task.cancel()

            tasks = set()
            tasks.update(callback_tasks.values())

            if tasks:
                closeout_task = asyncio.create_task(asyncio.wait(tasks))

                while not closeout_task.done():
                    try:
                        await asyncio.shield(closeout_task)
                    except asyncio.CancelledError:
                        pass

    def __output_result(self, res, jsonOutput=False, sortKeys=True, indent=4):
        """Output result as it is (e.g. dictionary) or JSON string."""
        if jsonOutput:
            return json.dumps(res, sort_keys=sortKeys, indent=indent)
        else:
            return res

    # manage state
    @property
    def power_state(self):
        return self._power_state

    @property
    def current_appId(self):
        return self._current_appId

    @property
    def muted(self):
        return self._muted

    @property
    def volume(self):
        return self._volume

    @property
    def current_channel(self):
        return self._current_channel

    @property
    def channel_info(self):
        return self._channel_info

    @property
    def channels(self):
        return self._channels

    @property
    def apps(self):
        return self._apps

    @property
    def inputs(self):
        return self._extinputs

    @property
    def system_info(self):
        return self._system_info

    @property
    def software_info(self):
        return self._software_info

    @property
    def hello_info(self):
        return self._hello_info

    @property
    def sound_output(self):
        return self._sound_output

    @property
    def picture_settings(self):
        return self._picture_settings

    @property
    def is_on(self):
        state = self._power_state.get("state")
        if state == "Unknown":
            # fallback to current app id for some older webos versions which don't support explicit power state
            if self._current_appId in [None, ""]:
                return False
            else:
                return True
        elif state in [None, "Power Off", "Suspend", "Active Standby"]:
            return False
        else:
            return True

    @property
    def is_screen_on(self):
        if self.is_on:
            return self._power_state.get("state") != "Screen Off"
        return False

    async def register_state_update_callback(self, callback):
        self.state_update_callbacks.append(callback)
        if self.doStateUpdate:
            await callback(self)

    def unregister_state_update_callback(self, callback):
        if callback in self.state_update_callbacks:
            self.state_update_callbacks.remove(callback)

    def clear_state_update_callbacks(self):
        self.state_update_callbacks = []

    async def do_state_update_callbacks(self):
        callbacks = set()
        for callback in self.state_update_callbacks:
            callbacks.add(callback(self))

        if callbacks:
            await asyncio.gather(*callbacks)

    async def set_power_state(self, payload):
        self._power_state = {"state": payload.get("state", "Unknown")}

        if not self.is_on:
            await self.disconnect()
        elif self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_current_app_state(self, appId):
        """Set current app state variable.  This function also handles subscriptions to current channel and channel list, since the current channel subscription can only succeed when Live TV is running, and the channel list subscription can only succeed after channels have been configured."""
        self._current_appId = appId

        if self._channels is None:
            try:
                await self.subscribe_channels(self.set_channels_state)
            except PyLGTVCmdException:
                pass

        if appId == "com.webos.app.livetv" and self._current_channel is None:
            try:
                await self.subscribe_current_channel(self.set_current_channel_state)
            except PyLGTVCmdException:
                pass

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_muted_state(self, muted):
        self._muted = muted

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_volume_state(self, volume):
        self._volume = volume

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_channels_state(self, channels):
        self._channels = channels

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_current_channel_state(self, channel):
        """Set current channel state variable.  This function also handles the channel info subscription, since that call may fail if channel information is not available when it's called."""
        self._current_channel = channel

        if self._channel_info is None:
            try:
                await self.subscribe_channel_info(self.set_channel_info_state)
            except PyLGTVCmdException:
                pass

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_channel_info_state(self, channel_info):
        self._channel_info = channel_info

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_apps_state(self, payload):
        apps = payload.get("launchPoints")
        if apps is not None:
            self._apps = {}
            for app in apps:
                self._apps[app["id"]] = app
        else:
            change = payload["change"]
            app_id = payload["id"]
            if change == "removed":
                del self._apps[app_id]
            else:
                self._apps[app_id] = payload

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_inputs_state(self, extinputs):
        self._extinputs = {}
        for extinput in extinputs:
            self._extinputs[extinput["appId"]] = extinput

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_sound_output_state(self, sound_output):
        self._sound_output = sound_output

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    async def set_picture_settings_state(self, picture_settings):
        if isinstance(self._picture_settings, dict) and isinstance(picture_settings, dict):
            self._picture_settings.update(picture_settings)
        else:
            self._picture_settings = picture_settings

        if self.state_update_callbacks and self.doStateUpdate:
            await self.do_state_update_callbacks()

    # low level request handling

    async def command(self, request_type, uri, payload=None, uid=None):
        """Build and send a command."""
        if uid is None:
            uid = self.command_count
            self.command_count += 1

        if payload is None:
            payload = {}

        message = {
            "id": uid,
            "type": request_type,
            "uri": f"ssap://{uri}",
            "payload": payload,
        }

        if self.connection is None:
            raise PyLGTVCmdException("Not connected, can't execute command.")

        await self.connection.send(json.dumps(message))

    async def request(self, uri, payload=None, cmd_type="request", uid=None):
        """Send a request and wait for response."""
        if uid is None:
            uid = self.command_count
            self.command_count += 1

        res = asyncio.Future()
        self.futures[uid] = res

        try:
            await self.command(cmd_type, uri, payload, uid)
        except (asyncio.CancelledError, PyLGTVCmdException):
            del self.futures[uid]
            raise

        try:
            response = await res
        except asyncio.CancelledError:
            if uid in self.futures:
                del self.futures[uid]
            raise

        del self.futures[uid]

        payload = response.get("payload")
        if payload is None:
            raise PyLGTVCmdException(f"Invalid request response {response}")

        returnValue = payload.get("returnValue") or payload.get("subscribed")

        if response.get("type") == "error":
            error = response.get("error")
            if error == "404 no such service or method":
                raise PyLGTVServiceNotFoundError(error)
            else:
                raise PyLGTVCmdError(response)
        elif returnValue is None:
            raise PyLGTVCmdException(f"Invalid request response {response}")
        elif not returnValue:
            raise PyLGTVCmdException(f"Request failed with response {response}")

        return payload

    async def subscribe(self, callback, uri, payload=None):
        """Subscribe to updates."""
        uid = self.command_count
        self.command_count += 1
        self.callbacks[uid] = callback

        try:
            return await self.request(
                uri, payload=payload, cmd_type="subscribe", uid=uid
            )
        except Exception:
            del self.callbacks[uid]
            raise

    async def input_command(self, message):
        inputws = None
        try:
            # open additional connection needed to send button commands
            # the url is dynamically generated and returned from the ep.INPUT_SOCKET
            # endpoint on the main connection
            if self.input_connection is None:
                sockres = await self.request(ep.INPUT_SOCKET)
                inputsockpath = sockres.get("socketPath")
                inputws = await asyncio.wait_for(
                    websockets.connect(
                        inputsockpath,
                        ping_interval=None,
                        close_timeout=self.timeout_connect,
                    ),
                    timeout=self.timeout_connect,
                )

                if self.ping_interval is not None and self.ping_timeout is not None:
                    self.handler_tasks.add(asyncio.create_task(self.ping_handler(inputws)))

                self.input_connection = inputws

            if self.input_connection is None:
                raise PyLGTVCmdException("Couldn't execute input command.")

            await self.input_connection.send(message)

        except Exception as ex:
            if not self.connect_result.done():
                self.connect_result.set_exception(ex)

    # high level request handling

    async def button(self, name, checkValid=True):
        """Send button press command."""
        if checkValid and str(name) not in btn.BUTTONS:
            raise ValueError(
                f"button {name} is not valid, use checkValid=False to try a new one"
            )

        message = f"type:button\nname:{name}\n\n"
        await self.input_command(message)

    async def move(self, dx, dy, down=0):
        """Send cursor move command."""
        message = f"type:move\ndx:{dx}\ndy:{dy}\ndown:{down}\n\n"
        await self.input_command(message)

    async def click(self):
        """Send cursor click command."""
        message = f"type:click\n\n"
        await self.input_command(message)

    async def scroll(self, dx, dy):
        """Send scroll command."""
        message = f"type:scroll\ndx:{dx}\ndy:{dy}\n\n"
        await self.input_command(message)

    async def send_message(self, message, icon_path=None):
        """Show a floating message."""
        icon_encoded_string = ""
        icon_extension = ""

        if icon_path is not None:
            icon_extension = os.path.splitext(icon_path)[1][1:]
            with open(icon_path, "rb") as icon_file:
                icon_encoded_string = base64.b64encode(icon_file.read()).decode("ascii")

        return await self.request(
            ep.SHOW_MESSAGE,
            {
                "message": message,
                "iconData": icon_encoded_string,
                "iconExtension": icon_extension,
            },
        )

    async def get_power_state(self):
        """Get current power state."""
        return await self.request(ep.GET_POWER_STATE)

    async def subscribe_power(self, callback):
        """Subscribe to current power state."""
        return await self.subscribe(callback, ep.GET_POWER_STATE)

    # Apps
    async def get_apps(self, jsonOutput=False):
        """Return all apps."""
        res = await self.request(ep.GET_APPS)
        return self.__output_result(res.get("launchPoints"), jsonOutput)

    async def subscribe_apps(self, callback):
        """Subscribe to changes in available apps."""
        return await self.subscribe(callback, ep.GET_APPS)

    async def get_apps_all(self, jsonOutput=False):
        """Return all apps, including hidden ones."""
        res = await self.request(ep.GET_APPS_ALL)
        return self.__output_result(res.get("apps"), jsonOutput)

    async def get_current_app(self):
        """Get the current app id."""
        res = await self.request(ep.GET_CURRENT_APP_INFO)
        return res.get("appId")

    async def subscribe_current_app(self, callback):
        """Subscribe to changes in the current app id."""
        async def current_app(payload):
            await callback(payload.get("appId"))

        return await self.subscribe(current_app, ep.GET_CURRENT_APP_INFO)

    async def launch_app(self, app):
        """Launch an app."""
        return await self.request(ep.LAUNCH, {"id": app})

    async def launch_app_with_params(self, app, params):
        """Launch an app with parameters."""
        return await self.request(ep.LAUNCH, {"id": app, "params": params})

    async def launch_app_with_content_id(self, app, contentId):
        """Launch an app with contentId."""
        return await self.request(ep.LAUNCH, {"id": app, "contentId": contentId})

    async def close_app(self, app):
        """Close the current app."""
        return await self.request(ep.LAUNCHER_CLOSE, {"id": app})

    # Services
    async def get_services(self, jsonOutput=False):
        """Get all services."""
        res = await self.request(ep.GET_SERVICES)
        return self.__output_result(res.get("services"), jsonOutput)

    async def get_software_info(self, jsonOutput=False):
        """Return the current software status."""
        res = await self.request(ep.GET_SOFTWARE_INFO)
        return self.__output_result(res, jsonOutput)

    async def get_system_info(self, jsonOutput=False):
        """Return the system information."""
        res = await self.request(ep.GET_SYSTEM_INFO)
        return self.__output_result(res, jsonOutput)

    async def get_hello_info(self, jsonOutput=False):
        """Return hello information."""
        return self.__output_result(self._hello_info, jsonOutput)

    async def power_off(self):
        """Power off TV."""

        # protect against turning tv back on if it is off
        power_state = await self.get_power_state()
        self._power_state = {"state": power_state.get("state", "Unknown")}

        if not self.is_on:
            return

        # if tv is shutting down and standby+ option is not enabled,
        # response is unreliable, so don't wait for one,
        await self.command("request", ep.POWER_OFF)

    async def power_on(self):
        """Power on TV."""
        return await self.request(ep.POWER_ON)

    async def turn_screen_off(self, webos_ver=""):
        """Turn TV Screen off. standbyMode values: 'active' or 'passive',
        passive cannot turn screen back on, need to pull TV plug.
        """
        epName = f"TURN_OFF_SCREEN_WO{webos_ver}" if webos_ver else "TURN_OFF_SCREEN"

        if not hasattr(ep, epName):
            raise ValueError(f"there's no {epName} endpoint")

        return await self.request(getattr(ep, epName), {"standbyMode": "active"})

    async def turn_screen_on(self, webos_ver=""):
        """Turn TV Screen on. standbyMode values: 'active' or 'passive',
        passive cannot turn screen back on, need to pull TV plug.
        """
        epName = f"TURN_ON_SCREEN_WO{webos_ver}" if webos_ver else "TURN_ON_SCREEN"

        if not hasattr(ep, epName):
            raise ValueError(f"there's no {epName} endpoint")

        return await self.request(getattr(ep, epName), {"standbyMode": "active"})

    # 3D Mode
    async def turn_3d_on(self):
        """Turn 3D on."""
        return await self.request(ep.SET_3D_ON)

    async def turn_3d_off(self):
        """Turn 3D off."""
        return await self.request(ep.SET_3D_OFF)

    # Inputs
    async def get_inputs(self, jsonOutput=False):
        """Get all inputs."""
        res = await self.request(ep.GET_INPUTS)
        return self.__output_result(res.get("devices"), jsonOutput)

    async def subscribe_inputs(self, callback):
        """Subscribe to changes in available inputs."""
        async def inputs(payload):
            await callback(payload.get("devices"))

        return await self.subscribe(inputs, ep.GET_INPUTS)

    async def get_input(self):
        """Get current input."""
        return await self.get_current_app()

    async def set_input(self, input):
        """Set the current input."""
        return await self.request(ep.SET_INPUT, {"inputId": input})

    # Audio
    async def get_audio_status(self):
        """Get the current audio status"""
        return await self.request(ep.GET_AUDIO_STATUS)

    async def get_muted(self):
        """Get mute status."""
        status = await self.get_audio_status()
        return status.get("mute")

    async def subscribe_muted(self, callback):
        """Subscribe to changes in the current mute status."""
        async def muted(payload):
            await callback(payload.get("mute"))

        return await self.subscribe(muted, ep.GET_AUDIO_STATUS)

    async def set_mute(self, mute):
        """Set mute."""
        return await self.request(ep.SET_MUTE, {"mute": mute})

    async def get_volume(self):
        """Get the current volume."""
        res = await self.request(ep.GET_VOLUME)
        return res.get("volumeStatus", res).get("volume")

    async def subscribe_volume(self, callback):
        """Subscribe to changes in the current volume."""
        async def volume(payload):
            await callback(payload.get("volumeStatus", payload).get("volume"))

        return await self.subscribe(volume, ep.GET_VOLUME)

    async def set_volume(self, volume):
        """Set volume."""
        volume = max(0, volume)
        return await self.request(ep.SET_VOLUME, {"volume": volume})

    async def volume_up(self):
        """Volume up."""
        return await self._volume_step(ep.VOLUME_UP)

    async def volume_down(self):
        """Volume down."""
        return await self._volume_step(ep.VOLUME_DOWN)

    async def _volume_step(self, endpoint):
        """Volume step and conditionally sleep afterwards if a consecutive volume step shouldn't be possible to perform immediately after."""
        if (
            self.sound_output in SOUND_OUTPUTS_TO_DELAY_CONSECUTIVE_VOLUME_STEPS
            and self._volume_step_delay is not None
        ):
            async with self._volume_step_lock:
                response = await self.request(endpoint)
                await asyncio.sleep(self._volume_step_delay.total_seconds())
                return response
        else:
            return await self.request(endpoint)

    # TV Channel
    async def channel_up(self):
        """Channel up."""
        return await self.request(ep.TV_CHANNEL_UP)

    async def channel_down(self):
        """Channel down."""
        return await self.request(ep.TV_CHANNEL_DOWN)

    async def get_channels(self, jsonOutput=False):
        """Get list of tv channels."""
        res = await self.request(ep.GET_TV_CHANNELS)
        return self.__output_result(res.get("channelList"), jsonOutput)

    async def subscribe_channels(self, callback):
        """Subscribe to list of tv channels."""
        async def channels(payload):
            await callback(payload.get("channelList"))

        return await self.subscribe(channels, ep.GET_TV_CHANNELS)

    async def get_current_channel(self):
        """Get the current tv channel."""
        return await self.request(ep.GET_CURRENT_CHANNEL)

    async def subscribe_current_channel(self, callback):
        """Subscribe to changes in the current tv channel."""
        return await self.subscribe(callback, ep.GET_CURRENT_CHANNEL)

    async def get_channel_info(self, jsonOutput=False):
        """Get the current channel info."""
        res = await self.request(ep.GET_CHANNEL_INFO)
        return self.__output_result(res, jsonOutput)

    async def subscribe_channel_info(self, callback):
        """Subscribe to current channel info."""
        return await self.subscribe(callback, ep.GET_CHANNEL_INFO)

    async def set_channel(self, channel):
        """Set the current channel."""
        return await self.request(ep.SET_CHANNEL, {"channelId": channel})

    async def get_sound_output(self):
        """Get the current audio output."""
        res = await self.request(ep.GET_SOUND_OUTPUT)
        return res.get("soundOutput")

    async def subscribe_sound_output(self, callback):
        """Subscribe to changes in current audio output."""
        async def sound_output(payload):
            await callback(payload.get("soundOutput"))

        return await self.subscribe(sound_output, ep.GET_SOUND_OUTPUT)

    async def change_sound_output(self, output):
        """Change current audio output."""
        return await self.request(ep.CHANGE_SOUND_OUTPUT, {"output": output})

    # Media control
    async def play(self):
        """Play media."""
        return await self.request(ep.MEDIA_PLAY)

    async def pause(self):
        """Pause media."""
        return await self.request(ep.MEDIA_PAUSE)

    async def stop(self):
        """Stop media."""
        return await self.request(ep.MEDIA_STOP)

    async def close(self):
        """Close media."""
        return await self.request(ep.MEDIA_CLOSE)

    async def rewind(self):
        """Rewind media."""
        return await self.request(ep.MEDIA_REWIND)

    async def fast_forward(self):
        """Fast Forward media."""
        return await self.request(ep.MEDIA_FAST_FORWARD)

    # Keys
    async def send_enter_key(self):
        """Send enter key."""
        return await self.request(ep.SEND_ENTER)

    async def send_delete_key(self):
        """Send delete key."""
        return await self.request(ep.SEND_DELETE)

    # Text entry
    async def insert_text(self, text, replace=False):
        """Insert text into field, optionally replace existing text."""
        return await self.request(ep.INSERT_TEXT, {"text": text, "replace": replace})

    # Web
    async def open_url(self, url):
        """Open URL."""
        return await self.request(ep.OPEN, {"target": url})

    async def close_web(self):
        """Close web app."""
        return await self.request(ep.CLOSE_WEB_APP)

    async def luna_request(self, uri, params):
        """luna api call."""
        # n.b. this is a hack which abuses the alert API
        # to call the internal luna API which is otherwise
        # not exposed through the websocket interface
        # An important limitation is that any returned
        # data is not accessible

        # set desired action for click, fail and close
        # for redundancy/robustness

        lunauri = f"luna://{uri}"

        buttons = [{"label": "", "onClick": lunauri, "params": params}]
        payload = {
            "message": " ",
            "buttons": buttons,
            "onclose": {"uri": lunauri, "params": params},
            "onfail": {"uri": lunauri, "params": params},
        }

        ret = await self.request(ep.CREATE_ALERT, payload)
        alertId = ret.get("alertId")
        if alertId is None:
            raise PyLGTVCmdException("Invalid alertId")

        return await self.request(ep.CLOSE_ALERT, payload={"alertId": alertId})

    async def input_button(self):
        """Input button."""
        return await self.luna_request(ep.LUNA_SHOW_INPUT_PICKER, {})

    async def set_device_info(self, input, icon, label):
        """Set device info. It can be used to switch between PC and non-PC modes.

        Inputs: "HDMI_1", "HDMI_2", "HDMI_3", "HDMI_4"
        Icons:  "HDMI_1", "HDMI_2", "HDMI_3", "HDMI_4", "satellite", "settopbox",
                "dvd", "bluray", "hometheater", "gameconsole",
                "streamingbox", "camera", "mobile", "pc"
        Labels: "HDMI 1", "HDMI 2", "HDMI 3", "HDMI 4", "Satellite", "Set-Top Box",
                "DVD Player", "Blu-ray Player", "Home Theatre", "Game Console",
                "Streaming Box", "Generic Camera", "Mobile Device", "PC"
        """

        params = {"id": input, "icon": f"{icon}.png", "label": label}

        return await self.luna_request(ep.LUNA_SET_DEVICE_INFO, params)

    async def set_current_picture_mode(self, pic_mode, category="picture"):
        """Set picture mode for current category, input, dynamic range and 3d mode (OLED C1).

        Known picture modes are: cinema, eco, expert1, expert2, game,
        normal, photo, sports, filmMaker, vivid, hdrCinema,
        hdrCinemaBright, hdrExternal, hdrGame, hdrStandard, hdrFilmMaker,
        hdrVivid, dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon,
        dolbyHdrGame, dolbyHdrStandard, dolbyHdrVivid, dolbyStandard

        Known categories are: picture, aiPicture

        Likely not all modes are valid for all tv models.
        """

        params = {"category": category, "settings": {"pictureMode": pic_mode}}

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def set_picture_mode(
        self, pic_mode, tv_input, dynamic_range="sdr", stereoscopic="2d", category="picture"
    ):
        """Set picture mode for specific category, input, dynamic range and 3d mode (OLED C1).

        Known picture modes are: cinema, eco, expert1, expert2, game,
        normal, photo, sports, filmMaker, vivid,  hdrCinema,
        hdrCinemaBright, hdrExternal, hdrGame, hdrStandard, hdrFilmMaker,
        hdrVivid, dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon,
        dolbyHdrGame, dolbyHdrStandard, dolbyHdrVivid, dolbyStandard

        Known inputs are: atv, av1, av2, camera, comp1, comp2, comp3,
        default, dtv, gallery, hdmi1, hdmi2, hdmi3, hdmi4,
        hdmi1_pc, hdmi2_pc, hdmi3_pc, hdmi4_pc, ip, movie,
        photo, pictest, rgb, scart, smhl

        Known dynamic range modes are: sdr, sdrALLM, hdr, hdrALLM,
        technicolorHdr, technicolorHdrALLM, dolbyHdr, dolbyHdrALLM

        Known stereoscopic modes are: 2d, 3d

        Known categories are: picture, aiPicture

        Likely not all inputs and modes are valid for all tv models.
        """

        params = {
            "category": f"{category}${tv_input}.x.{stereoscopic}.{dynamic_range}",
            "settings": {"pictureMode": pic_mode},
        }

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def set_current_picture_settings(self, settings, category="picture"):
        """Set picture settings for current category, picture mode, input, dynamic range and 3d mode.

        A possible list of settings and OLED C1 example values are below
        (not all settings are applicable for all modes and/or tv models):
        /etc/palm/defaultSettings.json

        Category: aiPicture
        -------------------

        "ai_Brightness": "off",
        "ai_Genre": "off",
        "ai_Picture": "off"

        Category: picture
        -----------------

        "adjustingLuminance": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "adjustingLuminance10pt": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "ambientLightCompensation": "off",
        "backlight": "80",
        "blackLevel": {
            "ntsc": "auto",
            "ntsc443": "auto",
            "pal": "auto",
            "pal60": "auto",
            "palm": "auto",
            "paln": "auto",
            "secam": "auto",
            "unknown": "auto"
        },
        "brightness": "50",
        "color": "50",
        "colorFilter": "off",
        "colorGamut": "auto",
        "colorManagementColorSystem": "red",
        "colorManagementHueBlue": "0",
        "colorManagementHueCyan": "0",
        "colorManagementHueGreen": "0",
        "colorManagementHueMagenta": "0",
        "colorManagementHueRed": "0",
        "colorManagementHueYellow": "0",
        "colorManagementLuminanceBlue": "0",
        "colorManagementLuminanceCyan": "0",
        "colorManagementLuminanceGreen": "0",
        "colorManagementLuminanceMagenta": "0",
        "colorManagementLuminanceRed": "0",
        "colorManagementLuminanceYellow": "0",
        "colorManagementSaturationBlue": "0",
        "colorManagementSaturationCyan": "0",
        "colorManagementSaturationGreen": "0",
        "colorManagementSaturationMagenta": "0",
        "colorManagementSaturationRed": "0",
        "colorManagementSaturationYellow": "0",
        "colorTemperature": "-50",
        "contrast": "80",
        "dynamicColor": "off",
        "dynamicContrast": "off",
        "edgeEnhancer": "on",
        "expertPattern": "off",
        "externalPqlDbType": "none",
        "gamma": "high2",
        "grassColor": "0",
        "hPosition": "0",
        "hSharpness": "10",
        "hSize": "0",
        "hdrDynamicToneMapping": "on",
        "localDimming": "medium",
        "motionEyeCare": "off",
        "motionPro": "off",
        "motionProOLED": "off",
        "mpegNoiseReduction": "off",
        "noiseReduction": "off",
        "peakBrightness": "off",
        "pictureTempKey": "off",
        "realCinema": "on",
        "sharpness": "10",
        "skinColor": "0",
        "skyColor": "0",
        "smoothGradation": "off",
        "superResolution": "off",
        "tint": "0",
        "truMotionBlur": "10",
        "truMotionJudder": "0",
        "truMotionMode": "user",
        "vPosition": "0",
        "vSharpness": "10",
        "vSize": "0",
        "whiteBalanceApplyAllInputs": "off",
        "whiteBalanceBlue": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "whiteBalanceBlue10pt": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "whiteBalanceBlueGain": "0",
        "whiteBalanceBlueOffset": "0",
        "whiteBalanceCodeValue": "21",
        "whiteBalanceCodeValue10pt": "9",
        "whiteBalanceColorTemperature": "warm2",
        "whiteBalanceGreen": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "whiteBalanceGreen10pt": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "whiteBalanceGreenGain": "0",
        "whiteBalanceGreenOffset": "0",
        "whiteBalanceIre": "100",
        "whiteBalanceIre10pt": "100",
        "whiteBalanceLuminance": "130",
        "whiteBalanceMethod": "2",
        "whiteBalancePattern": "outer",
        "whiteBalancePoint": "high",
        "whiteBalanceRed": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "whiteBalanceRed10pt": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "whiteBalanceRedGain": "0",
        "whiteBalanceRedOffset": "0",
        "xvycc": "auto"

        """

        params = {"category": category, "settings": settings}

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def set_picture_settings(
        self, settings, pic_mode, tv_input, stereoscopic="2d", category="picture"
    ):
        """Set picture settings for specific category, picture mode, input, and 3d mode."""

        params = {
            "category": f"{category}${tv_input}.{pic_mode}.{stereoscopic}.x",
            "settings": settings,
        }

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def set_other_settings(self, settings):
        """Set other settings.

        A possible list of settings and OLED C1 example values are below
        (not all settings are applicable for all tv models/firmwares):
        /etc/palm/defaultSettings.json

        "amazonHotkeyIsActive": true,
        "appReturn": "",
        "blackStabilizer": 13,
        "blueLight": "off",
        "care365": {
            "accountName": "",
            "accountNumber": "",
            "userAgreementLocation": "",
            "userAgreementVersion": "",
            "value": "off"
        },
        "colorimetry": "auto",
        "colorimetryHDMI1": "auto",
        "colorimetryHDMI2": "auto",
        "colorimetryHDMI3": "auto",
        "colorimetryHDMI4": "auto",
        "cursorAutoRemover": "on",
        "dolbyVSVDBVer": "v2",
        "dolbyVSVDBVerHDMI1": "v2",
        "dolbyVSVDBVerHDMI2": "v2",
        "dolbyVSVDBVerHDMI3": "v2",
        "dolbyVSVDBVerHDMI4": "v2",
        "enableQuickGame": "on",
        "eotf": "auto",
        "eotfHDMI1": "auto",
        "eotfHDMI2": "auto",
        "eotfHDMI3": "auto",
        "eotfHDMI4": "auto",
        "epgRowCount": "1",
        "flickerPatternCtrl": false,
        "freesync": "off",
        "freesyncLCDHDMI1": "off",
        "freesyncLCDHDMI2": "off",
        "freesyncLCDHDMI3": "off",
        "freesyncLCDHDMI4": "off",
        "freesyncOLEDHDMI1": "off",
        "freesyncOLEDHDMI2": "off",
        "freesyncOLEDHDMI3": "off",
        "freesyncOLEDHDMI4": "off",
        "freesyncSupport": "off",
        "freeviewTnCPopup": "off",
        "gameGenre": "Standard",
        "gameMode": {
            "hdmi1": "off",
            "hdmi2": "off",
            "hdmi3": "off",
            "hdmi4": "off"
        },
        "gameOptimization": "on",
        "gameOptimizationHDMI1": "on",
        "gameOptimizationHDMI2": "on",
        "gameOptimizationHDMI3": "on",
        "gameOptimizationHDMI4": "on",
        "gameUIColor": "violet",
        "hdmiPcMode": {
            "hdmi1": false,
            "hdmi2": false,
            "hdmi3": false,
            "hdmi4": false
        },
        "homeEffectVersion": [
            {
                "id": "Christmas",
                "version": 1.0
            },
            {
                "id": "Halloween",
                "version": 1.0
            }
        ],
        "illuminanceThreshold": 0,
        "inputOptimization": "auto",
        "isFirstCapture": "true",
        "isfUpdated": "false",
        "lgLogoDisplay": "on",
        "lowLevelAdjustment": 0,
        "mapping_info": [
            {
                "movies": {
                    "app_id": null,
                    "isActive": false,
                    "launch_param": null
                }
            },
            {
                "netflix": {
                    "app_id": "netflix",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "amazon": {
                    "app_id": "amazon",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "ivi": {
                    "app_id": "ivi",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "disneyplus": {
                    "app_id": "com.disney.disneyplus-prod",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "lgchannels": {
                    "app_id": "com.webos.app.lgchannels",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "rakutentv": {
                    "app_id": "ui30",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "globoplay": {
                    "app_id": "globoplaywebos",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "okko": {
                    "app_id": "yota.play",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "kinopoisk": {
                    "app_id": "com.685631.3411",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "watchaplay": {
                    "app_id": "com.frograms.watchaplay.webos",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "unext": {
                    "app_id": "u.next",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "hotstar": {
                    "app_id": "hotstar",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "new": {
                    "app_id": null,
                    "isActive": false,
                    "launch_param": null
                }
            }
        ],
        "masterLuminanceLevel": "540nit",
        "masteringColor": "auto",
        "masteringColorHDMI1": "auto",
        "masteringColorHDMI2": "auto",
        "masteringColorHDMI3": "auto",
        "masteringColorHDMI4": "auto",
        "masteringPeak": "auto",
        "masteringPeakHDMI1": "auto",
        "masteringPeakHDMI2": "auto",
        "masteringPeakHDMI3": "auto",
        "masteringPeakHDMI4": "auto",
        "maxCLL": "auto",
        "maxCLLHDMI1": "auto",
        "maxCLLHDMI2": "auto",
        "maxCLLHDMI3": "auto",
        "maxCLLHDMI4": "auto",
        "maxFALL": "auto",
        "maxFALLHDMI1": "auto",
        "maxFALLHDMI2": "auto",
        "maxFALLHDMI3": "auto",
        "maxFALLHDMI4": "auto",
        "netflixHotkeyIsActive": true,
        "newKey": "on",
        "quickSettingsMenuList": [
            "QuickSettings_picture_button",
            "QuickSettings_soundMode_button",
            "QuickSettings_soundOut_button",
            "QuickSettings_game_button",
            "QuickSettings_timer_button",
            "QuickSettings_network_button",
            "QuickSettings_menu_button"
        ],
        "screenRemoteAutoShow": "true",
        "screenRemoteExpanded": "false",
        "screenRemotePosition": "right",
        "simplinkAutoPowerOn": "on",
        "simplinkEnable": "off",
        "supportAirplay": false,
        "supportBnoModel": false,
        "ueiEnable": "off",
        "uhdDeepColor": "off",
        "uhdDeepColor8kHDMI1": "off",
        "uhdDeepColor8kHDMI2": "off",
        "uhdDeepColor8kHDMI3": "off",
        "uhdDeepColor8kHDMI4": "off",
        "uhdDeepColorAutoStatusHDMI1": "none",
        "uhdDeepColorAutoStatusHDMI2": "none",
        "uhdDeepColorAutoStatusHDMI3": "none",
        "uhdDeepColorAutoStatusHDMI4": "none",
        "uhdDeepColorHDMI1": "off",
        "uhdDeepColorHDMI2": "off",
        "uhdDeepColorHDMI3": "off",
        "uhdDeepColorHDMI4": "off",
        "weatherAllowed": false,
        "whiteStabilizer": 13

        """

        params = {"category": "other", "settings": settings}

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def set_option_settings(self, settings):
        """Set option settings.

        A possible list of settings and OLED C1 example values are below
        (not all settings are applicable for all tv models/firmwares):
        /etc/palm/defaultSettings.json

        "IPControlSecureKey": "",
        "_3dModeEstreamer": "off",
        "additionalAudioSelection": "none",
        "addressInfo": [
            "not_defined",
            "not_defined",
            "not_defined",
            "not_defined"
        ],
        "adjustments": {
            "blackAndWhite": "off",
            "colorInversion": "off"
        },
        "animationGuide": "on",
        "appInstallDevice": {
            "deviceId": "",
            "driveId": ""
        },
        "appUpdateMode": "manual",
        "audioGuidance": "off",
        "audioGuidancePitch": "medium",
        "audioGuidanceSpeed": "medium",
        "audioGuidanceVolume": "medium",
        "autoComplete": false,
        "autoSmartServiceCountry": "on",
        "avatar": "off",
        "backupPsm": {
            "backupPsm2d": "hdrStandard",
            "backupPsm3d": "hdrStandard"
        },
        "backupPsmDolby": {
            "backupPsm2d": "dolbyHdrDark",
            "backupPsm3d": "dolbyHdrDark"
        },
        "baloonHelp": "on",
        "bannerPosition": "none",
        "broadcastInfoNoti": "on",
        "channelplus": "off",
        "channelplusPopup": "off",
        "cicNumber": [
            {
                "country": "default",
                "number": "none",
                "shortName": "default"
            }
        ],
        "country": "other",
        "countryGroup": "UNDEFINED",
        "countryRegion": "other",
        "curDemoFile": "undefined",
        "dataService": "mheg",
        "dbgLogUpload": false,
        "demoFileList": "undefined",
        "demoMode": "on",
        "displayMusicWidget": true,
        "eStreamerPosition": "all",
        "emergencyAlert": "on",
        "enableIpControl": "off",
        "enableSDDP": "off",
        "enableToastPopup": "off",
        "enabling3dSettingsMenu": "off",
        "epgPipMode": "off",
        "estreamerMinimalMode": "off",
        "estreamerStatus": "off",
        "faultLogUpload": false,
        "firstTvSignalStatus": "undefined",
        "focusedItemEnlarged": "off",
        "freeviewMode": "off",
        "freeviewplay": "off",
        "googleAssistantTTS": "on",
        "graphicSharpnessLevel": 0,
        "hbbTV": "off",
        "hbbTvDeviceId": "on",
        "hbbTvDnt": "off",
        "hddEcoMode": "on",
        "helpOnSettings": "on",
        "highContrast": "off",
        "hybridCast": "off",
        "inputDevicesSupportStatus": {
            "keyboard": true,
            "motionSensor": true,
            "pointer": true,
            "touch": true,
            "voice": true
        },
        "interactive-service": "off",
        "interactivity": "off",
        "irBlaster": "off",
        "ismMethod": "normal",
        "japanCitySelection": "Tokyo",
        "liveMenuLaunched": false,
        "livePlus": "off",
        "localeCountryGroup": "UNDEFINED",
        "logoLight": "low",
        "magicNum1": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum2": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum3": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum4": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum5": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum6": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum7": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum8": {
            "id": "",
            "override": false,
            "params": {}
        },
        "magicNum9": {
            "id": "com.webos.app.self-diagnosis",
            "override": true,
            "params": {
                "from": "magicNum"
            }
        },
        "magicNumHelpShow": true,
        "menuLanguage": "eng",
        "menuTransparency": "on",
        "mhegGuide": "off",
        "miracastOverlayAdRecovery": "off",
        "miracastOverlayStatus": "off",
        "modeSelectFlag": "off",
        "motionRecognition": "off",
        "multiChannelAudio": "on",
        "multiViewStatus": "off",
        "ohtv": "on",
        "orbit": "off",
        "password_ipcontrol": "828",
        "phlCitySelection": "0",
        "pointerAlignment": "off",
        "pointerShape": "auto",
        "pointerSize": "medium",
        "pointerSpeed": "normal",
        "powerOnLight": "off",
        "promotionOriginEnd": "undefined",
        "promotionOriginStart": "undefined",
        "promotionPeriodEnd": "0",
        "promotionPeriodStart": "0",
        "promotionStreamer": "off",
        "pstreamerUser": "off",
        "quickStartMode": "off",
        "screenOff": "off",
        "screenRotation": "off",
        "searchAppTTS": "off",
        "setId": 1,
        "smartServiceCountryCode2": "other",
        "smartServiceCountryCode3": "other",
        "smartSoundDemo": "on",
        "speakToTv": "off",
        "standByLight": "on",
        "storeHDR": "on",
        "storeLogo": "0",
        "storeMode": "home",
        "storeMode2": "on",
        "storeModeVideo": "off",
        "storeUsbAlarm": "off",
        "subdivisionCodeOfServiceCountry": "",
        "subtitleLanguageFirst": "eng",
        "subtitleLanguageSecond": "eng",
        "supplementaryAudio": "off",
        "syncMode": "off",
        "syncModeTvCondition": "none",
        "teletextLanguageFirst": "eng",
        "teletextLanguageSecond": "eng",
        "turnOnByVoice": "off",
        "usbBuiltInVideo": "on",
        "virtualKeyboardLanguage": [
            "en-US"
        ],
        "virtualSetTop": "off",
        "voiceRecognitionLanguage": "eng",
        "vsn": "N/A",
        "wakeUpword": "LGTV",
        "watchedListCollection": "on",
        "webOSPromotionVideo": "on",
        "zipcode": "not_defined"

        """

        params = {"category": "option", "settings": settings}

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def get_configs(self, keys=["tv.model.*"], jsonOutput=False):
        """Get config settings.

        A possible list of keys of OLED C1 are below (not all settings are applicable for all tv models):
        /etc/configd/layers

        airplay.*
        audio.*
        broadcast.*
        com.palm.app.firstuse.*
        com.palm.app.settings.*
        com.palm.app.store-demo.*
        com.webos.app.connectionwizard.*
        com.webos.app.factorywin.*
        com.webos.app.favshows.*
        com.webos.app.home.*
        com.webos.app.igallery.*
        com.webos.app.inputcommon.*
        com.webos.app.mediadiscovery.*
        com.webos.app.photovideo.*
        com.webos.app.quickinputpicker.*
        com.webos.app.quicksettings.*
        com.webos.app.systemmusic.*
        com.webos.app.tips.*
        com.webos.applicationManager.*
        com.webos.authenticationMethods.*
        com.webos.keyaction.*
        com.webos.memorymanager.*
        com.webos.service.airplay.*
        com.webos.service.arccontroller.*
        com.webos.service.attachedstoragemanager.*
        com.webos.service.cbox.*
        com.webos.service.datamigrator.*
        com.webos.service.config.*
        com.webos.service.eim.*
        com.webos.service.favoriteservice.*
        com.webos.service.fepg.*
        com.webos.service.hybridtv.*
        com.webos.service.iepg.*
        com.webos.service.ime.*
        com.webos.service.irdbmanager.*
        com.webos.service.livepick.*
        com.webos.service.miracast.*
        com.webos.service.miracasttx.*
        com.webos.service.msc.*
        com.webos.service.nlpmanager.*
        com.webos.service.nop.*
        com.webos.service.nudge.*
        com.webos.service.pdm.*
        com.webos.service.photorenderer.*
        com.webos.service.preloadmanager.*
        com.webos.service.rollingscreen.*
        com.webos.service.scd.*
        com.webos.service.time.*
        com.webos.service.tnm.*
        com.webos.service.tvpower.*
        com.webos.service.utp.*
        com.webos.service.voiceinput.*
        com.webos.service.voiceinput.*
        com.webos.service.wampluggable.hbbtv.*
        com.webos.surfacemanager.*
        dvr.*
        extinput-service.*
        inputMap.*
        mediaCapability.*
        miracast.*
        system.*
        tv.config.*
        tv.conti.*
        tv.hw.*
        tv.model.*
        tv.nyx.*
        tv.rmm.*

        """

        payload = {"configNames": keys}
        res = await self.request(ep.GET_CONFIGS, payload=payload)
        return self.__output_result(res, jsonOutput)

    async def set_configs(self, settings):
        """Set config settings.

        Example:

        "tv.model.motionProMode": "OLED Motion",
        "tv.model.motionProMode": "OLED Motion Pro"

        """

        params = {"configs": settings}

        return await self.luna_request(ep.LUNA_SET_CONFIGS, params)

    async def show_screen_saver(self):
        return await self.luna_request(ep.LUNA_TURN_ON_SCREEN_SAVER, {})

    async def get_system_settings(self, category="option", keys=["audioGuidance"], jsonOutput=False):
        """Get system settings.

        Most of the settings are not exposed via this call, OLED C1 valid settings:
        /usr/palm/services/com.webos.service.apiadapter/adapters/settings/valid-settings.js

        "twinTv": [
                "status",
                "role",
                "systemMode"
        ],
        "network": [
                "deviceName",
                "wolwowlOnOff",
                "bleAdvertisingOnOff"
        ],
        "option": [
                "audioGuidance",
                "country",
                "zipcode",
                "livePlus",
                "firstTvSignalStatus",
                "addressInfo",
                "phlCitySelection",
                "smartServiceCountryCode3",
                "syncMode",
                "storeMode",
                "localeCountryGroup",
                "japanCitySelection",
                "countryBroadcastSystem"
        ],
        "time": [
                "onTimerVolume",
                "timeZone"
        ],
        "picture": [
                "brightness",
                "backlight",
                "contrast",
                "color",
                "energySaving"
        ],
        "" : [
                "eulaStatus",
                "eulaInfoNetwork",
                "mobileSetupStatus",
                "localeInfo"
        ],
        "other": [
                "simplinkEnable",
                "ueiEnable"
        ],
        "sound": [
                "avSync",
                "avSyncSpdif",
                "avSyncBypassInput",
                "eArcSupport",
                "soundOutput",
                "soundOutputDigital",
                "soundMode",
                "tvSetupConfiguration"
        ],
        "lock": [
                "parentalGuidance",
                "ziggoRaiting"
        ],
        "general": [
                "alwaysOn",
                "tvOnScreen",
                "tvInstallMethod",
                "powerOffBySCA3SystemChanged",
                "SCA3SystemCountry"
        ]

        """

        payload = {"category": category, "keys": keys}
        res = await self.request(ep.GET_SYSTEM_SETTINGS, payload=payload)
        return self.__output_result(res, jsonOutput)

    async def get_picture_settings(
        self, keys=["contrast", "backlight", "brightness", "color"], jsonOutput=False
    ):
        res = await self.get_system_settings("picture", keys)
        return self.__output_result(res["settings"], jsonOutput)

    async def subscribe_picture_settings(
        self, callback, keys=["contrast", "backlight", "brightness", "color"]
    ):
        async def settings(payload):
            await callback(payload.get("settings"))

        payload = {"category": "picture", "keys": keys}
        return await self.subscribe(settings, ep.GET_SYSTEM_SETTINGS, payload=payload)

    # Calibration

    if np:
        def calibration_support_info(self):
            if self._system_info is None:
                raise PyLGTVCmdException(f"System info is not available, -g command line switch is required.")

            info = {
                "lut1d": False,
                "lut3d_size": None,
                "custom_tone_mapping": False,
                "dv_config_type": None,
            }
            model_name = self._system_info["modelName"]
            if model_name.startswith("OLED") and len(model_name) > 7:
                model = model_name[6]
                year = int(model_name[7])
                if year >= 8:
                    info["lut1d"] = True
                    if model == "B":
                        info["lut3d_size"] = 17
                    else:
                        info["lut3d_size"] = 33
                if year == 8:
                    info["dv_config_type"] = 2018
                elif year == 9:
                    info["custom_tone_mapping"] = True
                    info["dv_config_type"] = 2019
            elif len(model_name) > 5:
                size = None
                try:
                    size = int(model_name[0:2])
                except ValueError:
                    pass
                if size:
                    modeltype = model_name[2]
                    modelyear = model_name[3]
                    modelseries = model_name[4]
                    modelnumber = model_name[5]

                    if modeltype == "S" and modelyear in ["K", "M"] and modelseries >= 8:
                        info["lut1d"] = True
                        if modelseries == 9 and modelnumber == 9:
                            info["lut3d_size"] = 33
                        else:
                            info["lut3d_size"] = 17
                        if modelyear == "K":
                            info["dv_config_type"] = 2018
                        elif modelyear == "M":
                            info["custom_tone_mapping"] = True
                            info["dv_config_type"] = 2019

            return info

        def validateCalibrationData(self, data, shape, dtype):
            if not isinstance(data, np.ndarray):
                raise TypeError(f"data must be of type ndarray but is instead {type(data)}")
            if data.shape != shape:
                raise ValueError(
                    f"data should have shape {shape} but instead has {data.shape}"
                )
            if data.dtype != dtype:
                raise TypeError(
                    f"numpy dtype should be {dtype} but is instead {data.dtype}"
                )

        async def calibration_request(self, command, picMode, data):
            dataenc = base64.b64encode(data.tobytes()).decode()

            payload = {
                "command": command,
                "data": dataenc,
                "dataCount": data.size,
                "dataOpt": 1,
                "dataType": CALIBRATION_TYPE_MAP[data.dtype.name],
                "profileNo": 0,
                "programID": 1,
            }
            if picMode is not None:
                payload["picMode"] = picMode

            return await self.request(ep.CALIBRATION, payload)

        async def start_calibration(self, picMode, data=DEFAULT_CAL_DATA):
            self.validateCalibrationData(data, (9,), np.float32)
            return await self.calibration_request(cal.CAL_START, picMode, data)

        async def end_calibration(self, picMode, data=DEFAULT_CAL_DATA):
            self.validateCalibrationData(data, (9,), np.float32)
            return await self.calibration_request(cal.CAL_END, picMode, data)

        async def upload_1d_lut(self, picMode, data=None):
            info = self.calibration_support_info()
            if not info["lut1d"]:
                model = self._system_info["modelName"]
                raise PyLGTVCmdException(
                    f"1D LUT Upload not supported by tv model {model}."
                )
            if data is None:
                data = await asyncio.get_running_loop().run_in_executor(None, unity_lut_1d)
            self.validateCalibrationData(data, (3, 1024), np.uint16)
            return await self.calibration_request(cal.UPLOAD_1D_LUT, picMode, data)

        async def upload_1d_lut_from_file(self, picMode, filename):
            ext = filename.split(".")[-1].lower()
            if ext == "cal":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_cal_file, filename
                )
            elif ext == "cube":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_cube_file, filename
                )
            else:
                raise ValueError(
                    f"Unsupported file format {ext} for 1D LUT.  Supported file formats are cal and cube."
                )

            return await self.upload_1d_lut(picMode, lut)

        async def upload_3d_lut(self, command, picMode, data):
            if command not in [cal.UPLOAD_3D_LUT_BT709, cal.UPLOAD_3D_LUT_BT2020]:
                raise PyLGTVCmdException(f"Invalid 3D LUT Upload command {command}.")
            info = self.calibration_support_info()
            lut3d_size = info["lut3d_size"]
            if not lut3d_size:
                model = self._system_info["modelName"]
                raise PyLGTVCmdException(
                    f"3D LUT Upload not supported by tv model {model}."
                )
            if data is None:
                data = await asyncio.get_running_loop().run_in_executor(
                    None, unity_lut_3d, lut3d_size
                )
            lut3d_shape = (lut3d_size, lut3d_size, lut3d_size, 3)
            self.validateCalibrationData(data, lut3d_shape, np.uint16)
            return await self.calibration_request(command, picMode, data)

        async def upload_3d_lut_bt709(self, picMode, data=None):
            return await self.upload_3d_lut(cal.UPLOAD_3D_LUT_BT709, picMode, data)

        async def upload_3d_lut_bt2020(self, picMode, data=None):
            return await self.upload_3d_lut(cal.UPLOAD_3D_LUT_BT2020, picMode, data)

        async def upload_3d_lut_from_file(self, command, picMode, filename):
            ext = filename.split(".")[-1].lower()
            if ext == "cube":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_cube_file, filename
                )
            else:
                raise ValueError(
                    f"Unsupported file format {ext} for 3D LUT.  Supported file formats are cube."
                )

            return await self.upload_3d_lut(command, picMode, lut)

        async def upload_3d_lut_bt709_from_file(self, picMode, filename):
            return await self.upload_3d_lut_from_file(
                cal.UPLOAD_3D_LUT_BT709, picMode, filename
            )

        async def upload_3d_lut_bt2020_from_file(self, picMode, filename):
            return await self.upload_3d_lut_from_file(
                cal.UPLOAD_3D_LUT_BT2020, picMode, filename
            )

        async def set_ui_data(self, command, picMode, value):
            if not (value >= 0 and value <= 100):
                raise ValueError

            data = np.array(value, dtype=np.uint16)
            return await self.calibration_request(command, picMode, data)

        async def set_brightness(self, picMode, value):
            return await self.set_ui_data(cal.BRIGHTNESS_UI_DATA, picMode, value)

        async def set_contrast(self, picMode, value):
            return await self.set_ui_data(cal.CONTRAST_UI_DATA, picMode, value)

        async def set_oled_light(self, picMode, value):
            return await self.set_ui_data(cal.BACKLIGHT_UI_DATA, picMode, value)

        async def set_color(self, picMode, value):
            return await self.set_ui_data(cal.COLOR_UI_DATA, picMode, value)

        async def set_1d_2_2_en(self, picMode, value=0):
            data = np.array(value, dtype=np.uint16)
            return await self.calibration_request(
                cal.ENABLE_GAMMA_2_2_TRANSFORM, picMode, data
            )

        async def set_1d_0_45_en(self, picMode, value=0):
            data = np.array(value, dtype=np.uint16)
            return await self.calibration_request(
                cal.ENABLE_GAMMA_0_45_TRANSFORM, picMode, data
            )

        async def set_bt709_3by3_gamut_data(
            self, picMode, data=np.identity(3, dtype=np.float32)
        ):
            self.validateCalibrationData(data, (3, 3), np.float32)
            return await self.calibration_request(cal.BT709_3BY3_GAMUT_DATA, picMode, data)

        async def set_bt2020_3by3_gamut_data(
            self, picMode, data=np.identity(3, dtype=np.float32)
        ):
            self.validateCalibrationData(data, (3, 3), np.float32)
            return await self.calibration_request(cal.BT2020_3BY3_GAMUT_DATA, picMode, data)

        async def set_dolby_vision_config_data(
            self, white_level=700.0, black_level=0.0, gamma=2.2, primaries=BT2020_PRIMARIES
        ):

            info = self.calibration_support_info()
            dv_config_type = info["dv_config_type"]
            if dv_config_type is None:
                model = self._system_info["modelName"]
                raise PyLGTVCmdException(
                    f"Dolby Vision Configuration Upload not supported by tv model {model}."
                )

            config = await asyncio.get_running_loop().run_in_executor(
                None,
                functools.partial(
                    create_dolby_vision_config,
                    version=dv_config_type,
                    white_level=white_level,
                    black_level=black_level,
                    gamma=gamma,
                    primaries=primaries,
                ),
            )

            data = np.frombuffer(config.encode(), dtype=np.uint8)
            return await self.calibration_request(
                command=cal.DOLBY_CFG_DATA, picMode=None, data=data
            )

        async def set_tonemap_params(
            self,
            picMode,
            luminance=700,
            mastering_peak_1=1000,
            rolloff_point_1=70,
            mastering_peak_2=4000,
            rolloff_point_2=60,
            mastering_peak_3=10000,
            rolloff_point_3=50,
        ):

            data = np.array(
                [
                    luminance,
                    mastering_peak_1,
                    rolloff_point_1,
                    mastering_peak_2,
                    rolloff_point_2,
                    mastering_peak_3,
                    rolloff_point_3,
                ],
                dtype=np.uint16,
            )

            return await self.calibration_request(cal.SET_TONEMAP_PARAM, picMode, data)

        async def ddc_reset(self, picMode, reset_1d_lut=True):
            if not isinstance(reset_1d_lut, bool):
                raise TypeError(
                    f"reset_1d_lut should be a bool, instead got {reset_1d_lut} of type {type(reset_1d_lut)}."
                )

            await self.set_1d_2_2_en(picMode)
            await self.set_1d_0_45_en(picMode)
            await self.set_bt709_3by3_gamut_data(picMode)
            await self.set_bt2020_3by3_gamut_data(picMode)
            await self.upload_3d_lut_bt709(picMode)
            await self.upload_3d_lut_bt2020(picMode)
            if reset_1d_lut:
                await self.upload_1d_lut(picMode)

            return True
