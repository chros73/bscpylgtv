# aiopylgtv
Library to control webOS based LG Tv devices.

Based on pylgtv library at https://github.com/TheRealLink/pylgtv which is no longer maintained.

## Requirements
- Python >= 3.7

## Install
```bash
pip install aiopylgtv
```

## Install from Source
Run the following command inside this folder
```bash
pip install --upgrade .
```

## Basic Example

```python
import asyncio
from aiopylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.53')
    await client.connect()
    apps = await client.get_apps()
    for app in apps:
        print(app)

    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
```

## Subscribed state updates
A callback coroutine can be registered with the client in order to be notified of any state changes.
```python
import asyncio
from aiopylgtv import WebOsClient

async def on_state_change():
    print("State changed:")
    print(client.current_appId)
    print(client.muted)
    print(client.volume)
    print(client.current_channel)
    print(client.apps)
    print(client.inputs)
    print(client.system_info)
    print(client.software_info)


async def runloop():
    client = await WebOsClient.create('192.168.1.53')
    await client.register_state_update_callback(on_state_change)

    await client.connect()

    print(client.inputs)
    ret = await client.set_input("HDMI_3")
    print(ret)

    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
```

## Calibration functionality
WARNING: Messing with the calibration data COULD brick your TV in some circumstances, requiring a mainboard replacement.
All of the currently implemented functions SHOULD be safe, but no guarantees.

On supported models, calibration functionality and upload to internal LUTs is supported.  The supported input formats for LUTs are IRIDAS .cube format for both 1D and 3D LUTs, and ArgyllCMS .cal files for 1D LUTs.

Not yet supported:
-Dolby Vision config upload
-Custom tone mapping for 2019 models (functionality does not exist on 2018 models)

Supported models:
LG 2019 Alpha 9 G2 OLED R9 Z9 W9 W9S E9 C9 NanoCell SM99
LG 2019 Alpha 7 G2 NanoCell (8000 & higher model numbers)
LG 2018 Alpha 7 Super UHD LED (8000 & higher model numbers)
LG 2018 Alpha 7 OLED B8
LG 2018 Alpha 9 OLED C8 E8 G8 W8

Models with Alpha 9 use 33 point 3D LUTs, while those with Alpha 7 use 17 points.

n.b. this has only been extensively tested for the 2018 Alpha 9 case, so fixes may be needed still for the others.

WARNING:  When running the ddc_reset or uploading LUT data on 2018 models the only way to restore the factory
LUTs and behaviour for a given input mode is to do a factory reset of the TV.
ddc_reset uploads unity 1d and 3d luts and resets oled light/brightness/contrast/color/ to default values (80/50/85/50).
When running the ddc_reset or uploading any 1D LUT data, service menu white balance settings are ignored, and gamma,
colorspace, and white balance settings in the user menu are greyed out and inaccessible.

Calibration data is specific to each picture mode, and picture modes are independent for SDR, HDR10+HLG, and Dolby Vision.
Picture modes from each of the three groups are only accessible when the TV is in the appropriate mode.  Ie to upload
calibration data for HDR10 picture modes, one has to send the TV an HDR10 signal or play an HDR10 file, and similarly
for Dolby Vision.

For SDR and HDR10 modes there are two 3D LUTs which will be automatically selected depending on the colorspace flags of the signal
or content.  In principle almost all SDR content should be bt709 and HDR10 content should be bt2020 but there could be
nonstandard cases where this is not true.

For Dolby Vision the bt709 3d LUT seems to be active and the only one used.

Known supported picMode strings are:
SDR: cinema, expert1, expert2, game, technicolorExpert
HDR10(+HLG): hdr_technicolorExpert, hdr_cinema, hdr_game
DV: dolby_cinema_dark, dolby_cinema_bright, dolby_game

Calibration commands can only be run while in calibration mode (controlled by "start_calibration" and "end_calibration").

While in calibration mode for HDR10 tone mapping is bypassed.
There may be other not fully known/understood changes in the image processing pipeline while in calibration mode.

```python
import asyncio
from aiopylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.53')
    await client.connect()

    await client.set_input("HDMI_2")
    await client.start_calibration(picMode="expert1")
    await client.ddc_reset(picMode="expert1")
    await client.set_oled_light(picMode="expert1", value=26)
    await client.set_contrast(picMode="expert1", value=100)
    await client.upload_1d_lut_from_file(picMode="expert1", filename="test.cal")
    await client.upload_3d_lut_bt709_from_file(picMode="expert1", filename="test3d.cube")
    await client.upload_3d_lut_bt2020_from_file(picMode="expert1", filename="test3d.cube")
    await client.end_calibration(picMode="expert1")

    await client.disconnect()

asyncio.run(runloop())
```

## Development of `aiopylgtv`

We use [`pre-commit`](https://pre-commit.com) to keep a consistent code style, so ``pip install pre_commit`` and run
```bash
pre-commit install
```
to install the hooks.
