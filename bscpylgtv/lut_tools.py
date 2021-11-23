try:
    import numpy as np
except ImportError:
    np = None

if np:
    from .constants import BT2020_PRIMARIES, DV_CONFIG_FILENAMES


    def unity_lut_1d():
        lutmono = np.linspace(0.0, 32767.0, 1024, dtype=np.float64)
        lut = np.stack([lutmono] * 3, axis=0)
        lut = np.rint(lut).astype(np.uint16)
        return lut


    def unity_lut_3d(n=33):
        spacing = complex(0, n)
        endpoint = 4096.0
        lut = np.mgrid[0.0:endpoint:spacing, 0.0:endpoint:spacing, 0.0:endpoint:spacing]
        lut = np.rint(lut).astype(np.uint16)
        lut = np.clip(lut, 0, 4095)
        lut = np.transpose(lut, axes=(1, 2, 3, 0))
        lut = np.flip(lut, axis=-1)
        return lut


    def read_cube_file(filename):  # noqa: C901
        nheader = 0
        lut_1d_size = None
        lut_3d_size = None
        domain_min = None
        domain_max = None

        with open(filename) as f:
            lines = f.readlines()

        def domain_check(line, which):
            domain_limit = np.genfromtxt([line], usecols=(1, 2, 3), dtype=np.float64)
            if domain_limit.shape != (3,):
                raise ValueError(f"DOMAIN_{which} must provide exactly 3 values.")
            if np.amin(domain_limit) < -1e37 or np.amax(domain_limit) > 1e37:
                raise ValueError(
                    f"Invalid value in DOMAIN_{which}, must be in range [-1e37,1e37]."
                )
            return domain_limit

        def lut_size(splitline, dim):
            lut_size = int(splitline[1])
            upper_limit = {1: 65536, 3: 256}[dim]
            if lut_size < 2 or lut_size > upper_limit:
                raise ValueError(
                    f"Invalid value {lut_size} for LUT_{dim}D_SIZE,"
                    f" must be in range [2, {upper_limit}]."
                )
            return lut_size

        for line in lines:
            icomment = line.find("#")
            if icomment >= 0:
                line = line[:icomment]

            splitline = line.split()
            if splitline:
                keyword = splitline[0]
            else:
                keyword = None

            if keyword is None:
                pass
            elif keyword == "TITLE":
                pass
            elif keyword == "LUT_1D_SIZE":
                lut_1d_size = lut_size(splitline, dim=1)
            elif keyword == "LUT_3D_SIZE":
                lut_3d_size = lut_size(splitline, dim=3)
            elif keyword == "DOMAIN_MIN":
                domain_min = domain_check(line, "MIN")
            elif keyword == "DOMAIN_MAX":
                domain_max = domain_check(line, "MAX")
            else:
                break

            nheader += 1

        if lut_1d_size and lut_3d_size:
            raise ValueError("Cannot specify both LUT_1D_SIZE and LUT_3D_SIZE.")

        if not lut_1d_size and not lut_3d_size:
            raise ValueError("Must specify one of LUT_1D_SIZE or LUT_3D_SIZE.")

        if domain_min is None:
            domain_min = np.zeros((1, 3), dtype=np.float64)

        if domain_max is None:
            domain_max = np.ones((1, 3), dtype=np.float64)

        lut = np.genfromtxt(lines[nheader:], comments="#", dtype=np.float64)
        if np.amin(lut) < -1e37 or np.amax(lut) > 1e37:
            raise ValueError("Invalid value in DOMAIN_MAX, must be in range [-1e37,1e37].")

        # shift and scale lut to range [0.,1.]
        lut = (lut - domain_min) / (domain_max - domain_min)

        if lut_1d_size:
            if lut.shape != (lut_1d_size, 3):
                raise ValueError(
                    f"Expected shape {(lut_1d_size, 3)} for 1D LUT, but got {lut.shape}."
                )
            # convert to integer with appropriate range
            lut = np.rint(lut * 32767.0).astype(np.uint16)
            # transpose to get the correct element order
            lut = np.transpose(lut)
        elif lut_3d_size:
            if lut.shape != (lut_3d_size ** 3, 3):
                raise ValueError(
                    f"Expected shape {(lut_3d_size**3, 3)} for 3D LUT, but got {lut.shape}."
                )
            lut = np.reshape(lut, (lut_3d_size, lut_3d_size, lut_3d_size, 3))
            lut = np.rint(lut * 4096.0).astype(np.uint16)
            lut = np.clip(lut, 0, 4095)
        return lut


    def read_cal_file(filename):
        with open(filename, "r") as f:
            caldata = f.readlines()

        dataidx = caldata.index("BEGIN_DATA\n")
        lut_1d_size_in = int(caldata[dataidx - 1].split()[1])

        lut = np.genfromtxt(
            caldata[dataidx + 1 : dataidx + 1 + lut_1d_size_in], dtype=np.float64
        )

        if lut.shape != (lut_1d_size_in, 4):
            raise ValueError(
                f"Expected shape {(lut_1d_size_in,3)} for 1D LUT, but got {lut.shape}."
            )

        lut_1d_size = 1024

        # interpolate if necessary
        if lut_1d_size_in != lut_1d_size:
            x = np.linspace(0.0, 1.0, lut_1d_size, dtype=np.float64)
            lutcomponents = [np.interp(x, lut[:, 0], lut[:, i]) for i in range(1, 4)]
            lut = np.stack(lutcomponents, axis=-1)
        else:
            lut = lut[:, 1:]

        # convert to integer with appropriate range
        lut = np.rint(32767.0 * lut).astype(np.uint16)
        # transpose to get the correct element order
        lut = np.transpose(lut)

        return lut


    def lms2rgb_matrix(primaries=BT2020_PRIMARIES):
        xy = np.array(primaries, dtype=np.float64)

        xy = np.resize(xy, (4, 2))
        y = xy[:, 1]
        y = np.reshape(y, (4, 1))
        zcol = 1.0 - np.sum(xy, axis=-1, keepdims=True)
        xyz = np.concatenate((xy, zcol), axis=-1)
        XYZ = xyz / y
        XYZ = np.transpose(XYZ)

        XYZrgb = XYZ[:, :3]
        XYZw = XYZ[:, 3:4]

        s = np.matmul(np.linalg.inv(XYZrgb), XYZw)
        s = np.reshape(s, (1, 3))

        rgb2xyz = s * XYZrgb
        xyz2rgb = np.linalg.inv(rgb2xyz)

        # normalized to d65
        xyz2lms = np.array(
            [[0.4002, 0.7076, -0.0808], [-0.2263, 1.1653, 0.0457], [0.0, 0.0, 0.9182]],
            dtype=np.float64,
        )
        lms2xyz = np.linalg.inv(xyz2lms)

        lms2rgb = np.matmul(xyz2rgb, lms2xyz)

        return lms2rgb


    def create_dolby_vision_config(
        version=2019,
        white_level=700.0,
        black_level=0.0,
        gamma=2.2,
        primaries=BT2020_PRIMARIES,
    ):

        if not (white_level >= 100.0 and white_level <= 999.0):
            raise ValueError(
                f"Invalid white_level {white_level}, must be between 100. and 999."
            )
        if not (black_level >= 0.0 and black_level <= 0.99):
            raise ValueError(
                f"Invalid black level {black_level}, must be between 0. and 0.99"
            )
        if not (gamma > 0.0 and gamma < 9.9):
            raise ValueError(f"Invalid gamma {gamma}, must be between 0. and 9.9")
        for value in primaries:
            if not (value >= 0.0 and value <= 1.0):
                raise ValueError(
                    f"Invalid primary value {value}, must be between 0. and 1."
                )

        xr, yr, xg, yg, xb, yb, xw, yw = primaries

        if version == 2018:
            lms2rgb = lms2rgb_matrix(primaries)
            tlms2rgb = np.reshape(lms2rgb, [9])

            config = f"""# Dolby Vision User Display Configuration File
    # Generated by aiopylgtv
    # Display: Unspecified
    # DM Version:\x20
    PictureMode = 2
    Tmax = {white_level:#.15g}
    Tmin = {black_level:#.15g}
    Tgamma = {gamma:#.2g}
    ColorPrimaries = {xr:.4f} {yr:.4f} {xg:.4f} {yg:.4f} {xb:.4f} {yb:.4f} {xw:.4f} {yw:.4f}
    TLMS2RGBmat = {tlms2rgb[0]:#.15g} {tlms2rgb[1]:#.15g} {tlms2rgb[2]:#.15g} {tlms2rgb[3]:#.15g} {tlms2rgb[4]:#.15g} {tlms2rgb[5]:#.15g} {tlms2rgb[6]:#.15g} {tlms2rgb[7]:#.15g} {tlms2rgb[8]:#.15g}
    """

        elif version == 2019:
            config = f"""# Dolby Vision User Display Configuration File
    # Generated by aiopylgtv
    # Display: Unspecified
    # DM Version:\x20
    [PictureMode = 2]
    Tmax = {white_level:#.15g}
    Tmin = {black_level:#.15g}
    Tgamma = {gamma:#.2g}
    TPrimaries = {xr:.4f} {yr:.4f} {xg:.4f} {yg:.4f} {xb:.4f} {yb:.4f} {xw:.4f} {yw:.4f}
    """
        else:
            raise ValueError(
                f"Invalid dolby vision config version {version}, valid options are 2018 or 2019"
            )

        config = config.replace("\n", "\r\n")
        return config


    def write_dolby_vision_config(
        version=2019,
        white_level=700.0,
        black_level=0.0,
        gamma=2.2,
        primaries=BT2020_PRIMARIES,
    ):

        config = create_dolby_vision_config(
            version=version,
            white_level=white_level,
            black_level=black_level,
            gamma=gamma,
            primaries=primaries,
        )

        filename = DV_CONFIG_FILENAMES[version]

        with open(filename, "w") as f:
            f.write(config)
