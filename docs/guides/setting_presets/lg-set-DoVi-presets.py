# Config all DoVi presets to be the same:
#     - dolbyHdrVivid, dolbyHdrStandard: apply the DoVi 2 point Low WB hack along with 22pt adjustment
#     - dolbyHdrGame, dolbyHdrCinemaBright, dolbyHdrCinema: upload the same 1D LUT (RGB only calibration)

import asyncio
import logging
from bscpylgtv import WebOsClient
from lg_constants import DB_PATH, LG_IP

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logging.getLogger("bscpylgtv").setLevel(logging.DEBUG)
logger = logging.getLogger("bscpylgtv")

async def runloop():
    client = await WebOsClient.create(LG_IP, ping_interval=None, states=[], key_file_path=DB_PATH)
    await client.connect()


    # Set preset
    logger.info("\n### dolbyHdrVivid ###")
    await client.set_system_picture_mode(pic_mode="dolbyHdrVivid")
    await asyncio.sleep(3)
    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "dolbyPrecisionDetail": "off", "whiteBalanceMethod": "22", "whiteBalanceRed": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "whiteBalanceGreen": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "whiteBalanceBlue": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "-2", "whiteBalanceGreenOffset": "-2", "whiteBalanceBlueOffset": "-2", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceIre": "10"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### dolbyHdrStandard ###")
    await client.set_system_picture_mode(pic_mode="dolbyHdrStandard")
    await asyncio.sleep(3)
    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "dolbyPrecisionDetail": "off", "whiteBalanceMethod": "22", "whiteBalanceRed": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "whiteBalanceGreen": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "whiteBalanceBlue": [2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "whiteBalancePoint": "low", "whiteBalanceRedOffset": "-2", "whiteBalanceGreenOffset": "-2", "whiteBalanceBlueOffset": "-2", "whiteBalanceRedGain": "0", "whiteBalanceGreenGain": "0", "whiteBalanceBlueGain": "0", "whiteBalanceIre": "10"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### dolbyHdrGame ###")
    await client.set_system_picture_mode(pic_mode="dolbyHdrGame")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="dolby_game")
    await asyncio.sleep(3)
    await client.upload_1d_lut_from_file(filename="dovi.1dlut")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "dolbyPrecisionDetail": "off"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### dolbyHdrCinemaBright ###")
    await client.set_system_picture_mode(pic_mode="dolbyHdrCinemaBright")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="dolby_cinema_bright")
    await asyncio.sleep(3)
    await client.upload_1d_lut_from_file(filename="dovi.1dlut")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "dolbyPrecisionDetail": "off"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### dolbyHdrCinema ###")
    await client.set_system_picture_mode(pic_mode="dolbyHdrCinema")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="dolby_cinema_dark")
    await asyncio.sleep(3)
    await client.upload_1d_lut_from_file(filename="dovi.1dlut")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_settings(category="picture", settings={"backlight": "100", "contrast": "100", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "high", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "-50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on", "dolbyPrecisionDetail": "off"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})


    await client.disconnect()

asyncio.run(runloop())
