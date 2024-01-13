### OLED C8 (2018) webOS v4.4.0
Available settings per category that can be used with various methods.

#### Inputs
```
atv, av1, av2, camera, comp1, comp2, comp3, default, dtv, gallery,
hdmi1, hdmi2, hdmi3, hdmi4, hdmi1_pc, hdmi2_pc, hdmi3_pc, hdmi4_pc,
ip, movie, photo, pictest, rgb, scart, smhl
```

#### Picture modes (presets)
```
cinema, eco, expert1, expert2, game, normal, photo, sports, technicolor, vivid, hdrEffect,
hdrCinema, hdrCinemaBright, hdrExternal, hdrGame, hdrStandard, hdrTechnicolor, hdrVivid,
technicolorHdrCinema, technicolorHdrCinemaBright, technicolorHdrGame, technicolorHdrStandard, technicolorHdrTechnicolor, technicolorHdrVivid,
dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon, dolbyHdrGame, dolbyHdrStandard, dolbyHdrVivid, dolbyStandard
```

#### Dynamic range modes
```
sdr, hdr, technicolorHdr, dolbyHdr
```

#### Stereoscopic modes
```
2d, 3d
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
        0
    ],
    "backlight": "80",
    "blackLevel": {
        "ntsc": "auto",
        "ntsc443": "auto",
        "pal": "auto",
        "pal60": "auto",
        "palm": "auto",
        "paln": "auto",
        "secam": "auto",
        "unknown": "low"
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
    "hdrLevel": "medium",
    "localDimming": "medium",
    "motionEyeCare": "off",
    "motionPro": "off",
    "mpegNoiseReduction": "off",
    "noiseReduction": "off",
    "realCinema": "on",
    "sharpness": "10",
    "skinColor": "0",
    "skyColor": "0",
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
        0
    ],
    "whiteBalanceBlueGain": "0",
    "whiteBalanceBlueOffset": "0",
    "whiteBalanceCodeValue": "19",
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
        0
    ],
    "whiteBalanceGreenGain": "0",
    "whiteBalanceGreenOffset": "0",
    "whiteBalanceIre": "100",
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
    "animationGuide": "on",
    "appInstallDevice": {
        "deviceId": "",
        "driveId": ""
    },
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
    "disclosureAccepted": false,
    "disclosureAcceptedVsn": "N/A",
    "displayMusicWidget": true,
    "eStreamerPosition": "all",
    "emergencyAlert": "on",
    "enableIpControl": "off",
    "enableSDDP": "off",
    "enableToastPopup": "on",
    "enabling3dSettingsMenu": "off",
    "estreamerStatus": "off",
    "firstTvSignalStatus": "undefined",
    "focusedItemEnlarged": "off",
    "freeviewMode": "off",
    "googleAssistantTTS": "on",
    "graphicSharpnessLevel": 0,
    "hbbTV": "off",
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
        "params": {}
    },
    "magicNum2": {
        "id": "",
        "params": {}
    },
    "magicNum3": {
        "id": "",
        "params": {}
    },
    "magicNum4": {
        "id": "",
        "params": {}
    },
    "magicNum5": {
        "id": "",
        "params": {}
    },
    "magicNum6": {
        "id": "",
        "params": {}
    },
    "magicNum7": {
        "id": "",
        "params": {}
    },
    "magicNum8": {
        "id": "",
        "params": {}
    },
    "magicNum9": {
        "id": "",
        "params": {}
    },
    "magicNumHelpShow": true,
    "menuLanguage": "eng",
    "menuTransparency": "on",
    "mhegGuide": "off",
    "miracastOverlayAdRecovery": "off",
    "miracastOverlayStatus": "off",
    "modeSelectFlag": "off",
    "motionRecognition": "off",
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
    "setId": "1",
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
    "appReturn": "",
    "epgRowCount": "1",
    "freeviewTnCPopup": "off",
    "hdmiPcMode": {
        "hdmi1": false,
        "hdmi2": false,
        "hdmi3": false,
        "hdmi4": false
    },
    "isFirstCapture": "true",
    "isfUpdated": "false",
    "masterLuminanceLevel": "540nit",
    "screenRemoteAutoShow": "true",
    "screenRemoteExpanded": "false",
    "screenRemotePosition": "right",
    "simplinkAutoPowerOn": "on",
    "simplinkEnable": "off",
    "supportAirplay": false,
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
            "addressInfo",
            "phlCitySelection",
            "smartServiceCountryCode3",
            "syncMode"
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
            "eulaInfoNetwork"
    ]
```

#### `config` keys (used by `get_configs` and `set_configs` methods)
```
com.palm.app.firstuse.*
com.palm.app.settings.*
com.palm.app.store-demo.*
com.webos.app.connectionwizard.*
com.webos.app.factorywin.*
com.webos.app.favshows.*
com.webos.app.home.*
com.webos.app.igallery.*
com.webos.app.inputcommon.*
com.webos.app.photovideo.*
com.webos.app.quicksettings.*
com.webos.app.systemmusic.*
com.webos.app.tips.*
com.webos.applicationManager.*
com.webos.authenticationMethods.*
com.webos.keyaction.*
com.webos.memorymanager.*
com.webos.service.attachedstoragemanager.*
com.webos.service.cbox.*
com.webos.service.config.*
com.webos.service.eim.*
com.webos.service.favoriteservice.*
com.webos.service.fepg.*
com.webos.service.iepg.*
com.webos.service.ime.*
com.webos.service.irdbmanager.*
com.webos.service.nlpmanager.*
com.webos.service.pdm.*
com.webos.service.photorenderer.*
com.webos.service.preloadmanager.*
com.webos.service.scd.*
com.webos.service.time.*
com.webos.service.tnm.*
com.webos.service.tvpower.*
com.webos.service.wampluggable.hbbtv.*
com.webos.surfacemanager.*
system.*
tv.config.*
tv.conti.*
tv.hw.*
tv.model.*
tv.rmm.*
```

#### part of default DoVi config of C8 (can be used for USB upload)
```ini
PictureMode=0
Tmax = 280
Tmin = 0.001
ColorPrimaries = 0.6760 0.3237 0.2544 0.6776 0.1433 0.0491 0.3127 0.3290

PictureMode=1
Tmax = 280
Tmin = 0.001
ColorPrimaries = 0.6760 0.3237 0.2544 0.6776 0.1433 0.0491 0.3127 0.3290

PictureMode=2
Tmax = 560
Tmin = 0.001
ColorPrimaries = 0.6760 0.3237 0.2544 0.6776 0.1433 0.0491 0.3127 0.3290

PictureMode=3
Tmax = 280
Tmin = 0.001
ColorPrimaries = 0.6760 0.3237 0.2544 0.6776 0.1433 0.0491 0.3127 0.3290

PictureMode=4
Tmax = 280
Tmin = 0.001
ColorPrimaries = 0.6760 0.3237 0.2544 0.6776 0.1433 0.0491 0.3127 0.3290

# For VSVDB
PictureMode=19
Tmax = 700
Tmin = 0.0001
ColorPrimaries = 0.6800	0.3200 0.2500 0.7000 0.1400 0.0450 0.3127 0.3290
```
