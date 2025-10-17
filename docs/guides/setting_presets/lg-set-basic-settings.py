# Config basic settings

import asyncio
from bscpylgtv import WebOsClient
from lg_constants import DB_PATH, LG_IP

async def runloop():
    client = await WebOsClient.create(LG_IP, ping_interval=None, states=[], key_file_path=DB_PATH)
    await client.connect()


    # Set APS preset
    print("\n### eco ###")
    await client.set_system_picture_mode(pic_mode="eco")
    await asyncio.sleep(3)

    print("\n# Set OLED Light to 0, disable Reduce Blue Light, Filmmaker Mode Auto Start, Screen Move, Logo Luminance Adjust, Energy Saving, Warning on changing preset for the first time")
    await client.set_settings(category="picture", settings={"backlight": "0", "eyeComfortMode": "off", "filmMakerMode": "off", "screenShift": "off", "logoLuminanceAdjust": "off", "energySaving": "off", "energySavingModified": "true", "erpUserConfirm": True})
    await asyncio.sleep(2)
    await client.button(name="ENTER")
    await asyncio.sleep(1)

    print("\n# Set Aspect Ratio to Original, Just Scan to On")
    await client.set_system_settings(category="aspectRatio", settings={"arcPerApp": "original", "justScan": "on"})
    await asyncio.sleep(1)

    print("\n# Set UHD Deep color to 4K, Simplink/CEC to On, disable Displaying LG logo and OLED Care settings")
    await client.set_settings(category="other", settings={"uhdDeepColor": "4k", "simplinkEnable": "on", "simplinkAutoPowerOn": "on", "lgLogoDisplay": "off", "oledCareMode": "off", "oledCareRecommendation": "off", "contentRecommendation": "off"})
    await asyncio.sleep(2)
    await client.button(name="ENTER")
    await asyncio.sleep(1)

    print("\n# Disable QuickStart+, Live Plus, Live Promotion, Settings Help, Set Pointer size and speed")
    await client.set_settings(category="option", settings={"quickStartMode": "off", "livePlus": "off", "livePromotion": "off", "helpOnSettings": "off", "pointerSize": "small", "pointerSpeed": "fast"})
    await asyncio.sleep(1)

    print("\n# Set Audio to eARC, Bitstream, Passthrough")
    await client.set_settings(category="sound", settings={"soundOutput": "external_arc", "digitalAudioPriority": "auto", "avSyncBypassInput": "on", "inputAudioFormatHDMI2": "bitstream", "soundOutputDigital": "passThrough", "eArcSupport": "on"})
    await asyncio.sleep(1)

    print("\n# Disable IPv6, enable WakeOnLan")
    await client.set_settings(category="network", settings={"ipv6Enable": "false", "wolwowlOnOff": "true"})
    await asyncio.sleep(1)

    print("\n# Disable No Signal Image, enable Limit Ad Tracking, disable AI Smart Tips, Smart Tips in Settings, Home Promotion, Screen Saver Promotion, Home Auto launch")
    await client.set_settings(category="general", settings={"noSignalScreenSaver": "off", "lmt": "on", "aiNudge": "off", "aiSettingsNudge": "off", "homePromotion": "off", "screenSaverAd": "off", "homeAutoLaunch": "off", "selectedInputApp": "off", "checkHomeAutoLaunchValue": "user"})
    await asyncio.sleep(1)

    print("\n# Disbale Auto Firmware Update")
    await client.set_system_settings(category="support", settings={"automaticUpdate": "off"})
    await asyncio.sleep(1)

    print("\n# Set Auto Power Off to 4 hours")
    await client.set_settings(category="time", settings={"automaticStandBy": "4", "autoOff2HourOnTimer": "on"})


    await client.disconnect()

asyncio.run(runloop())
