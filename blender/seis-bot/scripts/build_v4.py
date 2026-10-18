# v3 build (Ultron-style refs): blender -b -P build_v3.py
import bpy, bmesh, math, sys, os, importlib
sys.path.insert(0, '/workspace/robot/v4')
import lib, materials
importlib.reload(lib); importlib.reload(materials)
from lib import *
from mathutils import Vector as V, Matrix, Quaternion

OUT = '/workspace/robot/v4'
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = bpy.data.collections.new('Robot'); scene.collection.children.link(coll)
lib.COLL = coll
lib.MATS.update(materials.build_all())
lib.PARTS.clear(); lib.PATHS.clear()
R = math.radians
F = front_map(); B = back_map()
def SD(s): return '.L' if s > 0 else '.R'

# ====================================================================== HEAD (v2.3: skull-like, sculpted face, engraved panel lines)
skull_cols = [  # z, cy, rx, ryf, ryb
    (1.884, -0.058, 0.056, 0.016, 0.026), (1.893, -0.056, 0.066, 0.028, 0.038), (1.910, -0.051, 0.073, 0.04, 0.052),
    (1.935, -0.041, 0.078, 0.052, 0.066), (1.965, -0.027, 0.085, 0.064, 0.084), (1.995, -0.013, 0.09, 0.078, 0.1),
    (2.025, 0.001, 0.091, 0.088, 0.112), (2.060, 0.015, 0.1, 0.096, 0.122), (2.095, 0.027, 0.106, 0.1, 0.126),
    (2.130, 0.035, 0.103, 0.101, 0.123), (2.162, 0.041, 0.094, 0.095, 0.11), (2.188, 0.044, 0.076, 0.08, 0.088),
    (2.205, 0.045, 0.044, 0.052, 0.054), (2.215, 0.046, 0.014, 0.016, 0.016)]
def _interp(cols, f):
    out = []
    for i in range(len(cols) - 1):
        for k in range(f):
            t = k / f
            out.append(tuple(cols[i][j] * (1 - t) + cols[i + 1][j] * t for j in range(5)))
    out.append(cols[-1]); return out
skull_data = _interp(skull_cols, 4)
def skull_cy(z):
    for i in range(len(skull_data) - 1):
        z0, z1 = skull_data[i][0], skull_data[i + 1][0]
        if z0 <= z <= z1:
            f = (z - z0) / (z1 - z0)
            return 0.0, skull_data[i][1] * (1 - f) + skull_data[i + 1][1] * f
    return 0.0, skull_data[-1][1] if z > 2.0 else skull_data[0][1]
skull = vloft('Head_Skull', [(z, 0.0, cy, rx, f_, b_) for z, cy, rx, f_, b_ in skull_data], 'silver', 'head', p=2.3, nseg=128, sub=1)
def dens(pts, n=8):
    out = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        out += [(a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n) for j in range(n)]
    return out
def g2(x, y, cx, cy, sx, sy): return math.exp(-(((x - cx) / sx) ** 2 + ((y - cy) / sy) ** 2))
EYE_C = (0.36, 2.026); EYE_W, EYE_H, EYE_ROT = 0.024, 0.017, math.radians(10)
def zb(ap): return 2.037 + 0.034 * (ap - 0.1)  # brow line (inner low -> slanted, menacing)
def almond(cx_rad, cz, w, h, rot, s, n=48, r_eye=0.093):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = w * math.cos(t); z = h * math.sin(t) * abs(math.sin(t)) ** 0.35
        c, sn = math.cos(rot), math.sin(rot)
        xr, zr = x * c - z * sn, x * sn + z * c
        out.append((s * (cx_rad + xr / r_eye), cz + zr))
    return out
def sculpt(ob):
    for v in ob.data.vertices:
        p = v.co; cx, cy = skull_cy(p.z)
        dx, dy = p.x, -(p.y - cy)
        if dy <= 0: continue
        ph = math.atan2(dx, dy); ap = abs(ph)
        d = 0.0
        d -= 0.0075 * g2(ap, p.z, 0.66, 1.962, 0.2, 0.026)                 # hollow cheeks
        d -= 0.012 * g2(ap, p.z, 0.36, 2.026, 0.21, 0.014)                 # eye socket band
        d += 0.0042 * math.exp(-((p.z - zb(ap) - 0.004) / 0.0055) ** 2) * (1 if ap < 0.78 else math.exp(-((ap - 0.78) / 0.08) ** 2))  # brow ridge
        d += 0.0022 * g2(ap, p.z, 0.0, 1.975, 0.11, 0.035)                  # subtle muzzle plane (no nose)
        rad = V((math.sin(ph), -math.cos(ph), 0))
        v.co = p + rad * d
sculpt(skull)
T_skull = bvh(skull)
cmap = cyl_map(skull_cy)
HC = (0.0, 0.03, 2.03)
rmap = radial_map(HC)
# dark teal centre stripe over the dome (flush) + swept grooves
KS = [(9, 0.0007), (22, 0.008), (40, 0.02), (60, 0.034), (76, 0.042), (88, 0.036), (102, 0.016), (125, 0.009), (170, 0.007), (213, 0.003)]
stripe = [(R(a), w) for a, w in KS] + [(R(a), -w) for a, w in reversed(KS)]
def _wrap(n):
    _sw = bpy.data.objects[n].modifiers.new('Wrap', 'SHRINKWRAP'); _sw.target = skull
    _sw.wrap_method = 'NEAREST_SURFACEPOINT'; _sw.wrap_mode = 'OUTSIDE_SURFACE'; _sw.offset = 0.0012
plate('Head_CentreStripe', T_skull, rmap, dens(stripe, 6), 'tealflat', 'head', offset=0.0015, thick=0.0016)
def _sw(a):
    pts = KS
    for i in range(len(pts) - 1):
        if pts[i][0] <= a <= pts[i + 1][0]:
            f = (a - pts[i][0]) / (pts[i + 1][0] - pts[i][0]); return pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
    return 0.007
for s in (1, -1):
    engrave('Head_StripeGroove' + SD(s), T_skull, rmap, [(R(a), s * (_sw(a) + 0.0045)) for a in range(11, 211, 3)], 'head', w=0.0024, depth=0.0018)
for s in (1, -1):
    sd = SD(s)
    pan = [(R(118), s * 0.06), (R(150), s * 0.064), (R(195), s * 0.058), (R(200), s * 0.074), (R(170), s * 0.086), (R(130), s * 0.088), (R(108), s * 0.078)]
    plate('Head_DomePanel' + sd, T_skull, rmap, chaikin(pan, 2), 'tealflat', 'head', offset=0.0015, thick=0.0016)
    for k in range(6):
        th0 = 26 + 9 * k; th1 = 206 - 6 * k
        engrave('Head_Groove%d' % k + sd, T_skull, rmap, [(R(th0 + (th1 - th0) * i / 40.0), s * (_sw(th0 + (th1 - th0) * i / 40.0) + 0.009 + 0.0115 * k * (0.55 + 0.45 * math.sin(math.pi * min(1.0, i / 24.0) / 2)))) for i in range(41)], 'head', w=0.0026, depth=0.0005)
    # face: sockets + almond eye slits
    if False: plate('Head_EyeSocket' + sd, T_skull, cmap, almond(EYE_C[0] + 0.004, EYE_C[1] - 0.001, EYE_W * 1.45, EYE_H * 1.7, EYE_ROT, s), 'groove', 'head', offset=0.0002, thick=0.0015)
    _ph = s * EYE_C[0]; _cy = skull_cy(EYE_C[1])[1]; _d = V((math.sin(_ph), -math.cos(_ph), 0))
    _loc, _nn = hit(T_skull, V((0, _cy, EYE_C[1])) + _d * 0.4, -_d)
    ellipsoid('Head_Eye' + sd, _loc - _d * 0.002, EYE_W * 1.19, 0.0112, EYE_H * 1.25, 'eye', 'head', nseg=32, nz=16)
    ellipsoid('Head_EyeCore' + sd, _loc + _d * (0.0112 * 0.8 - 0.002), EYE_W * 1.19 * 0.3, 0.0042, EYE_H * 0.4, 'eyecore', 'head', nseg=20, nz=10)
    ellipsoid('Head_EyeGlow' + sd, _loc - _d * 0.002, EYE_W * 1.5, 0.004, EYE_H * 1.6, 'eyeglow', 'head', nseg=32, nz=12)
    if False: plate('Head_EyeCore' + sd, T_skull, cmap, almond(EYE_C[0] - 0.005, EYE_C[1] + 0.0005, EYE_W * 0.55, EYE_H * 0.6, EYE_ROT, s, n=24), 'eyecore', 'head', offset=0.0019, thick=0.0014, merge=3e-4)
    # v3: raised, layered sculpted face plates (brow ridge, stepped cheekbones)
    brow = [(0.04, 2.036), (0.25, 2.046), (0.52, 2.053), (0.74, 2.06), (0.88, 2.03), (0.94, 2.0), (1.02, 2.02), (0.92, 2.088), (0.5, 2.082), (0.25, 2.075), (0.04, 2.064)]
    bp = plate('Head_BrowPlate' + sd, T_skull, cmap, dens([(s * a, z) for a, z in brow]), 'silver', 'head', offset=0.0068, thick=0.0055, merge=2e-4)
    engrave('Head_BrowCut' + sd, T_skull, cmap, dens([(s * a, z) for a, z in brow], 6) + [(s * brow[0][0], brow[0][1])], 'head', w=0.0042, depth=0.0004, mat='black')
    ck1 = [(0.08, 2.006), (0.3, 2.002), (0.58, 2.005), (0.8, 2.02), (0.95, 1.985), (0.66, 1.946), (0.42, 1.943), (0.1, 1.958)]
    ckp = plate('Head_CheekPlate' + sd, T_skull, cmap, dens([(s * a, z) for a, z in ck1]), 'silver', 'head', offset=0.0046, thick=0.005, merge=2e-4)
    engrave('Head_CheekCut' + sd, T_skull, cmap, dens([(s * a, z) for a, z in ck1], 6) + [(s * ck1[0][0], ck1[0][1])], 'head', w=0.0042, depth=0.0004, mat='black')
    # jaw side plates (under the cheek plates), dark gap round them
    jw = [(0.62, 1.958), (0.98, 1.995), (1.08, 1.95), (0.98, 1.905), (0.72, 1.89)]
    plate('Head_JawPlate' + sd, T_skull, cmap, dens([(s * a, z) for a, z in jw]), 'silver', 'head', offset=0.0028, thick=0.0045, merge=2e-4)
    engrave('Head_JawCut' + sd, T_skull, cmap, dens([(s * a, z) for a, z in jw], 6) + [(s * jw[0][0], jw[0][1])], 'head', w=0.0036, depth=0.0004, mat='black')
    # cuts on the raised plates (diagonal cheek cuts, brow cuts)
    T_ck = bvh(ckp); T_bp = bvh(bp)
    for k, pts in enumerate(([(0.74, 2.0), (0.52, 1.976), (0.3, 1.956)], [(0.88, 1.984), (0.68, 1.957)])):
        engrave('Head_CheekDiag%d' % k + sd, T_ck, cmap, [(s * a, z) for a, z in pts], 'head', n=16, w=0.0016, depth=0.0006 - 0.005)
    for k, pts in enumerate(([(0.32, 2.072), (0.56, 2.064), (0.8, 2.052)],)):
        engrave('Head_BrowLine%d' % k + sd, T_bp, cmap, [(s * a, z) for a, z in pts], 'head', n=16, w=0.0015, depth=0.0006 - 0.0055)
    tp = [(0.80, 2.075), (1.05, 2.085), (1.2, 2.04), (1.02, 2.035)]
    plate('Head_TemplePlate' + sd, T_skull, cmap, chaikin([(s * a, z) for a, z in tp], 2), 'silver', 'head', offset=0.003, thick=0.005, merge=2e-4)
    # engraved face panel lines
    L = [[(0.08 + 0.7 * i / 30.0, zb(0.08 + 0.7 * i / 30.0) + 0.009) for i in range(31)],     # brow top line
         [(0.66, 2.036), (0.6, 1.995), (0.42, 1.958), (0.22, 1.938), (0.1, 1.93)],              # cheek diagonal (eye -> mouth)
         [(0.28, 1.926), (0.55, 1.946), (0.8, 1.985), (0.95, 2.03)],                             # jaw line
         [(0.82, 2.06), (0.98, 2.04), (1.15, 2.01)]]                                             # temple
    L += [[(0.07, 2.034), (0.06, 1.995), (0.07, 1.958)], [(0.82, 2.0), (0.7, 1.975), (0.56, 1.957)], [(0.12, 2.064), (0.2, 2.1), (0.26, 2.14)], [(0.55, 2.08), (0.62, 2.12)], [(0.95, 2.06), (1.05, 1.98), (0.9, 1.93)], [(0.3, 1.952), (0.26, 1.935)], [(0.0, 2.075), (0.0, 2.06)], [(0.38, 2.075), (0.48, 2.1), (0.5, 2.16)], [(0.2, 2.08), (0.3, 2.12), (0.34, 2.17)], [(0.62, 2.07), (0.72, 2.11), (0.76, 2.15)], [(0.1, 2.07), (0.16, 2.11)], [(0.9, 2.09), (1.0, 2.12), (1.1, 2.16)], [(1.0, 2.07), (1.12, 2.1), (1.24, 2.13)], [(0.84, 2.1), (0.9, 2.14), (0.96, 2.18)]]
    for k, pts in list(enumerate(L))[3:]:
        engrave('Head_FaceLine%d' % k + sd, T_skull, cmap, [(s * a, z) for a, z in pts], 'head', n=24, w=0.0016, depth=0.0008)
# thin vertical mouth plate with fine horizontal slits, small pointed chin
mz = plate('Head_Muzzle', T_skull, cmap, dens([(-0.66, 1.951), (0.66, 1.951), (0.7, 1.892), (0.66, 1.884), (-0.66, 1.884), (-0.7, 1.892)]), 'silver', 'head', offset=0.0034, thick=0.0055, merge=2e-4)
engrave('Head_MuzzleGap', T_skull, cmap, dens([(-0.66, 1.951), (0.66, 1.951), (0.7, 1.892), (0.66, 1.884), (-0.66, 1.884), (-0.7, 1.892)], 6) + [(-0.66, 1.951)], 'head', w=0.0036, depth=0.0004, mat='black')
T_mz = bvh(mz)
engrave('Head_MouthSlit0', T_mz, cmap, [(-0.52, 1.918), (0.0, 1.918), (0.52, 1.918)], 'head', n=32, w=0.0026, depth=0.0006 - 0.0055, mat='black')
for s in (1, -1):
    engrave('Head_MuzzleCut' + SD(s), T_mz, cmap, [(s * 0.3, 1.946), (s * 0.3, 1.924)], 'head', n=12, w=0.0014, depth=0.0006 - 0.0055)
# ears: flush round discs at the temples with red tissue rim and C fin
for s in (1, -1):
    sd = SD(s)
    loc, nn = hit(T_skull, (s * 0.5, 0.035, 1.995), (-s, 0, 0))
    E = loc
    disc('Head_EarTissue' + sd, E - nn * 0.002, nn, 0.038, 0.006, 'muscle', 'head', nseg=48)
    disc('Head_EarDisc' + sd, E + nn * 0.003, nn, 0.036, 0.009, 'dark', 'head', nseg=48)
    _u = nn.cross(V((0, 0, 1))).normalized(); _w = nn.cross(_u)
    for g in range(0):
        _a = 2 * math.pi * g / 16
        disc('Head_EarGear%02d' % g + sd, E + nn * 0.004 + (_u * math.cos(_a) + _w * math.sin(_a)) * 0.037, nn, 0.0042, 0.008, 'silver', 'head', nseg=12, sub=0)
    disc('Head_EarRing' + sd, E + nn * 0.0075, nn, 0.028, 0.004, 'silver', 'head', nseg=48)
    disc('Head_EarLens' + sd, E + nn * 0.009, nn, 0.02, 0.003, 'black', 'head', nseg=40)
    disc('Head_EarHub' + sd, E + nn * 0.0105, nn, 0.009, 0.004, 'silver', 'head', nseg=24)
    fin = spline([V((0.035 + 1.35 * (0.035 - y), 1.995 + 1.35 * (z - 1.995), 0)) for y, z in [(-0.035, 2.085), (0.01, 2.098), (0.06, 2.078), (0.09, 2.03), (0.086, 1.97), (0.06, 1.93), (0.015, 1.912), (-0.035, 1.925)]], 56)
    P, N = surf_path(T_skull, side_map(s), [(p.x, p.y) for p in fin], 0.018)
    sweep('Head_EarFin' + sd, P, lambda t: 0.009 + 0.007 * math.sin(math.pi * t) ** 0.5, 0.008, 'silver', 'head', normals=N, p=2.6)
    P2, N2 = surf_path(T_skull, side_map(s), [(p.x, p.y) for p in fin], 0.003)
    sweep('Head_EarFinGap' + sd, P2, lambda t: 0.012 + 0.008 * math.sin(math.pi * t) ** 0.5, 0.003, 'black', 'head', normals=N2, p=2.6)
    _o, _dd = cmap(s * 1.02, 1.936); loc, nn = hit(T_skull, _o, _dd)
    disc('Head_HingeDisc' + sd, loc + nn * 0.001, nn, 0.017, 0.008, 'dark', 'head', nseg=40)
    disc('Head_HingeRing' + sd, loc + nn * 0.0045, nn, 0.012, 0.004, 'silver', 'head', nseg=36)
    disc('Head_HingeHub' + sd, loc + nn * 0.0065, nn, 0.0055, 0.004, 'black', 'head', nseg=24)

# ====================================================================== NECK (long, segmented, red tissue between)
vloft('Neck_Tissue', [(1.77, 0, 0.012, 0.03, 0.03, 0.03), (1.84, 0, 0.018, 0.026, 0.026, 0.026), (1.93, 0, 0.012, 0.028, 0.03, 0.03)], 'muscle', 'neck', p=2.0, nseg=24)
for k in range(6):
    z0 = 1.781 + k * 0.022; r = 0.064 - 0.003 * k; cy = 0.012 + 0.002 * k
    rings = [dict(c=(0, cy, z0), rx=r * 0.82, ry=r * 0.74, p=2.6), dict(c=(0, cy, z0 + 0.003), rx=r, ry=r * 0.9, p=2.6),
             dict(c=(0, cy, z0 + 0.015), rx=r, ry=r * 0.9, p=2.6), dict(c=(0, cy, z0 + 0.019), rx=r * 0.82, ry=r * 0.74, p=2.6)]
    mk('Neck_Ring%d' % k, tube_bm(rings, 32, arc=None), 'teal2' if k % 2 else 'dark', 'neck', sub=1)
for s in (1, -1):
    sd = SD(s)
    P = spline([(s * 0.018, -0.038, 1.785), (s * 0.016, -0.042, 1.85), (s * 0.014, -0.038, 1.915)], 16)
    sweep('Neck_FrontStrap' + sd, P, 0.006, 0.004, 'silver', 'neck', ref=(0, -1, 0), nseg=10)
    for k in range(3):
        a = R(55 + 35 * k)
        p0 = V((s * 0.07 * math.sin(a), 0.02 - 0.05 * math.cos(a), 1.785)); p1 = V((s * 0.03 * math.sin(a), 0.045 - 0.035 * math.cos(a), 1.93))
        sweep('Neck_Cable%d' % k + sd, spline([p0, (p0 + p1) / 2 + V((s * 0.012, 0, 0)), p1], 16), 0.0045, 0.0045, 'dark', 'neck', ref=(1, 0, 0), nseg=10)

# ====================================================================== CHEST (red muscle core, gunmetal V-yoke pecs, sternum strip)
chest_core = vloft('Chest_Core', [
    (1.40, 0.0, 0.0, 0.14, 0.095, 0.10), (1.47, 0.0, 0.0, 0.18, 0.118, 0.115), (1.56, 0.0, 0.0, 0.215, 0.132, 0.125),
    (1.66, 0.0, 0.0, 0.245, 0.14, 0.128), (1.74, 0.0, 0.0, 0.26, 0.135, 0.12), (1.80, 0.0, 0.01, 0.235, 0.112, 0.1),
    (1.835, 0.0, 0.015, 0.16, 0.075, 0.07), (1.85, 0.0, 0.015, 0.06, 0.04, 0.04)], 'muscle', 'chest', p=3.0, nseg=48)
T_chest = bvh(chest_core)
vloft('Chest_Yoke', [(1.775, 0.0, 0.004, 0.2, 0.09, 0.1), (1.81, 0.0, 0.012, 0.236, 0.114, 0.104), (1.84, 0.0, 0.016, 0.17, 0.08, 0.075), (1.858, 0.0, 0.016, 0.07, 0.048, 0.046)], 'teal2', 'chest', p=3.0, nseg=48)
pec = [(0.03, 1.822), (0.12, 1.84), (0.22, 1.842), (0.285, 1.82), (0.315, 1.77), (0.318, 1.70), (0.30, 1.62),
       (0.255, 1.54), (0.195, 1.465), (0.13, 1.41), (0.075, 1.38), (0.03, 1.375)]
for s in (1, -1):
    plate('Chest_Pec' + SD(s), T_chest, F, chaikin(mirror_pts(pec, s), 2), 'teal', 'chest', offset=0.012, thick=0.024, merge=3e-4,
          disp=lambda a, z: 0.012 * g2(abs(a), z, 0.14, 1.70, 0.11, 0.1))
T_pec = bvh_multi([o for o, b in PARTS if o.name.startswith('Chest_Pec')] + [chest_core])
for s in (1, -1):
    sd = SD(s)
    # ribbing grooves on the upper outer pec
    for k in range(7):
        x0 = 0.14 + 0.018 * k
        P, N = surf_path(T_pec, F, [(s * x0, 1.818), (s * (x0 + 0.006), 1.79), (s * (x0 + 0.004), 1.765 - 0.004 * k)], -0.0003, n=10)
        if len(P) > 3: sweep('Chest_PecRib%d' % k + sd, P, 0.0013, 0.0012, 'groove', 'chest', normals=N, sub=0, nseg=6)
    # pec border arcs that continue down the abdomen (V arms)
    for k, (pts, w, t, off) in list(enumerate((
            ([(0.25, 1.822), (0.287, 1.775), (0.293, 1.71), (0.268, 1.635), (0.215, 1.565), (0.16, 1.495), (0.12, 1.415), (0.1, 1.33), (0.095, 1.25)], 0.016, 0.016, 0.034),
            ([(0.035, 1.452), (0.085, 1.468), (0.15, 1.512), (0.215, 1.572), (0.262, 1.635), (0.282, 1.70)], 0.008, 0.01, 0.034))))[2:]:
        P, N = surf_path(T_pec, F, [(s * a, b) for a, b in pts], off, n=56)
        P2, N2 = [], []
        for (a_, b_) in [(q.x, q.y) for q in spline([V((s * a, b, 0)) for a, b in pts], 56)]:
            loc, nn = hit(T_pec, (a_, -1.5, b_), (0, 1, 0))
            if loc is None:
                loc, nn = hit(T_pec, (a_ * 0.6, -1.5, b_), (0, 1, 0))
                if loc is None: continue
                loc = V((a_, loc.y + 0.01, b_))
            P2.append(loc + nn * off); N2.append(nn)
        P, N = P2, N2
        sweep('Chest_PecArc%d' % k + sd, P, lambda tt, w=w: w * (0.55 + 0.45 * math.sin(math.pi * tt) ** 0.4), t, 'teal2' if k == 0 else 'bronze', 'chest', normals=N, p=2.8)
    for _nm, _pts in (('Chest_PecTrim', [(0.25, 1.83), (0.297, 1.782), (0.304, 1.70), (0.286, 1.62), (0.24, 1.543), (0.174, 1.466), (0.104, 1.41)]),
                      ('Chest_PecTrimIn', [(0.046, 1.812), (0.044, 1.70), (0.044, 1.55), (0.047, 1.405), (0.08, 1.394), (0.13, 1.423), (0.186, 1.474)])):
        P, N = surf_path(T_pec, F, [(s * a, b) for a, b in _pts], 0.0, n=64)
        sweep(_nm + sd, P, lambda t: 0.0055 * (0.35 + 0.65 * math.sin(math.pi * t) ** 0.3), 0.0032, 'bronze', 'chest', normals=N, p=2.6)
    for k in range(6):
        z0 = 1.47 + 0.055 * k
        engrave('Chest_RibGroove%d' % k + sd, T_pec, F, [(s * 0.07, z0 - 0.01), (s * 0.15, z0 + 0.004), (s * 0.23, z0 + 0.022), (s * (0.27 - 0.01 * abs(k - 3)), z0 + 0.04)], 'chest', n=24, w=0.0034, depth=0.0005)
        engrave('Chest_RibLip%d' % k + sd, T_pec, F, [(s * 0.07, z0 - 0.0055), (s * 0.15, z0 + 0.0085), (s * 0.23, z0 + 0.0265), (s * (0.27 - 0.01 * abs(k - 3)), z0 + 0.0445)], 'chest', n=24, w=0.0014, depth=-0.0007, mat='silver')
    engrave('Chest_PecBorder' + sd, T_pec, F, [(s * 0.25, 1.826), (s * 0.292, 1.78), (s * 0.298, 1.70), (s * 0.28, 1.62), (s * 0.235, 1.545), (s * 0.17, 1.47), (s * 0.1, 1.415)], 'chest', n=48, w=0.0016)
    # swept ribs over the red core on the flanks
    cm0 = cyl_map(lambda zz: (0.0, 0.0))
    for k in range(3):
        z0 = 1.53 - 0.045 * k
        pts = [(s * R(a), z0 - 0.06 * max(0.0, (a - 40) / 80.0) ** 1.5) for a in range(40, 121, 3)]
        P, N = surf_path(bvh_multi([chest_core, abd]) if False else T_chest, cm0, pts, 0.014)
        if len(P) > 4:
            sweep('Chest_Rib%d' % k + sd, P, lambda tt: 0.011 * (0.5 + 0.5 * math.sin(math.pi * tt) ** 0.4), 0.012, 'teal2', 'chest', normals=N, p=2.6)
    # clavicle Y piece
    P = spline([(s * 0.09, -0.07, 1.82), (s * 0.05, -0.09, 1.81), (s * 0.012, -0.11, 1.795)], 20)
    sweep('Chest_Clavicle' + sd, P, 0.012, 0.008, 'teal2', 'chest', ref=(0, -1, 0.3), p=3)
    # trapezius shroud
    P = spline([(s * 0.05, 0.03, 1.83), (s * 0.13, 0.03, 1.81), (s * 0.2, 0.02, 1.79)], 24)
    sweep('Chest_Trap' + sd, P, lambda t: 0.032 + 0.02 * t, lambda t: 0.01, 'teal', 'chest', ref=(0, 0, 1), p=2.6, bend=-0.01)
    # back red muscle + cage
    for k, (x, z0, z1, rr) in enumerate(((0.06, 1.47, 1.76, 0.045), (0.13, 1.5, 1.74, 0.045), (0.19, 1.54, 1.70, 0.035))):
        rings = []
        for i in range(9):
            t = i / 8.0; z = z0 + (z1 - z0) * t
            r = rr * (0.25 + 0.75 * math.sin(math.pi * t) ** 0.6)
            loc, n = hit(T_chest, (s * x, 1.0, z), (0, -1, 0))
            rings.append(dict(c=(s * x, (loc.y if loc else 0.12) - r * 0.3, z), rx=r, ry=r * 0.8, p=2.0))
        mk('Back_Muscle%d' % k + sd, tube_bm(rings, 20), 'muscle', 'chest', sub=1)
    for k, pts in enumerate(([(0.05, 1.80), (0.12, 1.74), (0.16, 1.62), (0.13, 1.50), (0.06, 1.42)],
                             [(0.14, 1.79), (0.22, 1.72), (0.23, 1.6), (0.18, 1.48), (0.10, 1.40)],
                             [(0.03, 1.70), (0.10, 1.66), (0.2, 1.64), (0.25, 1.66)])):
        P, N = surf_path(T_chest, B, [(s * a, b) for a, b in pts], 0.05, n=40)
        sweep('Back_Cage%d' % k + sd, P, lambda tt: 0.016 * (0.5 + 0.5 * math.sin(math.pi * tt) ** 0.5), 0.011, 'teal', 'chest', normals=N, p=2.8)
# sternum strip: 6 plate + segmented column down to the pelvis
plate('Chest_SixPlate', T_chest, F, rrect(0.0, 1.668, 0.028, 0.054), 'teal2', 'chest', offset=0.024, thick=0.012)
T6 = bvh(PARTS[-1][0])
loc, n = hit(T6, (0, -1, 1.668), (0, 1, 0))
cu = bpy.data.curves.new('Six', 'FONT'); cu.body = '6'
cu.font = bpy.data.fonts.load('/workspace/robot/v4/DejaVuSans-Bold.ttf')
cu.size = 0.072; cu.extrude = 0.0025; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.bevel_depth = 0.0005
tob = bpy.data.objects.new('Chest_Six_tmp', cu); coll.objects.link(tob)
tob.location = (0, loc.y - 0.0015, 1.668); tob.rotation_euler = (R(90) - math.atan2(n.z, -n.y), 0, 0)
tob.scale = (0.82, 1.0, 1.0)
bpy.context.view_layer.update()
me6 = bpy.data.meshes.new_from_object(tob.evaluated_get(bpy.context.evaluated_depsgraph_get())); me6.transform(tob.matrix_world)
_bm = bmesh.new(); _bm.from_mesh(me6)
bmesh.ops.remove_doubles(_bm, verts=_bm.verts, dist=2e-5); bmesh.ops.dissolve_degenerate(_bm, dist=1e-7, edges=_bm.edges)
bmesh.ops.recalc_face_normals(_bm, faces=_bm.faces); _bm.to_mesh(me6); _bm.free()
six = bpy.data.objects.new('Chest_Six', me6); coll.objects.link(six); bpy.data.objects.remove(tob)
six.data.materials.append(lib.MATS['white']); PARTS.append((six, 'chest'))
P, N = surf_path(T_chest, F, [(0, 1.815), (0, 1.77), (0, 1.73)], 0.022, n=8)
sweep('Chest_SternumTop', P, 0.014, 0.008, 'silver', 'chest', normals=N, p=3)

# ====================================================================== ABDOMEN (narrow waist, red muscle, segmented column)
abd = vloft('Abdomen_Core', [
    (1.20, 0.0, 0.0, 0.12, 0.085, 0.09), (1.27, 0.0, 0.0, 0.108, 0.078, 0.085), (1.34, 0.0, 0.0, 0.112, 0.083, 0.088),
    (1.41, 0.0, 0.0, 0.132, 0.093, 0.098), (1.47, 0.0, 0.0, 0.16, 0.105, 0.105)], 'muscle', 'spine', p=2.6, nseg=40)
T_abd = bvh(abd)
for s in (1, -1):
    sd = SD(s)
    for k, zc in enumerate((1.255, 1.315, 1.375, 1.435)):
        loc, n = hit(T_abd if zc < 1.42 else T_chest, (s * 0.045, -1, zc), (0, 1, 0))
        if False: ellipsoid('Abdomen_Muscle%d' % k + sd, loc + V((0, 0.004, 0)), 0.024, 0.014, 0.026, 'muscle', 'spine' if zc < 1.42 else 'chest', nseg=20, nz=8)
    for k in range(6):
        z0 = 1.23 + 0.034 * k
        P, N = surf_path(T_abd if z0 < 1.42 else T_chest, cyl_map(lambda z: (0, 0)), [(s * R(a), z0 + 0.03 * ((a - 14) / 146.0) ** 1.3 - 0.012 * math.sin(math.pi * (a - 14) / 146.0)) for a in range(14, 161, 4)], 0.009)
        if len(P) > 3: sweep('Abdomen_SideRib%d' % k + sd, P, lambda tt: 0.0125 * (0.55 + 0.45 * math.sin(math.pi * tt) ** 0.4), 0.012, 'teal' if k % 2 else 'teal2', 'spine' if z0 < 1.42 else 'chest', normals=N, p=2.8)
for k in range(14):
    zc = 1.60 - k * 0.0285
    tree = T_abd if zc < 1.42 else T_chest
    bn = 'spine' if zc < 1.42 else 'chest'
    plate('Abdomen_Column%02d' % k, tree, F, rrect(0.0, zc, 0.0125, 0.0134), 'dark', bn, offset=0.014, thick=0.008)

# ====================================================================== PELVIS
pelv = vloft('Pelvis_Core', [
    (1.02, 0.0, 0.0, 0.09, 0.065, 0.075), (1.06, 0.0, 0.0, 0.145, 0.095, 0.105), (1.13, 0.0, 0.0, 0.165, 0.106, 0.116),
    (1.20, 0.0, 0.0, 0.152, 0.1, 0.108), (1.25, 0.0, 0.0, 0.128, 0.09, 0.094)], 'dark', 'hips', p=2.6, nseg=40)
T_pel = bvh(pelv)
belt = [(2 * math.pi * i / 72, 1.228 - 0.045 * max(0.0, math.cos(2 * math.pi * i / 72)) ** 3) for i in range(72)]
P, N = surf_path(T_pel, cyl_map(lambda z: (0, 0)), belt, 0.012)
sweep('Pelvis_Belt', P, 0.016, 0.012, 'teal', 'hips', normals=N, p=3.0, loop=True)
for s in (1, -1):
    sd = SD(s)
    vp = [(s * 0.025, 1.165), (s * 0.08, 1.185), (s * 0.155, 1.215), (s * 0.165, 1.175), (s * 0.12, 1.14), (s * 0.03, 1.115)]
    plate('Pelvis_VPlate' + sd, T_pel, F, chaikin(vp, 2), 'teal2', 'hips', offset=0.012, thick=0.012)
    disc('Pelvis_HipDisc' + sd, (s * 0.165, 0.0, 1.115), (1, 0, 0), 0.05, 0.03, 'dark', 'hips')
    disc('Pelvis_HipCap' + sd, (s * 0.183, 0.0, 1.115), (1, 0, 0), 0.036, 0.014, 'teal2', 'hips')
    disc('Pelvis_HipHub' + sd, (s * 0.191, 0.0, 1.115), (1, 0, 0), 0.016, 0.01, 'silver', 'hips')
    plate('Pelvis_Butt' + sd, T_pel, B, ellipse(s * 0.07, 1.12, 0.055, 0.06), 'teal2', 'hips', offset=0.006, thick=0.012)
plate('Pelvis_Cod', T_pel, F, chaikin([(-0.045, 1.185), (0.045, 1.185), (0.04, 1.10), (0.0, 1.05), (-0.04, 1.10)], 2), 'dark', 'hips', offset=0.006, thick=0.012)
for k in range(9):
    zc = 1.40 + k * 0.045
    disc('Back_Spine%d' % k, (0, 0.135 if zc > 1.45 else 0.11, zc), (0, 0, 1), 0.022, 0.03, 'dark', 'chest' if zc > 1.42 else 'spine')

# ====================================================================== PAULDRONS (3 smooth cowl plates + deltoid)
PL = [(104, 156, 1.3, 0.028), (70, 116, 1.25, 0.028), (36, 84, 1.2, 0.026), (2, 52, 1.15, 0.024)]
for s in (1, -1):
    sd = SD(s)
    J = V((s * 0.235, 0.0, 1.70))
    # v4: one big smooth hood following the shoulder, lower edge rolled under
    HR = (0.16, 0.226, 0.19); NA, NB = 22, 64
    hood, _ = cowl_shell('Pauldron_Hood' + sd, J, s, HR, -72, 76, -74, 100, 'teal', 'shoulder' + sd,
                         thick=0.03, na=NA, nb=NB, curl_front=0.22, curl_back=0.18, hug=0.22, keep=0.5)
    _hv = hood.data.vertices
    lipP, lipN = [], []
    for j in range(3, NB - 3):
        p = _hv[j * NA].co.copy(); q = _hv[j * NA + 1].co.copy()
        out = (p - J).normalized()
        lipP.append(p - out * 0.006 + (p - q).normalized() * 0.006); lipN.append(out)
    sweep('Pauldron_HoodLip' + sd, lipP, lambda t: 0.017 * (0.4 + 0.6 * math.sin(math.pi * t) ** 0.35), 0.016, 'teal2', 'shoulder' + sd, normals=lipN, p=2.0)
    # bronze trim just above the rolled lip and along the hood's inner edge
    FP, FN, RP = [], [], []
    for i in range(1, NA - 1):
        p = _hv[4 * NA + i].co.copy(); out = (p - J).normalized(); FP.append(p + out * 0.0015); FN.append(out)
        r_ = _hv[1 * NA + i].co.copy(); RP.append(r_ - out * 0.004)
    sweep('Pauldron_HoodTrimFront' + sd, FP, 0.0035, 0.0022, 'bronze', 'shoulder' + sd, normals=FN, sub=0, nseg=8)
    sweep('Pauldron_HoodRim' + sd, RP, lambda t: 0.015 * (0.5 + 0.5 * math.sin(math.pi * t) ** 0.4), 0.014, 'teal2', 'shoulder' + sd, normals=FN, p=2.0)
    for nm, col in (('Pauldron_HoodTrim', 2), ('Pauldron_HoodTrimTop', NA - 2), ('Pauldron_HoodGroove', NA // 2)):
        TP, TN = [], []
        for j in range(6, NB - 8):
            p = _hv[j * NA + col].co.copy(); out = (p - J).normalized()
            TP.append(p + out * 0.0015); TN.append(out)
        sweep(nm + sd, TP, 0.0035, 0.0022, 'bronze', 'shoulder' + sd, normals=TN, sub=0, nseg=8)
    # inner shells: long continuous arcs from behind the shoulder, in toward the neck and down onto the chest V plates
    T_up = bvh_multi([hood] + [o for o, b_ in PARTS if o.name.startswith('Chest_Pec') or o.name in ('Chest_Core', 'Chest_Yoke')])
    Cc = V((s * 0.10, 0.0, 1.64))
    for k, xk in enumerate((0.282, 0.24, 0.198)):
        ctrl = [V((s * (xk + 0.012), 0.06, 1.835)), V((s * (xk + 0.006), 0.03, 1.855)), V((s * xk, -0.03, 1.865)),
                V((s * (xk - 0.03), -0.11, 1.82)), V((s * (xk - 0.075), -0.15, 1.72)), V((s * (xk - 0.12), -0.155, 1.62)), V((s * (xk - 0.145), -0.15, 1.55))]
        AP, AN = [], []
        for p in spline(ctrl, 56):
            d = (p - Cc).normalized(); loc, nn = hit(T_up, Cc + d * 0.6, -d)
            if loc is None: continue
            AP.append(loc + nn * (0.010 + 0.003 * (2 - k))); AN.append(nn)
        if len(AP) < 8: continue
        wfn = lambda t: 0.019 * (0.45 + 0.55 * math.sin(math.pi * t) ** 0.4)
        sweep('Pauldron_Arc%d' % k + sd, AP, wfn, 0.0065, 'teal2' if k % 2 else 'teal', 'shoulder' + sd, normals=AN, p=3.0)
        sweep('Pauldron_ArcGap%d' % k + sd, [p_ - n_ * 0.006 for p_, n_ in zip(AP, AN)], lambda t: wfn(t) + 0.004, 0.003, 'black', 'shoulder' + sd, normals=AN, p=3.0, sub=0)
        # bronze edge trim on the outer (lateral) edge
        BP = []
        for i in range(len(AP)):
            tg = (AP[min(i + 1, len(AP) - 1)] - AP[max(i - 1, 0)]).normalized(); side = tg.cross(AN[i]).normalized()
            if side.x * s < 0: side = -side
            BP.append(AP[i] + side * wfn(i / (len(AP) - 1)) * 0.92 + AN[i] * 0.0055)
        sweep('Pauldron_ArcTrim%d' % k + sd, BP[2:-2], 0.0024, 0.0018, 'bronze', 'shoulder' + sd, normals=AN[2:-2], sub=0, nseg=8)

    ellipsoid('Pauldron_Under' + sd, J + V((-s * 0.015, 0.0, -0.02)), 0.1, 0.11, 0.1, 'dark', 'shoulder' + sd, nseg=32, nz=12)
    disc('Pauldron_Socket' + sd, J + V((s * 0.045, -0.088, -0.055)), (0, -1, 0), 0.045, 0.02, 'black', 'shoulder' + sd, nseg=36)
    disc('Pauldron_SocketRing' + sd, J + V((s * 0.045, -0.099, -0.055)), (0, -1, 0), 0.036, 0.006, 'silver', 'shoulder' + sd, nseg=36)
    disc('Pauldron_SocketHub' + sd, J + V((s * 0.045, -0.104, -0.055)), (0, -1, 0), 0.016, 0.008, 'dark', 'shoulder' + sd, nseg=24)
    # deltoid: one big rounded plate on the outer upper arm with a red inset slot
    J2 = V((s * 0.298, 0.0, 1.60))
    dl, _ = cowl_shell('UpperArm_Deltoid' + sd, J2, s, (0.072, 0.074, 0.105), -72, 74, -82, 82, 'teal', 'upper_arm' + sd, thick=0.015, curl_front=0.0, curl_back=0.0, hug=0.18)
    T_dl = bvh(dl)
    P, N = surf_path(T_dl, side_map(s), [(-0.03, 1.63), (-0.034, 1.575), (-0.03, 1.52)], -0.0015, n=20)
    sweep('UpperArm_Red' + sd, P, lambda t: 0.016 * math.sin(math.pi * (0.04 + 0.92 * t)) ** 0.6, 0.004, 'red', 'upper_arm' + sd, normals=N, p=2.2)
    engrave('UpperArm_RedRim' + sd, T_dl, side_map(s), lens(-0.033, 1.575, 0.022, 0.064, k=1.0) + [lens(-0.033, 1.575, 0.022, 0.064, k=1.0)[0]], 'upper_arm' + sd, w=0.0014, n=60)

# ====================================================================== ARMS
FYS = [-0.03, -0.01, 0.01, 0.029]; FSC = [1.0, 1.1, 1.02, 0.84]; FSEG = [0.038, 0.029, 0.023]; FZ = 1.045
for s in (1, -1):
    sd = SD(s)
    ua = vloft('UpperArm_Shell' + sd, [
        (1.685, s * 0.285, 0.0, 0.045, 0.045, 0.045), (1.64, s * 0.293, 0.0, 0.062, 0.064, 0.06),
        (1.56, s * 0.30, 0.005, 0.06, 0.064, 0.058), (1.49, s * 0.305, 0.01, 0.052, 0.056, 0.05),
        (1.455, s * 0.31, 0.015, 0.044, 0.048, 0.044)], 'teal', 'upper_arm' + sd, p=2.5)
    T_ua = bvh(ua)
    SM = side_map(s)
    for k, yy in enumerate((-0.03, 0.03)):
        engrave('UpperArm_Line%d' % k + sd, T_ua, F, [(s * 0.3 + yy, 1.50), (s * 0.305 + yy * 1.1, 1.475)], 'upper_arm' + sd, n=8)
    # elbow: ball joint + front disc
    ellipsoid('Elbow_Ball' + sd, (s * 0.31, 0.015, 1.44), 0.045, 0.045, 0.045, 'dark', 'forearm' + sd, nseg=32, nz=12)
    disc('Elbow_Cap' + sd, (s * 0.355, 0.015, 1.44), (1, 0, 0), 0.034, 0.016, 'teal2', 'forearm' + sd)
    disc('Elbow_Ring' + sd, (s * 0.364, 0.015, 1.44), (1, 0, 0), 0.025, 0.006, 'black', 'forearm' + sd)
    disc('Elbow_Hub' + sd, (s * 0.368, 0.015, 1.44), (1, 0, 0), 0.013, 0.01, 'silver', 'forearm' + sd)
    disc('Elbow_FrontDisc' + sd, (s * 0.31, -0.035, 1.44), (0, -1, 0), 0.026, 0.012, 'silver', 'forearm' + sd)
    disc('Elbow_FrontLens' + sd, (s * 0.31, -0.042, 1.44), (0, -1, 0), 0.016, 0.006, 'black', 'forearm' + sd)
    fa = vloft('Forearm_Core' + sd, [
        (1.42, s * 0.31, 0.015, 0.04, 0.042, 0.042), (1.32, s * 0.32, 0.008, 0.05, 0.05, 0.05),
        (1.17, s * 0.33, 0.0, 0.036, 0.036, 0.036), (1.135, s * 0.33, 0.0, 0.032, 0.032, 0.032)], 'muscle', 'forearm' + sd, p=2.4)
    for k, (z0, z1, r0, r1) in enumerate(((1.43, 1.335, 0.05, 0.062), (1.35, 1.25, 0.06, 0.058), (1.265, 1.15, 0.055, 0.044))):
        cx0 = s * (0.31 + 0.02 * (1.44 - z0) / 0.31); cx1 = s * (0.31 + 0.02 * (1.44 - z1) / 0.31)
        rings = []
        for t in (0, 0.06, 0.5, 0.94, 1.0):
            z = z0 + (z1 - z0) * t; r = r0 + (r1 - r0) * t; cx = cx0 + (cx1 - cx0) * t
            f = 0.9 if t in (0, 1.0) else 1.0
            rings.append(dict(c=(cx, 0.015 * (z - 1.13) / 0.31, z), rx=r * f, ry=r * 1.02 * f, p=2.6))
        sh = mk('Forearm_Shell%d' % k + sd, tube_bm(rings, 40, arc=(s * R(-150) - R(90) * (1 - s), s * R(150) - R(90) * (1 - s)) if False else None), 'teal' if k != 1 else 'teal2', 'forearm' + sd, sub=1)
    T_fa = bvh_multi([bpy.data.objects['Forearm_Shell%d' % k + sd] for k in range(3)])
    T_fa1 = bvh(bpy.data.objects['Forearm_Shell1' + sd])
    P, N = surf_path(T_fa1, SM, [(-0.004, 1.345), (-0.004, 1.30), (-0.004, 1.255)], 0.001, n=16)
    sweep('Forearm_RedSlot' + sd, P, lambda t: 0.008 * math.sin(math.pi * (0.04 + 0.92 * t)) ** 0.5, 0.004, 'muscle', 'forearm' + sd, normals=N, p=2.2)
    rim('Forearm_SlotRim' + sd, T_fa1, SM, lens(-0.004, 1.30, 0.015, 0.052, k=1.0), 'silver', 'forearm' + sd, 0.004, 0.004, 0.006)
    engrave('Forearm_FrontLine' + sd, T_fa, F, [(s * 0.30, 1.42), (s * 0.31, 1.33), (s * 0.32, 1.17)], 'forearm' + sd, n=24, w=0.0013)
    disc('Wrist_Ring' + sd, (s * 0.332, 0.0, 1.13), (0, 0, 1), 0.036, 0.02, 'dark', 'hand' + sd)
    # ---------------- HAND (slender)
    hx = s * 0.335
    palm = [dict(c=(hx, 0.0, z), rx=rx, ry=ry, p=4.0) for z, rx, ry in ((1.122, 0.014, 0.032), (1.112, 0.017, 0.04), (1.07, 0.017, 0.043), (1.05, 0.016, 0.042), (1.042, 0.012, 0.038))]
    po = mk('Hand_Palm' + sd, tube_bm(palm, 32), 'dark', 'hand' + sd)
    T_po = bvh(po)
    plate('Hand_Back' + sd, T_po, SM, rrect(0.0, 1.08, 0.034, 0.03), 'teal', 'hand' + sd, offset=0.002, thick=0.007)
    for j in range(4):
        z = FZ
        for k in range(3):
            L = FSEG[k] * FSC[j]; r = 0.0076 - 0.0008 * k
            bn = 'f%d_%d%s' % (j, k + 1, sd)
            rings = [dict(c=(hx, FYS[j], z - L * t), rx=r * (0.85 if t in (0, 1) else 1.0) * (1 - 0.1 * t), ry=r * 1.05 * (0.85 if t in (0, 1) else 1.0), p=3.2) for t in (0, 0.08, 0.5, 0.92, 1.0)]
            mk('Finger%d_%d%s' % (j, k, sd), tube_bm(rings, 16), 'teal' if k != 1 else 'teal2', bn)
            disc('Knuckle%d_%d%s' % (j, k, sd), (hx, FYS[j], z), (0, 1, 0), r * 0.85, r * 2.3, 'dark', bn, nseg=16)
            caps = [dict(c=(hx + s * r * 0.55, FYS[j], z - L * t), rx=r * 0.82 * f, ry=r * 1.32 * f, p=2.6) for t, f in ((0.02, 0.7), (0.1, 1.0), (0.55, 1.04), (0.9, 0.96), (0.98, 0.62 if k == 2 else 0.8))]
            mk('Finger%d_%d_Armor%s' % (j, k, sd), tube_bm(caps, 20), 'teal' if k != 1 else 'teal2', bn)
            for e in (-1, 1):
                bolt('Knuckle%d_%d_Pin%s%s' % (j, k, 'a' if e < 0 else 'b', sd), (hx, FYS[j] + e * r * 1.15, z), (0, e, 0), bn, r=0.0022, h=0.002)
            prs = [dict(c=(hx - s * r * 0.85, FYS[j], z - L * t), u=(0, 1, 0), v=(1, 0, 0), rx=r * 0.7 * (0.6 if t in (0.15, 0.85) else 1), ry=0.0025, p=3) for t in (0.15, 0.25, 0.75, 0.85)]
            mk('Finger%d_%d_Pad%s' % (j, k, sd), tube_bm(prs, 12), 'dark', bn, sub=0)
            z -= L
    tb = V((s * 0.322, -0.04, 1.105)); td = V((-s * 0.25, -0.55, -0.8)).normalized(); p0 = tb
    for k, L in enumerate((0.032, 0.027, 0.022)):
        p1 = p0 + td * L
        rod('Thumb_%d%s' % (k, sd), p0, p1, 0.0085 - 0.001 * k, 'teal' if k != 1 else 'teal2', 'thumb_%d%s' % (k + 1, sd), p=3.0, nseg=16)
        disc('ThumbKnuckle_%d%s' % (k, sd), p0, td.cross(V((0, 0, 1))), 0.0075, 0.019, 'dark', 'thumb_%d%s' % (k + 1, sd), nseg=16)
        p0 = p1

# ====================================================================== LEGS
for s in (1, -1):
    sd = SD(s)
    th = vloft('Thigh_Shell' + sd, [
        (1.15, s * 0.105, 0.0, 0.078, 0.082, 0.082), (1.10, s * 0.11, -0.005, 0.086, 0.094, 0.092),
        (1.00, s * 0.113, -0.01, 0.083, 0.092, 0.088), (0.88, s * 0.116, -0.012, 0.075, 0.084, 0.08),
        (0.76, s * 0.118, -0.012, 0.065, 0.074, 0.07), (0.67, s * 0.12, -0.01, 0.057, 0.064, 0.06),
        (0.64, s * 0.12, -0.01, 0.048, 0.052, 0.052)], 'teal', 'thigh' + sd, p=2.4, nseg=40)
    T_th = bvh(th)
    SM = side_map(s)
    plate('Thigh_Red' + sd, T_th, SM, lens(-0.012, 0.88, 0.016, 0.17, k=1.0), 'muscle', 'thigh' + sd, offset=0.002, thick=0.008)
    rim('Thigh_RedRim' + sd, T_th, SM, lens(-0.012, 0.88, 0.024, 0.182, k=1.0), 'teal2', 'thigh' + sd, 0.008, 0.006, 0.009)
    plate('Thigh_FrontPlate' + sd, T_th, F, lens(s * 0.105, 0.90, 0.045, 0.18, k=0.9), 'teal2', 'thigh' + sd, offset=0.001, thick=0.004)
    for k, yy in enumerate((-0.055, 0.045)):
        engrave('Thigh_Line%d' % k + sd, T_th, SM, [(yy, 1.12), (yy * 1.1, 0.95), (yy * 0.9, 0.80), (yy * 0.7, 0.69)], 'thigh' + sd, n=30, w=0.0014)
    for k in range(3):
        rod('Thigh_Hydraulic%d' % k + sd, (s * (0.08 + 0.03 * k), 0.07, 1.06), (s * (0.09 + 0.025 * k), 0.06, 0.70), 0.008, 'dark' if k != 1 else 'silver', 'thigh' + sd)
        a = V((s * (0.08 + 0.03 * k), 0.07, 1.06)); bb = V((s * (0.09 + 0.025 * k), 0.06, 0.70))
        for j, t in enumerate((0.04, 0.5, 0.96)):
            disc('Thigh_HydCollar%d_%d' % (k, j) + sd, a.lerp(bb, t), bb - a, 0.0115, 0.012, 'silver' if j != 1 else 'dark', 'thigh' + sd, nseg=12)
    # knee: layered caps
    disc('Knee_Joint' + sd, (s * 0.12, -0.01, 0.62), (1, 0, 0), 0.062, 0.12, 'dark', 'shin' + sd)
    disc('Knee_SideCap' + sd, (s * 0.175, -0.01, 0.62), (1, 0, 0), 0.04, 0.014, 'teal2', 'shin' + sd)
    disc('Knee_Hub' + sd, (s * 0.184, -0.01, 0.62), (1, 0, 0), 0.017, 0.012, 'silver', 'shin' + sd)
    for k, (zc, w, hgt, yo) in enumerate(((0.68, 0.066, 0.05, -0.062), (0.632, 0.074, 0.056, -0.072), (0.58, 0.064, 0.046, -0.064))):
        kc = [dict(c=(s * 0.12, yo, zc + hgt * t), rx=w * math.sqrt(max(0.05, 1 - t * t)), ry=0.04 * math.sqrt(max(0.05, 1 - t * t)), ryb=0.014, p=2.4) for t in (-1, -0.7, -0.3, 0.2, 0.7, 1.0)]
        if False: mk('Knee_Cap%d' % k + sd, tube_bm(kc, 32), 'teal' if k != 1 else 'teal2', 'shin' + sd)
    _kp = spline([V((s * 0.12, -0.062, 0.735)), V((s * 0.12, -0.084, 0.665)), V((s * 0.12, -0.086, 0.61)), V((s * 0.12, -0.07, 0.535))], 40)
    sweep('Knee_Plate' + sd, _kp, lambda t: 0.058 * math.sin(math.pi * t) ** 0.75 + 0.005, lambda t: 0.016 * math.sin(math.pi * t) ** 0.5 + 0.003, 'teal', 'shin' + sd, ref=(0, -1, 0.2), p=3.2)
    _kr = spline([V((s * 0.12, -0.075, 0.705)), V((s * 0.12, -0.104, 0.64)), V((s * 0.12, -0.096, 0.575))], 24)
    sweep('Knee_Ridge' + sd, _kr, lambda t: 0.005 * math.sin(math.pi * t) ** 0.5 + 0.0015, 0.004, 'silver', 'shin' + sd, ref=(0, -1, 0.2), p=2.4)
    sh_ = vloft('Shin_Shell' + sd, [
        (0.60, s * 0.12, -0.0, 0.055, 0.06, 0.062), (0.54, s * 0.12, 0.0, 0.06, 0.064, 0.076),
        (0.44, s * 0.12, 0.005, 0.056, 0.06, 0.074), (0.32, s * 0.12, 0.01, 0.049, 0.052, 0.06),
        (0.20, s * 0.12, 0.015, 0.041, 0.044, 0.045), (0.135, s * 0.12, 0.02, 0.039, 0.041, 0.041),
        (0.115, s * 0.12, 0.02, 0.031, 0.033, 0.033)], 'teal', 'shin' + sd, p=2.4, nseg=40)
    T_sn = bvh(sh_)
    SCM = cyl_map(lambda z, s=s: (s * 0.12, 0.01))
    plate('Shin_Red' + sd, T_sn, SCM, lens(s * 0.5, 0.38, 0.72, 0.205, k=0.8), 'red', 'shin' + sd, offset=0.002, thick=0.008)
    rim('Shin_RedRim' + sd, T_sn, SCM, lens(s * 0.5, 0.38, 0.84, 0.222, k=0.8), 'silver', 'shin' + sd, 0.008, 0.005, 0.008)
    plate('Shin_FrontRed' + sd, T_sn, F, lens(s * 0.12, 0.38, 0.007, 0.16, k=1.0), 'red', 'shin' + sd, offset=0.002, thick=0.005)
    for k, xx in enumerate((-0.022, 0.022)):
        engrave('Shin_Line%d' % k + sd, T_sn, F, [(s * 0.12 - s * abs(xx) * 1.4 if k else s * 0.12 + xx, 0.56), (s * 0.12 + (xx * 0.9 if not k else -s * abs(xx) * 1.3), 0.38), (s * 0.12 + (xx * 0.7 if not k else -s * abs(xx)), 0.18)], 'shin' + sd, n=30, w=0.0014)
    plate('Shin_Calf' + sd, T_sn, B, lens(s * 0.12, 0.42, 0.04, 0.14, k=0.7), 'teal2', 'shin' + sd, offset=0.005, thick=0.012)
    for k in range(3):
        P = spline([(s * (0.10 + 0.02 * k), 0.085, 0.56), (s * (0.10 + 0.02 * k), 0.095, 0.38), (s * (0.105 + 0.015 * k), 0.07, 0.17)], 20)
        sweep('Shin_Cable%d' % k + sd, P, 0.0042, 0.0042, 'dark', 'shin' + sd, ref=(1, 0, 0), nseg=10)
        for j, pp in enumerate((P[0], P[10], P[-1])):
            disc('Shin_CableClamp%d_%d' % (k, j) + sd, pp, (0, 0, 1), 0.006, 0.006, 'silver', 'shin' + sd, nseg=10, sub=0)
    # ankle + armoured boot (pointed, no toes)
    disc('Ankle_Joint' + sd, (s * 0.12, 0.02, 0.105), (1, 0, 0), 0.034, 0.095, 'dark', 'foot' + sd)
    disc('Ankle_Cap' + sd, (s * 0.168, 0.02, 0.105), (1, 0, 0), 0.025, 0.01, 'teal2', 'foot' + sd)
    ft = [dict(c=(s * 0.12, y, z), u=(1, 0, 0), v=(0, 0, 1), rx=rx, ry=ry, p=pp) for y, z, rx, ry, pp in (
        (0.085, 0.052, 0.03, 0.038, 3.0), (0.075, 0.056, 0.044, 0.052, 3.0), (0.03, 0.06, 0.049, 0.06, 3.0), (-0.03, 0.05, 0.05, 0.047, 2.8),
        (-0.09, 0.036, 0.046, 0.034, 2.6), (-0.14, 0.026, 0.036, 0.024, 2.4), (-0.18, 0.018, 0.02, 0.015, 2.2), (-0.198, 0.014, 0.006, 0.008, 2.0))]
    fo = mk('Foot_Shell' + sd, tube_bm(ft, 32), 'teal', 'foot' + sd)
    T_fo = bvh(fo)
    plate('Foot_TopPlate' + sd, T_fo, top_map(), chaikin([(s * 0.095, 0.02), (s * 0.145, 0.02), (s * 0.15, -0.08), (s * 0.12, -0.17), (s * 0.09, -0.08)], 2), 'teal2', 'foot' + sd, offset=0.003, thick=0.008)
    P, N = surf_path(T_fo, top_map(), [(s * 0.12, 0.03), (s * 0.12, -0.08), (s * 0.12, -0.18)], 0.009, n=20)
    sweep('Foot_Ridge' + sd, P, 0.006, 0.005, 'silver', 'foot' + sd, normals=N, p=2.6)
    P = [V((s * 0.12 + 0.05 * math.cos(a), 0.02 + 0.06 * math.sin(a), 0.004)) for a in [math.pi * i / 20 for i in range(21)]]
    sweep('Foot_Heel' + sd, P, 0.01, 0.005, 'dark', 'foot' + sd, ref=(0, 0, 1))
    ft2 = [(s * 0.12 + 0.052 * math.cos(R(a)) * (1.0 if a < 180 else 0.95), -0.05 + 0.135 * math.sin(R(a)) if math.sin(R(a)) < 0 else -0.05 + 0.13 * math.sin(R(a))) for a in range(0, 360, 10)]
    rings = [dict(c=(s * 0.12, -0.06, 0.003 + 0.006 * t), rx=0.054, ry=0.14, p=2.2) for t in (0, 1)]
    mk('Foot_Sole' + sd, tube_bm(rings, 40), 'dark', 'foot' + sd)

# ====================================================================== DETAIL PASS
OBJ = bpy.data.objects
def T(name): return bvh(OBJ[name])
for s in (1, -1):
    sd = SD(s); S_ = side_map(s)
    bolts_outline('Thigh_Rim' + sd, T('Thigh_RedRim' + sd), S_, lens(-0.012, 0.88, 0.024, 0.182, k=1.0), 10, 'thigh' + sd, r=0.003)
    bolts_outline('Shin_Rim' + sd, T('Shin_RedRim' + sd), cyl_map(lambda z, s=s: (s * 0.12, 0.01)), lens(s * 0.5, 0.38, 0.84, 0.222, k=0.8), 10, 'shin' + sd, r=0.003)
    bolts_outline('Forearm_SlotRim' + sd, T('Forearm_SlotRim' + sd), S_, lens(-0.004, 1.30, 0.015, 0.052, k=1.0), 6, 'forearm' + sd, r=0.0024)
    bolts_outline('Pelvis_VPlate' + sd, T('Pelvis_VPlate' + sd), F, [(s * 0.025, 1.165), (s * 0.08, 1.185), (s * 0.155, 1.215), (s * 0.165, 1.175), (s * 0.12, 1.14), (s * 0.03, 1.115)], 5, 'hips', r=0.0034, shrink=0.75)
    bolts_outline('Hand_Back' + sd, T('Hand_Back' + sd), S_, rrect(0.0, 1.08, 0.034, 0.03), 8, 'hand' + sd, r=0.0023, shrink=0.8)
    bolts_outline('Foot_Top' + sd, T('Foot_TopPlate' + sd), top_map(), [(s * 0.095, 0.02), (s * 0.145, 0.02), (s * 0.15, -0.08), (s * 0.12, -0.17), (s * 0.09, -0.08)], 6, 'foot' + sd, r=0.003, shrink=0.75)
    bolts_outline('Shin_Calf' + sd, T('Shin_Calf' + sd), B, lens(s * 0.12, 0.42, 0.04, 0.14, k=0.7), 6, 'shin' + sd, r=0.003, shrink=0.8)
    bolts_outline('Pelvis_Butt' + sd, T('Pelvis_Butt' + sd), B, ellipse(s * 0.07, 1.12, 0.055, 0.06), 6, 'hips', r=0.0032, shrink=0.78)
    for nm, c, bn, rr, nb in (('Elbow', (s * 0.355, 0.015, 1.44), 'forearm' + sd, 0.028, 12), ('Knee', (s * 0.175, -0.01, 0.62), 'shin' + sd, 0.032, 14),
                              ('Hip', (s * 0.19, 0.0, 1.115), 'hips', 0.029, 12), ('Ankle', (s * 0.168, 0.02, 0.105), 'foot' + sd, 0.02, 10)):
        c = V(c)
        ring = [c + V((s * 0.006, rr * math.cos(2 * math.pi * i / 48), rr * math.sin(2 * math.pi * i / 48))) for i in range(48)]
        sweep(nm + '_Race' + sd, ring, 0.0022, 0.0022, 'dark', bn, normals=[V((s, 0, 0))] * 48, loop=True, nseg=8, sub=0)
        for i in range(nb):
            a = 2 * math.pi * i / nb
            ball(nm + '_Bearing%02d' % i + sd, c + V((s * 0.008, rr * math.cos(a), rr * math.sin(a))), 0.0034, 'silver', bn)
        for i in range(6):
            a = 2 * math.pi * (i + 0.5) / 6
            bolt(nm + '_CapBolt%d' % i + sd, c + V((s * 0.012, rr * 0.55 * math.cos(a), rr * 0.55 * math.sin(a))), (s, 0, 0), bn, r=0.0026)
    c = V((s * 0.27, 0.0, 1.67))
    for i in range(14):
        a = 2 * math.pi * i / 14
        ball('Shoulder_Bearing%02d' % i + sd, c + V((s * 0.03, 0.04 * math.cos(a), 0.04 * math.sin(a))), 0.0045, 'silver', 'upper_arm' + sd)
    for k, (x0, y0, x1, y1) in enumerate(((0.1, 0.06, 0.11, 0.05), (0.12, -0.02, 0.13, -0.03), (0.07, 0.09, 0.08, 0.08))):
        P = spline([(s * x0, y0, 1.46), (s * (x0 + 0.015), y0 + 0.01 * (1 - 2 * (k % 2)), 1.34), (s * x1, y1, 1.22)], 24)
        sweep('Waist_Hose%d' % k + sd, P, 0.007, 0.007, 'dark', 'spine', ref=(1, 0, 0), nseg=12)
        for j, pp in enumerate((P[1], P[-2])):
            d = (P[2] - P[0]) if j == 0 else (P[-1] - P[-3])
            disc('Waist_HoseCollar%d_%d' % (k, j) + sd, pp, d, 0.01, 0.012, 'silver', 'spine', nseg=12)
        for j in range(4, 20, 3):
            disc('Waist_HoseRib%d_%d' % (k, j) + sd, P[j], P[j + 1] - P[j - 1], 0.0083, 0.003, 'dark', 'spine', nseg=12, sub=0)
    for k in range(2):
        P = spline([(s * (0.10 + 0.04 * k), 0.07, 0.76), (s * (0.105 + 0.04 * k), 0.09, 0.62), (s * (0.11 + 0.035 * k), 0.08, 0.50)], 20)
        sweep('Knee_Hose%d' % k + sd, P, 0.0065, 0.0065, 'dark', 'shin' + sd, ref=(1, 0, 0), nseg=12)
        for j, pp in enumerate((P[0], P[-1])):
            disc('Knee_HoseCollar%d_%d' % (k, j) + sd, pp, (0, 0, 1), 0.009, 0.012, 'silver', 'shin' + sd, nseg=12)
        P = spline([(s * (0.27 + 0.02 * k), 0.035, 1.50), (s * (0.27 + 0.02 * k), 0.05, 1.44), (s * (0.285 + 0.02 * k), 0.04, 1.37)], 16)
        sweep('Elbow_Hose%d' % k + sd, P, 0.0045, 0.0045, 'dark', 'forearm' + sd, ref=(1, 0, 0), nseg=10)
    for k in range(3):
        P = spline([(s * 0.343, -0.022 + 0.022 * k, 1.17), (s * 0.35, -0.022 + 0.022 * k, 1.135), (s * 0.346, -0.022 + 0.022 * k, 1.11)], 10)
        sweep('Wrist_Cable%d' % k + sd, P, 0.003, 0.003, 'dark', 'hand' + sd, ref=(0, 1, 0), nseg=8)
    for k in range(2):
        P = spline([(s * (0.05 + 0.012 * k), 0.06, 1.79), (s * (0.042 + 0.01 * k), 0.07, 1.86), (s * (0.03 + 0.008 * k), 0.055, 1.925)], 16)
        sweep('Neck_Hose%d' % k + sd, P, 0.0055, 0.0055, 'dark', 'neck', ref=(1, 0, 0), nseg=10)
    for k in range(3):
        bolts_along('Back_Cage%d' % k + sd, 4, 'chest', r=0.0032, t0=0.15, t1=0.85)
    for k in range(5):
        pass
    for k in range(3): bolts_along('Abdomen_SideRib%d' % k + sd, 2, 'spine', r=0.0025, t0=0.05, t1=0.95)
    bolts_along('Chest_Trap' + sd, 3, 'chest', r=0.0032)
    bolts_along('Chest_Clavicle' + sd, 3, 'chest', r=0.003)
    for k in range(4):
        P = spline([(s * (0.03 + 0.03 * k), 0.15, 1.48), (s * (0.05 + 0.035 * k), 0.17, 1.6), (s * (0.08 + 0.03 * k), 0.15, 1.73)], 20)
        Tc = T('Chest_Core'); lp = []
        for pp in P:
            loc, nn = hit(Tc, V((pp.x, 1.0, pp.z)), (0, -1, 0))
            lp.append((loc + nn * 0.02) if loc else pp)
        sweep('Back_Fibre%d' % k + sd, lp, 0.0055, 0.0055, 'muscle', 'chest', ref=(0, 1, 0), nseg=10)
for k in range(9):
    zc = 1.40 + k * 0.045; yb = 0.135 if zc > 1.45 else 0.11; bn = 'chest' if zc > 1.42 else 'spine'
    for e in (-1, 1):
        P = [V((e * (0.012 + 0.03 * t), yb + 0.012 + 0.012 * math.sin(math.pi * t), zc)) for t in [i / 8 for i in range(9)]]
        sweep('Back_VertebraFin%d%s' % (k, 'L' if e > 0 else 'R'), P, lambda t: 0.006 * (1 - 0.6 * t), 0.004, 'teal2', bn, ref=(0, 0, 1), nseg=10, sub=0)
        bolt('Back_Spine%d_Bolt%s' % (k, 'L' if e > 0 else 'R'), (e * 0.016, yb + 0.012, zc), (e * 0.3, 1, 0), bn, r=0.0028)
    rod('Back_SpineCore%d' % k, (0, yb - 0.01, zc - 0.022), (0, yb - 0.01, zc + 0.022), 0.008, 'silver', bn, nseg=10, sub=0)
for k in range(14):
    zc = 1.60 - k * 0.0285
    for e in (-1, 1):
        loc, nn = hit(T('Abdomen_Column%02d' % k), (e * 0.009, -1, zc), (0, 1, 0))
        if False: bolt('Abdomen_Column%02d_Bolt%s' % (k, 'L' if e > 0 else 'R'), loc, nn, 'spine' if zc < 1.42 else 'chest', r=0.0022, h=0.002)
Tb = T('Pelvis_Belt')
for i in range(20):
    ph = 2 * math.pi * i / 20; z = 1.228 - 0.045 * max(0.0, math.cos(ph)) ** 3
    o = V((math.sin(ph) * 0.6, -math.cos(ph) * 0.6, z))
    loc, nn = hit(Tb, o, -o + V((0, 0, z)))
    if loc: bolt('Pelvis_BeltRivet%02d' % i, loc, nn, 'hips', r=0.0034)
for k in range(6):
    z0 = 1.781 + k * 0.022; r = 0.064 - 0.003 * k; cy = 0.012 + 0.002 * k
    for i in range(6):
        a = 2 * math.pi * (i + 0.5 * (k % 2)) / 6
        bolt('Neck_Ring%d_Bolt%d' % (k, i), V((r * math.cos(a), cy + r * 0.9 * math.sin(a), z0 + 0.007)), V((math.cos(a), math.sin(a), 0)), 'neck', r=0.0022, h=0.002)
bolts_outline('Chest_SixPlate', T('Chest_SixPlate'), F, rrect(0.0, 1.668, 0.027, 0.052), 6, 'chest', r=0.0026, shrink=0.86)

# ---- detail pass 2 (fasteners)
for s in (1, -1):
    sd = SD(s)
    for k in range(4):
        pass
    for k in range(6):
        nm = 'Pauldron_Ridge%d' % k + sd
        if nm in PATHS: bolts_along(nm, 5, 'shoulder' + sd, r=0.0026, t0=0.1, t1=0.9)
    for k in range(3):
        ob = OBJ['Forearm_Shell%d' % k + sd]; tb = bvh(ob)
        z0 = (1.43, 1.35, 1.265)[k] - 0.012
        cx = s * (0.31 + 0.02 * (1.44 - z0) / 0.31)
        for i in range(6):
            a = 2 * math.pi * i / 6 + 0.3
            o = V((cx + 0.3 * math.cos(a), 0.3 * math.sin(a), z0)); dd = V((cx, 0, z0)) - o
            loc, nn = hit(tb, o, dd)
            if loc: bolt('Forearm_Shell%d_Bolt%d' % (k, i) + sd, loc, nn, 'forearm' + sd, r=0.0026)
    for k in range(0):
        tb = bvh(OBJ['Knee_Cap%d' % k + sd]); zc = (0.675, 0.632, 0.585)[k]
        for i in range(5):
            u = -1 + 2 * i / 4
            loc, nn = hit(tb, (s * 0.12 + 0.04 * u, -0.6, zc + 0.01 * (1 - u * u)), (0, 1, 0))
            if loc: bolt('Knee_Cap%d_Bolt%d' % (k, i) + sd, loc, nn, 'shin' + sd, r=0.0026)
    for k in range(4):
        tb = bvh(OBJ['Abdomen_Muscle%d' % k + sd]) if ('Abdomen_Muscle%d' % k + sd) in OBJ else None
    for j in range(4):
        L = FSEG[2] * FSC[j]; z = FZ - sum(FSEG[:2]) * FSC[j] - L
        disc('Finger%d_Tip%s' % (j, sd), (s * 0.335, FYS[j], z + 0.002), (0, 0, 1), 0.0055, 0.004, 'silver', 'f%d_3%s' % (j, sd), nseg=12)

# ---- engraved panel lines on limbs (separate meshes, flush)
for s in (1, -1):
    sd = SD(s)
    for nm, bn, ax, zs in (('Thigh_Shell', 'thigh', (0.115, -0.01), (1.06, 0.98, 0.78, 0.70)), ('Shin_Shell', 'shin', (0.12, 0.01), (0.56, 0.50, 0.22, 0.16)),
                           ('UpperArm_Shell', 'upper_arm', (0.30, 0.008), (1.52, 1.475))):
        tb = bvh(OBJ[nm + sd]); cm = cyl_map(lambda z, ax=ax, s=s: (s * ax[0], ax[1]))
        for k, z in enumerate(zs):
            engrave(nm.split('_')[0] + '_PanelRing%d' % k + sd, tb, cm, [(R(a), z + 0.004 * math.cos(R(a))) for a in range(-150, 151, 6)], bn + sd, w=0.0013)
    for k in range(3):
        tb = bvh(OBJ['Forearm_Shell%d' % k + sd]); z = (1.40, 1.31, 1.22)[k]
        cm = cyl_map(lambda zz, s=s: (s * 0.32, 0.008))
        engrave('Forearm_PanelRing%d' % k + sd, tb, cm, [(R(a), z) for a in range(-150, 151, 6)], 'forearm' + sd, w=0.0012)
print('PARTS2', len(PARTS))
print('PARTS', len(PARTS))

# ====================================================================== POST: bulk limbs, lengthen arms
GS = 0.95  # global scale -> ~2.1 m standing height
HS = 1.12
HEADS = (1.15, 1.17, 1.3)
TORSO_X = 1.16
def bulk(ob, a, b_, fx, fy):
    a = V(a); b_ = V(b_); d = (b_ - a).normalized()
    for v in ob.data.vertices:
        p = v.co
        t = (p - a).dot(d); foot = a + d * t
        off = p - foot
        v.co = foot + V((off.x * fx, off.y * fy, off.z))
def _sc(p, c, f):
    d = p - c
    if isinstance(f, (tuple, list)): return c + V((d.x * f[0], d.y * f[1], d.z * f[2]))
    return c + d * f
def uscale(ob, c, f):
    c = V(c)
    for v in ob.data.vertices:
        v.co = _sc(v.co, c, f)
def zarm(z):
    pts = [(2.0, 2.0), (1.70, 1.70), (1.44, 1.38), (1.13, 1.06), (0.9, 0.83)]
    for i in range(len(pts) - 1):
        (z0, w0), (z1, w1) = pts[i], pts[i + 1]
        if z1 <= z <= z0:
            f = (z - z0) / (z1 - z0); return w0 + (w1 - w0) * f
    return z - 0.07 if z < 0.9 else z
BULK = {'upper_arm': ((0.285, 0, 1.68), (0.31, 0.015, 1.44), 1.2, 1.2),
        'forearm': ((0.31, 0.015, 1.44), (0.33, 0, 1.13), 1.28, 1.28),
        'thigh': ((0.11, 0, 1.10), (0.12, -0.01, 0.62), 1.45, 1.62),
        'shin': ((0.12, -0.01, 0.62), (0.12, 0.02, 0.11), 1.4, 1.48)}
for ob, bn in PARTS:
    if ob.type != 'MESH': continue
    base, sd = (bn[:-2], bn[-1]) if bn[-2:] in ('.L', '.R') else (bn, '')
    sgn = -1 if sd == 'R' else 1
    # bake modifiers other than subsurf first
    if any(m.type != 'SUBSURF' for m in ob.modifiers):
        subs = [(m.levels, m.render_levels) for m in ob.modifiers if m.type == 'SUBSURF']
        for m in list(ob.modifiers):
            if m.type == 'SUBSURF': ob.modifiers.remove(m)
        dg = bpy.context.evaluated_depsgraph_get()
        nm = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        old = ob.data; ob.data = nm; nm.name = ob.name
        for m in list(ob.modifiers): ob.modifiers.remove(m)
        bpy.data.meshes.remove(old)
        for lv, rl in subs:
            m = ob.modifiers.new('Subsurf', 'SUBSURF'); m.levels = lv; m.render_levels = rl
    if base in BULK:
        a, b_, fx, fy = BULK[base]
        bulk(ob, (sgn * a[0], a[1], a[2]), (sgn * b_[0], b_[1], b_[2]), fx, fy)
    if base == 'foot':
        uscale(ob, (sgn * 0.12, 0.02, 0.11), 1.12)
    if base == 'head':
        uscale(ob, (0, 0.02, 1.91), HEADS)
    if base in ('chest', 'spine', 'shoulder'):
        for v in ob.data.vertices: v.co.x *= TORSO_X
    if (base.startswith('f') and base[1:2].isdigit()) or base.startswith('thumb'):
        _c = sum((v.co for v in ob.data.vertices), V()) / max(1, len(ob.data.vertices))
        for v in ob.data.vertices:
            v.co = V((_c.x + (v.co.x - _c.x) * 1.45, _c.y + (v.co.y - _c.y) * 1.45, v.co.z))
    if base == 'hand' or base.startswith('f') and base[1:2].isdigit() or base.startswith('thumb'):
        uscale(ob, (sgn * 0.332, 0, 1.13), HS)
    if base in ('upper_arm', 'forearm', 'hand') or base.startswith('thumb') or (base.startswith('f') and base[1:2].isdigit()):
        for v in ob.data.vertices:
            v.co.z = zarm(v.co.z)
    for v in ob.data.vertices:
        v.co *= GS
    _bm = bmesh.new(); _bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(_bm, verts=_bm.verts, dist=1e-6)
    bmesh.ops.dissolve_degenerate(_bm, dist=1e-7, edges=_bm.edges)
    loose = [v for v in _bm.verts if not v.link_faces]
    if loose: bmesh.ops.delete(_bm, geom=loose, context='VERTS')
    _bm.to_mesh(ob.data); _bm.free()

print('PARTS', len(PARTS))

# push dome stripe/panels fully outside the (subdivided) skull surface
from mathutils.bvhtree import BVHTree as _BT
_dg = bpy.context.evaluated_depsgraph_get()
_se = skull.evaluated_get(_dg); _sm = _se.to_mesh()
_T = _BT.FromPolygons([v.co.copy() for v in _sm.vertices], [tuple(p.vertices) for p in _sm.polygons])
_C = sum((v.co for v in _sm.vertices), V()) / len(_sm.vertices)
_se.to_mesh_clear()
for _n in ('Head_CentreStripe', 'Head_DomePanel.L', 'Head_DomePanel.R'):
    _o = bpy.data.objects[_n]; _moved = 0
    for _m in list(_o.modifiers): _o.modifiers.remove(_m)
    _bm = bmesh.new(); _bm.from_mesh(_o.data)
    for _i in range(2): bmesh.ops.subdivide_edges(_bm, edges=_bm.edges[:], cuts=1, use_grid_fill=True, smooth=0.0)
    bmesh.ops.triangulate(_bm, faces=[f for f in _bm.faces if len(f.verts) > 4])
    _bm.to_mesh(_o.data); _bm.free(); _o.data.shade_smooth()
    for v in _o.data.vertices:
        d = v.co - _C; L = d.length; d.normalize()
        h = _T.ray_cast(_C, d)
        if not h[0]: continue
        hd = (h[0] - _C).length
        tgt = hd + ((0.0062 if v.normal.dot(d) > 0 else 0.0008) if _n == 'Head_CentreStripe' else (0.0028 if v.normal.dot(d) > 0 else 0.0012)) * GS
        v.co = _C + d * tgt; _moved += 1
    print('STRIPEFIX', _n, _moved)
# ====================================================================== ARMATURE
arm_data = bpy.data.armatures.new('RobotRig')
arm = bpy.data.objects.new('RobotRig', arm_data); coll.objects.link(arm)
arm.show_in_front = True
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')
eb = arm_data.edit_bones
def xf(name, p):
    p = V(p)
    base, sd = (name[:-2], name[-1]) if name[-2:] in ('.L', '.R') else (name, '')
    sgn = -1 if sd == 'R' else 1
    if base == 'foot':
        p = V((sgn * 0.12, 0.02, 0.11)) + (p - V((sgn * 0.12, 0.02, 0.11))) * 1.12
    if base == 'head':
        p = _sc(p, V((0, 0.02, 1.91)), HEADS)
    if base == 'hand' or base.startswith('thumb') or (base.startswith('f') and base[1:2].isdigit()):
        p = V((sgn * 0.332, 0, 1.13)) + (p - V((sgn * 0.332, 0, 1.13))) * HS
    if base in ('upper_arm', 'forearm', 'hand') or base.startswith('thumb') or (base.startswith('f') and base[1:2].isdigit()):
        p.z = zarm(p.z)
    return p * GS
def bone(name, h, t, parent=None):
    b = eb.new(name); b.head = xf(name, h); b.tail = xf(name, t)
    if parent: b.parent = eb[parent]
    return b
bone('root', (0, 0, 0), (0, 0.3, 0))
bone('hips', (0, 0, 1.10), (0, 0, 1.22), 'root')
bone('spine', (0, 0, 1.22), (0, 0, 1.42), 'hips')
bone('chest', (0, 0, 1.42), (0, 0, 1.78), 'spine')
bone('neck', (0, 0.012, 1.785), (0, 0.02, 1.91), 'chest')
bone('head', (0, 0.02, 1.91), (0, 0.03, 2.12), 'neck')
for s in (1, -1):
    sd = '.L' if s > 0 else '.R'
    bone('shoulder' + sd, (s * 0.05, 0, 1.76), (s * 0.27, 0, 1.70), 'chest')
    bone('upper_arm' + sd, (s * 0.285, 0, 1.68), (s * 0.31, 0.015, 1.44), 'shoulder' + sd)
    bone('forearm' + sd, (s * 0.31, 0.015, 1.44), (s * 0.33, 0, 1.13), 'upper_arm' + sd)
    bone('hand' + sd, (s * 0.33, 0, 1.13), (s * 0.335, 0, 1.045), 'forearm' + sd)
    fys = FYS; fsc = FSC; seg = FSEG
    for j in range(4):
        z = FZ; par = 'hand' + sd
        for k in range(3):
            L = seg[k] * fsc[j]
            n = 'f%d_%d%s' % (j, k + 1, sd)
            bone(n, (s * 0.335, fys[j], z), (s * 0.335, fys[j], z - L), par)
            par = n; z -= L
    tb = V((s * 0.322, -0.04, 1.105)); td = V((-s * 0.25, -0.55, -0.8)).normalized(); par = 'hand' + sd
    for k, L in enumerate((0.032, 0.027, 0.022)):
        n = 'thumb_%d%s' % (k + 1, sd)
        bone(n, tb, tb + td * L, par); par = n; tb = tb + td * L
    bone('thigh' + sd, (s * 0.11, 0, 1.10), (s * 0.12, -0.01, 0.62), 'hips')
    bone('shin' + sd, (s * 0.12, -0.01, 0.62), (s * 0.12, 0.02, 0.11), 'thigh' + sd)
    bone('foot' + sd, (s * 0.12, 0.02, 0.11), (s * 0.12, -0.16, 0.03), 'shin' + sd)
for b in eb:
    b.roll = 0.0
bpy.ops.object.mode_set(mode='OBJECT')

bpy.context.view_layer.update()
for ob, bn in PARTS:
    mw = ob.matrix_world.copy()
    ob.parent = arm; ob.parent_type = 'BONE'; ob.parent_bone = bn
    pb = arm.pose.bones[bn]
    ob.matrix_parent_inverse = (arm.matrix_world @ pb.bone.matrix_local @ Matrix.Translation((0, pb.bone.length, 0))).inverted()
    ob.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()

# ====================================================================== POSES
for pb in arm.pose.bones:
    pb.rotation_mode = 'QUATERNION'

def q_world(axis, deg):
    return Quaternion(V(axis), R(deg))

def set_rot(name, q):
    pb = arm.pose.bones[name]
    Rm = pb.bone.matrix_local.to_quaternion()
    pb.rotation_quaternion = Rm.inverted() @ q @ Rm

def reset():
    for pb in arm.pose.bones:
        pb.rotation_quaternion = Quaternion(); pb.location = V()

exec(open('/workspace/robot/v4/poses.py').read())

def key_all(action_name):
    act = bpy.data.actions.new(action_name)
    arm.animation_data_create()
    arm.animation_data.action = act
    for pb in arm.pose.bones:
        pb.keyframe_insert('rotation_quaternion', frame=1, group=pb.name)
        pb.keyframe_insert('location', frame=1, group=pb.name)
    act.use_fake_user = True
    return act

reset(); pose_standing(); bpy.context.view_layer.update()
act_stand = key_all('Standing')
arm.animation_data.action = None
reset(); pose_thinker(); bpy.context.view_layer.update()
act_think = key_all('Thinker')
for act in (act_stand, act_think):
    tr = arm.animation_data.nla_tracks.new(); tr.name = act.name
    tr.strips.new(act.name, 1, act); tr.mute = True
arm.animation_data.action = act_think

# ====================================================================== STAGE
stage = bpy.data.collections.new('Stage'); scene.collection.children.link(stage)
# stepped stone plinth (top at PEDESTAL_TOP*GS)
ped_h = SEAT_Z if SEAT_Z else PEDESTAL_TOP * GS
def slab(name, sx, sy, z0, z1, bev=0.012):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= sx; v.co.y *= sy; v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); stage.objects.link(o); o.location = PEDESTAL_LOC
    me.materials.append(lib.MATS['concrete'])
    m = o.modifiers.new('Bevel', 'BEVEL'); m.width = bev; m.segments = 3
    return o
ped = slab('Pedestal', 0.50, 0.50, ped_h * 0.36, ped_h * 0.92)
slab('Pedestal_Base', 0.86, 0.80, 0.0, ped_h * 0.18, 0.015)
slab('Pedestal_Step', 0.66, 0.64, ped_h * 0.18, ped_h * 0.36, 0.015)
slab('Pedestal_Cap', 0.56, 0.55, ped_h * 0.92, ped_h, 0.008)
# backdrop: cyclorama bowl
bm = bmesh.new()
prof = [(r, 0.0) for r in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0)]
for i in range(1, 21):
    a = math.pi / 2 * i / 20
    prof.append((5.0 + 3.0 * math.sin(a), 3.0 - 3.0 * math.cos(a)))
prof.append((8.0, 12.0))
NS = 96
grid = []
for r, z in prof:
    grid.append([bm.verts.new((r * math.cos(2 * math.pi * j / NS), r * math.sin(2 * math.pi * j / NS), z)) for j in range(NS)])
for i in range(len(prof) - 1):
    for j in range(NS):
        try: bm.faces.new((grid[i][j], grid[i][(j + 1) % NS], grid[i + 1][(j + 1) % NS], grid[i + 1][j]))
        except ValueError: pass
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
me = bpy.data.meshes.new('Backdrop'); bm.to_mesh(me); bm.free(); me.shade_smooth()
bd = bpy.data.objects.new('Backdrop', me); stage.objects.link(bd); me.materials.append(lib.MATS['backdrop'])
# world + lights
world = bpy.data.worlds.new('Studio'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.75, 0.75, 0.76, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
def area(name, loc, target, power, size, color=(1, 1, 1)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = power; ld.size = size; ld.color = color
    lo = bpy.data.objects.new(name, ld); stage.objects.link(lo); lo.location = loc
    d = V(target) - V(loc); lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('Key', (-2.6, -3.2, 3.8), (0, 0, 1.0), 650, 2.5, (1.0, 0.97, 0.92))
area('Fill', (3.2, -2.4, 1.8), (0, 0, 1.0), 180, 3.0, (0.92, 0.96, 1.0))
area('Rim', (1.5, 3.0, 3.5), (0, 0, 1.2), 600, 1.5)
area('Top', (0, -0.5, 4.5), (0, 0, 1.0), 120, 2.0)

target = bpy.data.objects.new('CamTarget', None); stage.objects.link(target)
def cam(name, loc, tgt, lens):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    co = bpy.data.objects.new(name, cd); stage.objects.link(co); co.location = loc
    d = V(tgt) - V(loc); co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return co
for name, (loc, tgt, lens) in cameras().items():
    cam(name, loc, tgt, lens)
scene.camera = bpy.data.objects['Cam_Front']

# render settings
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.render.resolution_x = 1024; scene.render.resolution_y = 1365
scene.view_settings.view_transform = 'AgX'
try: scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
scene.render.film_transparent = False
scene.cycles.max_bounces = 8
scene.view_settings.exposure = -0.5
# bloom on the hot eye cores only (threshold well above the lit armour)
scene.use_nodes = True; _nt = scene.node_tree; _nt.nodes.clear()
_rl = _nt.nodes.new('CompositorNodeRLayers'); _gl = _nt.nodes.new('CompositorNodeGlare'); _cp = _nt.nodes.new('CompositorNodeComposite')
_gl.glare_type = 'FOG_GLOW'; _gl.quality = 'HIGH'; _gl.threshold = 4.0; _gl.size = 7; _gl.mix = 0.0
_nt.links.new(_rl.outputs['Image'], _gl.inputs['Image']); _nt.links.new(_gl.outputs['Image'], _cp.inputs['Image'])

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, os.environ.get('BUILD_NAME', 'robot_build.blend')))
print('SAVED')
