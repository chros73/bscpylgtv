try:
    import numpy as np
except ImportError:
    np = None

if np:
    CALIBRATION_TYPE_MAP = {
        "uint8": "unsigned char",
        "uint16": "unsigned integer16",
        "float32": "float",
    }

    DEFAULT_CAL_DATA = np.array(
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0044, -0.0453, 1.041], dtype=np.float32
    )

    #  xr, yr, xg, yg, xb, yb, xw, yw
    BT2020_PRIMARIES = (0.708, 0.292, 0.170, 0.797, 0.131, 0.046, 0.3127, 0.3290)
    DV_CONFIG_FILENAMES = {
        2018: "DolbyVision_UserDisplayConfiguration.txt",
        2019: "DolbyVision_UserDisplayConfiguration_2019.txt",
    }
