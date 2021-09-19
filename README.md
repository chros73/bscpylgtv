# aiopylgtv
Library to control webOS based LG Tv devices, basic version of aiopylgtv at https://github.com/bendavid/aiopylgtv

Based on pylgtv library at https://github.com/TheRealLink/pylgtv which is no longer maintained.

## Requirements
- Python >= 3.7

## Install
```bash
pip install bscpylgtv
```

## Install from Source
Run the following command inside this folder
```bash
pip install --upgrade .
```

## Basic Example

```python
import asyncio
from bscpylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.1.53')
    await client.connect()
    apps = await client.get_apps()
    for app in apps:
        print(app)

    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
```

## Development of `bscpylgtv`

We use [`pre-commit`](https://pre-commit.com) to keep a consistent code style, so ``pip install pre_commit`` and run
```bash
pre-commit install
```
to install the hooks.
