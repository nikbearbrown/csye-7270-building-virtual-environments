"""torso_hw - hardware creators for parts/torso.py (conform round 2): fasteners, washers, bearing rings, clevis plates, cable
clamps, ferrules and a dark-red shade material.  Everything returns UNFINISHED objects (torso.fin() finishes them) and is given in
metres / world axes.  A "site" is (point, normal): point on a surface, normal pointing away from it."""
import math
import bpy
from mathutils import Vector
import seis_lib as L


# ------------------------------------------------------------------------------------------------------- materials
_RS = {}


def redshade():
    """dark crimson satin for the cavity behind the armour (f07: the field between struts is #59010B-#770105, never glossy cherry)"""
    m = bpy.data.materials.get("SEIS_redshade")
    if m is not None:
        return m
    import seis_mat as M
    m, nt, b, out = M._simple("SEIS_redshade", M.hexlin("#5C0310"), metallic=0.0, rough=0.40, coat=0.3, coat_rough=0.15)
    return m


def podred():
    """satin crimson #A30515 for the ab pods: roughness 0.32 and a weak coat, so no white corner glints (critic torso 4)"""
    m = bpy.data.materials.get("SEIS_podred")
    if m is not None:
        return m
    import seis_mat as M
    m, nt, b, out = M._simple("SEIS_podred", M.hexlin("#8E0414"), metallic=0.0, rough=0.42, coat=0.08, coat_rough=0.3)
    return m


def olive():
    """olive-bronze band metal that stays olive under any lighting (f07: blades #615A3C, long spine bar #4D411A, belt #5A4C2F);
    the shared fully-metallic bronze mirrors the dark studio and goes black on small flat parts"""
    m = bpy.data.materials.get("SEIS_olive")
    if m is not None:
        return m
    import seis_mat as M
    m, nt, b, out = M._simple("SEIS_olive", M.hexlin("#3F381C"), metallic=0.3, rough=0.36, coat=0.15, coat_rough=0.25)
    return m


# ------------------------------------------------------------------------------------------------------ fasteners
def _fr(p, n, xhint=(1, 0, 0)):
    return L.Frame.at(Vector(p), Vector(n), xhint)


def hexbolt(name, p, n, r=0.0028, h=0.0022):
    """hex head bolt: `r` is the circumradius of the hex (so 4-6 mm across flats), standing `h` above the surface."""
    return L.bolt(name, Vector(p), Vector(n), radius=r, height=h, hexagon=True)


def washer(name, p, n, r=0.0042, h=0.0008):
    fr = _fr(p, n)
    return L.cylinder(name, r, h, L.Frame(fr.p(0, 0, h / 2), fr.x, fr.y, fr.z), segments=20)


def rivet(name, p, n, r=0.0022):
    """round (dome) head rivet"""
    fr = _fr(p, n)
    return L.sphere(name, r, L.Frame(fr.o, fr.x, fr.y, fr.z), scale=(1, 1, 0.55), segments=12, rings=6)


def ring_stack(name, p, n, rings, segments=28):
    """stepped bearing ring / washer stack; rings = [(radius, height), ...] base outward-to-inward"""
    return L.disc_stack(name, Vector(p), Vector(n), rings, segments=segments)


def pin(name, p, n, r=0.0022, length=0.012, segments=14):
    """cylindrical pin / axle centred on p, along n"""
    fr = _fr(p, n)
    return L.cylinder(name, r, length, L.Frame(fr.o, fr.x, fr.y, fr.z), segments=segments)


def clevis_plate(name, p, n, w=0.014, h=0.012, t=0.0020, xhint=(1, 0, 0), roundr=0.004):
    """small rounded plate lying on a surface: centred on p, thickness t along n"""
    fr = _fr(p, n, xhint)
    outl = L.outline_rrect(w, h, roundr, 4)
    verts, faces = [], []
    k = len(outl)
    for (x, y) in outl:
        verts.append(fr.p(x, y, 0.0))
    for (x, y) in outl:
        verts.append(fr.p(x, y, t))
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    faces.append(tuple(range(k - 1, -1, -1)))
    faces.append(tuple(k + i for i in range(k)))
    ob = L.new_mesh(name, verts, faces)
    # orientation check
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    if bm.calc_volume(signed=True) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.to_mesh(ob.data)
        ob.data.update()
    bm.free()
    return ob


def clamp_band(name, p, n, tangent, w=0.026, hgt=0.006, t=0.0035):
    """strap clamp: a flat box across a strut/cable at p, long side along `tangent`, standing t above the surface"""
    fr = L.Frame.at(Vector(p), Vector(n), tangent)
    return L.box(name, (w, hgt, t), L.Frame(fr.p(0, 0, t / 2), fr.x, fr.y, fr.z))


def ferrule(name, p, direction, r=0.0044, length=0.010):
    fr = L.Frame.at(Vector(p), Vector(direction), (1, 0, 0))
    return L.cylinder(name, r, length, L.Frame(fr.p(0, 0, length / 2), fr.x, fr.y, fr.z), segments=16)
