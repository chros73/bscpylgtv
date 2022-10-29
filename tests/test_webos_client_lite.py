import pytest
from bscpylgtv import WebOsClient


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

