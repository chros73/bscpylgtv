@echo off
REM set working directory to the current one
cd "%~dp0"
call lg_constants.cmd

REM Config all SDR presets to oled light 34, gamma 2.4, except for:
REM     - eco:         0  (51n), gamma 2.4
REM     - game:       34 (118n), gamma 2.2
REM     - cinema:     84 (234n), gamma 2.4, upload gamma 2.68 3D LUT for night
REM     - filmMaker:  84 (234n), gamma 2.4, upload gamma 2.48 3D LUT for day
REM     - expert1:    43 (138n), gamma 2.2, upload gamma 2.20 3D LUT for day
REM     - expert2:    34 (118n), gamma 2.4, upload gamma 2.40 3D LUT for night

%mcmdf% print "### vivid ###" , ^
set_system_picture_mode vivid , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"34\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### normal ###" , ^
set_system_picture_mode normal , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"34\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### eco ###" , ^
set_system_picture_mode eco , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"0\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### sports ###" , ^
set_system_picture_mode sports , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"34\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### game ###" , ^
set_system_picture_mode game , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"34\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### cinema ###" , ^
set_system_picture_mode cinema , ^
sleep 3 , ^
start_calibration cinema , ^
sleep 3 , ^
set_bypass_modes_sdr , ^
sleep 3 , ^
upload_3d_lut_bt709_from_file "sdr-cinema-g268-o84-234n-33p-3dlut.cube" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"84\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### filmMaker ###" , ^
set_system_picture_mode filmMaker , ^
sleep 3 , ^
start_calibration filmMaker , ^
sleep 3 , ^
set_bypass_modes_sdr , ^
sleep 3 , ^
upload_3d_lut_bt709_from_file "sdr-cinema-g248-o84-234n-33p-3dlut.cube" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"84\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### expert1 ###" , ^
set_system_picture_mode expert1 , ^
sleep 3 , ^
start_calibration expert1 , ^
sleep 3 , ^
set_bypass_modes_sdr , ^
sleep 3 , ^
upload_3d_lut_bt709_from_file "sdr-expert1-g220-o43-138n-33p-3dlut.cube" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"43\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3

REM Script is too long it needs to be split up in 2 parts
%mcmdf% print "### expert2 ###" , ^
set_system_picture_mode expert2 , ^
sleep 3 , ^
start_calibration expert2 , ^
sleep 3 , ^
set_bypass_modes_sdr , ^
sleep 3 , ^
upload_3d_lut_bt709_from_file "sdr-expert2-g240-o34-118n-33p-3dlut.cube" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_system_settings picture "{\"backlight\": \"34\", \"contrast\": \"85\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"off\", \"gamma\": \"high1\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
set_system_picture_mode eco

