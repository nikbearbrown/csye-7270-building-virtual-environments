#!/usr/bin/env python3
"""Procedural Ducati scrambler-custom build for Blender 4.2 (headless).
Run: blender --background --python scripts/build_ducati.py
Produces: ducati-scrambler-custom.blend, renders, then export .glb separately.
Coordinate system: X = bike forward (front wheel +X), Y = lateral (+Y = left
side of bike), Z = up. Units: meters. Exhaust on right side (-Y).
"""
import bpy, math, os

WORK = "/home/hatch/workspace/game-models/ducati-scrambler-custom-muse"
RENDERS = os.path.join(WORK, "renders")
os.makedirs(RENDERS, exist_ok=True)

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
import os as _os
scene.cycles.samples = int(_os.environ.get("CYCLES_SAMPLES", "96"))
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.render.resolution_x = 1400
scene.render.resolution_y = 1050
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.display.shading.light = 'STUDIO'
if 'World' in bpy.data.worlds:
    world = bpy.data.worlds['World']
else:
    world = bpy.data.worlds.new('World')
    scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.82, 0.82, 0.84, 1.0)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0

# ------------------------------------------------------------------ materials
def make_mat(name, base=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.5,
             clearcoat=0.0, emission=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = base
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = clearcoat
    if emission is not None:
        bsdf.inputs['Emission Color'].default_value = (*emission, 1.0)
        bsdf.inputs['Emission Strength'].default_value = 1.0
    return m

MAT = {
    'green_paint': make_mat('GreenPaint', (0.005, 0.062, 0.028, 1.0),
                            metallic=0.25, roughness=0.34, clearcoat=1.0),
    'leather':     make_mat('Leather', (0.070, 0.030, 0.012, 1.0),
                            metallic=0.0, roughness=0.75),
    'black_metal': make_mat('BlackMetal', (0.03, 0.03, 0.035, 1.0),
                            metallic=0.85, roughness=0.45),
    'chrome':      make_mat('Chrome', (0.95, 0.95, 0.97, 1.0),
                            metallic=1.0, roughness=0.12),
    'silver':      make_mat('Silver', (0.75, 0.76, 0.78, 1.0),
                            metallic=1.0, roughness=0.28),
    'gold':        make_mat('Gold', (0.85, 0.55, 0.16, 1.0),
                            metallic=1.0, roughness=0.30),
    'rubber':      make_mat('Rubber', (0.015, 0.015, 0.015, 1.0),
                            metallic=0.0, roughness=0.92),
    'white':       make_mat('White', (0.93, 0.93, 0.94, 1.0),
                            metallic=0.1, roughness=0.4),
    'red_lens':    make_mat('RedLens', (0.55, 0.02, 0.02, 1.0),
                            metallic=0.2, roughness=0.25, emission=(0.5, 0.02, 0.02)),
    'headlens':    make_mat('HeadLens', (0.92, 0.93, 0.90, 1.0),
                            metallic=0.1, roughness=0.12, emission=(0.75, 0.76, 0.70)),
    'dark_glass':  make_mat('DarkGlass', (0.05, 0.05, 0.06, 1.0),
                            metallic=0.4, roughness=0.15),
    'ground':      make_mat('Ground', (0.78, 0.78, 0.80, 1.0),
                            metallic=0.0, roughness=0.95),
}

def assign(obj, matname):
    obj.data.materials.clear()
    obj.data.materials.append(MAT[matname])

# ------------------------------------------------------------------ helpers
def tube(p1, p2, r, matname, name="tube", segs=12):
    """Cylinder between two 3D points."""
    v1, v2 = mathutils.Vector(p1), mathutils.Vector(p2)
    d = v2 - v1
    length = d.length
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=length,
                                       vertices=segs, location=(v1 + v2) / 2)
    o = bpy.context.active_object
    o.name = name
    # orient local Z along d
    z = mathutils.Vector((0, 0, 1))
    q = z.rotation_difference(d.normalized())
    o.rotation_euler = q.to_euler()
    assign(o, matname)
    return o

def box_at(loc, size, matname, name="box", bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0], size[1], size[2])
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        mod = o.modifiers.new("bev", 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        bpy.ops.object.modifier_apply(modifier=mod.name)
    assign(o, matname)
    return o

import mathutils

# ------------------------------------------------------------------ wheels
WHEEL_R = 0.32           # outer tire radius (640mm OD, matches reference)
RIM_R = 0.195            # rim radius
FRONT_X, REAR_X = 0.72, -0.72   # 1440mm wheelbase
AXLE_Z = 0.32

def make_wheel(x, front=True, name="wheel"):
    parts = []
    # tire carcass: torus (ring in XZ plane, axle along Y)
    bpy.ops.mesh.primitive_torus_add(major_radius=WHEEL_R - 0.062, minor_radius=0.062,
                                    major_segments=40, minor_segments=16,
                                    location=(x, 0, AXLE_Z), rotation=(math.pi / 2, 0, 0))
    tire = bpy.context.active_object
    tire.name = name + "_tire"
    assign(tire, 'rubber')
    parts.append(tire)
    # knobby tread blocks: 3 rows x 26 around
    knob_proto = None
    knobs = []
    for row, yoff in enumerate((-0.045, 0.0, 0.045)):
        for i in range(26):
            a = (i / 26) * 2 * math.pi + (row * 0.06)
            px = x + (WHEEL_R - 0.018) * math.cos(a)
            pz = AXLE_Z + (WHEEL_R - 0.018) * math.sin(a)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, yoff, pz))
            k = bpy.context.active_object
            k.scale = (0.055, 0.038, 0.030)
            k.rotation_euler = (0, -a, 0)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            knobs.append(k)
    bpy.ops.object.select_all(action='DESELECT')
    for k in knobs:
        k.select_set(True)
    bpy.context.view_layer.objects.active = knobs[0]
    bpy.ops.object.join()
    tread = bpy.context.active_object
    tread.name = name + "_tread"
    assign(tread, 'rubber')
    parts.append(tread)
    # rim (ring in XZ plane)
    bpy.ops.mesh.primitive_torus_add(major_radius=RIM_R, minor_radius=0.016,
                                    major_segments=32, minor_segments=10,
                                    location=(x, 0, AXLE_Z), rotation=(math.pi / 2, 0, 0))
    rim = bpy.context.active_object
    rim.name = name + "_rim"
    assign(rim, 'silver')
    parts.append(rim)
    # spokes: 20, slight tangential lace
    spokes = []
    for i in range(20):
        a = (i / 20) * 2 * math.pi
        side = 0.028 if i % 2 == 0 else -0.028
        p1 = (x + 0.030 * math.cos(a + 0.35), side, AXLE_Z + 0.030 * math.sin(a + 0.35))
        p2 = (x + (RIM_R - 0.01) * math.cos(a), side * 0.4, AXLE_Z + (RIM_R - 0.01) * math.sin(a))
        spokes.append(tube(p1, p2, 0.004, 'silver', name + f"_spoke{i}", segs=6))
    bpy.ops.object.select_all(action='DESELECT')
    for s in spokes:
        s.select_set(True)
    bpy.context.view_layer.objects.active = spokes[0]
    bpy.ops.object.join()
    sp = bpy.context.active_object
    sp.name = name + "_spokes"
    parts.append(sp)
    # hub (axle along Y)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.09, vertices=16,
                                      location=(x, 0, AXLE_Z), rotation=(math.pi / 2, 0, 0))
    hub = bpy.context.active_object
    hub.name = name + "_hub"
    assign(hub, 'black_metal')
    parts.append(hub)
    # brake disc
    disc_r = 0.155 if front else 0.11
    bpy.ops.mesh.primitive_cylinder_add(radius=disc_r, depth=0.012, vertices=36,
                                      location=(x, -0.055, AXLE_Z), rotation=(math.pi / 2, 0, 0))
    disc = bpy.context.active_object
    disc.name = name + "_disc"
    assign(disc, 'gold' if front else 'silver')
    # drilled holes (boolean)
    cutters = []
    for i in range(10):
        a = (i / 10) * 2 * math.pi
        cx = x + (disc_r * 0.62) * math.cos(a)
        cz = AXLE_Z + (disc_r * 0.62) * math.sin(a)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.011, depth=0.03, vertices=10,
                                          location=(cx, -0.055, cz), rotation=(math.pi / 2, 0, 0))
        cutters.append(bpy.context.active_object)
    bpy.ops.object.select_all(action='DESELECT')
    for c in cutters:
        c.select_set(True)
    bpy.context.view_layer.objects.active = cutters[0]
    bpy.ops.object.join()
    cutter = bpy.context.active_object
    bpy.ops.object.select_all(action='DESELECT')
    disc.select_set(True)
    bpy.context.view_layer.objects.active = disc
    mod = disc.modifiers.new("holes", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    parts.append(disc)
    return parts

front_wheel = make_wheel(FRONT_X, front=True, name="front")
rear_wheel = make_wheel(REAR_X, front=False, name="rear")

# ------------------------------------------------------------------ trellis frame
# nodes: (x, z); tubes run in pairs at y = +/-0.075, hugging the engine.
# Reference: thin ~25mm steel trellis, top rails run from the steering head
# back just under the tank's top edge, triangulated bays wrap the engine.
YF = 0.075
TR = 0.0125
N = {
    'steer_top':    (0.47, 0.90),
    'steer_bot':    (0.54, 0.74),
    'tank_mid':     (0.10, 0.845),
    'tank_rear':    (-0.14, 0.81),
    'seat_rear':    (-0.50, 0.795),
    'pivot':        (-0.33, 0.36),
    'eng_f_top':    (0.24, 0.56),
    'eng_f_bot':    (0.26, 0.26),
    'eng_r_top':    (-0.18, 0.55),
    'eng_r_bot':    (-0.22, 0.25),
}
def fnode(key, y):
    x, z = N[key]
    return (x, y, z)

frame_tubes = [
    # top run: steering head -> under tank -> seat
    ('steer_top', 'tank_mid'),
    ('tank_mid', 'tank_rear'),
    ('tank_rear', 'seat_rear'),
    # bottom run / engine cradle
    ('steer_bot', 'eng_f_top'),
    ('eng_f_top', 'eng_f_bot'),
    ('eng_f_bot', 'eng_r_bot'),
    ('eng_r_bot', 'pivot'),
    ('pivot', 'seat_rear'),
    # rear triangle
    ('tank_rear', 'pivot'),
    # triangulation bays around the engine
    ('steer_top', 'eng_f_top'),
    ('eng_f_top', 'tank_mid'),
    ('eng_f_top', 'eng_r_bot'),
    ('eng_r_top', 'tank_rear'),
    ('eng_r_top', 'eng_r_bot'),
    ('eng_r_top', 'pivot'),
    ('steer_bot', 'tank_mid'),
    ('tank_mid', 'eng_r_top'),
]
for i, (a, b) in enumerate(frame_tubes):
    for y in (YF, -YF):
        tube(fnode(a, y), fnode(b, y), TR, 'black_metal', f"frame_{i}")
# cross tubes
for key in ['steer_top', 'tank_rear', 'seat_rear', 'pivot', 'eng_f_bot']:
    x, z = N[key]
    tube((x, -YF, z), (x, YF, z), TR, 'black_metal', "frame_cross")
# swingarm: pivot -> rear axle
for y in (0.07, -0.07):
    tube((-0.33, y, 0.36), (REAR_X, y, AXLE_Z), 0.022, 'black_metal', "swingarm")
# rear shock: red coil-over, swingarm -> frame under the seat (as in reference)
red = make_mat('ShockRed', (0.45, 0.03, 0.02, 1.0), metallic=0.4, roughness=0.4)
MAT['shock_red'] = red
tube((-0.40, 0, 0.40), (-0.33, 0, 0.66), 0.016, 'black_metal', "shock_body")
for i in range(6):
    t = i / 5.0
    sx = -0.40 + t * 0.07
    sz = 0.40 + t * 0.26
    bpy.ops.mesh.primitive_torus_add(major_radius=0.028, minor_radius=0.007,
                                    major_segments=14, minor_segments=8,
                                    location=(sx, 0, sz),
                                    rotation=(0, math.radians(15), 0))
    assign(bpy.context.active_object, 'shock_red')

# ------------------------------------------------------------------ fuel tank
# Teardrop: wide/high at the front, tapering to the seat, sitting DOWN into
# the frame with a nearly flat top line. Reference tank spans from the
# steering head back to the seat nose.
# NOTE (Blender 4.2): transform_apply() bakes LOCATION too, so we never
# apply transforms on positioned parts. Shape in unit-sphere local coords,
# bake dimensions into vertices, then set location only.
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=40, ring_count=24)
tank = bpy.context.active_object
tank.name = "tank"
SX, SY, SZ = 0.42, 0.160, 0.115
mesh = tank.data
for v in mesh.vertices:
    x, y, z = v.co.x, v.co.y, v.co.z  # unit sphere: -1..1
    # nose: pinch width and dip slightly for x > 0.25
    if x > 0.25:
        t = (x - 0.25) / 0.75
        y *= (1.0 - 0.38 * t)
        z -= 0.30 * t
    # tail: narrow and tuck down under the seat nose for x < -0.30
    if x < -0.30:
        t = (-0.30 - x) / 0.70
        y *= (1.0 - 0.50 * t)
        z -= 0.65 * t
    # flat top line
    if z > 0.35:
        z = 0.35 + (z - 0.35) * 0.50
    # tuck underside into the frame
    if z < -0.48:
        z = -0.48 + (z + 0.48) * 0.35
    v.co = (x * SX, y * SY, z * SZ)
mesh.update()
tank.location = (0.10, 0, 0.80)
mod = tank.modifiers.new("smooth", 'SUBSURF')
mod.levels = 2
mod.render_levels = 2
assign(tank, 'green_paint')

# DUCATI decal: white-text planes shrinkwrapped onto the tank flanks.
# (v1 bug: planes were rotated 68 deg instead of 90, slicing into the tank.)
# Tank surface at decal height (z~0.85): y ~= +/-0.144 -> planes at +/-0.150.
decal_path = os.path.join(WORK, "textures", "ducati_decal.png")
img = bpy.data.images.load(decal_path)
img.pack()
dmat = bpy.data.materials.new("DecalMat")
dmat.use_nodes = True
nt = dmat.node_tree
nt.nodes.clear()
out = nt.nodes.new('ShaderNodeOutputMaterial')
bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
bsdf.inputs['Roughness'].default_value = 0.4
tex = nt.nodes.new('ShaderNodeTexImage')
tex.image = img
nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
nt.links.new(tex.outputs['Alpha'], bsdf.inputs['Alpha'])
nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
# Blender 4.2 EEVEE-Next transparency
try:
    dmat.surface_render_method = 'BLENDED'
except AttributeError:
    dmat.blend_method = 'BLEND'
for side, ypos in (("R", -0.150), ("L", 0.150)):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.10, ypos, 0.85))
    dec = bpy.context.active_object
    dec.name = f"tank_decal_{side}"
    # subdivide so shrinkwrap can conform to the tank curvature
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=11)
    bpy.ops.object.mode_set(mode='OBJECT')
    dec.scale = (0.36, 0.090, 1.0)  # 4:1 to match texture aspect
    # face exactly outward: plane normal +Z -> +/-Y
    dec.rotation_euler = (-math.pi / 2, 0, 0) if ypos > 0 else (math.pi / 2, 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    sw = dec.modifiers.new("wrap", 'SHRINKWRAP')
    sw.target = tank
    sw.wrap_method = 'PROJECT'
    sw.use_project_x = False
    sw.use_project_y = True
    sw.use_project_z = False
    sw.use_negative_direction = True
    sw.use_positive_direction = True
    sw.offset = 0.003
    dec.data.materials.clear()
    dec.data.materials.append(dmat)

# ------------------------------------------------------------------ seat (brown solo)
# Built in local coords (no transform_apply: 4.2 bakes location too).
# Nose tucks over the tank tail; slight tail kick.
bpy.ops.mesh.primitive_cube_add(size=1.0)
seat = bpy.context.active_object
seat.name = "seat"
sm = seat.data
for v in sm.vertices:
    x, y, z = v.co.x, v.co.y, v.co.z  # +-0.5
    if x > 0.30:          # nose taper (local +x)
        y *= 0.80
    if x < -0.30:         # tail kick
        z += (-0.30 - x) * 0.35
    v.co = (x * 0.48, y * 0.26, z * 0.10)
sm.update()
seat.location = (-0.36, 0, 0.80)
seat.rotation_euler = (0, -0.04, 0)  # now pivots around the seat itself
mod = seat.modifiers.new("bev", 'BEVEL')
mod.width = 0.035
mod.segments = 3
assign(seat, 'leather')

# ------------------------------------------------------------------ engine (L-twin)
# Crankcase: rounded mass filling the frame's lower bay
box_at((0.02, 0, 0.40), (0.44, 0.32, 0.32), 'black_metal', "engine_block", bevel=0.045)

def cylinder_with_fins(cx, cz, tilt_deg, name):
    """One cylinder barrel: tilted box core + stacked cooling fins + head."""
    tilt = math.radians(tilt_deg)  # from vertical, + = tilted forward
    # barrel core
    b = box_at((cx, 0, cz), (0.17, 0.17, 0.26), 'black_metal', name + "_barrel", bevel=0.015)
    b.rotation_euler = (0, -tilt, 0)
    # fin stack: 9 thin plates perpendicular to the barrel axis
    for i in range(9):
        t = (i - 4) / 4.0  # -1..1 along barrel
        # offset along the tilted axis
        ox = cx + math.sin(tilt) * t * 0.11
        oz = cz + math.cos(tilt) * t * 0.11
        f = box_at((ox, 0, oz), (0.23, 0.23, 0.011), 'black_metal', f"{name}_fin{i}")
        f.rotation_euler = (0, -tilt, 0)
    # head cover (slightly wider, top of barrel)
    hx = cx + math.sin(tilt) * 0.15
    hz = cz + math.cos(tilt) * 0.15
    h = box_at((hx, 0, hz), (0.20, 0.20, 0.07), 'black_metal', name + "_head", bevel=0.02)
    h.rotation_euler = (0, -tilt, 0)
    return (hx, hz)

# front cylinder: near-vertical, slight forward tilt; rear: laid back ~45 deg
fh = cylinder_with_fins(0.13, 0.60, 12, "cyl_front")
rh = cylinder_with_fins(-0.11, 0.58, -42, "cyl_rear")
# clutch cover (right side, round) + badge
bpy.ops.mesh.primitive_cylinder_add(radius=0.105, depth=0.035, vertices=28,
                                  location=(-0.04, -0.170, 0.38), rotation=(math.pi / 2, 0, 0))
cc = bpy.context.active_object
cc.name = "clutch_cover"
assign(cc, 'black_metal')
bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=0.038, vertices=20,
                                  location=(-0.04, -0.170, 0.38), rotation=(math.pi / 2, 0, 0))
assign(bpy.context.active_object, 'silver')
# left-side round cover
bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.030, vertices=24,
                                  location=(0.02, 0.168, 0.40), rotation=(math.pi / 2, 0, 0))
assign(bpy.context.active_object, 'black_metal')

# ------------------------------------------------------------------ exhaust (right side, high)
# Headers: one per cylinder, curving down into a collector under the engine
def header_pipe(start, mids, name):
    pts = [start] + mids
    bpy.ops.curve.primitive_bezier_curve_add(location=pts[0])
    ex = bpy.context.active_object
    ex.name = name
    spl = ex.data.splines[0]
    spl.bezier_points[0].co = mathutils.Vector(pts[0])
    spl.bezier_points[0].handle_left_type = spl.bezier_points[0].handle_right_type = 'VECTOR'
    spl.bezier_points.add(len(pts) - 1)
    for bp, p in zip(list(spl.bezier_points)[1:], pts[1:]):
        bp.co = mathutils.Vector(p)
        bp.handle_left_type = bp.handle_right_type = 'VECTOR'
    ex.data.bevel_depth = 0.016
    ex.data.bevel_resolution = 8
    assign(ex, 'silver')
    return ex

# front cylinder header: forward-down, sweep back under engine
header_pipe((0.16, -0.06, 0.52),
            [(0.24, -0.07, 0.38), (0.20, -0.085, 0.24), (0.05, -0.095, 0.19)],
            "header_front")
# rear cylinder header: down and forward into the collector
header_pipe((-0.13, -0.06, 0.50),
            [(-0.10, -0.075, 0.36), (-0.02, -0.090, 0.24), (0.05, -0.095, 0.19)],
            "header_rear")
# mid pipe: collector rising steeply at the rear to the muffler
ex_pts = [(0.05, -0.095, 0.19), (-0.10, -0.105, 0.24), (-0.22, -0.115, 0.36),
          (-0.30, -0.120, 0.50)]
bpy.ops.curve.primitive_bezier_curve_add(location=ex_pts[0])
ex = bpy.context.active_object
ex.name = "exhaust_mid"
spl = ex.data.splines[0]
spl.bezier_points[0].co = mathutils.Vector(ex_pts[0])
spl.bezier_points[0].handle_left_type = spl.bezier_points[0].handle_right_type = 'VECTOR'
spl.bezier_points.add(len(ex_pts) - 1)
for bp, p in zip(list(spl.bezier_points)[1:], ex_pts[1:]):
    bp.co = mathutils.Vector(p)
    bp.handle_left_type = bp.handle_right_type = 'VECTOR'
ex.data.bevel_depth = 0.019
ex.data.bevel_resolution = 8
assign(ex, 'silver')
# muffler: substantial tapered can, ~450mm long, ~115mm max diameter
p1 = mathutils.Vector((-0.28, -0.120, 0.52))
p2 = mathutils.Vector((-0.54, -0.120, 0.66))
mlen = (p2 - p1).length
bpy.ops.mesh.primitive_cone_add(radius1=0.058, radius2=0.050, depth=mlen,
                               vertices=28, location=(p1 + p2) / 2)
muf = bpy.context.active_object
muf.name = "muffler"
z = mathutils.Vector((0, 0, 1))
muf.rotation_euler = z.rotation_difference((p2 - p1).normalized()).to_euler()
assign(muf, 'silver')
# end cap: torus ring + dark outlet + rivet dots around the ring
cap_c = mathutils.Vector(p2)
maxis = (p2 - p1).normalized()
bpy.ops.mesh.primitive_torus_add(major_radius=0.048, minor_radius=0.008,
                                major_segments=24, minor_segments=10,
                                location=tuple(cap_c))
ring = bpy.context.active_object
ring.rotation_euler = z.rotation_difference(maxis).to_euler()
assign(ring, 'black_metal')
bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=0.012, vertices=20,
                                   location=tuple(cap_c))
tip = bpy.context.active_object
tip.rotation_euler = z.rotation_difference(maxis).to_euler()
assign(tip, 'black_metal')
_u = maxis.cross(mathutils.Vector((0, 1, 0))).normalized()
_v = maxis.cross(_u).normalized()
for i in range(6):
    a = (i / 6) * 2 * math.pi
    rp = cap_c + 0.048 * (math.cos(a) * _u + math.sin(a) * _v)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.006, segments=8, ring_count=6,
                                        location=tuple(rp))
    assign(bpy.context.active_object, 'black_metal')
# mounting bracket: muffler mid -> frame
tube((-0.41, -0.115, 0.59), (-0.38, -0.075, 0.63), 0.010, 'black_metal', "ex_bracket")

# ------------------------------------------------------------------ front end
# forks: axle -> steering head (chrome lower sliders, black uppers)
for y in (0.062, -0.062):
    tube((FRONT_X, y, AXLE_Z), (0.60, y, 0.62), 0.021, 'chrome', "fork_low")
    tube((0.60, y, 0.62), (0.52, y, 0.90), 0.017, 'black_metal', "fork_up")
# triple clamp
box_at((0.51, 0, 0.905), (0.06, 0.13, 0.035), 'black_metal', "triple")
# handlebar: wide flat-ish bar via curve
bpy.ops.curve.primitive_bezier_curve_add(location=(0.49, -0.34, 0.955))
hb = bpy.context.active_object
hb.name = "handlebar"
spl = hb.data.splines[0]
pts = [(-0.34, 0.955, -0.05), (-0.20, 0.958, -0.015), (0.0, 0.955, 0.0),
       (0.20, 0.958, -0.015), (0.34, 0.955, -0.05)]
# note: curve local coords (y lateral, z up, x pullback)
spl.bezier_points[0].co = mathutils.Vector((pts[0][2], pts[0][0], pts[0][1] - 0.955))
spl.bezier_points.add(len(pts) - 1)
for bp, (py, pz, px) in zip(list(spl.bezier_points)[1:], pts[1:]):
    bp.co = mathutils.Vector((px, py, pz - 0.955))
    bp.handle_left_type = bp.handle_right_type = 'AUTO'
spl.bezier_points[0].handle_left_type = spl.bezier_points[0].handle_right_type = 'AUTO'
hb.location = (0.49, 0, 0.955)
hb.data.bevel_depth = 0.014
hb.data.bevel_resolution = 6
assign(hb, 'black_metal')
# grips
for y in (0.335, -0.335):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.017, depth=0.13, vertices=12,
                                      location=(0.445, y, 0.955), rotation=(math.pi / 2, 0, 0.15))
    assign(bpy.context.active_object, 'rubber')
# mirrors: short stalks angled out
for y in (0.28, -0.28):
    tube((0.47, y, 0.965), (0.44, y * 1.35, 1.025), 0.006, 'black_metal', "mirror_stalk", segs=8)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, segments=12, ring_count=8,
                                       location=(0.44, y * 1.38, 1.03))
    m = bpy.context.active_object
    m.scale = (0.45, 1.0, 0.65)
    assign(m, 'black_metal')
# instrument: small round dial on the triple clamp
bpy.ops.mesh.primitive_cylinder_add(radius=0.032, depth=0.025, vertices=20,
                                  location=(0.51, 0, 0.935), rotation=(0, 0, 0))
assign(bpy.context.active_object, 'black_metal')
bpy.ops.mesh.primitive_cylinder_add(radius=0.027, depth=0.027, vertices=20,
                                  location=(0.51, 0, 0.936))
assign(bpy.context.active_object, 'dark_glass')
# front brake line: lever area -> down the fork to the caliper (thin bezier)
bpy.ops.curve.primitive_bezier_curve_add(location=(0.47, -0.30, 0.95))
bl = bpy.context.active_object
bl.name = "brake_line"
blpts = [(0.47, -0.30, 0.95), (0.55, -0.20, 0.80), (0.63, -0.10, 0.60),
         (0.70, -0.075, 0.42)]
spl = bl.data.splines[0]
spl.bezier_points[0].co = mathutils.Vector(blpts[0])
spl.bezier_points[0].handle_left_type = spl.bezier_points[0].handle_right_type = 'AUTO'
spl.bezier_points.add(len(blpts) - 1)
for bp, p in zip(list(spl.bezier_points)[1:], blpts[1:]):
    bp.co = mathutils.Vector(p)
    bp.handle_left_type = bp.handle_right_type = 'AUTO'
bl.data.bevel_depth = 0.004
bl.data.bevel_resolution = 4
assign(bl, 'rubber')

# ------------------------------------------------------------------ headlight + grille
# bucket (smaller, tighter)
bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.09, vertices=24,
                                  location=(0.665, 0, 0.865), rotation=(0, math.pi / 2, 0))
assign(bpy.context.active_object, 'black_metal')
# chrome rim ring (prominent)
bpy.ops.mesh.primitive_torus_add(major_radius=0.076, minor_radius=0.011,
                                major_segments=24, minor_segments=10,
                                location=(0.712, 0, 0.865), rotation=(0, math.pi / 2, 0))
assign(bpy.context.active_object, 'chrome')
# lens
bpy.ops.mesh.primitive_cylinder_add(radius=0.068, depth=0.012, vertices=24,
                                  location=(0.712, 0, 0.865), rotation=(0, math.pi / 2, 0))
assign(bpy.context.active_object, 'headlens')
# grille rings
for r in (0.080, 0.070):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.004,
                                    major_segments=24, minor_segments=8,
                                    location=(0.720, 0, 0.865), rotation=(0, math.pi / 2, 0))
    assign(bpy.context.active_object, 'black_metal')
# grille bars: 4 vertical + 3 horizontal
for i in range(4):
    yy = -0.051 + i * 0.034
    tube((0.722, yy, 0.865 - 0.053), (0.722, yy, 0.865 + 0.053), 0.003, 'black_metal', "grille_v", segs=6)
for i in range(3):
    zz = 0.865 - 0.034 + i * 0.034
    tube((0.722, -0.053, zz), (0.722, 0.053, zz), 0.003, 'black_metal', "grille_h", segs=6)
# headlight brackets
for y in (0.075, -0.075):
    tube((0.63, y, 0.83), (0.585, y * 0.9, 0.90), 0.010, 'black_metal', "hl_bracket")

# ------------------------------------------------------------------ fenders / tail / plate / chain
# front fender (white, hugging the tire): keep cylinder verts within +/-42 deg of top
bpy.ops.mesh.primitive_cylinder_add(radius=0.348, depth=0.13, vertices=32,
                                  location=(FRONT_X, 0, AXLE_Z), rotation=(math.pi / 2, 0, 0))
fen = bpy.context.active_object
fen.name = "front_fender"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
fm = fen.data
for v in fm.vertices:
    v.select = False  # clear the select-all from primitive_add
for v in fm.vertices:
    # angle from +Z axis in XZ plane (world coords, wheel center at FRONT_X, AXLE_Z)
    dx = v.co.x - FRONT_X
    dz = v.co.z - AXLE_Z
    ang = math.degrees(math.atan2(abs(dx), dz)) if dz > 0 else 90.0
    v.select = ang > 42.0  # mark outside-arc verts for deletion
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')
assign(fen, 'white')
mod = fen.modifiers.new("sol", 'SOLIDIFY')
mod.thickness = 0.004
# rear hugger (black, minimal): keep within +/-40 deg of top
bpy.ops.mesh.primitive_cylinder_add(radius=0.350, depth=0.16, vertices=32,
                                  location=(REAR_X, 0, AXLE_Z), rotation=(math.pi / 2, 0, 0))
rh = bpy.context.active_object
rh.name = "rear_hugger"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
rm = rh.data
for v in rm.vertices:
    v.select = False
for v in rm.vertices:
    dx = v.co.x - REAR_X
    dz = v.co.z - AXLE_Z
    ang = math.degrees(math.atan2(abs(dx), dz)) if dz > 0 else 90.0
    v.select = ang > 40.0
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')
assign(rh, 'black_metal')
mod = rh.modifiers.new("sol", 'SOLIDIFY')
mod.thickness = 0.004
# taillight
box_at((-0.70, 0, 0.70), (0.05, 0.10, 0.06), 'red_lens', "taillight", bevel=0.01)
# white round number plate (left side)
bpy.ops.mesh.primitive_cylinder_add(radius=0.105, depth=0.008, vertices=28,
                                  location=(-0.52, 0.155, 0.52), rotation=(math.pi / 2, 0, 0))
assign(bpy.context.active_object, 'white')
# chain (left side) + sprockets
bpy.ops.mesh.primitive_cylinder_add(radius=0.105, depth=0.014, vertices=24,
                                  location=(REAR_X, 0.085, AXLE_Z), rotation=(math.pi / 2, 0, 0))
assign(bpy.context.active_object, 'black_metal')
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.014, vertices=16,
                                  location=(-0.05, 0.085, 0.36), rotation=(math.pi / 2, 0, 0))
assign(bpy.context.active_object, 'black_metal')
box_at((-0.38, 0.085, 0.345), (0.68, 0.018, 0.030), 'black_metal', "chain_top")
box_at((-0.38, 0.085, 0.315), (0.68, 0.018, 0.030), 'black_metal', "chain_bot")
# foot pegs
for y in (0.17, -0.17):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.09, vertices=10,
                                      location=(-0.12, y, 0.30), rotation=(math.pi / 2, 0, 0))
    assign(bpy.context.active_object, 'rubber')
# kickstand
tube((-0.28, -0.09, 0.32), (-0.42, -0.20, 0.02), 0.012, 'black_metal', "kickstand")
# white belly pan under engine (subtle): keep lower bowl of a cylinder
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.14, vertices=24,
                                  location=(0.10, 0, 0.22), rotation=(math.pi / 2, 0, 0))
bp = bpy.context.active_object
bp.name = "belly_pan"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bisect(plane_co=(0.10, 0, 0.30), plane_no=(0, 0, -1),
                    clear_inner=True, clear_outer=False)
bpy.ops.object.mode_set(mode='OBJECT')
assign(bp, 'white')

# ------------------------------------------------------------------ ground + studio light
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
gnd = bpy.context.active_object
gnd.name = "ground"
assign(gnd, 'ground')

def area_light(name, loc, power, size=3.0, color=(1, 1, 1, 1)):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.active_object
    l.name = name
    l.data.energy = power
    l.data.size = size
    l.data.color = color[:3]
    return l

key = area_light("key", (3.5, -3.5, 4.0), 650, 3.5)
key.rotation_euler = (math.radians(55), 0, math.radians(45))
fill = area_light("fill", (-3.5, 3.0, 2.5), 280, 3.0)
fill.rotation_euler = (math.radians(60), 0, math.radians(-50))
rim = area_light("rim", (-4.0, -2.5, 3.0), 450, 2.5)
rim.rotation_euler = (math.radians(50), 0, math.radians(120))

# ------------------------------------------------------------------ cameras
def cam(name, loc, target=(0, 0, 0.55), lens=50):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.active_object
    c.name = name
    c.data.lens = lens
    # track to target
    con = c.constraints.new('TRACK_TO')
    emp = bpy.data.objects.new(name + "_tgt", None)
    bpy.context.collection.objects.link(emp)
    emp.location = target
    con.target = emp
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    return c

cams = {
    "right_side":  cam("Cam_RightSide", (0.05, -3.4, 0.72), lens=55),
    "front":       cam("Cam_Front", (3.4, 0, 0.75), lens=55),
    "rear":        cam("Cam_Rear", (-3.4, 0, 0.75), lens=55),
    "three_quarter": cam("Cam_3Q", (2.5, -2.3, 1.05), lens=50),
    "detail_tank": cam("Cam_Tank", (0.9, -1.15, 1.05), target=(0.10, 0, 0.82), lens=70),
    "detail_engine": cam("Cam_Engine", (0.55, -1.05, 0.50), target=(0.0, 0, 0.45), lens=70),
    "detail_frontwheel": cam("Cam_FrontWheel", (1.35, -1.05, 0.45), target=(0.71, 0, 0.33), lens=70),
    "detail_headlight": cam("Cam_Headlight", (1.45, -0.85, 1.00), target=(0.68, 0, 0.86), lens=70),
}

# ------------------------------------------------------------------ render selected views
# VIEWS env var: comma-separated subset (default: all). E.g. VIEWS=right_side,detail_tank
import os as _os2
_want = [v.strip() for v in _os2.environ.get("VIEWS", "").split(",") if v.strip()]
for vname, cobj in cams.items():
    if _want and vname not in _want:
        continue
    scene.camera = cobj
    scene.render.filepath = os.path.join(RENDERS, f"{vname}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", vname, flush=True)

# ------------------------------------------------------------------ save + stats
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(WORK, "ducati-scrambler-custom.blend"))
ntris = sum(len(m.loop_triangles) for o in bpy.data.objects
            for m in [o.data] if hasattr(m, 'loop_triangles') and o.type == 'MESH'
            for _ in [m.calc_loop_triangles()])
print("AUDIT objects:", len([o for o in bpy.data.objects if o.type == 'MESH']))
print("AUDIT triangles:", ntris)
print("AUDIT materials:", len(bpy.data.materials))
bb = [o.bound_box for o in bpy.data.objects if o.type == 'MESH' and o.name != 'ground']
import mathutils as _mu
mn = _mu.Vector((1e9, 1e9, 1e9)); mx = _mu.Vector((-1e9, -1e9, -1e9))
for o in [o for o in bpy.data.objects if o.type == 'MESH' and o.name != 'ground']:
    for c in o.bound_box:
        w = o.matrix_world @ _mu.Vector(c)
        mn = _mu.Vector(map(min, mn, w)); mx = _mu.Vector(map(max, mx, w))
print("AUDIT dims (x,y,z m):", tuple(round(v, 3) for v in (mx - mn)))

# ------------------------------------------------------------------ save .blend + export .glb
BLEND_PATH = os.path.join(WORK, "ducati-scrambler-custom.blend")
GLB_PATH = os.path.join(WORK, "ducati-scrambler-custom.glb")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print("saved", BLEND_PATH)
# glb export: include materials + packed images
bpy.ops.export_scene.gltf(filepath=GLB_PATH, export_format='GLB',
                          export_materials='EXPORT',
                          export_image_format='AUTO')
print("exported", GLB_PATH)
