#!/usr/bin/env python3
"""Procedural Planet Express ship (Futurama) for Blender 4.x.

Built from 5 reference photos of a model kit (teal hull, red cheatline stripe,
cream riveted trim, wraparound cockpit glass, porthole row, big tail fin with
circular PLANET EXPRESS logo, side strakes, glowing rear thruster cluster,
roof dome + periscope + antenna, tricycle landing gear).

Run:
    blender --background --python planet_express.py

Outputs (in this folder):
    planet_express.blend        - the model, organized in collection "PlanetExpress"
    planet_express_preview.png  - Cycles preview render (1280x720)
    planet_express_logo.png     - generated logo decal texture

Coordinate system: nose toward +Y, up +Z, units ~ meters.
"""

import bpy
import math
import os
from bisect import bisect_left
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Collection / scene helpers
# ----------------------------------------------------------------------------

def get_collection():
    coll = bpy.data.collections.get("PlanetExpress")
    if coll is None:
        coll = bpy.data.collections.new("PlanetExpress")
        bpy.context.scene.collection.children.link(coll)
    return coll

COLL = None  # set in main()

def own(obj):
    """Move an ops-created object into our collection."""
    COLL.objects.link(obj)
    try:
        bpy.context.scene.collection.objects.unlink(obj)
    except RuntimeError:
        pass
    return obj

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for coll in list(bpy.data.collections):
        if coll.name != "PlanetExpress":
            try:
                bpy.context.scene.collection.children.unlink(coll)
            except RuntimeError:
                pass
            bpy.data.collections.remove(coll)

def assign_mat(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True

def make_mesh_obj(name, verts, faces, mat, do_smooth=True):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    COLL.objects.link(obj)
    assign_mat(obj, mat)
    if do_smooth:
        smooth(obj)
    return obj

# ----------------------------------------------------------------------------
# Materials
# ----------------------------------------------------------------------------

def principled(name, base=(0.8, 0.8, 0.8, 1.0), metallic=0.0, rough=0.5,
               emission=None, estrength=0.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    def put(key, val):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = val
    put("Base Color", base)
    put("Metallic", metallic)
    put("Roughness", rough)
    if emission is not None:
        if len(emission) == 3:
            emission = (*emission, 1.0)
        put("Emission Color", emission)
        put("Emission Strength", estrength)
    return m

def logo_material(path):
    m = bpy.data.materials.get("LogoMat")
    if m is None:
        m = bpy.data.materials.new("LogoMat")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    bsdf.inputs["Roughness"].default_value = 0.55
    m.blend_method = 'BLEND'
    return m

# ----------------------------------------------------------------------------
# Hull math — rings along Y, theta measured from +Z (top) toward +X
# ----------------------------------------------------------------------------

CTRL = [  # (y, radius) nose -> tail
    (3.62, 0.001),
    (3.45, 0.28),
    (3.20, 0.62),
    (2.90, 0.90),
    (2.50, 1.10),
    (2.00, 1.24),
    (1.40, 1.34),
    (0.60, 1.40),
    (-0.40, 1.42),
    (-1.40, 1.34),
    (-2.20, 1.18),
    (-2.80, 1.00),
    (-3.10, 0.90),
]

def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t +
                  (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                  (-p0 + 3 * p1 - 3 * p2 + p3) * t3)

def cr_sample(pts, n):
    P = [pts[0]] + list(pts) + [pts[-1]]
    segs = len(pts) - 1
    out = []
    for i in range(n):
        T = i * segs / max(n - 1, 1)
        s = min(int(T), segs - 1)
        t = T - s
        p0, p1, p2, p3 = P[s], P[s + 1], P[s + 2], P[s + 3]
        y = _cr(p0[0], p1[0], p2[0], p3[0], t)
        r = _cr(p0[1], p1[1], p2[1], p3[1], t)
        out.append((y, max(r, 0.0008)))
    return out

RINGS = cr_sample(CTRL, 110)          # nose (+Y) -> tail (-Y)
ASC = sorted(RINGS)
_AYS = [p[0] for p in ASC]
_ARS = [p[1] for p in ASC]

def radius_at(y):
    if y >= _AYS[-1]:
        return _ARS[-1]
    if y <= _AYS[0]:
        return _ARS[0]
    i = bisect_left(_AYS, y)
    t = (y - _AYS[i - 1]) / (_AYS[i] - _AYS[i - 1])
    return _ARS[i - 1] + t * (_ARS[i] - _ARS[i - 1])

def _sstep(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3 - 2 * t)

def zc_at(y):
    return 0.03 - 0.08 * _sstep(2.0, 3.6, y)   # nose droops a touch

def hull_point(y, theta):
    r = radius_at(y)
    rx, rz, zc = r, r * 0.94, zc_at(y)
    return Vector((rx * math.sin(theta), y, zc + rz * math.cos(theta)))

def hull_normal(y, theta):
    r = max(radius_at(y), 1e-4)
    n = Vector((math.sin(theta) / r, 0.0, math.cos(theta) / (r * 0.94)))
    n.normalize()
    return n

# ----------------------------------------------------------------------------
# Mesh builders
# ----------------------------------------------------------------------------

def build_hull(mat):
    NSEG = 64
    verts, faces = [], []
    for (y, r) in RINGS:
        rx, rz, zc = r, r * 0.94, zc_at(y)
        for j in range(NSEG):
            th = 2 * math.pi * j / NSEG
            verts.append((rx * math.sin(th), y, zc + rz * math.cos(th)))
    nr = len(RINGS)
    for i in range(nr - 1):
        for j in range(NSEG):
            j2 = (j + 1) % NSEG
            a = i * NSEG + j
            b = (i + 1) * NSEG + j
            c = (i + 1) * NSEG + j2
            d = i * NSEG + j2
            faces.append((a, b, c, d))
    # rear cap (covered by engine pod, keeps mesh closed)
    ci = len(verts)
    verts.append((0.0, RINGS[-1][0], zc_at(RINGS[-1][0])))
    base = (nr - 1) * NSEG
    for j in range(NSEG):
        j2 = (j + 1) % NSEG
        faces.append((base + j2, base + j, ci))
    return make_mesh_obj("Hull", verts, faces, mat)

def _grid_patch(name, y0, y1, th0, th1, offset, mat, ny, nt, wrap):
    verts, faces, idx = [], [], {}
    for i in range(ny + 1):
        y = y0 + (y1 - y0) * i / ny
        for j in range(nt + 1):
            jj = j % nt if wrap else j
            th = th0 + (th1 - th0) * jj / nt
            p = hull_point(y, th) + hull_normal(y, th) * offset
            idx[(i, j)] = len(verts)
            verts.append((p.x, p.y, p.z))
    for i in range(ny):
        for j in range(nt):
            a, b, c, d = idx[(i, j)], idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]
            faces.append((a, b, c, d))
    return make_mesh_obj(name, verts, faces, mat)

def build_band(name, y0, y1, z_lo, z_hi, offset, mat, ny=170, nt=170):
    """Full-circumference band hugging the hull where z in [z_lo, z_hi]."""
    verts, faces, idx = [], [], {}
    for i in range(ny + 1):
        y = y0 + (y1 - y0) * i / ny
        for j in range(nt + 1):
            th = 2 * math.pi * (j % nt) / nt
            p = hull_point(y, th)
            inside = (z_lo <= p.z <= z_hi)
            idx[(i, j)] = (len(verts), inside)
            q = p + hull_normal(y, th) * offset
            verts.append((q.x, q.y, q.z))
    for i in range(ny):
        for j in range(nt):
            (a, ia), (b, ib), (c, ic), (d, idd) = (
                idx[(i, j)], idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)])
            if ia and ib and ic and idd:
                faces.append((a, b, c, d))
    return make_mesh_obj(name, verts, faces, mat)

def extrude_polygon(name, pts, axis, lo, hi, mat):
    """Extrude a 2D polygon (u,v). pts should be CCW seen from +axis; auto-fixed."""
    area = 0.0
    for i in range(len(pts)):
        u1, v1 = pts[i]
        u2, v2 = pts[(i + 1) % len(pts)]
        area += u1 * v2 - u2 * v1
    if area < 0:
        pts = pts[::-1]
    def P3(u, v, w):
        return (w, u, v) if axis == 'X' else ((u, w, v) if axis == 'Y' else (u, v, w))
    n = len(pts)
    verts = [P3(u, v, lo) for (u, v) in pts] + [P3(u, v, hi) for (u, v) in pts]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        i2 = (i + 1) % n
        faces.append((i, i2, n + i2, n + i))
    return make_mesh_obj(name, verts, faces, mat, do_smooth=False)

def oriented_box(name, size, pos, normal, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=pos)
    obj = own(bpy.context.active_object)
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    obj.rotation_euler = normal.to_track_quat('Z', 'Y').to_euler()
    assign_mat(obj, mat)
    return obj

def place_on_hull(obj, y, theta, dist):
    p = hull_point(y, theta)
    n = hull_normal(y, theta)
    obj.location = p + n * dist
    obj.rotation_euler = n.to_track_quat('Z', 'Y').to_euler()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# Logo decal texture (generated by gen_logo.py with system python/Pillow)
# ----------------------------------------------------------------------------

# Build
# ----------------------------------------------------------------------------

def build():
    global COLL
    COLL = get_collection()
    clear_scene()
    COLL = get_collection()

    M = {}
    M["hull"] = principled("HullTeal", (0.055, 0.50, 0.43, 1.0), metallic=0.25, rough=0.42)
    M["dark"] = principled("DarkTeal", (0.030, 0.33, 0.29, 1.0), metallic=0.2, rough=0.5)
    M["red"] = principled("StripeRed", (0.60, 0.085, 0.065, 1.0), rough=0.5)
    M["cream"] = principled("Cream", (0.90, 0.86, 0.76, 1.0), rough=0.6)
    M["glass"] = principled("Glass", (0.36, 0.53, 0.60, 1.0), metallic=0.1, rough=0.15)
    M["dglass"] = principled("DarkGlass", (0.07, 0.12, 0.16, 1.0), rough=0.15)
    M["glow"] = principled("ThrusterGlow", (0.25, 0.22, 0.35, 1.0),
                           emission=(0.70, 0.66, 1.0), estrength=7.0)
    M["tipglow"] = principled("TipGlow", (0.3, 0.05, 0.05, 1.0),
                              emission=(1.0, 0.15, 0.12), estrength=3.0)
    M["metal"] = principled("MetalGray", (0.42, 0.43, 0.45, 1.0), metallic=0.65, rough=0.45)
    M["dmmetal"] = principled("DarkMetal", (0.10, 0.10, 0.12, 1.0), metallic=0.4, rough=0.6)

    # --- hull ---
    build_hull(M["hull"])
    print("hull done")

    # --- red cheatline stripe + cream spine trim + tail-base trim ---
    build_band("Stripe", -2.70, 3.30, -0.02, 0.30, 0.015, M["red"], ny=320, nt=180)
    build_band("SpineTrim", -2.95, 0.20, 1.16, 1.34, 0.015, M["cream"], ny=220)
    build_band("TailBaseTrim", -3.05, -1.10, 0.70, 1.02, 0.015, M["cream"])
    print("bands done")

    # --- rivets along spine trim ---
    for k, y in enumerate([-2.75 + i * 0.16 for i in range(19)]):
        if radius_at(y) * 0.94 + zc_at(y) < 1.18:
            continue
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, segments=8,
                                             ring_count=6, location=(0, 0, 0))
        rv = own(bpy.context.active_object)
        rv.name = f"Rivet_{k:02d}"
        place_on_hull(rv, y, 0.0, 0.030)
        assign_mat(rv, M["dmmetal"])
    print("rivets done")

    # --- cockpit: dark frame patch, glass patch, mullions ---
    _grid_patch("CockpitFrame", 1.86, 3.10, -0.70, 0.70, 0.012, M["dark"], 26, 30, False)
    _grid_patch("CockpitGlass", 1.94, 3.03, -0.60, 0.60, 0.022, M["glass"], 26, 30, False)
    for (t0, t1) in [(-0.035, 0.035), (0.26, 0.33), (-0.33, -0.26)]:
        _grid_patch("Mullion", 1.97, 3.00, t0, t1, 0.028, M["dark"], 20, 4, False)
    print("cockpit done")

    # --- portholes ---
    for side in (1, -1):
        for k, y in enumerate([0.15, 0.70, 1.25, 1.80]):
            th = side * 1.02
            bpy.ops.mesh.primitive_torus_add(major_radius=0.145, minor_radius=0.042,
                                             major_segments=20, minor_segments=10,
                                             location=(0, 0, 0))
            ring = own(bpy.context.active_object)
            ring.name = f"PortholeRing_{side}_{k}"
            place_on_hull(ring, y, th, 0.008)
            assign_mat(ring, M["cream"])
            bpy.ops.mesh.primitive_cylinder_add(radius=0.132, depth=0.02, vertices=24,
                                              location=(0, 0, 0))
            disc = own(bpy.context.active_object)
            disc.name = f"PortholeGlass_{side}_{k}"
            place_on_hull(disc, y, th, 0.004)
            assign_mat(disc, M["dglass"])
    print("portholes done")

    # --- tail fin + logos ---
    fin_pts = [(-1.25, 0.75), (-4.00, 2.62), (-3.80, 2.50), (-2.95, 0.80)]
    extrude_polygon("TailFin", fin_pts, 'X', -0.07, 0.07, M["dark"])
    logo_path = os.path.join(OUT, "planet_express_logo.png")
    assert os.path.exists(logo_path), f"missing logo texture: {logo_path} (run gen_logo.py first)"
    lm = logo_material(logo_path)
    for sgn, nm in ((1, "Logo_R"), (-1, "Logo_L")):
        bpy.ops.mesh.primitive_plane_add(size=0.95, location=(sgn * 0.078, -2.97, 1.62))
        lp = own(bpy.context.active_object)
        lp.name = nm
        lp.rotation_euler = (0, sgn * math.pi / 2, 0)
        assign_mat(lp, lm)
    print("fin+logo done")

    # --- side strakes + tip lights ---
    for sgn in (1, -1):
        pts = [(sgn * 0.75, -1.55), (sgn * 2.75, -3.15), (sgn * 0.85, -2.95)]
        extrude_polygon(f"Strake_{sgn}", pts, 'Z', -0.36, -0.26, M["dark"])
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, segments=10, ring_count=8,
                                             location=(sgn * 2.72, -3.12, -0.31))
        tip = own(bpy.context.active_object)
        tip.name = f"StrakeTip_{sgn}"
        assign_mat(tip, M["tipglow"])
    print("strakes done")

    # --- rear engine pod + thruster cluster ---
    pod_rings = [(-3.02, 1.00), (-3.30, 0.965), (-3.58, 0.90)]
    pv, pf = [], []
    NSEG = 48
    for ri, (y, r) in enumerate(pod_rings):
        for j in range(NSEG):
            th = 2 * math.pi * j / NSEG
            pv.append((r * math.sin(th), y, r * math.cos(th)))
    for i in range(len(pod_rings) - 1):
        for j in range(NSEG):
            j2 = (j + 1) % NSEG
            pf.append((i * NSEG + j, (i + 1) * NSEG + j,
                       (i + 1) * NSEG + j2, i * NSEG + j2))
    make_mesh_obj("EnginePod", pv, pf, M["cream"])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.88, depth=0.04, vertices=48,
                                        location=(0, -3.585, 0),
                                        rotation=(math.pi / 2, 0, 0))
    disc = own(bpy.context.active_object)
    disc.name = "EngineFace"
    assign_mat(disc, M["dmmetal"])
    cell_pos = [(0.0, 0.0)]
    for ring_i, rr in enumerate((0.27, 0.54)):
        cnt = 6 if ring_i == 0 else 12
        for k in range(cnt):
            a = 2 * math.pi * k / cnt + (math.pi / cnt if ring_i else 0)
            cell_pos.append((rr * math.cos(a), rr * math.sin(a)))
    for k, (cx, cz) in enumerate(cell_pos):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.115, depth=0.14, vertices=20,
                                            location=(cx, -3.62, cz),
                                            rotation=(math.pi / 2, 0, 0))
        cell = own(bpy.context.active_object)
        cell.name = f"Thruster_{k:02d}"
        assign_mat(cell, M["glow"])
    bpy.ops.mesh.primitive_torus_add(major_radius=0.93, minor_radius=0.07,
                                     major_segments=40, minor_segments=12,
                                     location=(0, -3.52, 0),
                                     rotation=(math.pi / 2, 0, 0))
    rim = own(bpy.context.active_object)
    rim.name = "EngineRim"
    assign_mat(rim, M["cream"])
    print("engine done")

    # --- roof dome, periscope, antenna ---
    bpy.ops.mesh.primitive_cylinder_add(radius=0.30, depth=0.14, vertices=32,
                                        location=(0, 1.05, 1.34))
    own(bpy.context.active_object).name = "DomeBase"
    bpy.context.active_object.data.materials.append(M["hull"])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.12, vertices=32,
                                        location=(0, 1.05, 1.45))
    own(bpy.context.active_object).name = "DomeMid"
    bpy.context.active_object.data.materials.append(M["dark"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, segments=20, ring_count=12,
                                         location=(0, 1.05, 1.52))
    dome = own(bpy.context.active_object)
    dome.name = "DomeGlass"
    dome.scale = (1, 1, 0.72)
    assign_mat(dome, M["glass"])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.55, vertices=16,
                                        location=(0, 0.80, 1.62),
                                        rotation=(0.6, 0, 0))
    scope = own(bpy.context.active_object)
    scope.name = "Periscope"
    assign_mat(scope, M["dmmetal"])
    bpy.ops.mesh.primitive_cube_add(size=0.13, location=(0, 0.645, 1.83))
    eye = own(bpy.context.active_object)
    eye.name = "PeriscopeEye"
    eye.rotation_euler = (0.6, 0, 0)
    assign_mat(eye, M["dmmetal"])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.75, vertices=10,
                                        location=(0, 1.30, 1.60))
    ant = own(bpy.context.active_object)
    ant.name = "Antenna"
    assign_mat(ant, M["dmmetal"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, segments=10, ring_count=8,
                                         location=(0, 1.30, 1.99))
    aball = own(bpy.context.active_object)
    aball.name = "AntennaTip"
    assign_mat(aball, M["tipglow"])
    print("dome done")

    # --- landing gear ---
    for sgn in (1, -1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.65, vertices=14,
                                            location=(sgn * 0.80, -0.30, -1.475))
        leg = own(bpy.context.active_object)
        leg.name = f"MainLeg_{sgn}"
        assign_mat(leg, M["metal"])
        bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.10, vertices=20,
                                            location=(sgn * 0.80, -0.30, -1.85))
        foot = own(bpy.context.active_object)
        foot.name = f"MainFoot_{sgn}"
        assign_mat(foot, M["metal"])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.65, vertices=14,
                                        location=(0, 2.35, -1.22))
    nleg = own(bpy.context.active_object)
    nleg.name = "NoseLeg"
    assign_mat(nleg, M["metal"])
    blade = oriented_box("NoseBlade", (0.14, 1.15, 0.07), (0, 2.80, -1.60),
                         Vector((0, -0.34, 0.94)), M["dmmetal"])
    del blade
    tipb = oriented_box("NoseBladeTip", (0.14, 0.34, 0.07), (0, 3.28, -1.82),
                        Vector((0, -0.83, 0.56)), M["cream"])
    del tipb
    print("gear done")

    # --- side vents + hatch ---
    for sgn in (1, -1):
        y = -2.15
        th = sgn * 1.016
        p = hull_point(y, th)
        n = hull_normal(y, th)
        oriented_box(f"VentPlate_{sgn}", (0.50, 0.55, 0.035),
                     p + n * 0.012, n, M["cream"])
        for k in range(5):
            zk = 0.62 - 0.16 + k * 0.08
            thk = sgn * math.acos(max(min((zk - zc_at(y)) / (radius_at(y) * 0.94), 1), -1))
            pk = hull_point(y, thk)
            nk = hull_normal(y, thk)
            oriented_box(f"VentSlat_{sgn}_{k}", (0.44, 0.055, 0.03),
                         pk + nk * 0.035, nk, M["dmmetal"])
        yh = 0.55
        thh = sgn * 1.15
        ph = hull_point(yh, thh)
        nh = hull_normal(yh, thh)
        oriented_box(f"Hatch_{sgn}", (0.30, 0.42, 0.035), ph + nh * 0.012, nh, M["cream"])
    print("details done")

    bpy.context.view_layer.update()
    print("BUILD COMPLETE:", len(COLL.objects), "objects")

# ----------------------------------------------------------------------------
# Studio scene + render
# ----------------------------------------------------------------------------

def studio():
    sc = bpy.context.scene
    w = bpy.data.worlds["World"]
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.72, 0.75, 0.79, 1.0)
    bg.inputs["Strength"].default_value = 1.0

    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.98))
    g = own(bpy.context.active_object)
    g.name = "Ground"
    gm = principled("GroundMat", (0.62, 0.64, 0.66, 1.0), rough=0.9)
    assign_mat(g, gm)

    def aim(obj, target):
        d = Vector(target) - obj.location
        obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

    bpy.ops.object.camera_add(location=(8.2, 8.8, 3.6))
    cam = own(bpy.context.active_object)
    cam.name = "Camera"
    aim(cam, (0, 0.0, 0.3))
    cam.data.lens = 50
    sc.camera = cam

    bpy.ops.object.light_add(type='SUN', location=(5, -6, 9))
    key = own(bpy.context.active_object)
    key.data.energy = 4.0
    aim(key, (0, 0, 0))
    bpy.ops.object.light_add(type='AREA', location=(-6, 4, 5))
    fill = own(bpy.context.active_object)
    fill.data.energy = 700
    fill.data.size = 6
    aim(fill, (0, 0, 0))
    bpy.ops.object.light_add(type='SUN', location=(-2, 7, 6))
    rim = own(bpy.context.active_object)
    rim.data.energy = 1.4
    aim(rim, (0, 0, 0))

    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    try:
        sc.eevee.taa_render_samples = 36
    except AttributeError:
        pass
    sc.render.resolution_x = 1280
    sc.render.resolution_y = 720
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.filepath = os.path.join(OUT, "planet_express_preview.png")
    print("rendering preview...")
    bpy.ops.render.render(write_still=True)
    print("preview written")

def main():
    build()
    # save the model first so a killed render can't take it with it
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "planet_express.blend"))
    print("blend saved")
    studio()
    print("ALL DONE")

main()
