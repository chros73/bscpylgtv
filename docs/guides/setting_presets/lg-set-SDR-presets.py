# Config all SDR presets to oled light 34, gamma 2.4, except for:
#     - eco:         0  (51n), gamma 2.4
#     - game:       34 (118n), gamma 2.2
#     - cinema:     84 (234n), gamma 2.4, upload gamma 2.68 3D LUT for night
#     - filmMaker:  84 (234n), gamma 2.4, upload gamma 2.48 3D LUT for day
#     - expert1:    43 (138n), gamma 2.2, upload gamma 2.20 3D LUT for day
#     - expert2:    34 (118n), gamma 2.4, upload gamma 2.40 3D LUT for night

import asyncio
import logging
from bscpylgtv import WebOsClient
from lg_constants import DB_PATH, LG_IP

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logging.getLogger("bscpylgtv").setLevel(logging.DEBUG)
logger = logging.getLogger("bscpylgtv")

async def runloop():
    client = await WebOsClient.create(LG_IP, ping_interval=None, states=["software_info"], key_file_path=DB_PATH)
    await client.connect()


    # Set preset
    logger.info("\n### vivid ###")
    await client.set_system_picture_mode(pic_mode="vivid")
    await asyncio.sleep(3)
    await client.set_system_settings(category="picture", settings={"backlight": "34", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### normal ###")
    await client.set_system_picture_mode(pic_mode="normal")
    await asyncio.sleep(3)
    await client.set_system_settings(category="picture", settings={"backlight": "34", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### eco ###")
    await client.set_system_picture_mode(pic_mode="eco")
    await asyncio.sleep(3)
    await client.set_system_settings(category="picture", settings={"backlight": "0", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### sports ###")
    await client.set_system_picture_mode(pic_mode="sports")
    await asyncio.sleep(3)
    await client.set_system_settings(category="picture", settings={"backlight": "34", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### game ###")
    await client.set_system_picture_mode(pic_mode="game")
    await asyncio.sleep(3)
    await client.set_system_settings(category="picture", settings={"backlight": "34", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "auto", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### cinema ###")
    await client.set_system_picture_mode(pic_mode="cinema")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="cinema")
    await asyncio.sleep(3)
    await client.set_bypass_modes_sdr()
    await asyncio.sleep(3)
    await client.upload_3d_lut_bt709_from_file(filename="sdr-cinema-g268-o84-234n-33p-3dlut.cube")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_system_settings(category="picture", settings={"backlight": "84", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### filmMaker ###")
    await client.set_system_picture_mode(pic_mode="filmMaker")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="filmMaker")
    await asyncio.sleep(3)
    await client.set_bypass_modes_sdr()
    await asyncio.sleep(3)
    await client.upload_3d_lut_bt709_from_file(filename="sdr-cinema-g248-o84-234n-33p-3dlut.cube")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_system_settings(category="picture", settings={"backlight": "84", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### expert1 ###")
    await client.set_system_picture_mode(pic_mode="expert1")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="expert1")
    await asyncio.sleep(3)
    await client.set_bypass_modes_sdr()
    await asyncio.sleep(3)
    await client.upload_3d_lut_bt709_from_file(filename="sdr-expert1-g220-o43-138n-33p-3dlut.cube")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_system_settings(category="picture", settings={"backlight": "43", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "medium", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)

    # Set preset
    logger.info("\n### expert2 ###")
    await client.set_system_picture_mode(pic_mode="expert2")
    await asyncio.sleep(3)

    await client.start_calibration(picture_mode="expert2")
    await asyncio.sleep(3)
    await client.set_bypass_modes_sdr()
    await asyncio.sleep(3)
    await client.upload_3d_lut_bt709_from_file(filename="sdr-expert2-g240-o34-118n-33p-3dlut.cube")
    await asyncio.sleep(3)
    await client.end_calibration()
    await asyncio.sleep(3)

    await client.set_system_settings(category="picture", settings={"backlight": "34", "contrast": "85", "brightness": "50", "dynamicContrast": "off", "peakBrightness": "off", "gamma": "high1", "motionEyeCare": "off", "color": "50", "tint": "0", "colorGamut": "native", "dynamicColor": "off", "colorTemperature": "50", "sharpness": "0", "superResolution": "off", "noiseReduction": "off", "mpegNoiseReduction": "off", "smoothGradation": "off", "realCinema": "on"})
    await asyncio.sleep(1)
    await client.set_system_settings(category="picture", settings={"truMotionMode": "off"}, current_app=True)
    await asyncio.sleep(1)
    await client.set_settings(category="aiPicture", settings={"ai_Picture": "off", "ai_Brightness": "off", "ai_Genre": "off"})
    await asyncio.sleep(1)
    await client.set_settings(category="picture", settings={"applyToAllInput": "picture"})
    await asyncio.sleep(3)


    await client.set_system_picture_mode(pic_mode="eco")


    await client.disconnect()

asyncio.run(runloop())
