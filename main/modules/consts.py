import numpy as np

# color consts
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
BROWN = (153, 76, 0)
DGREEN = (0, 153, 0)
GREEN = (0, 204, 0)
LGREEN = (0, 255, 0)
CYAN = (0, 102, 204)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
PURPLE = (127, 0, 255)
# Color dictionary:
color_dictionary = {
    1: ("Unclassified", GRAY),
    2: ("Ground", BROWN),
    3: ("Low Vegetation", DGREEN),
    4: ("Medium Vegetation", GREEN),
    5: ("High Vegetation", LGREEN),
    6: ("Building", CYAN),
    7: ("Low point (low noise)", RED),
    8: ("Model Key (reserved)", YELLOW),
    9: ("Water", BLUE),
    12: ("Overlap/Reserved", ORANGE),
    17: ("Bridge Deck", PURPLE),
    41: ("Reserved", ORANGE),
}

# GeoUtils consts. See more at https://www.linz.govt.nz/data/geodetic-services/coordinate-conversion/projection
# -conversions/transverse-mercator-transformation-formulae semi-major axis of reference ellipsoid GRS80 (see
# https://www.linz.govt.nz/data/geodetic-system/datums-projections-and-heights/geodetic-datums/reference-ellipsoids)
A = 6378137
# ellipsoidal flattening (1-b/a), b-semi-minor axis of reference ellipsoid
F = 1 / 298.257222101
# origin latitude (долгота, 0y, 0 на экваторе)
PHI_CONST = 0
# origin longitude (широта, 0x, 0 в Гринвиче)
LAMBDA_CONST = 173 * np.pi / 180
# false Northing (смещение по 0y)
N_CONST = 10000000
# false Easting (смещение по 0x)
E_CONST = 1600000
# central meridian scale factor. See more at
# http://www.geography.hunter.cuny.edu/~jochen/gtech361/lectures/lecture04/concepts/Map%20coordinate%20systems/Projection%20parameters.htm#:~:text=The%20central%20meridian%20has%20a,of%20distortion%20within%20the%20zone.
K_CONST = 0.9996
# additional consts
B = A * (1 - F)
ECC = 2 * F - F ** 2
# A0 = 1-(ecc/4)-3*(ecc**2/64)-5*(ecc**3/256)
# A2 = 3/8*(ecc+(ecc**2/4)+15*(ecc**3/128))
# A4 = 15/256*(ecc**2+3*(ecc**3/4))
# A6 = 35*(ecc**3/3072)
M_PHI_CONST = 0
N = (A - B) / (A + B)
G = A * (1 - N) * (1 - N ** 2) * (1 + 9 * (N ** 2 / 4) + 225 * (N ** 4 / 64))

LAT_1M = 90 / 10_000_000
LON_1M = 111_319.488
