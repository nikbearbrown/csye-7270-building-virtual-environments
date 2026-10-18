"""leg - SEIS bot thigh shells, red inlays, knee, shin/calf plates, ankle housing (left built, right mirrored).

Bones: thigh.L/R (thigh core + shells + inlays + knee hood/cap above the knee axis), shin.L/R (everything below the
knee axis down to the ankle housing).  See leg.NOTES.md.
"""
import math
import bpy
import seis_lib as L
import seis_spec as S
import leg_helpers as LH
from leg_helpers import Skin, patch, ring, leaf_outline, leaf_patch, leaf_hw
from mathutils import Vector

PI = math.pi
h = S.hh
H = S.H
rad = math.radians
sm = LH.sm
sin = math.sin

OBJS = []          # left-side objects (mirrored at the end)


def fin(o, mat, bone, bevel=0.002, seg=2, wear=1.0, angle=38.0):
    """wear = gold TRIM strength on teal (0 = no gold line, 1 = thin gold line on every bevelled edge)."""
    L.finish(o, mat, bevel=bevel, bevel_segments=seg, bone=bone, wear=(wear if mat == "teal" else None),
             angle=angle)
    OBJS.append(o)
    return o


def K(t, rx, ry, n=3.2, **kw):
    d = dict(t=t, rx=h(rx), ry=h(ry), n=n)
    d.update({k: (h(v) if k in ("ox", "oy", "rxp", "rxn", "ryp", "ryn") else v) for k, v in kw.items()})
    return d


def fpatch_gen(sk, S_, name, z0, z1, f0, f1, infl, height, hp=1.0, ends=0.12, back=False, nu=20, nv=12, thick=0.007,
               top=0.0, bot=0.0, f0b=None, f1b=None):
    """Front-face plate between heights z0..z1 (head heights) and lateral fractions f0..f1 (f=+1 outer edge).
    top/bot = metres the top / bottom edge arches (top>0 arches UP in the middle, bot>0 points DOWN in the middle)."""
    s0, s1 = S_(z0), S_(z1)

    def suv(u, v):
        vv = 2 * v - 1
        arch = 1 - vv * vv
        ss0 = s0 - top * arch
        ss1 = s1 + bot * arch
        s = ss0 + (ss1 - ss0) * u
        a = f0 + (f0b - f0) * u if f0b is not None else f0
        b = f1 + (f1b - f1) * u if f1b is not None else f1
        return (s, (a + (b - a) * v) * sk.width(s))

    def off(u, v):
        e = sm(0, ends, u) * sm(1, 1 - ends, u) if ends else 1.0
        return infl + height * (sin(PI * v) ** hp) * e

    return patch(sk, name, suv, off, nu=nu, nv=nv, thickness=thick, back=back)


def theta_patch(sk, S_, name, z0, z1, a0, a1, infl, height, hp=0.8, ends=0.1, nu=20, nv=12, thick=0.008, top=0.0,
                bot=0.0):
    """Plate wrapping round the limb between angles a0 and a1 (degrees, or callables of t returning radians)."""
    s0, s1 = S_(z0), S_(z1)

    def suv(u, v):
        vv = 2 * v - 1
        arch = 1 - vv * vv
        ss0, ss1 = s0 - top * arch, s1 + bot * arch
        s = ss0 + (ss1 - ss0) * u
        t = s / sk.len
        A = a0(t) if callable(a0) else rad(a0)
        B = a1(t) if callable(a1) else rad(a1)
        return (s, None, A + (B - A) * v)

    def off(u, v):
        e = sm(0, ends, u) * sm(1, 1 - ends, u) if ends else 1.0
        return infl + height * (sin(PI * v) ** hp) * (0.5 + 0.5 * e)

    return patch(sk, name, suv, off, nu=nu, nv=nv, thickness=thick)


# =================================================================================================== THIGH
# On-model (ONMODEL.md LEG + CRITIC leg 1): thigh 20 % narrower / 15 % shallower, no red leaf, no bronze plates, no
# hoses (the two black cords between the thighs), clean glossy teal with at most thin gold edge lines.
# The thigh is ONE smooth teal skin that tapers into the knee hood, carrying a few low raised pads (front shield with a
# gold edge, outer fender, inner and rear pads) over thin dark seam lines.
ZT_TOP, ZT_BOT = 4.90, 2.50          # skin sweep top / bottom (head heights above floor)


def zt(z):
    return (ZT_TOP - z) / (ZT_TOP - ZT_BOT)


def thigh_sweep():
    # round 2 (CRITIC leg 1): heavier, tapering thigh: 0.23 m wide under the belt -> 0.18 m above the knee, 0.23 m deep
    P = [(h(.45), h(0.0), h(4.90)), (h(.465), h(0.0), h(4.62)), (h(.49), h(-.05), h(3.70)), (h(.53), h(-.10), h(2.62)),
         (h(.545), h(-.108), h(2.50))]
    keys = [K(zt(4.90), .37, .43, 3.0), K(zt(4.62), .415, .45, 3.0), K(zt(4.0), .395, .46, 3.2),
            K(zt(3.5), .36, .45, 3.2), K(zt(3.05), .33, .42, 3.3), K(zt(2.72), .315, .385, 3.4),
            K(zt(2.50), .31, .37, 3.4)]
    return L.Sweep([Vector(p) for p in P], keys)


def seam(sk, S_, name, fn_edge, z0, z1, off=0.0045, wd=0.012):
    """thin dark seam strip along a lateral fraction edge f=fn_edge(z)"""
    def suv(u, v):
        z = z0 + (z1 - z0) * u
        s = S_(z)
        return (s, (fn_edge(z) + (v - 0.5) * wd) * sk.width(s))
    return patch(sk, name, suv, lambda u, v: off, nu=22, nv=2, thickness=0.003)




import leg_detail as LD


def fx(name, pt, nrm, bone, mat="gunmetal", kind="hex", r=0.0026, h_=0.0022):
    """one fastener (washer + head) seated at pt with outward normal nrm"""
    o = LD.fastener(name, pt, nrm, r=r, h=h_, kind=kind)
    return fin(o, mat, bone, bevel=0.0003, seg=1)


def tube_pts(sk, s_list, w, offs, back=True):
    out = []
    for s, off in zip(s_list, offs):
        p, n = LD.site(sk, s, w=w, back=back)
        out.append(p + n * off)
    return out


# =================================================================================================== THIGH
def build_thigh():
    sw = thigh_sweep()
    sk = Skin(sw)
    S_ = lambda z: (ZT_TOP - z) / (ZT_TOP - ZT_BOT) * sk.len
    B = "thigh.L"
    skin = thigh_sweep().mesh("leg_thigh_skin.L", nring=48, round_start=(h(.05), 3), round_end=(h(.035), 3))
    fin(skin, "teal", B, bevel=0, wear=0)
    plates = []

    def a_mid(t):
        return rad(14)

    # ---- outer fender in two overlapping plates (upper laps over lower)
    o = theta_patch(sk, S_, "leg_thigh_fender_low.L", 3.92, 3.00, -40, a_mid, 0.003, 0.005, hp=0.8, ends=0.10, nu=26,
                    nv=14, thick=0.008, top=h(.03), bot=h(.08))
    fin(o, "teal", B, bevel=0.003, seg=3, wear=0); plates.append(o)
    o = theta_patch(sk, S_, "leg_thigh_fender_up.L", 4.58, 3.88, -40, a_mid, 0.003, 0.005, hp=0.8, ends=0.10, nu=26,
                    nv=14, thick=0.008, top=h(.05), bot=h(.0))
    fin(o, "teal", B, bevel=0.003, seg=3, wear=0); plates.append(o)

    # ---- front shield in two overlapping plates, gold bevel edge (wear 1)
    fp = fpatch_gen(sk, S_, "leg_thigh_shield_low.L", 3.78, 3.04, 0.50, -0.92, 0.003, 0.006, hp=0.9, nu=28, nv=18,
                    thick=0.008, top=h(.0), bot=h(.09))
    fin(fp, "teal", B, bevel=0.0025, seg=3, wear=1.0); plates.append(fp)
    fp = fpatch_gen(sk, S_, "leg_thigh_shield_up.L", 4.52, 3.80, 0.50, -0.92, 0.003, 0.006, hp=0.9, nu=28, nv=18,
                    thick=0.008, top=h(.03), bot=h(.0))
    fin(fp, "teal", B, bevel=0.0025, seg=3, wear=1.0); plates.append(fp)
    # lap seam: dark strip under the upper plate's lower lip
    ls = fpatch_gen(sk, S_, "leg_thigh_lap_seam.L", 3.793, 3.787, 0.52, -0.94, 0.0028, 0.0, nu=3, nv=14, thick=0.002)
    fin(ls, "dark", B, bevel=0)

    # ---- inner pad + rear shells (upper / lower)
    def a_in(t):
        return sk.theta(t, -0.92 * sk.sw.sec(t)["rxp"])

    o = theta_patch(sk, S_, "leg_thigh_inner.L", 4.46, 3.08, a_in, 236, 0.003, 0.005, hp=0.8, ends=0.1, nu=20,
                    nv=10, thick=0.007, top=h(.02), bot=h(.05))
    fin(o, "teal", B, bevel=0.0022, seg=2, wear=0); plates.append(o)
    o = theta_patch(sk, S_, "leg_thigh_rear_low.L", 3.84, 3.00, 238, 322, 0.003, 0.006, hp=0.8, ends=0.1, nu=26,
                    nv=14, thick=0.008, top=h(.0), bot=h(.08))
    fin(o, "teal", B, bevel=0.0025, seg=3, wear=0); plates.append(o)
    o = theta_patch(sk, S_, "leg_thigh_rear_up.L", 4.52, 3.84, 238, 322, 0.003, 0.006, hp=0.8, ends=0.1, nu=26,
                    nv=14, thick=0.008, top=h(.03), bot=h(.0))
    fin(o, "teal", B, bevel=0.0025, seg=3, wear=0); plates.append(o)

    # ---- ONE hairline seam at the outer edge (CRITIC leg 1) + hairline grooves at the plate edges
    sm_ = seam(sk, S_, "leg_thigh_seam_outer.L", lambda z: 0.97, 4.55, 3.10, off=0.0030, wd=0.0035)
    fin(sm_, "dark", B, bevel=0)

    # ---- hip collar: a dark groove ring hidden under the belt lip (no black strap, no silver lip, no bolts)
    cp = [Vector((h(.4625), h(0.0), h(4.69))), Vector((h(.4655), h(0.0), h(4.64)))]
    col = L.Sweep(cp, [K(0, .428, .468, 3.0), K(1, .43, .468, 3.0)]).mesh("leg_thigh_collar.L", nring=44)
    fin(col, "teal", B, bevel=0.0012, seg=2, wear=0)

    LD.sync()
    # ---- rear-of-thigh rivets stay (not visible in any frame view of the front; hidden-side hardware)
    k = 0
    for (z, a) in ((4.40, 252), (4.40, 308), (3.30, 252), (3.30, 308), (4.00, 252), (4.00, 308), (3.65, 252),
                   (3.65, 308), (4.62, 270), (3.10, 270), (3.50, 290), (4.20, 290)):
        p, n = LD.seat(sk, plates, S_(z), th=rad(a))
        fx(f"leg_thigh_rivet_rear_{k}.L", p, n, B, "gunmetal", "hex", 0.0025); k += 1
    k = 0
    # inner-face hardware (faces the other thigh; invisible in the front frames, kept from the stills)
    for (z, a) in ((4.30, 214), (3.85, 214), (3.40, 214), (4.30, 230), (3.85, 230), (3.40, 230)):
        p, n = LD.seat(sk, plates, S_(z), th=rad(a))
        fx(f"leg_thigh_rivet_inner_{k}.L", p, n, B, "gunmetal", "round", 0.0022); k += 1
    # hairline grooves along the plate edges (engraved seams, 0.0012 m)
    for nm, fe, z0, z1 in (("up_a", lambda z: 0.53, 4.50, 3.82), ("up_b", lambda z: -0.95, 4.50, 3.82),
                           ("lo_a", lambda z: 0.53, 3.76, 3.08), ("lo_b", lambda z: -0.95, 3.76, 3.08)):
        gs = seam(sk, S_, f"leg_thigh_groove_{nm}.L", fe, z0, z1, off=0.0016, wd=0.0022)
        gs2 = gs
        fin(gs2, "dark", B, bevel=0)
    return sk


# =================================================================================================== KNEE (thigh part)
def cap_hw(half, v):
    """kneecap half width at v (0 = top, 1 = tip): rounded top, rounded narrower bottom (capsule shield)."""
    vv = 2 * v - 1
    return half * max(0.0, 1 - abs(vv) ** 3.4) ** 0.45 * (1.0 - 0.24 * v)


def build_knee(sk_thigh, S_thigh):
    B = "thigh.L"
    K0 = S.J("knee.L")
    xk, yk, zk = K0.x, K0.y, K0.z
    hb = L.Sweep([Vector((h(.545), h(-.108), h(2.56))), Vector((h(.55), h(-.105), h(2.34)))],
                 [K(0, .30, .36, 3.0), K(1, .31, .37, 3.0)]).mesh("leg_knee_hinge_core.L", nring=36)
    fin(hb, "dark", B, bevel=0)
    kz = lambda z: (3.2 - z) / 1.3
    ksw = L.Sweep([Vector((h(.54), h(-.10), h(3.2))), Vector((h(.55), h(-.10), h(2.62))),
                   Vector((h(.556), h(-.085), h(2.05))), Vector((h(.558), h(-.075), h(1.9)))],
                  [K(kz(3.2), .32, .40, 3.4), K(kz(2.62), .31, .37, 3.1), K(kz(2.43), .345, .38, 3.1),
                   K(kz(2.05), .385, .385, 3.0, oy=0.025), K(kz(1.9), .38, .38, 3.0, oy=0.028)])
    ks = Skin(ksw)
    zs = lambda z: (3.2 - z) / 1.3 * ks.len

    half = 0.051                                   # kneecap 0.102 m wide (ONMODEL: 0.102 x 0.158 m)
    s_top, s_tip = zs(2.76), zs(2.14)              # 0.158 m tall (0.62 H)
    s_stip = zs(2.10)
    sk_half = half + 0.0028                        # narrow black gap hugging the cap (CRITIC: 0.015 m)

    def suv_sock(u, v):
        s = zs(2.40) + (s_stip - zs(2.40)) * v
        vv = (s - zs(2.40)) / (s_stip - zs(2.40))
        return (s, (2 * u - 1) * sk_half * max(0.0, 1 - max(0.0, 2 * vv - 1) ** 2.2) ** 0.45 * (1 - 0.30 * max(0, vv)) * (0.55 + 0.45 * sm(0, 0.3, vv)))

    sock = patch(ks, "leg_knee_socket.L", suv_sock, lambda u, v: 0.012, nu=14, nv=18, thickness=0.01)
    fin(sock, "dark", B, bevel=0.001, seg=1)

    def suv_pipe(u, v, side):
        s = zs(2.40) + (s_stip - zs(2.40)) * v
        vv = (s - zs(2.40)) / (s_stip - zs(2.40))
        hw = sk_half * max(0.0, 1 - max(0.0, 2 * vv - 1) ** 2.2) ** 0.45 * (1 - 0.30 * max(0, vv)) * (0.55 + 0.45 * sm(0, 0.3, vv))
        return (s, side * (hw + 0.0008 + 0.0035 * u))

    for side, nm in ((1, "a"), (-1, "b")):
        pp = patch(ks, f"leg_knee_socket_pipe_{nm}.L", lambda u, v, side=side: suv_pipe(u, v, side),
                   lambda u, v: 0.0125, nu=2, nv=24, thickness=0.003)
        fin(pp, "silver", B, bevel=0.0006, seg=1)

    def suv_cap(u, v):
        return (s_top + (s_tip - s_top) * v, (2 * u - 1) * cap_hw(half, v))

    def off_cap(u, v):
        hw = (1 - (2 * u - 1) ** 2) ** 0.55
        return 0.016 + 0.034 * hw * sin(PI * (0.03 + 0.94 * v)) ** 0.45 * (1 - 0.35 * v ** 3)

    cap = patch(ks, "leg_knee_cap.L", suv_cap, off_cap, nu=18, nv=26, thickness=0.012)
    fin(cap, "teal", B, bevel=0.0026, seg=3, wear=1.0)

    xs = -0.011
    def suv_str(u, v):
        vv = 0.06 + 0.86 * v
        return (s_top + (s_tip - s_top) * vv, xs + (u - 0.5) * 0.0065)

    def off_str(u, v):
        vv = 0.06 + 0.86 * v
        uu = 0.5 + xs / max(1e-6, cap_hw(half, vv)) / 2.0
        uu = min(max(uu, 0.0), 1.0)
        return off_cap(uu, vv) + 0.0016

    st = patch(ks, "leg_knee_cap_stripe.L", suv_str, off_str, nu=2, nv=22, thickness=0.0015)
    fin(st, "bronze", B, bevel=0.0004, seg=1)

    # ---- knee side wings: two low teal fairings flanking the kneecap (on-model: dark teal hood either side of the cap)
    for th_a, th_b, nm in ((50, 74, "a"), (106, 130, "b")):
        wg = theta_patch(ks, zs, f"leg_knee_wing_{nm}.L", 2.96, 2.50, th_a, th_b, 0.0022, 0.0045, hp=0.8, ends=0.15,
                         nu=20, nv=8, thick=0.004, top=h(.04), bot=h(.03))
        fin(wg, "teal", B, bevel=0.0014, seg=2, wear=0)
    # ---- lateral hinge: clevis plate + stacked bearing (flush, gunmetal base, teal ring, dark dish, olive boss)
    tk = zs(2.45) / ks.len
    for th0, sgn, nm in ((0.0, 1, "out"), (PI, -1, "in")):
        p0 = ksw.point(tk, th0)
        n = ksw.outward(tk, th0)
        c = p0 - n * 0.004
        base = L.disc_stack(f"leg_knee_hinge_base_{nm}.L", c, n, [(0.0315, 0.0078)], segments=48)
        fin(base, "gunmetal", B, bevel=0.0012, seg=2)
        rng = L.disc_stack(f"leg_knee_hinge_ring_{nm}.L", c + n * 0.0072, n, [(0.0268, 0.0040)], segments=48)
        fin(rng, "teal", B, bevel=0.0012, seg=2, wear=1.0)
        rec = L.disc_stack(f"leg_knee_hinge_dish_{nm}.L", c + n * 0.0108, n, [(0.0185, 0.0012)], segments=40)
        fin(rec, "darkdisc", B, bevel=0.0004, seg=1)
        bs = L.disc_stack(f"leg_knee_hinge_boss_{nm}.L", c + n * 0.0118, n, [(0.0080, 0.0028), (0.0048, 0.0040)],
                          segments=32)
        fin(bs, "bronze", B, bevel=0.0007, seg=1)
        if sgn > 0:
            # clevis plate: pointed teardrop leaf running up the thigh side from the bearing, held by two fasteners
            cv = theta_patch(ks, zs, "leg_knee_clevis.L", 2.88, 2.36, -10, 10, 0.0024, 0.0030, hp=0.8, ends=0.15,
                             nu=22, nv=10, thick=0.004, top=h(.06), bot=h(.02))
            fin(cv, "teal", B, bevel=0.0014, seg=2, wear=1.0)
    return ks


# =================================================================================================== SHIN
ZS_TOP, ZS_BOT = 2.62, 0.30
LENS_Z0, LENS_Z1 = 2.27, 1.45          # twin lens plates: 0.207 m long, start at the kneecap's lower edge
CM, HWM = 0.0650, 0.0310               # lens centre 0.0625 m off the shin axis, half width 0.0285 m


def build_shin(sk_thigh, S_thigh):
    B = "shin.L"
    zspan = ZS_TOP - ZS_BOT
    zs_t = lambda z: (ZS_TOP - z) / zspan
    P = [(h(.55), h(-.10), h(2.62)), (h(.56), h(-.06), h(1.5)), (h(.58), h(0.0), h(0.30))]
    keys = [K(zs_t(2.62), .31, .37, 3.0), K(zs_t(2.43), .345, .38, 3.1), K(zs_t(2.05), .385, .385, 3.0, oy=0.025),
            K(zs_t(1.62), .375, .35, 3.0, oy=0.03), K(zs_t(1.30), .325, .30, 3.0), K(zs_t(1.05), .295, .27, 3.1),
            K(zs_t(0.80), .275, .245, 3.2), K(zs_t(0.58), .275, .22, 3.3, ryp=.245, ryn=.19),
            K(zs_t(0.42), .275, .21, 3.4, ryp=.32, ryn=.17), K(zs_t(0.30), .275, .20, 3.4, ryp=.41, ryn=.16)]
    sw = L.Sweep([Vector(p) for p in P], keys)
    sk = Skin(sw)
    S_ = lambda z: zs_t(z) * sk.len
    shell = L.Sweep([Vector(p) for p in P], keys).mesh("leg_shin_shell.L", nring=48, round_start=(h(.04), 2))
    fin(shell, "teal", B, bevel=0, wear=0)

    # ---- central crest in three overlapping plates (upper laps over mid over lower), gold edge on the bevels
    CZ0, CZ1 = 2.30, 0.34

    def crest_plate(name, za, zb, lift):
        def zf(z):
            return (CZ0 - z) / (CZ0 - CZ1)

        def suv_cr(u, v):
            z = za + (zb - za) * u
            s = S_(z)
            f = 0.034 - 0.004 * sm(0.45, 0.8, zf(z)) + 0.014 * sm(0.80, 1.0, zf(z))
            return (s, (2 * v - 1) * f)

        def off_cr(u, v):
            e = sm(0, 0.10, u) * sm(1.0, 0.88, u)
            z = za + (zb - za) * u
            flare = 0.008 * sm(0.62, 1.0, zf(z)) ** 1.6
            return lift + 0.0032 * (1 - (2 * v - 1) ** 2) * e + flare

        return patch(sk, name, suv_cr, off_cr, nu=24, nv=10, thickness=0.008)

    crests = []
    for nm, za, zb, lift in (("up", 2.30, 1.56, 0.0050), ("mid", 1.64, 0.92, 0.0036), ("low", 1.00, 0.34, 0.0022)):
        cr = crest_plate(f"leg_shin_crest_{nm}.L", za, zb, lift)
        fin(cr, "teal", B, bevel=0.0018, seg=2, wear=1.0)
        crests.append(cr)
    for k, zl in enumerate((1.60, 0.96)):
        def suv_ls(u, v, zl=zl):
            return (S_(zl + 0.004 - 0.008 * u), (2 * v - 1) * 0.030)
        lsm = patch(sk, f"leg_shin_lap_seam_{k}.L", suv_ls, lambda u, v: 0.0022, nu=3, nv=8, thickness=0.002)
        fin(lsm, "dark", B, bevel=0)

    # thin gold centre line (0.004 m) from the knee V-plate to the instep
    def suv_gl(u, v):
        s = S_(2.12) + (S_(0.36) - S_(2.12)) * u
        return (s, (v - 0.5) * 0.004)

    def off_gl(u, v):
        z = 2.12 + (0.36 - 2.12) * u
        zf = (CZ0 - z) / (CZ0 - CZ1)
        lift = 0.0050 if z > 1.60 else (0.0036 if z > 0.96 else 0.0022)
        return lift + 0.0032 + 0.0010 + 0.008 * sm(0.62, 1.0, zf) ** 1.6

    gl = patch(sk, "leg_shin_gold_line.L", suv_gl, off_gl, nu=60, nv=2, thickness=0.0015)
    fin(gl, "gold", B, bevel=0.0004, seg=1)

    # ---- TWIN red almond lenses flanking the crest (each ~0.055 x 0.207 m), dark socket and silver piping
    s0, s1 = S_(LENS_Z0), S_(LENS_Z1)

    def lens_suv(side, grow=0.0):
        def f(u, v):
            s = s0 + (s1 - s0) * u
            hw = LH.leaf_hw(u, HWM + grow, 0.40, 0.004, 0.55)
            return (s, side * (CM + hw * (2 * v - 1)))
        return f

    lens_red = []
    for side, nm in ((1, "out"), (-1, "in")):
        so = patch(sk, f"leg_lens_socket_{nm}.L", lens_suv(side, 0.0018),
                   lambda u, v: 0.0022 + 0.0015 * sin(PI * u) ** 0.5, nu=26, nv=12, thickness=0.006)
        fin(so, "dark", B, bevel=0.0008, seg=1)
        red = patch(sk, f"leg_lens_red_{nm}.L", lens_suv(side),
                    lambda u, v: 0.004 + 0.027 * (sin(PI * v) ** 0.60) * (sin(PI * (0.03 + 0.94 * u)) ** 0.5),
                    nu=30, nv=14, thickness=0.008)
        fin(red, "red", B, bevel=0.001, seg=2)
        lens_red.append(red)
        # silver piping round the lens (ONMODEL: silver-gold edge)
        outl = LH.leaf_outline(s0, s1 - s0, side * CM, HWM + 0.0006, 0.40, n=26, sharp=0.55, hwmin=0.004)
        rg = ring(sk, f"leg_lens_piping_{nm}.L", outl, 0.0016, lambda v: 0.0040, thickness=0.002,
                  d_in=0.0, nv=2)
        fin(rg, "gold", B, bevel=0.0007, seg=1)

    # ---- the rear: two dark struts either side of the thin red strip (ONMODEL: 0.065 x 0.9 H, confirmed)
    sw_ = h(0.032)
    for side, nm in ((1, "a"), (-1, "b")):
        def suvs(u, v, side=side):
            s = S_(1.66) + (S_(0.40) - S_(1.66)) * u
            return (s, side * (h(0.035) + sw_ * v))
        o = patch(sk, f"leg_calf_strut_{nm}.L", suvs, lambda u, v: 0.003 + 0.006 * (sin(PI * v) ** 0.7) *
                  sm(0, .08, u) * sm(1, .85, u), nu=18, nv=6, thickness=0.01, back=True)
        fin(o, "dark", B, bevel=0.002, seg=2)
    strip = patch(sk, "leg_calf_red_strip.L", lambda u, v: (S_(1.62) + (S_(0.44) - S_(1.62)) * u, (v - 0.5) * h(0.065)),
                  lambda u, v: 0.009 + 0.006 * sin(PI * v) ** 0.6, nu=14, nv=6, thickness=0.006, back=True)
    fin(strip, "red", B, bevel=0.001, seg=2)

    # ---- silver outer-edge piping down the shin (f02: silver line continues below the lens)
    for side, nm in ((1, "out"), (-1, "in")):
        def suv_pp(u, v, side=side):
            s = S_(1.46) + (S_(0.50) - S_(1.46)) * u
            return (s, side * (0.80 * sk.width(s) + (v - 0.5) * 0.0032))
        pp = patch(sk, f"leg_shin_edge_piping_{nm}.L", suv_pp, lambda u, v: 0.0016, nu=34, nv=2, thickness=0.0015)
        fin(pp, "silver", B, bevel=0.0004, seg=1)

    # ---- ROUND 3 structure: dark hairline grooves along both crest edges (on-model: dark outline round the crest)
    def crest_f(z):
        zf = (CZ0 - z) / (CZ0 - CZ1)
        return 0.034 - 0.004 * sm(0.45, 0.8, zf) + 0.014 * sm(0.80, 1.0, zf)

    for side, nm in ((1, "a"), (-1, "b")):
        def suv_g(u, v, side=side):
            z = 2.26 + (1.10 - 2.26) * u
            return (S_(z), side * (crest_f(z) + 0.0022 + (v - 0.5) * 0.0013))
        gr = patch(sk, f"leg_shin_crest_groove_{nm}.L", suv_g, lambda u, v: 0.0016, nu=60, nv=2, thickness=0.0012)
        fin(gr, "dark", B, bevel=0)

    # ---- V plate: pointed teal tongue under the kneecap socket, gold edge (on-model: pale V outline)
    def suv_v(u, v):
        z = 2.30 + (2.02 - 2.30) * u
        hw = 0.026 * (1 - u) ** 0.8 + 0.003
        return (S_(z), (2 * v - 1) * hw)
    vp = patch(sk, "leg_shin_vplate.L", suv_v, lambda u, v: 0.0072 + 0.0022 * (1 - (2 * v - 1) ** 2), nu=16, nv=10,
               thickness=0.006)
    fin(vp, "teal", B, bevel=0.0016, seg=2, wear=1.0)

    # ---- brow piping: silver-gold piping runs down the outer edge from the knee brow to the lens, then on
    for side, nm in ((1, "out"), (-1, "in")):
        def suv_up(u, v, side=side):
            s = S_(2.52) + (S_(2.28) - S_(2.52)) * u
            return (s, side * (0.84 * sk.width(s) + (v - 0.5) * 0.0030))
        up = patch(sk, f"leg_shin_brow_piping_{nm}.L", suv_up, lambda u, v: 0.0016, nu=14, nv=2, thickness=0.0015)
        fin(up, "silver", B, bevel=0.0004, seg=1)
        def suv_lo(u, v, side=side):
            s = S_(0.52) + (S_(0.34) - S_(0.52)) * u
            return (s, side * (0.80 * sk.width(s) + (v - 0.5) * 0.0032))
        lo = patch(sk, f"leg_shin_ankle_piping_{nm}.L", suv_lo, lambda u, v: 0.0016, nu=10, nv=2, thickness=0.0015)
        fin(lo, "silver", B, bevel=0.0004, seg=1)

    # ---- calf rear: five dark transverse ribs bridging the two struts either side of the red strip
    for k, z in enumerate((1.50, 1.30, 1.10, 0.90, 0.70)):
        def suv_rb(u, v, z=z):
            return (S_(z + 0.012 - 0.024 * u), (2 * v - 1) * h(0.095))
        rb = patch(sk, f"leg_calf_rib_{k}.L", suv_rb, lambda u, v: 0.0045 + 0.003 * (1 - (2 * v - 1) ** 2), nu=3, nv=8,
                   thickness=0.004, back=True)
        fin(rb, "dark", B, bevel=0.0006, seg=1)

    # ---- rear-of-calf hardware (rear faces are not in the frames, kept from the stills): hex heads along both struts
    LD.sync()
    k = 0
    for z in (1.55, 1.25, 0.95, 0.70, 0.48):
        for sgn in (-1, 1):
            p, n = LD.site(sk, S_(z), w=sgn * 0.0127, back=True)
            fx(f"leg_calf_strut_bolt_{k}.L", p + n * 0.0075, n, B, "gunmetal", "hex", 0.0022, 0.0018); k += 1

    # ---- crest tail: the lower crest keeps sweeping to the ankle in one swept strip (no instep window step)
    def suv_tail(u, v):
        z = 0.40 + (0.27 - 0.40) * u
        return (S_(z), (2 * v - 1) * (0.040 - 0.012 * u))
    tl = patch(sk, "leg_shin_crest_tail.L", suv_tail, lambda u, v: 0.0040 + 0.0030 * (1 - (2 * v - 1) ** 2) +
               0.008 * u ** 1.6, nu=12, nv=8, thickness=0.006)
    fin(tl, "teal", B, bevel=0.0016, seg=2, wear=1.0)

    # ---- ankle: dark plug 0.05 H into the foot (the foot module owns the collar and the drum)
    A = S.J("ankle.L")
    plug = L.Sweep([Vector((A.x, A.y, h(0.40))), Vector((A.x, A.y, h(0.30)))],
                   [K(0, .28, .19, 3.4), K(1, .26, .17, 3.4)]).mesh("leg_ankle_plug.L", nring=32, round_end=(h(.02), 2))
    fin(plug, "dark", B, bevel=0)

    # ---- cables down the calf rear, held by clamps, ending in a small junction block
    for side, nm in ((1, "a"), (-1, "b")):
        zlist = (2.28, 2.02, 1.78, 1.58)
        pts = tube_pts(sk, [S_(z) for z in zlist], side * 0.0335, (0.016, 0.014, 0.012, 0.011))
        hs = LD.hose(f"leg_calf_hose_{nm}.L", pts, 0.0042)
        fin(hs, "dark", B, bevel=0)
        path = L.Path(pts)
        for i, tt in enumerate((0.32, 0.68)):
            cp_, tg = path.at(tt), path.tangent(tt)
            cl = LD.clamp(f"leg_calf_clamp_{nm}{i}.L", cp_, tg, 0.0052, 0.0055)
            fin(cl, "gunmetal", B, bevel=0.0004, seg=1)
        pe = pts[-1]
        te = LD.tangent_at(pts, len(pts) - 1)
        jb = L.box(f"leg_calf_junction_{nm}.L", (0.016, 0.012, 0.020), L.Frame.at(pe + te * 0.006, te))
        fin(jb, "gunmetal", B, bevel=0.0018, seg=2)
        p, n = pe + te * 0.006, te
        o = LD.fastener(f"leg_calf_junction_bolt_{nm}.L", pe + te * 0.0168, te, r=0.002, h=0.0018, kind="hex")
        fin(o, "silver", B, bevel=0.0003, seg=1)
    return sk


def build_back_of_knee(sk_t, S_t, sk_s, S_s):
    """thin cables behind the knee: thigh half ends in a gunmetal coupler, shin half starts inside it"""
    for side, nm in ((1, "a"), (-1, "b")):
        w = side * 0.030
        zl = (3.15, 2.92, 2.70, 2.55)
        pts = tube_pts(sk_t, [S_t(z) for z in zl], w, (0.012, 0.014, 0.016, 0.018))
        hs = LD.hose(f"leg_knee_hose_up_{nm}.L", pts, 0.0052)
        fin(hs, "dark", "thigh.L", bevel=0)
        path = L.Path(pts)
        for i, tt in enumerate((0.25, 0.60)):
            cp_, tg = path.at(tt), path.tangent(tt)
            cl = LD.clamp(f"leg_knee_clamp_{nm}{i}.L", cp_, tg, 0.0052, 0.0055)
            fin(cl, "gunmetal", "thigh.L", bevel=0.0004, seg=1)
        # coupler at the knee axis
        pe = pts[-1]
        te = LD.tangent_at(pts, len(pts) - 1)
        cpl = L.disc_stack(f"leg_knee_coupler_{nm}.L", pe - te * 0.004, te, [(0.0088, 0.004), (0.0074, 0.012),
                                                                      (0.0092, 0.0035)], segments=28)
        fin(cpl, "gunmetal", "thigh.L", bevel=0.0006, seg=1)
        # shin half
        zl2 = (2.50, 2.34)
        p0 = pe + te * 0.008
        pts2 = [p0] + tube_pts(sk_s, [S_s(z) for z in zl2], w, (0.018, 0.016))
        hs2 = LD.hose(f"leg_knee_hose_dn_{nm}.L", pts2, 0.0052)
        fin(hs2, "dark", "shin.L", bevel=0)


def build():
    OBJS.clear()
    skt = build_thigh()
    S_t = lambda z: (ZT_TOP - z) / (ZT_TOP - ZT_BOT) * skt.len
    build_knee(skt, S_t)
    sks = build_shin(skt, S_t)
    S_s = lambda z: (ZS_TOP - z) / (ZS_TOP - ZS_BOT) * sks.len
    build_back_of_knee(skt, S_t, sks, S_s)
    out = list(OBJS)
    for o in list(OBJS):
        out.append(L.mirror_x(o))
    return out
