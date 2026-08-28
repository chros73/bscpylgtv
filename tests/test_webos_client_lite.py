import asyncio
import sys

import pytest
from bscpylgtv import WebOsClient


@pytest.mark.asyncio
async def test_closeout_pattern_with_async_callback_is_wait_safe(tmp_path):
    """connect_handler's finally block hands state-update callback results to
    asyncio.wait(), which rejects raw coroutines with TypeError on Python
    3.11+ — aborting the closeout and leaving the client half-torn-down.
    Post-fix, callback results are wrapped with asyncio.ensure_future()."""

    client = await WebOsClient.create(
        "127.0.0.1",
        key_file_path=str(tmp_path / "key.sqlite"),
        states=[],
        timeout_connect=1,
    )

    fired = []

    async def on_update(client_arg):
        fired.append(client_arg)
        await asyncio.sleep(0)

    # doStateUpdate is False before connect: registration only appends.
    await client.register_state_update_callback(on_update)

    # Exact closeout semantics from connect_handler's finally block
    # (post-fix): callback results are wrapped with ensure_future().
    closeout = set()
    closeout.update(client.handler_tasks)
    for callback in client.state_update_callbacks:
        closeout.add(asyncio.ensure_future(callback(client)))

    done, pending = await asyncio.wait(closeout, timeout=5)
    assert pending == set()
    assert len(done) == 1
    assert fired  # the teardown fire reached the callback

    if sys.version_info >= (3, 11):
        # Pre-fix behaviour, kept as the regression guard: a raw coroutine
        # in the closeout set crashes asyncio.wait().
        async def raw(_client_arg):
            pass

        coro = raw(client)
        with pytest.raises(TypeError):
            await asyncio.wait({coro}, timeout=5)
        coro.close()


@pytest.mark.asyncio
class TestWebOsClientLite():

    data_calibration_support_info = [
        ( 'HE_DTV_W99H_XXXXXXXX',   {"foo": "17pt", "dovi": "2019" },   None,   2019,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "foo", "dovi": "2019" },  None,   2019,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt", "foo": "2019" },  17,     None,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt", "dovi": "foo" },  17,     None,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt" },                 17,     None,   0 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"dovi": "2019" },                  None,   2019,   0 ),

        ( 'HE_DTV_W99H_XXXXXXXX',   {"foo": "17pt", "foo": "2019" },    None,   None,   1 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "foo", "dovi": "foo" },   None,   None,   1 ),
        ( 'HE_DTV_W99H_XXXXXXXX',   {"lut3d": "17pt", "dovi": "2019" }, 17,     2019,   1 ),
        ( 'HE_DTV_W99O_XXXXXXXX',   {"lut3d": "33pt", "dovi": "2019" }, 33,     2019,   1 ),
        ( None,                     {"lut3d": "17pt", "dovi": "2019" }, 17,     2019,   1 ),
        ( None,                     {"lut3d": "33pt", "dovi": "2019" }, 33,     2019,   1 ),

        ( 'HE_DTV_W17H_XXXXXXXX',   None,                               None,   None,   1 ),
        ( 'HE_DTV_W17O_XXXXXXXX',   None,                               None,   None,   1 ),

        ( 'HE_DTV_W18H_XXXXXXXX',   None,                               17,     2018,   1 ),
        ( 'HE_DTV_W18O_XXXXXXXX',   None,                               33,     2018,   1 ),

        ( 'HE_DTV_W19H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W19O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W20H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W20O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W21H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W21O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W22H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W22O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W23H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W23O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W24H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W24G_XXXXXXXX',   None,                               33,     2019,   1 ),
        ( 'HE_DTV_W24O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W25H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W25G_XXXXXXXX',   None,                               33,     2019,   1 ),
        ( 'HE_DTV_W25O_XXXXXXXX',   None,                               33,     2019,   1 ),

        ( 'HE_DTV_W26H_XXXXXXXX',   None,                               17,     2019,   1 ),
        ( 'HE_DTV_W26G_XXXXXXXX',   None,                               33,     2019,   1 ),
        ( 'HE_DTV_W26O_XXXXXXXX',   None,                               33,     2019,   1 ),
    ]

    @pytest.mark.parametrize("model,calInfo,lut3d,dovi,expected", data_calibration_support_info)
    async def test_calibration_support_info(self, model, calInfo, lut3d, dovi, expected):
        client = await WebOsClient.create("x", states=["software_info"], calibration_info=calInfo, client_key="x")
        client._software_info = {"model_name" : model}
        client.calibration_support_info()

        if expected > 0:
            cal_info = {
                "lut3d":    lut3d,
                "dovi":     dovi,
            }
        else:
            cal_info = {}
            if lut3d:
                cal_info["lut3d"] = lut3d
            if dovi:
                cal_info["dovi"] = dovi

        assert cal_info == client._calibration_info

