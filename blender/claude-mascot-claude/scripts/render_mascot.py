# render_mascot.py - real Blender Workbench renders of claude_mascot.blend: an 8-angle turnaround, six orthographic views,
# a wireframe, and one rig POSE TEST per named animation (the 18 in ClaudeMascotScene.tsx), each posed by driving the rig's bones
# with the same maths as the 2D scene (ported below). No window.
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python render_mascot.py
import bpy, os, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "renders")
for sub in ("turnaround", "ortho", "poses"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "claude_mascot.blend"))
sc = bpy.context.scene
mesh = bpy.data.objects["ClaudeMascot"]
rig = bpy.data.objects["ClaudeMascotRig"]
U = 0.01
FPS = 24
CENTRE = Vector((0, 0, 0.43))

# ---------------------------------------------------------------- render setup (Workbench; flat colours stay true under Standard)
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = 1600, 1200
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'
sc.view_settings.exposure = 0.3        # studio lighting darkens the front face; +0.3 EV brings it to the canonical #dd775b
sh = sc.display.shading
sh.light = "STUDIO"; sh.studio_light = "paint.sl"
sh.color_type = 'MATERIAL'
sh.show_cavity = False
sh.show_object_outline = True
sh.object_outline_color = (0.16, 0.13, 0.10)
sh.show_specular_highlight = False
sh.show_shadows = True
sh.shadow_intensity = 0.35

# floor: a thin pale disc at z = 0 so planted feet and jump heights read
floor_mat = bpy.data.materials.new("Floor"); floor_mat.diffuse_color = (0.93, 0.91, 0.86, 1)
bpy.ops.mesh.primitive_cylinder_add(radius=1.3, depth=0.01, location=(0, 0, -0.005), vertices=64)
floor = bpy.context.active_object; floor.name = "Floor"; floor.data.materials.append(floor_mat)

cam = bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam"))
sc.collection.objects.link(cam); sc.camera = cam
tgt = bpy.data.objects.new("RenderTarget", None); sc.collection.objects.link(tgt); tgt.location = CENTRE
trk = cam.constraints.new('TRACK_TO'); trk.target = tgt; trk.track_axis = 'TRACK_NEGATIVE_Z'; trk.up_axis = 'UP_Y'


def persp(az_deg, el_deg, dist=3.4, lens=50):
    cam.data.type = 'PERSP'; cam.data.lens = lens
    az, el = math.radians(az_deg), math.radians(el_deg)
    cam.location = (CENTRE.x + dist * math.sin(az) * math.cos(el), CENTRE.y - dist * math.cos(az) * math.cos(el), CENTRE.z + dist * math.sin(el))


def ortho(direction, scale=1.6):
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = scale
    d = {"front": (0, -4, 0), "back": (0, 4, 0), "left": (-4, 0, 0), "right": (4, 0, 0), "top": (0, 0, 4), "bottom": (0, 0, -4)}[direction]
    cam.location = (CENTRE.x + d[0], CENTRE.y + d[1], CENTRE.z + d[2])
    # top/bottom views need a different up axis so the front of the mascot is at the bottom/top of the frame
    trk.up_axis = 'UP_Y'
    if direction in ("top", "bottom"):
        cam.location = (CENTRE.x + 0.0001, CENTRE.y + (0.0001 if direction == "top" else -0.0001) * 0 + 0.0, CENTRE.z + d[2])


def shot(path):
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered", os.path.relpath(path, HERE))


# ---------------------------------------------------------------- 1. turnaround, 8 angles
mesh.display_type = 'TEXTURED'
for az in range(0, 360, 45):
    persp(az, 12)
    shot(os.path.join(OUT, "turnaround", "az%03d.png" % az))

# ---------------------------------------------------------------- 2. orthographic views (no floor: the bottom view would otherwise see only the disc)
floor.hide_render = True
for d in ("front", "back", "left", "right"):
    ortho(d)
    shot(os.path.join(OUT, "ortho", d + ".png"))
# top/bottom: the tracker would roll about the view axis arbitrarily; render them with an explicit rotation instead
for d, rot in (("top", (0, 0, 0)), ("bottom", (math.pi, 0, 0))):
    trk.mute = True
    cam.rotation_euler = rot
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 1.6
    cam.location = (0, 0, CENTRE.z + (4 if d == "top" else -4))
    shot(os.path.join(OUT, "ortho", d + ".png"))
trk.mute = False
floor.hide_render = False

# ---------------------------------------------------------------- 3. wireframe (the 108 triangles' edges, front three-quarter)
persp(30, 18)
mesh.display_type = 'WIRE'
floor.hide_render = True
shot(os.path.join(OUT, "wireframe.png"))
mesh.display_type = 'TEXTURED'
floor.hide_render = False


# ---------------------------------------------------------------- 4. pose tests: the 18 animations of ClaudeMascotScene.tsx
def interp(x, xs, ys):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            f = (x - xs[i]) / (xs[i + 1] - xs[i]); return ys[i] + f * (ys[i + 1] - ys[i])


def state(name, frame, fps=FPS):
    s = dict(mascotTx=0, mascotTy=0, sx=1, sy=1, lArm=0, rArm=0, eyeTx=0, lEyeH=10, rEyeH=10,
             legTy=[0, 0, 0, 0], legH=[26] * 4)
    t = frame / fps * 2 * math.pi
    sin, cos, pi = math.sin, math.cos, math.pi
    if name == 'idle':
        s['mascotTy'] = sin(t * 1.2) * 2
        bp = frame % 80
        if bp < 4: s['lEyeH'] = s['rEyeH'] = interp(bp, [0, 2, 4], [10, 0, 10])
    elif name == 'bounce':
        arc = abs(sin(t * 3)); g = 1 - arc
        s['sy'] = 1 - g * 0.15; s['sx'] = 1 + g * 0.10
        s['mascotTy'] = 86 * (1 - s['sy']) - arc * 28; s['mascotTx'] = 48 * (1 - s['sx'])
    elif name == 'wave':
        s['rArm'] = sin(t * 3) * -12; s['mascotTy'] = sin(t * 1.5) * 2
    elif name == 'look':
        s['eyeTx'] = sin(t * 1.8) * 8; s['mascotTy'] = sin(t * 0.8) * 2
    elif name in ('walk', 'run'):
        k, amp, tx, ty = (4, 8, 3, 2) if name == 'walk' else (6, 14, 6, 4)
        lp = sin(t * k)
        s['legTy'] = [-max(0, lp) * amp, -max(0, -lp) * amp, -max(0, lp) * amp, -max(0, -lp) * amp]
        s['mascotTx'] = sin(t * k) * tx; s['mascotTy'] = -abs(sin(t * 2 * k)) * ty
    elif name == 'think':
        s['eyeTx'] = sin(t * 1.5) * 6; s['lArm'] = sin(t * 1.5) * -10; s['mascotTy'] = sin(t * 0.8) * 2
    elif name == 'type':
        s['lArm'] = s['rArm'] = 8; s['mascotTy'] = sin(t * 12) * 1.5
    elif name == 'sleep':
        h = interp(frame, [0, fps], [10, 2]); s['lEyeH'] = s['rEyeH'] = h; s['mascotTy'] = sin(t * 0.6) * 3
    elif name == 'error':
        s['mascotTx'] = sin(t * 15) * 10
    elif name == 'nod':
        s['sy'] = 1 - abs(sin(t * 3)) * 0.12; s['mascotTy'] = 86 * (1 - s['sy'])
    elif name == 'shake':
        s['mascotTx'] = sin(t * 8) * 12
    elif name == 'dance':
        arc = abs(sin(t * 4)); g = 1 - arc
        s['sy'] = 1 - g * 0.08; s['mascotTy'] = 86 * (1 - s['sy']) - arc * 15
        s['lArm'] = sin(t * 3) * -12; s['rArm'] = sin(t * 3 + pi) * -12; s['mascotTx'] = sin(t * 2) * 8
    elif name == 'stretch':
        s['sy'] = sin(t * 1.5) * 0.25 + 1; s['mascotTy'] = 86 * (1 - s['sy'])
    elif name == 'crouch':
        cr = (sin(t * 2) + 1) / 2; s['sy'] = 1 - cr * 0.25; s['mascotTy'] = 86 * (1 - s['sy'])
    elif name == 'jump':
        arc = max(0, sin(t * 2.5)); land = 1 - arc
        s['sy'] = 1 - land * 0.15; s['sx'] = 1 + land * 0.08
        s['mascotTy'] = 86 * (1 - s['sy']) - arc * 35; s['mascotTx'] = 48 * (1 - s['sx'])
    elif name == 'spin':
        s['sx'] = cos(frame / fps * 2 * pi * 1.5); s['mascotTx'] = 48 * (1 - s['sx'])
    elif name == 'celebrate':
        carc = max(0, sin(t * 2.5)); land = 1 - carc
        s['sy'] = 1 - land * 0.12; s['mascotTy'] = 86 * (1 - s['sy']) - carc * 35
        s['lArm'] = s['rArm'] = -carc * 20 - 10; s['mascotTx'] = sin(t * 4) * 10
    return s


ANIMS = ['idle', 'bounce', 'wave', 'look', 'walk', 'run', 'think', 'type', 'sleep', 'error', 'nod', 'shake', 'dance',
         'stretch', 'crouch', 'jump', 'spin', 'celebrate']


def up(ty):
    """an arm raised (2D Ty negative) is the characteristic pose of wave/think/dance; lowered counts for less"""
    return -ty if ty < 0 else ty * 0.3


def deviation(s):
    return (abs(s['mascotTx']) + abs(s['mascotTy']) + abs(1 - s['sx']) * 60 + abs(1 - s['sy']) * 60 + up(s['lArm']) + up(s['rArm'])
            + abs(s['eyeTx']) + (10 - s['lEyeH']) + sum(abs(v) for v in s['legTy']))


def pick_frame(name):
    if name == 'idle': return 10
    if name == 'sleep': return FPS
    if name == 'spin': return 5            # sx = cos(...) near 0 in 2D; in 3D this frame is rendered as a real yaw (see apply_pose)
    return max(range(0, 3 * FPS), key=lambda f: deviation(state(name, f)))


def reset_pose():
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0); pb.scale = (1, 1, 1); pb.rotation_mode = 'XYZ'; pb.rotation_euler = (0, 0, 0)


def apply_pose(name, frame):
    """2D AnimState -> bone channels. Bones point +Z, so bone-local Y is world up, local X is world right, local Z is toward the front."""
    reset_pose()
    s = state(name, frame)
    pb = rig.pose.bones
    root = pb["Root"]
    if name == 'spin':
        # the 2D scene fakes a spin with a scaleX flip (pixel-art law); in 3D it is a real yaw about the vertical axis
        root.rotation_euler = (0, math.radians(90 + 25), 0)          # bone-local Y = world up
    else:
        root.location = ((s['mascotTx'] - 48 * (1 - s['sx'])) * U, -(s['mascotTy'] - 86 * (1 - s['sy'])) * U, 0)
        root.scale = (s['sx'], s['sy'], s['sx'])
    pb["Arm.L"].location = (0, -s['lArm'] * U, 0)
    pb["Arm.R"].location = (0, -s['rArm'] * U, 0)
    for side, h in (("Eye.L", s['lEyeH']), ("Eye.R", s['rEyeH'])):
        pb[side].location = (s['eyeTx'] * U, 0, 0)
        pb[side].scale = (1, h / 10, 1)
    for i in range(4):
        pb["Leg.%d" % (i + 1)].location = (0, -s['legTy'][i] * U, 0)
        pb["Leg.%d" % (i + 1)].scale = (1, s['legH'][i] / 26, 1)


import json
poses = {}
for n, name in enumerate(ANIMS, 1):
    f = pick_frame(name)
    apply_pose(name, f)
    bpy.context.view_layer.update()
    persp(28, 10, dist=3.6)
    shot(os.path.join(OUT, "poses", "%02d-%s.png" % (n, name)))
    poses[name] = {"frame": f, "fps": FPS}
reset_pose()
json.dump(poses, open(os.path.join(OUT, "poses", "poses.json"), "w"), indent=1)
print("done: %d pose tests" % len(ANIMS))
