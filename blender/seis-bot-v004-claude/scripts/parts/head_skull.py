"""head_skull - the egg: dark core, rear dome, crest (lozenge + 2 stripes per side + silver side band), side panels."""
import math
import bmesh
import bpy
import seis_lib as L
from mathutils import Vector
import seis_spec as S
from head_lib import DISC_C, DISC_N, SK, CREST, SPH, FACE, chart_grid, chart_plate, prof, ends, both, add

RT = CREST.RT
PSI_A = 14.0          # front end of the crest ribs (the brow keystone line)
GAP = 0.024           # xi gap between neighbouring ribs  (~2.9 mm)


def bump(psi, p0=20.0, p1=165.0, pk=0.45, k=0.6):
    s = (psi - p0) / (p1 - p0)
    s = min(max(s, 0.0), 1.0)
    # asymmetric bump: rises quickly from the keystone, peaks over the crown, falls toward the rear
    s2 = s ** (math.log(0.5) / math.log(pk)) if 0 < pk < 1 else s
    return max(0.0, math.sin(math.pi * s2)) ** k


def benv(psi):
    """half width (xi) of the dark teal crown cap: ~0.17 at the keystone, ~0.47 over the crown (cap 0.09 m wide), then a rear taper"""
    return 0.225 + 0.255 * bump(psi, pk=0.42, k=0.55)


def loz_half(psi):
    b = benv(psi)
    pc, pb = 118.0, 140.0
    if psi <= pc:
        return b
    t = (psi - pc) / (pb - pc)
    return b * math.sqrt(max(0.0, 1 - t * t))


def rib(name, psi0, psi1, lo, hi, rise, nu=40, nv=8, e=0.10, p=0.42, thickness=0.003, taper=0.07, lift=0.0, chart=CREST):
    """a stripe on the egg between xi = lo(psi) and hi(psi) for psi in [psi0, psi1] (degrees)."""
    def stf(u, v):
        psi = psi0 + (psi1 - psi0) * u
        l, h = lo(psi), hi(psi)
        k = 1.0 if taper <= 0 else (L.smoothstep(0.0, taper, u) * L.smoothstep(1.0, 1.0 - taper, u)) ** 0.5
        k = max(k, 0.04)
        c, w = (l + h) / 2, (h - l) * k
        xi = c + (v - 0.5) * w
        return xi * SK.a, math.radians(psi) * RT
    return chart_grid(name, chart, stf, nu, nv, lambda u, v: rise * prof(v, p) * ends(u, e) ** 0.6, thickness, lift=lift)


def build(out):
    sk = SK
    # ------------------------------------------------------------------ dark core (the grooves read as black)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=56, v_segments=34, radius=1.0)
    for v in bm.verts:
        d = v.co.normalized()
        th = math.asin(max(-1, min(1, d.z)))
        ph = math.atan2(d.x, -d.y)
        q = sk.pt_sph(ph, th, -0.0035)
        w = L.clamp((sk.yc - q.y) / 0.04)                      # follow the receding lower face (same rule as FaceChart)
        q.y += 0.12 * max(0.0, FACE.zeye - q.z) * w
        v.co = q
    me = bpy.data.meshes.new("head_skull_core")
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    core = bpy.data.objects.new("head_skull_core", me)
    L._link(core)
    for sx in (1, -1):                         # carve a pocket for each speaker cup
        Dc = Vector((sx * DISC_C.x, DISC_C.y, DISC_C.z))
        nn = Vector((sx * DISC_N.x, DISC_N.y, DISC_N.z))
        fr = L.Frame.at(Dc, nn, (0, 0, 1))
        cut = L.cylinder("_pocket", 0.0372, 0.075, L.Frame(Dc - nn * 0.022, fr.x, fr.y, fr.z), segments=40)
        L.boolean_cut(core, cut)
    L.finish(core, "pewter_shade", bevel=0, bone="head")
    out.append(core)

    # dark underlay over the rear half of the egg: the gaps between the striation slats read as real dark seams
    def under(u, v):
        return (-0.975 + 1.95 * v) * sk.a, math.radians(98.0 + (238.0 - 98.0) * u) * RT
    ul = chart_grid("head_dome_underlay", CREST, under, 26, 10, lambda u, v: 0.0, 0.0015)
    L.finish(ul, "dark", bevel=0, bone="head", apply=False)
    out.append(ul)

    # ------------------------------------------------------------------ crown cap + silver pinstripe bands (left side then mirrored)
    # ONMODEL: ONE glossy dark-teal shield cap (no bronze ladder), flanked by a SILVER band with 3-4 fine black pinstripe
    # grooves.  The grooves are real gaps (xi 0.016 = 1.5 mm) between neighbouring silver ribs over the dark core.
    def lz(u, v):
        psi = PSI_A + (140.0 - PSI_A) * u
        h = loz_half(psi)
        return ((v - 0.5) * 2 * h * sk.a, math.radians(psi) * RT)
    loz = chart_grid("head_crest_cap", CREST, lz, 36, 14,
                     lambda u, v: 0.0030 * prof(v, 0.34) * ends(u, 0.05) ** 0.5, 0.003)
    L.finish(loz, "teal", bevel=0.0013, bevel_segments=2, bone="head", wear=0.0)
    out.append(loz)

    GX = 0.017
    PWD = 0.044

    def mk_edges(k):
        def lo(psi):
            if k == 0:
                return loz_half(psi) + GAP
            return hi_k(k - 1, psi) + GX
        return lo

    def hi_k(k, psi):
        if k == 0:
            lo = loz_half(psi) + GAP
        else:
            lo = hi_k(k - 1, psi) + GX
        return lo + PWD * (1.0 + 0.16 * bump(psi, pk=0.5))

    # one smooth silver band; the pinstripe grooves are thin dark engraved lines laid on it (3 lines, 4 strips)
    BR = 0.0007

    def band_lo(psi):
        return loz_half(psi) + GAP

    def band_hi(psi):
        return hi_k(3, psi)
    rb = rib("head_band.L", PSI_A + 4, 142.0, band_lo, band_hi, BR, nu=40, nv=10, p=0.55, taper=0.0, e=0.05, thickness=0.004)
    L.finish(rb, "pewter", bevel=0.0010, bevel_segments=2, bone="head", wear=0.0, weighted=False)
    both(rb, out)
    for k in range(3):
        pts = []
        for i in range(0, 41):
            u = i / 40
            psi = 46.0 + (142.0 - 46.0) * u
            xi_ = (hi_k(k, psi) + hi_k(k, psi) + GX) / 2.0
            lo_, hi_ = band_lo(psi), band_hi(psi)
            v = (xi_ - lo_) / (hi_ - lo_)
            rr = BR * prof(v, 0.55) * ends(u, 0.05) ** 0.6
            P = CREST.map(xi_ * sk.a, math.radians(psi) * RT)
            pts.append(P[0] + P[1] * (rr + 0.0003))
        gl = L.tube(f"head_band_groove_{k}.L", pts, 0.00060, nring=4, round_ends=True)
        L.finish(gl, "dark", bevel=0, bone="head", apply=False)
        both(gl, out)

    def band_out(psi):
        return hi_k(3, psi) + GX

    # temple (front part of the side): one silver panel; rear part: teal with fine parallel striations (4 ribs)
    def sd_hi(psi): return 0.955
    sdp = rib("head_side_temple_panel.L", PSI_A - 4, 102.0, band_out, sd_hi, 0.0024, nu=26, nv=12, p=0.25, taper=0.03, e=0.04)
    L.finish(sdp, "pewter", bevel=0.0012, bevel_segments=2, bone="head", wear=0.0, weighted=False)
    both(sdp, out)

    def stri(k, n=4):
        def lo(psi):
            o = band_out(psi)
            return o + (0.955 - o) * k / n + (0.006 if k else 0.0)

        def hi(psi):
            o = band_out(psi)
            return o + (0.955 - o) * (k + 1) / n - 0.006
        return lo, hi
    for k in range(4):
        lo_f, hi_f = stri(k)
        sr = rib(f"head_side_stria_{k}.L", 104.0 - 1.5 * k, 146.0, lo_f, hi_f, 0.0020, nu=20, nv=4, p=0.30, taper=0.30)
        L.finish(sr, "teal_deep", bevel=0.0010, bevel_segments=2, bone="head", wear=0.0)
        both(sr, out)

    # lower side shells behind the cheek / speaker cup (spherical chart: phi azimuth from the front, theta elevation)
    def lowside(u, v):
        phi = math.radians(104.0 + (150.0 - 104.0) * u)
        th = math.radians(14.0 - (14.0 + 52.0) * v)
        return phi * SPH.RS, th * SPH.RT
    ls = chart_grid("head_side_lower.L", SPH, lowside, 18, 12, lambda u, v: 0.0018 * ends(u, 0.06) * ends(v, 0.08), 0.003)
    L.finish(ls, "pewter", bevel=0.0014, bevel_segments=2, bone="head", wear=0.0)
    both(ls, out)

    # smooth silver skin under the side plates: the gaps between plates show pewter, never a black hole (f10/f12: the whole side is silver)
    def skin(u, v):
        phi = math.radians(60.0 + (126.0 - 60.0) * u)
        th = math.radians(36.0 - (36.0 + 58.0) * v)
        return phi * SPH.RS, th * SPH.RT
    sk_ = chart_grid("head_side_skin.L", SPH, skin, 24, 18, lambda u, v: 0.0, 0.003, lift=0.0006)
    Dc = Vector((DISC_C.x, DISC_C.y, DISC_C.z))
    nn = Vector((DISC_N.x, DISC_N.y, DISC_N.z))
    fr_ = L.Frame.at(Dc, nn, (0, 0, 1))
    L.boolean_cut(sk_, L.cylinder("_pocket2", 0.0385, 0.075, L.Frame(Dc - nn * 0.022, fr_.x, fr_.y, fr_.z), segments=40))
    L.finish(sk_, "pewter", bevel=0.0006, bevel_segments=1, bone="head", wear=0.0)
    both(sk_, out)

    def temple(u, v):
        phi = math.radians(56.0 + (112.0 - 56.0) * u)
        th = math.radians(10.0 - 28.0 * v)
        return phi * SPH.RS, th * SPH.RT
    tp = chart_grid("head_side_temple.L", SPH, temple, 14, 10, lambda u, v: 0.0018 * ends(u, 0.08) * ends(v, 0.1), 0.003)
    L.finish(tp, "pewter", bevel=0.0013, bevel_segments=2, bone="head", wear=0.0)
    both(tp, out)

    # ------------------------------------------------------------------ rear dome (dark teal, fine parallel striations)
    NS = 7
    for k in range(NS):
        x0 = -0.955 + 1.91 * k / NS + 0.007
        x1 = -0.955 + 1.91 * (k + 1) / NS - 0.007

        def dome(u, v, x0=x0, x1=x1):
            psi = 146.0 + (236.0 - 146.0) * u
            xi = x0 + (x1 - x0) * v
            return xi * sk.a, math.radians(psi) * RT
        dm = chart_grid(f"head_rear_dome_{k}", CREST, dome, 16, 4, lambda u, v: 0.0018 * ends(u, 0.05) * prof(v, 0.3), 0.003)
        L.finish(dm, "teal_deep", bevel=0.0010, bevel_segments=2, bone="head", wear=0.0)
        out.append(dm)
    return out
