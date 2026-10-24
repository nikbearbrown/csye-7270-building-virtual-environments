import bpy, math

# ---------- clean ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.meshes):
    bpy.data.meshes.remove(m)

S = bpy.context.scene
S.render.engine = 'BLENDER_EEVEE_NEXT'
S.render.resolution_x, S.render.resolution_y = 1280, 720
S.render.resolution_percentage = 100
S.eevee.taa_render_samples = 40
S.display_settings.display_device = 'sRGB'
S.view_settings.view_transform = 'Standard'

# ---------- materials ----------
def principled(name, color, metallic=0.0, roughness=0.5, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if alpha < 1.0:
        bsdf.inputs['Alpha'].default_value = alpha
        mat.blend_method = 'BLEND'
    return mat

paint   = principled('Paint',   (0.028, 0.105, 0.048), metallic=0.22, roughness=0.42)
chrome  = principled('Chrome',  (0.95, 0.95, 0.97), metallic=1.0, roughness=0.08)
steel   = principled('Steel',   (0.45, 0.46, 0.48), metallic=0.9, roughness=0.42)
rimmat  = principled('Rim',     (0.58, 0.59, 0.61), metallic=0.9, roughness=0.35)
rubber  = principled('Rubber',  (0.02, 0.02, 0.02), roughness=0.92)
tan     = principled('Tan',     (0.54, 0.30, 0.11), roughness=0.72)
black   = principled('Black',   (0.03, 0.03, 0.03), roughness=0.55)
dark    = principled('Dark',    (0.05, 0.05, 0.055), roughness=0.8)
glass   = principled('Glass',   (0.85, 0.92, 0.95), roughness=0.06, alpha=0.5)
steeldark = principled('SteelDark', (0.25, 0.26, 0.27), metallic=0.85, roughness=0.5)
lens    = principled('Lens',    (0.96, 0.96, 0.92), roughness=0.15)
redlens = principled('RedLens', (0.75, 0.04, 0.04), roughness=0.25)
wood    = principled('Wood',    (0.42, 0.26, 0.11), roughness=0.55)
grille  = principled('Grille',  (0.06, 0.06, 0.06), metallic=0.6, roughness=0.5)

def mesh_obj(name, verts, faces, mat, smooth=True, subdiv=0):
    me = bpy.data.meshes.new(name + 'Mesh')
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    me.from_pydata(verts, [], faces)
    me.update()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    if subdiv:
        md = ob.modifiers.new('Subdiv', 'SUBSURF')
        md.levels = md.render_levels = subdiv
    ob.data.materials.append(mat)
    return ob

def prim_add(op, mat, name, **kw):
    op(**kw)
    ob = bpy.context.active_object
    ob.name = name
    ob.data.materials.clear()
    ob.data.materials.append(mat)
    return ob

# ---------- body hull (lofted) ----------
stations = [  # x, half_width, center_z, r_top, r_bottom
    (-2.20, 0.50, 0.52, 0.16, 0.26),
    (-1.95, 0.74, 0.54, 0.26, 0.34),
    (-1.55, 0.84, 0.57, 0.32, 0.38),
    (-1.10, 0.87, 0.60, 0.35, 0.40),
    (-0.60, 0.86, 0.63, 0.36, 0.42),
    (-0.15, 0.84, 0.65, 0.36, 0.43),
    ( 0.30, 0.81, 0.63, 0.33, 0.43),
    ( 0.80, 0.82, 0.65, 0.34, 0.43),
    ( 1.30, 0.80, 0.63, 0.31, 0.41),
    ( 1.70, 0.74, 0.61, 0.27, 0.38),
    ( 2.00, 0.62, 0.59, 0.22, 0.34),
    ( 2.20, 0.42, 0.57, 0.15, 0.28),
]
N = 20
verts, faces = [], []
for (x, w, cy, rt, rb) in stations:
    for j in range(N):
        th = 2 * math.pi * j / N
        c, s = math.cos(th), math.sin(th)
        verts.append((x, w * c, cy + (rt * s if s > 0 else rb * s)))
for si in range(len(stations) - 1):
    for j in range(N):
        a = si * N + j
        b = si * N + (j + 1) % N
        c = (si + 1) * N + (j + 1) % N
        d = (si + 1) * N + j
        faces.append((a, b, c, d))
# caps
fc = len(verts); verts.append((stations[0][0] - 0.06, 0, stations[0][2])); 
for j in range(N):
    faces.append((fc, (j + 1) % N, j))
rc = len(verts); verts.append((stations[-1][0] + 0.06, 0, stations[-1][2]))
base = (len(stations) - 1) * N
for j in range(N):
    faces.append((rc, base + j, base + (j + 1) % N))
body = mesh_obj('Body', verts, faces, paint, subdiv=2)

# ---------- wheels ----------
def wheel(x, y):
    z = 0.34
    t = prim_add(bpy.ops.mesh.primitive_cylinder_add, rubber, 'Tire',
                 radius=0.34, depth=0.20, location=(x, y, z),
                 rotation=(math.pi / 2, 0, 0))
    r = prim_add(bpy.ops.mesh.primitive_cylinder_add, rimmat, 'Rim',
                 radius=0.195, depth=0.21, location=(x, y, z),
                 rotation=(math.pi / 2, 0, 0))
    h = prim_add(bpy.ops.mesh.primitive_cylinder_add, chrome, 'Hub',
                 radius=0.05, depth=0.24, location=(x, y, z),
                 rotation=(math.pi / 2, 0, 0))
    return (t, r, h)

for sx in (-1.35, 1.25):
    for sy in (-0.72, 0.72):
        wheel(sx, sy)

# ---------- cockpit ----------
# thin dark lid just above the hull reads as the cockpit opening
op = prim_add(bpy.ops.mesh.primitive_cube_add, dark, 'CockpitOpening',
              location=(0.25, 0, 0.99))
op.scale = (0.82, 0.60, 0.025)
# dashboard
db = prim_add(bpy.ops.mesh.primitive_cube_add, black, 'Dash',
              location=(-0.42, 0, 1.03))
db.scale = (0.14, 0.56, 0.05)
# seats
for sy in (-0.30, 0.30):
    sb = prim_add(bpy.ops.mesh.primitive_cube_add, tan, 'SeatBase',
                  location=(0.35, sy, 1.04))
    sb.scale = (0.24, 0.26, 0.05)
    bk = prim_add(bpy.ops.mesh.primitive_cube_add, tan, 'SeatBack',
                  location=(0.58, sy, 1.12), rotation=(0, -0.28, 0))
    bk.scale = (0.07, 0.26, 0.14)
# steering wheel (left-hand drive side, y=-0.30)
sw = prim_add(bpy.ops.mesh.primitive_torus_add, wood, 'Steering',
              location=(-0.28, -0.30, 1.06),
              rotation=(0, math.radians(62), 0),
              major_radius=0.16, minor_radius=0.018)
col = prim_add(bpy.ops.mesh.primitive_cylinder_add, steel, 'Column',
               location=(-0.36, -0.30, 0.99), rotation=(0, math.radians(62), 0),
               radius=0.02, depth=0.22)
# folded soft-top boot (black) behind seats
bt = prim_add(bpy.ops.mesh.primitive_uv_sphere_add, black, 'TopBoot',
              location=(1.02, 0, 1.00))
bt.scale = (0.30, 0.55, 0.14)
# headrest fairing (green teardrop behind driver)
hr = prim_add(bpy.ops.mesh.primitive_uv_sphere_add, paint, 'Headrest',
              location=(0.72, -0.30, 1.03))
hr.scale = (0.26, 0.13, 0.14)

# ---------- windshield (wraparound arc) ----------
def arc_panel(name, mat, r, y_half, z0, z1, x_base, lean, thicken=0.0):
    M = 12
    vv, ff = [], []
    for row, z in enumerate((z0, z1)):
        for i in range(M + 1):
            a = -y_half + 2 * y_half * i / M
            y = r * math.sin(a) * 1.0
            x = x_base - (r - r * math.cos(a)) + (lean if row == 1 else 0.0)
            vv.append((x, y + thicken * math.sin(a), z + thicken * 0.0))
    for i in range(M):
        ff.append((i, i + 1, M + 1 + i + 1, M + 1 + i))
    return mesh_obj(name, vv, ff, mat, smooth=True)

arc_panel('ShieldGlass', glass, 1.25, 0.53, 1.015, 1.325, -0.595, 0.14)
# A-posts
for sgn in (-1, 1):
    a = 0.53 * sgn
    y = 1.25 * math.sin(a)
    x = -0.595 - (1.25 - 1.25 * math.cos(a))
    p = prim_add(bpy.ops.mesh.primitive_cylinder_add, black, 'APost',
                 location=(x + 0.07, y, 1.17), rotation=(0, math.radians(-24), 0),
                 radius=0.018, depth=0.34)

# ---------- front details ----------
# headlights
for sy in (-0.40, 0.40):
    ring = prim_add(bpy.ops.mesh.primitive_torus_add, chrome, 'HeadRing',
                    location=(-2.02, sy, 0.74), rotation=(0, math.pi / 2, 0),
                    major_radius=0.135, minor_radius=0.022)
    bulb = prim_add(bpy.ops.mesh.primitive_uv_sphere_add, lens, 'HeadLens',
                    location=(-2.03, sy, 0.74))
    bulb.scale = (0.09, 0.12, 0.12)
# grille (oval)
gr = prim_add(bpy.ops.mesh.primitive_cylinder_add, grille, 'Grille',
              location=(-2.17, 0, 0.42), rotation=(0, math.pi / 2, 0),
              radius=0.16, depth=0.06)
gr.scale = (1.0, 1.0, 1.7)
# front bumper blades
for sy in (-0.38, 0.38):
    b = prim_add(bpy.ops.mesh.primitive_cube_add, chrome, 'FBumper',
                 location=(-2.26, sy, 0.34))
    b.scale = (0.05, 0.28, 0.045)

# ---------- rear details ----------
rb = prim_add(bpy.ops.mesh.primitive_cube_add, chrome, 'RBumper',
              location=(2.28, 0, 0.44))
rb.scale = (0.05, 0.78, 0.05)
for sy in (-0.55, 0.55):
    tl = prim_add(bpy.ops.mesh.primitive_cylinder_add, redlens, 'TailLight',
                  location=(2.22, sy, 0.66), rotation=(0, math.pi / 2, 0),
                  radius=0.055, depth=0.05)
    tr = prim_add(bpy.ops.mesh.primitive_torus_add, chrome, 'TailRing',
                  location=(2.23, sy, 0.66), rotation=(0, math.pi / 2, 0),
                  major_radius=0.055, minor_radius=0.012)
# luggage rack on rear deck
deck_z = 0.99
for i, yy in enumerate((-0.30, -0.10, 0.10, 0.30)):
    tube = prim_add(bpy.ops.mesh.primitive_cylinder_add, chrome, 'RackTube',
                    location=(1.55, yy, deck_z), rotation=(0, math.pi / 2, 0),
                    radius=0.014, depth=0.85)
for xx in (1.18, 1.92):
    tube = prim_add(bpy.ops.mesh.primitive_cylinder_add, chrome, 'RackCross',
                    location=(xx, 0, deck_z), rotation=(math.pi / 2, 0, 0),
                    radius=0.014, depth=0.68)
# fuel cap
fc2 = prim_add(bpy.ops.mesh.primitive_cylinder_add, chrome, 'FuelCap',
               location=(1.45, 0.28, 0.97), radius=0.05, depth=0.02)

# ---------- side exhaust + heat shield (camera side, -Y) ----------
ex = prim_add(bpy.ops.mesh.primitive_cylinder_add, steel, 'Exhaust',
              location=(0.15, -0.82, 0.24), rotation=(0, math.pi / 2, 0),
              radius=0.065, depth=1.5)
hs = prim_add(bpy.ops.mesh.primitive_cube_add, steeldark, 'HeatShield',
              location=(0.15, -0.86, 0.22))
hs.scale = (0.60, 0.03, 0.07)
# door handle + leather strap
dh = prim_add(bpy.ops.mesh.primitive_cube_add, chrome, 'DoorHandle',
              location=(-0.10, -0.845, 0.78))
dh.scale = (0.05, 0.02, 0.02)
st = prim_add(bpy.ops.mesh.primitive_cube_add, black, 'DoorStrap',
              location=(-0.02, -0.85, 0.72))
st.scale = (0.03, 0.015, 0.12)
# mirror
mk = prim_add(bpy.ops.mesh.primitive_cylinder_add, chrome, 'MirrorStalk',
              location=(-0.52, -0.92, 1.10), rotation=(0.5, 0, 0),
              radius=0.012, depth=0.16)
mr = prim_add(bpy.ops.mesh.primitive_cylinder_add, chrome, 'Mirror',
              location=(-0.52, -0.97, 1.18), rotation=(math.pi / 2, 0, 0),
              radius=0.05, depth=0.015)

# ---------- ground, lights, world ----------
gnd = prim_add(bpy.ops.mesh.primitive_plane_add, principled('Ground', (0.82, 0.82, 0.84), roughness=0.95),
               'Ground', location=(0, 0, 0))
gnd.scale = (10, 10, 1)

w = S.world
w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.94, 0.94, 0.96, 1.0)
w.node_tree.nodes['Background'].inputs[1].default_value = 1.0

def light(kind, loc, energy, size=1.0, color=(1, 1, 1, 1)):
    bpy.ops.object.light_add(type=kind, location=loc)
    ob = bpy.context.active_object
    ob.data.energy = energy
    ob.data.color = color[:3]
    if kind == 'AREA':
        ob.data.size = size
    return ob

light('SUN', (5, -6, 9), 2.2)
light('AREA', (-4, -5, 4), 900, size=3.0)
light('AREA', (5, 4, 3), 350, size=2.5)
light('AREA', (0, 6, 2.5), 250, size=2.0)

# ---------- cameras ----------
def camera(name, loc, target=(0, 0, 0.62)):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = name
    bpy.ops.object.empty_add(location=target)
    tgt = bpy.context.active_object
    tgt.name = name + 'Tgt'
    c = cam.constraints.new('TRACK_TO')
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    cam.data.lens = 55
    return cam

import os
outdir = os.path.expanduser('~/workspace/blender/jaguar-xkss')
os.makedirs(outdir, exist_ok=True)

c1 = camera('CamSide', (0.15, -6.9, 1.18))
S.camera = c1
S.render.filepath = os.path.join(outdir, 'xkss_side.png')
bpy.ops.render.render(write_still=True)

c2 = camera('CamRear34', (4.7, -4.3, 1.75))
S.camera = c2
S.render.filepath = os.path.join(outdir, 'xkss_rear34.png')
bpy.ops.render.render(write_still=True)

c3 = camera('CamFront34', (-4.7, -4.3, 1.55))
S.camera = c3
S.render.filepath = os.path.join(outdir, 'xkss_front34.png')
bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outdir, 'xkss.blend'))
print('DONE')
