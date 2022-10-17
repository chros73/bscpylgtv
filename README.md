# bscpylgtv
Library to control webOS based LG TV devices. Enhanced and faster version of
 [aiopylgtv](https://github.com/bendavid/aiopylgtv), it can be installed without calibration functionality,
 optimized for command line usage (it looks for the same `.aiopylgtv.sqlite` key config file).

## Requirements
- Python >= 3.8

## Install from package
```bash
# Install lite package without calibration functionality
pip install bscpylgtv
# Instal full package with calibration functionality (requires numpy package)
pip install bscpylgtv[with_calibration]
```

## Install from Source
Run the following command inside this folder:
```bash
# Install lite package without calibration functionality
pip install --upgrade .
# Instal full package with calibration functionality (requires numpy package)
pip install --upgrade .[with_calibration]
```

## Windows binary
Portable Windows binaries can be found under [releases](https://github.com/chros73/bscpylgtv/releases).

## Examples
Available settings can be found in [docs](https://github.com/chros73/bscpylgtv/tree/master/docs) directory.
```bash
# Get list of apps (including hidden ones as well)
bscpylgtvcommand 192.168.1.18 get_apps_all true
# Push info button
bscpylgtvcommand 192.168.1.18 button INFO
# Switch to HDMI2 input
bscpylgtvcommand 192.168.1.18 set_input HDMI_2
# Get values of backlight and contrast of the current picture preset (using list)
bscpylgtvcommand 192.168.1.18 get_picture_settings "[\"backlight\", \"contrast\"]" true
# Swtich to SDR ISF Expert Dark picture preset
bscpylgtvcommand 192.168.1.18 set_current_picture_mode expert2
# Set values of backlight and contrast of the current picture preset (using JSON)
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"backlight\": 0, \"contrast\": 85}"
# Turn hdrDynamicToneMapping on in the current HDR10 picture preset (using JSON)
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"hdrDynamicToneMapping\": \"on\"}"
# Set colorGamut to "auto" in the current picture preset (using JSON)
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"colorGamut\": \"auto\"}"
# Set mpegNoiseReduction off in the current picture preset (using JSON)
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"mpegNoiseReduction\": \"off\"}"
# Turn AI Picture Pro on in the current picture preset (using JSON)
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"ai_Picture\": \"on\"}" aiPicture
# Setting EOTF in HDMI Signal Override menu, values: auto, sdrGamma, hdrGamma, st2084, hlg (using JSON)
bscpylgtvcommand 192.168.1.18 set_other_settings "{\"eotf\": \"hlg\"}"
# Turn PC Mode on/off for HDMI2
bscpylgtvcommand 192.168.1.18 set_device_info HDMI_2 pc PC
bscpylgtvcommand 192.168.1.18 set_device_info HDMI_2 hometheater "Home Theatre"
# Launch and close screensaver
bscpylgtvcommand 192.168.1.18 launch_app com.webos.app.screensaver
bscpylgtvcommand 192.168.1.18 close_app com.webos.app.screensaver
# Turn screen off/on: turn_screen_off [webos_version] (e.g. for WebOS v4.x: turn_screen_off 4)
bscpylgtvcommand 192.168.1.18 turn_screen_off
bscpylgtvcommand 192.168.1.18 turn_screen_on
# Display current picture mode settings
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.palm.app.settings "{\"target\": \"PictureMode\"}"
# Launch installation app hidden menu (Hotel Mode, Password change, USB Cloning, Set ID setup, IP Control)
bscpylgtvcommand 192.168.1.18 launch_app com.webos.app.installation
# Display 3x MUTE button hidden menu (AVReset, Customer Support, etc)
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.webos.app.tvhotkey "{\"activateType\": \"mute-hidden-action\"}"
# Display 7x GREEN button hidden Freesync info
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.webos.app.tvhotkey "{\"activateType\": \"freesync-info\"}"
# NOTE: this does not work anymore on some models since end of 2021. Launch hidden software updater on older firmwares
bscpylgtvcommand 192.168.1.18 launch_app com.webos.app.softwareupdate
# NOTE: this does not work anymore on some models since end of 2021. Launch hidden software updater on newer firmwares, useful to downgrade (using JSON)
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.webos.app.softwareupdate "{\"mode\": \"user\", \"flagUpdate\": true}"
# Launch In-Start Service Menu (code: 0413) (using JSON)
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.webos.app.factorywin "{\"id\":\"executeFactory\", \"irKey\":\"inStart\"}"
# Launch Ez-Adjust Service Menu (code: 0413) (using JSON)
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.webos.app.factorywin "{\"id\":\"executeFactory\", \"irKey\":\"ezAdjust\"}"
# Get config values of "tv.model" category (using list)
bscpylgtvcommand 192.168.1.18 get_configs "[\"tv.model.*\"]" true
# Activate "OLED Motion Pro" on C9 (using JSON)
bscpylgtvcommand 192.168.1.18 set_configs "{\"tv.model.motionProMode\": \"OLED Motion Pro\"}"
# Display Total Power On Time under TV Information on EU models where it's hidden (using JSON)
bscpylgtvcommand 192.168.1.18 set_configs "{\"tv.conti.supportUsedTime\": true}"
# Turn the TV off (standby)
bscpylgtvcommand 192.168.1.18 power_off
```

## Optional command line switches

```bash
# -s "[\"<state1>\", "\<state2>\"]" : set states ("system_info" static state is required by some of the calibration commands)
#    values: ["system_info", "software_info", "power", "current_app", "muted", "volume", "apps", "inputs", "sound_output", "picture_settings"]
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt2020_from_file expert1 "test3d-2.cube" -s
bscpylgtvcommand -s "[\"system_info\"]" 192.168.1.18 upload_3d_lut_bt2020_from_file expert1 "test3d-2.cube"
# -o : getting hello info (e.g. to get unique deviceUUID)
bscpylgtvcommand -o 192.168.1.18 get_hello_info true
# -k <client_key> : specifying a client key
bscpylgtvcommand -k ef6858b2133d68854612831e3df8e495 192.168.1.18 button INFO
# -p <path_to_key_file> : specifying path to key file
bscpylgtvcommand -p "D:\config\.aiopylgtv.sqlite" 192.168.1.18 button INFO
# -l : get list of all saved client keys per ip (otionally from a specified key file)
bscpylgtvcommand -l
bscpylgtvcommand -l -p "D:\config\.aiopylgtv.sqlite"
# -v : display version number
bscpylgtvcommand -v
```

## Basic Scripting Example

```python
import asyncio
from bscpylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.18', ping_interval=None, states=[])
    await client.connect()
    apps = await client.get_apps_all()
    for app in apps:
        print(app)

    await client.disconnect()

asyncio.run(runloop())
```

## Subscribed State Updates Example

```python
import asyncio
from bscpylgtv import WebOsClient

async def on_state_change(client):
    print("State changed:")
    print(client.apps)
    print(client.inputs)
    print(client.power_state)
    print(client.current_appId)
    print(client.channels)
    print(client.current_channel)
    print(client.channel_info)
    print(client.muted)
    print(client.volume)
    print(client.sound_output)
    print(client.picture_settings)
    print(client.system_info)
    print(client.software_info)
    print(client.hello_info)

async def runloop():
    client = await WebOsClient.create('192.168.1.18', get_hello_info=True)
    await client.register_state_update_callback(on_state_change)
    await client.connect()

    ret = await client.volume_up()
    print(ret)
    await asyncio.sleep(30)

    await client.disconnect()

asyncio.run(runloop())
```

## Using external storage class via scripting

Replacing built-in `StorageSqliteDict` key storage with custom `StorageMy` class that implements [methods](https://github.com/chros73/bscpylgtv/tree/master/bscpylgtv/storage_proto.py) of `StorageProto` class:
```python
import asyncio
from bscpylgtv import WebOsClient
from storage_my import StorageMy

async def runloop():
    storage = await StorageMy.create("file_path")
    client = await WebOsClient.create('192.168.1.18', ping_interval=None, states=[], storage=storage)
    await client.connect()
    info = await client.get_software_info()
    print(info)

    await client.disconnect()

asyncio.run(runloop())
```

More useful examples can be found in [docs/scripts](https://github.com/chros73/bscpylgtv/tree/master/docs/scripts) directory.

## Calibration functionality (only in full version)
**WARNING:** *Messing with the calibration data COULD brick your TV in some circumstances, requiring a mainboard replacement. All of the currently implemented functions SHOULD be safe, but no guarantees.*

On supported models, calibration functionality, upload to internal LUTs, resetting uploaded data via calibration API, uploading custom tone mapping parameters (>=2019 models), using internal test pattern generator (iTPG, >=2019 models) and writing Dolby Vision config file is supported.

n.b. this has only been extensively tested for the 2018 Alpha 7/9, 2019/2021/2022 Alpha 9 models, so fixes may be needed still for the others.

Supported models (more models can be added via PR once they confirmed working well):
```
LG 2023-25 Alpha 9 Gx: OLED Rx Zx Gx Cx ARTx LXx
LG 2023-25 Alpha 7 Gx: OLED Bx Ax
LG 2022 Alpha 9 G5: OLED R2 Z2 G2 C2 CS ART90 LX1
LG 2022 Alpha 7 G5: OLED B2 A2
LG 2021 Alpha 9 G4: OLED R1 Z1 G1 C1
LG 2021 Alpha 7 G4: OLED B1 A1
LG 2020 Alpha 9 G3: OLED RX ZX WX GX CX
LG 2020 Alpha 7 G3: OLED BX
LG 2019 Alpha 9 G2: OLED R9 Z9 W9 W9S E9 C9 NanoCell SM99
LG 2019 Alpha 7 G2: OLED B9
LG 2019 Alpha 7 G2: NanoCell (8000 & higher model numbers)
LG 2018 Alpha 9 G1: OLED C8 E8 G8 W8
LG 2018 Alpha 7 G1: OLED B8
LG 2018 Alpha 7 G1: Super UHD LED (8000 & higher model numbers)
```

### Calibration commands

The supported input formats for LUTs are IRIDAS `.cube` format for both 1D and 3D LUTs, and ArgyllCMS `.cal` files for 1D LUTs. Models with Alpha 9 use 33 point 3D LUTs, while those with Alpha 7 use 17 points.

*WARNING:* When running the `set_bypass_modes_*` method or uploading LUT data on 2018 models the only way to restore the factory LUTs and behaviour for a given input mode is to do a factory reset of the TV. From 2019 models  picture preset reset results the same until calibration mode is activated again for the same preset.
`set_bypass_modes_*` uploads unity 1d and 3d luts and resets oled light/brightness/contrast/color/ to default values (80/50/85/50).
When running the `set_bypass_modes_*` or uploading any 1D LUT data, service menu white balance settings are ignored, and gamma, colorspace, and white balance settings in the user menu are greyed out and inaccessible. From 2019 models white balance 2pt low values can be set.

Calibration data is specific to each picture mode, and picture modes are independent for SDR, HDR10+HLG, and Dolby Vision.
Picture modes from each of the three groups are only accessible when the TV is in the appropriate mode. Ie to upload calibration data for HDR10 picture modes, one has to send the TV an HDR10 signal or play an HDR10 file, and similarly for Dolby Vision.

For SDR and HDR10 modes there are two 3D LUTs which will be automatically selected depending on the colorspace flags of the signal or content. In principle almost all SDR content should be bt709 and HDR10 content should be bt2020 but there could be nonstandard cases where this is not true. For Dolby Vision the bt709 3d LUT seems to be active and the only one used.

Known supported picMode strings are:
```
SDR: cinema, expert1, expert2, game, technicolorExpert, filmMaker
HDR10(+HLG): hdr_cinema, hdr_game, hdr_technicolorExpert, hdr_filmMaker
DV: dolby_cinema_bright, dolby_cinema_dark, dolby_game
```

Calibration commands can only be run while in calibration mode (controlled by `start_calibration` and `end_calibration`).

While in calibration mode for HDR10 tone mapping is bypassed.
There may be other not fully known/understood changes in the image processing pipeline while in calibration mode.

Calibration command line examples, modifying expert1 SDR preset (ISF Expert Bright Room):
```bash
# Switch to HDMI2 input
bscpylgtvcommand 192.168.1.18 set_input HDMI_2
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration expert1 -s
# Set oled light to 39, contrast to 85, brightness and color to 50
bscpylgtvcommand 192.168.1.18 set_oled_light 39 -s
bscpylgtvcommand 192.168.1.18 set_contrast -s
bscpylgtvcommand 192.168.1.18 set_brightness -s
bscpylgtvcommand 192.168.1.18 set_color -s
# Set SDR bypass mode (also known as DDC reset) including uploading unity 1DLUT
bscpylgtvcommand 192.168.1.18 set_bypass_modes_sdr true -s
# Upload custom 1DLUT from file
bscpylgtvcommand 192.168.1.18 upload_1d_lut_from_file "test.cal" -s
# Upload custom 3DLUT from file into BT709 slot
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt709_from_file "test3d-1.cube" -s
# Upload custom 3DLUT from file into bt2020 slot
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt2020_from_file "test3d-2.cube" -s
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration -s
```

Same calibration via scripting:
```python
import asyncio
from bscpylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.18', states=["system_info"])
    await client.connect()

    await client.set_input("HDMI_2")
    await client.start_calibration(picture_mode="expert1")
    await client.set_oled_light(value=39)
    await client.set_contrast()
    await client.set_brightness()
    await client.set_color()
    await client.set_bypass_modes_sdr(unity_1d_lut=True)
    await client.upload_1d_lut_from_file(filename="test.cal")
    await client.upload_3d_lut_bt709_from_file(filename="test3d-1.cube")
    await client.upload_3d_lut_bt2020_from_file(filename="test3d-2.cube")
    await client.end_calibration()

    await client.disconnect()

asyncio.run(runloop())
```

### Resetting uploaded calibration data via calibration API

Now it's possible to reset individual factory calibration data (previously a picture preset reset or factory reset was required for this) or reset all of them with `set_factory_calibration_data` command.
The following calibration commands are supported:
```
upload_1d_lut, upload_3d_lut_bt709, upload_3d_lut_bt2020,
set_1d_en_2_2, set_1d_en_0_45, set_3by3_gamut_data_bt709, set_3by3_gamut_data_bt2020,
set_tonemap_params (for HDR10 picture modes),
set_dolby_vision_config_data (not recommended on >=2020 models!)
```

Example usage (all the supported commands has the same syntax):
```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration expert1 -s
# Restore factory 1DLUT after custom 1DLUT was uploaded (by specifying empty list)
bscpylgtvcommand 192.168.1.18 upload_1d_lut [] -s
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration -s
```

### Uploading custom tonemapping parameters for HDR10 presets

- available only on supported (>=2019) models

```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_cinema -s
# Upload custom tonemapping parameters for HDR10 Cinema preset
bscpylgtvcommand 192.168.1.18 set_tonemap_params hdr_cinema 760 1000 75 4000 60 10000 50 -s
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration -s
```

### Writing Dolby Vision config file for USB upload

- picture modes: 1 - DoVi Cinema Home, 2 - DoVi Cinema, 4 - DoVi Game
- primaries (in this order): xr, yr, xg, yg, xb, yb
- config of 2018 models is different from the rest of the models

```bash
# Writing DoVi config for one preset (DoVi Cinema)
bscpylgtvcommand 192.168.1.18 write_dolby_vision_config_file "[{\"picture_mode\": \"dolby_cinema_dark\", \"white_level\": 750, \"primaries\": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}]" -s
# Writing DoVi config for all the presets (DoVi Cinema Home, Cinema, Game) based on one set of data
bscpylgtvcommand 192.168.1.18 write_dolby_vision_config_file "[{\"white_level\": 750, \"primaries\": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}]" true D:\temp -s
# Writing DoVi config for all the presets (DoVi Cinema Home, Cinema, Game) by specifying them separately
bscpylgtvcommand 192.168.1.18 write_dolby_vision_config_file "[{\"picture_mode\": \"dolby_cinema_bright\", \"white_level\": 710, \"primaries\": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {\"picture_mode\": \"dolby_cinema_dark\", \"white_level\": 750, \"primaries\": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {\"picture_mode\": \"dolby_game\", \"white_level\": 680, \"primaries\": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}]" -s
```

### Using the internal Test Pattern Generator (iTPG)

- it can be used inside or outside of calibration mode as well
- it can be broken in many defferent ways in a given firmware version / picture mode / etc
- available only on supported (>=2019) models
- 2019 models require Full Range 10 bit values (0-1023) using HDR10, while >=2020 models Limited Range 10 bit values (64-940)
- all suported models require Full Range 10 bit values (0-1023) using DoVi
- more useful example can be found in [docs/scripts](https://github.com/chros73/bscpylgtv/tree/master/docs/scripts/lg-itpg-manual-measure-from-csv.py) directory.

```bash
# Set full screen black window in the background
bscpylgtvcommand 192.168.1.18 set_itpg_patch_window 0 0 0 0 3840 2160 0 0 -s
# Set 5% window green patch on top of the background
bscpylgtvcommand 192.168.1.18 set_itpg_patch_window 0 1023 0 1 -s
# Display the 2 set patches
bscpylgtvcommand 192.168.1.18 toggle_itpg true 2 -s
# Disable the 2 set patches
bscpylgtvcommand 192.168.1.18 toggle_itpg false 0 -s

# Or using "overlay" 5% window green patch on top of the content
bscpylgtvcommand 192.168.1.18 set_itpg_patch_window 0 1023 0 0 -s
# Display the set patch
bscpylgtvcommand 192.168.1.18 toggle_itpg true 1 -s
# Disable the set patch
bscpylgtvcommand 192.168.1.18 toggle_itpg false 0 -s
```

Displaying gradation window:
```bash
# Set black to white gradation window for vertical type
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 0 3 0 0 0 1 1 1 -s
# Display vertical gradation bars
bscpylgtvcommand 192.168.1.18 toggle_itpg true 1 1 -s
# Set black to white gradation window for horizontal type
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 0 1 0 0 0 1 1 1 -s
# Display horizontal gradation bars
bscpylgtvcommand 192.168.1.18 toggle_itpg true 1 2 -s
# Display 2 colored vertical gradation bars at the same time
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 0 3 610 520 230 1 1 1 -s
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 1 3 610 50 23 1 1 1 -s
bscpylgtvcommand 192.168.1.18 toggle_itpg true 2 1 -s
# Disable gradation window
bscpylgtvcommand 192.168.1.18 toggle_itpg false 0 -s
```


## Development of `bscpylgtv`

A collection of useful commands and scripts are available under [docs/utils](https://github.com/chros73/bscpylgtv/tree/master/docs/utils) directory to add support for new firmwares in the future and make PRs easier to do.

We use [`pre-commit`](https://pre-commit.com) to keep a consistent code style, so ``pip install pre_commit`` and run
```bash
pre-commit install
```
to install the hooks.

### Unit testing

Required extra packages:
```bash
pip install numpy pytest pytest-asyncio pytest-mock
```

Running unit tests against the installed package:
```bash
# Run all the tests in all files
pytest tests
# Run all the tests in one file
pytest tests/test_webos_client_lite.py
# Run a specific test in one file
pytest tests/test_webos_client_calibration.py -k "test_set_ui_data_methods"
```


## Forum

Forum [topic](https://forum.doom9.org/showthread.php?t=175007).
