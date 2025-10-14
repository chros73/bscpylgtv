@echo off
REM set working directory to the current one
cd "%~dp0"
call lg_constants.cmd

REM Config all HDR10 presets to be the same:
REM     - apply 22pt WB RGB only calibration
REM     - hdrCinema: set tone mapping params to 870 1000 100 4000 100 10000 100
REM     - hdrFilmMaker: set tone mapping params to 950 1000 100 4000 100 10000 100

%mcmdf% print "### hdrVivid ###" , ^
set_system_picture_mode hdrVivid , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"hdrDynamicToneMapping\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"whiteBalanceMethod\": \"22code\", \"whiteBalanceRed\": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], \"whiteBalanceGreen\": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], \"whiteBalanceBlue\": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"0\", \"whiteBalanceGreenOffset\": \"0\", \"whiteBalanceBlueOffset\": \"0\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceCodeValue\": \"20\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### hdrStandard ###" , ^
set_system_picture_mode hdrStandard , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"hdrDynamicToneMapping\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"whiteBalanceMethod\": \"22code\", \"whiteBalanceRed\": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], \"whiteBalanceGreen\": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], \"whiteBalanceBlue\": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"0\", \"whiteBalanceGreenOffset\": \"0\", \"whiteBalanceBlueOffset\": \"0\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceCodeValue\": \"20\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### hdrCinemaBright ###" , ^
set_system_picture_mode hdrCinemaBright , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"hdrDynamicToneMapping\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"whiteBalanceMethod\": \"22code\", \"whiteBalanceRed\": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], \"whiteBalanceGreen\": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], \"whiteBalanceBlue\": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"0\", \"whiteBalanceGreenOffset\": \"0\", \"whiteBalanceBlueOffset\": \"0\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceCodeValue\": \"20\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### hdrGame ###" , ^
set_system_picture_mode hdrGame , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"hdrDynamicToneMapping\": \"HGIG\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"whiteBalanceMethod\": \"22code\", \"whiteBalanceRed\": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], \"whiteBalanceGreen\": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], \"whiteBalanceBlue\": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"0\", \"whiteBalanceGreenOffset\": \"0\", \"whiteBalanceBlueOffset\": \"0\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceCodeValue\": \"20\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3 , ^
 ^
print "### hdrCinema ###" , ^
set_system_picture_mode hdrCinema , ^
sleep 3 , ^
start_calibration hdr_cinema , ^
sleep 3 , ^
set_tonemap_params hdr_cinema 870 1000 100 4000 100 10000 100 , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"hdrDynamicToneMapping\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"whiteBalanceMethod\": \"22code\", \"whiteBalanceRed\": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], \"whiteBalanceGreen\": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], \"whiteBalanceBlue\": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"0\", \"whiteBalanceGreenOffset\": \"0\", \"whiteBalanceBlueOffset\": \"0\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceCodeValue\": \"20\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}" , ^
sleep 3

REM Script is too long it needs to be split up in 2 parts
%mcmdf% print "### hdrFilmMaker ###" , ^
set_system_picture_mode hdrFilmMaker , ^
sleep 3 , ^
start_calibration hdr_filmMaker , ^
sleep 3 , ^
set_tonemap_params hdr_filmMaker 950 1000 100 4000 100 10000 100 , ^
sleep 3 , ^
end_calibration , ^
sleep 3 , ^
set_settings picture "{\"backlight\": \"100\", \"contrast\": \"100\", \"brightness\": \"50\", \"dynamicContrast\": \"off\", \"hdrDynamicToneMapping\": \"off\", \"peakBrightness\": \"high\", \"gamma\": \"medium\", \"motionEyeCare\": \"off\", \"color\": \"50\", \"tint\": \"0\", \"colorGamut\": \"auto\", \"dynamicColor\": \"off\", \"colorTemperature\": \"-50\", \"sharpness\": \"0\", \"superResolution\": \"off\", \"noiseReduction\": \"off\", \"mpegNoiseReduction\": \"off\", \"smoothGradation\": \"off\", \"realCinema\": \"on\", \"whiteBalanceMethod\": \"22code\", \"whiteBalanceRed\": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], \"whiteBalanceGreen\": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], \"whiteBalanceBlue\": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], \"whiteBalancePoint\": \"low\", \"whiteBalanceRedOffset\": \"0\", \"whiteBalanceGreenOffset\": \"0\", \"whiteBalanceBlueOffset\": \"0\", \"whiteBalanceRedGain\": \"0\", \"whiteBalanceGreenGain\": \"0\", \"whiteBalanceBlueGain\": \"0\", \"whiteBalanceCodeValue\": \"20\"}" , ^
set_system_settings picture "{\"truMotionMode\": \"off\"}" true , ^
set_settings aiPicture "{\"ai_Picture\": \"off\", \"ai_Brightness\": \"off\", \"ai_Genre\": \"off\"}" , ^
set_settings picture "{\"applyToAllInput\": \"picture\"}"


