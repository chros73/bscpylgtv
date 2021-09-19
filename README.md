# bscpylgtv
Library to control webOS based LG Tv devices, a basic, smaller and faster version of [aiopylgtv](https://github.com/bendavid/aiopylgtv) 
(without calibration related features), optimized for command line usage 
(it looks for the same `.aiopylgtv.sqlite` key config file).

## Requirements
- Python >= 3.7

## Install from Source
Run the following command inside this folder
```bash
pip install --upgrade .
```

## Examples

```bash
# Get list of apps
bscpylgtvcommand 192.168.1.18 get_apps
# Push info button
bscpylgtvcommand 192.168.1.18 info_button
# Get values of backlight and contrast of the current picture preset (using list)
bscpylgtvcommand 192.168.1.18 get_picture_settings "[\"backlight\", \"contrast\"]"
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
# Turn PC Mode on for HDMI2 (using JSON)
bscpylgtvcommand 192.168.1.18 set_other_settings "{\"hdmiPcMode\": {\"hdmi2\": true}}"
# Launch hidden software updater on older firmwares
bscpylgtvcommand 192.168.1.18 launch_app com.webos.app.softwareupdate
# Launch hidden software updater on newer firmwares, useful to downgrade (using JSON)
bscpylgtvcommand 192.168.1.18 launch_app_with_params com.webos.app.softwareupdate "{\"mode\": \"user\", \"flagUpdate\": true}"
# Activate "OLED Motion Pro" on C9
bscpylgtvcommand 192.168.1.18 set_configs "{\"tv.model.motionProMode\": \"OLED Motion Pro\"}"
# Turn the TV off (standby) (using JSON)
bscpylgtvcommand 192.168.1.18 power_off
```

## Basic Scripting Example

```python
import asyncio
from bscpylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.53')
    await client.connect()
    apps = await client.get_apps()
    for app in apps:
        print(app)

    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
```

## Development of `bscpylgtv`

We use [`pre-commit`](https://pre-commit.com) to keep a consistent code style, so ``pip install pre_commit`` and run
```bash
pre-commit install
```
to install the hooks.

## Forum

Forum [topic](https://forum.doom9.org/showthread.php?t=175007).
