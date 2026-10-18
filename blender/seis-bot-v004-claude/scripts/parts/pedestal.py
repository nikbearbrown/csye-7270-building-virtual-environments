"""pedestal - the classical three-part stone plinth of the Thinker pose + the pale dais it stands on (NOT part of the rigged
robot; every object is 'static').  Dimensions from spec/ONMODEL.md section 4 (frames 01/02), metres:

    dais    1.29 wide, 0.04 thick, pale cream slab (material "dais")
    base    0.633 wide, 0.150 tall, three courses (bottom course, fillet + groove, chamfered course)
    shaft   0.499 wide, 0.193 tall, plain smooth face
    cap     0.530 wide, 0.059 tall, chamfered lip + thin top strip
    total plinth height 0.402 (= 0.75 U with U = shin length 0.536)
Square footprint.  build(center=(x, y), dais_center=None) puts the plinth centre at `center` standing on the dais top
(z = DAIS_T); returns the objects.  The seated figure's feet stand on the dais top (z = DAIS_T).
"""
import math
import seis_lib as L
import seis_spec as S
from mathutils import Vector

DAIS_T = 0.04
DAIS_W = 1.29
BASE_W, BASE_H = 0.633, 0.150
SHAFT_W, SHAFT_H = 0.499, 0.193
CAP_W, CAP_H = 0.530, 0.059


def dims():
    U = (S.J("knee.L") - S.J("ankle.L")).length
    return {"U": U, "height": BASE_H + SHAFT_H + CAP_H, "base_w": BASE_W, "shaft_w": SHAFT_W, "cap_w": CAP_W,
            "depth": CAP_W, "width": CAP_W, "dais_t": DAIS_T}


def _frustum(name, w0, w1, h, z0, cx, cy):
    """Square frustum (w0 at the bottom, w1 at the top)."""
    fr = L.Frame((cx, cy, z0 + h / 2), (math.cos(math.pi / 4), math.sin(math.pi / 4), 0),
                 (-math.sin(math.pi / 4), math.cos(math.pi / 4), 0), (0, 0, 1))
    return L.cylinder(name, w0 / math.sqrt(2), h, fr, segments=4, radius2=w1 / math.sqrt(2))


def build(top_z=None, center=(0.0, 0.0), dais_center=None, seat_z=None):
    """seat_z: if given, the shaft is lengthened/shortened (max 2 cm) so the cap top lands exactly on that height."""
    cx, cy = center
    objs = []
    shaft_h = SHAFT_H
    if seat_z is not None:
        shaft_h = SHAFT_H + max(-0.02, min(0.02, seat_z - (DAIS_T + BASE_H + SHAFT_H + CAP_H)))
    dc = dais_center or (cx, cy - 0.20)
    dais = L.box("block_dais", (DAIS_W, DAIS_W, DAIS_T), L.Frame((dc[0], dc[1], DAIS_T / 2)))
    L.finish(dais, "dais", bevel=0.003, bevel_segments=2, angle=30, weighted=False)
    objs.append(dais)
    z = DAIS_T
    # base: bottom course, fillet, groove neck, chamfered course
    c1 = L.box("block_base_course1", (BASE_W, BASE_W, 0.058), L.Frame((cx, cy, z + 0.029)))
    L.finish(c1, "stone", bevel=0.005, bevel_segments=2, angle=30, weighted=False)
    z += 0.058
    c2 = L.box("block_base_fillet", (BASE_W - 0.034, BASE_W - 0.034, 0.030), L.Frame((cx, cy, z + 0.015)))
    L.finish(c2, "stone", bevel=0.010, bevel_segments=3, angle=30, weighted=False)
    z += 0.030
    c3 = L.box("block_base_groove", (BASE_W - 0.080, BASE_W - 0.080, 0.014), L.Frame((cx, cy, z + 0.007)))
    L.finish(c3, "stone", bevel=0.002, bevel_segments=1, angle=30, weighted=False)
    z += 0.014
    c4 = _frustum("block_base_chamfer", BASE_W - 0.060, SHAFT_W + 0.020, BASE_H - 0.058 - 0.030 - 0.014, z, cx, cy)
    L.finish(c4, "stone", bevel=0.003, bevel_segments=2, angle=30, weighted=False)
    z += BASE_H - 0.058 - 0.030 - 0.014
    shaft = L.box("block_shaft", (SHAFT_W, SHAFT_W, shaft_h), L.Frame((cx, cy, z + shaft_h / 2)))
    L.finish(shaft, "stone", bevel=0.004, bevel_segments=2, angle=30, weighted=False)
    z += shaft_h
    under = L.box("block_cap_under", (CAP_W - 0.030, CAP_W - 0.030, 0.014), L.Frame((cx, cy, z + 0.007)))
    L.finish(under, "stone", bevel=0.002, bevel_segments=1, angle=30, weighted=False)
    z += 0.014
    cap = L.box("block_cap", (CAP_W, CAP_W, CAP_H - 0.014), L.Frame((cx, cy, z + (CAP_H - 0.014) / 2)))
    L.finish(cap, "stone", bevel=0.009, bevel_segments=3, angle=30, weighted=False)
    objs += [c1, c2, c3, c4, shaft, under, cap]
    for o in objs:
        o["static"] = True
    return objs
