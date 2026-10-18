"""pelvis (ON-MODEL conform, round 2) - curved belt of SEPARATE overlapping olive-bronze plates (real dark seams, hex
fasteners with washers) with pointed hip fins, teal lining, bronze lower lip, tapering olive-bronze lamed codpiece,
gunmetal hip pods with stepped bearing rings, tucked hip joints and mechanism, hoses with clamps, sacrum lobes and
lumbar blocks.  Built in WORLD coordinates of the standing A-pose.  See pelvis.NOTES.md (Conform round 2).

Units: P(x, y, z) and the helper functions below work in head-heights (H = 0.2554 m); the figure faces -Y."""
import math
import bpy
from mathutils import Vector

import seis_lib as L
import seis_spec as S
import pelvis_kit as K
from pelvis_kit import P, H, fin, mk, mirror

PI = math.pi
# plan of the belt centre line (superellipse, H units).  Tip span 0.377 m = 1.47 H_m -> half 0.735 H at the fin tips.
A_BELT, B_BELT, NP = 0.745, 0.480, 2.8
FLARE, FZ0, FZ1 = 0.075, 4.70, 5.30      # funnel flare of the belt: the bowl opens outward toward the fin tips (f07, f08)
PA0, PA_TIP = 0.056, 0.018          # radial half-thickness of the band at the front / at the fin tips


def xn(x):
    return min(1.0, abs(x) / A_BELT)


def sstep(a, b, v):
    t = L.clamp((v - a) / (b - a))
    return t * t * (3 - 2 * t)


def band_top(x, y):
    """top edge of the belt band: dips at the centre front, rises to the pointed hip fins (tips 0.51 m below the chin)"""
    s = sstep(-0.10, 0.20, y)                                   # 0 front .. 1 back
    f = 4.860 + 0.300 * xn(x) ** 2.0 + 0.140 * xn(x) ** 7.0
    b = 5.020 + 0.220 * xn(x) ** 2.0 + 0.060 * xn(x) ** 8.0
    return f + (b - f) * s


def band_bot(x, y):
    return 4.660 + 0.140 * xn(x) ** 1.6


def band_pa(x, y):
    return PA0 - (PA0 - PA_TIP) * xn(x) ** 2.0


def wall_x(y, A=A_BELT, B=B_BELT, n=NP):
    """x of the belt centre line at plan position y (H units)."""
    return A * max(0.0, 1.0 - (abs(y) / B) ** n) ** (1.0 / n)


zc_band = lambda x, y: 0.5 * (band_top(x, y) + band_bot(x, y))
pb_band = lambda x, y: 0.5 * (band_top(x, y) - band_bot(x, y))

# plate boundaries (radians; front = pi/2, +x side = 0).  LEFT plates run from the front centre plate to the rear centre
# plate; odd ones are the thicker, slightly shorter "stepped" lames so the seams read as overlaps.
GAP = 0.011
LEFT_PLATES = [(1.27, 0.86), (0.86, 0.45), (0.45, 0.06), (0.06, -0.40), (-0.40, -0.85), (-0.85, -1.27)]
FRONT_C = (PI / 2 - 0.30, PI / 2 + 0.30)
REAR_C = (-PI / 2 - 0.30, -PI / 2 + 0.30)
# lining / lip / trim / skirt partition: left side, front, (right = mirror), rear
ARC_L = (-0.85, 0.85)
ARC_F = (0.85 + 0.012, PI - 0.85 - 0.012)
ARC_R_REAR = (PI + 0.85 + 0.012, 2 * PI - 0.85 - 0.012)


def build():
    out = []

    def both(ob):
        r = mirror(ob)
        out.extend([ob, r])
        return ob, r

    def add(ob):
        out.append(ob)
        return ob

    from mathutils import Matrix as _M
    HIP_D = Vector((0.0, 0.05 * H, 0.0))      # hip assembly tucked inside the skirt (hidden when standing, shows when seated)

    def shift(ob):
        ob.data.transform(_M.Translation(HIP_D))
        return ob

    OLIVE = K.olive_material()

    def surf(a, grow=0.0):
        """point + outward normal on the belt centre line at plan angle a, offset to the outer face (grow = extra radial)"""
        x, y = K.plan_pt(a, A_BELT, B_BELT, NP)
        nx, ny = K.plan_normal(a, A_BELT, B_BELT, NP)
        return x, y, nx, ny, band_pa(x, y) + grow

    # ============================================================== core plug (dark) ==============================
    core = L.Sweep([P(0, 0.0, 4.52), P(0, 0.0, 4.80), P(0, 0.0, 5.19)],
                   [(0.0, H * 0.34, H * 0.26, 3.0), (0.3, H * 0.50, H * 0.36, 3.0), (1.0, H * 0.54, H * 0.40, 3.0)])
    cm = core.mesh("pelvis_core", nring=40, nstations=10, round_start=(0.03, 3))
    fin(cm, "dark", bevel=0.0, wear=0)
    add(cm)

    # dark seam core: a closed ring just under the plates; the real gaps between plates show it as a dark groove
    scr = K.ring_around("pelvis_belt_seamcore", A_BELT, B_BELT, NP, zc_band,
                        lambda x, y: band_pa(x, y) * 0.90, lambda x, y: pb_band(x, y) * 0.97, nu=110, nv=12, n_prof=3.4)
    fin(scr, "dark", bevel=0.0, wear=0)
    add(scr)

    # ============================================================== belt: SEPARATE overlapping plates ==============
    GROW = 0.006
    def plate(name, a0, a1, grown):
        lo, hi = (min(a0, a1) + GAP, max(a0, a1) - GAP)
        g = GROW if grown else 0.0
        shrink = 0.012 if grown else 0.0
        nu = max(6, int((hi - lo) * 30))
        ob = K.arc_around(name, A_BELT, B_BELT, NP, lo if a0 < a1 else hi, hi if a0 < a1 else lo, zc_band,
                          lambda x, y: band_pa(x, y) + g, lambda x, y: pb_band(x, y) - shrink, nu=nu, nv=24, n_prof=3.6)
        fin(ob, OLIVE, bevel=0.0016, seg=2, wear=1.0)
        return ob

    pc = K.arc_around("pelvis_belt_plate_front", A_BELT, B_BELT, NP, FRONT_C[0] + GAP, FRONT_C[1] - GAP, zc_band,
                      lambda x, y: band_pa(x, y), lambda x, y: pb_band(x, y), nu=14, nv=24, n_prof=3.6)
    fin(pc, OLIVE, bevel=0.0016, seg=2, wear=1.0)
    add(pc)
    for i, (a0, a1) in enumerate(LEFT_PLATES):
        ob = plate(f"pelvis_belt_plate_{i + 1}.L", a0, a1, grown=(i % 2 == 0))
        both(ob)
    prc = K.arc_around("pelvis_belt_plate_rear", A_BELT, B_BELT, NP, REAR_C[0] + GAP, REAR_C[1] - GAP, zc_band,
                       lambda x, y: band_pa(x, y) + GROW, lambda x, y: pb_band(x, y) - 0.012, nu=14, nv=24, n_prof=3.6)
    fin(prc, OLIVE, bevel=0.0016, seg=2, wear=1.0)
    add(prc)

    # champagne hairlines along the upper edge of the plates (0.004 m), four arcs
    def hair(name, a0, a1, grow):
        ob = K.arc_around(name, A_BELT, B_BELT, NP, a0, a1, lambda x, y: band_top(x, y) - 0.030 - 0.5 * 0.0,
                          lambda x, y: band_pa(x, y) + grow + 0.0025, lambda x, y: 0.0085,
                          nu=max(8, int(abs(a1 - a0) * 30)), nv=8, n_prof=3.0)
        fin(ob, "gold", bevel=0.0005, seg=1, wear=0)
        return ob

    both(hair("pelvis_belt_hair.L", ARC_L[0], ARC_L[1], 0.0030))
    add(hair("pelvis_belt_hair_front", ARC_F[0], ARC_F[1], 0.0))
    add(hair("pelvis_belt_hair_rear", ARC_R_REAR[0], ARC_R_REAR[1], GROW))

    # bronze lower lip: slim rolled bead under the band, 4 pieces
    def lip(name, a0, a1):
        ob = K.arc_around(name, A_BELT, B_BELT, NP, a0, a1, lambda x, y: band_bot(x, y) + 0.012,
                          lambda x, y: band_pa(x, y) + 0.016, lambda x, y: 0.030, nu=max(8, int(abs(a1 - a0) * 20)),
                          nv=12, n_prof=3.0)
        fin(ob, OLIVE, bone="abdomen", bevel=0.0014, wear=1.0)
        return ob

    both(lip("pelvis_belt_lip.L", ARC_L[0], ARC_L[1]))
    add(lip("pelvis_belt_lip_front", ARC_F[0], ARC_F[1]))
    add(lip("pelvis_belt_lip_rear", ARC_R_REAR[0], ARC_R_REAR[1]))

    # teal inner lining: shows inside the bowl and over the upper edge (olive outside, teal inside), 4 pieces
    def lining(name, a0, a1):
        ob = K.arc_around(name, A_BELT - 0.062, B_BELT - 0.056, NP, a0, a1,
                          lambda x, y: 0.5 * ((band_top(x, y) + 0.060 + 0.070 * xn(x) ** 2) + (band_bot(x, y) + 0.05)),
                          lambda x, y: 0.030,
                          lambda x, y: 0.5 * ((band_top(x, y) + 0.060 + 0.070 * xn(x) ** 2) - (band_bot(x, y) + 0.05)),
                          nu=max(8, int(abs(a1 - a0) * 20)), nv=16, n_prof=3.2)
        fin(ob, "teal", bevel=0.0016, wear=1.0)
        return ob

    both(lining("pelvis_belt_lining.L", ARC_L[0], ARC_L[1]))
    add(lining("pelvis_belt_lining_front", ARC_F[0], ARC_F[1]))
    add(lining("pelvis_belt_lining_rear", ARC_R_REAR[0], ARC_R_REAR[1]))

    # ============================================================== teal hip skirt (closes the gap to the thigh) ==
    def skirt_bot(x, y):
        k = sstep(0.08, 0.40, abs(x)) if y < 0.15 else 1.0     # no skirt at the crotch centre front: dark crotch shows
        return band_bot(x, y) - 0.02 - 0.27 * k

    def skirt_top(x, y):
        return band_bot(x, y) + 0.12

    def skirt(name, a0, a1):
        ob = K.arc_around(name, A_BELT - 0.030, B_BELT - 0.028, NP, a0, a1,
                          lambda x, y: 0.5 * (skirt_top(x, y) + skirt_bot(x, y)), lambda x, y: 0.050,
                          lambda x, y: 0.5 * (skirt_top(x, y) - skirt_bot(x, y)), nu=max(8, int(abs(a1 - a0) * 16)),
                          nv=14, n_prof=3.4)
        fin(ob, "teal", bevel=0.0024, seg=2, wear=1.0)
        return ob

    both(skirt("pelvis_hip_skirt.L", ARC_L[0], ARC_L[1]))
    add(skirt("pelvis_hip_skirt_front", ARC_F[0], ARC_F[1]))
    add(skirt("pelvis_hip_skirt_rear", ARC_R_REAR[0], ARC_R_REAR[1]))

    # ============================================================== belt fasteners: hex heads with washers =========
    # one pair (upper / lower) at the end of every grown plate, on the stepped plate face (4.5 to 6 mm heads)
    bolt_spec = []
    for i, (a0, a1) in enumerate(LEFT_PLATES):
        if i % 2 == 0:
            bolt_spec.append((a0 - 0.055 if a0 > a1 else a0 + 0.055, GROW))
            bolt_spec.append((a1 + 0.055 if a0 > a1 else a1 - 0.055, GROW))
    # rear centre plate (grown): bolt pair at the left end (mirror gives the right end)
    bolt_spec.append((REAR_C[1] - 0.055, GROW))
    n_b = 0
    for (a, g) in bolt_spec:
        x, y, nx, ny, pa = surf(a, g)
        zt, zb = band_top(x, y), band_bot(x, y)
        for fz in (0.27, 0.73):
            z = zb + (zt - zb) * fz
            c = P(x + nx * (pa + 0.0004), y + ny * (pa + 0.0004), z)
            b = K.fastener(f"pelvis_belt_bolt_{n_b}.L", c, (nx, ny, 0.0), r=0.0024, h=0.0007, washer=True)
            fin(b, "gunmetal", bevel=0.0003, seg=1, wear=0)
            both(b)
            n_b += 1

    # ============================================================== centre pill (teal) in a bronze bezel ==========
    pz = band_top(0, -B_BELT) + 0.06 - 0.035
    py = -B_BELT + 0.008
    pill = L.box("pelvis_belt_pill", (H * 0.13, H * 0.05, H * 0.26), L.Frame(P(0, py - 0.044, pz + 0.035)))
    fin(pill, "teal", bevel=0.0035, seg=3, wear=1.0)
    add(pill)
    bz = L.box("pelvis_belt_pill_bezel", (H * 0.185, H * 0.035, H * 0.12), L.Frame(P(0, py - 0.032, pz - 0.05)))
    fin(bz, OLIVE, bevel=0.0028, seg=2, wear=1.0)
    add(bz)
    for k, (dx, zz) in enumerate(((-0.062, pz - 0.05), (0.062, pz - 0.05))):
        sc = K.fastener(f"pelvis_pill_screw_{k}", P(dx, py - 0.0505, zz), (0, -1, 0), r=0.0026, h=0.0020, washer=True, hexagon=False)
        fin(sc, OLIVE, bevel=0.0004, seg=1, wear=0)
        add(sc)

    # ============================================================== codpiece: tapering olive-bronze LAMED plate ====
    def cod_c(u):
        return P(0, -0.545 - 0.040 * u ** 1.6, 4.705 - 0.30 * u)

    def cod_w(u):
        base = 0.150 - 0.072 * u ** 1.15           # half width: 0.077 m at the top tapering to 0.04 m at the tip
        end = max(0.0, (u - 0.88) / 0.12)
        return base * (0.80 + 0.20 * math.sqrt(max(0.0, 1.0 - end ** 2.0)))

    def cod_fn_range(u0, u1, ypush):
        def fn(u, v):
            uu = u0 + (u1 - u0) * u
            s = v * 2 - 1
            w = cod_w(uu)
            c = cod_c(uu)
            x = s * w
            ridge = (0.036 - 0.018 * uu) * (1 - abs(s))
            dy = -ridge + 0.9 * x * x - ypush
            return Vector((x * H, c.y + dy * H, c.z))
        return fn

    cod_parts = [("pelvis_codpiece_lame_1", 0.0, 0.40, 0.013), ("pelvis_codpiece_lame_2", 0.37, 0.72, 0.0065),
                 ("pelvis_codpiece_tip", 0.69, 1.0, 0.0)]
    for nm, u0, u1, yp in cod_parts:
        c = L.grid_surface(nm, cod_fn_range(u0, u1, yp), 14, 16, thickness=0.011, flip=True)
        fin(c, OLIVE, bevel=0.0010, seg=2, wear=0)
        add(c)

    def rid_fn(u, v):
        s = v * 2 - 1
        uu = 0.05 + 0.74 * u
        c = cod_c(uu)
        x = s * 0.016
        return Vector((x * H, c.y - (0.038 - 0.020 * uu - 0.3 * abs(s) * 0.02) * H - 0.014 * H * (1 - uu), c.z))

    ridge = L.grid_surface("pelvis_codpiece_ridge", rid_fn, 28, 4, thickness=0.004, flip=True)
    fin(ridge, "gold", bevel=0.0010, seg=1, wear=0)
    add(ridge)

    for i, (u, sg) in enumerate(((0.12, 1), (0.12, -1), (0.40, 1), (0.40, -1), (0.66, 1), (0.66, -1))):
        w = cod_w(u) * 0.70
        c = cod_c(u)
        yp = 0.013 if u < 0.37 else (0.0065 if u < 0.69 else 0.0)
        pos = Vector((sg * w * H, (c.y + (0.9 * w * w - yp) * H), c.z))
        rv = K.fastener(f"pelvis_codpiece_rivet_{i}", pos, (0, -1, 0.15), r=0.0027, h=0.0020, washer=False, hexagon=False)
        fin(rv, OLIVE, bevel=0.0004, seg=1, wear=0)
        add(rv)

    # hinge: pin across the codpiece top, two clevis ears on the belt lip, hex heads at the ends
    pin = L.cylinder("pelvis_codpiece_pin", H * 0.016, H * 0.34, L.Frame.at(P(0, -0.553, 4.742), (1, 0, 0), (0, 0, 1)), segments=20)
    fin(pin, "gunmetal", bevel=0.0005, seg=1, wear=0)
    add(pin)
    for sx in (-1, 1):
        ear = L.box(f"pelvis_codpiece_ear.{'L' if sx > 0 else 'R'}", (H * 0.030, H * 0.060, H * 0.085), L.Frame(P(sx * 0.100, -0.548, 4.742)))
        fin(ear, OLIVE, bevel=0.0018, seg=2, wear=1.0)
        add(ear)
        hd = K.fastener(f"pelvis_codpiece_pinhead.{'L' if sx > 0 else 'R'}", P(sx * 0.17, -0.553, 4.742), (sx, 0, 0), r=0.0034, h=0.0026, washer=True)
        fin(hd, "gunmetal", bevel=0.0004, seg=1, wear=0)
        add(hd)

    cb = L.sphere("pelvis_crotch_block", H * 0.5, L.Frame(P(0, -0.34, 4.52)), scale=(0.24, 0.17, 0.085), segments=32, rings=16)
    fin(cb, "dark", bevel=0.0, wear=0)
    add(cb)

    # dark crotch filler 0.05 m wide between the thighs under the codpiece (critic: the gap read as a slit)
    cf = L.box("pelvis_crotch_filler", (0.050, 0.140, 0.110), L.Frame(Vector((0.0, -0.065, 1.090))))
    fin(cf, "dark", bevel=0.004, seg=2, wear=0)
    add(cf)

    # ============================================================== hip balls + sockets (hidden standing) ==========
    bc = P(0.36, -0.285, 4.62)
    ball = L.sphere("pelvis_hip_ball.L", H * 0.092, L.Frame(bc), segments=40, rings=24)
    fin(ball, "gunmetal", bevel=0.0, wear=0)
    shift(ball)
    both(ball)
    lipf = L.Frame.at(bc + Vector((0, -0.05 * H, 0.012 * H)), (0, -1, 0.35))
    sock = L.torus("pelvis_hip_socket.L", H * 0.112, H * 0.017, lipf, major_seg=48, minor_seg=12)
    fin(sock, OLIVE, bevel=0.0, wear=1.0)
    shift(sock)
    both(sock)
    brs = []
    axis = Vector((0, -1, 0.35)).normalized()
    for i, ph in enumerate((16, 32, 48, 64)):
        R = 0.092 * H
        c = bc + axis * (R * math.cos(math.radians(ph)))
        trr = L.torus(f"pelvis_ballring_{i}", R * math.sin(math.radians(ph)), 0.0030 * H, L.Frame.at(c, axis), major_seg=40, minor_seg=8)
        brs.append(trr)
    bj = L.join(brs, "pelvis_hip_ball_rings.L")
    fin(bj, "silver", bevel=0.0, wear=0)
    shift(bj)
    both(bj)

    # ============================================================== mechanism (separate parts, hidden standing) ====
    def mat_obj(o, m, name, bevel=0.0012):
        o.name = name
        fin(o, m, bevel=bevel, seg=1, wear=1.0 if m in ("bronze", "teal") else 0)
        shift(o)
        both(o)
        return o

    g1 = K.gear("g", P(0.17, -0.36, 4.58), (0.05, -1, 0.1), H * 0.078, H * 0.060, 12, H * 0.032, (1, 0, 0))
    mat_obj(g1, "silver", "pelvis_gear_a.L")
    g1h = L.cylinder("g", H * 0.03, H * 0.05, L.Frame.at(P(0.17, -0.375, 4.58), (0.05, -1, 0.1)), segments=16)
    mat_obj(g1h, OLIVE, "pelvis_gear_a_hub.L")
    g2 = K.gear("g", P(0.55, -0.30, 4.68), (0.15, -1, 0.1), H * 0.062, H * 0.047, 10, H * 0.030, (0, 0, 1))
    mat_obj(g2, "silver", "pelvis_gear_b.L")
    g2h = L.cylinder("g", H * 0.025, H * 0.05, L.Frame.at(P(0.55, -0.315, 4.68), (0.15, -1, 0.1)), segments=16)
    mat_obj(g2h, OLIVE, "pelvis_gear_b_hub.L")
    g3 = K.gear("g", P(0.36, -0.38, 4.47), (0, -1, 0.2), H * 0.052, H * 0.040, 9, H * 0.028, (1, 0, 0))
    mat_obj(g3, OLIVE, "pelvis_gear_c.L")
    g4 = K.gear("g", P(0.27, -0.36, 4.43), (0, -1, 0.0), H * 0.036, H * 0.027, 8, H * 0.024, (1, 0, 0))
    mat_obj(g4, "silver", "pelvis_gear_d.L")
    pis = L.tube("g", [P(0.27, -0.30, 4.50), P(0.40, -0.30, 4.63), P(0.50, -0.27, 4.77)], H * 0.016, nring=12)
    mat_obj(pis, "silver", "pelvis_piston.L", 0.0008)
    slv = L.tube("g", [P(0.27, -0.30, 4.50), P(0.335, -0.30, 4.565)], H * 0.027, nring=14)
    mat_obj(slv, "dark", "pelvis_piston_sleeve.L", 0.001)
    slv2 = L.tube("g", [P(0.325, -0.30, 4.555), P(0.345, -0.30, 4.575)], H * 0.033, nring=14)
    mat_obj(slv2, OLIVE, "pelvis_piston_collar.L", 0.001)
    r1 = L.tube("g", [P(0.15, -0.34, 4.66), P(0.22, -0.40, 4.54), P(0.31, -0.40, 4.46)], H * 0.012, nring=10)
    mat_obj(r1, "silver", "pelvis_rod_a.L", 0.0008)
    r2 = L.tube("g", [P(0.50, -0.34, 4.56), P(0.44, -0.40, 4.47), P(0.40, -0.41, 4.40)], H * 0.012, nring=10)
    mat_obj(r2, "silver", "pelvis_rod_b.L", 0.0008)
    h1 = L.tube("g", [P(0.12, -0.30, 4.78), P(0.17, -0.40, 4.70), P(0.22, -0.40, 4.58), P(0.20, -0.38, 4.48)], H * 0.014, nring=10)
    mat_obj(h1, "dark", "pelvis_hose_a.L", 0.0006)
    h2 = L.tube("g", [P(0.60, -0.20, 4.80), P(0.56, -0.32, 4.72), P(0.50, -0.38, 4.60), P(0.52, -0.36, 4.50)], H * 0.014, nring=10)
    mat_obj(h2, "dark", "pelvis_hose_b.L", 0.0006)
    g5 = K.gear("g", P(0.44, -0.40, 4.52), (0.1, -1, 0.15), H * 0.046, H * 0.035, 9, H * 0.026, (1, 0, 0))
    mat_obj(g5, OLIVE, "pelvis_gear_e.L")
    g6 = K.gear("g", P(0.62, -0.26, 4.60), (0.3, -1, 0.1), H * 0.040, H * 0.030, 8, H * 0.024, (0, 0, 1))
    mat_obj(g6, "silver", "pelvis_gear_f.L")
    pis2 = L.tube("g", [P(0.55, -0.34, 4.46), P(0.50, -0.34, 4.55), P(0.46, -0.33, 4.62)], H * 0.014, nring=10)
    mat_obj(pis2, "silver", "pelvis_piston_b.L", 0.0008)
    slv3 = L.tube("g", [P(0.55, -0.34, 4.46), P(0.525, -0.34, 4.50)], H * 0.024, nring=12)
    mat_obj(slv3, "dark", "pelvis_piston_b_sleeve.L", 0.001)
    b1 = L.cylinder("g", H * 0.062, H * 0.024, L.Frame.at(P(0.36, -0.215, 4.62), (0, -1, 0.2)), segments=36)
    mat_obj(b1, "dark", "pelvis_bear_a.L", 0.0008)
    b2 = L.cylinder("g", H * 0.050, H * 0.034, L.Frame.at(P(0.36, -0.215, 4.62) + Vector((0, -0.004 * H, 0)), (0, -1, 0.2)), segments=36)
    mat_obj(b2, "silver", "pelvis_bear_b.L", 0.0008)

    # ============================================================== rear: lobes, keel, lumbar blocks ===============
    lobe = L.Sweep([P(0.19, 0.38, 4.36), P(0.19, 0.38, 4.74), P(0.19, 0.38, 5.08)],
                   [(0.0, H * 0.09, H * 0.085, 2.6), (0.18, H * 0.15, H * 0.135, 2.4), (0.33, H * 0.165, H * 0.150, 2.4),
                    (0.50, H * 0.170, H * 0.152, 2.4), (0.80, H * 0.125, H * 0.12, 2.4), (0.93, H * 0.07, H * 0.07, 2.2),
                    (1.0, H * 0.02, H * 0.03, 2.0)])
    lobeL = lobe.mesh("pelvis_sacrum_lobe.L", nring=36, nstations=24)
    fin(lobeL, "teal", bevel=0.002, seg=3, wear=0)
    both(lobeL)

    def lobe_plate(name, t_lo, t_hi, a0, a1, thickness=0.008, inflate=0.003, height=0.008, nu=14, nv=18):
        def fn(u, v):
            tl, th_ = t_lo(v), t_hi(v)
            t = tl + (th_ - tl) * u
            th = a0 + (a1 - a0) * v
            dome = height * math.sin(PI * v) ** 0.8 * math.sin(PI * min(1.0, max(0.0, u))) ** 0.6
            return lobe.point(t, th, 0.0) + lobe.outward(t, th) * (inflate + dome)
        return L.grid_surface(name, fn, nu, nv, thickness=thickness, flip=not lobe.handed)

    lcap = lobe_plate("pelvis_lobe_cap.L", lambda v: 0.60, lambda v: 0.995 - 0.22 * abs(2 * v - 1) ** 0.9,
                      math.radians(205), math.radians(335))
    fin(lcap, "teal", bevel=0.002, seg=2, wear=1.0)
    both(lcap)
    lskirt = lobe_plate("pelvis_lobe_skirt.L", lambda v: 0.03 + 0.10 * (2 * v - 1) ** 2, lambda v: 0.27,
                        math.radians(200), math.radians(340))
    fin(lskirt, "teal", bevel=0.002, seg=2, wear=0)
    both(lskirt)
    for k, zc in enumerate((5.00, 4.88, 4.76, 4.64)):
        w = 0.036 - 0.003 * k
        kb = L.box(f"pelvis_vert_{k}", (H * w * 2, H * 0.05, H * 0.085), L.Frame(P(0, 0.545, zc)))
        fin(kb, "teal", bevel=0.003, seg=2, wear=1.0)
        add(kb)
        # lumbar side tab pair on the spine block
        for sx in (-1, 1):
            tb = L.box(f"pelvis_lumbar_tab_{k}.{'L' if sx > 0 else 'R'}", (H * 0.030, H * 0.036, H * 0.055),
                       L.Frame(P(sx * (w + 0.040), 0.540, zc)))
            fin(tb, "gunmetal", bevel=0.0018, seg=2, wear=0)
            add(tb)

    keel = L.Sweep([P(0, 0.48, 5.12), P(0, 0.51, 4.82), P(0, 0.48, 4.50)],
                   [(0.0, H * 0.045, H * 0.04, 3.2), (0.5, H * 0.05, H * 0.05, 3.2), (1.0, H * 0.04, H * 0.04, 3.2)])
    km = keel.mesh("pelvis_sacrum_keel", nring=24, nstations=18)
    fin(km, "dark", bevel=0.0, wear=0)
    add(km)

    # ============================================================== hip pods: gunmetal bearing roundels ============
    ry = 0.20
    wx = wall_x(ry) + band_pa(wall_x(ry), ry)
    dz = 0.5 * (band_top(wall_x(ry), ry) + band_bot(wall_x(ry), ry)) - 0.02
    dc = P(wx - 0.032, ry, dz)
    R_D = 0.130
    ft = Vector((1, 0, 0))
    ax = ((1, 0, 0), (0, 1, 0))
    base = L.cylinder("pelvis_hip_pod.L", H * (R_D + 0.012), H * 0.050, L.Frame.at(dc + ft * (0.012 * H), *ax), segments=56)
    fin(base, "gunmetal", bevel=0.0030, seg=3, wear=0)
    both(base)
    fx = dc + ft * (0.040 * H)
    floor = L.cylinder("pelvis_hip_pod_floor.L", H * (R_D - 0.030), H * 0.012, L.Frame.at(fx, *ax), segments=48)
    fin(floor, "darkdisc", bevel=0.0, wear=0)
    both(floor)
    lipr = K.ring_disc("pelvis_hip_pod_lip.L", dc + ft * (0.040 * H), (1, 0, 0), H * (R_D + 0.012), H * (R_D - 0.014), H * 0.020,
                       xhint=(0, 1, 0), seg=64)
    fin(lipr, "silver", bevel=0.0010, seg=2, wear=0)
    both(lipr)
    for i, (r, mt, mi) in enumerate(((0.090, "silver", 0.0062), (0.068, "gunmetal", 0.0055), (0.048, "silver", 0.0050))):
        tr = L.torus(f"pelvis_hip_pod_ring_{i}.L", H * r, H * mi, L.Frame.at(fx + ft * (0.010 * H), *ax), major_seg=48, minor_seg=8)
        fin(tr, mt, bevel=0.0, wear=0)
        both(tr)
    boss = L.cylinder("pelvis_hip_pod_boss.L", H * 0.028, H * 0.026, L.Frame.at(fx + ft * (0.014 * H), *ax), segments=24)
    fin(boss, OLIVE, bevel=0.0010, seg=2, wear=1.0)
    both(boss)
    for k in range(6):
        th = 2 * PI * k / 6 + PI / 6
        pos = dc + Vector((0.0505 * H, 0.113 * H * math.cos(th), 0.113 * H * math.sin(th)))
        db = K.fastener(f"pelvis_hip_pod_bolt_{k}.L", pos, (1, 0, 0), r=0.0030, h=0.0022, washer=True)
        fin(db, "gunmetal", bevel=0.0004, seg=1, wear=0)
        both(db)

    # clevis plates above and below the pod, pin retaining ring
    for nm, dzz in (("up", R_D + 0.062), ("low", -(R_D + 0.062))):
        cv = L.box(f"pelvis_hip_clevis_{nm}.L", (H * 0.020, H * 0.115, H * 0.052), L.Frame(dc + Vector((0.020 * H, 0.0, dzz * H))))
        fin(cv, OLIVE, bevel=0.0022, seg=2, wear=1.0)
        both(cv)
        for sy in (-1, 1):
            sc = K.fastener(f"pelvis_hip_clevis_screw_{nm}_{'a' if sy < 0 else 'b'}.L",
                            dc + Vector((0.030 * H, sy * 0.040 * H, dzz * H)), (1, 0, 0), r=0.0024, h=0.0018, washer=False, hexagon=False)
            fin(sc, "gunmetal", bevel=0.0003, seg=1, wear=0)
            both(sc)
    cir = L.torus("pelvis_hip_pod_circlip.L", H * 0.029, H * 0.0045, L.Frame.at(fx + ft * (0.030 * H), *ax), major_seg=32, minor_seg=6)
    fin(cir, "silver", bevel=0.0, wear=0)
    both(cir)

    # ============================================================== hoses with clamps at the hip ===================
    def hose_with_clamps(base, pts, r, clamp_ts):
        name = base + ".L"
        hb = K.hose(name, pts, r)
        fin(hb, "dark", bevel=0.0, wear=0)
        path = L.Path(pts, n_per_seg=16)
        both(hb)
        for j, t in enumerate(clamp_ts):
            c = path.at(t)
            tg = path.tangent(t)
            cl = K.clamp_ring(f"{base}_clamp_{j}.L", c, tg, r)
            fin(cl, OLIVE, bevel=0.0, wear=0)
            both(cl)

    hose_with_clamps("pelvis_hose_up_a",
                     [P(0.745, 0.31, 4.96), P(0.741, 0.36, 5.10), P(0.68, 0.40, 5.24), P(0.60, 0.42, 5.34)], H * 0.017, (0.12, 0.88))
    hose_with_clamps("pelvis_hose_up_b",
                     [P(0.717, 0.31, 4.94), P(0.709, 0.37, 5.08), P(0.65, 0.43, 5.22), P(0.56, 0.45, 5.33)], H * 0.015, (0.14, 0.86))

    # ---- funnel flare: pushes the upper part of the belt (and what rides on it) outward so the teal lining shows
    #      from the front, as in f07/f08.  Plain vertex transform on real geometry, applied to both sides alike.
    FL_PREFIX = ("pelvis_belt_", "pelvis_hip_skirt", "pelvis_hip_pod", "pelvis_hip_clevis", "pelvis_hip_pod_")
    for o in out:
        if not o.name.startswith(FL_PREFIX) or o.name.startswith(("pelvis_belt_pill", "pelvis_belt_seamcore")):
            continue
        me = o.data
        for v in me.vertices:
            t = L.clamp((v.co.z / H - FZ0) / (FZ1 - FZ0))
            f = FLARE * t ** 1.4
            v.co.x *= 1.0 + f
            v.co.y *= 1.0 + 0.55 * f if v.co.y > -0.2 else 1.0 + 0.25 * f
        me.update()

    import os
    if os.environ.get("PELVIS_STATS"):
        rows = []
        for o in out:
            o.data.calc_loop_triangles()
            rows.append((len(o.data.loop_triangles), o.name))
        rows.sort(reverse=True)
        for r in rows[:22]:
            print("TRIS", r)
    return out
