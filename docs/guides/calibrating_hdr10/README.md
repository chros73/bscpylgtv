## Calibrating HDR10

During HDR10 calibration we only modify white balance in calibration mode and not 3D LUT (unlike Calman), either adjusting the 22pt white balance controls on the UI or uploading custom 1D LUT.

### 1. Start calibration mode
Start calibration mode:
```sh
bscpylgtvcommand 192.168.1.18 start_calibration hdr_cinema
```

Note about start_calibration command: it auto sets the color temperature to Warm (50)! If you use Cool preset in SM then you have to modify it back to Cold (50) before the `get_1d_lut` command!

### 2. Calibration
Adjust the 22pt white balance controls on the UI with a calibration software either just corretcing white balance or correcting it to gamma 2.2.

### 3. Uploading custom tonemapping parameters
Upload custom tonemapping parameters:
```sh
bscpylgtvcommand 192.168.1.18 set_tonemap_params hdr_cinema 880 1000 75 4000 60 10000 50
```

### 4. End calibration
Quit calibration mode, once you get the desired result:
```sh
bscpylgtvcommand 192.168.1.18 end_calibration
# set color gamut back to auto from wide
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"colorGamut\": \"auto\"}"
```

The last step (setting color gamut back to Auto) is important: since we only deal with white balance calibration and not touching anything 3D LUT related! `start_calibration` command auto-sets this value to `wide`, hence we have to set it back to `auto`, otherwise you will get oversaturated colors.

### Notes
If you want to create 1D LUT instead adjusting 22pt white balance controls on the UI then just follow the steps in the DoVi guide.

