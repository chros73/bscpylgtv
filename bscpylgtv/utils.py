import argparse
import asyncio
import json

from bscpylgtv import WebOsClient


def list_client_keys(path_key_file):
    if not path_key_file:
        path_key_file = WebOsClient._get_key_file_path()
    WebOsClient.list_client_keys(path_key_file)

async def runloop(args):
    client = await WebOsClient.create(args.host, timeout_connect=2, ping_interval=None,
        getSystemInfo=args.get_system_info, skipStateInfo=True,
        client_key=args.key, key_file_path=args.path_key_file, disable_key_file=args.disable_key_file)
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
        list_client_keys(argsL.path_key_file)
    else:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-k", "--key", type=str, help="optional client key"
        )
        parser.add_argument(
            "-d", "--disable_key_file",
            dest="disable_key_file",
            action="store_true",
            help="optional disabling key file"
        )
        parser.add_argument(
            "-g", "--get_system_info",
            dest="get_system_info",
            action="store_true",
            help="optional getting system info (required by some of the calibration commands)"
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
