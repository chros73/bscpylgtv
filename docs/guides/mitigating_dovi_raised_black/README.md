## Mitigating DoVi raised black with custom 1D LUT (with or without calibration)

This method can be used on all affected models that support calibration API and if it works properly.

Other known methods have side effects (the best method is on the top of the list):
- setting WB 2pt Low to -2 : darkens the lower end of gamma that can't be corrected with WB 22pt High controls
- setting black level to 49 : shrinks the dynamic range (similar to the source level toggle of MadVR)
- setting contrast to 99 : modifies the hue

### 0. Reset UI settings
Reset UI settings to default in DoVi Cinema preset to have a "clear" 1D LUT (it's still postprocessed)

### 1. Get 1D LUT from the TV
Get the 1D LUT from the TV into file `dovi_cinema_factory.1dlut`:
```sh
bscpylgtvcommand 192.168.1.18 start_calibration dolby_cinema_dark
# Reset any uploaded 1dlut, just in case
bscpylgtvcommand 192.168.1.18 upload_1d_lut []
bscpylgtvcommand 192.168.1.18 get_1d_lut "dovi_cinema_factory.1dlut"
```

Note about start_calibration command: it auto sets the color temperature to Warm (50)! If you use Cool preset in SM then you have to modify it back to Cold (50) before the `get_1d_lut` command!

### 2. Convert it into a 23pt ArgyllCMS cal file
Convert it into a 23pt ArgyllCMS cal file that can be used along with calibration softwares (HCFR/ColorSpace,  iTPG/PGenerator):
```sh
bscpylgtvcommand 192.168.1.18 convert_1dlut_to_cal "dovi_cinema_factory.1dlut" "dovi_cinema_factory.cal"
```

### 3. Calibration
Modify the RGB values (2nd-4th columns) in the `cal` file 1 by 1, just as you would do with the 22pt WB High controls, then upload it, rinse and repeat:
```sh
bscpylgtvcommand 192.168.1.18 upload_1d_lut_from_file "dovi_cinema_calibrated.cal"
```

### 4. Convert the final calibrated cal file into 1D LUT format
Convert the final calibrated cal file into 1D LUT format to be able to modify values in it easily:
```sh
bscpylgtvcommand 192.168.1.18 convert_cal_to_1dlut "dovi_cinema_calibrated.cal" "dovi_cinema_calibrated.1dlut"
```

### 5. Manually modifying 1D LUT
Make a copy of the calibrated 1D LUT file (e.g. `dovi_cinema_calibrated-mod.1dlut`) modify the first couple of RGB values manually in it by trying out different values in a pitch black room and check with patterns/full black sample that which ones gives you proper black by uploading it, then rinse and repeat:
```sh
bscpylgtvcommand 192.168.1.18 upload_1d_lut_from_file "dovi_cinema_calibrated-mod.1dlut"
```

### 6. End calibration
Quit calibration mode, once you get the desired result:
```sh
bscpylgtvcommand 192.168.1.18 end_calibration
# set color gamut back to native from wide
bscpylgtvcommand 192.168.1.18 set_current_picture_settings "{\"colorGamut\": \"native\"}"
```

### 7. Uploading DoVi config file via USB
`Tmax` and `Tprimaries` needs to be updated in the `DolbyVision_UserDisplayConfiguration.txt` file in case of gamma 2.2 calibration, if only white balance adjustment were made then only specify the latter.

Copy the config file into the root of a thumbdrive, plug it into the TV while it's in SDR mode then play a DoVi content (e.g. using any internal app), then a DoVi popup will appear with which the comfig can be updated or reset.

*Important:* if a 1D LUT is uploaded via the calibration API to a given DoVi preset then the DoVi config update popup is disabled via USB. Either you have to update the config beforehand or reset the preset on the UI (or via calibration API), update DoVi config via USB, then upload the 1D LUT again.

### Notes
About step 5., in my case, I had to modify 3 values (2nd-4th) in each RBG color to have perfect black:
```
0 7 7 30 ...
0 7 7 29 ...
0 5 6 20 ...
```
These were the original values for them (from step 4.):
```
0 33 65 98 ...
0 31 61 92 ...
0 24 48 71 ...
```

First, try to 0 out all the 3 values (2nd-4th) in each color (9 altogether), to see how your panel behaves, then you can start moving the values up.
If I set "0 8 8 8 ..." for all of them then I already see raised black, so the 2nd and 3rd values in each color have to be <=7 in my case.

If someone doesn't want to calibrate the display but only fix raised black then just leave steps 2-4 out from the process.

The corrected 1dlut can also be uploaded into other DoVi presets (`dolby_cinema_bright`, `dolby_game`).

