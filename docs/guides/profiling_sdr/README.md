## Profiling SDR

During profiling SDR we only create 3D LUT and not 1D LUT (unlike Calman).

### 0. Set oled light and gamma
Set oled light and gamma of the given preset to a desired value on the UI, e.g. to achive 120 nits and gamma 2.4.

### 1. Set bypass modes
Set bypass modes in the given preset:
```sh
bscpylgtvcommand 192.168.1.18 start_calibration cinema
bscpylgtvcommand 192.168.1.18 set_bypass_modes_sdr -s
bscpylgtvcommand 192.168.1.18 end_calibration
```

Note about start_calibration command: it auto sets the color temperature to Warm (50)! If you use Cool preset in SM then you have to modify it back to Cold (50)!

### 2. Profiling
Profile the display with DisplayCal and create a "cinema.3dlut" 3D LUT:
- select a css correction file
- set patch sequence to "Maximize RGB difference" under Profiling
- set "IRIDAS (.cube)" as format and 17 (Alpha 7) or 33 (Alpha 9) for size under 3D LUT

### 3. Uploading 3D LUT
Upload the created "cinema.3dlut" 3D LUT:
```sh
bscpylgtvcommand 192.168.1.18 start_calibration cinema
bscpylgtvcommand 192.168.1.18 upload_3d_lut_bt709_from_file "cinema.3dlut" -s
bscpylgtvcommand 192.168.1.18 end_calibration
```

Note about start_calibration command: it auto sets the color temperature to Warm (50)! If you use Cool preset in SM then you have to modify it back to Cold (50)!

