import asyncio
import os
from bscpylgtv import StorageSqliteDict, WebOsClient
from lg_constants import DB_PATH, DB_TABLE_COOKIE, LG_IP

async def runloop():
    cookieName = os.path.basename(__file__)
    storage = await StorageSqliteDict.create(DB_PATH, DB_TABLE_COOKIE)
    cookie = await storage.get_key(cookieName)

    client = await WebOsClient.create(LG_IP, ping_interval=None, states=[], key_file_path=DB_PATH)
    await client.connect()

    if cookie != 1:
        await client.launch_app_with_params('com.palm.app.settings', {"target": "picture"})

        await asyncio.sleep(2)

        await client.button("RIGHT")
        await client.button("1")
        await client.button("1")
        await client.button("1")
        await client.button("3")
        await client.button("1")
        await client.button("1")
        await client.button("1")

        await storage.set_key(cookieName, 1)
    else:
        await client.close_app('com.palm.app.settings')

        await storage.set_key(cookieName, 0)

    await client.disconnect()

asyncio.run(runloop())
