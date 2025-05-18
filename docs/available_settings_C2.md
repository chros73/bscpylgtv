### OLED C2 (2022) firmware v23.20.72, webOS v9.2.1
Available settings per category that can be used with various methods.

#### Inputs
```
atv, av1, av2, browser, camera, comp1, comp2, comp3, default, dp1, dp2, dtv, gallery,
hdmi1, hdmi1_pc, hdmi2, hdmi2_pc, hdmi3, hdmi3_pc, hdmi4, hdmi4_pc,
ip, movie, photo, pictest, rgb, scart, smhl, usbc1, usbc2
```

#### Picture modes (presets)
```
cinema, eco, expert1, expert2, filmMaker, game, normal, personalized, photo, sports, vivid,
hdrCinema, hdrCinemaBright, hdrEco, hdrExternal, hdrFilmMaker, hdrGame, hdrPersonalized, hdrStandard, hdrVivid,
dolbyHdrCinema, dolbyHdrCinemaBright, dolbyHdrDarkAmazon, dolbyHdrGame, dolbyHdrPersonalized, dolbyHdrStandard, dolbyHdrVivid
```

#### Dynamic range modes
```
sdr, hdr, technicolorHdr, dolbyHdr,
sdrALLM, hdrALLM, technicolorHdrALLM, dolbyHdrALLM
```

#### `aiPicture` category - default settings: `hdmi1` input - `expert2` preset (used by `set_current_picture_settings` method)
```json
    "ai_Brightness": "off",
    "ai_Genre": "off",
    "ai_Picture": "off",
    "isAiPictureActing": false
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
    "colorTemperature": "-50",
    "contrast": "80",
    "dolbyPrecisionDetail": "off",
    "dynamicColor": "off",
    "dynamicContrast": "off",
    "edgeEnhancer": "on",
    "expertPattern": "off",
    "expressionEnhancer": "off",
    "externalPqlDbType": "none",
    "gamma": "high2",
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
    "a11yQuickList": [
        "AudioGuidance",
        "VideoDescription",
        "AudioDescription",
        "AudioDescriptionAtsc",
        "TvPowerSound",
        "HighContrast",
        "GreyScale",
        "InvertColors",
        "Caption",
        "Subtitles",
        "TunerlessCaption",
        "HardOfHearing",
        "DialogEnhancement"
    ],
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
    "aodThemeHistory": [
        {
            "category": "category-movements",
            "name": "Blooms",
            "subType": "igallery_littleflower",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/list/main/Little Flower.png"
        },
        {
            "category": "category-movements",
            "name": "Plants",
            "subType": "igallery_leaf",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/list/main/Leaf.png"
        },
        {
            "category": "category-movements",
            "name": "Turtle in the sea",
            "subType": "igallery_turtle",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/list/main/Turtle.png"
        },
        {
            "category": "category-movements",
            "name": "Aquarium",
            "subType": "igallery_aquarium",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/list/main/Aquarium.png"
        },
        {
            "category": "category-movements",
            "name": "Chandelier",
            "subType": "igallery_chandelier",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/list/main/Chandelier.png"
        },
        {
            "category": "category-movements",
            "name": "Reed Glass",
            "subType": "igallery_reedglass",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/list/main/Reed Glass.png"
        },
        {
            "category": "category-information",
            "name": "Live Window",
            "subType": "liveWindow",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/information/img_category_live_window.png"
        },
        {
            "category": "category-tbar",
            "name": "Space",
            "subType": "tbar_space",
            "thumbUrl": "/usr/palm/applications/com.webos.app.lifeonscreen/assets/tbar/img_tbar_space01.png"
        }
    ],
    "appInstallDevice": {
        "deviceId": "",
        "driveId": ""
    },
    "appUpdateMode": "manual",
    "artisticDisplayTimer": "off",
    "audioGuidance": "off",
    "audioGuidancePitch": "medium",
    "audioGuidanceSpeed": "fast",
    "audioGuidanceVolume": "medium",
    "autoComplete": false,
    "autoSmartServiceCountry": "on",
    "avatar": "off",
    "backupPsm": {
        "backupPsm2d": "hdrStandard"
    },
    "backupPsmDolby": {
        "backupPsm2d": "dolbyHdrDark"
    },
    "baloonHelp": "on",
    "bannerPosition": "none",
    "broadcastInfoNoti": "on",
    "cameraResourcePermission": [],
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
    "curvature": {
        "curvatureList": [
            {
                "disable": false,
                "selected": true,
                "type": "flat",
                "user": false,
                "value": "0%"
            },
            {
                "disable": false,
                "selected": false,
                "type": "curvature1",
                "user": false,
                "value": "50%"
            },
            {
                "disable": false,
                "selected": false,
                "type": "curvature2",
                "user": false,
                "value": "100%"
            },
            {
                "disable": true,
                "selected": false,
                "type": "curvature3",
                "user": false,
                "value": "100%"
            }
        ],
        "valueList": [
            "0%",
            "5%",
            "10%",
            "15%",
            "20%",
            "25%",
            "30%",
            "35%",
            "40%",
            "45%",
            "50%",
            "55%",
            "60%",
            "65%",
            "70%",
            "75%",
            "80%",
            "85%",
            "90%",
            "95%",
            "100%"
        ]
    },
    "dataService": "mheg",
    "dbgLogUpload": false,
    "demoFileList": "undefined",
    "demoMode": "on",
    "displayMusicWidget": true,
    "eStreamerPosition": "all",
    "emergencyAlert": "on",
    "emergencyInformationAtsc30": "on",
    "emergencyInformationLanguageAtsc30": "eng",
    "enableIpControl": "off",
    "enableSDDP": "off",
    "enableToastPopup": "on",
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
    "homeWallPaper": "opt1",
    "hybridCast": "off",
    "inputDevicesSupportStatus": {
        "keyboard": true,
        "motionSensor": true,
        "pointer": true,
        "touch": true,
        "voice": true
    },
    "interactive-service": "off",
    "interactive-service-hdmi": "off",
    "interactive-service-id": "",
    "interactivity": "off",
    "irBlaster": "off",
    "ismMethod": "normal",
    "japanCitySelection": "Tokyo",
    "lifeOnScreenEnergySaving": "auto",
    "lifeOnScreenNotification": true,
    "lifeOnScreenOnTimer": [],
    "lifeOnScreenUsingMotionSensor": false,
    "lineView": "on",
    "liveMenuLaunched": false,
    "livePlus": "off",
    "livePromotion": "on",
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
    "magicNumFvp": false,
    "magicNumHelpShow": true,
    "menuLanguage": "eng",
    "menuTransparency": "on",
    "mhegGuide": "off",
    "miracastOverlayAdRecovery": "off",
    "miracastOverlayStatus": "off",
    "modeSelectFlag": "off",
    "motionRecognition": "off",
    "motionSensorSensitivity": "medium",
    "motionSensorSensitivityForAOD": "medium",
    "multiChannelAudio": "on",
    "multiViewStatus": "off",
    "nearbyDevicePermission": [],
    "ohtv": "on",
    "orbit": "off",
    "password_ipcontrol": "828",
    "personalizedDemoImgList": {
        "list": [],
        "userSelected": false
    },
    "personalizedDemoString": {
        "longStrIdx": 0,
        "shortList": []
    },
    "personalizedImgList": {
        "list": [],
        "otherUserPreferences": {},
        "userSelected": false
    },
    "personalizedString": {
        "longStrIdx": 0,
        "shortList": [],
        "userNo": ""
    },
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
    "restoreCurve": "on",
    "screenOff": "off",
    "screenOffTime": "5",
    "screenRotation": "off",
    "searchAppTTS": "off",
    "serviceCountryForMagicNum": "",
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
    "wallPaperHistory": [
        {
            "color": "#D4B04F",
            "name": "Flip",
            "thumb": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_clock_calendar.png",
            "type": "clock_flip_color1"
        },
        {
            "color": "#CFC1AB",
            "name": "Typography 1",
            "thumb": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_poster_minimal_01.png",
            "type": "poster_minimal1_color1"
        },
        {
            "frame": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_frame_peaceful.png",
            "name": "Dream",
            "thumb": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_window_dream.png",
            "type": "window_dream_wooden"
        },
        {
            "name": "Cozy Fireplace",
            "thumb": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_healing_fire.png",
            "type": "healing_fire"
        },
        {
            "name": "Modern",
            "thumb": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_music_modern.png",
            "type": "music_modern"
        },
        {
            "name": "Home Screen Wallpaper",
            "thumb": "/usr/palm/applications/com.webos.app.artisticdisplay/assets/thumbnails/thumb_home.png",
            "type": "homeBg"
        }
    ],
    "wallPaperSettings": {
        "artisticDisplayTheme": "clock_flip",
        "artisticDisplayThemeVersion": 0,
        "homeImageVersion": 0,
        "imageLimit": 0,
        "isFullView": false
    },
    "watchedListCollection": "on",
    "webOSPromotionVideo": "on",
    "yourMomentsVersion": "0",
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
    "autoSLZoomWithObjectDetection": false,
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
    "enable144HzBooster": "off",
    "enableALLM": "on",
    "enableDolbyVisionPC": "off",
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
    "homeAppLaunched": "off",
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
    "homelegalPopup": "on",
    "hueSyncAutoEnable": false,
    "hueSyncManualEnable": false,
    "illuminanceThreshold": 0,
    "inputOptimization": "auto",
    "isFirstCapture": "true",
    "isHdpOpAppPopupDone": false,
    "isSLZoomExecutable": false,
    "isSLZoomOn": "off",
    "isSLZoomOperable": false,
    "isfUpdated": "false",
    "lgLogoDisplay": "on",
    "lightingAutoBrightness": "off",
    "lightingBrightness": 8,
    "lightingColorMode": "whiteColorMode",
    "lightingEnable": "off",
    "lightingMode": "dynamic",
    "lightingTnativeBrightness": 100,
    "lightingTnativeMode": "off",
    "lowLevelAdjustment": 0,
    "lowPowerMode": "off",
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
            "fptplay": {
                "app_id": "com.fpt.fptplay",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "shahid": {
                "app_id": "net.mbc.shahid-lgapp",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "wavve": {
                "app_id": "pooq",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "coupangplay": {
                "app_id": "coupangplay",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "stan": {
                "app_id": "stan.webos2",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "shop": {
                "app_id": "com.lgshop.app79",
                "isActive": false,
                "launch_param": null
            }
        },
        {
            "slingtv": {
                "app_id": "com.movenetworks.app.sling-tv-sling-production",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "tver": {
                "app_id": "tver",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "hulu": {
                "app_id": "jp.happyon.app",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "nhkplus": {
                "app_id": "jp.nhk.plus",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "tod": {
                "app_id": "webos.tod.tv",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "apps": {
                "app_id": "com.webos.app.discovery",
                "isActive": false,
                "launch_param": null
            }
        },
        {
            "sonyliv": {
                "app_id": "com.sonyliv2.tvapp",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "tv360": {
                "app_id": "com.viettel.media.tv360",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "vtvgo": {
                "app_id": "com.vtvgotv.app",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "freeviewplay": {
                "app_id": "com.fvp.fve",
                "isActive": true,
                "launch_param": null
            }
        },
        {
            "wink": {
                "app_id": "ru.rt.video.app.tv",
                "isActive": false,
                "launch_param": null
            }
        },
        {
            "start": {
                "app_id": "start",
                "isActive": false,
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
    "multiViewLaunchMode": "sxs",
    "netflixHotkeyIsActive": true,
    "newKey": "on",
    "oledCareMode": "off",
    "oledCareRecommendation": "off",
    "othersColorMode": 0,
    "playbackThreshold": 200,
    "pseudoTouchMode": "on",
    "qmsVrr": "on",
    "quickSettingsMenuList": [
        "QuickSettings_picture_button",
        "QuickSettings_OledLcdBrightness_button",
        "QuickSettings_soundMode_button",
        "QuickSettings_soundOut_button",
        "QuickSettings_timer_button",
        "QuickSettings_eyecare_button",
        "QuickSettings_screenOff_button",
        "QuickSettings_privacyTerms_button",
        "QuickSettings_multiview_button",
        "QuickSettings_musicSearch_button"
    ],
    "quickSettingsRecentMenu": "",
    "screenRemoteAutoShow": "true",
    "screenRemoteExpanded": "false",
    "screenRemotePosition": "right",
    "simplinkAutoPowerOn": "on",
    "simplinkEnable": "off",
    "slzoomTargetAreaLevel": -1,
    "slzoomTargetAreaX": -1,
    "slzoomTargetAreaY": -1,
    "soundSyncModeColor": "auto",
    "soundSyncModeDisplayMode": "bar",
    "soundSyncModeFrequency": "mid",
    "soundSyncModeStaticColor": 35,
    "staticModeColor1": 35,
    "staticModeColor2": 1,
    "staticModeColor3": 12,
    "staticModeColor4": 0,
    "supportAirplay": false,
    "supportBnoModel": false,
    "svcMenuFlag": true,
    "touchRemoteLaunchMode": "edgeSwipe",
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
    "whiteColorMode": 1,
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
            "whiteBalanceLuminance"
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
            "ziggoRaiting"
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
amazon-alexa-adapter.*
amazon.*
audio.*
broadcast.*
com.palm.app.firstuse.*
com.palm.app.settings.*
com.palm.app.store-demo.*
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
com.webos.service.wowplay.*
com.webos.surfacemanager.*
con.webos.service.pbsw.*
dvr.*
extinput-service.*
gip.*
inputMap.*
mediaCapability.*
miracast.*
multiview.*
operatorApp.*
profile.*
system.*
tv.config.*
tv.conti.*
tv.hw.*
tv.model.*
tv.nyx.*
tv.rmm.*
wee.*
```

#### part of default DoVi config of >=55" C2 (DMSwVersion = 4.0, IDK_Version = SOC_5.0) (can be used for USB upload)
```ini
[Global]
# Panel Specific
Tmax = 810
Tmin = 0.001
# From panel specification
TPrimaries = 0.6801 0.3195 0.2603 0.6870 0.1470 0.0478 0.3127 0.329

# VSVDB Related Information
vsvdb_Tmax = 810
vsvdb_Tmin = 0.001
vsvdb_TPrimaries = 0.6801 0.3195 0.2603 0.6870 0.1470 0.0478 0.3127 0.329

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
# Panel Specific
DBrightness = 0.6
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1
# Precision Detail
SupportsPrecisionRendering = 1
PrecisionRenderingStrength = 0.75
PrecisionRendering29Scalar = 0.75
DBrightness_PR_on = 0.6
DLocalContrast = 0.2

[PictureMode = 1]
PictureModeName = CinemaHome
# Panel Specific
DBrightness = 0.3
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1
# Precision Detail
SupportsPrecisionRendering = 1
PrecisionRenderingStrength = 0.75
PrecisionRendering29Scalar = 0.75
DBrightness_PR_on = 0.35
DLocalContrast = 0.2

[PictureMode = 2]
PictureModeName = Cinema
# Panel Specific
DBrightness = 0.0
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 0
# Precision Detail
SupportsPrecisionRendering = 0
PrecisionRenderingStrength = 0.15
PrecisionRendering29Scalar = 0.15
DBrightness_PR_on = 0.0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
DBrightness = 0.3
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1
# Precision Detail
SupportsPrecisionRendering = 1
PrecisionRenderingStrength = 0.75
PrecisionRendering29Scalar = 0.75
DBrightness_PR_on = 0.3
DLocalContrast = 0.2

[PictureMode = 4]
PictureModeName = Game
# Panel Specific
DBrightness = 0.3
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1
# Precision Detail
SupportsPrecisionRendering = 0
PrecisionRenderingStrength = 0.15
PrecisionRendering29Scalar = 0.15
DBrightness_PR_on = 0.3
```

##### differences in <=48" C2 config
```ini
[Global]
# Panel Specific
Tmax = 648

# VSVDB Related Information
vsvdb_Tmax = 648
```

##### differences in 55"-77" G2 config
```ini
[Global]
# Panel Specific
Tmax = 990

# VSVDB Related Information
vsvdb_Tmax = 990
```

##### part of default DoVi config of B2 (DMSwVersion = 4.0, IDK_Version = SOC_1.6.1.4)
```ini
[Global]
# Panel Specific
Tmax = 640
Tmin = 0.001
# From panel specification
TPrimaries = 0.6773 0.3219 0.2586 0.6762 0.1449 0.0484 0.3127 0.329

# VSVDB Related Information
vsvdb_Tmax = 640
vsvdb_Tmin = 0.001
vsvdb_TPrimaries = 0.6773 0.3219 0.2586 0.6762 0.1449 0.0484 0.3127 0.329

# PictureMode 0-4 don't support Iamge Customization.
[PictureMode = 0]
PictureModeName = Vivid
# Panel Specific
Tmax = 224
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1

[PictureMode = 1]
PictureModeName = CinemaHome
# Panel Specific
Tmax = 320
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1

[PictureMode = 2]
PictureModeName = Cinema
SupportsDM3 = 1
BrightnessPreservation = 0
# Panel Specific
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 0

[PictureMode = 3]
PictureModeName = Standard
# Panel Specific
Tmax = 320
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1

[PictureMode = 4]
PictureModeName = Game
# Panel Specific
Tmax = 320
# Dark Detail
DarkDetail = 0
DarkDetailCompLum = 50
# Light Sense
Ambient = 1
```

##### differences in A2 config compared to B2
```ini
[Global]
# Panel Specific
Tmax = 576
# From panel specification
TPrimaries = 0.6772 0.3221 0.2604 0.6735 0.1440 0.0475 0.3127 0.329

# VSVDB Related Information
vsvdb_Tmax = 576
vsvdb_TPrimaries = 0.6772 0.3221 0.2604 0.6735 0.1440 0.0475 0.3127 0.329

[PictureMode = 0]
Tmax = 202

[PictureMode = 1]
Tmax = 288

[PictureMode = 3]
Tmax = 288

[PictureMode = 4]
Tmax = 288
```
