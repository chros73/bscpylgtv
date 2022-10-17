import pytest
from datetime import date
import os
from bscpylgtv import WebOsClient
from bscpylgtv import endpoints as ep
from bscpylgtv import cal_commands as cal
from bscpylgtv.exceptions import PyLGTVCmdException
from bscpylgtv.constants import DV_CONFIG_FILENAME

TEST_DIR_DATA = "data"
TEST_DIR_EXPECTED = "expected"


@pytest.mark.asyncio
class TestWebOsClientCalibration():

    data_check_calibration_support = [
        ( "OLED65C6V",      "lut1d",                "1D LUT Upload",                            False ),
        ( "OLED65C6V",      "lut3d_size",           "3D LUT Upload",                            False ),
        ( "OLED65C6V",      "custom_tone_mapping",  "Custom tone mapping parameters Upload",    False ),
        ( "OLED65C6V",      "itpg",                 "iTPG",                                     False ),
        ( "OLED65C6V",      "dv_config_type",       "Dolby Vision Configuration Upload",        False ),

        ( "OLED65C26LA",    "lut1d",                "1D LUT Upload",                            True ),
        ( "OLED65C26LA",    "lut3d_size",           "3D LUT Upload",                            True ),
        ( "OLED65C26LA",    "custom_tone_mapping",  "Custom tone mapping parameters Upload",    True ),
        ( "OLED65C26LA",    "itpg",                 "iTPG",                                     True ),
        ( "OLED65C26LA",    "dv_config_type",       "Dolby Vision Configuration Upload",        True ),
    ]

    @pytest.mark.parametrize("model,property,message,expected", data_check_calibration_support)
    async def test_check_calibration_support(self, model, property, message, expected):
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected:
            client.check_calibration_support(property, message)
            assert expected == True
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                client.check_calibration_support(property, message)



    data_start_calibration = [
        ( "OLED65C6V",      "expert1",  None,           -1 ),
        ( "OLED65C26LA",    "foo",      None,           0 ),
        ( "OLED65C26LA",    "expert1",  cal.CAL_START,  1 ),
    ]

    @pytest.mark.parametrize("model,picMode,command,expected", data_start_calibration)
    async def test_start_calibration(self, mocker, model, picMode, command, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.start_calibration(picMode)

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
                "picMode":      picMode,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid picture_mode .+$'):
                await client.start_calibration(picMode)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.start_calibration(picMode)



    data_end_calibration = [
        ( "OLED65C6V",      None,           0 ),
        ( "OLED65C26LA",    cal.CAL_END,    1 ),
    ]

    @pytest.mark.parametrize("model,command,expected", data_end_calibration)
    async def test_end_calibration(self, mocker, model, command, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.end_calibration()

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.end_calibration()



    data_set_ui_data_methods = [
        ( "OLED65C6V",      39,     "oled_light",   None,                   None,   -1 ),
        ( "OLED65C26LA",    -1,     "oled_light",   cal.BACKLIGHT_UI_DATA,  None,   0 ),
        ( "OLED65C26LA",    102,    "oled_light",   cal.BACKLIGHT_UI_DATA,  None,   0 ),
        ( "OLED65C26LA",    39,     "oled_light",   cal.BACKLIGHT_UI_DATA,  "JwA=", 1 ),

        ( "OLED65C6V",      39,     "contrast",     None,                   None,   -1 ),
        ( "OLED65C26LA",    -1,     "contrast",     cal.CONTRAST_UI_DATA,   None,   0 ),
        ( "OLED65C26LA",    102,    "contrast",     cal.CONTRAST_UI_DATA,   None,   0 ),
        ( "OLED65C26LA",    39,     "contrast",     cal.CONTRAST_UI_DATA,   "JwA=", 1 ),

        ( "OLED65C6V",      39,     "brightness",   None,                   None,   -1 ),
        ( "OLED65C26LA",    -1,     "brightness",   cal.BRIGHTNESS_UI_DATA, None,   0 ),
        ( "OLED65C26LA",    102,    "brightness",   cal.BRIGHTNESS_UI_DATA, None,   0 ),
        ( "OLED65C26LA",    39,     "brightness",   cal.BRIGHTNESS_UI_DATA, "JwA=", 1 ),

        ( "OLED65C6V",      39,     "color",        None,                   None,   -1 ),
        ( "OLED65C26LA",    -1,     "color",        cal.COLOR_UI_DATA,      None,   0 ),
        ( "OLED65C26LA",    102,    "color",        cal.COLOR_UI_DATA,      None,   0 ),
        ( "OLED65C26LA",    39,     "color",        cal.COLOR_UI_DATA,      "JwA=", 1 ),
    ]

    @pytest.mark.parametrize("model,value,methodName,command,data,expected", data_set_ui_data_methods)
    async def test_set_ui_data_methods(self, mocker, model, value, methodName, command, data, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}
        method = getattr(client, f'set_{methodName}')

        if expected > 0:
            await method(value)

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    1,
                "dataType":     "unsigned integer16",
                "dataOpt":      1,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await method(value)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await method(value)



    data_upload_1d_lut = [
        ( "OLED65C6V",     None,    None,               None,   None,   -1 ),
        ( "OLED65C26LA",   [3],     None,               None,   None,   0 ),
        ( "OLED65C26LA",   [],      "",                 0,      2,      1 ),
        ( "OLED65C26LA",   None,    "1dlut_unity.txt",  3072,   1,      1 ),
    ]

    @pytest.mark.parametrize("model,inputData,dataFile,dataCount,dataOpt,expected", data_upload_1d_lut)
    async def test_upload_1d_lut(self, mocker, model, inputData, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.upload_1d_lut(inputData)
            
            data = dataFile
            if dataFile:
                currentDir = os.path.dirname(os.path.realpath(__file__))
                with open(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile)) as f:
                    data = f.read()

            payload = {
                "command":      cal.UPLOAD_1D_LUT,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned integer16",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(TypeError, match=r'data must be of type ndarray .+$'):
                await client.upload_1d_lut(inputData)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.upload_1d_lut(inputData)



    data_upload_1d_lut_from_file = [
        ( "OLED65C6V",     "1dlut.cal",     None,               None,   None,   -4 ),
        ( "OLED65C26LA",   "1dlut.txt",     None,               None,   None,   -3 ),

        ( "OLED65C26LA",   "1dlut_11.cal",  None,               None,   None,   -2 ),
        ( "OLED65C26LA",   "1dlut_12.cube", None,               None,   None,   -1 ),
        ( "OLED65C26LA",   "1dlut_13.cube", None,               None,   None,   0 ),

        ( "OLED65C26LA",   "1dlut_01.cal",  "1dlut_01.txt",     3072,   1,      1 ),
        ( "OLED65C26LA",   "1dlut_02.cal",  "1dlut_02.txt",     3072,   1,      1 ),
        ( "OLED65C26LA",   "1dlut_03.cube", "1dlut_03.txt",     3072,   1,      1 ),
    ]

    @pytest.mark.parametrize("model,fileName,dataFile,dataCount,dataOpt,expected", data_upload_1d_lut_from_file)
    async def test_upload_1d_lut_from_file(self, mocker, model, fileName, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}
        currentDir = os.path.dirname(os.path.realpath(__file__))

        if expected > 0:
            await client.upload_1d_lut_from_file(os.path.join(currentDir, TEST_DIR_DATA, fileName))
            
            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile)) as f:
                data = f.read()

            payload = {
                "command":      cal.UPLOAD_1D_LUT,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned integer16",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'data should have shape .+$'):
                await client.upload_1d_lut_from_file(os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -1:
            with pytest.raises(ValueError, match=r'Expected shape .+$'):
                await client.upload_1d_lut_from_file(os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -2:
            with pytest.raises(ValueError, match=r'Some errors were detected .+'):
                await client.upload_1d_lut_from_file(os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -3:
            with pytest.raises(ValueError, match=r'Unsupported file format .+$'):
                await client.upload_1d_lut_from_file(fileName)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.upload_1d_lut_from_file(fileName)



    data_upload_3d_lut = [
        ( "OLED65C6V",     None,    None,                       None,                   None,   None,   -2 ),
        ( "OLED65B8SLC",   None,    "foo",                      None,                   None,   None,   -1 ),
        ( "OLED65B8SLC",   [3],     cal.UPLOAD_3D_LUT_BT709,    None,                   None,   None,   0 ),
        ( "OLED65B8SLC",   [],      cal.UPLOAD_3D_LUT_BT2020,   "",                     0,      2,      1 ),
        ( "OLED65B8SLC",   None,    cal.UPLOAD_3D_LUT_BT709,    "3dlut_17pt_unity.txt", 14739,  1,      1 ),
        ( "OLED65C26LA",   None,    cal.UPLOAD_3D_LUT_BT2020,   "3dlut_33pt_unity.txt", 107811, 1,      1 ),
    ]

    @pytest.mark.parametrize("model,inputData,command,dataFile,dataCount,dataOpt,expected", data_upload_3d_lut)
    async def test_upload_3d_lut(self, mocker, model, inputData, command, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.upload_3d_lut(command, inputData)
            
            data = dataFile
            if dataFile:
                currentDir = os.path.dirname(os.path.realpath(__file__))
                with open(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile)) as f:
                    data = f.read()

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned integer16",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(TypeError, match=r'data must be of type ndarray .+$'):
                await client.upload_3d_lut(command, inputData)
        elif expected == -1:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid 3D LUT Upload command .+$'):
                await client.upload_3d_lut(command, inputData)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.upload_3d_lut(command, inputData)



    data_upload_3d_lut_bt709_bt2020 = [
        ( "bt709",  cal.UPLOAD_3D_LUT_BT709 ),
        ( "bt2020", cal.UPLOAD_3D_LUT_BT2020 ),
    ]

    @pytest.mark.parametrize("methodName,command", data_upload_3d_lut_bt709_bt2020)
    async def test_upload_3d_lut_bt709_bt2020(self, mocker, methodName, command):
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut')
        
        data = []
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : "OLED65C26LA"}
        method = getattr(client, f'upload_3d_lut_{methodName}')
        await method(data)

        client.upload_3d_lut.assert_called_once_with(command, data)



    data_upload_3d_lut_from_file = [
        ( "OLED65C6V",     "3dlut.cal",         None,                       None,                   None,   None,   -5 ),
        ( "OLED65B8SLC",   "3dlut.txt",         None,                       None,                   None,   None,   -4 ),

        ( "OLED65B8SLC",   "3dlut_11.cube",     None,                       None,                   None,   None,   -3 ),
        ( "OLED65B8SLC",   "3dlut_12.cube",     None,                       None,                   None,   None,   -2 ),
        ( "OLED65B8SLC",   "3dlut_13.cube",     None,                       None,                   None,   None,   -1 ),
        ( "OLED65B8SLC",   "3dlut_14.cube",     cal.UPLOAD_3D_LUT_BT709,    None,                   None,   None,   0 ),

        ( "OLED65B8SLC",   "3dlut_17pt.cube",   cal.UPLOAD_3D_LUT_BT709,    "3dlut_17pt_01.txt",    14739,  1,      1 ),
        ( "OLED65C26LA",   "3dlut_33pt.cube",   cal.UPLOAD_3D_LUT_BT2020,   "3dlut_33pt_01.txt",    107811, 1,      1 ),
    ]

    @pytest.mark.parametrize("model,fileName,command,dataFile,dataCount,dataOpt,expected", data_upload_3d_lut_from_file)
    async def test_upload_3d_lut_from_file(self, mocker, model, fileName, command, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}
        currentDir = os.path.dirname(os.path.realpath(__file__))

        if expected > 0:
            await client.upload_3d_lut_from_file(command, os.path.join(currentDir, TEST_DIR_DATA, fileName))
            
            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile)) as f:
                data = f.read()

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned integer16",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'data should have shape .+$'):
                await client.upload_3d_lut_from_file(command, os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -1:
            with pytest.raises(ValueError, match=r'Must specify one of .+$'):
                await client.upload_3d_lut_from_file(command, os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -2:
            with pytest.raises(ValueError, match=r'Cannot specify both .+$'):
                await client.upload_3d_lut_from_file(command, os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -3:
            with pytest.raises(ValueError, match=r'Expected shape .+$'):
                await client.upload_3d_lut_from_file(command, os.path.join(currentDir, TEST_DIR_DATA, fileName))
        elif expected == -4:
            with pytest.raises(ValueError, match=r'Unsupported file format .+$'):
                await client.upload_3d_lut_from_file(command, fileName)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.upload_3d_lut_from_file(command, fileName)



    data_upload_3d_lut_bt709_bt2020_from_file = [
        ( "bt709",  cal.UPLOAD_3D_LUT_BT709 ),
        ( "bt2020", cal.UPLOAD_3D_LUT_BT2020 ),
    ]

    @pytest.mark.parametrize("methodName,command", data_upload_3d_lut_bt709_bt2020_from_file)
    async def test_upload_3d_lut_bt709_bt2020_from_file(self, mocker, methodName, command):
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_from_file')
        
        fileName = f'3dlut_33pt_{methodName}.cube'
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : "OLED65C26LA"}
        method = getattr(client, f'upload_3d_lut_{methodName}_from_file')
        await method(fileName)

        client.upload_3d_lut_from_file.assert_called_once_with(command, fileName)



    data_set_1d_2_2_1d_0_45_en = [
        ( "OLED65C6V",      0,  "1d_en_2_2",    None,                           None,   None,   None,   -1 ),
        ( "OLED65C26LA",    -1, "1d_en_2_2",    None,                           None,   None,   None,   0 ),
        ( "OLED65C26LA",    2,  "1d_en_2_2",    None,                           None,   None,   None,   0 ),
        ( "OLED65C26LA",    [], "1d_en_2_2",    cal.ENABLE_GAMMA_2_2_TRANSFORM, "",     0,      2,      1 ),
        ( "OLED65C26LA",    0,  "1d_en_2_2",    cal.ENABLE_GAMMA_2_2_TRANSFORM, "AAA=", 1,      1,      1 ),
        ( "OLED65C26LA",    1,  "1d_en_2_2",    cal.ENABLE_GAMMA_2_2_TRANSFORM, "AQA=", 1,      1,      1 ),

        ( "OLED65C6V",      0,  "1d_en_0_45",   None,                           None,   None,   None,   -1 ),
        ( "OLED65C26LA",    -1, "1d_en_0_45",   None,                           None,   None,   None,   0 ),
        ( "OLED65C26LA",    2,  "1d_en_0_45",   None,                           None,   None,   None,   0 ),
        ( "OLED65C26LA",    [], "1d_en_0_45",   cal.ENABLE_GAMMA_0_45_TRANSFORM,"",     0,      2,      1 ),
        ( "OLED65C26LA",    0,  "1d_en_0_45",   cal.ENABLE_GAMMA_0_45_TRANSFORM,"AAA=", 1,      1,      1 ),
        ( "OLED65C26LA",    1,  "1d_en_0_45",   cal.ENABLE_GAMMA_0_45_TRANSFORM,"AQA=", 1,      1,      1 ),
    ]

    @pytest.mark.parametrize("model,value,methodName,command,data,dataCount,dataOpt,expected", data_set_1d_2_2_1d_0_45_en)
    async def test_set_1d_2_2_1d_0_45_en(self, mocker, model, value, methodName, command, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}
        method = getattr(client, f'set_{methodName}')

        if expected > 0:
            await method(value)

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned integer16",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await method(value)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await method(value)



    data_set_bt709_bt2020_3by3_gamut_data = [
        ( "OLED65C6V",      0,                                      "3by3_gamut_data_bt709",    None,   None,   None,   None,   -3 ),

        ( "OLED65C26LA",    "",                                     "3by3_gamut_data_bt709",    None,   None,   None,   None,   -2 ),

        ( "OLED65C26LA",    [3],                                    "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
        ( "OLED65C26LA",    [[1, 0, 1]],                            "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
        ( "OLED65C26LA",    [[1, 0, 1], [0, 1, 0]],                 "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
        ( "OLED65C26LA",    [[1, 0], [0, 1], [0, 0]],               "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),

        ( "OLED65C26LA",    [[1, 2, 0], [0, 1, 0], [0, 0, 1]],      "3by3_gamut_data_bt709",    None,   None,   None,   None,   0 ),
        ( "OLED65C26LA",    [[1, 0, 0], [0, 1, -1], [0, 0, 1]],     "3by3_gamut_data_bt709",    None,   None,   None,   None,   0 ),
        ( "OLED65C26LA",    [[1, 0, 0], [0, 1, 0], [0, 0, 1.1]],    "3by3_gamut_data_bt709",    None,   None,   None,   None,   0 ),

        ( "OLED65C26LA",    [], "3by3_gamut_data_bt709",    cal.BT709_3BY3_GAMUT_DATA,  "",     0,      2,      1 ),
        ( "OLED65C26LA",    0,  "3by3_gamut_data_bt709",    cal.BT709_3BY3_GAMUT_DATA,  "AACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAAAAAAAAAAAAAIA/", 9,      1,      1 ),
        ( "OLED65C26LA",    [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]],    "3by3_gamut_data_bt709",    cal.BT709_3BY3_GAMUT_DATA,  "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", 9,  1,  1 ),

        ( "OLED65C6V",      0,                                      "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -3 ),

        ( "OLED65C26LA",    "",                                     "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -2 ),

        ( "OLED65C26LA",    [3],                                    "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
        ( "OLED65C26LA",    [[1, 0, 1]],                            "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
        ( "OLED65C26LA",    [[1, 0, 1], [0, 1, 0]],                 "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
        ( "OLED65C26LA",    [[1, 0], [0, 1], [0, 0]],               "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),

        ( "OLED65C26LA",    [[1, 2, 0], [0, 1, 0], [0, 0, 1]],      "3by3_gamut_data_bt2020",   None,   None,   None,   None,   0 ),
        ( "OLED65C26LA",    [[1, 0, 0], [0, 1, -1], [0, 0, 1]],     "3by3_gamut_data_bt2020",   None,   None,   None,   None,   0 ),
        ( "OLED65C26LA",    [[1, 0, 0], [0, 1, 0], [0, 0, 1.1]],    "3by3_gamut_data_bt2020",   None,   None,   None,   None,   0 ),

        ( "OLED65C26LA",    [], "3by3_gamut_data_bt2020",   cal.BT2020_3BY3_GAMUT_DATA, "",     0,      2,      1 ),
        ( "OLED65C26LA",    0,  "3by3_gamut_data_bt2020",   cal.BT2020_3BY3_GAMUT_DATA, "AACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAAAAAAAAAAAAAIA/", 9,      1,      1 ),
        ( "OLED65C26LA",    [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]],    "3by3_gamut_data_bt2020",    cal.BT2020_3BY3_GAMUT_DATA,  "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", 9,  1,  1 ),
    ]

    @pytest.mark.parametrize("model,value,methodName,command,data,dataCount,dataOpt,expected", data_set_bt709_bt2020_3by3_gamut_data)
    async def test_set_bt709_bt2020_3by3_gamut_data(self, mocker, model, value, methodName, command, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}
        method = getattr(client, f'set_{methodName}')

        if expected > 0:
            if value == 0:
                await method()
            else:
                await method(value)

            payload = {
                "command":      command,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "float",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'values in data must be between .+$'):
                await method(value)
        elif expected == -1:
            with pytest.raises(ValueError, match=r'data should have shape .+$'):
                await method(value)
        elif expected == -2:
            with pytest.raises(ValueError, match=r'could not convert .+$'):
                await method(value)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await method(value)



    data_set_bypass_modes = [
        ( False ),
        ( True  ),
    ]

    @pytest.mark.parametrize("unity1dLut", data_set_bypass_modes)
    async def test_set_bypass_modes(self, mocker, unity1dLut):
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_2_2')
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_0_45')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt709')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt709')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt2020')
        if unity1dLut:
            mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : "OLED65C26LA"}
        result = await client.set_bypass_modes(unity1dLut)

        client.set_1d_en_2_2.assert_called_once_with()
        client.set_1d_en_0_45.assert_called_once_with()
        client.set_3by3_gamut_data_bt709.assert_called_once_with()
        client.set_3by3_gamut_data_bt2020.assert_called_once_with()
        client.upload_3d_lut_bt709.assert_called_once_with()
        client.upload_3d_lut_bt2020.assert_called_once_with()
        if unity1dLut:
            client.upload_1d_lut.assert_called_once_with()
        assert result == True



    data_set_factory_calibration_data = [
        ( False ),
        ( True  ),
    ]

    @pytest.mark.parametrize("hdr10TonemapParams", data_set_factory_calibration_data)
    async def test_set_factory_calibration_data(self, mocker, hdr10TonemapParams):
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_2_2')
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_0_45')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt709')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt709')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        if hdr10TonemapParams:
            mocker.patch('bscpylgtv.WebOsClient.set_tonemap_params')
        
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : "OLED65C26LA"}
        result = await client.set_factory_calibration_data(hdr10TonemapParams)

        client.set_1d_en_2_2.assert_called_once_with([])
        client.set_1d_en_0_45.assert_called_once_with([])
        client.set_3by3_gamut_data_bt709.assert_called_once_with([])
        client.set_3by3_gamut_data_bt2020.assert_called_once_with([])
        client.upload_3d_lut_bt709.assert_called_once_with([])
        client.upload_3d_lut_bt2020.assert_called_once_with([])
        client.upload_1d_lut.assert_called_once_with([])
        if hdr10TonemapParams:
            client.set_tonemap_params.assert_called_once_with("hdr_cinema", [])
        assert result == True



    data_set_tonemap_params = [
        ( "OLED65C6V",      "hdr_cinema",   810,    1000,   75, None,                   None,   None,   -2 ),

        ( "OLED65C26LA",    "foo",          810,    1000,   75, None,                   None,   None,   -1 ),
        ( "OLED65C26LA",    "expert1",      810,    1000,   75, None,                   None,   None,   -1 ),

        ( "OLED65C26LA",    "hdr_cinema",   99,     1000,   75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "OLED65C26LA",    "hdr_game",     4001,   1000,   75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "OLED65C26LA",    "hdr_cinema",   810,    99,     75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "OLED65C26LA",    "hdr_cinema",   810,    10001,  75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "OLED65C26LA",    "hdr_cinema",   810,    1000,   -1, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "OLED65C26LA",    "hdr_cinema",   810,    1000,   101,"KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),

        ( "OLED65C26LA",    "hdr_cinema",   [],     1000,   75, "",                     0,      2,      1 ),
        ( "OLED65C26LA",    "hdr_game",     810,    1000,   75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      1 ),
    ]

    @pytest.mark.parametrize("model,picMode,luminance,mp,rp,data,dataCount,dataOpt,expected", data_set_tonemap_params)
    async def test_set_tonemap_params(self, mocker, model, picMode, luminance, mp, rp, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.set_tonemap_params(picMode, luminance, mp, rp)

            payload = {
                "command":      cal.SET_TONEMAP_PARAM,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned integer16",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.set_tonemap_params(picMode, luminance, mp, rp)
        elif expected == -1:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid picture_mode .+$'):
                await client.set_tonemap_params(picMode, luminance, mp, rp)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.set_tonemap_params(picMode, luminance, mp, rp)



    data_set_dolby_vision_config_data = [
        ( "OLED65C6V",      "dolby_game",   620, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  -1 ),

        ( "OLED65C8PLA",    "foo",          620, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "expert1",      620, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   50,  0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   4001,0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   620, -1,     2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   620, 1,      2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   620, 0.0001, -1,  [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   620, 0.0001, 10,  [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   620, 0.0001, 2.2, [-0.0001, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "OLED65C8PLA",    "dolby_game",   620, 0.0001, 2.2, [0.6796, 1.0001, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),

        ( "OLED65C8PLA",    "dolby_game",   [],   None,   None,   None,   "", 0,  2,  1 ),
        ( "OLED65C8PLA",    "dolby_cinema_dark",    710, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], "UGljdHVyZU1vZGUgPSAyDQpUbWF4ID0gNzEwLjAwMDANClRtaW4gPSAwLjAwMDENClRnYW1tYSA9IDIuMg0KQ29sb3JQcmltYXJpZXMgPSAwLjY3OTYgMC4zMTg3IDAuMjU5NSAwLjY4NDkgMC4xNDQ4IDAuMDQ5NCAwLjMxMjcgMC4zMjkwDQpUTE1TMlJHQm1hdCA9IDQuMTgyNzgzOTgzMjk0NTEgLTMuMzAwNDkyOTUxMDE5NDEgMC4xMTc3NDk4NzA5NTUzMjUgLTAuODgyNDY3MTQwNzYyNzUwIDIuMDE3MzQ1NDgyODExODMgLTAuMTM0ODY1ODY5Nzg0NTI3IDAuMDQzNzgyNzQ3MzA0ODQzMSAtMC4xMDc2NzAyODY3NTcwMjUgMS4wNjM5MTU1MTA2MDc1MA0K",  315,    1,  1 ),
        ( "OLED65C26LA",    "dolby_game",   [],   None,   None,   None,   "", 0,  2,  1 ),
        ( "OLED65C26LA",    "dolby_game",   820, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], "W1BpY3R1cmVNb2RlID0gNF0NClRtYXggPSA4MjAuMDAwMA0KVG1pbiA9IDAuMDAwMQ0KVGdhbW1hID0gMi4yDQpUUHJpbWFyaWVzID0gMC42Nzk2IDAuMzE4NyAwLjI1OTUgMC42ODQ5IDAuMTQ0OCAwLjA0OTQgMC4zMTI3IDAuMzI5MA0K",  135,    1,  1 ),
    ]

    @pytest.mark.parametrize("model,picMode,whiteL,blackL,gamma,primaries,data,dataCount,dataOpt,expected", data_set_dolby_vision_config_data)
    async def test_set_dolby_vision_config_data(self, mocker, model, picMode, whiteL, blackL, gamma, primaries, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.set_dolby_vision_config_data(picMode, whiteL, blackL, gamma, primaries)

            payload = {
                "command":      cal.DOLBY_CFG_DATA,
                "profileNo":    0,
                "programID":    1,
                "data":         data,
                "dataCount":    dataCount,
                "dataType":     "unsigned char",
                "dataOpt":      dataOpt,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.set_dolby_vision_config_data(picMode, whiteL, blackL, gamma, primaries)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.set_dolby_vision_config_data(picMode, whiteL, blackL, gamma, primaries)



    data_write_dolby_vision_config_file = [
        ( "OLED65C6V",      [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   -3 ),

        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,    None, None, -2 ),

        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   "false",    "", None,   -1 ),

        ( "OLED65C8PLA",    [{"picture_mode": "foo", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   0 ),
        ( "OLED65C26LA",    [{"picture_mode": "dolby_cinema_bright", "white_level": 710, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   0 ),
        ( "OLED65C8PLA",    [{"white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False, "", None,   0 ),
        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_dark", "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   0 ),
        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750}],   False, "", None,   0 ),
        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448]}],   False,  "", None,   0 ),
        ( "OLED65C8PLA",    [{}], False,  "", None, 0 ),
        ( "OLED65C8PLA",    [],   False,  "", None, 0 ),
        ( "OLED65C8PLA",    None, False,  "", None, 0 ),

        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", "dv_cfg_2018_01.txt",   1 ),
        ( "OLED65C8PLA",    [{"white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   True,  "", "dv_cfg_2018_02.txt",   1 ),
        ( "OLED65C8PLA",    [{"picture_mode": "dolby_cinema_bright", "white_level": 710, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", "dv_cfg_2018_03.txt",   1 ),
        ( "OLED65C26LA",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", "dv_cfg_2019_01.txt",   1 ),
        ( "OLED65C26LA",    [{"white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   True,  "", "dv_cfg_2019_02.txt",   1 ),
        ( "OLED65C26LA",    [{"picture_mode": "dolby_cinema_bright", "white_level": 710, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "d:\temp",    "dv_cfg_2019_03.txt",   1 ),
    ]

    @pytest.mark.parametrize("model,data,allModes,path,cfgFile,expected", data_write_dolby_vision_config_file)
    async def test_write_dolby_vision_config_file(self, mocker, model, data, allModes, path, cfgFile, expected):
        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            currentDir = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, cfgFile)) as f:
                expectedData = f.read().replace("2022-10-13", date.today().isoformat())

            mockedOpen = mocker.patch("builtins.open", mocker.mock_open())
            result = await client.write_dolby_vision_config_file(data, allModes, path)

            assert result == True
            mockedOpen.assert_called_once_with(os.path.join(path, DV_CONFIG_FILENAME), "w", newline='\r\n')
            mockedOpen.return_value.write.assert_called_once_with(expectedData)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.write_dolby_vision_config_file(data, allModes, path)
        elif expected == -1:
            with pytest.raises(TypeError, match=r'^.+ should be a bool, .+$'):
                await client.write_dolby_vision_config_file(data, allModes, path)
        elif expected == -2:
            with pytest.raises(TypeError, match=r'^.+ should be a str, .+$'):
                await client.write_dolby_vision_config_file(data, allModes, path)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.write_dolby_vision_config_file(data, allModes, path)



    data_set_itpg_patch_window = [
        ( "OLED65C6V",      71, 81,     98, 1,  858,    482,    1491,   839,    -1 ),

        ( "OLED65C26LA",    -1, 81,     98, 0,  858,    482,    1491,   839,    0 ),
        ( "OLED65C26LA",    71, 1024,   98, 0,  858,    482,    1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, -1, 858,    482,    1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 10, 858,    482,    1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  99,     482,    1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    7681,   1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    55,     1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    4321,   1491,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    482,    -1,     839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    482,    7580,   839,    0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    482,    1491,   -1,     0 ),
        ( "OLED65C26LA",    71, 81,     98, 0,  858,    482,    1491,   4264,   0 ),

        ( "OLED65C26LA",    71, 81,     98, 0,  858,    482,    1491,   839,    1 ),
        ( "OLED65C26LA",    71, 81,     98, 1,  858,    482,    1491,   839,    1 ),
    ]

    @pytest.mark.parametrize("model,r,g,b,winId,w,h,sx,sy,expected", data_set_itpg_patch_window)
    async def test_set_itpg_patch_window(self, mocker, model, r, g, b, winId, w, h, sx, sy, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.set_itpg_patch_window(r, g, b, winId, w, h, sx, sy)

            payload = {
                "command":      cal.PATTERN_WINDOW,
                "fillR":        r,
                "fillG":        g,
                "fillB":        b,
                "winId":        winId,
                "width":        858,
                "height":       482,
                "startX":       1491,
                "startY":       839,
                "programID":    1,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.set_itpg_patch_window(r, g, b, winId, w, h, sx, sy)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.set_itpg_patch_window(r, g, b, winId, w, h, sx, sy)



    data_set_itpg_gradation_window = [
        ( "OLED65C6V",      0,  3,      610,    520,    230,    1,  1,      1,  -1 ),

        ( "OLED65C26LA",    -1, 3,      610,    520,    230,    1,  1,      1,  0 ),
        ( "OLED65C26LA",    4,  3,      610,    520,    230,    1,  1,      1,  0 ),
        ( "OLED65C26LA",    0,  -1,     610,    520,    230,    1,  1,      1,  0 ),
        ( "OLED65C26LA",    0,  7681,   610,    520,    230,    1,  1,      1,  0 ),
        ( "OLED65C26LA",    0,  3,      -1,     520,    230,    1,  1,      1,  0 ),
        ( "OLED65C26LA",    0,  3,      610,    1024,   230,    1,  1,      1,  0 ),
        ( "OLED65C26LA",    0,  3,      610,    520,    230,    -1, 1,      1,  0 ),
        ( "OLED65C26LA",    0,  3,      610,    520,    230,    1,  513,    1,  0 ),

        ( "OLED65C26LA",    0,  3,      610,    520,    230,    1,  1,      1,  1 ),
        ( "OLED65C26LA",    1,  3,      610,    50,     23,     1,  1,      1,  1 ),
    ]

    @pytest.mark.parametrize("model,id,ss,ar,ag,ab,er,eg,eb,expected", data_set_itpg_gradation_window)
    async def test_set_itpg_gradation_window(self, mocker, model, id, ss, ar, ag, ab, er, eg, eb, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected > 0:
            await client.set_itpg_gradation_window(id, ss, ar, ag, ab, er, eg, eb)

            payload = {
                "command":      cal.PATTERN_GRADATION,
                "barId":        id,
                "strideSize":   ss,
                "startR":       ar,
                "startG":       ag,
                "startB":       ab,
                "stepR":        er,
                "stepG":        eg,
                "stepB":        eb,
                "programID":    1,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.set_itpg_gradation_window(id, ss, ar, ag, ab, er, eg, eb)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.set_itpg_gradation_window(id, ss, ar, ag, ab, er, eg, eb)



    data_toggle_itpg = [
        ( "OLED65C6V",      True,   2,  0,  True,  (True,       -2) ),

        ( "OLED65C9PLA",    None,   2,  0,  False, (True,       -1) ),
        ( "OLED65C9PLA",    True,   2,  0,  None,  (True,       -1) ),
        ( "OLED65C9PLA",    True,   -1, 0,  False, (True,       0) ),
        ( "OLED65C9PLA",    True,   11, 0,  False, (True,       0) ),
        ( "OLED65C9PLA",    True,   2,  -1, False, (True,       0) ),
        ( "OLED65C9PLA",    True,   2,  3,  False, (True,       0) ),

        ( "OLED65C9PLA",    True,   2,  0,  False, (True,       1) ),
        ( "OLED65C9PLA",    True,   2,  1,  False, (True,       1) ),
        ( "OLED65C9PLA",    False,  0,  0,  False, (False,      1) ),
        ( "OLED65C26LA",    True,   2,  0,  True,  ("true",     1) ),
        ( "OLED65C26LA",    True,   2,  1,  True,  ("true",     1) ),
        ( "OLED65C26LA",    False,  0,  0,  True,  ("false",    1) ),
    ]

    @pytest.mark.parametrize("model,enable,numOfBox,ptnType,fixEnable,expected", data_toggle_itpg)
    async def test_toggle_itpg(self, mocker, model, enable, numOfBox, ptnType, fixEnable, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["system_info"], client_key="x")
        client._system_info = {"modelName" : model}

        if expected[1] > 0:
            await client.toggle_itpg(enable, numOfBox, ptnType, fixEnable)

            payload = {
                "command":      cal.PATTERN_CONTROL,
                "enable":       expected[0],
                "numOfBox":     numOfBox,
                "ptnType":      ptnType,
                "programID":    1,
            }

            client.request.assert_called_once_with(ep.CALIBRATION, payload)
        elif expected[1] == 0:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.toggle_itpg(enable, numOfBox, ptnType, fixEnable)
        elif expected[1] == -1:
            with pytest.raises(TypeError, match=r'^.+ should be a bool, .+$'):
                await client.toggle_itpg(enable, numOfBox, ptnType, fixEnable)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by tv model .+$'):
                await client.toggle_itpg(enable, numOfBox, ptnType, fixEnable)

