from types import MappingProxyType

try:
    import numpy as np
except ImportError:
    np = None

LUT3D_SIZES = MappingProxyType({
    "17pt": 17,
    "33pt": 33,
})

DV_CONFIG_TYPES = MappingProxyType({
    "2018": 2018,
    "2019": 2019,
})

if np:
    #  xr, yr, xg, yg, xb, yb, xw, yw
    BT2020_PRIMARIES = (0.708, 0.292, 0.170, 0.797, 0.131, 0.046, 0.3127, 0.3290)

    CALIBRATION_TYPE_MAP = MappingProxyType({
        "uint8":    "unsigned char",
        "uint16":   "unsigned integer16",
        "float32":  "float",
    })

    SDR_PICTURE_MODES = ("cinema", "expert1", "expert2", "game", "technicolorExpert", "filmMaker")
    HDR10_PICTURE_MODES = ("hdr_cinema", "hdr_game", "hdr_technicolorExpert", "hdr_filmMaker")

    DV_PICTURE_MODES = MappingProxyType({
        "dolby_cinema_bright":  1,
        "dolby_cinema_dark":    2,
        "dolby_game":           4,
    })

    DV_BLACK_LEVEL = 0.0001
    DV_GAMMA = 2.2

    DV_CONFIG_FILENAME = "DolbyVision_UserDisplayConfiguration.txt"

    LUT1D_POINTS = MappingProxyType({
        "0.0000":   0,
        "0.0250":   26,
        "0.0500":   51,
        "0.0750":   77,
        "0.1000":   102,
        "0.1500":   153,
        "0.2000":   205,
        "0.2500":   256,
        "0.3000":   307,
        "0.3500":   358,
        "0.4000":   409,
        "0.4500":   460,
        "0.5000":   512,
        "0.5500":   563,
        "0.6000":   614,
        "0.6500":   665,
        "0.7000":   716,
        "0.7500":   767,
        "0.8000":   818,
        "0.8500":   870,
        "0.9000":   921,
        "0.9500":   972,
        "1.0000":   1023,
    })
