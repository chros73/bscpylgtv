### OLED C1 (2021) firmware v3.36.50, webOS v6.1.0
Available settings per category that can be used with various methods.

#### Inputs
```
atv, av1, av2, camera, comp1, comp2, comp3, default, dtv, gallery,
hdmi1, hdmi2, hdmi3, hdmi4, hdmi1_pc, hdmi2_pc, hdmi3_pc, hdmi4_pc,
ip, movie, photo, pictest, rgb, scart, smhl
```

#### Picture modes (presets)
```
cinema, eco, expert1, expert2, filmMaker, game, normal, photo, sports, vivid,
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
    "colorTemperature": "-50",
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
    "dbgLogUpload": false,
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
    "faultLogUpload": false,
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
    "screenOff": "off",
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
    "storeUsbAlarm": "off",
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
    "cursorAutoRemover": "on",
    "dolbyVSVDBVer": "v2",
    "dolbyVSVDBVerHDMI1": "v2",
    "dolbyVSVDBVerHDMI2": "v2",
    "dolbyVSVDBVerHDMI3": "v2",
    "dolbyVSVDBVerHDMI4": "v2",
    "enableQuickGame": "on",
    "eotf": "auto",
    "eotfHDMI1": "auto",
    "eotfHDMI2": "auto",
    "eotfHDMI3": "auto",
    "eotfHDMI4": "auto",
    "epgRowCount": "1",
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
    "gameGenre": "Standard",
    "gameMode": {
        "hdmi1": "off",
        "hdmi2": "off",
        "hdmi3": "off",
        "hdmi4": "off"
    },
    "gameOptimization": "on",
    "gameOptimizationHDMI1": "on",
    "gameOptimizationHDMI2": "on",
    "gameOptimizationHDMI3": "on",
    "gameOptimizationHDMI4": "on",
    "gameUIColor": "violet",
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
    "illuminanceThreshold": 0,
    "inputOptimization": "auto",
    "isFirstCapture": "true",
    "isfUpdated": "false",
    "lgLogoDisplay": "on",
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
                "app_id": "com.webos.app.lgchannels",
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
    "masteringColor": "auto",
    "masteringColorHDMI1": "auto",
    "masteringColorHDMI2": "auto",
    "masteringColorHDMI3": "auto",
    "masteringColorHDMI4": "auto",
    "masteringPeak": "auto",
    "masteringPeakHDMI1": "auto",
    "masteringPeakHDMI2": "auto",
    "masteringPeakHDMI3": "auto",
    "masteringPeakHDMI4": "auto",
    "maxCLL": "auto",
    "maxCLLHDMI1": "auto",
    "maxCLLHDMI2": "auto",
    "maxCLLHDMI3": "auto",
    "maxCLLHDMI4": "auto",
    "maxFALL": "auto",
    "maxFALLHDMI1": "auto",
    "maxFALLHDMI2": "auto",
    "maxFALLHDMI3": "auto",
    "maxFALLHDMI4": "auto",
    "netflixHotkeyIsActive": true,
    "newKey": "on",
    "quickSettingsMenuList": [
        "QuickSettings_picture_button",
        "QuickSettings_soundMode_button",
        "QuickSettings_soundOut_button",
        "QuickSettings_game_button",
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
    "weatherAllowed": false,
    "whiteStabilizer": 13
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
            "firstTvSignalStatus",
            "addressInfo",
            "phlCitySelection",
            "smartServiceCountryCode3",
            "syncMode",
            "storeMode",
            "localeCountryGroup",
            "japanCitySelection",
            "countryBroadcastSystem"
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
            "energySaving"
    ],
    "" : [
            "eulaStatus",
            "eulaInfoNetwork",
            "mobileSetupStatus",
            "localeInfo"
    ],
    "other": [
            "simplinkEnable",
            "ueiEnable"
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
    "lock": [
            "parentalGuidance",
            "ziggoRaiting"
    ],
    "general": [
            "alwaysOn",
            "tvOnScreen",
            "tvInstallMethod",
            "powerOffBySCA3SystemChanged",
            "SCA3SystemCountry"
    ]
```

#### `config` keys (used by `get_configs` and `set_configs` methods)
```
airplay.*
audio.*
broadcast.*
com.palm.app.firstuse.*
com.palm.app.settings.*
com.palm.app.store-demo.*
com.webos.app.connectionwizard.*
com.webos.app.factorywin.*
com.webos.app.favshows.*
com.webos.app.home.*
com.webos.app.igallery.*
com.webos.app.inputcommon.*
com.webos.app.mediadiscovery.*
com.webos.app.photovideo.*
com.webos.app.quickinputpicker.*
com.webos.app.quicksettings.*
com.webos.app.systemmusic.*
com.webos.app.tips.*
com.webos.applicationManager.*
com.webos.authenticationMethods.*
com.webos.keyaction.*
com.webos.memorymanager.*
com.webos.service.airplay.*
com.webos.service.arccontroller.*
com.webos.service.attachedstoragemanager.*
com.webos.service.cbox.*
com.webos.service.datamigrator.*
com.webos.service.config.*
com.webos.service.eim.*
com.webos.service.favoriteservice.*
com.webos.service.fepg.*
com.webos.service.hybridtv.*
com.webos.service.iepg.*
com.webos.service.ime.*
com.webos.service.irdbmanager.*
com.webos.service.livepick.*
com.webos.service.miracast.*
com.webos.service.miracasttx.*
com.webos.service.msc.*
com.webos.service.nlpmanager.*
com.webos.service.nop.*
com.webos.service.nudge.*
com.webos.service.pdm.*
com.webos.service.photorenderer.*
com.webos.service.preloadmanager.*
com.webos.service.rollingscreen.*
com.webos.service.scd.*
com.webos.service.time.*
com.webos.service.tnm.*
com.webos.service.tvpower.*
com.webos.service.utp.*
com.webos.service.voiceinput.*
com.webos.service.wampluggable.hbbtv.*
com.webos.surfacemanager.*
dvr.*
extinput-service.*
inputMap.*
mediaCapability.*
miracast.*
system.*
tv.config.*
tv.conti.*
tv.hw.*
tv.model.*
tv.nyx.*
tv.rmm.*
```

#### part of default DoVi config of C1 (DMSwVersion = 4.0) (can be used for USB upload)
```ini
[Global]
# Panel Specific
Tmax = 680
Tmin = 0.001
# From panel specification
TPrimaries = 0.6771 0.3213 0.252 0.6829 0.1434 0.0496 0.3127 0.329

# VSVDB Related Information
vsvdb_Tmax = 680
vsvdb_Tmin = 0.0001
vsvdb_TPrimaries = 0.6771 0.3213 0.252 0.6829 0.1434 0.0496 0.3127 0.329

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
# Panel Specific
Tmax = 300
# Light Sense
Ambient = 1

[PictureMode = 1]
PictureModeName = CinemaHome
# Panel Specific
Tmax = 340
# Light Sense
Ambient = 1

[PictureMode = 2]
PictureModeName = Cinema
SupportsDM3 = 1
BrightnessPreservation = 0
# Panel Specific
# Light Sense
Ambient = 0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
Tmax = 340
# Light Sense
Ambient = 1

[PictureMode = 4]
PictureModeName = Game
# Panel Specific
Tmax = 340
# Light Sense
Ambient = 1
```

##### differences in B1 config
```ini
[Global]
# Panel Specific
Tmax = 610
# From panel specification
TPrimaries = 0.6767 0.3225 0.2535 0.6804 0.1443 0.0484 0.3127 0.3290

# VSVDB Related Information
vsvdb_Tmax = 610
vsvdb_Tmin = 0.001
vsvdb_TPrimaries = 0.6767 0.3225 0.2535 0.6804 0.1443 0.0484 0.3127 0.3290

[PictureMode = 0]
Tmax = 260

[PictureMode = 1]
Tmax = 305

[PictureMode = 3]
Tmax = 305

[PictureMode = 4]
Tmax = 305
```

##### differences in A1 config
```ini
[Global]
# Panel Specific
Tmax = 610
# From panel specification
TPrimaries = 0.6791 0.3206 0.2522 0.6837 0.1434 0.0485 0.3127 0.3290 

# VSVDB Related Information
vsvdb_Tmax = 610
vsvdb_Tmin = 0.001
vsvdb_TPrimaries = 0.6791 0.3206 0.2522 0.6837 0.1434 0.0485 0.3127 0.3290

[PictureMode = 0]
Tmax = 260

[PictureMode = 1]
Tmax = 305

[PictureMode = 3]
Tmax = 305

[PictureMode = 4]
Tmax = 305
```
