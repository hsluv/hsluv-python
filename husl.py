import operator
import math

__version__ = "2.0.1"


m = [
    [3.2406, -1.5372, -0.4986],
    [-0.9689, 1.8758, 0.0415],
    [0.0557, -0.2040, 1.0570]
]

m_inv = [
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505]
]

# Hard-coded D65 illuminant
refX = 0.95047
refY = 1.00000
refZ = 1.08883
refU = 0.19784
refV = 0.46834
lab_e = 0.008856
lab_k = 903.3

def husl_to_rgb(h, s, l):
    return XYZ_RGB(LUV_XYZ(LCH_LUV(HUSL_LCH([h, s, l]))))

def husl_to_hex(h, s, l):
    return '#%02x%02x%02x' % tuple(rgb_prepare(husl_to_rgb(h, s, l)))

def rgb_to_husl(r, g, b):
    return LCH_HUSL(LUV_LCH(XYZ_LUV(RGB_XYZ([r, g, b]))))

def hex_to_husl(hex):
    if hex.startswith('#'): hex = hex[1:]
    r = int(hex[0:2], 16) / 255.0
    g = int(hex[2:4], 16) / 255.0
    b = int(hex[4:6], 16) / 255.0
    return rgb_to_husl(r, g, b)

def maxChroma(L, H):
    _ref = [0.0, 1.0]

    hrad = ((H / 360.0) * 2 * math.pi)
    sinH = (math.sin(hrad))
    cosH = (math.cos(hrad))
    sub1 = (math.pow(L + 16, 3) / 1560896.0)
    sub2 = sub1 if sub1 > 0.008856 else (L / 903.3)
    result = float("inf")
    for row in m:
        m1 = row[0]
        m2 = row[1]
        m3 = row[2]
        top = ((0.99915 * m1 + 1.05122 * m2 + 1.14460 * m3) * sub2)
        rbottom = (0.86330 * m3 - 0.17266 * m2)
        lbottom = (0.12949 * m3 - 0.38848 * m1)
        bottom = (rbottom * sinH + lbottom * cosH) * sub2

        for t in _ref:
            C = (L * (top - 1.05122 * t) / (bottom + 0.17266 * sinH * t))
            if C > 0 and C < result:
                result = C
    return result

def dot_product(a, b):
    return sum(map(operator.mul, a, b))

def f(t):
    if t > lab_e:
        return (math.pow(t, 1.0 / 3.0))
    else:
        return (7.787 * t + 16 / 116.0)

def f_inv(t):
    if math.pow(t, 3) > lab_e:
        return (math.pow(t, 3))
    else:
        return (116 * t - 16) / lab_k

def from_linear(c):
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return (1.055 * math.pow(c, 1 / 2.4) - 0.055)

def to_linear(c):
    a = 0.055

    if c > 0.04045:
        return (math.pow((c + a) / (1 + a), 2.4))
    else:
        return (c / 12.92)

def rgb_prepare(triple):
    ret = []
    for ch in triple:
        ch = round(ch, 3)

        if ch < -0.0001 or ch > 1.0001:
            raise Exception("Illegal RGB value %f" % ch)
            
        if ch < 0: ch = 0
        if ch > 1: ch = 1

        ret.append(round(ch * 255, 0))

    return ret

def XYZ_RGB(triple):
    xyz = map(lambda row: dot_product(row, triple), m)
    return map(from_linear, xyz)

def RGB_XYZ(triple):
    rgbl = map(to_linear, triple)
    return map(lambda row: dot_product(row, rgbl), m_inv)

def XYZ_LUV(triple):
    X, Y, Z = triple
    
    if X == 0 and Y == 0 and Z == 0: return [0, 0, 0]

    varU = (4 * X) / (X + (15.0 * Y) + (3 * Z))
    varV = (9 * Y) / (X + (15.0 * Y) + (3 * Z))
    L = 116.0 * f(Y / refY) - 16

    # Black will create a divide-by-zero error
    if L == 0: return [0, 0, 0]

    U = 13 * L * (varU - refU)
    V = 13 * L * (varV - refV)

    return [L, U, V]

def LUV_XYZ(triple):
    L, U, V = triple

    if L == 0: return [0, 0, 0]

    varY = f_inv((L + 16) / 116.0)
    varU = U / (13.0 * L) + refU
    varV = V / (13.0 * L) + refV
    Y = varY * refY
    X = 0 - (9 * Y * varU) / ((varU - 4.0) * varV - varU * varV)
    Z = (9 * Y - (15 * varV * Y) - (varV * X)) / (3.0 * varV)

    return [X, Y, Z]

def LUV_LCH(triple):
    L, U, V = triple

    C = (math.pow(math.pow(U, 2) + math.pow(V, 2), (1 / 2.0)))
    Hrad = (math.atan2(V, U))
    H = (Hrad * 360.0 / 2.0 / math.pi)
    if H < 0:
        H = 360 + H

    return [L, C, H]

def LCH_LUV(triple):
    L, C, H = triple

    Hrad = (H / 360.0 * 2.0 * math.pi)
    U = (math.cos(Hrad) * C)
    V = (math.sin(Hrad) * C)

    return [L, U, V]

def HUSL_LCH(triple):
    H, S, L = triple

    if L > 99.9999999: return [100, 0, H]
    if L < 0.00000001: return [0, 0, H]

    mx = maxChroma(L, H)
    C = mx / 100.0 * S

    return [L, C, H]

def LCH_HUSL(triple):
    L, C, H = triple

    if L > 99.9999999: return [H, 0, 100]
    if L < 0.00000001: return [H, 0, 0]
    
    mx = maxChroma(L, H)
    S = C / mx * 100

    return [H, S, L]
