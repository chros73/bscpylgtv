# bscpylgtv
Library to control webOS based LG TV devices. Enhanced and faster version of
 [aiopylgtv](https://github.com/bendavid/aiopylgtv), it can be installed without calibration functionality,
 optimized for command line usage (it looks for the same `.aiopylgtv.sqlite` key config file).

## Requirements
- Python >= 3.8

### Install from package
```bash
# Install lite package without calibration functionality
pip install bscpylgtv
# Instal full package with calibration functionality (requires numpy package)
pip install bscpylgtv[with_calibration]
```

### Install from Source
Run the following command inside this folder:
```bash
# Install lite package without calibration functionality
pip install --upgrade .
# Instal full package with calibration functionality (requires numpy package)
pip install --upgrade .[with_calibration]
```

### Windows binaries
Portable Windows binaries can be found under [releases](https://github.com/chros73/bscpylgtv/releases).

## Examples
Available settings can be found in [docs](https://github.com/chros73/bscpylgtv/tree/master/docs) directory, also available [buttons](https://github.com/chros73/bscpylgtv/tree/master/bscpylgtv/buttons.py).
They can even be more useful when they are paired with other frontend utilities that can run batch files (e.g. [madvr-js-remote](https://github.com/chros73/madvr-js-remote) or [HTWebRemote
](https://github.com/nicko88/HTWebRemote) on Windows).
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
# Turn screen off/on: turn_screen_off [webos_version] (e.g. for older WebOS: turn_screen_off 4)
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
# Take screenshot
bscpylgtvcommand 192.168.1.18 take_screenshot
# Soft reboot the TV in case it is malfunctioning: reboot_soft [webos_version] (e.g. for older WebOS: reboot_soft 4)
bscpylgtvcommand 192.168.1.18 reboot_soft
# Turn the TV off (standby)
bscpylgtvcommand 192.168.1.18 power_off
```

### Optional command line switches

```bash
# -s "[\"<state1>\", "\<state2>\"]" : set states ("software_info" static state is required by some of the calibration commands)
#    values: ["system_info", "software_info", "power", "current_app", "muted", "volume", "apps", "inputs", "sound_output", "picture_settings"]
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt2020_from_file expert1 "test3d-2.cube" -s
bscpylgtvcommand -s "[\"software_info\"]" 192.168.1.18 upload_3d_lut_bt2020_from_file expert1 "test3d-2.cube"
# -c "{\"lut3d\": \"33pt\", \"dovi\": \"2019\"}" : set calibration_info for unsupported chip types (be careful!)
#    values for "lut3d": "17pt", "33pt"
#    values for "dovi": "2018", "2019"
bscpylgtvcommand -c "{\"lut3d\": \"33pt\", \"dovi\": \"2019\"}" 192.168.1.18 upload_3d_lut_bt2020_from_file expert1 "test3d-2.cube"
# -o : getting hello info (e.g. to get unique deviceUUID)
bscpylgtvcommand -o 192.168.1.18 get_hello_info true
# -w : connecting without SSL
bscpylgtvcommand -w 192.168.1.18 button INFO
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

### Subscribed State Updates Example

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

### Using external storage class via scripting

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

## Calibration functionality (in full version)
**WARNING:** *Messing with the calibration data COULD brick your TV in some circumstances, requiring a mainboard replacement. All of the currently implemented functions SHOULD be safe (although they have only been extensively tested for the 2018 Alpha 7/9, 2019/2021/2022 Alpha 9 models), but no guarantees.*

On LG WebOS TVs with Alpha 7 and Alpha 9 chipsets, upload to internal 1D/3D LUTs, resetting factory calibration data uploaded via calibration API, uploading custom tone mapping parameters (>=2019 models), using internal test pattern generator (iTPG, >=2019 models), writing Dolby Vision config file and other calibration commands are supported.

### Calibration commands

Here is a simplified version of the [image processing pipeline](https://displaycalibrations.com/images/LG_OLED_Video_Signal_Chain_Diagram_Picture.png) (there may be other not fully known/understood changes).

Calibration commands can only be run while in calibration mode (controlled by `start_calibration` and `end_calibration`).
Some of the calibration commands aren't used (question mark behind the name of the method) depending on the model/firmware.
Most of the commands can be run in any mode, except for `set_tonemap_params` that is only for HDR10+HLG and `set_dolby_vision_config_data` that is only for Dolby Vision.
Only 3D LUT and Dolby Vision config related commands require `-s` (states) command line switch (or the use of `-c` (calibration_info) instead for unsuppported chip types if other calibration commands work fine, but be very careful!).
In general, `set_1d_en_*` (de-gamma, re-gamma) and `set_3by3_gamut_data_*` (3x3 color matrices) commands should only be used with unity/custom 3D LUT.

The following commands are supported via calibration API:
```
start_calibration, end_calibration,
set_oled_light, set_contrast, set_brightness, set_color
upload_1d_lut, upload_1d_lut_from_file, set_1d_lut_en (?),
upload_3d_lut_bt709, upload_3d_lut_bt709_from_file, upload_3d_lut_bt2020, upload_3d_lut_bt2020_from_file, 
set_1d_en_2_2, set_1d_en_0_45,
set_3by3_gamut_data_bt709, set_3by3_gamut_data_bt2020, set_3by3_gamut_data_hdr (only used in 2019 models), set_3by3_gamut_data_from_file, set_3by3_gamut_en (?),
set_tonemap_params (for HDR10 picture modes),
set_dolby_vision_config_data (not recommended on >=2020 models!)
```

Combined commands for setting bypass modes and resetting factory data:
```
set_bypass_modes_sdr, set_bypass_modes_hdr10, set_bypass_modes_dovi,
reset_factory_data_sdr, reset_factory_data_hdr10, reset_factory_data_dovi
```

Calibration data is specific to each picture mode, and picture modes are independent for SDR, HDR10+HLG, and Dolby Vision.
Picture modes from each of the three groups are only accessible when the TV is in the appropriate mode. Ie to upload calibration data for HDR10 picture modes, one has to send the TV an HDR10 signal or play an HDR10 file, and similarly for Dolby Vision.

Known supported `picture_mode` strings are:
```
SDR: cinema, expert1, expert2, game, technicolorExpert, filmMaker
HDR10(+HLG): hdr_cinema, hdr_game, hdr_technicolorExpert, hdr_filmMaker
DV: dolby_cinema_bright, dolby_cinema_dark, dolby_game
```

For SDR and HDR10 modes there are two 3D LUTs which will be automatically selected depending on the colorspace flags of the signal or content. In principle almost all SDR content should be BT709 and HDR10 content should be BT2020 but there could be nonstandard cases where this is not true.
For Dolby Vision the BT709 3D LUT seems to be active and the only one used.

The supported input formats for LUTs are IRIDAS `.cube` format for both 1D and 3D LUTs, and ArgyllCMS `.cal` files for 1D LUTs.
Models with Alpha 9 use 33 point 3D LUTs, while those with Alpha 7 use 17 points.

When uploading any 1D LUT data, service menu white balance settings are ignored, and gamma, colorspace, and white balance settings in the user menu are greyed out and inaccessible. From 2019 models white balance 2pt values can be set.
While in calibration mode for HDR10 tone mapping is bypassed.

#### Calibration examples

Modifying expert1 SDR preset (ISF Expert Bright Room):
```bash
# Switch to HDMI2 input
bscpylgtvcommand 192.168.1.18 set_input HDMI_2
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration expert1
# Set oled light to 39, contrast to 85, brightness and color to 50
bscpylgtvcommand 192.168.1.18 set_oled_light 39
bscpylgtvcommand 192.168.1.18 set_contrast
bscpylgtvcommand 192.168.1.18 set_brightness
bscpylgtvcommand 192.168.1.18 set_color
# Set SDR bypass mode (also known as DDC reset) including uploading unity 1DLUT
bscpylgtvcommand 192.168.1.18 set_bypass_modes_sdr true -s
# Upload custom 1DLUT from file
bscpylgtvcommand 192.168.1.18 upload_1d_lut_from_file "test.cal"
# Upload custom 3DLUT from file into BT709 slot
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt709_from_file "test3d-1.cube" -s
# Upload custom 3DLUT from file into bt2020 slot
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt2020_from_file "test3d-2.cube" -s
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

Same calibration session via scripting:
```python
import asyncio
from bscpylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.18', states=["software_info"])
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

#### Uploading bypass values (also known as DDC reset)

The following commands are supported via calibration API beside of the the combined `set_bypass_modes_*` commands:
```
upload_1d_lut,
upload_3d_lut_bt709, upload_3d_lut_bt2020,
set_1d_en_2_2, set_1d_en_0_45, set_1d_lut_en (?),
set_3by3_gamut_data_bt709, set_3by3_gamut_data_bt2020, set_3by3_gamut_data_hdr (only used in 2019 models), set_3by3_gamut_en (?),
```

Example usage (all the supported commands have the same syntax):
```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_game
# Upload unity 1DLUT (no extra parameter is required)
bscpylgtvcommand 192.168.1.18 upload_1d_lut
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

#### Resetting factory calibration data uploaded via calibration API

It's possible to reset individual factory calibration data (previously a picture preset reset or factory reset was required for this)
or reset all/most of them with the combined `reset_factory_data_*` commands.
The following commands are supported via calibration API:
```
upload_1d_lut,
upload_3d_lut_bt709, upload_3d_lut_bt2020,
set_1d_en_2_2, set_1d_en_0_45, set_1d_lut_en (?),
set_3by3_gamut_data_bt709, set_3by3_gamut_data_bt2020, set_3by3_gamut_data_hdr (only used in 2019 models), set_3by3_gamut_en (?),
set_tonemap_params (for HDR10 picture modes),
set_dolby_vision_config_data (not recommended on >=2020 models!)
```

Example usage (all the supported commands have the same syntax except for those that require a `picture_mode`):
```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_game
# Restore factory 1DLUT after custom 1DLUT was uploaded (by specifying empty list)
bscpylgtvcommand 192.168.1.18 upload_1d_lut []
# Restore factory tonemapping parameters after custom ones were uploaded (by specifying empty list)
bscpylgtvcommand 192.168.1.18 set_tonemap_params hdr_game []
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

#### Get calibration commands

- NOTE: they can be partially or completely broken (depending on firmware version, picture preset, etc)
- they can be used inside or outside of calibration mode as well
- they return the data of the currently active picture mode
- in case of factory LUTs (sometimes even with custom LUTs as well), they return the post-processed LUTs with all customizations factored in (including customizations via the user settings menu or service menu)

The following commands are supported via calibration API:
```
get_1d_en_2_2, get_1d_en_0_45,
get_3by3_gamut_data, get_3by3_gamut_data_hdr,
get_1d_lut, get_3d_lut
```

Example usage (all the supported commands have the same syntax):
```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_game
# Get 3x3 color matrix (no extra parameter is required)
bscpylgtvcommand 192.168.1.18 get_3by3_gamut_data
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

##### Backup and restore 1D/3D LUTs and 3x3 color matrices

It's possible to backup and resture 1D/3D LUTs and 3x3 color matrices (if the getter interface of the calibration API works fine).

Example usage for backuping:
```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_cinema
# Backup 3x3 color matrix
bscpylgtvcommand 192.168.1.18 get_3by3_gamut_data "hdr_cinema_3x3.matrix"
# Backup 1D LUT
bscpylgtvcommand 192.168.1.18 get_1d_lut "hdr_cinema.1dlut"
# Backup 3D LUT
bscpylgtvcommand 192.168.1.18 get_3d_lut "hdr_cinema.3dlut"
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

Example usage for restoring:
```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_cinema
# Restore 3x3 color matrix
bscpylgtvcommand 192.168.1.18 set_3by3_gamut_data_from_file "bt2020" "hdr_cinema_3x3.matrix"
# Restore 1D LUT
bscpylgtvcommand 192.168.1.18 upload_1d_lut_from_file "hdr_cinema.1dlut"
# Restore 3D LUT
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt2020_from_file "hdr_cinema.3dlut"
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

#### Uploading custom tonemapping parameters for HDR10 presets

- available only on supported models (>=2019)
- parameters (in this order): picture_mode, peak luminance, mastering_peak_1, rolloff_point_1, mastering_peak_2, rolloff_point_2, mastering_peak_3, rolloff_point_3 

```bash
# Start calibration mode
bscpylgtvcommand 192.168.1.18 start_calibration hdr_cinema
# Upload custom tonemapping parameters for HDR10 Cinema preset
bscpylgtvcommand 192.168.1.18 set_tonemap_params hdr_cinema 760 1000 75 4000 60 10000 50
# Or upload custom tonemapping parameters to disable internal tonemapping entirely
bscpylgtvcommand 192.168.1.18 set_tonemap_params hdr_cinema 760 1000 100 4000 100 10000 100
# End calibration mode
bscpylgtvcommand 192.168.1.18 end_calibration
```

### Writing Dolby Vision config file for USB upload

- picture modes: dolby_cinema_bright - 1 (DoVi Cinema Home), dolby_cinema_dark - 2 (DoVi Cinema), dolby_game - 4 (DoVi Game)
- primaries (in this order): xr, yr, xg, yg, xb, yb
- config of 2018 models is different from newer models (>=2019)

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
bscpylgtvcommand 192.168.1.18 set_itpg_patch_window 0 0 0 0 3840 2160 0 0
# Set 5% window green patch on top of the background
bscpylgtvcommand 192.168.1.18 set_itpg_patch_window 0 1023 0 1
# Display the 2 set patches
bscpylgtvcommand 192.168.1.18 toggle_itpg true 2
# Disable the 2 set patches
bscpylgtvcommand 192.168.1.18 toggle_itpg false 0

# Or using "overlay" 5% window green patch on top of the content
bscpylgtvcommand 192.168.1.18 set_itpg_patch_window 0 1023 0 0
# Display the set patch
bscpylgtvcommand 192.168.1.18 toggle_itpg true 1
# Disable the set patch
bscpylgtvcommand 192.168.1.18 toggle_itpg false 0
```

Displaying gradation window:
```bash
# Set black to white gradation window for vertical type
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 0 3 0 0 0 1 1 1
# Display vertical gradation bars
bscpylgtvcommand 192.168.1.18 toggle_itpg true 1 1
# Set black to white gradation window for horizontal type
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 0 1 0 0 0 1 1 1
# Display horizontal gradation bars
bscpylgtvcommand 192.168.1.18 toggle_itpg true 1 2
# Display 2 colored vertical gradation bars at the same time
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 0 3 610 520 230 1 1 1
bscpylgtvcommand 192.168.1.18 set_itpg_gradation_window 1 3 610 50 23 1 1 1
bscpylgtvcommand 192.168.1.18 toggle_itpg true 2 1
# Disable gradation window
bscpylgtvcommand 192.168.1.18 toggle_itpg false 0
```


## Development of `bscpylgtv`

### Adding available settings for newer models

A collection of useful commands and scripts are available under [docs/utils](https://github.com/chros73/bscpylgtv/tree/master/docs/utils) directory to add support for new firmwares in the future and make PRs easier to do.

### Adding new chip type

Only 3D LUT and Dolby Vision config related calibration commands require chip type to be present to work properly, utilising `calibration_support_info` method.
The `model_name` field of the response of `get_software_info` method contains the chip type:
```bash
bscpylgtvcommand 192.168.1.18 get_software_info true
```

### Unit testing

Required extra packages:
```bash
pip install numpy pytest pytest-asyncio pytest-mock
```

Running unit tests against the installed package:
```bash
# Run all the tests in all files in tests/ directory
pytest tests
# Run all the tests in one file
pytest tests/test_webos_client_lite.py
# Run a specific test in one file
pytest tests/test_webos_client_calibration.py -k test_set_ui_data_methods
```


## Forum

Forum [topic](https://forum.doom9.org/showthread.php?t=175007).


## Acknowledgement

Thanks to the following people:
- [TheRealLink](https://github.com/TheRealLink/pylgtv) for the original implementation
- [bendavid](https://github.com/bendavid/aiopylgtv) for lot of modification, especially with calibration functionality
- [Maassoft](https://github.com/Maassoft/ColorControl) for useful ideas
- Hifi4Vision for his invaluable calibration knowledge

