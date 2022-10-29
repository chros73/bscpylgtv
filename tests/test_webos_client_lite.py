import pytest
from bscpylgtv import WebOsClient


@pytest.mark.asyncio
class TestWebOsClientLite():

    data_calibration_support_info = [
        ( '55EF950V',       (None,   None) ),
        ( '55EA880V',       (None,   None) ),
        ( '55EA970V',       (None,   None) ),
        ( '55EA980W',       (None,   None) ),
                                     
        ( '55EC930V',       (None,   None) ),
        ( '65EC970V',       (None,   None) ),
        ( '77EC980V',       (None,   None) ),
                                     
        ( '55EG910V',       (None,   None) ),
        ( '55EG920V',       (None,   None) ),
        ( '65EF950V',       (None,   None) ),
        ( '65EG960V',       (None,   None) ),
        ( '65EF9800',       (None,   None) ),
        ( '77EG990V',       (None,   None) ),
                                     
        ( 'OLED65B6V',      (None,   None) ),
        ( 'OLED65C6V',      (None,   None) ),
        ( 'OLED65E6V',      (None,   None) ),
        ( 'OLED65G6V',      (None,   None) ),
                                     
        ( 'OLED65B7V',      (None,   None) ),
        ( 'OLED65C7V',      (None,   None) ),
        ( 'OLED65E7V',      (None,   None) ),
        ( 'OLED65G7V',      (None,   None) ),
        ( 'OLED65W7V',      (None,   None) ),
                                     
        ( 'OLED65B8SLC',    (17,     2018) ),
        ( 'OLED65C8PLA',    (33,     2018) ),
        ( 'OLED65E8PLA',    (33,     2018) ),
        ( 'OLED65G8PLA',    (33,     2018) ),
        ( 'OLED65W8PLA',    (33,     2018) ),
                                     
        ( 'OLED65B9PLA',    (17,     2019) ),
        ( 'OLED65C9PLA',    (33,     2019) ),
        ( 'OLED65E9PLA',    (33,     2019) ),
        ( 'OLED65W9PLA',    (33,     2019) ),
        ( 'OLED88Z9PLA',    (33,     2019) ),
                                     
        ( 'OLED65BX6LB',    (17,     2019) ),
        ( 'OLED65CX6LA',    (33,     2019) ),
        ( 'OLED65GX6LA',    (33,     2019) ),
        ( 'OLED65WX9LA',    (33,     2019) ),
        ( 'OLED88ZX9LA',    (33,     2019) ),
                                     
        ( 'OLED65A16LA',    (17,     2019) ),
        ( 'OLED65B16LA',    (17,     2019) ),
        ( 'OLED65C15LA',    (33,     2019) ),
        ( 'OLED65G15LA',    (33,     2019) ),
        ( 'OLED77Z19LA',    (33,     2019) ),
                                     
        ( 'OLED65A26LA',    (17,     2019) ),
        ( 'OLED65B26LA',    (17,     2019) ),
        ( 'OLED55CS6LA',    (33,     2019) ),
        ( 'OLED65C26LA',    (33,     2019) ),
        ( 'OLED65G26LA',    (33,     2019) ),
        ( 'OLED77Z29LA',    (33,     2019) ),
                                     
        ( '42LX3QPUA',      (33,     2019) ),
        ( '55LX1Q6LA',      (33,     2019) ),
        ( '65ART90E6QA',    (33,     2019) ),
                                     
        ( 'OLED65A36LA',    (17,     2019) ),
        ( 'OLED65B36LA',    (17,     2019) ),
        ( 'OLED65C36LA',    (33,     2019) ),
                                     
        ( 'OLED65A46LA',    (17,     2019) ),
        ( 'OLED65B46LA',    (17,     2019) ),
        ( 'OLED65C46LA',    (33,     2019) ),
                                     
        ( 'OLED65A56LA',    (17,     2019) ),
        ( 'OLED65B56LA',    (17,     2019) ),
        ( 'OLED65C56LA',    (33,     2019) ),
                                     
        ( 'OLED65A66LA',    (None,   None) ),
        ( 'OLED65B66LA',    (None,   None) ),
        ( 'OLED65C66LA',    (None,   None) ),
                                     
        ( '55SK8100PLA',    (17,     2018) ),
        ( '65SK9500PUA',    (17,     2018) ),
                                     
        ( '55SM8050PLC',    (17,     2019) ),
        ( '65SM9800PLA',    (17,     2019) ),
        ( '75SM9900PLA',    (33,     2019) ),
    ]

    @pytest.mark.parametrize("modelName,expected", data_calibration_support_info)
    async def test_calibration_support_info(self, modelName, expected):
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : modelName}
        client.calibration_support_info()

        expected = {
            "lut3d_size":       expected[0],
            "dv_config_type":   expected[1],
        }

        assert expected == client._calibration_info

