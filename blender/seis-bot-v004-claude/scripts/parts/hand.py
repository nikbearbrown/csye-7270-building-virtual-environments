"""hand - the SEIS bot hand (left built at J("wrist.L"), then mirrored).

4 fingers x 3 capsule phalanges + a thumb (pod + 2 phalanges) = 15 separate finger meshes per hand, each with its own
bone and its origin on its proximal hinge.  Round 2 adds, as SEPARATE meshes: stepped bearing washers + hex bolts at every hinge,
pointed claw caps, overlapping dorsal plates with a dark groove, knuckle bolts, a split back-of-hand shield (shield, groove,
panel, ridge, gold lip, bolts), three palm slats, three thumb bearings, side plates, cable clamps and a 5-part wrist socket
(about 67 meshes per hand, about 134 for both).

HAND-LOCAL FRAME (origin = wrist axis):  +x = palm normal (towards the thigh), +y = towards the little finger
(= world +Y, backwards), +z = along the forearm, down the fingers.
"""
import math
import os
import bpy
from mathutils import Vector, Matrix

import seis_lib as L
import seis_spec as S
import hand_geo as G
from hand_geo import TEAL, DARK, BRONZE, SILVER, DISC
FLOOR = DISC

# ------------------------------------------------------------------------------------------------------------ finish
# On-model frames (spec/onmodel_limbs.md): the hand is CLEAN glossy dark gunmetal with only a thin gold edge line.  The shared
# SEIS_teal carries heavy craquelure and bronze wear that the frames do not show, so this module makes its own two finishes
# (named SEIS_handgm / SEIS_handgold; seis_lib.mat() finds them by name).  Slot order: TEAL=gunmetal, BRONZE=gold.
G.SLOTS[:] = ["handgm", "dark", "handgold", "silver", "darkdisc"]


def _hex(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    c = [((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c]
    return (c[0], c[1], c[2], 1.0)


def ensure_materials():
    import seis_mat as M
    if bpy.data.materials.get("SEIS_handgm") is None:
        m, nt, b, out = M._fresh("SEIS_handgm")
        nb = M._NB(nt)
        geo = nb.n("ShaderNodeNewGeometry")
        bev = nb.n("ShaderNodeBevel", samples=12)
        bev.inputs["Radius"].default_value = 0.0010
        dot = nb.n("ShaderNodeVectorMath", operation="DOT_PRODUCT")
        nt.links.new(bev.outputs["Normal"], dot.inputs[0])
        nt.links.new(geo.outputs["Normal"], dot.inputs[1])
        edge = nb.maprange(dot.outputs["Value"], 0.9992, 0.975, 0.0, 1.0)
        lw = nb.n("ShaderNodeLayerWeight")
        lw.inputs["Blend"].default_value = 0.5
        paint = nb.mixc(lw.outputs["Facing"], _hex("#22271D"), _hex("#12150F"))       # ON-MODEL gunmetal #1A1F18, olive-neutral
        col = nb.mixc(nb.math("MULTIPLY", edge, 0.24, clamp=True), paint, _hex("#B4B9AE"))   # pale chrome edge glint, no gold
        nt.links.new(col, b.inputs["Base Color"])
        nt.links.new(nb.mixf(edge, 0.58, 0.90), b.inputs["Metallic"])
        nt.links.new(nb.mixf(edge, 0.30, 0.36), b.inputs["Roughness"])
        b.inputs["Coat Weight"].default_value = 0.32
        b.inputs["Coat Roughness"].default_value = 0.06
        m.diffuse_color = _hex("#1F2A22")
    if bpy.data.materials.get("SEIS_handgold") is None:
        m, nt, b, out = M._fresh("SEIS_handgold")
        b.inputs["Base Color"].default_value = _hex("#B59B62")
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Roughness"].default_value = 0.36
        m.diffuse_color = _hex("#B59B62")

# ------------------------------------------------------------------------------------------------------------ numbers
M_LEN = 0.121                 # open middle-finger length (m)  ~ 0.44 H ;  palm 0.092 -> hand open ~0.80 H
SPLIT = (0.42, 0.32, 0.26)    # proximal / middle / distal share of a finger (spec 2)
PALM_Z = 0.092                # wrist axis -> knuckle line
W_WRIST, W_KNUCK = 0.067, 0.088

# name, y centre, pitch width, thickness, mcp z, length factor, (mcp, pip, dip) deg, splay deg
FINGERS = [
    ("index",  -0.0318, 0.0222, 0.0178, 0.091, 0.95, (36, 63, 32), -3.0),
    ("middle", -0.0095, 0.0222, 0.0182, 0.093, 1.00, (40, 68, 34), 0.0),
    ("ring",    0.0127, 0.0212, 0.0172, 0.090, 0.95, (43, 71, 36), 2.5),
    ("pinky",   0.0330, 0.0192, 0.0158, 0.084, 0.80, (47, 74, 38), 6.0),
]


def _hand_frame():
    o = S.J("wrist.L")
    d = (S.J("wrist.L") - S.J("elbow.L")).normalized()          # forearm direction
    n = Vector((-1, 0, 0))
    n = (n - d * n.dot(d)).normalized()
    y = d.cross(n)
    return L.Frame(o, n, y, d)


HF = _hand_frame()


def W(lx=0.0, ly=0.0, lz=0.0):
    """hand-local point -> world"""
    return HF.p(lx, ly, lz)


def Wd(v):
    return HF.d(v[0], v[1], v[2])


def seg_frame(pos, X, Y, Z):
    """world Frame for a local frame (hand-local vectors)"""
    return L.Frame(W(*pos), Wd(X), Wd(Y), Wd(Z))


# ------------------------------------------------------------------------------------------------------------ phalanx
SUP = lambda s: G.ring_super(s["w"] / 2, s["t"] / 2, 24, 2.25)

HW = dict(bevel=0.0004, segs=1)          # make() settings for tiny hardware meshes


def _barrel(P, pw, T, rad=0.46):
    """hinge barrel (gunmetal knuckle roll closing the wedge opened when the finger flexes)."""
    bl = 0.94 * pw
    P.cyl((0, 0, 0), (0, 1, 0), rad * T, bl, TEAL, segments=16, xhint=(1, 0, 0))
    return bl


def _caps(Lj, wp, tp, zs, wf, tf):
    return [dict(z=z, w=wp * a, t=tp * b) for z, a, b in zip(zs, wf, tf)]


# phalanx section tables (z as a fraction of Lj except the two end stations)
def _tabs(j, Lj):
    if j < 2:
        zs = [0.0025, 0.0062, 0.30 * Lj, 0.64 * Lj, Lj - 0.0058, Lj - 0.0008]
        wf = [0.90, 1.0, 1.03, 1.0, 0.97, 0.97]
        tf = [0.84, 0.96, 1.0, 0.98, 0.94, 0.94]
    else:
        zs = [0.0025, 0.0062, 0.28 * Lj, 0.55 * Lj, 0.80 * Lj, Lj]
        wf = [0.90, 1.0, 1.0, 0.93, 0.72, 0.40]
        tf = [0.84, 0.97, 1.0, 0.92, 0.72, 0.46]
    return zs, wf, tf


def _dims(j, Wn, T):
    if j == 0:
        return 0.97 * Wn, T
    if j == 1:
        return 0.945 * Wn, 0.93 * T
    return 0.94 * Wn, 0.88 * T


def phalanx(name, bone, frame, origin, j, Lj, Wn, T):
    """One phalanx: smooth rounded capsule plate (frame 06 / 04), hairline gaps, no gold band."""
    P = G.Part()
    wp, tp = _dims(j, Wn, T)
    zs, wf, tf = _tabs(j, Lj)
    if j < 2:
        P.loft(_caps(Lj, wp, tp, zs, wf, tf), TEAL, ring_fn=SUP)
    else:
        P.loft(_caps(Lj, wp, tp, zs, wf, tf), TEAL, ring_fn=SUP, tip=(0, 0, 0.0060))
    _barrel(P, wp, T)
    return P.make(name, frame, origin, bone, wear=0.0, bevel=0.0018, segs=3)


def finger_hardware(name, bone, frame, origin, j, Lj, Wn, T, outer):
    """Hinge hardware of phalanx j as its own mesh: a stepped washer + hex bolt on the dorsal face just before the next hinge,
    and (outer fingers only) a bearing washer + bolt on the outer end of this phalanx's own hinge barrel.  outer = -1 (index),
    +1 (pinky) or 0."""
    P = G.Part()
    wp, tp = _dims(j, Wn, T)
    rw = min(0.0033, 0.165 * Wn)
    n = 0
    if j < 2:
        P.washer_bolt((-tp * 0.47, 0, Lj - 0.0050), (-1, 0, 0), r_wash=rw, r_mid=rw * 0.76, r_hex=rw * 0.52)
        n += 1
    if outer:
        bl = 0.94 * wp
        P.washer_bolt((0, outer * bl / 2, 0), (0, outer, 0), r_wash=rw * 1.15, r_mid=rw * 0.85, r_hex=rw * 0.6, xhint=(1, 0, 0))
        n += 1
    if not n:
        return None
    return P.make(name, frame, origin, bone, wear=0.0, **HW)


def finger_claw(name, bone, frame, origin, Lj, Wn, T):
    """Pointed dark claw cap over the last 50% of the distal phalanx (frame 06: tips are pointed dark claws)."""
    P = G.Part()
    wp, tp = _dims(2, Wn, T)
    zs, wf, tf = _tabs(2, Lj)
    zz = [0.50 * Lj, 0.60 * Lj, 0.72 * Lj, 0.84 * Lj, 0.94 * Lj]
    st = [dict(z=z, w=wp * _lerp(list(zip(zs, wf)), z) * 1.075 + 0.0004, t=tp * _lerp(list(zip(zs, tf)), z) * 1.10 + 0.0004) for z in zz]
    P.loft(st, DISC, ring_fn=SUP, tip=(0, 0, 0.0085))
    return P.make(name, frame, origin, bone, wear=0.0, bevel=0.0007, segs=2)


def finger_plate(name, bone, frame, origin, j, Lj, Wn, T):
    """Overlapping dorsal cover plate on a phalanx: dark groove oval + raised island (separate mesh)."""
    P = G.Part()
    wp, tp = _dims(j, Wn, T)
    ox = -tp * 0.497
    zm, hl = 0.52 * Lj, 0.30 * Lj
    P.oval_pad(zm, hl + 0.0008, wp * 0.60 + 0.0010, 0.0014, ox, DISC)
    P.oval_pad(zm, hl, wp * 0.60, 0.0020, ox, TEAL)
    return P.make(name, frame, origin, bone, wear=0.0, bevel=0.0005, segs=2)


def build_finger(fname, ycen, Wn, T, mcp_z, lf, angs, splay):
    objs = []
    sp = math.radians(splay)
    X0 = Vector((1, 0, 0))
    Y0 = Vector((0, math.cos(sp), -math.sin(sp)))
    Z0 = Vector((0, math.sin(sp), math.cos(sp)))
    pos = Vector((0.0, ycen, mcp_z))
    a = 0.0
    lens = [M_LEN * lf * k for k in SPLIT]
    outer = {"index": -1, "pinky": 1}.get(fname, 0)
    for j in range(3):
        a += math.radians(angs[j])
        Xi = X0 * math.cos(a) - Z0 * math.sin(a)
        Zi = Z0 * math.cos(a) + X0 * math.sin(a)
        fr = seg_frame(pos, Xi, Y0, Zi)
        bone = f"{fname}{j + 1}.L"
        objs.append(phalanx(f"hand_{fname}{j + 1}.L", bone, fr, fr.o, j, lens[j], Wn, T))
        hw = finger_hardware(f"hand_{fname}_hinge{j + 1}.L", bone, fr, fr.o, j, lens[j], Wn, T, outer)
        if hw:
            objs.append(hw)
        if j == 0:
            objs.append(finger_plate(f"hand_{fname}_plate{j + 1}.L", bone, fr, fr.o, j, lens[j], Wn, T))
        if j == 2:
            objs.append(finger_claw(f"hand_{fname}_claw.L", bone, fr, fr.o, lens[j], Wn, T))
        pos = pos + Zi * lens[j]
    return objs


# ------------------------------------------------------------------------------------------------------------ thumb
def _unit(v):
    return Vector(v).normalized()


def build_thumb():
    objs = []
    base = Vector((0.0045, -0.0385, 0.020))
    ventral = _unit((0.42, 0.90, 0.0))
    d = _unit((0.30, -0.42, 0.85))                         # pod axis: ~40 deg off the finger line, in and forward
    lens = [0.038, 0.028, 0.027]
    widths = [0.030, 0.025, 0.022]
    thick = [0.027, 0.023, 0.021]
    curls = [0.0, 22.0, 28.0]
    pos = base
    for i in range(3):
        if i > 0:
            vperp = (ventral - d * ventral.dot(d)).normalized()
            ang = math.radians(curls[i])
            d = (d * math.cos(ang) + vperp * math.sin(ang)).normalized()
        xh = (ventral - d * ventral.dot(d)).normalized()   # local +x (palm / ventral face)
        yv = d.cross(xh)
        fr = seg_frame(pos, xh, yv, d)
        bone = f"thumb{i + 1}.L"
        objs.append(thumb_seg(f"hand_thumb{i + 1}.L", bone, fr, fr.o, i, lens[i], widths[i], thick[i]))
        objs += thumb_extras(i, bone, fr, lens[i], widths[i], thick[i])
        pos = pos + d * lens[i]
    return objs


def thumb_seg(name, bone, frame, origin, i, Lj, Wn, T):
    P = G.Part()
    if i == 0:       # metacarpal pod
        zs = [0.0030, 0.0085, 0.30 * Lj, 0.62 * Lj, Lj - 0.0064, Lj - 0.0008]
        wf = [0.86, 1.0, 1.06, 1.0, 0.95, 0.95]
        tf = [0.84, 1.0, 1.06, 1.0, 0.92, 0.92]
        P.loft(_caps(Lj, Wn, T, zs, wf, tf), TEAL, ring_fn=SUP)
    elif i == 1:
        zs = [0.0025, 0.0062, 0.30 * Lj, 0.62 * Lj, Lj - 0.0058, Lj - 0.0008]
        wf = [0.90, 1.0, 1.03, 1.0, 0.97, 0.97]
        tf = [0.86, 0.97, 1.0, 0.98, 0.95, 0.95]
        P.loft(_caps(Lj, Wn, T, zs, wf, tf), TEAL, ring_fn=SUP)
    else:            # distal: round pad tip
        zs = [0.0025, 0.0062, 0.30 * Lj, 0.62 * Lj, 0.86 * Lj, Lj]
        wf = [0.90, 1.0, 1.0, 0.94, 0.80, 0.56]
        tf = [0.86, 0.98, 1.0, 0.94, 0.80, 0.58]
        P.loft(_caps(Lj, Wn, T, zs, wf, tf), TEAL, ring_fn=SUP, tip=(0, 0, 0.0030))
    _barrel(P, Wn, T, rad=0.45)
    return P.make(name, frame, origin, bone, wear=0.0, bevel=0.0010, segs=2)


def thumb_extras(i, bone, fr, Lj, Wn, T):
    """separate hardware meshes of a thumb segment"""
    out = []
    org = fr.o
    if i == 0:
        # bearing washer + bolt on the outer end of the pod's hinge barrel, and one on the dorsal face
        P = G.Part()
        P.washer_bolt((0, -0.94 * Wn / 2, 0), (0, -1, 0), r_wash=0.0040, r_mid=0.0030, r_hex=0.0020, xhint=(1, 0, 0))
        P.washer_bolt((-T * 0.50, 0, Lj * 0.70), (-1, 0, 0), r_wash=0.0036, r_mid=0.0027, r_hex=0.0018)
        out.append(P.make("hand_thumb_hinge1.L", fr, org, bone, wear=0.0, **HW))
    elif i == 1:
        P = G.Part()
        P.washer_bolt((0, -0.945 * Wn / 2, 0), (0, -1, 0), r_wash=0.0036, r_mid=0.0027, r_hex=0.0018, xhint=(1, 0, 0))
        P.washer_bolt((-T * 0.48, 0, Lj - 0.0050), (-1, 0, 0), r_wash=0.0032, r_mid=0.0024, r_hex=0.0016)
        out.append(P.make("hand_thumb_hinge2.L", fr, org, bone, wear=0.0, **HW))
        P = G.Part()
        ox = -T * 0.497
        P.oval_pad(0.50 * Lj, 0.0105, Wn * 0.56 + 0.0014, 0.0017, ox, DARK)
        P.oval_pad(0.50 * Lj, 0.0095, Wn * 0.56, 0.0024, ox, TEAL)
        out.append(P.make("hand_thumb_plate2.L", fr, org, bone, wear=0.0, bevel=0.0005, segs=2))
    else:
        # pad: gunmetal lip, dark dish, dull dark boss (the stills' chrome ring is darkened to gunmetal)
        P = G.Part()
        zc = 0.58 * Lj
        P.cyl((-T * 0.5 - 0.0002, 0, zc), (-1, 0, 0), 0.0070, 0.0014, TEAL, segments=28, xhint=(0, 0, 1))
        P.cyl((-T * 0.5 - 0.0009, 0, zc), (-1, 0, 0), 0.0053, 0.0014, DISC, segments=28, xhint=(0, 0, 1))
        P.cyl((-T * 0.5 - 0.0014, 0, zc), (-1, 0, 0), 0.0018, 0.0010, DARK, segments=16, xhint=(0, 0, 1))
        out.append(P.make("hand_thumb_pad.L", fr, org, bone, wear=0.0, bevel=0.0005, segs=1))
    return out


# ------------------------------------------------------------------------------------------------------------ palm
def _lerp(tab, z):
    """piecewise-linear lookup in [(z, v), ...]"""
    if z <= tab[0][0]:
        return tab[0][1]
    for (z0, v0), (z1, v1) in zip(tab, tab[1:]):
        if z <= z1:
            return v0 + (v1 - v0) * (z - z0) / (z1 - z0)
    return tab[-1][1]


SH_W = [(0.010, 0.054), (0.020, 0.062), (0.034, 0.0745), (0.050, 0.085), (0.064, 0.0895), (0.074, 0.0905), (0.080, 0.0880), (0.0845, 0.0805)]
SH_T = [(0.010, 0.020), (0.034, 0.025), (0.050, 0.025), (0.066, 0.022), (0.078, 0.018), (0.0845, 0.016)]
SH_OX = [(0.010, -0.0090), (0.022, -0.0092), (0.050, -0.0086), (0.074, -0.0076), (0.0845, -0.0070)]


def _dorsal_x(z):
    return _lerp(SH_OX, z) - _lerp(SH_T, z) / 2


def _oval(P, zm, hl, wmax, t, off, mat, n=17, power=2.6):
    """an elongated oval pad lying on the dorsal surface; its outer face is `off` proud of the shield"""
    sts = []
    for k in range(n):
        u = -1 + 2 * k / (n - 1)
        z = zm + u * hl
        wv = max(0.0030, wmax * max(0.0, 1 - abs(u) ** 2.6) ** (1 / 2.6))
        ox = _dorsal_x(z) - off + t / 2
        sts.append(dict(z=z, w=wv, t=t, ox=ox))
    P.loft(sts, mat, ring_fn=lambda s: G.ring_super(s["w"] / 2, s["t"] / 2, 24, power, ox=s["ox"]))


SLAT_Z = ((0.036, 0.054, 0.072), (0.056, 0.072, 0.078), (0.074, 0.0900, 0.083))
CABLE_YY = ((-0.026, -0.003), (-0.020, 0.0))


def _cable_pts(yy, dy):
    return [(0.0125, yy, 0.004), (0.0185, yy + dy, 0.016), (0.0200, yy + dy * 1.5, 0.034), (0.0150, yy + dy, 0.052), (0.0100, yy, 0.062)]


def build_palm():
    objs = []
    fr = L.Frame(W(0, 0, 0), HF.x, HF.y, HF.z)        # hand frame itself
    zl = [0.010, 0.020, 0.034, 0.050, 0.064, 0.074, 0.080, 0.0845]
    zE = zl[-1]

    # --- dorsal shield: ONE big smooth crowned shield (superellipse section), flaring wrist -> knuckles
    P = G.Part()
    st = [dict(z=z, w=_lerp(SH_W, z), t=_lerp(SH_T, z), ox=_lerp(SH_OX, z)) for z in zl]
    P.loft(st, TEAL, ring_fn=lambda s: G.ring_super(s["w"] / 2, s["t"] / 2, 40, 2.15, ox=s["ox"]))
    objs.append(P.make("hand_shield.L", fr, W(0, 0, 0.010), "hand.L", wear=0.0, bevel=0.0014, segs=3))

    # inset oval panel: dark outline groove, then the raised island (ref 06) as two separate meshes
    P = G.Part()
    _oval(P, 0.0475, 0.0345, 0.0470, 0.0036, 0.0003, DARK)
    objs.append(P.make("hand_shield_groove.L", fr, W(0, 0, 0.0475), "hand.L", wear=0.0, bevel=0.0004, segs=1))
    P = G.Part()
    _oval(P, 0.0475, 0.0300, 0.0395, 0.0040, 0.0010, TEAL)
    objs.append(P.make("hand_shield_panel.L", fr, W(0, 0, 0.0475), "hand.L", wear=0.0, bevel=0.0008, segs=2))

    # transverse knuckle ridge and its pale gold lip (ref 02)
    P = G.Part()
    P.loft([dict(z=zE - 0.0050, w=_lerp(SH_W, zE) + 0.0010, t=_lerp(SH_T, zE) + 0.0014, ox=_lerp(SH_OX, zE), c=0.0030),
            dict(z=zE + 0.0004, w=_lerp(SH_W, zE) + 0.0010, t=_lerp(SH_T, zE) + 0.0012, ox=_lerp(SH_OX, zE), c=0.0028)], TEAL, c=0.0030,
           ring_fn=lambda s: G.ring_super(s["w"] / 2, s["t"] / 2, 36, 3.0, ox=s["ox"]))
    objs.append(P.make("hand_knuckle_ridge.L", fr, W(0, 0, zE), "hand.L", wear=0.0, bevel=0.0010, segs=2))
    P = G.Part()
    P.loft([dict(z=zE - 0.0010, w=_lerp(SH_W, zE) + 0.0016, t=_lerp(SH_T, zE) + 0.0020, ox=_lerp(SH_OX, zE)),
            dict(z=zE + 0.0004, w=_lerp(SH_W, zE) + 0.0016, t=_lerp(SH_T, zE) + 0.0018, ox=_lerp(SH_OX, zE))], BRONZE,
           ring_fn=lambda s: G.ring_super(s["w"] / 2, s["t"] / 2, 36, 3.0, ox=s["ox"]))
    objs.append(P.make("hand_knuckle_lip.L", fr, W(0, 0, zE), "hand.L", wear=0.0, bevel=0.0004, segs=1))

    # six hex bolts on stepped washers around the oval panel (4-6 mm heads)
    P = G.Part()
    for zz, yy in ((0.0125, 0.0), (0.0805, 0.0), (0.030, 0.0285), (0.030, -0.0285), (0.064, 0.0335), (0.064, -0.0335)):
        P.washer_bolt((_dorsal_x(zz), yy, zz), (-1, 0, 0), r_wash=0.0030, r_mid=0.0022, r_hex=0.0015)
    objs.append(P.make("hand_shield_bolts.L", fr, W(0, 0, 0.04), "hand.L", wear=0.0, **HW))

    # --- palm core + three separate palm slats (the stacked slats of ref 013)
    P = G.Part()
    st = [dict(z=0.006, w=0.058, t=0.022, ox=0.0040, c=0.006), dict(z=0.050, w=0.074, t=0.022, ox=0.0045, c=0.006),
          dict(z=PALM_Z, w=0.083, t=0.020, ox=0.0030, c=0.006)]
    P.loft(st, TEAL, c=0.006)
    objs.append(P.make("hand_palm.L", fr, W(0, 0, 0.0), "hand.L", wear=0.0, bevel=0.0012, segs=2))
    for k, (z0, z1, w_) in enumerate(SLAT_Z):
        P = G.Part()
        rr, fbb = P.loft([dict(z=z0, w=w_, t=0.0050, ox=0.0140, c=0.0018), dict(z=(z0 + z1) / 2, w=w_ + 0.001, t=0.0060, ox=0.0140, c=0.0020),
                          dict(z=z1, w=w_, t=0.0050, ox=0.0140, c=0.0018)], TEAL, c=0.0018)
        P.recess(fbb[0][0:2], 0.0005, 0.0020)
        for sgn in (-1, 1):
            P.washer_bolt((0.0172, sgn * (w_ / 2 - 0.0045), (z0 + z1) / 2), (1, 0, 0), r_wash=0.0026, r_mid=0.0019, r_hex=0.0013, xhint=(0, 0, 1))
        objs.append(P.make(f"hand_palm_slat{k + 1}.L", fr, W(0, 0, (z0 + z1) / 2), "hand.L", wear=0.0, bevel=0.0010, segs=2))
    # heel plate at the wrist on the palm side
    P = G.Part()
    P.loft([dict(z=0.004, w=0.060, t=0.0050, ox=0.0140, c=0.0018), dict(z=0.032, w=0.066, t=0.0056, ox=0.0140, c=0.0020)], TEAL, c=0.0018)
    objs.append(P.make("hand_palm_heel.L", fr, W(0, 0, 0.004), "hand.L", wear=0.0, bevel=0.0010, segs=2))

    # three round thumb bearings (replace the stills' hex plates), one mesh each
    for k, (hx_, hz_) in enumerate(((0.002, 0.026), (0.0105, 0.040), (0.002, 0.054))):
        P = G.Part()
        P.cyl((hx_, -0.0398, hz_), (0, -1, 0), 0.0068, 0.0032, TEAL, segments=28, xhint=(1, 0, 0))
        P.washer_bolt((hx_, -0.0414, hz_), (0, -1, 0), r_wash=0.0046, r_mid=0.0033, r_hex=0.0018, xhint=(1, 0, 0))
        objs.append(P.make(f"hand_thumb_bearing{k + 1}.L", fr, W(hx_, -0.0398, hz_), "hand.L", wear=0.0, bevel=0.0006, segs=1))

    # teal side plates closing the palm edges (follow the flare of the shield), each with a dark inlay
    ang = math.atan2((0.088 - 0.066) / 2, 0.082)
    for nm, sgn in (("inner", -1), ("outer", 1)):
        P = G.Part()
        rot = Matrix.Rotation(-sgn * ang, 3, "X")
        P.box((0.0050, sgn * (0.0418 - 0.0005), 0.052), (0.0150, 0.0034, 0.074), TEAL, rot=rot)
        P.box((0.0050, sgn * (0.0418 - 0.0005), 0.052), (0.0030, 0.0040, 0.062), DISC, rot=rot)
        objs.append(P.make(f"hand_side_plate_{nm}.L", fr, W(0.005, sgn * 0.0418, 0.052), "hand.L", wear=0.0, bevel=0.0008, segs=2))

    # --- palm-side cables (heel -> between the slats) and their two clamps (own meshes)
    P = G.Part()
    for yy, dy in CABLE_YY:
        P.tube([Vector(p) for p in _cable_pts(yy, dy)], 0.0021, DARK, nring=8)
    objs.append(P.make("hand_cables.L", fr, W(0, -0.023, 0.03), "hand.L", wear=0.0, bevel=0.0004, segs=1))
    for k, idx in enumerate((1, 2)):
        P = G.Part()
        for yy, dy in CABLE_YY:
            pt = _cable_pts(yy, dy)[idx]
            P.torus(Vector(pt), (0, 0, 1), 0.0023, 0.0008, SILVER, major=14, minor=5, xhint=(1, 0, 0))
        mid = Vector(_cable_pts(CABLE_YY[0][0], CABLE_YY[0][1])[idx]).lerp(Vector(_cable_pts(CABLE_YY[1][0], CABLE_YY[1][1])[idx]), 0.5)
        P.washer_bolt(mid + Vector((0.0034, 0, 0)), (1, 0, 0), r_wash=0.0024, r_mid=0.0017, r_hex=0.0012, xhint=(0, 0, 1))
        objs.append(P.make(f"hand_cable_clamp{k + 1}.L", fr, W(*mid), "hand.L", wear=0.0, **HW))

    # --- knuckle caps: four low domes (frame 04: 4 knuckle columns), each with a bolt on its crown (own mesh)
    for i, (fname, ycen, Wn, T, mcp_z, lf, angs, splay) in enumerate(FINGERS):
        P = G.Part()
        cx = -0.0133
        P.sphere((cx + 0.0004, ycen, mcp_z - 0.0018), (0.0020, Wn * 0.44, 0.0072), TEAL, segments=20, rings=10)
        objs.append(P.make(f"hand_knuckle_{fname}.L", fr, W(0, ycen, mcp_z), "hand.L", wear=0.0, bevel=0.0009, segs=2))
        P = G.Part()
        P.washer_bolt((cx + 0.0004 - 0.0019, ycen, mcp_z - 0.0018), (-1, 0, 0), r_wash=min(0.0030, 0.15 * Wn), r_mid=0.0020, r_hex=0.0014)
        objs.append(P.make(f"hand_knuckle_bolt_{fname}.L", fr, W(0, ycen, mcp_z), "hand.L", wear=0.0, **HW))

    # --- wrist socket (5 meshes): dark plug into the forearm cuff, thin dark ring, slim gunmetal collar, pewter band, 3 collar bolts
    a_, b_ = 0.0305, 0.0225
    ring_fn = lambda s: G.ring_super(s["w"], s["t"], 28, 2.6, ox=s.get("ox", 0.0))
    sup = lambda s: G.ring_super(s["w"] / 2, s["t"] / 2, 36, 3.0, ox=s["ox"])
    P = G.Part()
    P.loft([dict(z=-0.006, w=a_ * 0.9, t=b_ * 0.9, ox=-0.0010), dict(z=0.0, w=a_ * 0.9, t=b_ * 0.9, ox=-0.0010), dict(z=0.006, w=a_ * 0.9, t=b_ * 0.9, ox=-0.0010)], DARK,
           ring_fn=ring_fn)
    objs.append(P.make("hand_wrist_plug.L", fr, W(0, 0, 0), "hand.L", wear=0.0, bevel=0.0010, segs=2))
    P = G.Part()
    P.loft([dict(z=0.0, w=0.0572, t=0.0340, ox=-0.0045), dict(z=0.0042, w=0.0576, t=0.0344, ox=-0.0045)], DARK, ring_fn=sup)
    objs.append(P.make("hand_wrist_ring.L", fr, W(0, 0, 0), "hand.L", wear=0.0, bevel=0.0008, segs=1))
    P = G.Part()
    P.loft([dict(z=0.0042, w=0.0575, t=0.0330, ox=-0.0045), dict(z=0.0070, w=0.0582, t=0.0336, ox=-0.0045), dict(z=0.0100, w=0.0582, t=0.0336, ox=-0.0045)], TEAL, ring_fn=sup)
    objs.append(P.make("hand_wrist_collar.L", fr, W(0, 0, 0.004), "hand.L", wear=0.0, bevel=0.0010, segs=2))
    P = G.Part()
    P.loft([dict(z=0.0088, w=0.0590, t=0.0344, ox=-0.0045), dict(z=0.0102, w=0.0590, t=0.0344, ox=-0.0045)], SILVER, ring_fn=sup)
    objs.append(P.make("hand_wrist_band.L", fr, W(0, 0, 0.009), "hand.L", wear=0.0, bevel=0.0004, segs=1))
    P = G.Part()
    for k in (-1, 0, 1):
        P.washer_bolt((-0.0045 - 0.0168, k * 0.0125, 0.0058), (-1, 0, 0), r_wash=0.0026, r_mid=0.0019, r_hex=0.0013)
    objs.append(P.make("hand_wrist_bolts.L", fr, W(0, 0, 0.006), "hand.L", wear=0.0, **HW))
    return objs


def build():
    ensure_materials()
    objs = []
    for spec in FINGERS:
        objs += build_finger(*spec)
    objs += build_thumb()
    objs += build_palm()
    out = list(objs)
    if os.environ.get("HAND_SIDE") == "L":      # dev switch: left hand only (tight framing while iterating)
        bpy.context.view_layer.update()
        return out
    mir = [L.mirror_x(o) for o in objs]
    if os.environ.get("HAND_SIDE") == "R":
        bpy.context.view_layer.update()
        return mir
    out += mir
    bpy.context.view_layer.update()
    return out
