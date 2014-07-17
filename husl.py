import operator
import math

__version__ = "3.0.0"


m = [
    [ 3.240454162114103, -1.537138512797715, -0.49853140955601 ],
    [ -0.96926603050518, 1.876010845446694,  0.041556017530349 ],
    [ 0.055643430959114, -0.20402591351675,  1.057225188223179 ]
]
m_inv = [
    [ 0.41245643908969,  0.3575760776439,  0.18043748326639  ],
    [ 0.21267285140562,  0.71515215528781, 0.072174993306559 ],
    [ 0.019333895582329, 0.1191920258813,  0.95030407853636  ]
]

# Hard-coded D65 illuminant
refX = 0.95047
refY = 1.00000
refZ = 1.08883
refU = (4 * refX) / (refX + (15 * refY) + (3 * refZ))
refV = (9 * refY) / (refX + (15 * refY) + (3 * refZ))


kappa = 24389.0 / 27
epsilon = 216.0 / 24389


# Public API

def husl_to_rgb(h, s, l):
    return lch_to_rgb(*husl_to_lch([h, s, l]))


def husl_to_hex(h, s, l):
    return rgb_to_hex(husl_to_rgb(h, s, l))


def rgb_to_husl(r, g, b):
    return lch_to_husl(rgb_to_lch(r, g, b))


def hex_to_husl(hex):
    return rgb_to_husl(*hex_to_rgb(hex))


def huslp_to_rgb(h, s, l):
    return lch_to_rgb(*huslp_to_lch([h, s, l]))


def huslp_to_hex(h, s, l):
    return rgb_to_hex(huslp_to_rgb(h, s, l))


def rgb_to_huslp(r, g, b):
    return lch_to_huslp(rgb_to_lch(r, g, b))


def hex_to_huslp(hex):
    return rgb_to_huslp(*hex_to_rgb(hex))


def lch_to_rgb(l, c, h):
    return xyz_to_rgb(luv_to_xyz(lch_to_luv([l, c, h])))


def rgb_to_lch(r, g, b):
    return luv_to_lch(xyz_to_luv(rgb_to_xyz([r, g, b])))


def max_chroma(L, H):
    hrad = math.radians(H)
    sinH = (math.sin(hrad))
    cosH = (math.cos(hrad))
    sub1 = (math.pow(L + 16, 3.0) / 1560896.0)
    sub2 = sub1 if sub1 > epsilon else (L / kappa)
    result = float("inf")
    for row in m:
        m1 = row[0]
        m2 = row[1]
        m3 = row[2]

        top = (12739311 * m3 + 11700000 * m2 + 11120499 * m1) * sub2
        rbottom = 9608480 * m3 - 1921696 * m2
        lbottom = 1441272 * m3 - 4323816 * m1

        bottom = (rbottom * sinH + lbottom * cosH) * sub2

        for limit in (0.0, 1.0):
            C = L * (top - 11700000 * limit) / (bottom + 1921696 * sinH * limit)

            # TODO: GET RID OF THIS SHIT
            if C > 0.0 and C < result:
                result = C
    return result


def _hrad_extremum(L):
    lhs = (math.pow(L, 3.0) + 48.0 * math.pow(L, 2.0) + 768.0 * L + 4096.0) / 1560896.0
    rhs = epsilon
    sub = lhs if lhs > rhs else L / kappa

    chroma = float("inf")
    result = None
    for row in m:
        for limit in (0.0, 1.0):
            [m1, m2, m3] = row
            top = (20 * m3 - 4 * m2) * sub + 4 * limit
            bottom = (3 * m3 - 9 * m1) * sub
            hrad = math.atan2(top, bottom)
            # This is a math hack to deal with tan quadrants, I'm too lazy to figure
            # out how to do this properly
            if limit == 1.0:
                hrad += math.pi
            test = max_chroma(L, math.degrees(hrad))
            if test < chroma:
                chroma = test
                result = hrad
    return result


def max_chroma_pastel(L):
    H = math.degrees(_hrad_extremum(L))
    return max_chroma(L, H)


def dot_product(a, b):
    return sum(map(operator.mul, a, b))


def f(t):
    if t > epsilon:
        return 116 * math.pow((t / refY), 1.0 / 3.0) - 16.0
    else:
        return (t / refY) * kappa


def f_inv(t):
    if t > 8:
        return refY * math.pow((t + 16.0) / 116.0, 3.0)
    else:
        return refY * t / kappa


def from_linear(c):
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return (1.055 * math.pow(c, 1.0 / 2.4) - 0.055)


def to_linear(c):
    a = 0.055

    if c > 0.04045:
        return (math.pow((c + a) / (1.0 + a), 2.4))
    else:
        return (c / 12.92)


def rgb_prepare(triple):
    ret = []
    for ch in triple:
        ch = round(ch, 3)

        if ch < -0.0001 or ch > 1.0001:
            raise Exception("Illegal RGB value %f" % ch)

        if ch < 0:
            ch = 0
        if ch > 1:
            ch = 1

        # Fix for Python 3 which by default rounds 4.5 down to 4.0
        # instead of Python 2 which is rounded to 5.0 which caused
        # a couple off by one errors in the tests. Tests now all pass
        # in Python 2 and Python 3
        ret.append(round(ch * 255 + 0.001, 0))

    return ret


def hex_to_rgb(hex):
    if hex.startswith('#'):
        hex = hex[1:]
    r = int(hex[0:2], 16) / 255.0
    g = int(hex[2:4], 16) / 255.0
    b = int(hex[4:6], 16) / 255.0
    return [r, g, b]


def rgb_to_hex(triple):
    [r, g, b] = triple
    return '#%02x%02x%02x' % tuple(rgb_prepare([r, g, b]))


def xyz_to_rgb(triple):
    xyz = map(lambda row: dot_product(row, triple), m)
    return list(map(from_linear, xyz))


def rgb_to_xyz(triple):
    rgbl = list(map(to_linear, triple))
    return list(map(lambda row: dot_product(row, rgbl), m_inv))


def xyz_to_luv(triple):
    X, Y, Z = triple

    if X == Y == Z == 0.0:
        return [0.0, 0.0, 0.0]

    varU = (4.0 * X) / (X + (15.0 * Y) + (3.0 * Z))
    varV = (9.0 * Y) / (X + (15.0 * Y) + (3.0 * Z))
    L = f(Y)

    # Black will create a divide-by-zero error
    if L == 0.0:
        return [0.0, 0.0, 0.0]

    U = 13.0 * L * (varU - refU)
    V = 13.0 * L * (varV - refV)

    return [L, U, V]


def luv_to_xyz(triple):
    L, U, V = triple

    if L == 0:
        return [0.0, 0.0, 0.0]

    varY = f_inv(L)
    varU = U / (13.0 * L) + refU
    varV = V / (13.0 * L) + refV
    Y = varY * refY
    X = 0.0 - (9.0 * Y * varU) / ((varU - 4.0) * varV - varU * varV)
    Z = (9.0 * Y - (15.0 * varV * Y) - (varV * X)) / (3.0 * varV)

    return [X, Y, Z]


def luv_to_lch(triple):
    L, U, V = triple

    C = (math.pow(math.pow(U, 2) + math.pow(V, 2), (1.0 / 2.0)))
    hrad = (math.atan2(V, U))
    H = math.degrees(hrad)
    if H < 0.0:
        H = 360.0 + H

    return [L, C, H]


def lch_to_luv(triple):
    L, C, H = triple

    Hrad = math.radians(H)
    U = (math.cos(Hrad) * C)
    V = (math.sin(Hrad) * C)

    return [L, U, V]


def husl_to_lch(triple):
    H, S, L = triple

    if L > 99.9999999:
        return [100, 0.0, H]
    if L < 0.00000001:
        return [0.0, 0.0, H]

    mx = max_chroma(L, H)
    C = mx / 100.0 * S

    return [L, C, H]


def lch_to_husl(triple):
    L, C, H = triple

    if L > 99.9999999:
        return [H, 0.0, 100.0]
    if L < 0.00000001:
        return [H, 0.0, 0.0]

    mx = max_chroma(L, H)
    S = C / mx * 100.0

    return [H, S, L]


def huslp_to_lch(triple):
    H, S, L = triple

    if L > 99.9999999:
        return [100, 0.0, H]
    if L < 0.00000001:
        return [0.0, 0.0, H]

    mx = max_chroma_pastel(L)
    C = mx / 100.0 * S

    return [L, C, H]


def lch_to_huslp(triple):
    L, C, H = triple

    if L > 99.9999999:
        return [H, 0.0, 100.0]
    if L < 0.00000001:
        return [H, 0.0, 0.0]

    mx = max_chroma_pastel(L)
    S = C / mx * 100.0

    return [H, S, L]
