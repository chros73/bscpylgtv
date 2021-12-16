import argparse
import asyncio
import json

from ._version import __version__
from bscpylgtv import WebOsClient


async def list_keys(path_key_file):
    client = await WebOsClient.create(None, key_file_path=path_key_file)
    storage = await client.get_storage()
    await storage.list_keys()

async def runloop(args):
    client = await WebOsClient.create(args.host, ping_interval=None, get_hello_info=args.get_hello_info,
        states=args.states, client_key=args.key, key_file_path=args.path_key_file)
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
    try:
        return json.loads(arg)
    except ValueError:
        pass
    if arg.lower() == "true":
        return True
    elif arg.lower() == "false":
        return False
    return arg


def bscpylgtvcommand():
    parser = argparse.ArgumentParser(description="Send command to LG WebOs TV.")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        "-l", "--list_client_keys",
        dest="list_client_keys",
        action="store_true",
        help="display all saved client keys per ip"
    )
    parser.add_argument(
        "-p", "--path_key_file", type=str, help="optional path to key file"
    )

    argsL, remainder = parser.parse_known_args()

    if argsL.list_client_keys:
        asyncio.run(list_keys(argsL.path_key_file))
    else:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-k", "--key", type=str, help="optional client key"
        )
        parser.add_argument(
            "-o", "--get_hello_info",
            dest="get_hello_info",
            action="store_true",
            help="optional getting hello info (e.g. to get unique deviceUUID)"
        )
        parser.add_argument(
            "-s", "--set_states",
            dest="states",
            type=convert_arg,
            nargs="?",
            const='["system_info"]',
            help='optional setting states ("system_info" static state is required by some of the calibration commands)'
        )
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

        args = parser.parse_args(remainder, namespace=argsL)

        asyncio.run(runloop(args))
