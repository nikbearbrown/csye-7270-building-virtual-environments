"""foot_detail - small tidy detail for the foot (round-2): ankle hinge assemblies, toe flex hinge, plate fasteners, hoses.
All helpers add LEFT-side objects to the foot Reg `reg`; the caller mirrors.  Sizes 4-6 mm fasteners, never noisy."""
import math
from mathutils import Vector
import seis_lib as L
from foot_kit import H, AX, P, h, join_named

PI = math.pi


def _frame(center, normal, xhint=(0, 0, 1)):
    return L.Frame.at(Vector(center), Vector(normal), xhint)


def _cyl(name, fr, r, z0, hgt, seg=36, r2=None):
    return L.cylinder(name, r, hgt, L.Frame(fr.p(0, 0, z0 + hgt / 2), fr.x, fr.y, fr.z), segments=seg, radius2=r2)


def _hex(name, center, normal, r=0.0025, hgt=0.0027, xhint=(0, 0, 1), washer=True):
    parts = []
    fr = _frame(center, normal, xhint)
    if washer:
        parts.append(_cyl(name + "_w", fr, r * 1.55, -0.0003, 0.0009, seg=12))
        parts.append(_cyl(name + "_h", fr, r, 0.0006, hgt, seg=6))
    else:
        parts.append(_cyl(name + "_h", fr, r, -0.0003, hgt, seg=6))
    return parts


def _round(name, center, normal, r=0.0023, hgt=0.0022, xhint=(0, 0, 1)):
    fr = _frame(center, normal, xhint)
    w = _cyl(name + "_w", fr, r * 1.5, -0.0003, 0.0008, seg=12)
    hd = _cyl(name + "_h", fr, r, 0.0005, hgt, seg=14, r2=r * 0.78)
    return [w, hd]


def ankle_hinge(reg, hk, HF, sgn, bone, full=True):
    """clevis plate + stepped bearing (base, ring, recess, boss) + washer + round-head bolts on one side of the heel"""
    tag = "out" if sgn > 0 else "in"
    c = hk.pt(HF, 0.0 if sgn > 0 else PI, 0.0)
    n = Vector((sgn, 0, 0))
    xh = Vector((0, -1, 0))                    # local x = forward
    sz = (0.058, 0.046) if full else (0.050, 0.040)
    rr = 0.016 if full else 0.014
    pl = L.plate("clevis", L.outline_rrect(sz[0], sz[1], rr, n=8), L.Frame.at(c + n * 0.0016, n, xh), rise=0.0012,
                 thickness=0.0045, steps=2, inset=0.002)
    reg.add(pl, f"ankle_clevis_{tag}", "gunmetal", bone, bevel=0.0012, seg=2, wear=0)
    fr = L.Frame.at(c + n * 0.0016, n, xh)
    k = 0.85 if full else 0.74
    reg.add(_cyl("b", fr, 0.0166 * k, 0.0, 0.0036), f"ankle_bearing_base_{tag}", "gunmetal", bone, bevel=0.0012, seg=2, wear=0)
    reg.add(L.torus("r", 0.0128 * k, 0.0026 * k, L.Frame(fr.p(0, 0, 0.0036), fr.x, fr.y, fr.z), 40, 8),
            f"ankle_bearing_ring_{tag}", "bronze", bone, bevel=0, wear=None)
    reg.add(_cyl("rc", fr, 0.0098 * k, 0.0030, 0.0012), f"ankle_bearing_recess_{tag}", "darkdisc", bone, bevel=0.0004, seg=1, wear=0)
    reg.add(_cyl("wa", fr, 0.0072 * k, 0.0040, 0.0013, seg=32), f"ankle_washer_{tag}", "bronze", bone, bevel=0.0004, seg=1, wear=None)
    reg.add(_cyl("bo", fr, 0.0046 * k, 0.0050, 0.0044, seg=28, r2=0.0040 * k), f"ankle_boss_{tag}", "bronze", bone, bevel=0.0009, seg=2, wear=0)
    reg.add(L.torus("col", 0.0205 * k, 0.0015, L.Frame(fr.p(0, 0, 0.0012), fr.x, fr.y, fr.z), 44, 8),
            f"ankle_bearing_collar_{tag}", "bronze", bone, bevel=0, wear=None)


def toe_hinge(reg, up, CF, FB, TB):
    """flex hinge across the toe seam: a clevis plate each side, a pin cap + washer in it, two hex bolts"""
    caps, bolts = [], []
    for sgn, tag in ((1, "out"), (-1, "in")):
        c = up.pt(CF, 0.0 if sgn > 0 else PI, 0.0)
        n = Vector((sgn, 0, 0))
        xh = Vector((0, -1, 0))
        fr0 = L.Frame.at(c + n * 0.0032, n, xh)
        pl = L.plate("tc", L.outline_rrect(0.044, 0.021, 0.0095, n=8), fr0, rise=0.0010, thickness=0.0030, steps=2, inset=0.0012)
        reg.add(pl, f"toe_clevis_{tag}", "gunmetal", FB, bevel=0.0010, seg=2, wear=0)
        fr = L.Frame.at(c + n * 0.0038, n, xh)
        caps.append(_cyl("w", fr, 0.0058, 0.0, 0.0010, seg=28))
        caps.append(_cyl("c", fr, 0.0040, 0.0010, 0.0024, seg=24, r2=0.0034))
        for dx in (-0.0150, 0.0150):
            bolts += _hex("tb", fr.p(dx, 0, 0.0004), n, r=0.0021, hgt=0.0022, xhint=xh, washer=False)
    reg.add(join_named(caps, "toe_pins"), "toe_hinge_pin_caps", "silver", FB, bevel=0.0004, seg=1, wear=None)
    reg.add(join_named(bolts, "toe_bolts"), "toe_hinge_bolts", "silver", FB, bevel=0.0003, seg=1, wear=None)


def plate_fasteners(reg, up, hk, sw, IN_F0, IN_F1, IN_A0, IN_A1, Q_F0, Q_F1, FB):
    # instep plate: 4 round heads at the corners
    parts = []
    for fH in (IN_F0 + 0.045, IN_F1 - 0.050):
        for th in (IN_A0 + 0.14, IN_A1 - 0.14):
            p = up.pt(fH, th, 0.0019 - 0.0002)
            parts += _round("is", p, up.nrm(fH, th), r=0.0022, hgt=0.0022, xhint=(0, -1, 0))
    reg.add(join_named(parts, "instep_bolts"), "instep_plate_bolts", "silver", FB, bevel=0.0004, seg=1, wear=None)
    # quarter plates: 2 hex bolts each, on the plate's upper edge region
    parts = []
    for th in (0.30, PI - 0.30):
        for fH in (Q_F0 + 0.07, Q_F1 - 0.10):
            p = up.pt(fH, th, 0.0017 - 0.0002)
            parts += _hex("qb", p, up.nrm(fH, th), r=0.0024, hgt=0.0026, xhint=(0, -1, 0))
    reg.add(join_named(parts, "quarter_bolts"), "quarter_plate_bolts", "silver", FB, bevel=0.0004, seg=1, wear=None)
    # heel cap plate: 4 hex bolts at its corners
    parts = []
    for fH in (-0.255, -0.075):
        for th in (0.55 + 0.20, PI - 0.55 - 0.20):
            p = hk.pt(fH, th, 0.0018 - 0.0002)
            parts += _hex("hb", p, hk.nrm(fH, th), r=0.0027, hgt=0.0029, xhint=(0, -1, 0))
    reg.add(join_named(parts, "heel_bolts"), "heel_cap_bolts", "silver", FB, bevel=0.0004, seg=1, wear=None)


def hoses(reg, hk, FB):
    """two thin hoses down the INNER ankle into the heel wedge, with clamps and ferrules"""
    hose_defs = [
        (0.0034, [P(-0.050, -0.040, 0.078), P(-0.066, -0.047, 0.060), P(-0.071, -0.060, 0.074), None], -0.215, PI - 1.05),
        (0.0026, [P(-0.030, -0.046, 0.082), P(-0.048, -0.056, 0.064), P(-0.056, -0.068, 0.078), None], -0.255, PI - 0.80),
    ]
    hoses_o, clamps, fer = [], [], []
    for k, (r, pts, fE, thE) in enumerate(hose_defs):
        end = hk.pt(fE, thE, 0.0)
        # end point just inside the wedge surface, route comes from above
        pts = list(pts[:-1]) + [end + (hk.nrm(fE, thE)) * 0.0006]
        tube = L.tube(f"hose{k}", pts, r, nring=10, round_ends=True)
        hoses_o.append(tube)
        path = L.Path(pts, n_per_seg=12)
        for tt in (0.30, 0.62):
            pc = path.at(tt)
            tg = path.tangent(tt)
            fr = L.Frame.at(pc, tg, (1, 0, 0))
            clamps.append(L.torus(f"cl{k}", r * 1.02, r * 0.42, fr, 14, 6))
            clamps += _hex("cb", pc + fr.x * (r * 1.5), fr.x, r=0.0017, hgt=0.0018, xhint=(0, 0, 1), washer=False)
        # ferrule where the hose enters the wedge
        te = path.tangent(0.96)
        fe = L.Frame.at(path.at(0.95), te, (1, 0, 0))
        fer.append(L.cylinder(f"fe{k}", r * 1.45, 0.0075, L.Frame(fe.o, fe.x, fe.y, fe.z), segments=20))
    reg.add(join_named(hoses_o, "hoses"), "ankle_hoses", "silver", FB, bevel=0, wear=None)
    reg.add(join_named(clamps, "clamps"), "hose_clamps", "bronze", FB, bevel=0.0003, seg=1, wear=None)
    reg.add(join_named(fer, "ferrules"), "hose_ferrules", "gunmetal", FB, bevel=0.0005, seg=1, wear=0)


def _x_at(hk, t, z, sgn):
    """half width (x offset from the ankle axis) of the heel skin at path param t and height z, on side sgn"""
    sc = hk.sw.sec(t)
    zp = hk.sw.path.at(t).z
    u = (z - zp - sc["oy"]) / sc["ryp"]
    u = max(-0.999, min(0.999, u))
    return sgn * sc["rxp"] * (1 - abs(u) ** sc["n"]) ** (1 / sc["n"])


def heel_detail(reg, hk, up, FB, TB_BONE="toes.L"):
    """clean heel dressing: gold + silver rim pipes round the scooped arch, two gusset ribs, a kick plate, three dark vent slots,
    a dark gasket ring where the shin drops into the boot, a bronze outer ring on the ankle bearing"""
    import seis_spec as S
    from foot import ARCH_F, ARCH_R
    f0 = h(ARCH_F)
    R = h(ARCH_R)
    zc = 0.0015
    for sgn, tag in ((1, "out"), (-1, "in")):
        for k, (rr, mat, rad) in enumerate(((R + 0.0016, "gold", 0.0016), (R + 0.0052, "silver", 0.0010))):
            pts = []
            for i in range(24):
                a = math.radians(8 + 164 * i / 23)
                f = f0 + rr * math.cos(a)
                z = zc + rr * math.sin(a)
                t = hk.t_of(f)
                pts.append(P(_x_at(hk, t, z, sgn), f, z))
            reg.add(L.tube(f"arch{k}", pts, rad, nring=8, round_ends=True), f"heel_arch_{'rim' if k == 0 else 'silver_rim'}_{tag}", mat, FB, bevel=0, wear=None)
        # gusset ribs: two thin raised ribs running up the flank from the heel top toward the back
        for k, fH in enumerate((-0.385, -0.35, -0.315)):
            pts = []
            for i in range(10):
                z = 0.050 + 0.030 * i / 9
                t = hk.t_of(h(fH))
                pts.append(P(_x_at(hk, t, z, sgn) + sgn * 0.0006, h(fH), z))
            reg.add(L.tube(f"rib{k}", pts, 0.0017, nring=8, round_ends=True), f"heel_gusset_rib_{k}_{tag}", "gunmetal", FB, bevel=0, wear=0)
    # kick plate on the very back of the heel (centre line, rear face)
    ptsr = [hk.pt(-0.305 + 0.0 * i, PI / 2 * 0 + 0, 0.0) for i in range(1)]
    cp = hk.sw.panel("kick", hk.t_of(h(-0.422)), hk.t_of(h(-0.385)), PI / 2 - 0.9, PI / 2 + 0.9, thickness=0.0025, inflate=0.0014,
                     height=0.0014, hp=1.0, ends=0.2, nu=8, nv=12)
    reg.add(cp, "heel_kick_plate", "gunmetal", FB, bevel=0.0012, seg=2, wear=0)
    # three recessed vent slots on the rear of the heel
    sl = []
    for k, dx in enumerate((-0.020, 0.0, 0.020)):
        c = hk.pt(-0.40, PI / 2, 0.0)
        sl.append(L.box(f"vent{k}", (0.008, 0.0035, 0.034), L.Frame(origin=Vector((c.x + dx, c.y + 0.0006, c.z - 0.010)))))
    reg.add(join_named(sl, "vents"), "heel_vent_slots", "dark", FB, bevel=0.0006, seg=1, wear=None)

    # silver rim pipe along the top edge of the heel wedge, each side
    for sgn, tag in ((1, "out"), (-1, "in")):
        th = 0.62 if sgn > 0 else PI - 0.62
        pts = [hk.pt(-0.40 + 0.26 * i / 14, th, 0.0004) for i in range(15)]
        reg.add(L.tube("hrim", pts, 0.0012, nring=8, round_ends=True), f"heel_top_rim_pipe_{tag}", "silver", FB, bevel=0, wear=None)
    # one silver wrap-line round the rear of the wedge (a clean seam, not a strap)
    t1 = hk.t_of(h(-0.375))
    wr = [hk.sw.point(t1, 2 * PI * k / 64, 0.0006) for k in range(65)]
    reg.add(L.tube("wrap", wr, 0.0011, nring=6, n_per_seg=2), "heel_rear_wrap_line", "silver", FB, bevel=0, wear=None)
    # silver pipe under the gold welt at the toe (silver-gold edge piping)
    tl = []
    for sgn in (1, -1):
        th = -0.70 if sgn > 0 else PI + 0.70
        tl.append(L.tube("toesilv", [up.pt(0.64 + (0.88 - 0.64) * i / 8, th, 0.0003) for i in range(9)], 0.0011, nring=6, round_ends=True))
    reg.add(join_named(tl, "toe_silver"), "toe_silver_pipe", "silver", TB_BONE, bevel=0, wear=None)
