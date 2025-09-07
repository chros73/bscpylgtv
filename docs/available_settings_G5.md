### OLED G5 (2025) firmware v33.21.81.01, webOS v10.2.0
Available settings per category that can be used with various methods.

#### Inputs
```
atv, av1, av2, browser, camera, comp1, comp2, comp3, default, dp1, dp2, dtv, gallery,
hdmi1, hdmi1_pc, hdmi2, hdmi2_pc, hdmi3, hdmi3_pc, hdmi4, hdmi4_pc,
ip, movie, photo, pictest, rgb, scart, smhl, usbc1, usbc2, x
```

#### Picture modes (presets)
```
cinema, eco, expert1, expert2, filmMaker, game, normal, personalized, photo, sports, vivid, x,
hdrCinema, hdrCinemaBright, hdrEco, hdrExternal, hdrFilmMaker, hdrGame, hdrPersonalized, hdrStandard, hdrVivid,
dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon, dolbyHdrGame, dolbyHdrPersonalized, dolbyHdrStandard, dolbyHdrVivid
```

#### Dynamic range modes
```
sdr, hdr, technicolorHdr, dolbyHdr, x,
sdrALLM, hdrALLM, technicolorHdrALLM, dolbyHdrALLM
```

#### `aiPicture` category - default settings: `hdmi1` input - `expert2` preset (used by `set_current_picture_settings` method)
```json
    "ai_Brightness": "off",
    "ai_Genre": "off",
    "ai_Picture": "off"
```

#### `picture` category - default settings: `hdmi1` input - `expert2` preset (used by `set_current_picture_settings` method)
```json
    "DtmMastering10k": 40,
    "DtmMastering1k": 80,
    "DtmMastering4k": 60,
    "DtmProfessional": false,
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
    "applyToAllInput": "done",
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
    "colorTemperature": "-40",
    "contrast": "80",
    "dolbyPrecisionDetail": "off",
    "dynamicColor": "off",
    "dynamicContrast": "off",
    "edgeEnhancer": "on",
    "expertPattern": "off",
    "expressionEnhancer": "off",
    "externalPqlDbType": "none",
    "filmmakerAmbientLight": "off",
    "gamma": "high2",
    "gammaLevel": "0",
    "grassColor": "0",
    "hPosition": "0",
    "hSharpness": "10",
    "hSize": "0",
    "hdrDynamicToneMapping": "on",
    "localDimming": "low",
    "motionEyeCare": "off",
    "motionPro": "off",
    "motionProOLED": "off",
    "mpegNoiseReduction": "off",
    "nearBlackDetail": "0",
    "noiseReduction": "off",
    "peakBrightness": "off",
    "pictureTempKey": "off",
    "precisionHdrMasterPro": "off",
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
    "a11yQuickList": [
        "AudioGuidance",
        "TvPowerSound",
        "HighContrast",
        "FocusEmphasis",
        "Magnification",
        "VideoDescription",
        "AudioDescription",
        "ReadingMagnification",
        "RemoteAssistance",
        "CaptionSign"
    ],
    "activeStandby": "off",
    "additionalAudioSelection": "none",
    "addressInfo": [
        "not_defined",
        "not_defined"
    ],
    "adjustServiceRemoteControlMode": true,
    "animationGuide": "on",
    "appInstallDevice": "internal",
    "appReturn": "off",
    "audioDescription": "off",
    "audioDescriptionSpeed": "0",
    "audioDescriptionVolume": "10",
    "audioGuidance": "off",
    "audioGuidancePitch": "medium",
    "audioGuidanceSpeed": "medium",
    "audioGuidanceVolume": "medium",
    "authKeyServer": "off",
    "autoComplete": false,
    "autoConfigurationPhase": "done",
    "autoOff15Min": "off",
    "autoPowerOn": "off",
    "baloonHelp": "on",
    "broadcastingSystemPref": {
        "analog": "pal",
        "analogCable": "pal",
        "dab": "0",
        "digital": "dvb",
        "digitalCable": "dvb",
        "digitalSatellite": "dvb",
        "ip": "0"
    },
    "captionColor": "white",
    "captionDisplay": "off",
    "captionEdgeColor": "black",
    "captionEdgeType": "normal",
    "captionFontSize": "normal",
    "captionFontStyle": "normal",
    "captionMargin": "0",
    "captionMenuLanguageMode": "off",
    "captionMode": "custom",
    "captionOpacity": "100",
    "captionWindowColor": "black",
    "captionWindowOpacity": "0",
    "channelAutoRun": "off",
    "channelBanner": "on",
    "channelplus": "off",
    "channelPlusApplyPrimaryCh": "off",
    "citySelection": "other",
    "colorDepth": "auto",
    "contentStore": "off",
    "countryGroup": "UNDEFINED",
    "countryRegion": "other",
    "dataService": "mheg",
    "demoMode": "off",
    "demoModeOnOff": "off",
    "demoUsageMode": "home",
    "deviceName": "LG TV",
    "deviceNameEdit": "off",
    "displayMusicWidget": true,
    "emergencyAlert": "on",
    "enableMediaPlayer": "on",
    "enableWOL": "off",
    "energySaving": "auto",
    "epgRowCount": "1",
    "faultRecording": "off",
    "favoriteGroup": "A",
    "firstTvSignalStatus": "undefined",
    "focusEmphasis": "off",
    "freesyncOLEDMotionPro": "off",
    "freesyncPremium": "off",
    "freesyncSupport": "off",
    "gameGenre": "Standard",
    "gameMode": "off",
    "gameOptimization": "on",
    "gameScreenPosition": "off",
    "graphicSharpnessLevel": 0,
    "gsync": "off",
    "hapticFeedback": "off",
    "hbbTV": "off",
    "hddEcoMode": "on",
    "helpOnSettings": "on",
    "highContrast": "off",
    "hotelModeActive": "off",
    "hotkey": [
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
    "inputControl": "off",
    "inputControlTV": "on",
    "inputDevicesSupportStatus": {
        "keyboard": true,
        "motionRemoteControl": true,
        "pointer": true,
        "touch": true,
        "voice": true
    },
    "inputOptimization": "auto",
    "instantGameResponse": "off",
    "interactive-service": "off",
    "irdBlaster": "off",
    "ismMethod": "normal",
    "japanCitySelection": "0",
    "largeOsdEnable": false,
    "liveMenuLaunched": false,
    "livePlus": "off",
    "localeCountryGroup": "UNDEFINED",
    "logoLight": "low",
    "magnification": "off",
    "masterkey": "00000000",
    "masterPasswordEnable": "off",
    "masterPincode": "0000",
    "menuPosition": "bottom",
    "menuTransparency": "on",
    "mhegGuide": "off",
    "miracast": "off",
    "modeSelectFlag": "off",
    "multiChannelAudio": "on",
    "multiRCCode": "1",
    "multiViewStatus": "off",
    "neverShowQuickTips": false,
    "ohtv": "on",
    "onTimerVolume": "0",
    "password": "0000",
    "passwordEnable": "off",
    "phlCitySelection": "0",
    "pictureTestMode": "off",
    "pincode": "0000",
    "playControlMode": "on",
    "pointerAlignment": "off",
    "pointerShape": "auto",
    "pointerSize": "small",
    "pointerSpeed": "normal",
    "powerOffByAbsence": "off",
    "powerOffByNoSignal": "on",
    "powerOnLight": "off",
    "pqFaultRecording": "off",
    "promotionChannel": "off",
    "promotionOriginType": "undefined",
    "promotionPeriod": "0",
    "promotionStreamer": "off",
    "publicDisplay": "off",
    "quickBootWarningPopup": "unchecked",
    "quickStartMode": "off",
    "quickStartPlusPopup": "unchecked",
    "readingMagnification": "off",
    "readingMagnificationLevel": "small",
    "screenOff": "off",
    "screenRotation": "off",
    "screenSaver": "on",
    "searchAppTTS": "off",
    "setId": 1,
    "shopDemo": "off",
    "signageMode": "off",
    "simplinkAutoPowerOn": "on",
    "simplinkEnable": "off",
    "simplinkRemoteAlarmDevice": false,
    "simplinkRemoteDevice": false,
    "singleRemoteDevice": false,
    "smartServiceCountryCode3": "0",
    "soundTestMode": "off",
    "speakToTv": "off",
    "standByLight": "on",
    "storeHDR": "on",
    "storeLogo": "0",
    "storeMode": "home",
    "storeMode2": "on",
    "storeModeVideo": "off",
    "subdivision": "others",
    "supplementaryAudio": "off",
    "supportAudioSupport": "on",
    "supportBandwidth": "highest",
    "supportUHD": "on",
    "syncMode": "off",
    "syncModeTvCondition": "none",
    "tailDirection": "right",
    "teletextLanguage": "eng",
    "turnOnByVoice": "off",
    "tvFeedbackRecord": "on",
    "tvInstallationType": "normal",
    "tvOrientation": "down",
    "tvPowerSound": "on",
    "usbApps": "on",
    "usedMemoryInKB": 0,
    "usedMemoryInPercentage": 0,
    "videoDescription": "off",
    "viewerDiagAgreement": "off",
    "voiceRecognitionLanguage": "eng",
    "wakeUpword": "LGTV",
    "weatherAllowed": false,
    "webOSPromotionVideo": "on",
    "wifiConnectionOnOff": "off",
    "wifiCountryCodeManualValue": "",
    "wifiCountrySetting": "auto",
    "wifiDriverPowerSave": "off",
    "wifiPassiveScan": "off",
    "wifiPowerSave": "off",
    "wifiStrengthChecking": "on",
    "wifiTV": "off",
    "wowlEnable": "off",
    "zipcode": "not_defined"
```

#### `other` category - default settings (used by `set_other_settings` method)
```json
    "444BypassHDMI1": "off",
    "444BypassHDMI2": "off",
    "444BypassHDMI3": "off",
    "444BypassHDMI4": "off",
    "444BypassHDMINone": "off",
    "activeArtisticDisplayScreenSaver": false,
    "amazonHotkeyIsActive": true,
    "aodPictureSyncMode": "on",
    "appReturn": "",
    "autoSLZoomWithObjectDetection": "off",
    "battery25PercentMode": "off",
    "batteryInstopProtect": "on",
    "blackStabilizer": 13,
    "blueLight": "off",
    "care365": {
        "accountName": "",
        "accountNumber": "",
        "userAgreementLocation": "",
        "userAgreementVersion": "",
        "value": "off"
    },
    "colorimetry": "auto",
    "colorimetryHDMI1": "auto",
    "colorimetryHDMI2": "auto",
    "colorimetryHDMI3": "auto",
    "colorimetryHDMI4": "auto",
    "contentRecommendation": "on",
    "cursorAutoRemover": "on",
    "darkMode": "off",
    "dolbyVSVDBVer": "v2",
    "dolbyVSVDBVerHDMI1": "v2",
    "dolbyVSVDBVerHDMI2": "v2",
    "dolbyVSVDBVerHDMI3": "v2",
    "dolbyVSVDBVerHDMI4": "v2",
    "dpPcMode": {
        "dp1": false,
        "dp2": false
    },
    "enable144HzBooster": "off",
    "enableALLM": "on",
    "enableDolbyVisionPC": "off",
    "enableQFT": "off",
    "enableQuickGame": "on",
    "eotf": "auto",
    "eotfHDMI1": "auto",
    "eotfHDMI2": "auto",
    "eotfHDMI3": "auto",
    "eotfHDMI4": "auto",
    "epgRowCount": "1",
    "fitLogUsbDump": "off",
    "flickerPatternCtrl": false,
    "freesync": "off",
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
    "gameAdjustContrast": 100,
    "gameBlackLevel": 50,
    "gameColorDepth": 65,
    "gameDashboardStatusList": [
        "fps",
        "vrr_aiGameSound_whiteStabilizer",
        "blackStabilizer",
        "lowLatency"
    ],
    "gameGenre": "Standard",
    "gameMode": {
        "hdmi1": "off",
        "hdmi2": "off",
        "hdmi3": "off",
        "hdmi4": "off"
    },
    "gameOptimization": "on",
    "gameOptimizationDP1": "on",
    "gameOptimizationDP2": "on",
    "gameOptimizationHDMI1": "on",
    "gameOptimizationHDMI2": "on",
    "gameOptimizationHDMI3": "on",
    "gameOptimizationHDMI4": "on",
    "gameOptimizationUSBC1": "on",
    "gameOptimizationUSBC2": "on",
    "gameScreenPosition": "middle",
    "gameScreenRatio": "16:9",
    "gameScreenSize": "full",
    "gameSettingModified": {
        "FPS": false,
        "RPG": false,
        "RTS": false,
        "Sports": false,
        "Standard": false,
        "USER": false
    },
    "gameSharpness": 25,
    "gameUIColor": "violet",
    "hdmiPcMode": {
        "hdmi1": false,
        "hdmi2": false,
        "hdmi3": false,
        "hdmi4": false
    },
    "simplinkAutoPowerOn": "on",
    "simplinkEnable": "off",
    "ueiEnable": "off",
    "uhdDeepColor": "off",
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
    "uhdDeepColorHDMI4": "off",
    "usbcPcMode": {
        "usbc1": false,
        "usbc2": false
    },
    "whiteStabilizer": 13
```

#### `system` categories and keys (used by `get_system_settings` method)
```json
    "aspectRatio": [
            "arcPerApp",
            "justScan"
    ],
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
            "firstTvSignalStatus",
            "addressInfo",
            "phlCitySelection",
            "smartServiceCountryCode3",
            "syncMode",
            "storeMode",
            "localeCountryGroup",
            "japanCitySelection",
            "countryBroadcastSystem",
            "yourMomentsVersion",
            "wallPaperSettings",
            "quickStartMode"
    ],
    "time": [
            "onTimerVolume",
            "timeZone"
    ],
    "picture": [
            "brightness",
            "backlight",
            "contrast",
            "color",
            "energySaving",
            "pictureMode",
            "dynamicContrast",
            "peakBrightness",
            "gamma",
            "blackLevel",
            "motionEyeCare",
            "colorGamut",
            "hdrDynamicToneMapping",
            "realCinema",
            "truMotionMode",
            "tint",
            "adjustingLuminance",
            "colorTemperature",
            "whiteBalancePoint",
            "superResolution",
            "sharpness",
            "noiseReduction",
            "mpegNoiseReduction",
            "smoothGradation",
            "dynamicColor",
            "whiteBalanceMethod",
            "whiteBalanceIre10pt",
            "whiteBalanceIre",
            "whiteBalanceRedOffset",
            "whiteBalanceRedGain",
            "whiteBalanceRed10pt",
            "whiteBalanceRed",
            "adjustingLuminance10pt",
            "whiteBalanceGreenOffset",
            "whiteBalanceGreenGain",
            "whiteBalanceGreen10pt",
            "whiteBalanceGreen",
            "whiteBalanceBlueOffset",
            "whiteBalanceBlueGain",
            "whiteBalanceBlue10pt",
            "whiteBalanceBlue",
            "colorManagementColorSystem",
            "colorManagementSaturationRed",
            "colorManagementSaturationGreen",
            "colorManagementSaturationBlue",
            "colorManagementSaturationCyan",
            "colorManagementSaturationMagenta",
            "colorManagementSaturationYellow",
            "colorManagementHueRed",
            "colorManagementHueGreen",
            "colorManagementHueBlue",
            "colorManagementHueCyan",
            "colorManagementHueMagenta",
            "colorManagementHueYellow",
            "colorManagementLuminanceRed",
            "colorManagementLuminanceGreen",
            "colorManagementLuminanceBlue",
            "colorManagementLuminanceCyan",
            "colorManagementLuminanceMagenta",
            "colorManagementLuminanceYellow",
            "whiteBalanceLuminance",
            "eyeComfortMode"
    ],
    "" : [
            "eulaStatus",
            "eulaInfoNetwork",
            "mobileSetupStatus",
            "localeInfo"
    ],
    "other": [
            "simplinkEnable",
            "ueiEnable",
            "gameWallpaper",
            "uhdDeepColorHDMI1",
            "uhdDeepColorHDMI2",
            "uhdDeepColorHDMI3",
            "uhdDeepColorHDMI4"
    ],
    "sound": [
            "avSync",
            "avSyncSpdif",
            "avSyncBypassInput",
            "eArcSupport",
            "soundOutput",
            "soundOutputDigital",
            "soundMode",
            "tvSetupConfiguration"
    ],
    "support": [
             "automaticUpdate"
    ],
    "lock": [
            "parentalGuidance",
            "ziggoRaiting",
            "parentalControl"
    ],
    "general": [
            "alwaysOn",
            "tvOnScreen",
            "tvInstallMethod",
            "powerOffBySCA3SystemChanged",
            "SCA3SystemCountry",
            "homeAutoLaunch",
            "lifeOnScreenMode",
            "homePromotion"
    ]
```

#### `config` keys (used by `get_configs` and `set_configs` methods)
```
airplay.*
amazon.*
amazon-alexa-adapter.*
audio.*
broadcast.*
com.palm.app.firstuse.*
com.palm.app.settings.*
com.palm.app.store-demo.*
com.webos.app.camera.*
com.webos.app.connectionwizard.*
com.webos.app.factorywin.*
com.webos.app.familycare.*
com.webos.app.favshows.*
com.webos.app.home.*
com.webos.app.igallery.*
com.webos.app.inputcommon.*
com.webos.app.mediadiscovery.*
com.webos.app.quicksettings.*
com.webos.app.systemmusic.*
com.webos.app.tips.*
com.webos.applicationManager.*
com.webos.authenticationMethods.*
com.webos.keyaction.*
com.webos.memorymanager.*
com.webos.service.airplay.*
com.webos.service.alwaysready.*
com.webos.service.arccontroller.*
com.webos.service.attachedstoragemanager.*
com.webos.service.btaudiosrc.*
com.webos.service.bthidmanager.*
com.webos.service.camera.*
com.webos.service.cbox.*
com.webos.service.config.*
com.webos.service.datamigrator.*
com.webos.service.eim.*
com.webos.service.favoriteservice.*
com.webos.service.fepg.*
com.webos.service.homelaunchpoints.*
com.webos.service.hybridtv.*
com.webos.service.iepg.*
com.webos.service.ime.*
com.webos.service.irdbmanager.*
com.webos.service.jsserver.*
com.webos.service.livepick.*
com.webos.service.miracast.*
com.webos.service.miracasttx.*
com.webos.service.msc.*
com.webos.service.nlpmanager.*
com.webos.service.nop.*
com.webos.service.nudge.*
com.webos.service.pbsw.*
com.webos.service.pdm.*
com.webos.service.photorenderer.*
com.webos.service.pqcontroller.*
com.webos.service.preloadmanager.*
com.webos.service.rollingscreen.*
com.webos.service.scd.*
com.webos.service.screenmanager.*
com.webos.service.time.*
com.webos.service.tnm.*
com.webos.service.tvpower.*
com.webos.service.update.*
com.webos.service.utp.*
com.webos.service.voiceinput.*
com.webos.service.wampluggable.hbbtv.*
com.webos.service.wbs.*
com.webos.service.wowplay.*
com.webos.surfacemanager.*
con.webos.service.pbsw.*
dvr.*
dynamicStreamChange.*
extinput-service.*
gip.*
inputMap.*
lg.thinqai.adapter.*
mediaCapability.*
miracast.*
multiview.*
operatorApp.*
profile.*
system.*
test.category.*
tv.config.*
tv.conti.*
tv.hw.*
tv.model.*
tv.nyx.*
tv.rmm.*
wee.*
```

###25Y\_C1A\_XXG5 (55', 65', 77', 83' G5) DV config file

```ini
#-----------------------------------------------------------------------------------------------
# Dolby Vision Configuration File Specification : v5.0.1
# Feature(System) : Best PQ, Source-led
# One picture mode supports all input type : OTT, USB, HDMI(Sink-led, Source-led).
# Created on: 2024-05-13
# Modified on: 2024-09-12
# File : Sample_TV_IDK_5.0_int3.cfg
#-----------------------------------------------------------------------------------------------

[Global]
# Panel Specific
Tmax = 2400
Tmin = 0.0001
# From panel specification
TPrimaries = 0.6872 0.3109 0.2474 0.7044 0.1492 0.0512 0.3127 0.329
TEOTF = POWER
Tgamma = 2.2
#TContrast = 1600000  # not for IDK5.X

# System-specific
RGB2YCCmat = 0.18191707 0.61198066 0.06177993 -0.10029949 -0.33730735 0.43760684 0.43760684 -0.39752205 -0.04008479
RGB2YCCOffsetNorm = 0.0625 0.5 0.5
DMSwVersion = 4.0
IDK_Version = SOC_5.0

# Picture mode index parameters
ReferenceDarkPicModeIndex = 2
DoViBrightPicModeIndex = 1

# Global Dimming
GlobalDimming = 0

# Light Sense
Ambient = 0

# Dark Detail
DarkDetail = 0

# Precision Detail
SupportsPrecisionRendering = 0

# Picture Mode: the current values must be appplied in [Global]
DBrightness = 0.0

# VSVDB Related Information
vsvdb_version = 2
vsvdb_dm_version = 4.0
vsvdb_Tmax = 2400
vsvdb_Tmin = 0.0001
vsvdb_TPrimaries = 0.6872 0.3109 0.2474 0.7044 0.1492 0.0512 0.3127 0.329
vsvdb_GlobalDimming = 0    # For standard Dolby Vision input
support_normal_dolbyvision = 1                    # Support tunneled picture
support_lowlatency_rgb_dolbyvision = 1
support_lowlatency_bt2020_dolbyvision = 1  # Source-Led with BT.2020
support_12b_yuv_422 = 0
support_12b_yuv_rgb_444 = 1
support_10b_yuv_rgb_444 = 0
support_dolby_vision_gaming = 0
vsvdb_parity = 1

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
DBrightness = 0.7

[PictureMode = 1]
PictureModeName = CinemaHome
DBrightness = 0.3

[PictureMode = 2]
PictureModeName = Cinema
DBrightness = 0.0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
DBrightness = 0.3

[PictureMode = 4]
PictureModeName = Game
DBrightness = 0.3
```

###25Y\_C1B\_48G5 (48' G5) DV config file
```ini
#-----------------------------------------------------------------------------------------------
# Dolby Vision Configuration File Specification : v5.0.1
# Feature(System) : Best PQ, Source-led
# One picture mode supports all input type : OTT, USB, HDMI(Sink-led, Source-led).
# Created on: 2024-08-07
# Modified on: 2024-09-25
# File : Sample_TV_IDK_5.0_int3.cfg
#-----------------------------------------------------------------------------------------------

[Global]
# Panel Specific
Tmax = 1200
Tmin = 0.0001
# From panel specification
TPrimaries = 0.6891 0.3094 0.2394 0.7090 0.1497 0.0476 0.3127 0.329
TEOTF = POWER
Tgamma = 2.2
#TContrast = 1600000  # not for IDK5.X

# System-specific
RGB2YCCmat = 0.18191707 0.61198066 0.06177993 -0.10029949 -0.33730735 0.43760684 0.43760684 -0.39752205 -0.04008479
RGB2YCCOffsetNorm = 0.0625 0.5 0.5
DMSwVersion = 4.0
IDK_Version = SOC_5.0

# Picture mode index parameters
ReferenceDarkPicModeIndex = 2
DoViBrightPicModeIndex = 1

# Global Dimming
GlobalDimming = 0

# Light Sense
Ambient = 0

# Dark Detail
DarkDetail = 0

# Precision Detail
SupportsPrecisionRendering = 0

# Picture Mode: the current values must be appplied in [Global]
DBrightness = 0.0

# VSVDB Related Information
vsvdb_version = 2
vsvdb_dm_version = 4.0
vsvdb_Tmax = 1200
vsvdb_Tmin = 0.0001
vsvdb_TPrimaries = 0.6891 0.3094 0.2394 0.7090 0.1497 0.0476 0.3127 0.329
vsvdb_GlobalDimming = 0    # For standard Dolby Vision input
support_normal_dolbyvision = 1                    # Support tunneled picture
support_lowlatency_rgb_dolbyvision = 1
support_lowlatency_bt2020_dolbyvision = 1  # Source-Led with BT.2020
support_12b_yuv_422 = 0
support_12b_yuv_rgb_444 = 1
support_10b_yuv_rgb_444 = 0
support_dolby_vision_gaming = 0
vsvdb_parity = 1

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
DBrightness = 0.7

[PictureMode = 1]
PictureModeName = CinemaHome
DBrightness = 0.3

[PictureMode = 2]
PictureModeName = Cinema
DBrightness = 0.0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
DBrightness = 0.3

[PictureMode = 4]
PictureModeName = Game
DBrightness = 0.3
```

###25Y\_C1A\_97G5 (97' G5) DV config file
```ini
#-----------------------------------------------------------------------------------------------
# Dolby Vision Configuration File Specification : v5.0.1
# Feature(System) : Best PQ, Source-led
# One picture mode supports all input type : OTT, USB, HDMI(Sink-led, Source-led).
# Created on: 2024-05-13
# Modified on: 2023-0X-XX
# File : Sample_TV_IDK_5.0_int3.cfg
#-----------------------------------------------------------------------------------------------

[Global]
# Panel Specific
Tmax = 990
Tmin = 0.0001
# From panel specification
TPrimaries = 0.6706 0.3213 0.2514 0.6837 0.1437 0.0568 0.3127 0.329
TEOTF = POWER
Tgamma = 2.2
#TContrast = 1600000  # not for IDK5.X

# System-specific
RGB2YCCmat = 0.18191707 0.61198066 0.06177993 -0.10029949 -0.33730735 0.43760684 0.43760684 -0.39752205 -0.04008479
RGB2YCCOffsetNorm = 0.0625 0.5 0.5
DMSwVersion = 4.0
IDK_Version = SOC_5.0

# Picture mode index parameters
ReferenceDarkPicModeIndex = 2
DoViBrightPicModeIndex = 1

# Global Dimming
GlobalDimming = 0

# Light Sense
Ambient = 0

# Dark Detail
DarkDetail = 0

# Precision Detail
SupportsPrecisionRendering = 0

# Picture Mode: the current values must be appplied in [Global]
DBrightness = 0.0

# VSVDB Related Information
vsvdb_version = 2
vsvdb_dm_version = 4.0
vsvdb_Tmax = 990
vsvdb_Tmin = 0.0001
vsvdb_TPrimaries = 0.6706 0.3213 0.2514 0.6837 0.1437 0.0568 0.3127 0.329
vsvdb_GlobalDimming = 0    # For standard Dolby Vision input
support_normal_dolbyvision = 1                    # Support tunneled picture
support_lowlatency_rgb_dolbyvision = 1
support_lowlatency_bt2020_dolbyvision = 1  # Source-Led with BT.2020
support_12b_yuv_422 = 0
support_12b_yuv_rgb_444 = 1
support_10b_yuv_rgb_444 = 0
support_dolby_vision_gaming = 0
vsvdb_parity = 1

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
DBrightness = 0.7

[PictureMode = 1]
PictureModeName = CinemaHome
DBrightness = 0.3

[PictureMode = 2]
PictureModeName = Cinema
DBrightness = 0.0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
DBrightness = 0.3

[PictureMode = 4]
PictureModeName = Game
DBrightness = 0.3

```