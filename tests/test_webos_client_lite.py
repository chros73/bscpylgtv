import asyncio
import base64
import json

import pytest
from bscpylgtv import WebOsClient
from bscpylgtv import endpoints as ep


@pytest.mark.asyncio
class TestWebOsClientLite():

    async def test_connect_handler_invokes_state_update_callbacks_on_failed_connect(self, monkeypatch):
        async def fake_connect(*args, **kwargs):
            raise OSError("simulated connect failure")

        monkeypatch.setattr("bscpylgtv.webos_client.websockets.connect", fake_connect)

        called = []

        async def on_update(client):
            called.append(client)

        client = await WebOsClient.create("x", states=["power", "software_info"], client_key="x")
        client.connect_retry_attempts = 1
        await client.register_state_update_callback(on_update)
        res = asyncio.Future()
        await client.connect_handler(res)

        assert isinstance(res.exception(), OSError)
        assert called == [client]

    data_output_result = [
        ({"b": 2, "a": 1}, False, {"b": 2, "a": 1}),
        ({"b": 2, "a": 1}, True, '{\n    "a": 1,\n    "b": 2\n}'),
    ]

    @pytest.mark.parametrize("payload, json_output, expected", data_output_result)
    async def test_output_result(self, payload, json_output, expected):
        client = await WebOsClient.create("x", states=[], client_key="x")
        result = client._WebOsClient__output_result(payload, json_output)
        assert result == expected

    data_state_setters = [
        ("set_power_state", {"state": "Power On"}, "_power_state", {"state": "Power On"}),
        ("set_current_app_state", "com.app.test", "_current_appId", "com.app.test"),
        ("set_muted_state", True, "_muted", True),
        ("set_volume_state", 42, "_volume", 42),
        ("set_channels_state", ["ch1", "ch2"], "_channels", ["ch1", "ch2"]),
        ("set_current_channel_state", "ch1", "_current_channel", "ch1"),
        ("set_channel_info_state", {"channelId": "ch1"}, "_channel_info", {"channelId": "ch1"}),
        ("set_apps_state", {"launchPoints": [{"id": "app1", "name": "App 1"}]}, "_apps", {"app1": {"id": "app1", "name": "App 1"}}),
        ("set_inputs_state", [{"appId": "in1", "label": "Input 1"}], "_extinputs", {"in1": {"appId": "in1", "label": "Input 1"}}),
        ("set_sound_output_state", "arc", "_sound_output", "arc"),
        ("set_picture_settings_state", {"brightness": 50}, "_picture_settings", {"brightness": 50}),
    ]

    @pytest.mark.parametrize("method_name, payload, attr, expected", data_state_setters)
    async def test_state_setters_update_internal_state(self, method_name, payload, attr, expected):
        client = await WebOsClient.create("x", states=[], client_key="x")
        method = getattr(client, method_name)
        await method(payload)
        assert getattr(client, attr) == expected

    async def test_register_unregiser_and_clear_callbacks(self):
        client = await WebOsClient.create("x", states=[], client_key="x")
        client.doStateUpdate = True
        calls = []

        async def callback(value):
            calls.append(value)

        await client.register_state_update_callback(callback)
        assert calls == [client]

        client.unregister_state_update_callback(callback)
        assert callback not in client.state_update_callbacks

        client.clear_state_update_callbacks()
        assert client.state_update_callbacks == []

    async def test_print_sleep_and_do_state_update_callbacks(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")

        captured = []

        async def cb(value):
            captured.append(value)

        client.state_update_callbacks = [cb]
        client.doStateUpdate = True

        sleep_mock = mocker.patch("asyncio.sleep", new_callable=mocker.AsyncMock)
        await client.sleep(0.25)
        await client.do_state_update_callbacks()

        sleep_mock.assert_awaited_once_with(0.25)
        assert captured == [client]

        await client.print("hello")

    data_simple_request_methods = [
        ("get_power_state", ep.GET_POWER_STATE, {"state": "Power On"}, {"state": "Power On"}),
        ("get_apps", ep.GET_APPS, {"launchPoints": [{"id": "app1"}]}, [{"id": "app1"}]),
        ("get_apps_all", ep.GET_APPS_ALL, {"apps": [{"id": "app2"}]}, [{"id": "app2"}]),
        ("get_current_app", ep.GET_CURRENT_APP_INFO, {"appId": "app3"}, "app3"),
        ("get_services", ep.GET_SERVICES, {"services": [{"id": "svc"}]}, [{"id": "svc"}]),
        ("get_software_info", ep.GET_SOFTWARE_INFO, {"software": "ok"}, {"software": "ok"}),
        ("get_system_info", ep.GET_SYSTEM_INFO, {"model_name": "x"}, {"model_name": "x"}),
        ("get_hello_info", None, {"hello": "ok"}, {"hello": "ok"}),
        ("get_inputs", ep.GET_INPUTS, {"devices": [{"appId": "in1"}]}, [{"appId": "in1"}]),
        ("get_audio_status", ep.GET_AUDIO_STATUS, {"mute": True}, {"mute": True}),
        ("get_channels", ep.GET_TV_CHANNELS, {"channelList": [{"id": "1"}]}, [{"id": "1"}]),
        ("get_channel_info", ep.GET_CHANNEL_INFO, {"channelId": "1"}, {"channelId": "1"}),
        ("get_sound_output", ep.GET_SOUND_OUTPUT, {"soundOutput": "arc"}, "arc"),
        ("get_calibration_info", None, {"lut3d": 17, "dovi": 2019}, {"lut3d": 17, "dovi": 2019}),
    ]

    @pytest.mark.parametrize("method_name, endpoint, request_result, expected", data_simple_request_methods)
    async def test_simple_request_methods(self, mocker, method_name, endpoint, request_result, expected):
        client = await WebOsClient.create("x", states=[], client_key="x")
        if method_name == "get_hello_info":
            client._hello_info = request_result
        elif method_name == "get_calibration_info":
            client._calibration_info = request_result
        else:
            mocker.patch.object(client, "request", return_value=request_result)

        result = await getattr(client, method_name)()
        if method_name in {"get_power_state", "get_apps", "get_apps_all", "get_services", "get_software_info", "get_system_info", "get_hello_info", "get_calibration_info", "get_inputs", "get_channels", "get_channel_info"}:
            assert result == expected
        else:
            assert result == expected

        if endpoint is not None and method_name != "get_hello_info" and method_name != "get_calibration_info":
            client.request.assert_called_once_with(endpoint)

    data_input_commands = [
        ("button", ("ok",), {"type": "button", "name": "ok"}),
        ("move", (10, 20), {"type": "move", "dx": 10, "dy": 20, "down": 0}),
        ("click", (), {"type": "click"}),
        ("scroll", (10, 20), {"type": "scroll", "dx": 10, "dy": 20}),
    ]

    @pytest.mark.parametrize("method_name, args, expected_message", data_input_commands)
    async def test_button_like_input_commands(self, mocker, method_name, args, expected_message):
        client = await WebOsClient.create("x", states=[], client_key="x")
        mock_input = mocker.patch.object(client, "input_command", new_callable=mocker.AsyncMock)

        if method_name == "button":
            await client.button(args[0], checkValid=False)
        else:
            await getattr(client, method_name)(*args)

        mock_input.assert_awaited_once()
        message = mock_input.await_args.args[0]
        assert expected_message["type"] in message
        for key, val in expected_message.items():
            if key == "type":
                assert f"type:{val}" in message
            elif key == "name":
                assert f"name:{val}" in message
            else:
                assert f"{key}:{val}" in message

    async def test_send_message_includes_icon_data(self, tmp_path):
        client = await WebOsClient.create("x", states=[], client_key="x")
        icon = tmp_path / "icon.png"
        icon.write_bytes(b"abcd")

        expected_payload = {
            "message": "hello",
            "iconData": base64.b64encode(b"abcd").decode("ascii"),
            "iconExtension": "png",
        }

        async def fake_request(uri, payload=None, cmd_type="request", uid=None):
            assert uri == ep.SHOW_MESSAGE
            assert payload == expected_payload
            return {"returnValue": True}

        client.request = fake_request
        result = await client.send_message("hello", str(icon))

        assert result == {"returnValue": True}

    data_singleton_helpers = [
        ("get_input", "app1", ep.GET_CURRENT_APP_INFO, {"appId": "app1"}),
        ("set_input", "hdmi1", ep.SET_INPUT, {"inputId": "hdmi1"}),
        ("turn_3d_on", None, ep.SET_3D_ON, None),
        ("turn_3d_off", None, ep.SET_3D_OFF, None),
        ("play", None, ep.MEDIA_PLAY, None),
        ("pause", None, ep.MEDIA_PAUSE, None),
        ("stop", None, ep.MEDIA_STOP, None),
        ("close", None, ep.MEDIA_CLOSE, None),
        ("rewind", None, ep.MEDIA_REWIND, None),
        ("fast_forward", None, ep.MEDIA_FAST_FORWARD, None),
        ("send_enter_key", None, ep.SEND_ENTER, None),
        ("send_delete_key", None, ep.SEND_DELETE, None),
        ("open_url", "https://example.com", ep.OPEN, {"target": "https://example.com"}),
        ("close_web", None, ep.CLOSE_WEB_APP, None),
    ]

    @pytest.mark.parametrize("method_name, arg, endpoint, payload", data_singleton_helpers)
    async def test_singleton_request_helpers(self, mocker, method_name, arg, endpoint, payload):
        client = await WebOsClient.create("x", states=[], client_key="x")
        request_mock = mocker.patch.object(client, "request", return_value={"returnValue": True})

        if method_name == "get_input":
            result = await client.get_input()
            assert result is None
        elif method_name == "set_input":
            await client.set_input(arg)
        else:
            if arg is None:
                await getattr(client, method_name)()
            else:
                await getattr(client, method_name)(arg)

        if method_name == "get_input":
            request_mock.assert_called_once_with(ep.GET_CURRENT_APP_INFO)
        elif payload is None:
            request_mock.assert_called_once_with(endpoint)
        else:
            request_mock.assert_called_once_with(endpoint, payload)

    async def test_set_device_info_and_reboot_and_settings(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")
        request_mock = mocker.patch.object(
            client,
            "request",
            side_effect=[
                {"returnValue": True},
                {"returnValue": True},
                {"returnValue": True},
                {"returnValue": True},
                {"settings": {"brightness": 50}},
                {"settings": {"brightness": 50}},
                {"configs": {"tv.model.*": "X"}},
            ],
        )

        await client.set_device_info("HDMI_1", "HDMI_1", "PC")
        await client.reboot()
        await client.set_system_settings("picture", {"pictureMode": "vivid"}, current_app=True)
        await client.set_system_picture_mode("vivid")
        await client.get_system_settings("picture", ["brightness"], jsonOutput=True)
        await client.get_picture_settings(["brightness"], jsonOutput=True)
        await client.get_configs(["tv.model.*"], jsonOutput=True)

        assert request_mock.call_count == 7

    data_luna_helpers = [
        ("set_device_info_luna", ("HDMI_1", "HDMI_1", "PC"), ep.LUNA_SET_DEVICE_INFO, {"id": "HDMI_1", "icon": "HDMI_1.png", "label": "PC"}),
        ("set_current_picture_mode", ("vivid",), ep.LUNA_SET_SYSTEM_SETTINGS, {"category": "picture", "settings": {"pictureMode": "vivid"}}),
        ("set_picture_mode", ("vivid", "hdmi1", "hdr", "3d", "picture"), ep.LUNA_SET_SYSTEM_SETTINGS, {"category": "picture$hdmi1.x.3d.hdr", "settings": {"pictureMode": "vivid"}}),
        ("set_picture_settings", ({"brightness": 50}, "vivid", "hdmi1", "2d", "picture", True), ep.LUNA_SET_SYSTEM_SETTINGS, {"category": "picture$hdmi1.vivid.2d.x", "settings": {"brightness": 50}, "current_app": True}),
        ("set_settings", ("picture", {"pictureMode": "vivid"}, True), ep.LUNA_SET_SYSTEM_SETTINGS, {"category": "picture", "settings": {"pictureMode": "vivid"}, "current_app": True}),
        ("enable_tpc_or_gsr", ("tpc", True), ep.LUNA_SET_TPC, {"enable": True}),
        ("set_sm_white_balance", ("warm", 10, 20, 30, 40, 50, 60), ep.LUNA_SET_WHITE_BALANCE, {"colorTemp": "warm", "gain": [10, 20, 30], "offset": [40, 50, 60]}),
        ("set_usb_dolby_vision_config", ("Update",), ep.LUNA_SET_PQ_PROPERTIES, {"dolbyCfgAlertReturn": "Update"}),
        ("set_configs", ({"tv.model.motionProMode": "OLED Motion"},), ep.LUNA_SET_CONFIGS, {"configs": {"tv.model.motionProMode": "OLED Motion"}}),
        ("show_screen_saver", (), ep.LUNA_TURN_ON_SCREEN_SAVER, {}),
        ("reboot_soft", ("",), ep.LUNA_REBOOT_TV, {"reason": "remoteKey"}),
        ("eject_attached_device", ("dev1",), ep.LUNA_EJECT_DEVICE, {"deviceId": "dev1"}),
    ]

    @pytest.mark.parametrize("method_name, args, endpoint, payload", data_luna_helpers)
    async def test_luna_helpers(self, mocker, method_name, args, endpoint, payload):
        client = await WebOsClient.create("x", states=[], client_key="x")
        request_mock = mocker.patch.object(client, "luna_request", return_value={"returnValue": True})

        await getattr(client, method_name)(*args)
        request_mock.assert_called_once_with(endpoint, payload)

    data_simple_media_helpers = [
        ("get_muted", {"mute": True}, True),
        ("set_mute", True, True),
        ("get_volume", {"volumeStatus": {"volume": 22}}, 22),
        ("set_volume", 18, 18),
        ("get_current_channel", {"channelId": "1"}, {"channelId": "1"}),
    ]

    @pytest.mark.parametrize("method_name, request_value, expected", data_simple_media_helpers)
    async def test_audio_and_channel_helpers(self, mocker, method_name, request_value, expected):
        client = await WebOsClient.create("x", states=[], client_key="x")
        request_mock = mocker.patch.object(client, "request", return_value=request_value)

        if method_name in {"get_muted", "get_volume", "get_current_channel"}:
            result = await getattr(client, method_name)()
            assert result == expected
        elif method_name == "set_mute":
            await client.set_mute(request_value)
            request_mock.assert_called_once_with(ep.SET_MUTE, {"mute": request_value})
        elif method_name == "set_volume":
            await client.set_volume(request_value)
            request_mock.assert_called_once_with(ep.SET_VOLUME, {"volume": request_value})

    async def test_volume_step_and_state_callbacks(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")
        client._sound_output = "external_arc"
        client._volume_step_delay = __import__("datetime").timedelta(milliseconds=5)

        request_mock = mocker.patch.object(client, "request", return_value={"returnValue": True})
        sleep_mock = mocker.patch("asyncio.sleep", new_callable=mocker.AsyncMock)

        await client._volume_step(ep.VOLUME_UP)

        request_mock.assert_called_once_with(ep.VOLUME_UP)
        sleep_mock.assert_awaited_once_with(0.005)

    async def test_get_attached_devices_input_button_and_pickers(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")
        request_mock = mocker.patch.object(client, "request", return_value={"devices": [{"id": "dev1"}]})

        result = await client.get_attached_devices(["usb"], jsonOutput=True)
        assert json.loads(result) == [{"id": "dev1"}]
        await client.input_button()
        request_mock.assert_any_call(ep.LIST_DEVICES, {"deviceType": ["usb"]})
        request_mock.assert_any_call(ep.SHOW_INPUT_PICKER, {})

    async def test_get_system_settings_and_configs_for_json_output(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")
        response = {"settings": {"brightness": 50}, "configs": {"x": 1}}
        request_mock = mocker.patch.object(client, "request", return_value=response)

        result = await client.get_system_settings("picture", ["brightness"], jsonOutput=True)
        assert json.loads(result) == response

        result = await client.get_picture_settings(["brightness"], jsonOutput=True)
        assert json.loads(result) == {"brightness": 50}

        result = await client.get_configs(["tv.model.*"], jsonOutput=True)
        assert json.loads(result) == response

        assert request_mock.call_count == 3

    async def test_subscribe_helpers_and_callback_wrappers(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")

        async def fake_subscribe(callback, uri, payload=None):
            return {"returnValue": True}

        mock_subscribe = mocker.patch.object(client, "subscribe", side_effect=fake_subscribe)

        called = []

        async def cb(payload):
            called.append(payload)

        await client.subscribe_power(cb)
        await client.subscribe_apps(cb)
        await client.subscribe_inputs(cb)
        await client.subscribe_muted(cb)
        await client.subscribe_volume(cb)
        await client.subscribe_channels(cb)
        await client.subscribe_current_channel(cb)
        await client.subscribe_channel_info(cb)
        await client.subscribe_sound_output(cb)
        await client.subscribe_picture_settings(cb)

        assert mock_subscribe.call_count == 10

    async def test_luna_request_invalid_alert_id_raises(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")
        mocker.patch.object(client, "request", return_value={})

        with pytest.raises(Exception):
            await client.luna_request("test.uri", {"a": 1})

    async def test_enable_tpc_or_gsr_validation(self):
        client = await WebOsClient.create("x", states=[], client_key="x")

        with pytest.raises(ValueError):
            await client.enable_tpc_or_gsr("bad")

        with pytest.raises(ValueError):
            await client.enable_tpc_or_gsr("tpc", enable="yes")

    async def test_set_sm_white_balance_validation(self):
        client = await WebOsClient.create("x", states=[], client_key="x")

        with pytest.raises(ValueError):
            await client.set_sm_white_balance("bad", 1, 1, 1)

        with pytest.raises(ValueError):
            await client.set_sm_white_balance("warm", -1, 1, 1)

    async def test_set_usb_dolby_vision_config_validation(self):
        client = await WebOsClient.create("x", states=[], client_key="x")

        with pytest.raises(ValueError):
            await client.set_usb_dolby_vision_config("Bad")

    async def test_set_configs_and_screen_saver_and_reboot_soft(self, mocker):
        client = await WebOsClient.create("x", states=[], client_key="x")
        request_mock = mocker.patch.object(client, "luna_request", return_value={"returnValue": True})

        await client.set_configs({"tv.model.motionProMode": "OLED Motion"})
        await client.show_screen_saver()
        await client.reboot_soft()
        await client.eject_attached_device("dev1")

        assert request_mock.call_count == 4

    data_calibration_support_info = [
        ( 'HE_DTV_W99H_XXXXXXXX',   {"foo": "17pt", "dovi": "2019" },   None,   2019,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "foo", "dovi": "2019" },  None,   2019,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt", "foo": "2019" },  17,     None,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt", "dovi": "foo" },  17,     None,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt" },                 17,     None,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"dovi": "2019" },                  None,   2019,   0 ),

        ( 'HE_DTV_W99H_XXXXXXXX',   {"foo": "17pt", "foo": "2019" },    None,   None,   1 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "foo", "dovi": "foo" },   None,   None,   1 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt", "dovi": "2019" }, 17,     2019,   1 ),
        ( 'HE_DTV_W99O_XXXXXXXX',   {"lut3d": "33pt", "dovi": "2019" }, 33,     2019,   1 ),
        ( None,                     {"lut3d": "17pt", "dovi": "2019" }, 17,     2019,   1 ),
        ( None,                     {"lut3d": "33pt", "dovi": "2019" }, 33,     2019,   1 ),

        ( 'HE_DTV_W17H_XXXXXXXX',   None,                               None,   None,   1 ),
        ( 'HE_DTV_W17O_XXXXXXXX',   None,                               None,   None,   1 ),

        ( 'HE_DTV_W18H_XXXXXXXX',   None,                               17,     2018,   1 ),
        ( 'HE_DTV_W18O_XXXXXXXX',   None,                               33,     2018,   1 ),

        ( 'HE_DTV_W19H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W19O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W20H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W20O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W21H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W21O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W22H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W22O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W23H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W23O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W24H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W24G_XXXXXXXX',   None,                               33,     2019,   1 ),
        ( 'HE_DTV_W24O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W25H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W25G_XXXXXXXX',   None,                               33,     2019,   1 ),
        ( 'HE_DTV_W25O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W26H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W26G_XXXXXXXX',   None,                               33,     2019,   1 ),
        ( 'HE_DTV_W26O_XXXXXXXX',   None,                               33,     2019,   1 ),
    ]

    @pytest.mark.parametrize("model,calInfo,lut3d,dovi,expected", data_calibration_support_info)
    async def test_calibration_support_info(self, model, calInfo, lut3d, dovi, expected):
        client = await WebOsClient.create("x", states=["software_info"], calibration_info=calInfo, client_key="x")
        client._software_info = {"model_name" : model}
        client.calibration_support_info()

        if expected > 0:
            cal_info = {
                "lut3d":    lut3d,
                "dovi":     dovi,
            }
        else:
            cal_info = {}
            if lut3d:
                cal_info["lut3d"] = lut3d
            if dovi:
                cal_info["dovi"] = dovi

        assert cal_info == client._calibration_info

