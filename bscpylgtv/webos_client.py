import asyncio
import base64
import copy
import functools
import json
import os
import ssl
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
from .constants import LUT3D_SIZES, DV_CONFIG_TYPES

if np:
    from . import cal_commands as cal
    from .constants import (
        BT2020_PRIMARIES,
        CALIBRATION_TYPE_MAP,
        SDR_PICTURE_MODES,
        HDR10_PICTURE_MODES,
        DV_PICTURE_MODES,
        DV_BLACK_LEVEL,
        DV_GAMMA,
        DV_CONFIG_FILENAME,
    )
    from .lut_tools import (
        create_dolby_vision_config,
        generate_dolby_vision_config,
        read_cal_file,
        read_cube_file,
        read_1dlut_file,
        read_3by3_gamut_file,
        read_3dlut_file,
        backup_lut_into_file,
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
        calibration_info=None,
        without_ssl=False,
        storage: StorageProto=None,
    ):
        """Initialize the client."""
        self.ip = ip
        self.port = (3000 if without_ssl else 3001)
        self.proto = ('ws' if without_ssl else 'wss')
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
        self._calibration_info = {}
        self._ssl_context = None
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
        if calibration_info and isinstance(calibration_info, dict):
            if "lut3d" in calibration_info and calibration_info["lut3d"] in LUT3D_SIZES:
                self._calibration_info['lut3d'] = LUT3D_SIZES[calibration_info["lut3d"]]
            if "dovi" in calibration_info and calibration_info["dovi"] in DV_CONFIG_TYPES:
                self._calibration_info['dovi'] = DV_CONFIG_TYPES[calibration_info["dovi"]]
        if not without_ssl:
            self._ssl_context = ssl.create_default_context()
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE

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
                    f"{self.proto}://{self.ip}:{self.port}",
                    ping_interval=None,
                    close_timeout=self.timeout_connect,
                    max_size=None,
                    ssl=self._ssl_context,
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
            self._calibration_info = {}
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
    def calibration_info(self):
        return self._calibration_info

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
                        ssl=self._ssl_context,
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

    async def get_calibration_info(self, jsonOutput=False):
        """Return calibration support information."""
        self.calibration_support_info()
        return self.__output_result(self._calibration_info, jsonOutput)

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

    async def take_screenshot(self, method="DISPLAY", format="JPG", width=960, height=540, path=""):
        """Take screenshot.
            method: DISPLAY (SCREEN), SCREEN_WITH_SOURCE_VIDEO, VIDEO, GRAPHIC, SOURCE (SCALER)
            format: BMP, JPG, PNG, RGB, RGBA, YUV422
        """
        return await self.request(ep.TAKE_SCREENSHOT, {"method": method, "format": format, "width": width, "height": height, "path": path})

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

    async def get_attached_devices(self, types=[], jsonOutput=False):
        """Get attached devices. types can be:
            ["usb", "internal camera", "internal samples", "internal igallery", "dms", "internal store demo"]
        """
        types = types if type(types) is list else []
        res = await self.request(ep.LIST_DEVICES, {"deviceType": types})
        return self.__output_result(res.get("devices"), jsonOutput)

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
        """Set picture mode for current category, input, dynamic range and 3d mode (OLED C2).

        Known picture modes are: cinema, eco, expert1, expert2, filmMaker,
        game, normal, photo, sports, vivid, hdrCinema, hdrCinemaBright,
        hdrExternal, hdrFilmMaker, hdrGame, hdrStandard, hdrVivid,
        dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon,
        dolbyHdrGame, dolbyHdrStandard, dolbyHdrVivid

        Known categories are: picture, aiPicture

        Likely not all modes are valid for all tv models.
        """

        params = {"category": category, "settings": {"pictureMode": pic_mode}}

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def set_picture_mode(
        self, pic_mode, tv_input, dynamic_range="sdr", stereoscopic="2d", category="picture"
    ):
        """Set picture mode for specific category, input, dynamic range and 3d mode (OLED C2).

        Known picture modes are: cinema, eco, expert1, expert2, filmMaker,
        game, normal, photo, sports, vivid, hdrCinema, hdrCinemaBright,
        hdrExternal, hdrFilmMaker, hdrGame, hdrStandard, hdrVivid,
        dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon,
        dolbyHdrGame, dolbyHdrStandard, dolbyHdrVivid

        Known inputs are: atv, av1, av2, browser, camera, comp1, comp2,
        comp3, default, dtv, gallery, hdmi1, hdmi1_pc, hdmi2, hdmi2_pc,
        hdmi3, hdmi3_pc, hdmi4, hdmi4_pc, ip, movie, photo, pictest,
        rgb, scart, smhl

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

        A possible list of settings and OLED C2 example values are below
        (not all settings are applicable for all modes and/or tv models):
        /etc/palm/defaultSettings.json

        Category: aiPicture
        -------------------

        "ai_Brightness": "off",
        "ai_Genre": "off",
        "ai_Picture": "off",
        "isAiPictureActing": false

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
        "applyToAllInput": "done",
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
        "dolbyPrecisionDetail": "off",
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
        "localDimming": "low",
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

        A possible list of settings and OLED C2 example values are below
        (not all settings are applicable for all tv models/firmwares):
        /etc/palm/defaultSettings.json

        "activeArtisticDisplayScreenSaver": false,
        "amazonHotkeyIsActive": true,
        "appReturn": "",
        "battery25PercentMode": "off",
        "batteryInstopProtect": "on",
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
        "darkMode": "off",
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
        "fitLogUsbDump": "off",
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
        "gameAdjustContrast": 95,
        "gameBlackLevel": 50,
        "gameColorDepth": 55,
        "gameDashboardStatusList": [
            "fps",
            "vrr_aiGameSound_whiteStabilizer",
            "blackStabilizer",
            "lowLatency"
        ],
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
        "gameScreenPosition": "middle",
        "gameScreenRatio": "16:9",
        "gameScreenSize": "full",
        "gameSettingModified": {
            "FPS": false,
            "RPG": false,
            "RTS": false,
            "Sports": false,
            "Standard": false,
            "USER": false
        },
        "gameSharpness": 10,
        "gameUIColor": "violet",
        "gameWallpaper": {
            "folderUpdateVersion": 0,
            "imgSrc": ""
        },
        "hdmiPcMode": {
            "hdmi1": false,
            "hdmi2": false,
            "hdmi3": false,
            "hdmi4": false
        },
        "homeAppLaunched": "off",
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
        "lightingBrightness": 8,
        "lightingEnable": "off",
        "lightingMode": "dynamic",
        "lowLevelAdjustment": 0,
        "lowPowerMode": "off",
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
                "fptplay": {
                    "app_id": "com.fpt.fptplay",
                    "isActive": true,
                    "launch_param": null
                }
            },
            {
                "shahid": {
                    "app_id": "net.mbc.shahid-lgapp",
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
        "oledCareMode": "off",
        "oledCareRecommendation": "off",
        "playbackThreshold": 200,
        "pseudoTouchMode": "on",
        "quickSettingsMenuList": [
            "QuickSettings_picture_button",
            "QuickSettings_soundMode_button",
            "QuickSettings_soundOut_button",
            "QuickSettings_game_button",
            "QuickSettings_multiview_button",
            "QuickSettings_ocp_button",
            "QuickSettings_network_button",
            "QuickSettings_menu_button"
        ],
        "screenRemoteAutoShow": "true",
        "screenRemoteExpanded": "false",
        "screenRemotePosition": "right",
        "simplinkAutoPowerOn": "on",
        "simplinkEnable": "off",
        "soundSyncModeColor": "auto",
        "soundSyncModeDisplayMode": "bar",
        "soundSyncModeFrequency": "mid",
        "soundSyncModeStaticColor": 35,
        "staticModeColor1": 35,
        "staticModeColor2": 1,
        "staticModeColor3": 12,
        "staticModeColor4": 0,
        "supportAirplay": false,
        "supportBnoModel": false,
        "touchRemoteLaunchMode": "edgeSwipe",
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

        A possible list of settings and OLED C2 example values are below
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
        "artisticDisplayTimer": "off",
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
        "cameraResourcePermission": [],
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
        "curvature": {
            "curvatureList": [
                {
                    "disable": false,
                    "selected": true,
                    "type": "flat",
                    "user": false,
                    "value": "0%"
                },
                {
                    "disable": false,
                    "selected": false,
                    "type": "curvature1",
                    "user": false,
                    "value": "50%"
                },
                {
                    "disable": false,
                    "selected": false,
                    "type": "curvature2",
                    "user": false,
                    "value": "100%"
                },
                {
                    "disable": true,
                    "selected": false,
                    "type": "curvature3",
                    "user": false,
                    "value": "100%"
                }
            ],
            "valueList": [
                "0%",
                "5%",
                "10%",
                "15%",
                "20%",
                "25%",
                "30%",
                "35%",
                "40%",
                "45%",
                "50%",
                "55%",
                "60%",
                "65%",
                "70%",
                "75%",
                "80%",
                "85%",
                "90%",
                "95%",
                "100%"
            ]
        },
        "dataService": "mheg",
        "dbgLogUpload": false,
        "demoFileList": "undefined",
        "demoMode": "on",
        "displayMusicWidget": true,
        "eStreamerPosition": "all",
        "emergencyAlert": "on",
        "emergencyInformationAtsc30": "on",
        "emergencyInformationLanguageAtsc30": "eng",
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
        "interactive-service-hdmi": "off",
        "interactive-service-id": "",
        "interactivity": "off",
        "irBlaster": "off",
        "ismMethod": "normal",
        "japanCitySelection": "Tokyo",
        "lifeOnScreenEnergySaving": "auto",
        "lifeOnScreenNotification": true,
        "lifeOnScreenOnTimer": [],
        "lifeOnScreenUsingMotionSensor": false,
        "lineView": "on",
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
        "magicNumFvp": false,
        "magicNumHelpShow": true,
        "menuLanguage": "eng",
        "menuTransparency": "on",
        "mhegGuide": "off",
        "miracastOverlayAdRecovery": "off",
        "miracastOverlayStatus": "off",
        "modeSelectFlag": "off",
        "motionRecognition": "off",
        "motionSensorSensitivity": "medium",
        "motionSensorSensitivityForAOD": "medium",
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
        "restoreCurve": "on",
        "screenOff": "off",
        "screenOffTime": "5",
        "screenRotation": "off",
        "searchAppTTS": "off",
        "serviceCountryForMagicNum": "",
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
        "wallPaperSettings": {
            "artisticDisplayTheme": "default",
            "artisticDisplayThemeVersion": 0,
            "homeImageVersion": 0,
            "imageLimit": 0,
            "isFullView": false
        },
        "watchedListCollection": "on",
        "webOSPromotionVideo": "on",
        "yourMomentsVersion": "0",
        "zipcode": "not_defined"

        """

        params = {"category": "option", "settings": settings}

        return await self.luna_request(ep.LUNA_SET_SYSTEM_SETTINGS, params)

    async def get_configs(self, keys=["tv.model.*"], jsonOutput=False):
        """Get config settings.

        A possible list of keys of OLED C2 are below (not all settings are applicable for all tv models):
        /etc/configd/layers

        airplay.*
        amazon-alexa-adapter.*
        amazon.*
        audio.*
        broadcast.*
        com.palm.app.firstuse.*
        com.palm.app.settings.*
        com.palm.app.store-demo.*
        com.webos.app.connectionwizard.*
        com.webos.app.factorywin.*
        com.webos.app.familycare.*
        com.webos.app.favshows.*
        com.webos.app.home.*
        com.webos.app.igallery.*
        com.webos.app.inputcommon.*
        com.webos.app.mediadiscovery.*
        com.webos.app.quicksettings.*
        com.webos.app.systemmusic.*
        com.webos.app.tips.*
        com.webos.applicationManager.*
        com.webos.authenticationMethods.*
        com.webos.keyaction.*
        com.webos.memorymanager.*
        com.webos.service.airplay.*
        com.webos.service.alwayready.*
        com.webos.service.arccontroller.*
        com.webos.service.attachedstoragemanager.*
        com.webos.service.bthidmanager.*
        com.webos.service.camera.*
        com.webos.service.cbox.*
        com.webos.service.config.*
        com.webos.service.datamigrator.*
        com.webos.service.eim.*
        com.webos.service.favoriteservice.*
        com.webos.service.fepg.*
        com.webos.service.hybridtv.*
        com.webos.service.iepg.*
        com.webos.service.ime.*
        com.webos.service.irdbmanager.*
        com.webos.service.jsserver.*
        com.webos.service.livepick.*
        com.webos.service.miracast.*
        com.webos.service.miracasttx.*
        com.webos.service.msc.*
        com.webos.service.nlpmanager.*
        com.webos.service.nop.*
        com.webos.service.nudge.*
        com.webos.service.pbsw.*
        com.webos.service.pdm.*
        com.webos.service.photorenderer.*
        com.webos.service.pqcontroller.*
        com.webos.service.preloadmanager.*
        com.webos.service.rollingscreen.*
        com.webos.service.scd.*
        com.webos.service.time.*
        com.webos.service.tnm.*
        com.webos.service.tvpower.*
        com.webos.service.utp.*
        com.webos.service.voiceinput.*
        com.webos.service.wampluggable.hbbtv.*
        com.webos.surfacemanager.*
        dvr.*
        extinput-service.*
        gip.*
        inputMap.*
        mediaCapability.*
        miracast.*
        multiview.*
        profile.*
        system.*
        tv.config.*
        tv.conti.*
        tv.hw.*
        tv.model.*
        tv.nyx.*
        tv.rmm.*
        wee.*

        """

        payload = {"configNames": keys}
        res = await self.request(ep.GET_CONFIGS, payload=payload)
        return self.__output_result(res, jsonOutput)

    async def set_configs(self, settings):
        """Set config settings.

        Example:

        "tv.model.motionProMode": "OLED Motion",
        "tv.model.motionProMode": "OLED Motion Pro"
        "tv.conti.supportUsedTime": true

        """

        params = {"configs": settings}

        return await self.luna_request(ep.LUNA_SET_CONFIGS, params)

    async def show_screen_saver(self):
        return await self.luna_request(ep.LUNA_TURN_ON_SCREEN_SAVER, {})

    async def reboot_soft(self, webos_ver=""):
        epName = f"LUNA_REBOOT_TV_WO{webos_ver}" if webos_ver else "LUNA_REBOOT_TV"

        if not hasattr(ep, epName):
            raise ValueError(f"there's no {epName} endpoint")

        return await self.luna_request(getattr(ep, epName), {"reason": "reset"})

    async def eject_attached_device(self, device_id):
        """Eject a USB device. deviceId can be obtained with get_attached_devices method."""
        return await self.luna_request(ep.LUNA_EJECT_DEVICE, {"deviceId": device_id})

    async def get_system_settings(self, category="option", keys=["audioGuidance"], jsonOutput=False):
        """Get system settings.

        Most of the settings are not exposed via this call, OLED C2 valid settings:
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
                "countryBroadcastSystem",
                "yourMomentsVersion",
                "wallPaperSettings"
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
                "ueiEnable",
                "gameWallpaper"
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
                "SCA3SystemCountry",
                "homeAutoLaunch",
                "lifeOnScreenMode"
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

    def calibration_support_info(self):
        if not self._calibration_info:
            if self._software_info is None:
                raise PyLGTVCmdException(f"Software info is not available, -s command line switch is required.")

            info = {
                "lut3d":    None,
                "dovi":     None,
            }

            model_name = self._software_info["model_name"]
            if model_name.startswith("HE_DTV_") and len(model_name) >= 11:
                chip_type = model_name[7:11]

                if chip_type in ["W18H", "W19H", "W20H", "W21H", "W22H"]:
                    info["lut3d"] = LUT3D_SIZES["17pt"]
                elif chip_type in ["W18O", "W19O", "W20O", "W21O", "W22O"]:
                    info["lut3d"] = LUT3D_SIZES["33pt"]

                if chip_type in ["W18H", "W18O"]:
                    info["dovi"] = DV_CONFIG_TYPES["2018"]
                elif chip_type in ["W19H", "W19O", "W20H", "W20O", "W21H", "W21O", "W22H", "W22O"]:
                    info["dovi"] = DV_CONFIG_TYPES["2019"]

            self._calibration_info = info

    if np:
        def check_calibration_support(self, property="lut3d", message="3D LUT Upload"):
            self.calibration_support_info()
            if not self._calibration_info[property]:
                model = self._software_info["model_name"]
                raise PyLGTVCmdException(f"{message} not supported by model {model}.")

        def validateCalibrationData(self, data, shape, dtype, range=None, count=None):
            if not isinstance(data, np.ndarray):
                raise TypeError(f"data must be of type ndarray but is instead {type(data)}")
            if data.shape != shape:
                raise ValueError(f"data should have shape {shape} but instead has {data.shape}")
            if data.dtype != dtype:
                raise TypeError(f"numpy dtype should be {dtype} but is instead {data.dtype}")
            if isinstance(range, tuple) and len(range) == 2 and ((data >= range[0]).all() != (data <= range[1]).all()):
                raise ValueError(f"values in data must be between {range[0]} and {range[1]}")
            if isinstance(count, int) and data.size != count:
                raise ValueError(f"data should have size {count} but instead has {data.size}")

        async def get_calibration_data(self, command, shape, filename=""):
            if command not in [cal.GET_GAMMA_2_2_TRANSFORM, cal.GET_GAMMA_0_45_TRANSFORM, cal.GET_3BY3_GAMUT_DATA, cal.GET_HDR_3BY3_GAMUT_DATA, cal.GET_1D_LUT, cal.GET_3D_LUT]:
                raise PyLGTVCmdException(f"Invalid Get Calibration command {command}.")
            if filename and filename.split(".")[-1].lower() not in ["1dlut", "matrix", "3dlut"]:
                raise PyLGTVCmdException(f"Invalid Get Calibration file extension, must be: 1dlut or matrix or 3dlut.")

            response = await self.request(ep.GET_CALIBRATION, {"command": command})

            encodedData = response.get("data")
            dataCount = response.get("dataCount")
            dataType = response.get("dataType")
            type = [k for k, v in CALIBRATION_TYPE_MAP.items() if v == dataType]

            if not encodedData or not dataCount or not dataType or not type:
                raise PyLGTVCmdException(f"Invalid response {response}.")

            npType = getattr(np, type[0])
            data_bytes = base64.b64decode(encodedData.encode())
            deserialized_bytes = np.frombuffer(data_bytes, dtype=npType)
            data = np.reshape(deserialized_bytes, newshape=shape)
            self.validateCalibrationData(data, shape, npType, None, dataCount)

            if filename:
                # backup numpy array
                return await asyncio.get_running_loop().run_in_executor(
                    None, backup_lut_into_file, filename, data
                )
            else:
                # print the full numpy array
                np.set_printoptions(threshold=np.inf)
                return data if shape != (1, ) else data[0]

        async def get_1d_en_2_2(self):
            return await self.get_calibration_data(cal.GET_GAMMA_2_2_TRANSFORM, (1, ))

        async def get_1d_en_0_45(self):
            return await self.get_calibration_data(cal.GET_GAMMA_0_45_TRANSFORM, (1, ))

        async def get_3by3_gamut_data(self, filename=""):
            return await self.get_calibration_data(cal.GET_3BY3_GAMUT_DATA, (3, 3), filename)

        async def get_3by3_gamut_data_hdr(self, filename=""):
            return await self.get_calibration_data(cal.GET_HDR_3BY3_GAMUT_DATA, (3, 3), filename)

        async def get_1d_lut(self, filename=""):
            return await self.get_calibration_data(cal.GET_1D_LUT, (3, 1024), filename)

        async def get_3d_lut(self, filename=""):
            self.check_calibration_support("lut3d", "3D LUT Upload")
            lut3d_size = self._calibration_info["lut3d"]
            lut3d_shape = (lut3d_size, lut3d_size, lut3d_size, 3)
            return await self.get_calibration_data(cal.GET_3D_LUT, lut3d_shape, filename)

        async def calibration_request(self, command, data=None, dataOpt=1, picture_mode=None):
            # dataOpt: 0 - Apply, 1 - Apply and Save, 2 - Reset
            if dataOpt < 0 or dataOpt > 2:
                raise ValueError(f"Invalid dataOpt {dataOpt}, must be between 0. and 2.")
            if not command:
                raise PyLGTVCmdException(f"Invalid Calibration Request command {command}.")

            payload = {
                "command": command,
                "profileNo": 0,
                "programID": 1,
            }
            if picture_mode is not None:
                payload["picMode"] = picture_mode

            if data is not None:
                payload["data"] = base64.b64encode(data.tobytes()).decode()
                payload["dataCount"] = data.size
                payload["dataType"] = CALIBRATION_TYPE_MAP[data.dtype.name]
                payload["dataOpt"] = dataOpt

            return await self.request(ep.CALIBRATION, payload)

        async def start_calibration(self, picture_mode):
            if not any(picture_mode in ls for ls in [SDR_PICTURE_MODES, HDR10_PICTURE_MODES, DV_PICTURE_MODES]):
                raise PyLGTVCmdException(f"Invalid picture_mode {picture_mode}.")

            return await self.calibration_request(cal.CAL_START, None, 1, picture_mode)

        async def end_calibration(self):
            return await self.calibration_request(cal.CAL_END)

        async def set_ui_data(self, command, value):
            if command not in [cal.BACKLIGHT_UI_DATA, cal.CONTRAST_UI_DATA, cal.BRIGHTNESS_UI_DATA, cal.COLOR_UI_DATA]:
                raise PyLGTVCmdException(f"Invalid UI Data command {command}.")
            if type(value) is not int or value < 0 or value > 100:
                raise ValueError(f"Invalid value {value}, must be between 0. and 100.")

            data = np.array(value, dtype=np.uint16)
            return await self.calibration_request(command, data)

        async def set_oled_light(self, value=33):
            return await self.set_ui_data(cal.BACKLIGHT_UI_DATA, value)

        async def set_contrast(self, value=85):
            return await self.set_ui_data(cal.CONTRAST_UI_DATA, value)

        async def set_brightness(self, value=50):
            return await self.set_ui_data(cal.BRIGHTNESS_UI_DATA, value)

        async def set_color(self, value=50):
            return await self.set_ui_data(cal.COLOR_UI_DATA, value)

        async def upload_1d_lut(self, data=None):
            if type(data) is list and len(data) == 0:
                # Reset uploaded data
                data = np.array([], dtype=np.uint16)
                dataOpt = 2
            else:
                if data is None:
                    data = await asyncio.get_running_loop().run_in_executor(None, unity_lut_1d)
                self.validateCalibrationData(data, (3, 1024), np.uint16)
                dataOpt = 1

            return await self.calibration_request(cal.UPLOAD_1D_LUT, data, dataOpt)

        async def upload_1d_lut_from_file(self, filename):
            ext = filename.split(".")[-1].lower()
            if ext == "cal":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_cal_file, filename
                )
            elif ext == "cube":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_cube_file, filename
                )
            elif ext == "1dlut":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_1dlut_file, filename
                )
            else:
                raise ValueError(
                    f"Unsupported file format {ext} for 1D LUT. Supported file formats are cal, cube and 1dlut."
                )

            return await self.upload_1d_lut(lut)

        async def toggle_calibration_flag(self, command, enable):
            """Toggle various calibration flags."""
            if command not in [cal.ENABLE_GAMMA_2_2_TRANSFORM, cal.ENABLE_GAMMA_0_45_TRANSFORM, cal.ENABLE_1D_LUT, cal.ENABLE_3BY3_GAMUT]:
                raise PyLGTVCmdException(f"Invalid calibration flag command {command}.")
            if not ((type(enable) is list and len(enable) == 0)
                or (type(enable) is bool)):
                raise ValueError(f"Invalid enable {enable}, must be bool or empty list.")

            if type(enable) is list and len(enable) == 0:
                # Reset uploaded data
                data = np.array([], dtype=np.uint16)
                dataOpt = 2
            else:
                value = 1 if enable else 0
                data = np.array(value, dtype=np.uint16)
                dataOpt = 1

            return await self.calibration_request(command, data, dataOpt)

        async def set_1d_lut_en(self, enable=False):
            """Toggle 1D LUT flag."""
            return await self.toggle_calibration_flag(cal.ENABLE_1D_LUT, enable)

        async def upload_3d_lut(self, command, data):
            if command not in [cal.UPLOAD_3D_LUT_BT709, cal.UPLOAD_3D_LUT_BT2020]:
                raise PyLGTVCmdException(f"Invalid 3D LUT Upload command {command}.")

            if type(data) is list and len(data) == 0:
                # Reset uploaded data
                data = np.array([], dtype=np.uint16)
                dataOpt = 2
            else:
                self.check_calibration_support("lut3d", "3D LUT Upload")

                lut3d_size = self._calibration_info["lut3d"]
                if data is None:
                    data = await asyncio.get_running_loop().run_in_executor(
                        None, unity_lut_3d, lut3d_size
                    )
                lut3d_shape = (lut3d_size, lut3d_size, lut3d_size, 3)
                self.validateCalibrationData(data, lut3d_shape, np.uint16)
                dataOpt = 1

            return await self.calibration_request(command, data, dataOpt)

        async def upload_3d_lut_bt709(self, data=None):
            return await self.upload_3d_lut(cal.UPLOAD_3D_LUT_BT709, data)

        async def upload_3d_lut_bt2020(self, data=None):
            return await self.upload_3d_lut(cal.UPLOAD_3D_LUT_BT2020, data)

        async def upload_3d_lut_from_file(self, command, filename):
            ext = filename.split(".")[-1].lower()
            if ext == "cube":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_cube_file, filename
                )
            elif ext == "3dlut":
                self.check_calibration_support("lut3d", "3D LUT Upload")
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_3dlut_file, filename, self._calibration_info["lut3d"]
                )
            else:
                raise ValueError(
                    f"Unsupported file format {ext} for 3D LUT. Supported file formats are cube and 3dlut."
                )

            return await self.upload_3d_lut(command, lut)

        async def upload_3d_lut_bt709_from_file(self, filename):
            return await self.upload_3d_lut_from_file(cal.UPLOAD_3D_LUT_BT709, filename)

        async def upload_3d_lut_bt2020_from_file(self, filename):
            return await self.upload_3d_lut_from_file(cal.UPLOAD_3D_LUT_BT2020, filename)

        async def set_1d_en_2_2(self, enable=False):
            """Toggle 1D LUT de-gamma flag (gamma to linear space transformation)."""
            return await self.toggle_calibration_flag(cal.ENABLE_GAMMA_2_2_TRANSFORM, enable)

        async def set_1d_en_0_45(self, enable=False):
            """Toggle 1D LUT re-gamma flag (linear to gamma space transformation)."""
            return await self.toggle_calibration_flag(cal.ENABLE_GAMMA_0_45_TRANSFORM, enable)

        async def set_3by3_gamut_data(self, command, data):
            if command not in [cal.BT709_3BY3_GAMUT_DATA, cal.BT2020_3BY3_GAMUT_DATA, cal.HDR_3BY3_GAMUT_DATA]:
                raise PyLGTVCmdException(f"Invalid 3by3 Gamut Data Upload command {command}.")

            if type(data) is list and len(data) == 0:
                # Reset uploaded data
                data = np.array([], dtype=np.float32)
                dataOpt = 2
            else:
                if data is None:
                    data = np.identity(3, dtype=np.float32)
                elif not isinstance(data, np.ndarray):
                    data = np.array(data, dtype=np.float32)
                self.validateCalibrationData(data, (3, 3), np.float32, (-1024, 1024))
                dataOpt = 1

            return await self.calibration_request(command, data, dataOpt)

        async def set_3by3_gamut_data_bt709(self, data=None):
            """Set BT709 slot 3x3 color matrix (color gamut space transformation in linear space)."""
            return await self.set_3by3_gamut_data(cal.BT709_3BY3_GAMUT_DATA, data)

        async def set_3by3_gamut_data_bt2020(self, data=None):
            """Set BT2020 slot 3x3 color matrix (color gamut space transformation in linear space)."""
            return await self.set_3by3_gamut_data(cal.BT2020_3BY3_GAMUT_DATA, data)

        async def set_3by3_gamut_data_hdr(self, data=None):
            """Set HDR 3x3 color matrix used only in 2019 models (color gamut space transformation in linear space)."""
            return await self.set_3by3_gamut_data(cal.HDR_3BY3_GAMUT_DATA, data)

        async def set_3by3_gamut_data_from_file(self, type, filename):
            methodName = f'set_3by3_gamut_data_{type}'
            if not callable(getattr(self, methodName, None)):
                raise PyLGTVCmdException(f"Invalid 3by3 gamut type {type}, must be: bt709 or bt2020 or hdr")

            ext = filename.split(".")[-1].lower()
            if ext == "matrix":
                lut = await asyncio.get_running_loop().run_in_executor(
                    None, read_3by3_gamut_file, filename
                )
            else:
                raise ValueError(
                    f"Unsupported file format {ext} for 3by3 gamut. Supported file format is matrix."
                )

            method = getattr(self, methodName)
            return await method(lut)

        async def set_3by3_gamut_en(self, enable=False):
            """Toggle 3x3 color matrix flag (color gamut space transformation in linear space)."""
            return await self.toggle_calibration_flag(cal.ENABLE_3BY3_GAMUT, enable)

        async def set_bypass_modes_sdr(self, unity_1d_lut=False):
            """Set SDR bypass modes."""
            if not isinstance(unity_1d_lut, bool):
                raise TypeError(
                    f"unity_1d_lut should be a bool, instead got {unity_1d_lut} of type {type(unity_1d_lut)}."
                )

            await self.set_1d_en_2_2()
            await self.set_1d_en_0_45()
            await self.set_3by3_gamut_data_bt709()
            await self.set_3by3_gamut_data_bt2020()
            await self.upload_3d_lut_bt709()
            await self.upload_3d_lut_bt2020()
            if unity_1d_lut:
                await self.upload_1d_lut()

            return True

        async def reset_factory_data_sdr(self):
            """Reset SDR factory calibration data."""
            await self.set_1d_en_2_2([])
            await self.set_1d_en_0_45([])
            await self.set_3by3_gamut_data_bt709([])
            await self.set_3by3_gamut_data_bt2020([])
            await self.upload_3d_lut_bt709([])
            await self.upload_3d_lut_bt2020([])
            await self.upload_1d_lut([])

            return True

        async def set_bypass_modes_hdr10(self, unity_3d_lut=False):
            """Set HDR10 bypass modes."""
            if not isinstance(unity_3d_lut, bool):
                raise TypeError(
                    f"unity_3d_lut should be a bool, instead got {unity_3d_lut} of type {type(unity_3d_lut)}."
                )

            await self.upload_1d_lut()
            if unity_3d_lut:
                await self.set_1d_en_2_2()
                await self.set_1d_en_0_45()
                await self.set_3by3_gamut_data_bt709()
                await self.set_3by3_gamut_data_bt2020()
                await self.upload_3d_lut_bt709()
                await self.upload_3d_lut_bt2020()

            return True

        async def reset_factory_data_hdr10(self, picture_mode=None, tonemap_params=False):
            """Reset HDR10 factory calibration data."""
            if not isinstance(tonemap_params, bool):
                raise TypeError(
                    f"tonemap_params should be a bool, instead got {tonemap_params} of type {type(tonemap_params)}."
                )

            await self.set_1d_en_2_2([])
            await self.set_1d_en_0_45([])
            await self.set_3by3_gamut_data_bt709([])
            await self.set_3by3_gamut_data_bt2020([])
            await self.upload_3d_lut_bt709([])
            await self.upload_3d_lut_bt2020([])
            await self.upload_1d_lut([])
            if tonemap_params:
                await self.set_tonemap_params(picture_mode, [])

            return True

        async def set_bypass_modes_dovi(self):
            """Set DoVi bypass modes."""
            await self.upload_1d_lut()

            return True

        async def reset_factory_data_dovi(self, picture_mode=None, dovi_config=False):
            """Reset DoVi factory calibration data."""
            if not isinstance(dovi_config, bool):
                raise TypeError(
                    f"dovi_config should be a bool, instead got {dovi_config} of type {type(dovi_config)}."
                )

            await self.upload_1d_lut([])
            if dovi_config:
                await self.set_dolby_vision_config_data(picture_mode, [])

            return True

        async def set_tonemap_params(
            self,
            picture_mode,
            luminance=700,
            mastering_peak_1=1000,
            rolloff_point_1=70,
            mastering_peak_2=4000,
            rolloff_point_2=60,
            mastering_peak_3=10000,
            rolloff_point_3=50,
        ):
            """Uploads custom HDR10 tone mapping parameters."""
            if picture_mode not in HDR10_PICTURE_MODES:
                raise PyLGTVCmdException(f"Invalid picture_mode {picture_mode}, must be an HDR10 one.")
            if ((type(luminance) is list and len(luminance) != 0)
                or (type(luminance) is int and (luminance < 100 or luminance > 4000))):
                raise ValueError(f"Invalid luminance {luminance}, must be between 100. and 4000.")
            for value in [mastering_peak_1, mastering_peak_2, mastering_peak_3]:
                if value < 100 or value > 10000:
                    raise ValueError(f"Invalid mastering_peak {value}, must be between 100. and 10000.")
            for value in [rolloff_point_1, rolloff_point_2, rolloff_point_3]:
                if value < 0 or value > 100:
                    raise ValueError(f"Invalid rolloff_point {value}, must be between 0. and 100.")

            if type(luminance) is list and len(luminance) == 0:
                # Reset uploaded data
                data = np.array([], dtype=np.uint16)
                dataOpt = 2
            else:
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
                dataOpt = 1

            return await self.calibration_request(cal.SET_TONEMAP_PARAM, data, dataOpt)

        async def set_dolby_vision_config_data(
            self, picture_mode, white_level=700.0, black_level=DV_BLACK_LEVEL, gamma=DV_GAMMA, primaries=BT2020_PRIMARIES
        ):
            """This method is NOT recommended since it uses the calibration API,
            use generate_dolby_vision_config method instead!"""

            if type(white_level) is list and len(white_level) == 0:
                # Reset uploaded data
                data = np.array([], dtype=np.uint8)
                dataOpt = 2
            else:
                self.check_calibration_support("dovi", "Dolby Vision Configuration Upload")

                config = await asyncio.get_running_loop().run_in_executor(
                    None,
                    functools.partial(
                        create_dolby_vision_config,
                        version=self._calibration_info["dovi"],
                        picture_mode=picture_mode,
                        white_level=white_level,
                        black_level=black_level,
                        gamma=gamma,
                        primaries=primaries,
                    ),
                )
                data = np.frombuffer(config.replace("\n", "\r\n").encode(), dtype=np.uint8)
                dataOpt = 1

            return await self.calibration_request(cal.DOLBY_CFG_DATA, data, dataOpt)

        async def write_dolby_vision_config_file(self, data, apply_to_all_modes=False, full_path=""):
            """Writes Dolby Vision config file for USB upload."""

            self.check_calibration_support("dovi", "Dolby Vision Configuration Generation")
            if not isinstance(apply_to_all_modes, bool):
                raise TypeError(
                    f"apply_to_all_modes should be a bool, instead got {apply_to_all_modes} of type {type(apply_to_all_modes)}."
                )
            if not isinstance(full_path, str):
                raise TypeError(
                    f"full_path should be a str, instead got {full_path} of type {type(full_path)}."
                )

            if apply_to_all_modes and len(data) == 1 and type(data[0]) is dict and 'primaries' in data[0]:
                # copy picture mode data multiple times and modify picture mode
                counter = 0

                for picture_mode in DV_PICTURE_MODES:
                    if counter > 0:
                        data.append({**data[0]})
                        data[counter]['primaries'] = list(data[0]['primaries'])

                    data[counter]['picture_mode'] = picture_mode
                    counter += 1

            config = await asyncio.get_running_loop().run_in_executor(
                None,
                functools.partial(
                    generate_dolby_vision_config,
                    data=data,
                    version=self._calibration_info["dovi"],
                ),
            )

            with open(os.path.join(full_path, DV_CONFIG_FILENAME), "w", newline='\r\n') as f:
                f.write(config)

            print(f"Generated DoVi config file: {DV_CONFIG_FILENAME}")
            return True

        async def set_itpg_patch_window(
            self, r=0, g=0, b=0, win_id=0, width=858, height=482, startx=1491, starty=839
        ):
            """Set iTPG patch window properties.

                r / g / b: The fill color of the window. Values are 10 bit full range (0-1023).
                win_id: Identifier of the window to be displayed on the screen together with all others.
                    The maximum number of simultaneous windows is 10, so valid values are 0 to 9.
                    Use the IDs in ascending order, with the window with ID 0 on the Z axis at the very back.
                width / height: The size of the window. The size of the screen is defined by
                    its native resolution and not the resolution of the current signal.
                    So with UHD TVs the screen always has a size of 3840x2160.
                startx / starty: The origin of the window, the coordinate system of the screen
                    has its origin in the upper left corner.

            """

            for value in [r, g, b]:
                if value < 0 or value > 1023:
                    raise ValueError(f"Invalid fill color {value}, must be between 0. and 1023.")
            if win_id < 0 or win_id > 9:
                raise ValueError(f"Invalid win_id {win_id}, must be between 0. and 9.")
            if width < 100 or width > 7680:
                raise ValueError(f"Invalid width {width}, must be between 100. and 7680.")
            if height < 56 or height > 4320:
                raise ValueError(f"Invalid height {height}, must be between 56. and 4320.")
            if startx < 0 or startx > 7579:
                raise ValueError(f"Invalid startx {startx}, must be between 0. and 7579.")
            if starty < 0 or starty > 4263:
                raise ValueError(f"Invalid starty {starty}, must be between 0. and 4263.")

            payload = {
                "command": cal.PATTERN_WINDOW,
                "fillR": r,
                "fillG": g,
                "fillB": b,
                "winId": win_id,
                "width": width,
                "height": height,
                "startX": startx,
                "startY": starty,
                "programID": 1,
            }

            return await self.request(ep.CALIBRATION, payload)

        async def set_itpg_gradation_window(
            self, bar_id=0, stride_size=240, start_r=64, start_g=64, start_b=64, step_r=58, step_g=58, step_b=58
        ):
            """Set iTPG gradation window properties.

                bar_id: Identifier of the gradient bar to be displayed on the screen.
                    The maximum number of simultaneous displayed gradient bars is 4, so the valid value range is 0 to 3.
                stride_size: Stride size of the gradient bars in pixels. The value of the first
                    bar with ID 0 defines the stride size of all displayed gradient bars.
                    I.e. all bars always have the same size.
                start_r / start_g / start_g: The starting color of the gradient (10 bit full range).
                step_r / step_g / step_b: The color value increment applied to the gradient
                    (10 bit full range) for each color step.

                E.g. displaying vertical grayscale gradient pattern from black (0) to white (1023)
                    on 3840 width display with the following example results in bars being 3 pixels wide
                    and the pattern ends at a witdh of 3072 pixels and the rest of the screen is filled with the color of the last color step:
                    bar_id=0, stride_size=3, start_r=0, start_g=0, start_b=0, step_r=1, step_g=1, step_b=1

            """

            if bar_id < 0 or bar_id > 3:
                raise ValueError(f"Invalid bar_id {bar_id}, must be between 0. and 3.")
            if stride_size < 0 or stride_size > 7680:
                raise ValueError(f"Invalid stride_size {stride_size}, must be between 0. and 7680.")
            for value in [start_r, start_g, start_b]:
                if value < 0 or value > 1023:
                    raise ValueError(f"Invalid starting color {value}, must be between 0. and 1023.")
            for value in [step_r, step_g, step_b]:
                if value < 0 or value > 512:
                    raise ValueError(f"Invalid starting color {value}, must be between 0. and 512.")

            payload = {
                "command": cal.PATTERN_GRADATION,
                "barId": bar_id,
                "strideSize": stride_size,
                "startR": start_r,
                "startG": start_g,
                "startB": start_b,
                "stepR": step_r,
                "stepG": step_g,
                "stepB": step_b,
                "programID": 1,
            }

            return await self.request(ep.CALIBRATION, payload)

        async def toggle_itpg(self, enable=True, numOfBox=2, ptnType=0, fix_enable=True):
            """Toggle (enable / disable) iTPG.

                enable: "true" or "false" String value activating or deactivating the pattern display.
                    This used to be a Bool value on older models / firmware versions
                    but now has to be a String value (fix_enable can be used to mitigate the issue).
                numOfBox: The total number of windows or gradient bars to activate, maximum is 10.
                    Usually "2" if you have one window for the background and one for the
                    calibration pattern in the center of the screen.
                ptnType: 0 windowBoxes, 1 gradationBarsVertical, 2 gradationBarsHorizontal

            """

            if not isinstance(enable, bool):
                raise TypeError(f"enable should be a bool, instead got {enable} of type {type(enable)}.")
            if numOfBox < 0 or numOfBox > 10:
                raise ValueError(f"Invalid numOfBox {numOfBox}, must be between 0. and 10.")
            if ptnType < 0 or ptnType > 2:
                raise ValueError(f"Invalid ptnType {ptnType}, must be between 0. and 2.")
            if not isinstance(fix_enable, bool):
                raise TypeError(f"fix_enable should be a bool, instead got {fix_enable} of type {type(fix_enable)}.")


            payload = {
                "command": cal.PATTERN_CONTROL,
                "enable": (str(enable).lower() if fix_enable else enable),
                "numOfBox": numOfBox,
                "ptnType": ptnType,
                "programID": 1,
            }

            return await self.request(ep.CALIBRATION, payload)
