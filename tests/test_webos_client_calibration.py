import pytest
from datetime import date
import os
import numpy as np
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
        ( "HE_DTV_W17H",    "lut3d",    "3D LUT Upload",                        False ),
        ( "HE_DTV_W17H",    "dovi",     "Dolby Vision Configuration Upload",    False ),

        ( "HE_DTV_W22O",    "lut3d",    "3D LUT Upload",                        True ),
        ( "HE_DTV_W22O",    "dovi",     "Dolby Vision Configuration Upload",    True ),
    ]

    @pytest.mark.parametrize("model,property,message,expected", data_check_calibration_support)
    async def test_check_calibration_support(self, model, property, message, expected):
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}
        
        if expected:
            client.check_calibration_support(property, message)
            assert expected == True
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                client.check_calibration_support(property, message)



    data_get_1d_en_2_2_0_45 = [
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"datax": "AAA=", "dataCount": 1, "dataType": "unsigned integer16"},  -2 ),
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"data": "AAA=", "dataCountx": 1, "dataType": "unsigned integer16"},  -2 ),
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"data": "AAA=", "dataCount": 1, "dataTypex": "unsigned integer16"},   -2 ),
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"data": "AAA=", "dataCount": 1, "dataType": "unsigned integer"},   -2 ),
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"data": "AAA=", "dataCount": 2, "dataType": "unsigned integer16"},   -1 ),
          
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"data": "AAA=", "dataCount": 1, "dataType": "unsigned integer16"},   0 ),
        ( "1d_en_2_2",    cal.GET_GAMMA_2_2_TRANSFORM,    {"data": "AQA=", "dataCount": 1, "dataType": "unsigned integer16"},   1 ),
          
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"datax": "AAA=", "dataCount": 1, "dataType": "unsigned integer16"},  -2 ),
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"data": "AAA=", "dataCountx": 1, "dataType": "unsigned integer16"},  -2 ),
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"data": "AAA=", "dataCount": 1, "dataTypex": "unsigned integer16"},   -2 ),
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"data": "AAA=", "dataCount": 1, "dataType": "unsigned integer"},   -2 ),
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"data": "AAA=", "dataCount": 2, "dataType": "unsigned integer16"},   -1 ),
          
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"data": "AAA=", "dataCount": 1, "dataType": "unsigned integer16"},   0 ),
        ( "1d_en_0_45",   cal.GET_GAMMA_0_45_TRANSFORM,   {"data": "AQA=", "dataCount": 1, "dataType": "unsigned integer16"},   1 ),
    ]

    @pytest.mark.parametrize("methodName,command,data,expected", data_get_1d_en_2_2_0_45)
    async def test_get_1d_en_2_2_0_45(self, mocker, methodName, command, data, expected):
        mocker.patch('bscpylgtv.WebOsClient.request', return_value=data)

        client = await WebOsClient.create("x", states=[], client_key="x")
        method = getattr(client, f'get_{methodName}')

        if expected >= 0:
            res = await method()

            assert expected == res
            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
        elif expected == -1:
            with pytest.raises(ValueError, match=r'data should have size .+$'):
                await method()
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid .+$'):
                await method()



    data_get_3by3_gamut_data = [
        ( "",   "foo.bar",      cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 9, "dataType": "float"},   None, -2 ),
        ( "",   "",             cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataTypex": "foo"},   None, -1 ),
        ( "",   "",             cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataTypex": "float"},   None, -1 ),
        ( "",   "",             cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCountx": 7, "dataType": "float"},   None, -1 ),
        ( "",   "",             cal.GET_3BY3_GAMUT_DATA,    {"datax": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataType": "float"},   None, -1 ),
        ( "",   "",             cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataType": "float"},   None, 0 ),

        ( "",   "",             cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 9, "dataType": "float"},   [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]], 1 ),
        ( "",   "test.matrix",  cal.GET_3BY3_GAMUT_DATA,    {"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 9, "dataType": "float"},   "3by3.matrix", 2 ),

        ( "_hdr",   "foo.bar",  cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 9, "dataType": "float"},   None, -2 ),
        ( "_hdr",   "",         cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataTypex": "foo"},   None, -1 ),
        ( "_hdr",   "",         cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataTypex": "float"},   None, -1 ),
        ( "_hdr",   "",         cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCountx": 7, "dataType": "float"},   None, -1 ),
        ( "_hdr",   "",         cal.GET_HDR_3BY3_GAMUT_DATA,{"datax": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataType": "float"},   None, -1 ),
        ( "_hdr",   "",         cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 7, "dataType": "float"},   None, 0 ),

        ( "_hdr",   "",         cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 9, "dataType": "float"},   [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]], 1 ),
        ( "_hdr",   "test.matrix",  cal.GET_HDR_3BY3_GAMUT_DATA,{"data": "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", "dataCount": 9, "dataType": "float"},  "3by3.matrix", 2 ),
    ]

    @pytest.mark.parametrize("methodName,backupFile,command,data,result,expected", data_get_3by3_gamut_data)
    async def test_get_3by3_gamut_data(self, tmp_path, mocker, methodName, backupFile, command, data, result, expected):
        mocker.patch('bscpylgtv.WebOsClient.request', return_value=data)

        client = await WebOsClient.create("x", states=[], client_key="x")
        method = getattr(client, f'get_3by3_gamut_data{methodName}')

        if expected > 1:
            backupFileObj = tmp_path / backupFile
            res = await method(str(backupFileObj))

            currentDir = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, result)) as f:
                result = f.read()

            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
            assert backupFileObj.read_text() == result
        elif expected == 1:
            res = await method(backupFile)
            result = np.array(result, np.float32)

            assert np.array_equal(result, res)
            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
        elif expected == 0:
            with pytest.raises(ValueError, match=r'data should have size .+$'):
                await method(backupFile)
        elif expected == -1:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid .+$'):
                await method(backupFile)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid Get Calibration file extension, .+$'):
                await method(backupFile)



    data_get_1d_lut = [
        ( "foo.bar",    cal.GET_1D_LUT, "1dlut_00.txt", 3072,   "unsigned integer16",   "1dlut_00.cube",    -2 ),
        ( "",           cal.GET_1D_LUT, "1dlut_00.txt", 3072,   "foo",                  "1dlut_00.cube",    -1 ),
        ( "",           cal.GET_1D_LUT, "1dlut_00.txt", 3073,   "unsigned integer16",   None,               0 ),

        ( "",           cal.GET_1D_LUT, "1dlut_00.txt", 3072,   "unsigned integer16",   "1dlut_00.cube",    1 ),
        ( "test.1dlut", cal.GET_1D_LUT, "1dlut_00.txt", 3072,   "unsigned integer16",   "1dlut_00.cube",    2 ),
    ]

    @pytest.mark.parametrize("backupFile,command,fileName,count,type,dataFile,expected", data_get_1d_lut)
    async def test_get_1d_lut(self, tmp_path, mocker, backupFile, command, fileName, count, type, dataFile, expected):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(currentDir, TEST_DIR_DATA, fileName)) as f:
                dataLut = f.read()
        data = {"data": dataLut, "dataCount": count, "dataType": type}
        mocker.patch('bscpylgtv.WebOsClient.request', return_value=data)

        client = await WebOsClient.create("x", states=[], client_key="x")

        if expected > 1:
            backupFileObj = tmp_path / backupFile
            res = await client.get_1d_lut(str(backupFileObj))

            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile)) as f:
                result = f.read()

            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
            assert backupFileObj.read_text() == result
        elif expected == 1:
            res = await client.get_1d_lut(backupFile)
            result = np.loadtxt(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile), dtype=np.uint16)

            assert np.array_equal(result, res)
            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
        elif expected == 0:
            with pytest.raises(ValueError, match=r'data should have size .+$'):
                await client.get_1d_lut(backupFile)
        elif expected == -1:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid .+$'):
                await client.get_1d_lut(backupFile)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid Get Calibration file extension, .+$'):
                await client.get_1d_lut(backupFile)



    data_get_3d_lut = [
        ( "HE_DTV_W17H",    "",             None,           "3dlut_33pt_00.txt",    None,   None,                   None,                   -3 ),
        ( "HE_DTV_W18H",    "foo.bar",      None,           "3dlut_33pt_00.txt",    None,   None,                   None,                   -2 ),
        ( "HE_DTV_W18H",    "",             cal.GET_3D_LUT, "3dlut_17pt_00.txt",    14740,  "foo",                  "3dlut_17pt_00.npy",    -1 ),
        ( "HE_DTV_W22O",    "",             cal.GET_3D_LUT, "3dlut_33pt_00.txt",    107812, "foo",                  "3dlut_33pt_00.npy",    -1 ),
        ( "HE_DTV_W18H",    "",             cal.GET_3D_LUT, "3dlut_17pt_00.txt",    14740,  "unsigned integer16",   "3dlut_17pt_00.npy",    0 ),
        ( "HE_DTV_W22O",    "",             cal.GET_3D_LUT, "3dlut_33pt_00.txt",    107812, "unsigned integer16",   "3dlut_33pt_00.npy",    0 ),

        ( "HE_DTV_W18H",    "",             cal.GET_3D_LUT, "3dlut_17pt_00.txt",    14739,  "unsigned integer16",   "3dlut_17pt_00.npy",    1 ),
        ( "HE_DTV_W22O",    "",             cal.GET_3D_LUT, "3dlut_33pt_00.txt",    107811, "unsigned integer16",   "3dlut_33pt_00.npy",    1 ),
        ( "HE_DTV_W18H",    "test.3dlut",   cal.GET_3D_LUT, "3dlut_17pt_00.txt",    14739,  "unsigned integer16",   "3dlut_17pt.3dlut",     2 ),
        ( "HE_DTV_W22O",    "test.3dlut",   cal.GET_3D_LUT, "3dlut_33pt_00.txt",    107811, "unsigned integer16",   "3dlut_33pt.3dlut",     2 ),
    ]

    @pytest.mark.parametrize("model,backupFile,command,fileName,count,type,dataFile,expected", data_get_3d_lut)
    async def test_get_3d_lut(self, tmp_path, mocker, model, backupFile, command, fileName, count, type, dataFile, expected):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(currentDir, TEST_DIR_DATA, fileName)) as f:
                dataLut = f.read()
        data = {"data": dataLut, "dataCount": count, "dataType": type}
        mocker.patch('bscpylgtv.WebOsClient.request', return_value=data)

        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}

        if expected > 1:
            backupFileObj = tmp_path / backupFile
            res = await client.get_3d_lut(str(backupFileObj))

            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile)) as f:
                result = f.read()

            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
            assert backupFileObj.read_text() == result
        elif expected == 1:
            res = await client.get_3d_lut(backupFile)
            result = np.load(os.path.join(currentDir, TEST_DIR_EXPECTED, dataFile))

            assert np.array_equal(result, res)
            client.request.assert_called_once_with(ep.GET_CALIBRATION, {"command": command})
        elif expected == 0:
            with pytest.raises(ValueError, match=r'data should have size .+$'):
                await client.get_3d_lut(backupFile)
        elif expected == -1:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid .+$'):
                await client.get_3d_lut(backupFile)
        elif expected == -2:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid Get Calibration file extension, .+$'):
                await client.get_3d_lut(backupFile)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                await client.get_3d_lut(backupFile)



    data_start_calibration = [
        ( "foo",      None,           0 ),
        ( "expert1",  cal.CAL_START,  1 ),
    ]

    @pytest.mark.parametrize("picMode,command,expected", data_start_calibration)
    async def test_start_calibration(self, mocker, picMode, command, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

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
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                await client.start_calibration(picMode)



    data_end_calibration = [
        ( cal.CAL_END ),
    ]

    @pytest.mark.parametrize("command", data_end_calibration)
    async def test_end_calibration(self, mocker, command):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

        await client.end_calibration()

        payload = {
            "command":      command,
            "profileNo":    0,
            "programID":    1,
        }

        client.request.assert_called_once_with(ep.CALIBRATION, payload)



    data_set_ui_data_methods = [
        ( "x",    "oled_light",   cal.BACKLIGHT_UI_DATA,  None,   0 ),
        ( 4.5,    "oled_light",   cal.BACKLIGHT_UI_DATA,  None,   0 ),
        ( -1,     "oled_light",   cal.BACKLIGHT_UI_DATA,  None,   0 ),
        ( 102,    "oled_light",   cal.BACKLIGHT_UI_DATA,  None,   0 ),
        ( 39,     "oled_light",   cal.BACKLIGHT_UI_DATA,  "JwA=", 1 ),
          
        ( "x",    "contrast",     cal.CONTRAST_UI_DATA,   None,   0 ),
        ( 4.5,    "contrast",     cal.CONTRAST_UI_DATA,   None,   0 ),
        ( -1,     "contrast",     cal.CONTRAST_UI_DATA,   None,   0 ),
        ( 102,    "contrast",     cal.CONTRAST_UI_DATA,   None,   0 ),
        ( 39,     "contrast",     cal.CONTRAST_UI_DATA,   "JwA=", 1 ),
          
        ( "x",   "brightness",   cal.BRIGHTNESS_UI_DATA, None,   0 ),
        ( 4.5,    "brightness",   cal.BRIGHTNESS_UI_DATA, None,   0 ),
        ( -1,     "brightness",   cal.BRIGHTNESS_UI_DATA, None,   0 ),
        ( 102,    "brightness",   cal.BRIGHTNESS_UI_DATA, None,   0 ),
        ( 39,     "brightness",   cal.BRIGHTNESS_UI_DATA, "JwA=", 1 ),
          
        ( "x",    "color",        cal.COLOR_UI_DATA,      None,   0 ),
        ( 4.5,    "color",        cal.COLOR_UI_DATA,      None,   0 ),
        ( -1,     "color",        cal.COLOR_UI_DATA,      None,   0 ),
        ( 102,    "color",        cal.COLOR_UI_DATA,      None,   0 ),
        ( 39,     "color",        cal.COLOR_UI_DATA,      "JwA=", 1 ),
    ]

    @pytest.mark.parametrize(",value,methodName,command,data,expected", data_set_ui_data_methods)
    async def test_set_ui_data_methods(self, mocker, value, methodName, command, data, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")
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
        else:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await method(value)



    data_upload_1d_lut = [
        ( [3],     None,               None,   None,   0 ),
        ( [],      "",                 0,      2,      1 ),
        ( None,    "1dlut_unity.txt",  3072,   1,      1 ),
    ]

    @pytest.mark.parametrize("inputData,dataFile,dataCount,dataOpt,expected", data_upload_1d_lut)
    async def test_upload_1d_lut(self, mocker, inputData, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

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
        else:
            with pytest.raises(TypeError, match=r'data must be of type ndarray .+$'):
                await client.upload_1d_lut(inputData)



    data_upload_1d_lut_from_file = [
        ( "1dlut.txt",     None,               None,   None,   -3 ),
          
        ( "1dlut_11.cal",  None,               None,   None,   -2 ),
        ( "1dlut_12.cube", None,               None,   None,   -1 ),
        ( "1dlut_13.cube", None,               None,   None,   0 ),
          
        ( "1dlut_01.cal",  "1dlut_01.txt",     3072,   1,      1 ),
        ( "1dlut_02.cal",  "1dlut_02.txt",     3072,   1,      1 ),
        ( "1dlut_03.cube", "1dlut_03.txt",     3072,   1,      1 ),
        ( "1dlut_03.1dlut","1dlut_03.txt",     3072,   1,      1 ),
    ]

    @pytest.mark.parametrize("fileName,dataFile,dataCount,dataOpt,expected", data_upload_1d_lut_from_file)
    async def test_upload_1d_lut_from_file(self, mocker, fileName, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")
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
        else:
            with pytest.raises(ValueError, match=r'Unsupported file format .+$'):
                await client.upload_1d_lut_from_file(fileName)



    data_upload_3d_lut = [
        ( "HE_DTV_W17H",   None,    cal.UPLOAD_3D_LUT_BT709,    None,                   None,   None,   -2 ),
        ( "HE_DTV_W17H",   None,    None,                       None,                   None,   None,   -1 ),
        ( "HE_DTV_W18H",   None,    "foo",                      None,                   None,   None,   -1 ),
        ( "HE_DTV_W18H",   [3],     cal.UPLOAD_3D_LUT_BT709,    None,                   None,   None,   0 ),
        ( "HE_DTV_W18H",   [],      cal.UPLOAD_3D_LUT_BT2020,   "",                     0,      2,      1 ),
        ( "HE_DTV_W18H",   None,    cal.UPLOAD_3D_LUT_BT709,    "3dlut_17pt_unity.txt", 14739,  1,      1 ),
        ( "HE_DTV_W22O",   None,    cal.UPLOAD_3D_LUT_BT2020,   "3dlut_33pt_unity.txt", 107811, 1,      1 ),
    ]

    @pytest.mark.parametrize("model,inputData,command,dataFile,dataCount,dataOpt,expected", data_upload_3d_lut)
    async def test_upload_3d_lut(self, mocker, model, inputData, command, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}

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
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                await client.upload_3d_lut(command, inputData)



    data_upload_3d_lut_bt709_bt2020 = [
        ( "bt709",  cal.UPLOAD_3D_LUT_BT709 ),
        ( "bt2020", cal.UPLOAD_3D_LUT_BT2020 ),
    ]

    @pytest.mark.parametrize("methodName,command", data_upload_3d_lut_bt709_bt2020)
    async def test_upload_3d_lut_bt709_bt2020(self, mocker, methodName, command):
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut')
        
        data = []
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : "HE_DTV_W22O"}
        method = getattr(client, f'upload_3d_lut_{methodName}')
        await method(data)

        client.upload_3d_lut.assert_called_once_with(command, data)



    data_upload_3d_lut_from_file = [
        ( "HE_DTV_W17H",   "3dlut_17pt.cube",   cal.UPLOAD_3D_LUT_BT709,    None,                   None,   None,   -5 ),
        ( "HE_DTV_W18H",   "3dlut.cal",         None,                       None,                   None,   None,   -4 ),

        ( "HE_DTV_W18H",   "3dlut_11.cube",     None,                       None,                   None,   None,   -3 ),
        ( "HE_DTV_W18H",   "3dlut_12.cube",     None,                       None,                   None,   None,   -2 ),
        ( "HE_DTV_W18H",   "3dlut_13.cube",     None,                       None,                   None,   None,   -1 ),
        ( "HE_DTV_W18H",   "3dlut_14.cube",     cal.UPLOAD_3D_LUT_BT709,    None,                   None,   None,   0 ),

        ( "HE_DTV_W18H",   "3dlut_17pt.cube",   cal.UPLOAD_3D_LUT_BT709,    "3dlut_17pt_01.txt",    14739,  1,      1 ),
        ( "HE_DTV_W22O",   "3dlut_33pt.cube",   cal.UPLOAD_3D_LUT_BT2020,   "3dlut_33pt_01.txt",    107811, 1,      1 ),
        ( "HE_DTV_W18H",   "3dlut_17pt.3dlut",  cal.UPLOAD_3D_LUT_BT2020,   "3dlut_17pt_01.txt",    14739,  1,      1 ),
        ( "HE_DTV_W22O",   "3dlut_33pt.3dlut",  cal.UPLOAD_3D_LUT_BT709,    "3dlut_33pt_01.txt",    107811, 1,      1 ),
    ]

    @pytest.mark.parametrize("model,fileName,command,dataFile,dataCount,dataOpt,expected", data_upload_3d_lut_from_file)
    async def test_upload_3d_lut_from_file(self, mocker, model, fileName, command, dataFile, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}
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
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                await client.upload_3d_lut_from_file(command, os.path.join(currentDir, TEST_DIR_DATA, fileName))



    data_upload_3d_lut_bt709_bt2020_from_file = [
        ( "bt709",  cal.UPLOAD_3D_LUT_BT709 ),
        ( "bt2020", cal.UPLOAD_3D_LUT_BT2020 ),
    ]

    @pytest.mark.parametrize("methodName,command", data_upload_3d_lut_bt709_bt2020_from_file)
    async def test_upload_3d_lut_bt709_bt2020_from_file(self, mocker, methodName, command):
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_from_file')
        
        fileName = f'3dlut_33pt_{methodName}.cube'
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : "HE_DTV_W22O"}
        method = getattr(client, f'upload_3d_lut_{methodName}_from_file')
        await method(fileName)

        client.upload_3d_lut_from_file.assert_called_once_with(command, fileName)



    data_set_1d_en_2_2_0_45_1d_lut_3by3_gamut = [
        ( "",     "1d_en_2_2",    None,                           None,   None,   None,   0 ),
        ( "x",    "1d_en_2_2",    None,                           None,   None,   None,   0 ),
        ( 2,      "1d_en_2_2",    None,                           None,   None,   None,   0 ),
        ( [],     "1d_en_2_2",    cal.ENABLE_GAMMA_2_2_TRANSFORM, "",     0,      2,      1 ),
        ( False,  "1d_en_2_2",    cal.ENABLE_GAMMA_2_2_TRANSFORM, "AAA=", 1,      1,      1 ),
        ( True,   "1d_en_2_2",    cal.ENABLE_GAMMA_2_2_TRANSFORM, "AQA=", 1,      1,      1 ),
          
        ( "",     "1d_en_0_45",   None,                           None,   None,   None,   0 ),
        ( "x",    "1d_en_0_45",   None,                           None,   None,   None,   0 ),
        ( 2,      "1d_en_0_45",   None,                           None,   None,   None,   0 ),
        ( [],     "1d_en_0_45",   cal.ENABLE_GAMMA_0_45_TRANSFORM,"",     0,      2,      1 ),
        ( False,  "1d_en_0_45",   cal.ENABLE_GAMMA_0_45_TRANSFORM,"AAA=", 1,      1,      1 ),
        ( True,   "1d_en_0_45",   cal.ENABLE_GAMMA_0_45_TRANSFORM,"AQA=", 1,      1,      1 ),
          
        ( "",     "1d_lut_en",    None,                           None,   None,   None,   0 ),
        ( "x",    "1d_lut_en",    None,                           None,   None,   None,   0 ),
        ( 2,      "1d_lut_en",    None,                           None,   None,   None,   0 ),
        ( [],     "1d_lut_en",    cal.ENABLE_1D_LUT,              "",     0,      2,      1 ),
        ( False,  "1d_lut_en",    cal.ENABLE_1D_LUT,              "AAA=", 1,      1,      1 ),
        ( True,   "1d_lut_en",    cal.ENABLE_1D_LUT,              "AQA=", 1,      1,      1 ),
          
        ( "",     "3by3_gamut_en",None,                           None,   None,   None,   0 ),
        ( "x",    "3by3_gamut_en",None,                           None,   None,   None,   0 ),
        ( 2,      "3by3_gamut_en",None,                           None,   None,   None,   0 ),
        ( [],     "3by3_gamut_en",cal.ENABLE_3BY3_GAMUT,          "",     0,      2,      1 ),
        ( False,  "3by3_gamut_en",cal.ENABLE_3BY3_GAMUT,          "AAA=", 1,      1,      1 ),
        ( True,   "3by3_gamut_en",cal.ENABLE_3BY3_GAMUT,          "AQA=", 1,      1,      1 ),
    ]

    @pytest.mark.parametrize("enable,methodName,command,data,dataCount,dataOpt,expected", data_set_1d_en_2_2_0_45_1d_lut_3by3_gamut)
    async def test_set_1d_en_2_2_0_45_1d_lut_3by3_gamut(self, mocker, enable, methodName, command, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")
        method = getattr(client, f'set_{methodName}')

        if expected > 0:
            await method(enable)

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
        else:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await method(enable)



    data_set_3by3_gamut_data_bt709_bt2020_hdr = [
        ( "",                                     "3by3_gamut_data_bt709",    None,   None,   None,   None,   -2 ),
          
        ( [1025],                                 "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
        ( [[1, 0, 1]],                            "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
        ( [[1, 0, 1], [0, 1, 0]],                 "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
        ( [[1, 0], [0, 1], [0, 0]],               "3by3_gamut_data_bt709",    None,   None,   None,   None,   -1 ),
          
        ( [[1, 1025, 0], [0, 1, 0], [0, 0, 1]],   "3by3_gamut_data_bt709",    None,   None,   None,   None,   0 ),
        ( [[1, 0, 0], [0, 1, -1025], [0, 0, 1]],  "3by3_gamut_data_bt709",    None,   None,   None,   None,   0 ),
        ( [[1, 0, 0], [0, 1, 0], [0, 0, 1025]],   "3by3_gamut_data_bt709",    None,   None,   None,   None,   0 ),
          
        ( [], "3by3_gamut_data_bt709",    cal.BT709_3BY3_GAMUT_DATA,  "",     0,      2,      1 ),
        ( 0,  "3by3_gamut_data_bt709",    cal.BT709_3BY3_GAMUT_DATA,  "AACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAAAAAAAAAAAAAIA/", 9,      1,      1 ),
        ( [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]],    "3by3_gamut_data_bt709",    cal.BT709_3BY3_GAMUT_DATA,  "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", 9,  1,  1 ),
          
        ( "",                                     "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -2 ),
          
        ( [1025],                                 "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
        ( [[1, 0, 1]],                            "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
        ( [[1, 0, 1], [0, 1, 0]],                 "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
        ( [[1, 0], [0, 1], [0, 0]],               "3by3_gamut_data_bt2020",   None,   None,   None,   None,   -1 ),
          
        ( [[1, 1025, 0], [0, 1, 0], [0, 0, 1]],   "3by3_gamut_data_bt2020",   None,   None,   None,   None,   0 ),
        ( [[1, 0, 0], [0, 1, -1025], [0, 0, 1]],  "3by3_gamut_data_bt2020",   None,   None,   None,   None,   0 ),
        ( [[1, 0, 0], [0, 1, 0], [0, 0, 1025]],   "3by3_gamut_data_bt2020",   None,   None,   None,   None,   0 ),
          
        ( [], "3by3_gamut_data_bt2020",   cal.BT2020_3BY3_GAMUT_DATA, "",     0,      2,      1 ),
        ( 0,  "3by3_gamut_data_bt2020",   cal.BT2020_3BY3_GAMUT_DATA, "AACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAAAAAAAAAAAAAIA/", 9,      1,      1 ),
        ( [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]],    "3by3_gamut_data_bt2020",    cal.BT2020_3BY3_GAMUT_DATA,  "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", 9,  1,  1 ),
          
        ( "",                                     "3by3_gamut_data_hdr",      None,   None,   None,   None,   -2 ),
          
        ( [1025],                                 "3by3_gamut_data_hdr",      None,   None,   None,   None,   -1 ),
        ( [[1, 0, 1]],                            "3by3_gamut_data_hdr",      None,   None,   None,   None,   -1 ),
        ( [[1, 0, 1], [0, 1, 0]],                 "3by3_gamut_data_hdr",      None,   None,   None,   None,   -1 ),
        ( [[1, 0], [0, 1], [0, 0]],               "3by3_gamut_data_hdr",      None,   None,   None,   None,   -1 ),
          
        ( [[1, 1025, 0], [0, 1, 0], [0, 0, 1]],   "3by3_gamut_data_hdr",      None,   None,   None,   None,   0 ),
        ( [[1, 0, 0], [0, 1, -1025], [0, 0, 1]],  "3by3_gamut_data_hdr",      None,   None,   None,   None,   0 ),
        ( [[1, 0, 0], [0, 1, 0], [0, 0, 1025]],   "3by3_gamut_data_hdr",      None,   None,   None,   None,   0 ),
          
        ( [], "3by3_gamut_data_hdr",      cal.HDR_3BY3_GAMUT_DATA,    "",     0,      2,      1 ),
        ( 0,  "3by3_gamut_data_hdr",      cal.HDR_3BY3_GAMUT_DATA,    "AACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAAAAAAAAAAAAAIA/", 9,      1,      1 ),
        ( [[0.4, 0.3, 0.2], [0.2, 0.4, 0.3], [0.3, 0.2, 0.4]],    "3by3_gamut_data_hdr",      cal.HDR_3BY3_GAMUT_DATA,   "zczMPpqZmT7NzEw+zcxMPs3MzD6amZk+mpmZPs3MTD7NzMw+", 9,  1,  1 ),
    ]

    @pytest.mark.parametrize("value,methodName,command,data,dataCount,dataOpt,expected", data_set_3by3_gamut_data_bt709_bt2020_hdr)
    async def test_set_3by3_gamut_data_bt709_bt2020_hdr(self, mocker, value, methodName, command, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")
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
        else:
            with pytest.raises(ValueError, match=r'could not convert .+$'):
                await method(value)



    data_set_3by3_gamut_data_from_file = [
        ( "foo",  "3by3.1dlut",     None,                       -1 ),
        ( "bt709",  "3by3.1dlut",   None,                       0 ),
        ( "bt709",  "3by3.matrix",  cal.BT709_3BY3_GAMUT_DATA,  1 ),
        ( "bt2020", "3by3.matrix",  cal.BT2020_3BY3_GAMUT_DATA, 1 ),
        ( "hdr",    "3by3.matrix",  cal.HDR_3BY3_GAMUT_DATA,    1 ),
    ]

    @pytest.mark.parametrize("type,fileName,command,expected", data_set_3by3_gamut_data_from_file)
    async def test_set_3by3_gamut_data_from_file(self, mocker, type, fileName, command, expected):
        mocker.patch('bscpylgtv.WebOsClient.calibration_request')

        currentDir = os.path.dirname(os.path.realpath(__file__))
        client = await WebOsClient.create("x", states=[], client_key="x")

        if expected > 0:
            data = np.array([[1.3207, -0.2826, -0.0381], [-0.0749, 1.0719, 0.003], [0.0046, -0.0397, 1.0351]], dtype=np.float32)

            await client.set_3by3_gamut_data_from_file(type, os.path.join(currentDir, TEST_DIR_DATA, fileName))

            client.calibration_request.assert_called_once_with(command, mocker.ANY, 1)
            assert np.array_equal(data, client.calibration_request.call_args[0][1])
        elif expected == 0:
            with pytest.raises(ValueError, match=r'Unsupported file format .+$'):
                await client.set_3by3_gamut_data_from_file(type, os.path.join(currentDir, TEST_DIR_DATA, fileName))
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid 3by3 gamut type .+$'):
                await client.set_3by3_gamut_data_from_file(type, os.path.join(currentDir, TEST_DIR_DATA, fileName))



    data_set_bypass_modes_sdr = [
        ( False ),
        ( True  ),
    ]

    @pytest.mark.parametrize("unity1dLut", data_set_bypass_modes_sdr)
    async def test_set_bypass_modes_sdr(self, mocker, unity1dLut):
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_2_2')
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_0_45')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt709')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt709')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt2020')
        if unity1dLut:
            mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : "HE_DTV_W22O"}
        result = await client.set_bypass_modes_sdr(unity1dLut)

        client.set_1d_en_2_2.assert_called_once_with()
        client.set_1d_en_0_45.assert_called_once_with()
        client.set_3by3_gamut_data_bt709.assert_called_once_with()
        client.set_3by3_gamut_data_bt2020.assert_called_once_with()
        client.upload_3d_lut_bt709.assert_called_once_with()
        client.upload_3d_lut_bt2020.assert_called_once_with()
        if unity1dLut:
            client.upload_1d_lut.assert_called_once_with()
        assert result == True



    async def test_reset_factory_data_sdr(self, mocker):
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_2_2')
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_0_45')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt709')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt709')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        
        client = await WebOsClient.create("x", states=[], client_key="x")
        result = await client.reset_factory_data_sdr()

        client.set_1d_en_2_2.assert_called_once_with([])
        client.set_1d_en_0_45.assert_called_once_with([])
        client.set_3by3_gamut_data_bt709.assert_called_once_with([])
        client.set_3by3_gamut_data_bt2020.assert_called_once_with([])
        client.upload_3d_lut_bt709.assert_called_once_with([])
        client.upload_3d_lut_bt2020.assert_called_once_with([])
        client.upload_1d_lut.assert_called_once_with([])
        assert result == True



    data_set_bypass_modes_hdr10 = [
        ( False ),
        ( True  ),
    ]

    @pytest.mark.parametrize("unity_3d_lut", data_set_bypass_modes_hdr10)
    async def test_set_bypass_modes_hdr10(self, mocker, unity_3d_lut):
        mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        if unity_3d_lut:
            mocker.patch('bscpylgtv.WebOsClient.set_1d_en_2_2')
            mocker.patch('bscpylgtv.WebOsClient.set_1d_en_0_45')
            mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt709')
            mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt2020')
            mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt709')
            mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt2020')
        
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : "HE_DTV_W22O"}
        result = await client.set_bypass_modes_hdr10(unity_3d_lut)

        client.upload_1d_lut.assert_called_once_with()
        if unity_3d_lut:
            client.set_1d_en_2_2.assert_called_once_with()
            client.set_1d_en_0_45.assert_called_once_with()
            client.set_3by3_gamut_data_bt709.assert_called_once_with()
            client.set_3by3_gamut_data_bt2020.assert_called_once_with()
            client.upload_3d_lut_bt709.assert_called_once_with()
            client.upload_3d_lut_bt2020.assert_called_once_with()
        assert result == True



    data_reset_factory_data_hdr10 = [
        ( None,         False ),
        ( None,         True ),
        ( "hdr_game",   False ),
        ( "hdr_game",   True ),
    ]

    @pytest.mark.parametrize("picMode,tonemap_params", data_reset_factory_data_hdr10)
    async def test_reset_factory_data_hdr10(self, mocker, picMode, tonemap_params):
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_2_2')
        mocker.patch('bscpylgtv.WebOsClient.set_1d_en_0_45')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt709')
        mocker.patch('bscpylgtv.WebOsClient.set_3by3_gamut_data_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt709')
        mocker.patch('bscpylgtv.WebOsClient.upload_3d_lut_bt2020')
        mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        if tonemap_params:
            mocker.patch('bscpylgtv.WebOsClient.set_tonemap_params')

        client = await WebOsClient.create("x", states=[], client_key="x")
        result = await client.reset_factory_data_hdr10(picMode, tonemap_params)

        client.set_1d_en_2_2.assert_called_once_with([])
        client.set_1d_en_0_45.assert_called_once_with([])
        client.set_3by3_gamut_data_bt709.assert_called_once_with([])
        client.set_3by3_gamut_data_bt2020.assert_called_once_with([])
        client.upload_3d_lut_bt709.assert_called_once_with([])
        client.upload_3d_lut_bt2020.assert_called_once_with([])
        client.upload_1d_lut.assert_called_once_with([])
        if tonemap_params:
            client.set_tonemap_params.assert_called_once_with(picMode, [])
        assert result == True



    async def test_set_bypass_modes_dovi(self, mocker):
        mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        
        client = await WebOsClient.create("x", states=[], client_key="x")
        result = await client.set_bypass_modes_dovi()

        client.upload_1d_lut.assert_called_once_with()
        assert result == True



    data_reset_factory_data_dovi = [
        ( None,         False ),
        ( None,         True ),
        ( "hdr_game",   False ),
        ( "hdr_game",   True ),
    ]

    @pytest.mark.parametrize("picMode,dovi_config", data_reset_factory_data_dovi)
    async def test_reset_factory_data_dovi(self, mocker, picMode, dovi_config):
        mocker.patch('bscpylgtv.WebOsClient.upload_1d_lut')
        if dovi_config:
            mocker.patch('bscpylgtv.WebOsClient.set_dolby_vision_config_data')

        client = await WebOsClient.create("x", states=[], client_key="x")
        result = await client.reset_factory_data_dovi(picMode, dovi_config)

        client.upload_1d_lut.assert_called_once_with([])
        if dovi_config:
            client.set_dolby_vision_config_data.assert_called_once_with(picMode, [])
        assert result == True



    data_set_tonemap_params = [
        ( "foo",          810,    1000,   75, None,                   None,   None,   -1 ),
        ( "expert1",      810,    1000,   75, None,                   None,   None,   -1 ),
          
        ( "hdr_cinema",   99,     1000,   75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "hdr_game",     4001,   1000,   75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "hdr_cinema",   810,    99,     75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "hdr_cinema",   810,    10001,  75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "hdr_cinema",   810,    1000,   -1, "KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
        ( "hdr_cinema",   810,    1000,   101,"KgPoA0sAoA88ABAnMgA=", 7,      1,      0 ),
          
        ( "hdr_cinema",   [],     1000,   75, "",                     0,      2,      1 ),
        ( "hdr_game",     810,    1000,   75, "KgPoA0sAoA88ABAnMgA=", 7,      1,      1 ),
    ]

    @pytest.mark.parametrize("picMode,luminance,mp,rp,data,dataCount,dataOpt,expected", data_set_tonemap_params)
    async def test_set_tonemap_params(self, mocker, picMode, luminance, mp, rp, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

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
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid picture_mode .+$'):
                await client.set_tonemap_params(picMode, luminance, mp, rp)



    data_set_dolby_vision_config_data = [
        ( "HE_DTV_W17H",    "dolby_game",   620, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  -1 ),

        ( "HE_DTV_W18H",    "foo",          620, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "expert1",      620, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   50,  0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   4001,0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   620, -1,     2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   620, 1,      2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   620, 0.0001, -1,  [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   620, 0.0001, 10,  [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   620, 0.0001, 2.2, [-0.0001, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),
        ( "HE_DTV_W18H",    "dolby_game",   620, 0.0001, 2.2, [0.6796, 1.0001, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], None,  None,    None,  0 ),

        ( "HE_DTV_W18H",    "dolby_game",   [],   None,   None,   None,   "", 0,  2,  1 ),
        ( "HE_DTV_W18H",    "dolby_cinema_dark",    710, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], "UGljdHVyZU1vZGUgPSAyDQpUbWF4ID0gNzEwLjAwMDANClRtaW4gPSAwLjAwMDENClRnYW1tYSA9IDIuMg0KQ29sb3JQcmltYXJpZXMgPSAwLjY3OTYgMC4zMTg3IDAuMjU5NSAwLjY4NDkgMC4xNDQ4IDAuMDQ5NCAwLjMxMjcgMC4zMjkwDQpUTE1TMlJHQm1hdCA9IDQuMTgyNzgzOTgzMjk0NTEgLTMuMzAwNDkyOTUxMDE5NDEgMC4xMTc3NDk4NzA5NTUzMjUgLTAuODgyNDY3MTQwNzYyNzUwIDIuMDE3MzQ1NDgyODExODMgLTAuMTM0ODY1ODY5Nzg0NTI3IDAuMDQzNzgyNzQ3MzA0ODQzMSAtMC4xMDc2NzAyODY3NTcwMjUgMS4wNjM5MTU1MTA2MDc1MA0K",  315,    1,  1 ),
        ( "HE_DTV_W22O",    "dolby_game",   [],   None,   None,   None,   "", 0,  2,  1 ),
        ( "HE_DTV_W22O",    "dolby_game",   820, 0.0001, 2.2, [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494, 0.3127, 0.3290], "W1BpY3R1cmVNb2RlID0gNF0NClRtYXggPSA4MjAuMDAwMA0KVG1pbiA9IDAuMDAwMQ0KVGdhbW1hID0gMi4yDQpUUHJpbWFyaWVzID0gMC42Nzk2IDAuMzE4NyAwLjI1OTUgMC42ODQ5IDAuMTQ0OCAwLjA0OTQgMC4zMTI3IDAuMzI5MA0K",  135,    1,  1 ),
    ]

    @pytest.mark.parametrize("model,picMode,whiteL,blackL,gamma,primaries,data,dataCount,dataOpt,expected", data_set_dolby_vision_config_data)
    async def test_set_dolby_vision_config_data(self, mocker, model, picMode, whiteL, blackL, gamma, primaries, data, dataCount, dataOpt, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}

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
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                await client.set_dolby_vision_config_data(picMode, whiteL, blackL, gamma, primaries)



    data_write_dolby_vision_config_file = [
        ( "HE_DTV_W17H",      [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   -3 ),

        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,    None, None, -2 ),

        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   "false",    "", None,   -1 ),

        ( "HE_DTV_W18H",    [{"picture_mode": "foo", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   0 ),
        ( "HE_DTV_W22O",    [{"picture_mode": "dolby_cinema_bright", "white_level": 710, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   0 ),
        ( "HE_DTV_W18H",    [{"white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False, "", None,   0 ),
        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_dark", "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", None,   0 ),
        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750}],   False, "", None,   0 ),
        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448]}],   False,  "", None,   0 ),
        ( "HE_DTV_W18H",    [{}], False,  "", None, 0 ),
        ( "HE_DTV_W18H",    [],   False,  "", None, 0 ),
        ( "HE_DTV_W18H",    None, False,  "", None, 0 ),

        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", "dv_cfg_2018_01.txt",   1 ),
        ( "HE_DTV_W18H",    [{"white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   True,  "", "dv_cfg_2018_02.txt",   1 ),
        ( "HE_DTV_W18H",    [{"picture_mode": "dolby_cinema_bright", "white_level": 710, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", "dv_cfg_2018_03.txt",   1 ),
        ( "HE_DTV_W22O",    [{"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "", "dv_cfg_2019_01.txt",   1 ),
        ( "HE_DTV_W22O",    [{"white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   True,  "", "dv_cfg_2019_02.txt",   1 ),
        ( "HE_DTV_W22O",    [{"picture_mode": "dolby_cinema_bright", "white_level": 710, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_cinema_dark", "white_level": 750, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}, {"picture_mode": "dolby_game", "white_level": 680, "primaries": [0.6796, 0.3187, 0.2595, 0.6849, 0.1448, 0.0494]}],   False,  "d:\temp",    "dv_cfg_2019_03.txt",   1 ),
    ]

    @pytest.mark.parametrize("model,data,allModes,path,cfgFile,expected", data_write_dolby_vision_config_file)
    async def test_write_dolby_vision_config_file(self, mocker, model, data, allModes, path, cfgFile, expected):
        client = await WebOsClient.create("x", states=["software_info"], client_key="x")
        client._software_info = {"model_name" : model}

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
            with pytest.raises(PyLGTVCmdException, match=r'^.+ not supported by model .+$'):
                await client.write_dolby_vision_config_file(data, allModes, path)



    data_convert_1dlut_to_cal = [
        ( "",               "1dlut_14.cal", -1),
        ( "1dlut_14.txt",   "1dlut_14.cal", -1),

        ( "1dlut_14.1dlut", "",             0),
        ( "1dlut_14.1dlut", "1dlut_14.txt", 0),

        ( "1dlut_14.1dlut", "1dlut_14.cal", 1),
    ]

    @pytest.mark.parametrize("infile,outfile,expected", data_convert_1dlut_to_cal)
    async def test_convert_1dlut_to_cal(self, mocker, infile, outfile, expected):
        client = await WebOsClient.create("x", states=[], client_key="x")

        if expected > 0:
            currentDir = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, outfile)) as f:
                expectedData = f.read().replace("2023-12-23", date.today().isoformat())

            mockedOpen = mocker.patch("builtins.open", mocker.mock_open())
            result = await client.convert_1dlut_to_cal(os.path.join(currentDir, TEST_DIR_DATA, infile), outfile)

            assert result == True
            mockedOpen.assert_called_once_with(outfile, "w", newline='\r\n')
            mockedOpen.return_value.write.assert_called_once_with(expectedData)
        elif expected == 0:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid cal file extension.+$'):
                await client.convert_1dlut_to_cal(infile, outfile)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid 1DLUT file extension.+$'):
                await client.convert_1dlut_to_cal(infile, outfile)



    data_convert_cal_to_1dlut = [
        ( "",               "1dlut_15.1dlut",   -1),
        ( "1dlut_15.txt",   "1dlut_15.1dlut",   -1),

        ( "1dlut_15.cal",   "",                 0),
        ( "1dlut_15.cal",   "1dlut_15.txt",     0),

        ( "1dlut_15.cal",   "1dlut_15.1dlut",   1),
    ]

    @pytest.mark.parametrize("infile,outfile,expected", data_convert_cal_to_1dlut)
    async def test_convert_cal_to_1dlut(self, tmp_path, infile, outfile, expected):
        client = await WebOsClient.create("x", states=[], client_key="x")

        if expected > 0:
            currentDir = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(currentDir, TEST_DIR_EXPECTED, outfile)) as f:
                expectedData = f.read()

            tmpFileObj = tmp_path / "1dlut.1dlut"
            result = await client.convert_cal_to_1dlut(os.path.join(currentDir, TEST_DIR_DATA, infile), str(tmpFileObj))

            assert result == True
            assert tmpFileObj.read_text() == expectedData
        elif expected == 0:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid 1DLUT file extension.+$'):
                await client.convert_cal_to_1dlut(infile, outfile)
        else:
            with pytest.raises(PyLGTVCmdException, match=r'Invalid cal file extension.+$'):
                await client.convert_cal_to_1dlut(infile, outfile)



    data_set_itpg_patch_window = [
        ( -1, 81,     98, 0,  858,    482,    1491,   839,    0 ),
        ( 71, 1024,   98, 0,  858,    482,    1491,   839,    0 ),
        ( 71, 81,     98, -1, 858,    482,    1491,   839,    0 ),
        ( 71, 81,     98, 10, 858,    482,    1491,   839,    0 ),
        ( 71, 81,     98, 0,  99,     482,    1491,   839,    0 ),
        ( 71, 81,     98, 0,  858,    7681,   1491,   839,    0 ),
        ( 71, 81,     98, 0,  858,    55,     1491,   839,    0 ),
        ( 71, 81,     98, 0,  858,    4321,   1491,   839,    0 ),
        ( 71, 81,     98, 0,  858,    482,    -1,     839,    0 ),
        ( 71, 81,     98, 0,  858,    482,    7580,   839,    0 ),
        ( 71, 81,     98, 0,  858,    482,    1491,   -1,     0 ),
        ( 71, 81,     98, 0,  858,    482,    1491,   4264,   0 ),
          
        ( 71, 81,     98, 0,  858,    482,    1491,   839,    1 ),
        ( 71, 81,     98, 1,  858,    482,    1491,   839,    1 ),
    ]

    @pytest.mark.parametrize("r,g,b,winId,w,h,sx,sy,expected", data_set_itpg_patch_window)
    async def test_set_itpg_patch_window(self, mocker, r, g, b, winId, w, h, sx, sy, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

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
        else:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.set_itpg_patch_window(r, g, b, winId, w, h, sx, sy)



    data_set_itpg_gradation_window = [
        ( -1, 3,      610,    520,    230,    1,  1,      1,  0 ),
        ( 4,  3,      610,    520,    230,    1,  1,      1,  0 ),
        ( 0,  -1,     610,    520,    230,    1,  1,      1,  0 ),
        ( 0,  7681,   610,    520,    230,    1,  1,      1,  0 ),
        ( 0,  3,      -1,     520,    230,    1,  1,      1,  0 ),
        ( 0,  3,      610,    1024,   230,    1,  1,      1,  0 ),
        ( 0,  3,      610,    520,    230,    -1, 1,      1,  0 ),
        ( 0,  3,      610,    520,    230,    1,  513,    1,  0 ),
          
        ( 0,  3,      610,    520,    230,    1,  1,      1,  1 ),
        ( 1,  3,      610,    50,     23,     1,  1,      1,  1 ),
    ]

    @pytest.mark.parametrize("id,ss,ar,ag,ab,er,eg,eb,expected", data_set_itpg_gradation_window)
    async def test_set_itpg_gradation_window(self, mocker, id, ss, ar, ag, ab, er, eg, eb, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

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
        else:
            with pytest.raises(ValueError, match=r'Invalid .+$'):
                await client.set_itpg_gradation_window(id, ss, ar, ag, ab, er, eg, eb)



    data_toggle_itpg = [
        ( None,   2,  0,  False, (True,       -1) ),
        ( True,   2,  0,  None,  (True,       -1) ),
        ( True,   -1, 0,  False, (True,       0) ),
        ( True,   11, 0,  False, (True,       0) ),
        ( True,   2,  -1, False, (True,       0) ),
        ( True,   2,  3,  False, (True,       0) ),
          
        ( True,   2,  0,  False, (True,       1) ),
        ( True,   2,  1,  False, (True,       1) ),
        ( False,  0,  0,  False, (False,      1) ),
        ( True,   2,  0,  True,  ("true",     1) ),
        ( True,   2,  1,  True,  ("true",     1) ),
        ( False,  0,  0,  True,  ("false",    1) ),
    ]

    @pytest.mark.parametrize("enable,numOfBox,ptnType,fixEnable,expected", data_toggle_itpg)
    async def test_toggle_itpg(self, mocker, enable, numOfBox, ptnType, fixEnable, expected):
        mocker.patch('bscpylgtv.WebOsClient.request')

        client = await WebOsClient.create("x", states=[], client_key="x")

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
        else:
            with pytest.raises(TypeError, match=r'^.+ should be a bool, .+$'):
                await client.toggle_itpg(enable, numOfBox, ptnType, fixEnable)

