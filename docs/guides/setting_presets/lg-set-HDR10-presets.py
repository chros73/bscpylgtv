# Config all HDR10 presets to be the same:
#     - apply 22pt WB RGB only calibration
#     - hdrCinema: set tone mapping params to 870 1000 100 4000 100 10000 100
#     - hdrFilmMaker: set tone mapping params to 950 1000 100 4000 100 10000 100

import asyncio
from bscpylgtv import WebOsClient
from lg_constants import DB_PATH, LG_IP

async def runloop():
    client = await WebOsClient.create(LG_IP, ping_interval=None, states=[], key_file_path=DB_PATH)
    await client.connect()


    # Set preset
    print("\n### hdrVivid ###")
    await client.set_system_picture_mode(pic_mode="hdrVivid")
    await asyncio.sleep(3)
    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "hdrDynamicToneMapping": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "whiteBalanceMethod": "22code", "whiteBalanceRed": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], "whiteBalanceGreen": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], "whiteBalanceBlue": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "0", "whiteBalanceGreenOffset": "0", "whiteBalanceBlueOffset": "0", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceCodeValue": "20"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    print("\n### hdrStandard ###")
    await client.set_system_picture_mode(pic_mode="hdrStandard")
    await asyncio.sleep(3)
    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "hdrDynamicToneMapping": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "whiteBalanceMethod": "22code", "whiteBalanceRed": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], "whiteBalanceGreen": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], "whiteBalanceBlue": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "0", "whiteBalanceGreenOffset": "0", "whiteBalanceBlueOffset": "0", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceCodeValue": "20"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    print("\n### hdrCinemaBright ###")
    await client.set_system_picture_mode(pic_mode="hdrCinemaBright")
    await asyncio.sleep(3)
    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "hdrDynamicToneMapping": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "whiteBalanceMethod": "22code", "whiteBalanceRed": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], "whiteBalanceGreen": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], "whiteBalanceBlue": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "0", "whiteBalanceGreenOffset": "0", "whiteBalanceBlueOffset": "0", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceCodeValue": "20"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    print("\n### hdrGame ###")
    await client.set_system_picture_mode(pic_mode="hdrGame")
    await asyncio.sleep(3)
    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "hdrDynamicToneMapping": "HGIG", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "whiteBalanceMethod": "22code", "whiteBalanceRed": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], "whiteBalanceGreen": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], "whiteBalanceBlue": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "0", "whiteBalanceGreenOffset": "0", "whiteBalanceBlueOffset": "0", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceCodeValue": "20"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    print("\n### hdrCinema ###")
    await client.set_system_picture_mode(pic_mode="hdrCinema")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="hdr_cinema")
    await asyncio.sleep(3)
    await client.set_tonemap_params("hdr_cinema", 870, 1000, 100, 4000, 100, 10000, 100)
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "hdrDynamicToneMapping": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "whiteBalanceMethod": "22code", "whiteBalanceRed": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], "whiteBalanceGreen": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], "whiteBalanceBlue": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "0", "whiteBalanceGreenOffset": "0", "whiteBalanceBlueOffset": "0", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceCodeValue": "20"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    print("\n### hdrFilmMaker ###")
    await client.set_system_picture_mode(pic_mode="hdrFilmMaker")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="hdr_filmMaker")
    await asyncio.sleep(3)
    await client.set_tonemap_params("hdr_filmMaker", 950, 1000, 100, 4000, 100, 10000, 100)
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "hdrDynamicToneMapping": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "whiteBalanceMethod": "22code", "whiteBalanceRed": [0,2,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-2,0,0], "whiteBalanceGreen": [1,2,0,1,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,0,0,0,0,0], "whiteBalanceBlue": [-1,1,-1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,3,4,4,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "0", "whiteBalanceGreenOffset": "0", "whiteBalanceBlueOffset": "0", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceCodeValue": "20"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})


    await client.disconnect()

asyncio.run(runloop())
