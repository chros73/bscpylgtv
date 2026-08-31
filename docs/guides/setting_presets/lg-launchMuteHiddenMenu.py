# Launch 3x Mute button hidden menu

import asyncio
import logging
from bscpylgtv import WebOsClient
from lg_constants import DB_PATH, LG_IP

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logging.getLogger("bscpylgtv").setLevel(logging.DEBUG)

async def runloop():
    client = await WebOsClient.create(LG_IP, ping_interval=None, states=[], key_file_path=DB_PATH)
    await client.connect()

    await client.launch_app_with_params('com.webos.app.tvhotkey', {"activateType": "mute-hidden-action"})

    await client.disconnect()

asyncio.run(runloop())
