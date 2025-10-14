@echo off
REM set working directory to the current one
cd "%~dp0"
call lg_constants.cmd

REM Config all DoVi presets to be the same:
REM     - dolbyHdrVivid, dolbyHdrStandard: apply the DoVi 2 point Low WB hack along with 22pt adjustment
REM     - dolbyHdrGame, dolbyHdrCinemaBright, dolbyHdrCinema: upload the same 1D LUT (RGB only calibration)

%mcmdf% print "### dolbyHdrVivid ###" , ^
set_system_picture_mode dolbyHdrVivid , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"dolbyPrecisionDetail\": \"off\", \"whiteBalanceMethod\": \"22\", \"whiteBalanceRed\": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \"whiteBalanceGreen\": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \"whiteBalanceBlue\": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"-2\", \"whiteBalanceGreenOffset\": \"-2\", \"whiteBalanceBlueOffset\": \"-2\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceIre\": \"10\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### dolbyHdrStandard ###" , ^
set_system_picture_mode dolbyHdrStandard , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"dolbyPrecisionDetail\": \"off\", \"whiteBalanceMethod\": \"22\", \"whiteBalanceRed\": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \"whiteBalanceGreen\": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \"whiteBalanceBlue\": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"-2\", \"whiteBalanceGreenOffset\": \"-2\", \"whiteBalanceBlueOffset\": \"-2\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceIre\": \"10\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### dolbyHdrGame ###" , ^
set_system_picture_mode dolbyHdrGame , ^
sleep 3 , ^
start_calibration dolby_game , ^
sleep 3 , ^
upload_1d_lut_from_file "dovi\dv_c_0001.1dlut" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"dolbyPrecisionDetail\": \"off\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### dolbyHdrCinemaBright ###" , ^
set_system_picture_mode dolbyHdrCinemaBright , ^
sleep 3 , ^
start_calibration dolby_cinema_bright , ^
sleep 3 , ^
upload_1d_lut_from_file "dovi\dv_c_0001.1dlut" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"dolbyPrecisionDetail\": \"off\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### dolbyHdrCinema ###" , ^
set_system_picture_mode dolbyHdrCinema , ^
sleep 3 , ^
start_calibration dolby_cinema_dark , ^
sleep 3 , ^
upload_1d_lut_from_file "dovi\dv_c_0001.1dlut" , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"native\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"dolbyPrecisionDetail\": \"off\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}"

