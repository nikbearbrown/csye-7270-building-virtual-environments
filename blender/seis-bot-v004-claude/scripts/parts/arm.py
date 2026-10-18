"""arm - SEIS bot arm, shoulder cup to wrist cuff, CONFORMED to the on-model frames (spec/ONMODEL.md, ARM table).
Build LEFT (+X), mirror to RIGHT.

Layout (theta around the limb, left arm): 0 = outer (+X), 90 = front (-Y), 180 = inner (-X), 270 = rear.
Heights are written in head-heights above the floor (zh), converted with H.  Everything is clean glossy teal, flat gold
bezel panels, red lacquer in two places (the stadium window, the forearm slot), a big elbow disc, a thin gold-edged wing
on the outer forearm edge.  No bronze wear, no bulging cowl, no stacked straps.
"""
import math
import os
import time
import bpy
import seis_lib as L
import seis_spec as S
import arm_util as U
import arm_detail as D

H = S.H
PI = math.pi
rad = math.radians
deg = math.degrees
sm = L.smoothstep


def hz(h):
    return h * H


def Zh(h):
    return h * H


def lerp(a, b, t):
    return a + (b - a) * t


# ------------------------------------------------------------------------------------------------ generic helpers
PLATES = {}


def top_off(name, z, th):
    """height (m) of plate `name`'s outer surface above its skin at (z zh, th deg): inflate + dome (for seating fasteners)."""
    ft, fb, fa, fc, infl, dome, hp = PLATES[name]
    a, b = fa(0.5), fc(0.5)
    lo = min(a, b)
    th = lo + ((th - lo) % 360.0)
    v = (th - a) / ((b - a) or 1.0)
    u = 0.5
    for _ in range(3):
        zt, zb = ft(v), fb(v)
        u = (z - zt) / ((zb - zt) or 1.0)
        a, b = fa(u), fc(u)
        lo = min(a, b)
        th2 = lo + ((th - lo) % 360.0)
        v = (th2 - a) / ((b - a) or 1.0)
    u, v = min(max(u, 0.0), 1.0), min(max(v, 0.0), 1.0)
    return infl + dome * (math.sin(PI * u) ** hp) * (math.sin(PI * v) ** hp)


def plate(sw, name, z_top, z_bot, th_a, th_b, mat, bone, nu=26, nv=14, inflate=0.002, dome=0.004, hp=1.0,
          thickness=0.007, holes=(), bevel=0.0022, wear=None, bevel_seg=2, ends=0.0):
    """Plate on skin `sw` between heights z_top/z_bot (zh; const or fn(v)) and angles th_a/th_b (deg; const or fn(u))."""
    ft = z_top if callable(z_top) else (lambda v, _a=z_top: _a)
    fb = z_bot if callable(z_bot) else (lambda v, _a=z_bot: _a)
    fa = th_a if callable(th_a) else (lambda u, _a=th_a: _a)
    fc = th_b if callable(th_b) else (lambda u, _a=th_b: _a)

    def zth(u, v):
        zt, zb = ft(v), fb(v)
        z = zt + (zb - zt) * u
        a, b = fa(u), fc(u)
        return z, a + (b - a) * v

    def fn(u, v):
        z, th = zth(u, v)
        d = dome * (math.sin(PI * u) ** hp) * (math.sin(PI * v) ** hp)
        return U.tz(sw, Zh(z)), rad(th), inflate + d

    hl = [(lambda u, v, _h=h: _h(*zth(u, v))) for h in holes]
    ob = U.patch(sw, name, fn, nu, nv, thickness=thickness, holes=hl)
    L.finish(ob, mat, bevel=bevel, bevel_segments=bevel_seg, bone=bone, **({"wear": wear} if wear is not None else {}))
    PLATES[name] = (ft, fb, fa, fc, inflate, dome, hp)
    return ob


def surf_point(sw, zh, th_deg, off=0.0):
    t = U.tz(sw, Zh(zh))
    p, n = U.skin_n(sw, t, rad(th_deg))
    return p + n * off, n, sw.frame(t)[1]


def torus_on(name, fr, major, minor, mat, bone, seg=56, mseg=10, bevel=0):
    t = L.torus(name, major, minor, fr, major_seg=seg, minor_seg=mseg)
    L.finish(t, mat, bevel=bevel, bone=bone)
    return t


def stadium_cut(ob, spot, ha, r, n=40):
    """exact stadium-shaped hole through plate `ob` at `spot` (replaces a staircase hole): prism along the skin normal"""
    import bmesh as _bm
    fr = spot.frame(off=0.0)
    outl = U.stadium_outline(ha, r)
    pts2 = [outl(2 * PI * i / n) for i in range(n)]
    bm = _bm.new()
    lo, hi = -0.016, 0.022
    ring_lo = [bm.verts.new(fr.p(B, A, lo)) for (A, B) in pts2]       # frame x = along the perimeter (B), y = down the limb (A)
    ring_hi = [bm.verts.new(fr.p(B, A, hi)) for (A, B) in pts2]
    bm.faces.new(ring_lo)
    bm.faces.new(list(reversed(ring_hi)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([ring_lo[i], ring_lo[j], ring_hi[j], ring_hi[i]])
    _bm.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new("cutter")
    bm.to_mesh(me)
    bm.free()
    cut = bpy.data.objects.new("cutter", me)
    (L._COLL or bpy.context.scene.collection).objects.link(cut)
    L.boolean_cut(ob, cut)
    return ob


def rivet_row(name, sw, pts, bone, r=0.0016, mat_="silver"):
    """one SEPARATE round-head rivet per point (z zh, th deg, offset m)"""
    out = []
    for i_, (z, th, off) in enumerate(pts):
        p, n, T = surf_point(sw, z, th, off)
        out.append(D.round_rivet(f"{name}_{i_}", L.Frame.at(p, n, T), r, mat_, bone))
    return out


BOLT_K = 0.72          # round-3: the frames are clean lacquer, so fasteners stay (count kept) but read small and dark


def bolt_at(name, sw, plate_name, z, th, r, bone, mat_="gunmetal", extra=0.0, kind="hex"):
    r = r * BOLT_K
    """a hex / round-head fastener seated on plate `plate_name` at (z zh, th deg)"""
    off = top_off(plate_name, z, th) + extra
    p, n, T = surf_point(sw, z, th, off)
    fr = L.Frame.at(p, n, T)
    if kind == "hex":
        return D.hex_bolt(name, fr, r, mat_, bone)
    return D.round_rivet(name, fr, r, mat_, bone)


def olive_mat():
    """dull olive-bronze (the elbow boss in f08 is NOT shiny)"""
    m = bpy.data.materials.get("SEIS_arm_olive")
    if m is None:
        m = bpy.data.materials.new("SEIS_arm_olive")
        m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = (0.062, 0.056, 0.020, 1.0)
        b.inputs["Metallic"].default_value = 0.85
        b.inputs["Roughness"].default_value = 0.46
        m.diffuse_color = (0.062, 0.056, 0.020, 1.0)
    return m


def satin_red():
    """satin crimson for the two lacquer windows: the shared red with a softer coat (round-3 critic: cherry with white blotches)"""
    m = bpy.data.materials.get("SEIS_arm_red")
    if m is None:
        base = L.mat("red")
        m = base.copy()
        m.name = "SEIS_arm_red"
        b = m.node_tree.nodes.get("Principled BSDF") if m.use_nodes else None
        if b is not None:
            for k, v in (("Coat Weight", 0.55), ("Coat Roughness", 0.16), ("Roughness", 0.22)):
                if k in b.inputs:
                    b.inputs[k].default_value = v
    return m


# ------------------------------------------------------------------------------------------------ on-model numbers
WIN_Z = 6.07                 # window centre, zh: 0.146 m (0.57 H) above the elbow disc centre (5.50)
WIN_TH = 68.0                # window centre theta: f04/f08 crops put the stadium at the CENTRE of the visible arm face
WIN_HA, WIN_R = 0.046, 0.0255        # stadium 0.051 x 0.092 m (half length, half width), metres
DISC_Z, DISC_TH = 5.50, 90.0
ELB_IN = 0.025               # elbow tucked in 0.025 m (CRITIC round 3 arm item 1: disc centre x about 0.276, outer span about 0.66 m); wrist stays at the spec joint
DISC_R = 0.0434              # 0.087 m dia (0.34 H_m)
SLOT_Z, SLOT_TH = 4.945, 113.0       # forearm slot centre (35% to 70% down the forearm)
SLOT_HA, SLOT_R = 0.0445, 0.0115     # stadium bar 0.089 x 0.023 m


# ------------------------------------------------------------------------------------------------ the side
def build_side():
    objs = []
    Sh, E, W = S.J("shoulder.L"), S.J("elbow.L"), S.J("wrist.L")
    E = E + L.V(-ELB_IN, 0.0, 0.0)
    UB, FB = "upperarm.L", "forearm.L"

    # =========================================================================== UPPER ARM skin (0.38 H incl. plates)
    d_u = (E - Sh).normalized()
    top = Sh
    bot = E + d_u * hz(0.25)
    mid = (top + bot) * 0.5 + L.V(0.004, 0.0, 0.0)
    path_u = L.Path([top, mid, bot])
    rows_u = [(6.45, 0.164, 0.158, 3.0), (6.20, 0.163, 0.157, 3.0), (5.95, 0.162, 0.156, 3.0),
              (5.72, 0.165, 0.159, 3.0), (5.60, 0.173, 0.167, 3.6), (5.50, 0.178, 0.173, 4.2), (5.40, 0.173, 0.168, 4.0), (5.33, 0.160, 0.156, 3.6), (5.25, 0.146, 0.142, 3.0)]
    sw0 = L.Sweep(path_u, [(0, 0.05, 0.05)])

    def mk_u(shrink):
        ks = [(U.tz(sw0, Zh(z)), hz(rx - shrink), hz(ry - shrink), n) for z, rx, ry, n in rows_u]
        ks[0] = (0.0,) + ks[0][1:]
        ks[-1] = (1.0,) + ks[-1][1:]
        return L.Sweep(path_u, ks)

    sw_u = mk_u(0.0)
    core_u = mk_u(0.034).mesh("arm_upper_core.L", nring=40)
    L.finish(core_u, "dark", bevel=0.0, bone=UB)
    objs.append(core_u)

    # dark plug that tucks into the shoulder cup
    plug = L.cylinder("arm_shoulder_plug.L", hz(0.150), hz(0.11),
                      L.Frame(Sh + L.V(0, 0, -hz(0.0)), (1, 0, 0), (0, 1, 0), (0, 0, 1)), segments=32)
    L.finish(plug, "dark", bevel=0.001, bone=UB)
    objs.append(plug)

    win = U.Spot(sw_u, Zh(WIN_Z), rad(WIN_TH))
    thS = lambda s: deg(win._th_of_s(s))          # theta (deg) at perimeter offset s (m) from the window centre

    # =========================================================================== upper arm plates (clean teal)
    TOP, PODTOP = 6.40, 5.70
    objs.append(plate(sw_u, "arm_upper_outer_wrap.L", TOP, PODTOP, -36, lambda u: thS(-0.0545), "teal", UB, dome=0.005,
                      wear=0.7, nv=10))
    objs.append(plate(sw_u, "arm_upper_rear_shell.L", TOP, PODTOP, 217, 321, "teal", UB, dome=0.006, wear=0.0, nv=16))
    objs.append(plate(sw_u, "arm_upper_inner_plate.L", TOP, PODTOP, thS(0.044), 212, "teal", UB, dome=0.005, wear=0.5,
                      nv=14))

    # window surround: teal plate whose hole is the recess footprint (hole edge hidden under the dark funnel ring)
    marg = 0.0035
    hole_ha, hole_r = WIN_HA + marg, WIN_R + marg

    def win_hole(z, th):
        A, B = win.AB(Zh(z), rad(th))
        return U.stadium_in(A, B, hole_ha + 0.0012, hole_r + 0.0012)

    objs.append(plate(sw_u, "arm_window_surround.L", TOP, PODTOP, lambda u: thS(-0.051), lambda u: thS(0.0405), "teal", UB,
                      dome=0.004, inflate=0.0018, thickness=0.007, nu=30, nv=22, bevel=0.0018, wear=1.0,
                      hp=0.6))
    stadium_cut(objs[-1], win, hole_ha + 0.0012, hole_r + 0.0012)

    # dark funnel (the recess wall) and the thin teal lip ring with a gold hairline
    outline_hole = U.stadium_outline(hole_ha, hole_r)
    wall = U.ring_surface(sw_u, "arm_window_recess.L", win, outline_hole,
                          [(0.0, 0.0006, 0.0034), (0.5, -0.0012, -0.0020), (1.0, -0.0026, -0.0075)], nu=60, thickness=0.004)
    L.finish(wall, "dark", bevel=0.0004, bevel_segments=1, bone=UB)
    objs.append(wall)
    lip = U.ring_surface(sw_u, "arm_window_lip.L", win, outline_hole,
                         [(0.0, 0.0004, 0.0030), (0.35, 0.0014, 0.0050), (0.7, 0.0040, 0.0050), (1.0, 0.0068, 0.0028)],
                         nu=60, thickness=0.005)
    L.finish(lip, "teal", bevel=0.0010, bevel_segments=2, bone=UB, wear=1.0)
    objs.append(lip)

    # red lacquer stadium, fully red, slightly domed, in the recess
    gl = U.radial_fill(sw_u, "arm_window_glass.L", win, lambda A, B: U.stadium_in(A, B, WIN_HA, WIN_R), centre=(0.0, 0.0),
                       off=lambda f: -0.0070 + 0.0016 * (1 - f * f), nu=56, nv=6, rmax=0.07, thickness=0.003)
    L.finish(gl, satin_red(), bevel=0.0005, bevel_segments=1, bone=UB)
    objs.append(gl)

    # flat olive-bronze bezel panel: an L down the inner side and under the window, stepped zig-zag lower edge
    th_in0, th_in1 = thS(0.0385), thS(0.086)
    th_out = thS(-0.056)

    def l_a(u):
        return th_out

    def l_b(u):
        return th_in1

    vc = (thS(0.047) - th_out) / (th_in1 - th_out)
    z_under = 5.855                       # top edge under the window (just below the lip ring)

    def l_top(v):
        return z_under + (6.345 - z_under) * sm(vc - 0.05, vc + 0.05, v)

    def l_bot(v):
        return 5.716 + 0.022 * (sm(0.28, 0.34, v) + sm(0.50, 0.56, v) + sm(0.70, 0.76, v))

    objs.append(plate(sw_u, "arm_window_bezel_L.L", l_top, l_bot, l_a, l_b, "bronze", UB, nu=14, nv=72, dome=0.0015,
                      inflate=0.0092, thickness=0.0032, bevel=0.0014, hp=0.5))
    # thin gold hairline cap along the bezel's inner (window-facing) edge
    objs.append(plate(sw_u, "arm_window_bezel_hair.L", 6.343, 5.862, thS(0.0381), thS(0.0398), "gold", UB,
                      nu=24, nv=2, dome=0.0, inflate=0.0118, thickness=0.0025, bevel=0.0006, bevel_seg=1, hp=0.5, wear=0.0))
    # tiny rivet row along the zig-zag lower edge
    riv = []
    for k in range(9):
        v = 0.06 + 0.88 * k / 8
        riv.append((l_bot(v) + 0.012, lerp(th_out, th_in1, v), 0.0128))
    objs += rivet_row("arm_bezel_rivet", sw_u, riv, UB, r=0.0013)

    # ---- thin gold ring round the window lip (champagne rim of the red stadium)
    gring = U.ring_surface(sw_u, "arm_window_gold_ring.L", win, outline_hole,
                           [(0.0, 0.0066, 0.0030), (0.5, 0.0075, 0.0042), (1.0, 0.0090, 0.0030)], nu=60, thickness=0.0020)
    L.finish(gring, "gold", bevel=0.0004, bevel_segments=1, bone=UB, wear=0.0)
    objs.append(gring)

    # ---- fasteners: three hex bolts above the window, three along the gold band, four at every plate's corners
    for k, B_ in enumerate((-0.028, 0.0, 0.028)):
        t_, th_ = win.zt(-0.066, B_)
        zz = (win.z + 0.066) / H
        objs.append(bolt_at(f"arm_window_bolt_{k}.L", sw_u, "arm_window_surround.L", zz, deg(th_), 0.0027, UB))
    for k, vv in enumerate((0.20, 0.52, 0.84)):
        zz = (l_top(vv) + l_bot(vv)) * 0.5
        th_ = lerp(th_out, th_in1, vv)
        p_, n_, T_ = surf_point(sw_u, zz, th_, 0.0100)
        objs.append(D.hex_bolt(f"arm_bezel_bolt_{k}.L", L.Frame.at(p_, n_, T_), 0.0018, "gunmetal", UB))

    def corner_bolts(tag, plate_name, zt_, zb_, ta, tb, r=0.0027, fa_=0.17, fb_=0.83):
        for iz, zz in enumerate((zt_, zb_)):
            for it, f_ in enumerate((fa_, fb_)):
                th_ = ta + (tb - ta) * f_
                objs.append(bolt_at(f"arm_{tag}_bolt_{iz}{it}.L", sw_u, plate_name, zz, th_, r, UB))

    th_ow = thS(-0.0545)
    corner_bolts("outer", "arm_upper_outer_wrap.L", TOP - 0.055, PODTOP + 0.055, -36.0, th_ow, fa_=0.22, fb_=0.78)
    corner_bolts("rear", "arm_upper_rear_shell.L", TOP - 0.055, PODTOP + 0.055, 217.0, 321.0)
    corner_bolts("inner", "arm_upper_inner_plate.L", TOP - 0.055, PODTOP + 0.055, thS(0.044), 212.0, fa_=0.2, fb_=0.8)

    # ---- shoulder-joint collar: dark boot, pewter bearing washer, gold hairline (under the pauldron horn)
    boot = plate(sw_u, "arm_swivel_boot.L", 6.452, 6.414, 0, 360, "dark", UB, nu=3, nv=48, inflate=0.0030, dome=0.0010,
                 thickness=0.005, bevel=0.0008, hp=0.5)
    U.weld_loose(boot)
    objs.append(boot)
    wash = plate(sw_u, "arm_swivel_washer.L", 6.416, 6.407, 0, 360, "silver", UB, nu=2, nv=48, inflate=0.0050, dome=0.0,
                 thickness=0.004, bevel=0.0007, bevel_seg=1)
    U.weld_loose(wash)
    objs.append(wash)
    wgold = plate(sw_u, "arm_swivel_gold.L", 6.407, 6.403, 0, 360, "gold", UB, nu=2, nv=48, inflate=0.0054, dome=0.0,
                  thickness=0.003, bevel=0.0004, bevel_seg=1, wear=0.0)
    U.weld_loose(wgold)
    objs.append(wgold)

    # ---- two exposed hoses lying in the plate seams (inner and rear), dark, clamped, diving under the elbow pod
    def hose_run(tag, th0, specs, r, clamps, bone, sw, mat_="gunmetal"):
        pts = [surf_point(sw, z, th0 + dth, off)[0] for (z, dth, off) in specs]
        out = [D.hose(f"arm_hose_{tag}.L", pts, r, mat_, bone)]
        for k, ci in enumerate(clamps):
            c = pts[ci]
            tan_ = (pts[min(ci + 1, len(pts) - 1)] - pts[max(ci - 1, 0)]).normalized()
            _, nn, _ = surf_point(sw, specs[ci][0], th0 + specs[ci][1], 0.0)
            out.append(D.clamp(f"arm_hose_{tag}_clamp_{k}.L", c, tan_, nn, r, "silver", bone))
        return out
    objs += hose_run("inner", 214.5, [(6.42, 0, 0.0062), (6.30, 0, 0.0092), (6.10, 1, 0.0098), (5.90, -1, 0.0098),
                                      (5.76, 0, 0.0090), (5.69, 0, 0.0055), (5.645, 0, 0.0018)], 0.0021, (1, 3), UB, sw_u)
    objs += hose_run("rear", 322.5, [(6.42, 0, 0.0062), (6.30, 0, 0.0090), (6.08, 1, 0.0096), (5.88, -1, 0.0096),
                                     (5.76, 0, 0.0088), (5.69, 0, 0.0055), (5.645, 0, 0.0018)], 0.0021, (1, 3), UB, sw_u)

    # =========================================================================== elbow pod + speaker disc
    disc = U.Spot(sw_u, Zh(DISC_Z), rad(DISC_TH))
    R = DISC_R

    def disc_hole(z, th):
        th = (th - DISC_TH + 180.0) % 360.0 - 180.0 + DISC_TH        # the pod ring runs past 360 deg: wrap into the table
        A, B = disc.AB(Zh(z), rad(th))
        return A * A + B * B < (R + 0.0016) ** 2

    pod = plate(sw_u, "arm_elbow_pod.L", PODTOP, 5.275, 270.0, 630.0, "teal", UB, dome=0.0045, inflate=0.0026, thickness=0.008,
                nu=20, nv=72, bevel=0.002, wear=0.0, hp=0.5)
    objs.append(pod)
    # the disc socket is an EXACT circular cut (a staircase hole showed teeth round the rim)
    cfr = disc.frame(off=0.0)
    cutter = L.cylinder("arm_pod_cutter", R + 0.0016, 0.020, L.Frame(cfr.p(0, 0, 0.004), cfr.x, cfr.y, cfr.z), segments=72)
    L.boolean_cut(pod, cutter)
    # bearing races where the pod meets the shaft and the forearm: pewter ring on top, gunmetal ring below
    for nm_, z0_, z1_, mt_, inf_ in (("arm_pod_race_top.L", 5.709, 5.695, "silver", 0.0064),
                                     ("arm_pod_race_bot.L", 5.288, 5.272, "gunmetal", 0.0062)):
        rb = plate(sw_u, nm_, z0_, z1_, 0, 360, mt_, UB, nu=2, nv=56, inflate=inf_, dome=0.0, thickness=0.004, bevel=0.0006,
                   bevel_seg=1, wear=0.0)
        U.weld_loose(rb)
        objs.append(rb)

    fr = disc.frame(off=-0.007)
    rim_prof = [(R - 0.0008, -0.022), (R + 0.0034, -0.022), (R + 0.0034, 0.0075), (R + 0.0028, 0.0130),
                (R + 0.0014, 0.0150), (R - 0.0004, 0.0150), (R - 0.0010, 0.0135), (R - 0.0008, -0.022)]
    rim = U.lathe("arm_disc_socket.L", fr, rim_prof, segments=64)
    U.weld_loose(rim)
    L.finish(rim, "teal", bevel=0.0007, bevel_segments=2, bone=UB, wear=0.0)
    objs.append(rim)
    Rd = R - 0.0012
    # black dish: deep soft bowl, one faint step ring, gentle central swell
    dish_prof = [(0.0, -0.003), (0.0, 0.0050), (0.16 * Rd, 0.0052), (0.34 * Rd, 0.0042), (0.58 * Rd, 0.0030),
                 (0.60 * Rd, 0.0040), (0.62 * Rd, 0.0030), (0.82 * Rd, 0.0020), (Rd, 0.0014), (Rd, -0.003), (0.0, -0.003)]
    dish = U.lathe("arm_disc_dish.L", fr, dish_prof, segments=56)
    U.weld_loose(dish)
    L.finish(dish, "darkdisc", bevel=0.0004, bevel_segments=1, bone=UB)
    objs.append(dish)
    objs.append(torus_on("arm_disc_lip.L", L.Frame(fr.p(0, 0, 0.0030), fr.x, fr.y, fr.z), 0.90 * Rd, 0.0010, "silver", UB,
                         seg=64, mseg=6))
    objs.append(torus_on("arm_disc_step.L", L.Frame(fr.p(0, 0, 0.0036), fr.x, fr.y, fr.z), 0.60 * Rd, 0.0007, "gunmetal", UB,
                         seg=56, mseg=6))
    objs.append(D.stepped("arm_disc_boss.L", L.Frame(fr.p(0, 0, 0.0058), fr.x, fr.y, fr.z),
                          [(0.17 * Rd, 0.0014), (0.12 * Rd, 0.0020)], olive_mat(), UB, segs=32))
    objs.append(D.hex_bolt("arm_disc_boss_nut.L", L.Frame(fr.p(0, 0, 0.0092), fr.x, fr.y, fr.z), 0.050 * Rd, "gunmetal", UB,
                           washer=False))
    objs.append(torus_on("arm_disc_ring_a.L", L.Frame(fr.p(0, 0, 0.0050), fr.x, fr.y, fr.z), 0.36 * Rd, 0.0006, "gunmetal", UB,
                         seg=48, mseg=6))
    objs.append(torus_on("arm_disc_ring_b.L", L.Frame(fr.p(0, 0, 0.0028), fr.x, fr.y, fr.z), 0.76 * Rd, 0.0005, "gunmetal", UB,
                         seg=56, mseg=6))
    # eight tiny studs round the socket rim
    for k in range(8):
        a_ = 2 * PI * (k + 0.5) / 8
        rr_ = R + 0.0013
        objs.append(D.round_rivet(f"arm_disc_stud_{k}.L", L.Frame(fr.p(rr_ * math.cos(a_), rr_ * math.sin(a_), 0.0148), fr.x, fr.y, fr.z),
                                  0.00095, "silver", UB))

    # ---- elbow hinge, outer and inner faces: flat machined boss (clevis plate), stepped bearing, bolt circle
    def hinge_side(tag, th_deg, n_bolts, ring_r):
        p0, n0, T0 = surf_point(sw_u, DISC_Z, th_deg, top_off("arm_elbow_pod.L", DISC_Z, th_deg) - 0.0036)
        fr0 = L.Frame.at(p0, n0, T0)
        bp = L.plate(f"arm_elbow_clevis_{tag}.L", L.outline_rrect(0.066, 0.058, 0.021, n=5), fr0, rise=0.0012,
                     thickness=0.011, steps=2)
        L.finish(bp, "gunmetal", bevel=0.0009, bevel_segments=2, bone=UB)
        out = [bp]
        top = L.Frame(fr0.p(0, 0, 0.0012), fr0.x, fr0.y, fr0.z)
        out.append(D.stepped(f"arm_elbow_bearing_{tag}.L", top, [(0.0215, 0.0014), (0.0165, 0.0014)], "silver", UB, segs=36,
                             hollow=0.0))
        out.append(D.stepped(f"arm_elbow_race_{tag}.L", L.Frame(top.p(0, 0, 0.0028), top.x, top.y, top.z),
                             [(0.0130, 0.0012)], "dark", UB, segs=32))
        out.append(D.hex_bolt(f"arm_elbow_pin_{tag}.L", L.Frame(top.p(0, 0, 0.0028), top.x, top.y, top.z), 0.0070, "gunmetal", UB,
                              h=0.0032, washer=False))
        for k in range(n_bolts):
            a_ = 2 * PI * (k + 0.5) / n_bolts
            out.append(D.hex_bolt(f"arm_elbow_bolt_{tag}_{k}.L",
                                  L.Frame(top.p(ring_r * math.cos(a_), ring_r * math.sin(a_), 0.0014), top.x, top.y, top.z), 0.0019,
                                  "gunmetal", UB, h=0.0026))
        return out
    objs += hinge_side("out", 0.0, 6, 0.0270)
    objs += hinge_side("in", 180.0, 4, 0.0270)

    # =========================================================================== FOREARM skin (0.32 H -> wrist 0.22 H)
    d_f = (W - E).normalized()
    f_top = E - d_f * hz(0.16)
    f_bot = W + d_f * hz(0.06)
    f_mid = (E + W) * 0.5 + L.V(-0.004, 0.0, 0.0)
    path_f = L.Path([f_top, E, f_mid, W, f_bot])
    rows_f = [(5.66, 0.110, 0.110, 3.0), (5.52, 0.136, 0.146, 3.0), (5.30, 0.140, 0.150, 3.0), (5.00, 0.126, 0.136, 3.0),
              (4.70, 0.109, 0.118, 3.0), (4.52, 0.098, 0.104, 3.0), (4.44, 0.094, 0.099, 3.0), (4.38, 0.088, 0.090, 3.0)]
    swf0 = L.Sweep(path_f, [(0, 0.05, 0.05)])

    def mk_f(shrink):
        ks = [(U.tz(swf0, Zh(z)), hz(rx - shrink), hz(ry - shrink), n) for z, rx, ry, n in rows_f]
        ks[0] = (0.0,) + ks[0][1:]
        ks[-1] = (1.0,) + ks[-1][1:]
        return L.Sweep(path_f, ks)

    sw_f = mk_f(0.0)
    core_f = mk_f(0.030).mesh("arm_forearm_core.L", nring=40, round_start=(hz(0.03), 3), round_end=(hz(0.03), 3))
    L.finish(core_f, "dark", bevel=0.0, bone=FB)
    objs.append(core_f)

    # ---------------- plates: smooth glossy teal, hairline seams
    slot_c = U.Spot(sw_f, Zh(SLOT_Z), rad(SLOT_TH))
    sh_ha, sh_r = SLOT_HA + 0.0030, SLOT_R + 0.0030          # recess hole, a bit larger than the bar

    def slot_hole(z, th):
        A, B = slot_c.AB(Zh(z), rad(th))
        return U.stadium_in(A, B, sh_ha + 0.0012, sh_r + 0.0012)

    ZTOP_F, ZBOT_F = 5.325, 4.505
    objs.append(plate(sw_f, "arm_forearm_inner_front.L", ZTOP_F, ZBOT_F, 2, 196, "teal", FB, nu=34, nv=30, dome=0.004,
                      wear=0.15))
    stadium_cut(objs[-1], slot_c, sh_ha + 0.0012, sh_r + 0.0012)
    objs.append(plate(sw_f, "arm_forearm_rear.L", ZTOP_F + 0.015, ZBOT_F, 202, 358, "teal", FB, nu=30, nv=24, dome=0.005,
                      wear=0.0))

    # pale facet chevron under the disc (a separate raised facet, gold hairline from the bevel)
    objs.append(plate(sw_f, "arm_forearm_facet.L", 5.292, lambda v: 5.292 - 0.092 * (1 - abs(2 * v - 1)) ** 0.85 - 0.02,
                      52, 142, "teal", FB, nu=14, nv=28, dome=0.002, inflate=0.0038, thickness=0.005, bevel=0.0015, wear=1.0,
                      hp=0.5))

    # thin swept gold-edged wing along the OUTER edge, from just below the disc, tapering to the wrist
    zw_a, zw_b = 5.345, 4.585

    def wing_h(z):
        u = (zw_a - z) / (zw_a - zw_b)
        return sm(0.0, 0.16, u) * (1.0 - 0.80 * sm(0.20, 1.0, u))

    def wing_fn(w_th, extra=0.0, hmax=0.0190):
        def fn(u, v):
            z = lerp(zw_a, zw_b, u)
            prof = (1.0 - abs(2 * v - 1)) ** 1.15
            th = w_th * (2 * v - 1) * (1.0 - 0.35 * wing_h(z))
            return U.tz(sw_f, Zh(z)), rad(th), 0.0030 + hmax * wing_h(z) * prof + extra
        return fn

    wg = U.patch(sw_f, "arm_forearm_wing.L", wing_fn(21.0), 40, 12, thickness=0.005)
    L.finish(wg, "teal", bevel=0.0016, bevel_segments=2, bone=FB, wear=1.0)
    objs.append(wg)
    wcrest = U.patch(sw_f, "arm_forearm_wing_edge.L", lambda u, v: (lambda z: (U.tz(sw_f, Zh(z)), rad((v - 0.5) * 9.0),
                     0.0030 + 0.0190 * wing_h(z) + 0.0012))(lerp(zw_a - 0.01, zw_b + 0.02, u)), 40, 2, thickness=0.003)
    L.finish(wcrest, "bronze", bevel=0.0008, bevel_segments=1, bone=FB, wear=0.0)
    objs.append(wcrest)

    # ---------------- red stadium slot: black recess + pewter lip, red bar with 2 fine dark ribs
    out_hole = U.stadium_outline(sh_ha, sh_r)
    sw_wall = U.ring_surface(sw_f, "arm_forearm_slot_recess.L", slot_c, out_hole,
                             [(0.0, 0.0006, 0.0030), (0.5, -0.0010, -0.0015), (1.0, -0.0022, -0.0060)], nu=56, thickness=0.004)
    L.finish(sw_wall, "dark", bevel=0.0004, bevel_segments=1, bone=FB)
    objs.append(sw_wall)
    sl_lip = U.ring_surface(sw_f, "arm_forearm_slot_lip.L", slot_c, out_hole,
                            [(0.0, 0.0004, 0.0028), (0.4, 0.0011, 0.0042), (0.8, 0.0024, 0.0040), (1.0, 0.0036, 0.0022)],
                            nu=56, thickness=0.004)
    L.finish(sl_lip, "silver", bevel=0.0006, bevel_segments=2, bone=FB)
    objs.append(sl_lip)
    sg = U.radial_fill(sw_f, "arm_forearm_slot_glass.L", slot_c, lambda A, B: U.stadium_in(A, B, SLOT_HA, SLOT_R),
                       centre=(0.0, 0.0), off=lambda f: -0.0042 + 0.0012 * (1 - f * f), nu=48, nv=5, rmax=0.07, thickness=0.003)
    L.finish(sg, satin_red(), bevel=0.0005, bevel_segments=1, bone=FB)
    objs.append(sg)
    for k, bo in enumerate((-0.0054, 0.0, 0.0054)):
        pts = []
        for a in (-0.033, -0.011, 0.011, 0.033):
            t_, th_ = slot_c.zt(a, bo)
            p_, n_ = U.skin_n(sw_f, t_, th_)
            pts.append(p_ + n_ * (-0.0028))
        rb_ = L.tube(f"arm_slot_rib_{k}.L", pts, 0.0007, nring=6, caps=True)
        L.finish(rb_, "dark", bevel=0, bone=FB, weighted=False)
        objs.append(rb_)

    # ---------------- one row of tiny rivets on the forearm top (outer-rear edge)
    objs += rivet_row("arm_forearm_rivet", sw_f, [(5.12 - 0.095 * k, 340, 0.0048) for k in range(7)], FB, r=0.0016)

    # ---------------- plate-corner fasteners and the slot's four screws
    for iz, zz in enumerate((5.285, 4.545)):
        for it, th_ in enumerate((26.0, 180.0)):
            objs.append(bolt_at(f"arm_fore_if_bolt_{iz}{it}.L", sw_f, "arm_forearm_inner_front.L", zz, th_, 0.0022, FB))
        for it, th_ in enumerate((218.0, 338.0)):
            objs.append(bolt_at(f"arm_fore_rear_bolt_{iz}{it}.L", sw_f, "arm_forearm_rear.L", zz, th_, 0.0022, FB))
    for k, (A_, B_) in enumerate(((-0.0595, 0.0), (0.0595, 0.0), (-0.0505, 0.0205), (0.0505, -0.0205))):
        t_, th_ = slot_c.zt(A_, B_)
        zz = (slot_c.z - A_) / H
        objs.append(bolt_at(f"arm_slot_screw_{k}.L", sw_f, "arm_forearm_inner_front.L", zz, deg(th_), 0.0017, FB,
                            kind="round", mat_="gunmetal"))

    # ---------------- two exposed cables in the inner seam, dark, clamped, diving into the cuff
    def hose_f(tag, th0, rr, clamps):
        specs = ((5.20, 0, -0.0012), (5.02, 2, 0.0004), (4.84, -2, 0.0002), (4.68, 2, 0.0004), (4.55, 0, -0.0030))
        pts = [surf_point(sw_f, z, th0 + dth, off)[0] for z, dth, off in specs]
        ob_ = L.tube(f"arm_cable_{tag}.L", pts, rr, nring=10, caps=True, round_ends=True)
        L.finish(ob_, "dark", bevel=0.0004, bevel_segments=1, bone=FB, weighted=False)
        res = [ob_]
        for k, ci in enumerate(clamps):
            tan_ = (pts[ci + 1] - pts[ci - 1]).normalized()
            _, nn, _ = surf_point(sw_f, specs[ci][0], th0 + specs[ci][1], 0.0)
            res.append(D.clamp(f"arm_cable_{tag}_clamp_{k}.L", pts[ci], tan_, nn, rr, "silver", FB))
        return res
    objs += hose_f("a", 198.0, 0.0026, (1, 3))
    objs += hose_f("b", 200.5, 0.0020, (2,))

    # ---------------- wrist: thin dark ring (about 0.013 m) with a gold hairline edge above it; dark plug into the hand
    ring = plate(sw_f, "arm_cuff_ring.L", 4.478, 4.428, 0, 360, "dark", FB, nu=3, nv=64, inflate=0.0035, dome=0.0012,
                 thickness=0.006, bevel=0.001, hp=0.5)
    U.weld_loose(ring)
    objs.append(ring)
    edge = plate(sw_f, "arm_cuff_edge.L", 4.4855, 4.4785, 0, 360, "silver", FB, nu=2, nv=64, inflate=0.0036, dome=0.0,
                 thickness=0.004, bevel=0.0006, bevel_seg=1, wear=0.0)
    U.weld_loose(edge)
    objs.append(edge)
    for nm_, z0_, z1_, mt_, inf_ in (("arm_wrist_washer_top.L", 4.506, 4.490, "silver", 0.0042),
                                     ("arm_wrist_washer_bot.L", 4.427, 4.410, "gunmetal", 0.0034)):
        rb = plate(sw_f, nm_, z0_, z1_, 0, 360, mt_, FB, nu=2, nv=48, inflate=inf_, dome=0.0, thickness=0.004, bevel=0.0006,
                   bevel_seg=1, wear=0.0)
        U.weld_loose(rb)
        objs.append(rb)
    for k in range(6):
        th_ = 30.0 + 60.0 * k
        objs.append(bolt_at(f"arm_wrist_bolt_{k}.L", sw_f, "arm_cuff_ring.L", 4.453, th_, 0.0016, FB))
    return objs


def build():
    t0 = time.time()
    left = build_side()
    only = os.environ.get("ARM_SIDE", "")
    if only == "L":
        print(f"ARM build {time.time() - t0:.1f}s (left only)")
        return left
    right = [L.mirror_x(o) for o in left]
    if only == "R":
        return right
    print(f"ARM build {time.time() - t0:.1f}s")
    return left + right
