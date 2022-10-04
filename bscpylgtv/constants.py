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

    # DoVi picture modes: 1 - DoVi Cinema Home, 2 - DoVi Cinema, 4 - DoVi Game
    DV_PICTURE_MODES = (1, 2, 4)
    DV_BLACK_LEVEL = 0.0001
    DV_GAMMA = 2.2

    DV_CONFIG_FILENAME = "DolbyVision_UserDisplayConfiguration.txt"
