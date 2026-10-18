"""head_neck - neck core, two columns of 4 arched lames, throat chevrons over a red core, collar bars, V sternum bracket,
nape bands and the round back socket.  Bone: neck (the head carries the chin yoke)."""
import math
from mathutils import Vector
import seis_lib as L
import seis_spec as S
from head_lib import chart_plate, chart_grid, both, loop_tube, shrink, prof, ends

NECK_Z0 = 1.725          # bottom of the dark plug (inside the chest)
NECK_Z1 = 1.905          # top (inside the head)
Z_COLLAR = S.hh(6.9)     # 1.762


def yc(z):
    """neck axis y at height z: leans forward 11 degrees, passes (y=+0.0128, z=neck_base) -> (y=-0.0128, z=head pivot)"""
    return 0.0128 + 0.012 - 0.2 * (z - Z_COLLAR)


def rx_(z):
    return 0.073 + 0.012 * L.clamp((1.84 - z) / 0.10)


def ry_(z):
    return 0.060 + 0.006 * L.clamp((1.84 - z) / 0.10)


class NeckChart:
    """(x, z) -> front surface of the neck core."""
    def y(self, x, z):
        r = max(0.0, 1 - (x / rx_(z)) ** 2)
        return yc(z) - ry_(z) * math.sqrt(max(r, 0.0004))

    def map(self, x, z):
        e = 0.0008
        fx = (self.y(x + e, z) - self.y(x - e, z)) / (2 * e)
        fz = (self.y(x, z + e) - self.y(x, z - e)) / (2 * e)
        return Vector((x, self.y(x, z), z)), Vector((fx, -1.0, fz)).normalized()


class PlaneChart:
    """(x, z) -> the sloping chest top in front of the neck base (collar / sternum bracket)."""
    def y(self, x, z):
        return -0.100 - 0.30 * abs(x) - 0.55 * max(0.0, 1.775 - z)

    def map(self, x, z):
        e = 0.0008
        fx = (self.y(x + e, z) - self.y(x - e, z)) / (2 * e)
        fz = (self.y(x, z + e) - self.y(x, z - e)) / (2 * e)
        return Vector((x, self.y(x, z), z)), Vector((fx, -1.0, fz)).normalized()


NC, PC = NeckChart(), PlaneChart()


SLAB_Z0 = 1.744          # lowest slab bottom
SLAB_PITCH = 0.0205
SLAB_H = 0.0160
SLAB_N = 4
SLAB_OUT = 0.0058        # slab outer face stands this far off the dark core


def neck_pt(z, ang, off=0.0):
    """point on the neck ellipse at height z, angle ang (radians) from the front (0) toward +x (pi/2) and the back (pi); off = outward"""
    rx, ry = rx_(z), ry_(z)
    x, y = rx * math.sin(ang), yc(z) - ry * math.cos(ang)
    nx, ny = math.sin(ang) / rx, -math.cos(ang) / ry
    ln = math.hypot(nx, ny)
    return Vector((x + off * nx / ln, y + off * ny / ln, z))


def slab_fn(i, a0, a1, off=SLAB_OUT):
    zlo = SLAB_Z0 + SLAB_PITCH * i

    def fn(u, v):
        z = zlo + SLAB_H * u
        ang = a0 + (a1 - a0) * v
        o = off * (1.0 - 0.28 * (2 * u - 1) ** 2)                           # slightly crowned face
        return neck_pt(z, ang, o)
    return fn


def build(out):
    # ----------------------------------------------------------------- dark core (the plug)
    path = [Vector((0.0, yc(z), z)) for z in (NECK_Z0, 1.78, 1.84, NECK_Z1)]
    keys = [(0.0, rx_(NECK_Z0) * 0.97, ry_(NECK_Z0) * 0.97, 2.0), (0.5, rx_(1.8) * 0.97, ry_(1.8) * 0.97, 2.0), (1.0, rx_(NECK_Z1) * 0.97, ry_(NECK_Z1) * 0.97, 2.0)]
    sw = L.Sweep(path, keys)
    core = sw.mesh("neck_core", nring=48, round_start=(0.006, 2))
    L.finish(core, "dark", bevel=0, bone="neck")
    out.append(core)

    # ----------------------------------------------------------------- 4 flat horizontal pewter slabs per side, round to the back
    a0 = math.asin(0.0405 / rx_(1.80))
    for i in range(SLAB_N):
        fn = slab_fn(i, a0, math.pi - 0.05)
        pu = fn(0.55, 0.5) - fn(0.5, 0.5)
        pv = fn(0.5, 0.55) - fn(0.5, 0.5)
        flip = pu.cross(pv).dot(Vector((1, 0, 0)) * 0 + (fn(0.5, 0.5) - Vector((0, yc(1.80), 1.80)))) < 0
        slab = L.grid_surface(f"neck_slab_{i}.L", fn, 6, 24, thickness=0.0048, flip=flip, offset=-1.0)
        L.finish(slab, "pewter", bevel=0.0016, bevel_segments=2, bone="neck", wear=0.0)
        both(slab, out)
        # dark centre line on the slab face (the pinstripe groove of the reference)
        pts = [neck_pt(SLAB_Z0 + SLAB_PITCH * i + SLAB_H * 0.5, a0 + (math.pi - 0.05 - a0) * k / 20, SLAB_OUT * 0.96)
               for k in range(21)]
        gl = L.tube(f"neck_slab_line_{i}.L", pts, 0.0005, nring=4)
        L.finish(gl, "dark", bevel=0, bone="neck", apply=False)
        both(gl, out)

    # ----------------------------------------------------------------- RED throat panel with a pale tile and a dark V chevron below
    zt0, zt1 = SLAB_Z0 - 0.002, SLAB_Z0 + SLAB_PITCH * (SLAB_N - 1) + SLAB_H + 0.001
    red = chart_plate("neck_red_throat", [(-0.0405, zt1), (0.0405, zt1), (0.0405, zt0), (-0.0405, zt0)], NC, rise=0.0035,
                      thickness=0.004, steps=2, lift=0.0010, step=0.004)
    L.finish(red, "red", bevel=0.0010, bone="neck")
    out.append(red)
    tile = chart_plate("neck_throat_tile", shrink([(-0.0105, 1.8140), (0.0105, 1.8140), (0.0105, 1.7985), (-0.0105, 1.7985)], 0.0004),
                       NC, rise=0.0030, thickness=0.004, steps=1, lift=0.0045, step=0.003)
    L.finish(tile, "pewter", bevel=0.0009, bone="neck", wear=0.0)
    out.append(tile)
    chev = [(-0.0345, 1.7860), (0.0, 1.7700), (0.0345, 1.7860), (0.0345, 1.7795), (0.0, 1.7635), (-0.0345, 1.7795)]
    cv = chart_plate("neck_throat_chevron", shrink(chev, 0.0004), NC, rise=0.0030, thickness=0.004, steps=1, lift=0.0042, step=0.003)
    L.finish(cv, "dark", bevel=0.0008, bone="neck")
    out.append(cv)

    # (collar Y-fork, lozenge pads, sternum bracket and the nape port belong to `shoulder` / `torso` on-model: not duplicated here)
    return out
