#!/usr/bin/env python3
"""derive-bt709-weights.py: derives the grey weights the film uses (0.2126, 0.7152, 0.0722) from first principles.
Input: the chromaticities of the Rec. ITU-R BT.709 primaries (the primaries Godot says it uses, and sRGB shares) and the D65 white point.
Method: solve for the RGB -> XYZ matrix whose columns are the primaries scaled so that R = G = B = 1 gives the white point; the Y row is the weights.
No Godot involved. Run: python3 derive-bt709-weights.py"""
import numpy as np
xy = {"R": (0.640, 0.330), "G": (0.300, 0.600), "B": (0.150, 0.060)}
white_xy = (0.3127, 0.3290)          # D65
def XYZ(x, y): return np.array([x / y, 1.0, (1 - x - y) / y])
P = np.stack([XYZ(*xy[c]) for c in "RGB"], axis=1)       # columns: unscaled primaries with Y = 1
W = XYZ(*white_xy)                                        # white with Y = 1
S = np.linalg.solve(P, W)                                 # scale of each primary
M = P * S                                                 # RGB -> XYZ
print("Y row (the weights):", [round(float(v), 4) for v in M[1]], " sum =", round(float(M[1].sum()), 6))
