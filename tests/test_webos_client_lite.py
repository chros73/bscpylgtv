import pytest
from bscpylgtv import WebOsClient


@pytest.mark.asyncio
class TestWebOsClientLite():

    data_calibration_support_info = [
        ( 'HE_DTV_W17H_XXXXXXXX',   (None,  None) ),
        ( 'HE_DTV_W17O_XXXXXXXX',   (None,  None) ),

        ( 'HE_DTV_W18H_XXXXXXXX',   (17,    2018) ),
        ( 'HE_DTV_W18O_XXXXXXXX',   (33,    2018) ),

        ( 'HE_DTV_W19H_XXXXXXXX',   (17,    2019) ),
        ( 'HE_DTV_W19O_XXXXXXXX',   (33,    2019) ),

        ( 'HE_DTV_W20H_XXXXXXXX',   (17,    2019) ),
        ( 'HE_DTV_W20O_XXXXXXXX',   (33,    2019) ),

        ( 'HE_DTV_W21H_XXXXXXXX',   (17,    2019) ),
        ( 'HE_DTV_W21O_XXXXXXXX',   (33,    2019) ),

        ( 'HE_DTV_W22H_XXXXXXXX',   (17,    2019) ),
        ( 'HE_DTV_W22O_XXXXXXXX',   (33,    2019) ),
    ]

    @pytest.mark.parametrize("model,expected", data_calibration_support_info)
    async def test_calibration_support_info(self, model, expected):
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}
        client.calibration_support_info()

        expected = {
            "lut3d":    expected[0],
            "dovi":     expected[1],
        }

        assert expected == client._calibration_info

