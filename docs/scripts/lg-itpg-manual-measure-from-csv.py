# Display patches from csv file using iTPG for manual measurements
# Usage: lg-itpg-manual-measure-from-csv.py csv_file.csv [bfi_interval [patch_interval [patch_size]]]
#   lg-itpg-manual-measure-from-csv.py csv/rgbw_limited_10bit.csv
#   lg-itpg-manual-measure-from-csv.py csv/rgbw_limited_10bit.csv 2
#   lg-itpg-manual-measure-from-csv.py csv/rgbw_limited_10bit.csv 2 3
#   lg-itpg-manual-measure-from-csv.py csv/rgbw_limited_10bit.csv 2 3 2

import asyncio
import csv
import math
import sys
from bscpylgtv import WebOsClient
from lg_constants import DB_PATH, LG_IP

screen_resolution = (3840, 2160)
bfi_interval = 0
patch_interval = 3
patch_size = 5


async def get_optional_argument(number, default):
    return int(sys.argv[number]) if len(sys.argv) > number else default


async def get_window_properties(screen_resolution, patch_size):
    ratio = screen_resolution[0] / screen_resolution[1]
    area = screen_resolution[0] * screen_resolution[1] * patch_size / 100
    height = int(round(math.sqrt(area/ratio)))
    width = int(round(height * ratio))
    startx = int(round(screen_resolution[0] / 2 - width / 2))
    starty = int(round(screen_resolution[1] / 2 - height / 2))
    window = {'width': width, 'height': height, 'startx': startx, 'starty': starty}

    if patch_size < 100:
        print(f"patch window: {window}")

    return window


async def display_patch(client, patch, patch_interval, bfi_interval, window_full, window_patch):
    """ Display full screen black window in the background and color patch on top of it
    in the given window size. The complete new state should always be set for both."""

    print(f"patch: {patch}")
    await client.set_itpg_patch(r=int(patch[1]), g=int(patch[2]), b=int(patch[3]), win_id=1, width=window_patch['width'], height=window_patch['height'], startx=window_patch['startx'], starty=window_patch['starty'])
    await client.set_itpg_patch(r=0, b=0, g=0, win_id=0, width=window_full['width'], height=window_full['height'], startx=window_full['startx'], starty=window_full['starty'])

    await client.toggle_itpg(enable=True, numOfBox=2)
    await asyncio.sleep(patch_interval)

    if bfi_interval:
        print("BFI")
        # Set full screen black window in the background again
        await client.set_itpg_patch(r=0, b=0, g=0, win_id=0, width=window_full['width'], height=window_full['height'], startx=window_full['startx'], starty=window_full['starty'])
        await client.toggle_itpg(enable=True, numOfBox=1)
        await asyncio.sleep(bfi_interval)


async def runloop(screen_resolution, bfi_interval, patch_interval, patch_size):
    # Get command line arguments
    csv_filename = sys.argv[1]
    bfi_interval = await get_optional_argument(2, bfi_interval)
    patch_interval = await get_optional_argument(3, patch_interval)
    patch_size = await get_optional_argument(4, patch_size)

    # Connect to WebOS
    client = await WebOsClient.create(LG_IP, states=["system_info"], key_file_path=DB_PATH)
    await client.connect()

    # Get full and patch window properties
    window_full = await get_window_properties(screen_resolution, 100)
    window_patch = await get_window_properties(screen_resolution, patch_size)

    # Import csv file
    with open(csv_filename, newline='') as csv_file:
        cvs_reader = csv.reader(csv_file, delimiter=',')
        for patch in cvs_reader:
            # Display background and color patch on top of it
            await display_patch(client, patch, patch_interval, bfi_interval, window_full, window_patch)

    # Disable patches
    await client.toggle_itpg(enable=False, numOfBox=0)

    # Disconnect WebOS
    await client.disconnect()


asyncio.run(runloop(screen_resolution, bfi_interval, patch_interval, patch_size))
