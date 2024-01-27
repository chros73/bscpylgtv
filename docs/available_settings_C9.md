### OLED C9 (2019) firmware v5.30.40, webOS v4.9.7
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
sdr, hdr, technicolorHdr, dolbyHdr,
sdrALLM, hdrALLM, technicolorHdrALLM, dolbyHdrALLM
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
    "aiPicture": "off",
    "aiPictureReset": "off",
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
    "enableToastPopup": "on",
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
        "id": "com.webos.app.self-diagnosis",
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
    "multiViewStatus": "off",
    "ohtv": "on",
    "orbit": "off",
    "password_ipcontrol": "828",
    "phlCitySelection": "0",
    "play8kVideoOnApps": "off",
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
    "appReturn": "",
    "care365": {
        "accountName": "",
        "accountNumber": "",
        "userAgreementLocation": "",
        "userAgreementVersion": "",
        "value": "off"
    },
    "cursorAutoRemover": "on",
    "epgRowCount": "1",
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
    "mapping_info": [
        {
            "movies": {
                "app_id": null,
                "isActive": false,
                "launch_param": null
            }
        },
        {
            "netflix": {
                "app_id": "netflix",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "amazon": {
                "app_id": "amazon",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "ivi": {
                "app_id": "ivi",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "disneyplus": {
                "app_id": "com.disney.disneyplus-prod",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "lgchannels": {
                "app_id": "com.webos.app.livetv",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "rakutentv": {
                "app_id": "ui30",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "globoplay": {
                "app_id": "globoplaywebos",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "okko": {
                "app_id": "yota.play",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "kinopoisk": {
                "app_id": "com.685631.3411",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "watchaplay": {
                "app_id": "com.frograms.watchaplay.webos",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "unext": {
                "app_id": "u.next",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "hotstar": {
                "app_id": "hotstar",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "new": {
                "app_id": null,
                "isActive": false,
                "launch_param": null
            }
        }
    ],
    "masterLuminanceLevel": "540nit",
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
commercial.applist.*
commercial.com.lge.settingsservice.*
commercial.com.palm.app.firstuse.*
commercial.com.palm.app.settings.*
commercial.com.webos.app.inputcommon.*
commercial.com.webos.applicationManager.*
commercial.com.webos.service.attachedstoragemanager.*
commercial.com.webos.surfacemanager.*
commercial.enterprisecode.*
commercial.hdmicec.*
commercial.hw.i2c.*
commercial.hw.*
commercial.hw.sensor.*
commercial.*
commercial.network.*
commercial.overlayapp.*
commercial.path.*
commercial.sdx.*
commercial.sensor.*
commercial.ssw.*
commercial.supersign.cms.*
commercial.video.*
com.palm.app.firstuse.*
com.palm.app.settings.*
com.palm.app.store-demo.*
com.webos.app.connectionwizard.*
com.webos.app.controlmanager.*
com.webos.app.factorywin.*
com.webos.app.favshows.*
com.webos.app.home.*
com.webos.app.igallery.*
com.webos.app.inputcommon.*
com.webos.app.installation.*
com.webos.app.pcbr.*
com.webos.app.photovideo.*
com.webos.app.quicksettings.*
com.webos.app.systemmusic.*
com.webos.app.tips.*
com.webos.app.tvhotkey.*
com.webos.applicationManager.*
com.webos.authenticationMethods.*
com.webos.bootManager.*
com.webos.keyaction.*
com.webos.keyaction.lockmode.*
com.webos.memorymanager.*
com.webos.service.airplay.*
com.webos.service.attachedstoragemanager.*
com.webos.service.cbox.*
com.webos.service.commercialinputdevice.*
com.webos.service.commercial.*
com.webos.service.commerciallogger.*
com.webos.service.commercial.remotediagnosticservice.*
com.webos.service.commercial.remotemanagerservice.*
com.webos.service.commercial.webgateway.*
com.webos.service.config.*
com.webos.service.eim.*
com.webos.service.favoriteservice.*
com.webos.service.fepg.*
com.webos.service.hcapmw.*
com.webos.service.iepg.*
com.webos.service.ime.*
com.webos.service.irdbmanager.*
com.webos.service.livepick.*
com.webos.service.nlpmanager.*
com.webos.service.nop.*
com.webos.service.nudge.*
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
webos.keyaction.*
```

#### part of default DoVi config of C9 (DMSwVersion = 4.0) (can be used for USB upload)
```ini
[Global]
# Panel Specific
Tmax = 600
Tmin = 0.001
# From panel specification
TPrimaries = 0.6766 0.3231 0.2526 0.6822 0.1413 0.0483 0.3127 0.3290

# VSVDB Related Information
vsvdb_Tmax = 700
vsvdb_Tmin = 0.0001
vsvdb_TPrimaries = 0.7080 0.2920 0.1700 0.7970 0.1310 0.0460 0.3127 0.3290

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
# Panel Specific
Tmax = 200
# Ambient Light Compensation
Ambient = 1
# Preference Picture
DBacklight = 1
DContrast = 0
DBrightness = 0
DSaturation = 0
DColorShift = 0

[PictureMode = 1]
PictureModeName = CinemaHome
# Panel Specific
Tmax = 300
# Ambient Light Compensation
Ambient = 1
# Preference Picture
DBacklight = 1
DContrast = 0
DBrightness = 0
DSaturation = 0
DColorShift = 0

[PictureMode = 2]
PictureModeName = Cinema
SupportsDM3 = 1 
BrightnessPreservation = 0
# Ambient Light Compensation
Ambient = 0
# Preference Picture
DBacklight = 1
DContrast = 0
DBrightness = 0
DSaturation = 0
DColorShift = 0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
Tmax = 300
# Ambient Light Compensation
Ambient = 1
# Preference Picture
DBacklight = 1
DContrast = 0
DBrightness = 0
DSaturation = 0
DColorShift = 0

[PictureMode = 4]
PictureModeName = Game
# Panel Specific
Tmax = 300
# Ambient Light Compensation
Ambient = 1
# Preference Picture
DBacklight = 1
DContrast = 0
DBrightness = 0
DSaturation = 0
DColorShift = 0
```

##### differences in B9 config
```ini
# From panel specification
TPrimaries = 0.6789 0.3211 0.2520 0.6847 0.1433 0.0477 0.3127 0.3290

# VSVDB Related Information
vsvdb_Tmax = 600
vsvdb_Tmin = 0.001
vsvdb_TPrimaries = 0.7222 0.2978 0.2142 0.7655 0.1310 0.0396 0.3127 0.3290 
```
