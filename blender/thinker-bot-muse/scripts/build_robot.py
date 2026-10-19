"""Build the Thinker robot (Blender 4.x, headless).
Run: blender -b --python build_robot.py
Outputs: robot.blend, robot.glb, hero.png, front.png, head.png in OUT dir.
"""
import bpy
import math
import os
from mathutils import Vector as V

OUT = "/home/hatch/workspace/blender-robot"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for _coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
    for _x in list(_coll):
        _coll.remove(_x)

# ---------------------------------------------------------------- materials
def principled(name, base, metallic, rough, emission=None, estrength=0.0,
               spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Specular IOR Level"].default_value = spec
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = estrength
    return m

mat_armor  = principled("Armor",   (0.10, 0.16, 0.17), 1.0, 0.38)
mat_armor_lt = principled("ArmorLight", (0.17, 0.25, 0.26), 0.9, 0.42)
mat_silver = principled("Silver",  (0.72, 0.75, 0.78), 1.0, 0.28)
mat_red    = principled("RedGlow", (0.02, 0.00, 0.00), 0.0, 0.50,
                        emission=(1.0, 0.0, 0.0), estrength=1.2, spec=0.0)
mat_inner  = principled("InnerRed",(0.30, 0.015, 0.02), 0.2, 0.65)
mat_brass  = principled("Brass",   (0.50, 0.38, 0.20), 1.0, 0.40)
mat_white  = principled("White",   (0.92, 0.92, 0.92), 0.1, 0.40,
                        emission=(0.9, 0.9, 0.9), estrength=0.6)
mat_dark   = principled("Dark",    (0.03, 0.03, 0.035), 0.6, 0.50)
mat_stone  = principled("Stone",   (0.09, 0.09, 0.10), 0.0, 0.95)

# ---------------------------------------------------------------- helpers
def M(obj, mat):
    if mat is not None and obj.data is not None and hasattr(obj.data, "materials"):
        obj.data.materials.append(mat)
    return obj

def ball(p, r, mat=None, name="ball", s=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12,
                                        radius=r, location=p)
    o = bpy.context.active_object
    o.name = name
    o.scale = s
    return M(o, mat)

def limb(p1, p2, r1, r2=None, mat=None, name="limb", verts=32, caps=True):
    """Tapered capsule from p1 to p2 (caps=False leaves flat capped ends)."""
    p1, p2 = V(p1), V(p2)
    d = p2 - p1
    L = d.length
    r2 = r1 if r2 is None else r2
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2,
                                    depth=L)
    o = bpy.context.active_object
    o.name = name
    o.location = (p1 + p2) / 2
    o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    M(o, mat)
    if caps:
        ball(p1, r1, mat, name + "_a")
        ball(p2, r2, mat, name + "_b")
    return o

def box(p, dims, mat=None, name="box", rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=p, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = dims
    if bevel > 0:
        md = o.modifiers.new("Bevel", 'BEVEL')
        md.width = bevel
        md.segments = 2
        md.limit_method = 'ANGLE'
    return M(o, mat)

def torus(p, R, r, mat=None, name="torus", rot=(0, 0, 0),
          major=48, minor=16):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     major_segments=major, minor_segments=minor,
                                     location=p, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    return M(o, mat)

def joint_ring(p, axis, R, r, mat, name):
    """Smooth joint ring encircling a limb; axis = limb direction at the joint."""
    o = torus(p, R, r, mat, name)
    q = V((0, 0, 1)).rotation_difference(V(axis).normalized())
    o.rotation_euler = q.to_euler()
    return o

def pivot(name, p, rot=(0, 0, 0)):
    bpy.ops.object.empty_add(location=p, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    return o

def at_parent(obj, piv, loc, rot=(0, 0, 0)):
    obj.parent = piv
    obj.location = loc
    obj.rotation_euler = rot
    return obj

# ---------------------------------------------------------------- pedestal
# Stone block the robot sits on (hero reference: concrete pedestal)
box((0, 0.05, 0.275), (0.95, 0.75, 0.55), mat_stone, "Pedestal", bevel=0.015)
box((0, 0.05, 0.045), (1.05, 0.85, 0.09), mat_stone, "PedestalBase", bevel=0.01)

# ---------------------------------------------------------------- torso
LEAN = -0.15  # torso leans forward (+Y)

# pelvis + abdomen (deep red inner body shows between armor)
box((0, 0.03, 0.70), (0.40, 0.30, 0.22), mat_armor, "Pelvis", bevel=0.05)
limb((0, 0.04, 0.78), (0, 0.08, 0.96), 0.150, 0.135, mat_inner, "Abdomen")
ball((0.17, 0.02, 0.64), 0.100, mat_inner, "HipJoint_R")
ball((-0.17, 0.02, 0.64), 0.100, mat_inner, "HipJoint_L")

# ---- tapered chest on its own pivot (follows the forward lean) ----
chest_piv = pivot("ChestPivot", (0, 0.10, 1.11), rot=(LEAN, 0, 0))

def chest_r(zl):
    """Cone surface radius at local height zl (0.20 bottom -> 0.30 top)."""
    return 0.25 + 0.2381 * zl

# main torso: tapered cone, wider than deep — sculpted, not crate-like
bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.20, radius2=0.30,
                                depth=0.42, location=(0, 0, 0))
torso = bpy.context.active_object
torso.name = "Chest"
torso.scale = (1.25, 1.0, 1.0)
md = torso.modifiers.new("Bevel", 'BEVEL')
md.width = 0.04
md.segments = 2
md.limit_method = 'ANGLE'
M(torso, mat_armor)
at_parent(torso, chest_piv, (0, 0, 0))

# brass trim strip across the mid chest
at_parent(box((0, 0, 0), (0.30, 0.014, 0.05), mat_brass, "ChestTrim"),
          chest_piv, (0, chest_r(-0.09) + 0.002, -0.09))

# sternum strip: dark backing + 5 armor plates, hugging the cone's front
at_parent(box((0, 0, 0), (0.100, 0.030, 0.40), mat_dark, "SternumBack",
              bevel=0.006),
          chest_piv, (0, chest_r(0.0) - 0.004, 0.0))
for i in range(5):
    zl = 0.14 - i * 0.07
    at_parent(box((0, 0, 0), (0.095, 0.030, 0.058), mat_armor_lt,
                  f"SternumSeg_{i}", bevel=0.008),
              chest_piv, (0, chest_r(zl) + 0.004, zl))

# white "6" on the sternum. Orientation verified empirically (Blender 4.5):
# Blender XYZ Euler composes as Rz*Ry*Rx, and (pi/2, 0, pi) maps the text
# face to +Y, text-up to +Z and text-right to -X (screen-right for a front
# viewer), so the glyph reads as "6". The chest pivot adds the lean.
bpy.ops.object.text_add(location=(0, 0, 0))
six = bpy.context.active_object
six.name = "SixMark"
six.data.body = "6"
six.data.align_x = 'CENTER'
six.data.align_y = 'CENTER'
six.data.extrude = 0.008
six.scale = (0.095, 0.095, 0.095)
M(six, mat_white)
at_parent(six, chest_piv, (0, chest_r(0.08) + 0.022, 0.08),
          rot=(math.pi / 2, 0, math.pi))

# red glow accents on the tapered torso sides
for side, sgn in (("R", 1), ("L", -1)):
    at_parent(ball((0, 0, 0), 1.0, mat_red, f"TorsoGlow_{side}",
                   s=(0.035, 0.025, 0.075)),
              chest_piv, (sgn * 1.25 * chest_r(0.05), 0.02, 0.05))

# ---------------------------------------------------------------- neck (segmented rings over red core)
limb((0, 0.17, 1.28), (0, 0.20, 1.44), 0.060, 0.055, mat_inner, "NeckCore")
for i, z in enumerate((1.305, 1.350, 1.395)):
    torus((0, 0.175 + i * 0.008, z), 0.082, 0.020, mat_armor,
          f"NeckRing_{i}")

# ---------------------------------------------------------------- head (pivot so we can bow/turn it)
head_piv = pivot("HeadPivot", (0, 0.22, 1.53), rot=(-0.18, 0, 0.10))

# dark helmet shell (elongated)
at_parent(ball((0, 0, 0), 1.0, mat_armor, "Helmet", s=(0.155, 0.175, 0.205)),
          head_piv, (0, 0, 0))
# silver faceplate (slightly smaller, pushed forward -> dark rim shows)
at_parent(ball((0, 0, 0), 1.0, mat_silver, "Faceplate", s=(0.132, 0.152, 0.178)),
          head_piv, (0, 0.045, -0.012))
# pale crown stripe
at_parent(box((0, 0, 0), (0.055, 0.200, 0.020), mat_silver, "CrownStripe"),
          head_piv, (0, 0.012, 0.188))
# slanted angular red lenses: thin dark socket flush on the faceplate with a
# slimmer red lens set into it; inner corner dropped toward the nose
# (no brow band — not in the reference)
for side, sgn in (("R", 1), ("L", -1)):
    at_parent(box((0, 0, 0), (0.076, 0.012, 0.034), mat_dark,
                  f"EyeSocket_{side}", rot=(0, sgn * -0.45, 0), bevel=0.004),
              head_piv, (sgn * 0.060, 0.176, 0.016))
    at_parent(box((0, 0, 0), (0.060, 0.014, 0.022), mat_red,
                  f"EyeLens_{side}", rot=(0, sgn * -0.45, 0), bevel=0.004),
              head_piv, (sgn * 0.060, 0.181, 0.016))
# circular ear discs
for side, sgn in (("R", 1), ("L", -1)):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.042, depth=0.028,
                                        location=(0, 0, 0),
                                        rotation=(0, math.pi / 2, 0))
    ear = bpy.context.active_object
    ear.name = f"EarDisc_{side}"
    M(ear, mat_dark)
    at_parent(ear, head_piv, (sgn * 0.150, 0.008, 0.008))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.020, depth=0.034,
                                        location=(0, 0, 0),
                                        rotation=(0, math.pi / 2, 0))
    hub = bpy.context.active_object
    hub.name = f"EarHub_{side}"
    M(hub, mat_brass)
    at_parent(hub, head_piv, (sgn * 0.150, 0.008, 0.008))
# angular cheek/jaw lines (subtle)
for side, sgn in (("R", 1), ("L", -1)):
    at_parent(box((0, 0, 0), (0.010, 0.010, 0.085), mat_dark,
                  f"CheekLine_{side}", rot=(0.1, 0, sgn * -0.28)),
              head_piv, (sgn * 0.095, 0.150, -0.070))
# chin block
at_parent(box((0, 0, 0), (0.055, 0.030, 0.035), mat_dark, "ChinBlock"),
          head_piv, (0, 0.162, -0.128))

# ---------------------------------------------------------------- pauldrons (big layered shells sweeping down)
for side, sgn in (("R", 1), ("L", -1)):
    sx = sgn
    ball((sx * 0.40, 0.10, 1.26), 0.120, mat_inner, f"ShoulderJoint_{side}")
    # main shell
    ball((sx * 0.44, 0.10, 1.30), 1.0, mat_armor, f"PauldronMain_{side}",
         s=(0.200, 0.215, 0.170))
    # lower lame sweeping down-forward
    ball((sx * 0.47, 0.16, 1.16), 1.0, mat_armor, f"PauldronLame_{side}",
         s=(0.160, 0.180, 0.120))
    # brass rim on the shell edge
    torus((sx * 0.47, 0.13, 1.20), 0.150, 0.014, mat_brass,
          f"PauldronRim_{side}", rot=(0, math.pi / 2 - 0.25, 0))

# ---------------------------------------------------------------- arms
def build_arm(side, sgn, thinker):
    """thinker=True -> right arm: elbow on knee, hand to chin."""
    sx = sgn
    sh = (sx * 0.42, 0.10, 1.22)
    if thinker:
        el = (sx * 0.40, 0.38, 0.78)     # elbow near right knee
        wr = (sx * 0.09, 0.34, 1.22)     # wrist raised so fingers reach the chin
    else:
        el = (sx * 0.40, 0.28, 0.80)     # elbow low
        wr = (sx * 0.24, 0.50, 0.46)     # hand resting on left knee
    # upper arm + bicep guard
    limb(sh, el, 0.125, 0.110, mat_armor, f"UpperArm_{side}", caps=False)
    ball((sx * 0.44, 0.17, 1.08), 1.0, mat_armor, f"BicepGuard_{side}",
         s=(0.125, 0.125, 0.150))
    # red oval panel on outer upper arm
    ball((sx * 0.505, 0.20, 1.06), 1.0, mat_red, f"ArmGlow_{side}",
         s=(0.028, 0.060, 0.085))
    # smooth dark-red joint rings (no joint balls -> no torn-paper rims)
    joint_ring(el, V(wr) - V(el), 0.100, 0.030, mat_inner, f"ElbowRing_{side}")
    # forearm (tapered) + wrist
    limb(el, wr, 0.105, 0.080, mat_armor, f"Forearm_{side}", caps=False)
    joint_ring(wr, V(wr) - V(el), 0.075, 0.025, mat_inner, f"WristRing_{side}")
    return wr

def build_hand(side, sgn, wrist, thinker):
    """Articulated hand; thinker -> fingers curled up to chin."""
    wx, wy, wz = wrist
    sx = sgn
    if thinker:
        # palm tilted, fingers reaching up to touch the chin
        box((wx - sx * 0.03, wy - 0.02, wz + 0.07), (0.085, 0.095, 0.050),
            mat_armor, f"Palm_{side}", rot=(0.35, 0, sx * 0.15), bevel=0.015)
        for f in range(4):
            fx = wx - sx * 0.03 + (f - 1.5) * 0.024
            p0 = (fx, wy - 0.015, wz + 0.100)
            p1 = (fx - sx * 0.008, wy + 0.000, wz + 0.140)
            p2 = (fx - sx * 0.022, wy + 0.010, wz + 0.175)
            limb(p0, p1, 0.016, 0.014, mat_silver, f"Finger{side}_{f}a")
            limb(p1, p2, 0.014, 0.011, mat_silver, f"Finger{side}_{f}b")
        # thumb bracing the jaw
        limb((wx + sx * 0.045, wy - 0.02, wz + 0.05),
             (wx + sx * 0.060, wy + 0.03, wz + 0.12),
             0.017, 0.013, mat_silver, f"Thumb_{side}")
    else:
        # palm flat on knee, fingers draped down over the knee
        box((wx, wy + 0.02, wz), (0.090, 0.100, 0.050),
            mat_armor, f"Palm_{side}", rot=(-0.25, 0, 0), bevel=0.015)
        for f in range(4):
            fx = wx + (f - 1.5) * 0.024
            p0 = (fx, wy + 0.055, wz - 0.015)
            p1 = (fx, wy + 0.075, wz - 0.075)
            p2 = (fx, wy + 0.070, wz - 0.135)
            limb(p0, p1, 0.016, 0.014, mat_silver, f"Finger{side}_{f}a")
            limb(p1, p2, 0.014, 0.011, mat_silver, f"Finger{side}_{f}b")
        limb((wx + sx * 0.05, wy + 0.02, wz),
             (wx + sx * 0.075, wy + 0.06, wz - 0.05),
             0.017, 0.013, mat_silver, f"Thumb_{side}")

wrist_R = build_arm("R", 1, thinker=True)
wrist_L = build_arm("L", -1, thinker=False)
build_hand("R", 1, wrist_R, thinker=True)
build_hand("L", -1, wrist_L, thinker=False)

# ---------------------------------------------------------------- legs
def build_leg(side, sgn):
    sx = sgn
    hip = (sx * 0.17, 0.03, 0.64)
    knee = (sx * 0.20, 0.52, 0.40)
    ankle = (sx * 0.20, 0.44, 0.12)
    # thigh (bulky) + thigh guard shell
    limb(hip, knee, 0.140, 0.115, mat_armor, f"Thigh_{side}", caps=False)
    ball((sx * 0.19, 0.28, 0.55), 1.0, mat_armor, f"ThighGuard_{side}",
         s=(0.150, 0.190, 0.135))
    # smooth dark-red joint rings (no joint balls -> no torn-paper rims)
    joint_ring(knee, V(ankle) - V(knee), 0.105, 0.032, mat_inner,
               f"KneeRing_{side}")
    # shin (tapered)
    limb(knee, ankle, 0.115, 0.085, mat_armor, f"Shin_{side}", caps=False)
    # LARGE red oval panel on the front of the shin
    ball((sx * 0.20, 0.585, 0.27), 1.0, mat_red, f"ShinGlow_{side}",
         s=(0.075, 0.028, 0.110))
    joint_ring(ankle, V(ankle) - V(knee), 0.080, 0.026, mat_inner,
               f"AnkleRing_{side}")
    # foot: heel block + pointed toe
    box((sx * 0.20, 0.44, 0.060), (0.110, 0.130, 0.100), mat_armor,
        f"Heel_{side}", bevel=0.02)
    ball((sx * 0.20, 0.585, 0.048), 1.0, mat_armor, f"Toe_{side}",
         s=(0.058, 0.135, 0.048))

build_leg("R", 1)
build_leg("L", -1)

# ---------------------------------------------------------------- smooth shading (except pedestal)
for o in bpy.data.objects:
    if o.type == 'MESH' and not o.name.startswith("Pedestal"):
        for p in o.data.polygons:
            p.use_smooth = True

# ---------------------------------------------------------------- lights
def area_light(name, loc, energy, size, color=(1, 1, 1)):
    bpy.ops.object.light_add(type='AREA', location=loc)
    o = bpy.context.active_object
    o.name = name
    o.data.energy = energy
    o.data.size = size
    o.data.color = color
    return o

area_light("Key", (2.6, 2.8, 3.6), 900, 3.0, (1.0, 0.93, 0.85))
area_light("Fill", (-3.0, 2.2, 2.0), 320, 2.5, (0.75, 0.85, 1.0))
# small fill aimed at the face so the silver faceplate reads
bpy.ops.object.light_add(type='AREA', location=(0.9, 2.4, 1.78))
face_fill = bpy.context.active_object
face_fill.name = "FaceFill"
face_fill.data.energy = 170
face_fill.data.size = 1.2
face_fill.data.color = (1.0, 0.95, 0.90)
_d = V((0, 0.22, 1.45)) - V((0.9, 2.4, 1.78))
face_fill.rotation_euler = _d.to_track_quat('-Z', 'Y').to_euler()
bpy.ops.object.light_add(type='SPOT', location=(0.5, -4.5, 3.2))
rim = bpy.context.active_object
rim.name = "Rim"
rim.data.energy = 1400
rim.data.color = (1.0, 0.85, 0.7)
rim.data.spot_size = 0.7

# dark studio world
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.012, 0.012, 0.014, 1.0)
bg.inputs["Strength"].default_value = 1.0

# ---------------------------------------------------------------- cameras
def camera(name, loc, target, lens=50):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = name
    cam.data.lens = lens
    tgt = bpy.data.objects.new(name + "_tgt", None)
    bpy.context.collection.objects.link(tgt)
    tgt.location = target
    con = cam.constraints.new('TRACK_TO')
    con.target = tgt
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    return cam

cam_hero = camera("CamHero", (2.05, 3.35, 1.55), (0, 0.10, 0.88), lens=50)
cam_front = camera("CamFront", (0, 4.6, 1.00), (0, 0.10, 0.85), lens=55)
cam_head = camera("CamHead", (0.58, 1.80, 1.64), (0, 0.24, 1.47), lens=70)

# ---------------------------------------------------------------- render settings
# Cycles on CPU (EEVEE needs system EGL libs that don't persist on this VM)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 80
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.film_transparent = False

# glow for the red emissives: compositor Glare (Fog Glow)
scene.use_nodes = True
nt = scene.node_tree
nt.nodes.clear()
rl = nt.nodes.new('CompositorNodeRLayers')
glare = nt.nodes.new('CompositorNodeGlare')
glare.glare_type = 'FOG_GLOW'
glare.quality = 'HIGH'
glare.threshold = 1.0
glare.size = 3
comp = nt.nodes.new('CompositorNodeComposite')
nt.links.new(rl.outputs['Image'], glare.inputs['Image'])
nt.links.new(glare.outputs['Image'], comp.inputs['Image'])

def render(cam, fname):
    scene.camera = cam
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print("rendered", fname)

render(cam_hero, "hero.png")
render(cam_front, "front.png")
render(cam_head, "head.png")

# ---------------------------------------------------------------- save + export
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "robot.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "robot.glb"),
                          export_format='GLB',
                          export_materials='EXPORT')
print("DONE")
