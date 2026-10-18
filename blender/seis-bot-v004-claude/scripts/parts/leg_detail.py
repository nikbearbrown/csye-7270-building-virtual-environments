"""leg_detail - small tidy hardware for the leg module (round 2): fasteners with washers, clamps, hoses, bearing
rings, ray-cast seating on plates.  Only calls seis_lib; nothing here edits the shared toolkit."""
import math
import bpy
from mathutils import Vector
import seis_lib as L

PI = math.pi


def sync():
    bpy.context.view_layer.update()


def drop(targets, origin, direction, max_dist=0.2):
    """Ray-cast onto the closest of `targets`; returns (point, normal) or (None, None)."""
    best = (None, None, 1e9)
    d = Vector(direction).normalized()
    for t in targets:
        p, n = L.surface_hit(t, origin, d, max_dist)
        if p is not None:
            dist = (p - Vector(origin)).length
            if dist < best[2]:
                best = (p, n, dist)
    return best[0], best[1]


def site(sk, s, w=None, th=None, back=False):
    """world point + outward normal on a Skin at metric (s, w) or (s, th)"""
    t = L.clamp(s / sk.len)
    if th is None:
        th = sk.theta(t, w, back)
    return sk.sw.point(t, th), sk.sw.outward(t, th)


def seat(sk, targets, s, w=None, th=None, back=False):
    """a point on the visible surface of `targets` at the skin site (s, w/th) and its normal"""
    p, n = site(sk, s, w, th, back)
    hit, hn = drop(targets, p + n * 0.05, -n, 0.12)
    if hit is None:
        return p, n
    if hn.dot(n) < 0:
        hn = -hn
    return hit, hn


def fastener(name, c, n, r=0.0026, h=0.0022, kind="hex", wr=1.6, wh=0.0007, xhint=(1, 0, 0)):
    """washer + hex head (or domed round head) sitting on a surface at c with outward normal n.  ONE object."""
    n = Vector(n).normalized()
    c = Vector(c) - n * 0.0004
    w = L.bolt(name + "_w", c, n, radius=r * wr, height=wh + 0.0004, hexagon=False, xhint=xhint)
    top = c + n * (wh + 0.0004)
    if kind == "hex":
        hd = L.bolt(name + "_h", top, n, radius=r, height=h, hexagon=True, xhint=xhint)
    else:
        fr = L.Frame.at(top, n, xhint)
        hd = L.sphere(name + "_h", r * 1.15, fr, scale=(1, 1, 0.55), segments=14, rings=6)
    return L.join([w, hd], name)


def stepped(name, c, n, rings, segments=40, xhint=(1, 0, 0)):
    """bearing / washer stack: rings = [(radius, height), ...] base outward; ONE object (L.disc_stack)"""
    return L.disc_stack(name, Vector(c), Vector(n).normalized(), rings, segments=segments, xhint=xhint)


def clamp(name, p, tangent, r, width=0.006, xhint=(0, 0, 1)):
    """hose clamp: band round a tube of radius r at p along `tangent`, plus a buckle block.  ONE object."""
    t = Vector(tangent).normalized()
    fr = L.Frame.at(Vector(p), t, xhint)
    band = L.cylinder(name + "_b", r * 1.5, width, L.Frame(Vector(p), fr.x, fr.y, fr.z), segments=18)
    bk = L.box(name + "_k", (r * 0.9, r * 0.9, width * 1.15),
               L.Frame(Vector(p) + fr.x * (r * 1.5 + r * 0.25), fr.x, fr.y, fr.z))
    return L.join([band, bk], name)


def hose(name, pts, r, nring=10):
    return L.tube(name, [Vector(p) for p in pts], r, nring=nring, caps=True, round_ends=True)


def tangent_at(pts, i):
    a = Vector(pts[max(0, i - 1)])
    b = Vector(pts[min(len(pts) - 1, i + 1)])
    return (b - a).normalized()
