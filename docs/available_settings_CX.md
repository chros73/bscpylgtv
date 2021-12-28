### OLED CX (2020) webOS v5.2.3
Available settings per category that can be used with various methods.

#### Inputs
```
atv, av1, av2, camera, comp1, comp2, comp3, default, dtv, gallery,
hdmi1, hdmi2, hdmi3, hdmi4, hdmi1_pc, hdmi2_pc, hdmi3_pc, hdmi4_pc,
ip, movie, photo, pictest, rgb, scart, smhl
```

#### Picture modes (presets)
```
cinema, eco, expert1, expert2, filmMaker, game, normal, photo, sports, vivid, hdrEffect,
hdrCinema, hdrCinemaBright, hdrExternal, hdrFilmMaker, hdrGame, hdrStandard, hdrVivid,
dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon, dolbyHdrGame, dolbyHdrStandard, dolbyHdrVivid, dolbyStandard
```

#### Dynamic range modes
```
sdr, hdr, technicolorHdr, dolbyHdr,
sdrALLM, hdrALLM, technicolorHdrALLM, dolbyHdrALLM
```

#### Stereoscopic modes
```
2d, 3d
```

#### `aiPicture` category - default settings: `hdmi1` input - `expert2` preset (used by `set_current_picture_settings` method)
```json
    "ai_Brightness": "off",
    "ai_Genre": "off",
    "ai_Picture": "off"
```

#### `picture` category - default settings: `hdmi1` input - `expert2` preset (used by `set_current_picture_settings` method)
```json
    "adjustingLuminance": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "adjustingLuminance10pt": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "ambientLightCompensation": "off",
    "backlight": "80",
    "blackLevel": {
        "ntsc": "auto",
        "ntsc443": "auto",
        "pal": "auto",
        "pal60": "auto",
        "palm": "auto",
        "paln": "auto",
        "secam": "auto",
        "unknown": "auto"
    },
    "brightness": "50",
    "color": "50",
    "colorFilter": "off",
    "colorGamut": "auto",
    "colorManagementColorSystem": "red",
    "colorManagementHueBlue": "0",
    "colorManagementHueCyan": "0",
    "colorManagementHueGreen": "0",
    "colorManagementHueMagenta": "0",
    "colorManagementHueRed": "0",
    "colorManagementHueYellow": "0",
    "colorManagementLuminanceBlue": "0",
    "colorManagementLuminanceCyan": "0",
    "colorManagementLuminanceGreen": "0",
    "colorManagementLuminanceMagenta": "0",
    "colorManagementLuminanceRed": "0",
    "colorManagementLuminanceYellow": "0",
    "colorManagementSaturationBlue": "0",
    "colorManagementSaturationCyan": "0",
    "colorManagementSaturationGreen": "0",
    "colorManagementSaturationMagenta": "0",
    "colorManagementSaturationRed": "0",
    "colorManagementSaturationYellow": "0",
    "colorTemperature": "0",
    "contrast": "80",
    "dynamicColor": "off",
    "dynamicContrast": "off",
    "edgeEnhancer": "on",
    "expertPattern": "off",
    "externalPqlDbType": "none",
    "gamma": "high2",
    "grassColor": "0",
    "hPosition": "0",
    "hSharpness": "10",
    "hSize": "0",
    "hdrDynamicToneMapping": "on",
    "localDimming": "medium",
    "motionEyeCare": "off",
    "motionPro": "off",
    "motionProOLED": "off",
    "mpegNoiseReduction": "off",
    "noiseReduction": "off",
    "peakBrightness": "off",
    "pictureTempKey": "off",
    "realCinema": "on",
    "sharpness": "10",
    "skinColor": "0",
    "skyColor": "0",
    "smoothGradation": "off",
    "superResolution": "off",
    "tint": "0",
    "truMotionBlur": "10",
    "truMotionJudder": "0",
    "truMotionMode": "user",
    "vPosition": "0",
    "vSharpness": "10",
    "vSize": "0",
    "whiteBalanceApplyAllInputs": "off",
    "whiteBalanceBlue": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "whiteBalanceBlue10pt": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "whiteBalanceBlueGain": "0",
    "whiteBalanceBlueOffset": "0",
    "whiteBalanceCodeValue": "21",
    "whiteBalanceCodeValue10pt": "9",
    "whiteBalanceColorTemperature": "warm2",
    "whiteBalanceGreen": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "whiteBalanceGreen10pt": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "whiteBalanceGreenGain": "0",
    "whiteBalanceGreenOffset": "0",
    "whiteBalanceIre": "100",
    "whiteBalanceIre10pt": "100",
    "whiteBalanceLuminance": "130",
    "whiteBalanceMethod": "2",
    "whiteBalancePattern": "outer",
    "whiteBalancePoint": "high",
    "whiteBalanceRed": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "whiteBalanceRed10pt": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ],
    "whiteBalanceRedGain": "0",
    "whiteBalanceRedOffset": "0",
    "xvycc": "auto"
```

#### `option` category - default settings (used by `set_option_settings` method)
```json
    "IPControlSecureKey": "",
    "_3dModeEstreamer": "off",
    "additionalAudioSelection": "none",
    "addressInfo": [
        "not_defined",
        "not_defined",
        "not_defined",
        "not_defined"
    ],
    "adjustments": {
        "blackAndWhite": "off",
        "colorInversion": "off"
    },
    "animationGuide": "on",
    "appInstallDevice": {
        "deviceId": "",
        "driveId": ""
    },
    "appUpdateMode": "manual",
    "audioGuidance": "off",
    "audioGuidancePitch": "medium",
    "audioGuidanceSpeed": "medium",
    "audioGuidanceVolume": "medium",
    "autoComplete": false,
    "autoSmartServiceCountry": "on",
    "avatar": "off",
    "backupPsm": {
        "backupPsm2d": "hdrStandard",
        "backupPsm3d": "hdrStandard"
    },
    "backupPsmDolby": {
        "backupPsm2d": "dolbyHdrDark",
        "backupPsm3d": "dolbyHdrDark"
    },
    "baloonHelp": "on",
    "bannerPosition": "none",
    "broadcastInfoNoti": "on",
    "channelplus": "off",
    "channelplusPopup": "off",
    "cicNumber": [
        {
            "country": "default",
            "number": "none",
            "shortName": "default"
        }
    ],
    "country": "other",
    "countryGroup": "UNDEFINED",
    "countryRegion": "other",
    "curDemoFile": "undefined",
    "dataService": "mheg",
    "demoFileList": "undefined",
    "demoMode": "on",
    "displayMusicWidget": true,
    "eStreamerPosition": "all",
    "emergencyAlert": "on",
    "enableIpControl": "off",
    "enableSDDP": "off",
    "enableToastPopup": "off",
    "enabling3dSettingsMenu": "off",
    "epgPipMode": "off",
    "estreamerMinimalMode": "off",
    "estreamerStatus": "off",
    "firstTvSignalStatus": "undefined",
    "focusedItemEnlarged": "off",
    "freeviewMode": "off",
    "freeviewplay": "off",
    "googleAssistantTTS": "on",
    "graphicSharpnessLevel": 0,
    "hbbTV": "off",
    "hbbTvDeviceId": "on",
    "hbbTvDnt": "off",
    "hddEcoMode": "on",
    "helpOnSettings": "on",
    "highContrast": "off",
    "hybridCast": "off",
    "ibb": "off",
    "ibbDnt": "off",
    "inputDevicesSupportStatus": {
        "keyboard": true,
        "motionSensor": true,
        "pointer": true,
        "touch": true,
        "voice": true
    },
    "interactive-service": "off",
    "interactivity": "off",
    "irBlaster": "off",
    "ismMethod": "normal",
    "japanCitySelection": "Tokyo",
    "liveMenuLaunched": false,
    "livePlus": "off",
    "localeCountryGroup": "UNDEFINED",
    "logoLight": "low",
    "magicNum1": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum2": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum3": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum4": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum5": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum6": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum7": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum8": {
        "id": "",
        "override": false,
        "params": {}
    },
    "magicNum9": {
        "id": "com.webos.app.self-diagnosis",
        "override": true,
        "params": {
            "from": "magicNum"
        }
    },
    "magicNumHelpShow": true,
    "menuLanguage": "eng",
    "menuTransparency": "on",
    "mhegGuide": "off",
    "miracastOverlayAdRecovery": "off",
    "miracastOverlayStatus": "off",
    "modeSelectFlag": "off",
    "motionRecognition": "off",
    "multiChannelAudio": "on",
    "multiViewStatus": "off",
    "ohtv": "on",
    "orbit": "off",
    "password_ipcontrol": "828",
    "phlCitySelection": "0",
    "pointerAlignment": "off",
    "pointerShape": "auto",
    "pointerSize": "medium",
    "pointerSpeed": "normal",
    "powerOnLight": "off",
    "promotionOriginEnd": "undefined",
    "promotionOriginStart": "undefined",
    "promotionPeriodEnd": "0",
    "promotionPeriodStart": "0",
    "promotionStreamer": "off",
    "pstreamerUser": "off",
    "quickStartMode": "off",
    "screenRotation": "off",
    "searchAppTTS": "off",
    "setId": 1,
    "smartServiceCountryCode2": "other",
    "smartServiceCountryCode3": "other",
    "smartSoundDemo": "on",
    "speakToTv": "off",
    "standByLight": "on",
    "storeHDR": "on",
    "storeLogo": "0",
    "storeMode": "home",
    "storeMode2": "on",
    "storeModeVideo": "off",
    "subdivisionCodeOfServiceCountry": "",
    "subtitleLanguageFirst": "eng",
    "subtitleLanguageSecond": "eng",
    "supplementaryAudio": "off",
    "syncMode": "off",
    "syncModeTvCondition": "none",
    "teletextLanguageFirst": "eng",
    "teletextLanguageSecond": "eng",
    "turnOnByVoice": "off",
    "usbBuiltInVideo": "on",
    "virtualKeyboardLanguage": [
        "en-US"
    ],
    "virtualSetTop": "off",
    "voiceRecognitionLanguage": "eng",
    "vsn": "N/A",
    "wakeUpword": "LGTV",
    "watchedListCollection": "on",
    "webOSPromotionVideo": "on",
    "zipcode": "not_defined"
```

#### `other` category - default settings (used by `set_other_settings` method)
```json
    "amazonHotkeyIsActive": true,
    "appReturn": "",
    "care365": {
        "accountName": "",
        "accountNumber": "",
        "userAgreementLocation": "",
        "userAgreementVersion": "",
        "value": "off"
    },
    "colorimetryHDMI1": "auto",
    "colorimetryHDMI2": "auto",
    "colorimetryHDMI3": "auto",
    "colorimetryHDMI4": "auto",
    "cursorAutoRemover": "on",
    "dolbyVSVDBVerHDMI1": "v1",
    "dolbyVSVDBVerHDMI2": "v1",
    "dolbyVSVDBVerHDMI3": "v1",
    "dolbyVSVDBVerHDMI4": "v1",
    "eotfHDMI1": "auto",
    "eotfHDMI2": "auto",
    "eotfHDMI3": "auto",
    "eotfHDMI4": "auto",
    "epgRowCount": "1",
    "flickerPatternCtrl": false,
    "freesyncLCDHDMI1": "off",
    "freesyncLCDHDMI2": "off",
    "freesyncLCDHDMI3": "off",
    "freesyncLCDHDMI4": "off",
    "freesyncOLEDHDMI1": "off",
    "freesyncOLEDHDMI2": "off",
    "freesyncOLEDHDMI3": "off",
    "freesyncOLEDHDMI4": "off",
    "freesyncSupport": "off",
    "freeviewTnCPopup": "off",
    "gameOptimizationHDMI1": "on",
    "gameOptimizationHDMI2": "on",
    "gameOptimizationHDMI3": "on",
    "gameOptimizationHDMI4": "on",
    "hdmiPcMode": {
        "hdmi1": false,
        "hdmi2": false,
        "hdmi3": false,
        "hdmi4": false
    },
    "homeEffectVersion": [
        {
            "id": "Christmas",
            "version": 1.0
        },
        {
            "id": "Halloween",
            "version": 1.0
        }
    ],
    "isFirstCapture": "true",
    "isfUpdated": "false",
    "lowLevelAdjustment": 0,
    "masterLuminanceLevel": "540nit",
    "masteringColorHDMI1": "auto",
    "masteringColorHDMI2": "auto",
    "masteringColorHDMI3": "auto",
    "masteringColorHDMI4": "auto",
    "masteringPeakHDMI1": "auto",
    "masteringPeakHDMI2": "auto",
    "masteringPeakHDMI3": "auto",
    "masteringPeakHDMI4": "auto",
    "maxCLLHDMI1": "auto",
    "maxCLLHDMI2": "auto",
    "maxCLLHDMI3": "auto",
    "maxCLLHDMI4": "auto",
    "maxFALLHDMI1": "auto",
    "maxFALLHDMI2": "auto",
    "maxFALLHDMI3": "auto",
    "maxFALLHDMI4": "auto",
    "netflixHotkeyIsActive": true,
    "quickSettingsMenuList": [
        "QuickSettings_picture_button",
        "QuickSettings_soundMode_button",
        "QuickSettings_soundOut_button",
        "QuickSettings_timer_button",
        "QuickSettings_network_button",
        "QuickSettings_menu_button"
    ],
    "screenRemoteAutoShow": "true",
    "screenRemoteExpanded": "false",
    "screenRemotePosition": "right",
    "simplinkAutoPowerOn": "on",
    "simplinkEnable": "off",
    "supportAirplay": false,
    "supportBnoModel": false,
    "ueiEnable": "off",
    "uhdDeepColor8kHDMI1": "off",
    "uhdDeepColor8kHDMI2": "off",
    "uhdDeepColor8kHDMI3": "off",
    "uhdDeepColor8kHDMI4": "off",
    "uhdDeepColorAutoStatusHDMI1": "none",
    "uhdDeepColorAutoStatusHDMI2": "none",
    "uhdDeepColorAutoStatusHDMI3": "none",
    "uhdDeepColorAutoStatusHDMI4": "none",
    "uhdDeepColorHDMI1": "off",
    "uhdDeepColorHDMI2": "off",
    "uhdDeepColorHDMI3": "off",
    "uhdDeepColorHDMI4": "off"
```

#### `system` categories and keys (used by `get_system_settings` method)
```json
    "twinTv": [
            "status",
            "role",
            "systemMode"
    ],
    "network": [
            "deviceName",
            "wolwowlOnOff",
            "bleAdvertisingOnOff"
    ],
    "option": [
            "audioGuidance",
            "country",
            "zipcode",
            "livePlus",
            "addressInfo",
            "phlCitySelection",
            "smartServiceCountryCode3",
            "syncMode",
            "storeMode"
    ],
    "time": [
            "onTimerVolume"
    ],
    "picture": [
            "brightness",
            "backlight",
            "contrast",
            "color"
    ],
    "" : [
            "eulaStatus",
            "eulaInfoNetwork",
            "mobileSetupStatus",
            "localeInfo"
    ],
    "other": [
            "simplinkEnable"
    ],
    "sound": [
            "avSync",
            "avSyncSpdif",
            "avSyncBypassInput",
            "eArcSupport",
            "soundOutput",
            "soundOutputDigital"
    ]
```

#### `config` keys (used by `get_configs` and `set_configs` methods)
```
audio.*
com.palm.app.settings.*
com.palm.app.store-demo.*
com.webos.app.home.*
com.webos.app.igallery.*
com.webos.app.inputcommon.*
com.webos.app.quickinputpicker.*
com.webos.app.quicksettings.*
com.webos.app.systemmusic.*
com.webos.app.tips.*
com.webos.authenticationMethods.*
com.webos.keyaction.*
com.webos.service.arccontroller.*
com.webos.service.config.*
com.webos.service.fepg.*
com.webos.service.ime.*
com.webos.service.irdbmanager.*
com.webos.service.nop.*
com.webos.service.scd.*
com.webos.service.voiceinput.*
com.webos.surfacemanager.*
inputMap.hdcp22forHDMI.*
system.*
tv.config.*
tv.conti.*
tv.hw.*
tv.model.*
tv.nyx.*
tv.rmm.*
```

