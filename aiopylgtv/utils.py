import argparse
import asyncio

from aiopylgtv import WebOsClient


async def runloop(args):
    client = await WebOsClient.create(args.host, timeout_connect=2)
    await client.connect()
    print(await getattr(client, args.command)(*args.parameters))
    await client.disconnect()


def convert_arg(arg):
    try:
        return int(arg)
    except ValueError:
        pass
    try:
        return float(arg)
    except ValueError:
        pass
    if arg.lower() == "true":
        return True
    elif arg.lower() == "false":
        return False
    return arg


def aiopylgtvcommand():
    parser = argparse.ArgumentParser(description="Send command to LG WebOs TV.")
    parser.add_argument(
        "host", type=str, help="hostname or ip address of the TV to connect to"
    )
    parser.add_argument(
        "command",
        type=str,
        help="command to send to the TV (can be any function of WebOsClient)",
    )
    parser.add_argument(
        "parameters",
        type=convert_arg,
        nargs="*",
        help="additional parameters to be passed to WebOsClient function call",
    )

    args = parser.parse_args()

    asyncio.run(runloop(args))
