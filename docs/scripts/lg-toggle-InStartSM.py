import asyncio
import os
from bscpylgtv import StorageSqliteDict, WebOsClient
from lg_constants import DB_PATH, DB_TABLE_COOKIE, LG_IP

async def runloop():
    cookieName = os.path.basename(__file__)
    storage = await StorageSqliteDict.create(DB_PATH, DB_TABLE_COOKIE)
    cookie = await storage.get_key(cookieName)

    client = await WebOsClient.create(LG_IP, ping_interval=None, getSystemInfo=False, skipStateInfo=True, key_file_path=DB_PATH)
    await client.connect()

    if cookie != 1:
        await client.launch_app_with_params('com.webos.app.factorywin', {"id": "executeFactory", "irKey": "inStart"})

        await asyncio.sleep(2)

        await client.number_button(0)
        await client.number_button(4)
        await client.number_button(1)
        await client.number_button(3)

        await storage.set_key(cookieName, 1)
    else:
        await client.close_app('com.webos.app.factorywin')

        await storage.set_key(cookieName, 0)

    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
