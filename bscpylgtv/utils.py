import argparse
import asyncio
import json
import logging

from ._version import __version__
from bscpylgtv import WebOsClient


async def list_keys(path_key_file):
    """Print all saved client keys from the configured key store."""
    client = await WebOsClient.create(None, key_file_path=path_key_file)
    storage = await client.get_storage()
    keys = await storage.list_keys()
    for key, value in keys.items():
        print(key, value)

async def runloop(args):
    """Execute a series of LG webOS commands provided via the command-line parser."""
    # parse multiple commands with parameters separated by ","
    commands = []
    current = []
    for arg in args.commands:
        if arg == ",":
            if current:
                commands.append(current)
                current = []
        else:
            current.append(arg)
    if current:
        commands.append(current)
    
    client = await WebOsClient.create(
        ip=args.host,
        timeout_connect=args.timeout_connect,
        connect_retry_attempts=args.connect_retry_attempts,
        connect_retry_interval_ms=args.connect_retry_interval_ms,
        ping_interval=None,
        volume_step_delay_ms=args.volume_step_delay_ms,
        get_hello_info=args.get_hello_info,
        without_ssl=args.without_ssl,
        states=args.states,
        calibration_info=args.calibration_info,
        client_key=args.key,
        key_file_path=args.path_key_file,
        manifest_file_path=args.manifest_file_path,
        pairing_type=args.pairing_type
    )
    await client.connect()
    for cmd in commands:
        cmd_name = cmd[0]
        cmd_args = cmd[1:]
        print(await getattr(client, cmd_name)(*cmd_args))
    await client.disconnect()


def convert_arg(arg):
    """Coerce a command-line string argument to a JSON-like Python value."""
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
    """Entry point for the command-line interface used to control LG webOS TVs."""
    parser = argparse.ArgumentParser(description="Send command to LG WebOs TV.")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        "--log",
        dest="log",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="set logging level (default: DEBUG)",
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

    log_level = getattr(logging, argsL.log.upper(), logging.DEBUG)
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logging.getLogger("bscpylgtv").setLevel(log_level)

    if argsL.list_client_keys:
        asyncio.run(list_keys(argsL.path_key_file))
    else:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-k", "--key", type=str, help="optional client key"
        )
        parser.add_argument(
            "-m", "--manifest_file_path", type=str, help="optional path to manifest JSON file"
        )
        parser.add_argument(
            "-t", "--pairing_type", type=str, help="optional pairing type"
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
            const='["software_info"]',
            help='optional setting states ("software_info" static state is required by some of the calibration commands)'
        )
        parser.add_argument(
            "-c", "--set_calibration_info",
            dest="calibration_info",
            type=convert_arg,
            help='optional setting calibration info (for couple of calibration commands when chip type is not supported)'
        )
        parser.add_argument(
            "-w", "--without_ssl",
            dest="without_ssl",
            action="store_true",
            help="optional connecting without SSL"
        )
        parser.add_argument(
            "--timeout_connect",
            dest="timeout_connect",
            type=int,
            default=2,
            help="optional setting the connection timout in seconds"
        )
        parser.add_argument(
            "--connect_retry_attempts",
            dest="connect_retry_attempts",
            type=int,
            default=9,
            help="optional setting the number of times the client tries to connect to host"
        )
        parser.add_argument(
            "--connect_retry_interval_ms",
            dest="connect_retry_interval_ms",
            type=int,
            default=200,
            help="optional setting the time in ms between connection retries"
        )
        parser.add_argument(
            "--volume_step_delay_ms",
            dest="volume_step_delay_ms",
            type=int,
            help="optional setting the volume step delay in ms"
        )
        parser.add_argument(
            "host", type=str, help="hostname or ip address of the TV to connect to"
        )
        parser.add_argument(
            "commands",
            type=convert_arg,
            nargs="+",
            help="commands to send to the TV (can be any function of WebOsClient)",
        )

        args = parser.parse_args(remainder, namespace=argsL)

        asyncio.run(runloop(args))
