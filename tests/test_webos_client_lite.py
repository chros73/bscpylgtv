import pytest
from bscpylgtv import WebOsClient


@pytest.mark.asyncio
class TestWebOsClientLite():

    data_calibration_support_info = [
        ( '55EF950V',       (False, None,   False,  False,  None) ),
        ( '55EA880V',       (False, None,   False,  False,  None) ),
        ( '55EA970V',       (False, None,   False,  False,  None) ),
        ( '55EA980W',       (False, None,   False,  False,  None) ),

        ( '55EC930V',       (False, None,   False,  False,  None) ),
        ( '65EC970V',       (False, None,   False,  False,  None) ),
        ( '77EC980V',       (False, None,   False,  False,  None) ),

        ( '55EG910V',       (False, None,   False,  False,  None) ),
        ( '55EG920V',       (False, None,   False,  False,  None) ),
        ( '65EF950V',       (False, None,   False,  False,  None) ),
        ( '65EG960V',       (False, None,   False,  False,  None) ),
        ( '65EF9800',       (False, None,   False,  False,  None) ),
        ( '77EG990V',       (False, None,   False,  False,  None) ),

        ( 'OLED65B6V',      (False, None,   False,  False,  None) ),
        ( 'OLED65C6V',      (False, None,   False,  False,  None) ),
        ( 'OLED65E6V',      (False, None,   False,  False,  None) ),
        ( 'OLED65G6V',      (False, None,   False,  False,  None) ),

        ( 'OLED65B7V',      (False, None,   False,  False,  None) ),
        ( 'OLED65C7V',      (False, None,   False,  False,  None) ),
        ( 'OLED65E7V',      (False, None,   False,  False,  None) ),
        ( 'OLED65G7V',      (False, None,   False,  False,  None) ),
        ( 'OLED65W7V',      (False, None,   False,  False,  None) ),

        ( 'OLED65B8SLC',    (True,  17,     False,  False,  2018) ),
        ( 'OLED65C8PLA',    (True,  33,     False,  False,  2018) ),
        ( 'OLED65E8PLA',    (True,  33,     False,  False,  2018) ),
        ( 'OLED65G8PLA',    (True,  33,     False,  False,  2018) ),
        ( 'OLED65W8PLA',    (True,  33,     False,  False,  2018) ),

        ( 'OLED65B9PLA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65C9PLA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65E9PLA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65W9PLA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED88Z9PLA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65BX6LB',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65CX6LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65GX6LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65WX9LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED88ZX9LA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65A16LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65B16LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65C15LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65G15LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED77Z19LA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65A26LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65B26LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED55CS6LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65C26LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED65G26LA',    (True,  33,     True,   True,   2019) ),
        ( 'OLED77Z29LA',    (True,  33,     True,   True,   2019) ),

        ( '42LX3QPUA',      (True,  33,     True,   True,   2019) ),
        ( '55LX1Q6LA',      (True,  33,     True,   True,   2019) ),
        ( '65ART90E6QA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65A36LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65B36LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65C36LA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65A46LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65B46LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65C46LA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65A56LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65B56LA',    (True,  17,     True,   True,   2019) ),
        ( 'OLED65C56LA',    (True,  33,     True,   True,   2019) ),

        ( 'OLED65A66LA',    (False, None,   False,  False,  None) ),
        ( 'OLED65B66LA',    (False, None,   False,  False,  None) ),
        ( 'OLED65C66LA',    (False, None,   False,  False,  None) ),

        ( '55SK8100PLA',    (True,  17,     False,  False,  2018) ),
        ( '65SK9500PUA',    (True,  17,     False,  False,  2018) ),

        ( '55SM8050PLC',    (True,  17,     True,   True,   2019) ),
        ( '65SM9800PLA',    (True,  17,     True,   True,   2019) ),
        ( '75SM9900PLA',    (True,  33,     True,   True,   2019) ),
    ]

    @pytest.mark.parametrize("modelName,expected", data_calibration_support_info)
    async def test_calibration_support_info(self, modelName, expected):
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : modelName}
        client.calibration_support_info()

        expected = {
            "lut1d":                expected[0],
            "lut3d_size":           expected[1],
            "custom_tone_mapping":  expected[2],
            "itpg":                 expected[3],
            "dv_config_type":       expected[4],
        }

        assert expected == client._calibration_info

