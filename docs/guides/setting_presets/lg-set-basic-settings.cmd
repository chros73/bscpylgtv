@echo off
REM set working directory to the current one
cd "%~dp0"
call lg_constants.cmd

REM Config basic settings

%mcmd% print "### eco ###" , ^
set_system_picture_mode eco , ^
sleep 3 , ^
 ^
print "# Set OLED Light to 0, disable Reduce Blue Light, Filmmaker Mode Auto Start, Screen Move, Logo Luminance Adjust, Energy Saving, Warning on changing preset for the first time" , ^
set_settings picture "{\"backlight\": \"0\", \"eyeComfortMode\": \"off\", \"filmMakerMode\": \"off\", \"screenShift\": \"off\", \"logoLuminanceAdjust\": \"off\", \"energySaving\": \"off\", \"energySavingModified\": \"true\", \"erpUserConfirm\": true}" , ^
sleep 2 , ^
button ENTER , ^
 ^
print "# Set Aspect Ratio to Original, Just Scan to On" , ^
set_system_settings aspectRatio "{\"arcPerApp\": \"original\", \"justScan\": \"on\"}" , ^
 ^
print "# Set UHD Deep color to 4K, Simplink/CEC to On, disable Displaying LG logo and OLED Care settings" , ^
set_settings other "{\"uhdDeepColor\": \"4k\", \"simplinkEnable\": \"on\", \"simplinkAutoPowerOn\": \"on\", \"lgLogoDisplay\": \"off\", \"oledCareMode\": \"off\", \"oledCareRecommendation\": \"off\", \"contentRecommendation\": \"off\"}" , ^
sleep 2 , ^
button ENTER , ^
 ^
print "# Disable QuickStart+, Live Plus, Live Promotion, Settings Help, Set Pointer size and speed" , ^
set_settings option "{\"quickStartMode\": \"off\", \"livePlus\": \"off\", \"livePromotion\": \"off\", \"helpOnSettings\": \"off\", \"pointerSize\": \"small\", \"pointerSpeed\": \"fast\"}" , ^
 ^
print "# Audio to eARC, Bitstream, Passthrough" , ^
set_settings sound "{\"soundOutput\": \"external_arc\", \"digitalAudioPriority\": \"auto\", \"avSyncBypassInput\": \"on\", \"inputAudioFormatHDMI2\": \"bitstream\", \"soundOutputDigital\": \"passThrough\", \"eArcSupport\": \"on\"}" , ^
 ^
print "# Disable IPv6, enable WakeOnLan" , ^
set_settings network "{\"ipv6Enable\": \"false\", \"wolwowlOnOff\": \"true\"}" , ^
 ^
print "# Disable No Signal Image, enable Limit Ad Tracking, disable AI Smart Tips, Smart Tips in Settings, Home Promotion, Screen Saver Promotion, Home Auto launch" , ^
set_settings general "{\"noSignalScreenSaver\": \"off\", \"lmt\": \"on\", \"aiNudge\": \"off\", \"aiSettingsNudge\": \"off\", \"homePromotion\": \"off\", \"screenSaverAd\": \"off\", \"homeAutoLaunch\": \"off\", \"selectedInputApp\": \"off\", \"checkHomeAutoLaunchValue\": \"user\"}" , ^
 ^
print "# Disbale Auto Firmware Update" , ^
set_system_settings support "{\"automaticUpdate\": \"off\"}" , ^
 ^
print "# Set Auto Power Off to 4 hours" , ^
set_settings time "{\"automaticStandBy\": \"4\", \"autoOff2HourOnTimer\": \"on\"}"

