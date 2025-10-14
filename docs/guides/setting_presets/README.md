## Setting presets

These example scripts can be used to set all presets to their desired state after a factory reset or A/V reset (in 3x MUTE button hidden menu).

You have to go through all of them (they are used with a G2 (2022) running WebOS v9 (2024)) and adjust them to your liking based on the available settings doc of the given display or WebOS version.

### 1. Setting basic options
Run one of the `lg-set-basic-settings.*` scripts while the TV is in SDR mode.

### 2. Setting SDR presets
Run one of the `lg-set-SDR-presets.*` scripts while the TV is in SDR mode.

### 3. Setting HDR10 presets
Run one of the `lg-set-HDR10-presets.*` scripts while the TV is in HDR10 mode.

### 4. Setting DoVi presets
Steps:
- update DoVi cfg with `DolbyVision_UserDisplayConfiguration.txt` [via USB](https://github.com/chros73/bscpylgtv#writing-dolby-vision-config-file-for-usb-upload)
- run one of the `lg-set-DoVi-presets.*` scripts while the TV is in DoVi mode

