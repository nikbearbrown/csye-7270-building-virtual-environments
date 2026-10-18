"""head_extra - round 3 detail that REPLACES the rivet rows removed on-model: real engraved / piped features read from the
frames (f07 sharp crop, f08, f10, f12): pale eye rims, more forehead V cuts and bridge hatching, a champagne piping line round the
dark cap, concentric yoke swirl lines, ear-shell pinstripes + champagne rim piping, pinstripes down the temple, neck slab edge piping,
extra rings on the speaker dish, cheek chevrons.  Every object is a thin separate mesh with a material and a bone; left built, mirrored."""
import math
from mathutils import Vector
import seis_lib as L
import seis_spec as S
import head_lib as H
import head_face as F
import head_neck as N
import head_skull as K
from head_lib import both, loop_tube, FACE, SK, SPH, CREST, on_surface, oval

f8 = F.f8


def line(out, name, pts, r, mat, bone="head", mirror=True, nring=4, round_ends=True):
    t = L.tube(name, pts, r, nring=nring, round_ends=round_ends)
    L.finish(t, mat, bevel=0, bone=bone, wear=0.0, apply=False)
    if mirror:
        both(t, out)
    else:
        out.append(t)
    return t


def face_lines(out):
    # pale silver rim round each eye socket (f07: a light lip frames the red bulb), wider than the dark bezel
    cx, cz = f8(543, 614)
    rim = on_surface(FACE, oval(cx, cz, 0.0455, 0.0400, 8.0, n=40, power=2.3), 0.0016)
    t = loop_tube("head_eye_rim.L", rim, 0.0011, nring=6)
    L.finish(t, "pewter", bevel=0, bone="head", wear=0.0)
    both(t, out)
    # two more fine V cut lines on the forehead outer panel (f07 shows 4-5 short diagonal cuts running toward the brow)
    for i, (p0, p1) in enumerate((((560, 372), (640, 424)), ((600, 366), (668, 408)))):
        pts = on_surface(FACE, [f8(*p0), f8(*p1)], 0.0020)
        line(out, f"head_forehead_vcut_b{i}.L", pts, 0.00045, "dark")
    # hatch lines on the brow ridge next to the bridge (3 more, shorter)
    for i in range(3):
        y0 = 468 + 24 * i
        pts = on_surface(FACE, [f8(460, y0), f8(484, y0 + 26)], 0.0030)
        line(out, f"head_brow_hatch_{i}.L", pts, 0.00045, "dark")
    # cheek chevrons: two more diagonal cuts on the outer cheek plane toward the pod arc (f07 lines at the cheek)
    for i, (p0, p1) in enumerate((((632, 690), (590, 770)), ((650, 676), (618, 742)))):
        pts = on_surface(FACE, [f8(*p0), f8(*p1)], 0.0042)
        line(out, f"head_cheek_cut_{i}.L", pts, 0.00055, "dark")
    # a second thin brow ridge (the brow in f08 is a double shelf over the socket)
    pts = on_surface(FACE, [f8(486, 516), f8(552, 504), f8(620, 508), f8(660, 528)], 0.0060)
    line(out, "head_brow_ridge2.L", pts, 0.0010, "pewter_shade", nring=6)
    # small pale lip notches either side of the lip slot
    z_lip = f8(390, 906)[1]
    for sx in (1,):
        P, N_ = FACE.map(0.026, z_lip - 0.0010)
        pts = [P + N_ * 0.0030, P + Vector((0.010, 0.0, -0.0004)) + N_ * 0.0030]
        line(out, "head_lip_notch.L", pts, 0.0007, "pewter_shade")


def cap_lines(out):
    # champagne-silver piping line along the dark cap's edge, and a dark hairline just outside it (the cap is a separate shield)
    sk = SK
    for k, (off, mat, rad) in enumerate(((0.000, "pewter", 0.0007), (0.012, "dark", 0.0004))):
        pts = []
        for i in range(0, 31):
            psi = 22.0 + (122.0 - 22.0) * i / 30
            xi = K.loz_half(psi) + off
            P, Nn = CREST.map(xi * sk.a, math.radians(psi) * CREST.RT)
            pts.append(P + Nn * (0.0036 if k == 0 else 0.0014))
        line(out, f"head_cap_{'piping' if k == 0 else 'hairline'}.L", pts, rad, mat)
    # a hairline round the crown tip of the cap where it meets the keystone
    pts = [on_surface(FACE, [f8(390 - 78, 340)], 0.0042)[0], on_surface(FACE, [f8(390, 336)], 0.0050)[0],
           on_surface(FACE, [f8(390 + 78, 340)], 0.0042)[0]]
    line(out, "head_keystone_hairline", pts, 0.0005, "dark", mirror=False)


def temple_lines(out):
    # three long pinstripes sweeping down the silver temple (f10/f12: the dome pinstripes run on down the side of the face)
    for k, th0 in enumerate((14.0, 2.0, -10.0)):
        pts = []
        for i in range(0, 17):
            u = i / 16
            phi = math.radians(70.0 + 44.0 * u)
            th = math.radians(th0 - 22.0 * u - 6.0 * math.sin(math.pi * u))
            P = SK.pt_sph(phi, th)
            pts.append(P + SK.normal(P) * 0.0014)
        line(out, f"head_temple_pinstripe_{k}.L", pts, 0.00045, "dark")


def pod_lines(out):
    """a thin red lens ring on each pod floor (the red glows behind and round the dish: f04/f06/f10/f12)"""
    D, n = H.DISC_C, H.DISC_N
    fr = L.Frame.at(D, n, (0, 0, 1))
    pts = [D - n * 0.0138 + (fr.x * math.cos(2 * math.pi * i / 40) + fr.y * math.sin(2 * math.pi * i / 40)) * 0.0300 for i in range(40)]
    t = loop_tube("head_pod_red_ring.L", pts, 0.0007, nring=4)
    L.finish(t, "red", bevel=0, bone="head", wear=0.0)
    both(t, out)


def throat_lines(out):
    """outline of the pale throat tile and a second chevron line under the dark V (f08: tile + chevron)"""
    z0, z1 = 1.7985, 1.8140
    pts = []
    for x, z in ((-0.0125, z0 - 0.0015), (-0.0125, z1 + 0.0015), (0.0125, z1 + 0.0015), (0.0125, z0 - 0.0015), (-0.0125, z0 - 0.0015)):
        P, Nn = N.NC.map(x, z)
        pts.append(P + Nn * 0.0052)
    line(out, "neck_throat_tile_outline", pts, 0.0004, "dark", bone="neck", mirror=False, round_ends=False)
    pts = []
    for x, z in ((-0.0345, 1.7740), (0.0, 1.7580), (0.0345, 1.7740)):
        P, Nn = N.NC.map(x, z)
        pts.append(P + Nn * 0.0050)
    line(out, "neck_throat_chevron2", pts, 0.0005, "dark", bone="neck", mirror=False, round_ends=False)


def ear_lines(out):
    ep = F.ear_pt
    for j, v in enumerate((0.14, 0.80, 0.93)):
        pts = [ep(0.10 + 0.80 * i / 26, v, 0.0009) for i in range(27)]
        line(out, f"head_ear_pinstripe_{j}.L", pts, 0.0007, "dark")
    # champagne rim piping on the shell's front and rear edges (f06/f12: champagne edge on the dark teal shell)
    for nm, v in (("front", 0.0), ("rear", 1.0)):
        pts = [ep(0.04 + 0.92 * i / 28, v, 0.0016) for i in range(29)]
        line(out, f"head_ear_piping_{nm}.L", pts, 0.0011, "gold", nring=6)
    # the gold inner face of the cup shows as a fine line just inside the shell's front opening (f06/f10: gold inside the ear shell)
    pts = [ep(0.08 + 0.84 * i / 24, 0.06, -0.0044) for i in range(25)]
    line(out, "head_ear_inner_line.L", pts, 0.0008, "gold", nring=6)


def neck_lines(out):
    a0 = math.asin(0.0405 / N.rx_(1.80))
    for i in range(N.SLAB_N):
        zlo = N.SLAB_Z0 + N.SLAB_PITCH * i
        for e, z in (("lo", zlo + 0.0012), ("hi", zlo + N.SLAB_H - 0.0012)):
            pts = [N.neck_pt(z, a0 + (math.pi - 0.05 - a0) * k / 20, N.SLAB_OUT * 0.80) for k in range(21)]
            line(out, f"neck_slab_edge_{i}_{e}.L", pts, 0.0006, "pewter_shade", bone="neck", nring=4, round_ends=False)
    # two thin dark rails either side of the red throat panel, and a pale tile outline
    for sx_, z0, z1 in ((0.0412, N.SLAB_Z0 - 0.002, N.SLAB_Z0 + N.SLAB_PITCH * 3 + N.SLAB_H + 0.001),):
        pts = []
        for k in range(9):
            z = z0 + (z1 - z0) * k / 8
            P, Nn = N.NC.map(sx_, z)
            pts.append(P + Nn * 0.0050)
        line(out, "neck_throat_rail.L", pts, 0.0006, "dark", bone="neck")


def cup_lines(out):
    D, n = H.DISC_C, H.DISC_N
    fr = L.Frame.at(D, n, (0, 0, 1))
    hv, uv = -fr.y, fr.x
    off = -hv * 0.0050 - uv * 0.0040
    base = D - n * 0.0145 + off
    for j, (r_, h_, mat) in enumerate(((0.0085, 0.0112, "gunmetal"), (0.0155, 0.0085, "gunmetal"), (0.0235, 0.0060, "gunmetal"))):
        pts = [base + n * h_ + (fr.x * math.cos(2 * math.pi * i / 36) + fr.y * math.sin(2 * math.pi * i / 36)) * r_ for i in range(36)]
        t = loop_tube(f"head_speaker_groove_{j}.L", pts, 0.0004, nring=4)
        L.finish(t, mat, bevel=0, bone="head", wear=0.0)
        both(t, out)


def build(out):
    face_lines(out)
    cap_lines(out)
    temple_lines(out)
    pod_lines(out)
    throat_lines(out)
    ear_lines(out)
    neck_lines(out)
    cup_lines(out)
    return out
