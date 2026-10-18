# Jaguar XKSS (1957 / continuation) - lofted subdivision body + detail parts
# Usage: blender -b -P build_xkss.py -- --round 1 --res 800 --samples 16 [--cams side,front,rear34,hero] [--norender]
import bpy, bmesh, math, sys, os, json
import numpy as np
from mathutils import Vector, Matrix, Euler
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def arg(name, default):
    if '--'+name in argv:
        return argv[argv.index('--'+name)+1]
    return default
ROUND = int(arg('round', 1)); RES = int(arg('res', 800)); SAMPLES = int(arg('samples', 16))
CAMS = arg('cams', 'side,front,rear34,hero').split(',')
NORENDER = '--norender' in argv
OUT = '/workspace/cars/xkss'
os.makedirs(OUT+'/renders', exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col_body = bpy.data.collections.new('Body'); scene.collection.children.link(col_body)

# ---------------------------------------------------------------- materials
def mat(name, color, metal=0.0, rough=0.5, coat=0.0, coat_rough=0.03, emis=None, emis_str=0.0, alpha=1.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat
    b.inputs['Coat Roughness'].default_value = coat_rough
    b.inputs['Transmission Weight'].default_value = trans
    b.inputs['IOR'].default_value = ior
    if emis:
        b.inputs['Emission Color'].default_value = (*emis, 1); b.inputs['Emission Strength'].default_value = emis_str
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
    return m

M = {}
M['chrome'] = mat('Chrome', (0.9, 0.9, 0.92), 1.0, 0.06)
M['darkchrome'] = mat('FrameDark', (0.05, 0.05, 0.05), 0.6, 0.25, coat=0.5)
M['rubber'] = mat('TyreRubber', (0.018, 0.018, 0.018), 0.0, 0.7)
M['black'] = mat('SatinBlack', (0.01, 0.01, 0.01), 0.0, 0.45)
M['leather'] = mat('TanLeather', (0.42, 0.20, 0.08), 0.0, 0.5, coat=0.15, coat_rough=0.3)
M['wood'] = mat('WoodRim', (0.35, 0.16, 0.05), 0.0, 0.3, coat=0.6)
M['glass'] = mat('Glass', (0.95, 0.97, 0.96), 0.0, 0.0, trans=1.0, ior=1.5)
M['lens'] = mat('LampLens', (0.95, 0.95, 0.9), 0.0, 0.05, trans=0.9, ior=1.5)
M['reflector'] = mat('Reflector', (0.9, 0.9, 0.88), 1.0, 0.12)
M['redlens'] = mat('TailRed', (0.6, 0.01, 0.01), 0.0, 0.08, coat=1.0, emis=(0.8, 0.02, 0.01), emis_str=0.4)
M['amber'] = mat('SideLens', (0.9, 0.85, 0.75), 0.0, 0.1, trans=0.6)
M['silver'] = mat('WheelSilver', (0.62, 0.63, 0.64), 0.85, 0.3)
M['fabric'] = mat('HoodFabric', (0.006, 0.006, 0.007), 0.0, 0.95)
M['mesh'] = mat('GrilleMesh', (0.03, 0.035, 0.03), 0.7, 0.4)
M['plate'] = mat('PlateBlack', (0.008, 0.008, 0.008), 0.0, 0.35, coat=0.8)
M['white'] = mat('PlateText', (0.9, 0.9, 0.9), 0.0, 0.4)
M['strap'] = mat('StrapLeather', (0.09, 0.035, 0.015), 0.0, 0.55, coat=0.2)
M['steel'] = mat('PerfSteel', (0.7, 0.7, 0.7), 1.0, 0.22)
M['inner'] = mat('WellDark', (0.006, 0.01, 0.007), 0.0, 0.6)
M['gauge'] = mat('GaugeFace', (0.02, 0.02, 0.02), 0.0, 0.2, coat=1.0)

# --- paint with procedural panel gaps (object-space line masks -> bump + darken)
def paint_material():
    m = bpy.data.materials.new('BRG_Paint'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.010, 0.050, 0.026, 1)
    b.inputs['Metallic'].default_value = 0.55
    b.inputs['Roughness'].default_value = 0.32
    b.inputs['Coat Weight'].default_value = 1.0
    b.inputs['Coat Roughness'].default_value = 0.02
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ')
    L.new(tc.outputs['Object'], sep.inputs[0])
    X, Y, Z = sep.outputs[0], sep.outputs[1], sep.outputs[2]
    absN = N.new('ShaderNodeMath'); absN.operation = 'ABSOLUTE'; L.new(Y, absN.inputs[0]); absY = absN.outputs[0]
    def mnode(op, a, bval=None):
        n = N.new('ShaderNodeMath'); n.operation = op
        if isinstance(a, float): n.inputs[0].default_value = a
        else: L.new(a, n.inputs[0])
        if bval is not None:
            if isinstance(bval, float): n.inputs[1].default_value = bval
            else: L.new(bval, n.inputs[1])
        return n.outputs[0]
    def band(coord, c0, hw):  # 1 inside |coord-c0|<hw (soft)
        d = mnode('ABSOLUTE', mnode('SUBTRACT', coord, float(c0)))
        return mnode('SUBTRACT', 1.0, mnode('SMOOTH_MIN', mnode('DIVIDE', d, float(hw)), 1.0) if False else mnode('MINIMUM', mnode('DIVIDE', d, float(hw)), 1.0))
    def rng(coord, a, b_):
        return mnode('MULTIPLY', mnode('GREATER_THAN', coord, float(a)), mnode('LESS_THAN', coord, float(b_)))
    hw = 0.0012
    lines = []
    side = mnode('GREATER_THAN', absY, 0.55)
    # horizontal waist seam (rivet line) along the sides
    lines.append(mnode('MULTIPLY', mnode('MULTIPLY', band(Z, 0.470, hw), rng(X, -1.62, 1.58)), side))
    # door front & rear edges, rear wing seam, bonnet rear seam (vertical lines on sides)
    for x0, z0, z1 in [(0.075, 0.47, 0.72), (-0.545, 0.47, 0.72), (-0.72, 0.47, 0.80), (0.30, 0.47, 0.80)]:
        lines.append(mnode('MULTIPLY', mnode('MULTIPLY', band(X, x0, hw), rng(Z, z0, z1)), side))
    # bonnet top seam where bonnet meets scuttle (transverse line on top)
    lines.append(mnode('MULTIPLY', band(X, 0.30, hw), mnode('GREATER_THAN', Z, 0.70)))
    acc = lines[0]
    for l in lines[1:]:
        acc = mnode('MAXIMUM', acc, l)
    bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; bump.inputs['Distance'].default_value = 0.002
    inv = mnode('SUBTRACT', 1.0, acc)
    L.new(inv, bump.inputs['Height'])
    L.new(bump.outputs['Normal'], b.inputs['Normal'])
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    L.new(acc, mix.inputs['Factor'])
    mix.inputs[6].default_value = (0.010, 0.050, 0.026, 1); mix.inputs[7].default_value = (0.002, 0.006, 0.003, 1)
    L.new(mix.outputs[2], b.inputs['Base Color'])
    return m
M['paint'] = paint_material()

def link(obj, coll=None):
    (coll or scene.collection).objects.link(obj); return obj

def new_obj(name, me, material=None, coll=None):
    o = bpy.data.objects.new(name, me); link(o, coll)
    if material: o.data.materials.append(material)
    return o

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True

# ---------------------------------------------------------------- profile tables (metres)
# X, half-width w, shoulder z, bottom z, crown z, crown y-frac, centre z, valley z
T = np.array([
(1.745,0.55,0.46,0.30,0.56,0.80,0.50,0.51),
(1.735,0.68,0.47,0.235,0.625,0.84,0.53,0.545),
(1.71, 0.78,0.48,0.20,0.675,0.85,0.565,0.585),
(1.66, 0.815,0.49,0.185,0.71,0.82,0.62,0.625),
(1.58, 0.83,0.50,0.18,0.745,0.79,0.68,0.665),
(1.45, 0.832,0.51,0.205,0.775,0.75,0.74,0.715),
(1.25, 0.832,0.52,0.20,0.810,0.75,0.785,0.755),
(1.05, 0.825,0.525,0.21,0.822,0.74,0.815,0.78),
(0.85, 0.80,0.53,0.22,0.820,0.73,0.83,0.785),
(0.65, 0.775,0.53, 0.205,0.810,0.73,0.825,0.78),
(0.45, 0.75, 0.53, 0.20,0.792,0.75,0.805,0.77),
(0.25, 0.735,0.53, 0.20,0.778,0.80,0.785,0.765),
(0.15, 0.73, 0.53, 0.20,0.74,0.84,0.74,0.74),
(0.0,  0.725,0.53, 0.20,0.705,0.86,0.705,0.705),
(-0.30,0.725,0.53, 0.20,0.70,0.86,0.70,0.70),
(-0.60,0.735,0.535,0.20,0.705,0.85,0.705,0.705),
(-0.75,0.77, 0.545,0.21,0.725,0.75,0.70,0.695),
(-0.90,0.805,0.555,0.235,0.748,0.66,0.70,0.69),
(-1.05,0.825,0.565,0.24,0.758,0.62,0.70,0.69),
(-1.25,0.83,0.57,0.24,0.750,0.60,0.695,0.685),
(-1.45,0.815,0.56,0.25,0.718,0.58,0.675,0.665),
(-1.63,0.79,0.545,0.265,0.665,0.56,0.635,0.625),
(-1.76,0.75,0.525,0.29,0.62,0.54,0.60,0.595),
(-1.87,0.69,0.50,0.33,0.575,0.52,0.56,0.555),
(-1.96,0.61,0.48,0.365,0.535,0.50,0.525,0.52),
(-2.01,0.50,0.47,0.395,0.505,0.48,0.50,0.50),
(-2.035,0.36,0.465,0.42,0.485,0.45,0.48,0.48),
])[::-1]  # ascending X

def pchip(xk, yk, x):
    xk = np.asarray(xk); yk = np.asarray(yk); h = np.diff(xk); d = np.diff(yk)/h
    m = np.zeros_like(yk)
    for i in range(1, len(xk)-1):
        if d[i-1]*d[i] > 0:
            w1 = 2*h[i]+h[i-1]; w2 = h[i]+2*h[i-1]
            m[i] = (w1+w2)/(w1/d[i-1]+w2/d[i])
    m[0] = d[0]; m[-1] = d[-1]
    i = np.clip(np.searchsorted(xk, x)-1, 0, len(xk)-2)
    t = (x-xk[i])/h[i]; h00 = 2*t**3-3*t**2+1; h10 = t**3-2*t**2+t; h01 = -2*t**3+3*t**2; h11 = t**3-t**2
    return h00*yk[i]+h10*h[i]*m[i]+h01*yk[i+1]+h11*h[i]*m[i+1]

def prof(x):
    return [float(pchip(T[:,0], T[:,j], np.array([x]))[0]) for j in range(1, 8)]

def smoothstep(e0, e1, v):
    t = min(max((v-e0)/(e1-e0), 0.0), 1.0); return t*t*(3-2*t)

# cockpit
CK_FRONT, CK_REAR, CK_FLOOR = 0.17, -0.70, 0.30
def dep(x):
    return smoothstep(CK_FRONT+0.05, CK_FRONT-0.02, x) * smoothstep(CK_REAR-0.06, CK_REAR+0.02, x)

# parameter grids
s_c = 0.70
s_up = np.concatenate([np.linspace(0, 0.46, 12, endpoint=False), np.linspace(0.46, 0.66, 14, endpoint=False),
                       np.linspace(0.66, 1.0, 16)])
K = len(s_up); Lw = 16
th = np.linspace(math.pi/2, 0, Lw+1)[1:]  # lower, excluding shoulder

def section(x):
    w, zs, zb, Zc, ycf, Zh, Zv = prof(x)
    yc = ycf*w; yv = 0.55*yc; d = dep(x)
    pts = []; flags = []
    for s in s_up:
        if s <= s_c:
            y = s/s_c*yc
            if y <= yv:
                t = y/yv; z = Zh + (Zv-Zh)*(1-math.cos(math.pi*t))/2
            else:
                t = (y-yv)/(yc-yv); z = Zv + (Zc-Zv)*(1-math.cos(math.pi*t))/2
        else:
            a = (s-s_c)/(1-s_c)*math.pi/2
            y = yc+(w-yc)*math.sin(a); z = zs+(Zc-zs)*math.cos(a)
        inside = False
        if d > 0:
            if s < 0.50:
                zc = CK_FLOOR; inside = True
            elif s < 0.62:
                t = (s-0.50)/0.12; zc = CK_FLOOR + (z-CK_FLOOR)*math.sin(t*math.pi/2)**0.7; inside = t < 0.85
            else:
                zc = z
            z = z + (zc-z)*d
            inside = inside and d > 0.5
        pts.append((x, y, z)); flags.append(inside)
    n = 1.9
    for t in th:
        y = w*math.sin(t)**(2/n); z = zs-(zs-zb)*math.cos(t)**(2/n)
        pts.append((x, y, z)); flags.append(False)
    right = pts; rf = flags
    left = [(p[0], -p[1], p[2]) for p in right[1:-1]][::-1]
    return right+left, rf+rf[1:-1][::-1]

def build_body():
    xs = np.concatenate([np.linspace(-2.035, -1.85, 14, endpoint=False), np.linspace(-1.85, 1.55, 120, endpoint=False),
                         np.linspace(1.55, 1.745, 14)])
    # make cockpit edges dense
    xs = np.unique(np.concatenate([xs, np.linspace(CK_FRONT-0.04, CK_FRONT+0.07, 6), np.linspace(CK_REAR-0.08, CK_REAR+0.04, 6)]))
    bm = bmesh.new(); rings = []; rflags = []
    for x in xs:
        pts, fl = section(float(x))
        rings.append([bm.verts.new(p) for p in pts]); rflags.append(fl)
    R = len(rings[0])
    for i in range(len(rings)-1):
        for j in range(R):
            j2 = (j+1) % R
            f = bm.faces.new((rings[i][j], rings[i+1][j], rings[i+1][j2], rings[i][j2]))
            if rflags[i][j] and rflags[i+1][j] and rflags[i][j2] and rflags[i+1][j2]:
                f.material_index = 1
    for ring, sign in ((rings[0], -1), (rings[-1], 1)):
        c = Vector((0, 0, 0))
        for v in ring: c += v.co
        c /= len(ring); c.x += sign*0.012
        cv = bm.verts.new(c)
        for j in range(R):
            v1, v2 = ring[j], ring[(j+1) % R]
            bm.faces.new((v1, v2, cv) if sign > 0 else (v2, v1, cv))
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # ---- wheel arches: delete faces then snap boundary to ellipse
    arches = [dict(cx=1.15, rx=0.40, ry=0.285, cz=0.33, yin=0.47), dict(cx=-1.185, rx=0.37, ry=0.150, cz=0.33, yin=0.45)]
    def in_arch(co, a, grow=0.0):
        dx = (co.x-a['cx'])/(a['rx']+grow); dz = co.z-a['cz']
        if abs(co.y) < a['yin']: return False
        if dz > 0: return dx*dx + (dz/(a['ry']+grow))**2 < 1
        return abs(dx) < 1
    kill = [f for f in bm.faces if any(in_arch(f.calc_center_median(), a) for a in arches)]
    # grille mouth: front-facing faces inside an ellipse in y/z
    GZ, GW, GH = 0.335, 0.27, 0.098
    def in_grille(co): return co.x > 1.55 and (co.y/GW)**2 + ((co.z-GZ)/GH)**2 < 1
    kill += [f for f in bm.faces if f.normal.x > 0.3 and in_grille(f.calc_center_median())]
    HL = [(sy*0.645, 0.515) for sy in (1, -1)]; HR = 0.126
    def in_lamp(co): return co.x > 1.45 and any((co.y-hy)**2 + (co.z-hz)**2 < HR*HR for hy, hz in HL)
    kill += [f for f in bm.faces if f.normal.x > 0.25 and in_lamp(f.calc_center_median())]
    bmesh.ops.delete(bm, geom=list(set(kill)), context='FACES')
    for v in bm.verts:
        if not v.is_boundary: continue
        for a in arches:
            if abs(v.co.y) < a['yin']+0.05: continue
            dx = v.co.x-a['cx']; dz = v.co.z-a['cz']
            if abs(dx) > a['rx']*1.35 or dz > a['ry']*1.6: continue
            if dz > 0:
                ang = math.atan2(dz/a['ry'], dx/a['rx'])
                v.co.x = a['cx']+a['rx']*math.cos(ang); v.co.z = a['cz']+a['ry']*math.sin(ang)
            else:
                v.co.x = a['cx'] + math.copysign(a['rx'], dx)
        for hy, hz in HL:
            if v.co.x > 1.45 and (v.co.y-hy)**2 + (v.co.z-hz)**2 < (HR*1.5)**2:
                ang = math.atan2(v.co.z-hz, v.co.y-hy); v.co.y = hy+HR*math.cos(ang); v.co.z = hz+HR*math.sin(ang)
        if v.co.x > 1.55 and abs(v.co.y) < GW*1.3 and abs(v.co.z-GZ) < GH*1.4:
            ang = math.atan2((v.co.z-GZ)/GH, v.co.y/GW)
            v.co.y = GW*math.cos(ang); v.co.z = GZ+GH*math.sin(ang)
    me = bpy.data.meshes.new('XKSS_Body'); bm.to_mesh(me); bm.free()
    o = new_obj('XKSS_Body', me, M['paint'], col_body); o.data.materials.append(M['leather'])
    smooth(o)
    sub = o.modifiers.new('Subsurf', 'SUBSURF'); sub.levels = 1; sub.render_levels = 2
    so = o.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = 0.003; so.offset = -1
    return o, arches, (GZ, GW, GH)

body, ARCHES, GRILLE = build_body()
dg = bpy.context.evaluated_depsgraph_get()
bvh = BVHTree.FromObject(body, dg)

def hit(origin, direction):
    loc, nor, idx, dist = bvh.ray_cast(Vector(origin), Vector(direction).normalized(), 10.0)
    return loc, nor

# ---------------------------------------------------------------- helpers for parts
def add_prim(kind, name, mat_, loc=(0,0,0), rot=(0,0,0), scale=(1,1,1), coll=None, **kw):
    if kind == 'cyl': bpy.ops.mesh.primitive_cylinder_add(location=loc, rotation=rot, **kw)
    elif kind == 'cube': bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot, **kw)
    elif kind == 'sphere': bpy.ops.mesh.primitive_uv_sphere_add(location=loc, rotation=rot, **kw)
    elif kind == 'torus': bpy.ops.mesh.primitive_torus_add(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    if mat_: o.data.materials.append(mat_)
    if coll:
        for c in o.users_collection: c.objects.unlink(o)
        coll.objects.link(o)
    return o

def lathe(name, profile, mat_, segs=64, coll=None):
    """profile: list of (r, a) where a is axial coordinate; revolve around local Z"""
    bm = bmesh.new(); rings = []
    for k in range(segs):
        ang = 2*math.pi*k/segs; c, s = math.cos(ang), math.sin(ang)
        rings.append([bm.verts.new((r*c, r*s, a)) for r, a in profile])
    for k in range(segs):
        r1, r2 = rings[k], rings[(k+1) % segs]
        for i in range(len(profile)-1):
            try: bm.faces.new((r1[i], r2[i], r2[i+1], r1[i+1]))
            except ValueError: pass
    bmesh.remove_doubles(bm, verts=bm.verts, dist=1e-6) if False else None
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = new_obj(name, me, mat_, coll); smooth(o); return o

def tube_path(name, pts, radius, mat_, coll=None, flat=1.0, res=8):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i, p in enumerate(pts): sp.points[i].co = (*p, 1)
    cu.bevel_depth = radius; cu.bevel_resolution = res//2; cu.use_fill_caps = True
    o = bpy.data.objects.new(name, cu); link(o, coll)
    o.data.materials.append(mat_)
    if flat != 1.0:
        o.data.taper_radius_mode = 'MULTIPLY'
    return o

def to_mesh(o):
    bpy.context.view_layer.objects.active = o
    for ob in bpy.context.selected_objects: ob.select_set(False)
    o.select_set(True); bpy.ops.object.convert(target='MESH'); return o

col_parts = bpy.data.collections.new('Parts'); scene.collection.children.link(col_parts)
col_wheels = bpy.data.collections.new('Wheels'); scene.collection.children.link(col_wheels)
col_int = bpy.data.collections.new('Interior'); scene.collection.children.link(col_int)

def orient_to(o, normal):
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector(normal).to_track_quat('Z', 'Y')

# ---------------------------------------------------------------- wheels
TYRE_R, RIM_R, TW = 0.318, 0.205, 0.155
def build_wheel_mesh():
    # tyre profile in (r, axial) - axial along local Z, outer face at +Z
    tp = []
    for k in range(25):
        a = math.pi*(k/24)  # 0..pi around section
        r = (RIM_R+TYRE_R)/2 + (TYRE_R-RIM_R)/2*math.sin(a)*1.0
        r = RIM_R + 0.012 + (TYRE_R-RIM_R-0.012)*(math.sin(a)**0.45)
        z = (TW/2)*math.cos(a)*(0.92+0.08*math.sin(a))
        tp.append((r, z))
    tyre = lathe('Tyre', tp, M['rubber'], 96, col_wheels)
    # disc wheel: rim lip, dish, holes ring, hub
    dp = [(RIM_R+0.018, 0.07), (RIM_R+0.012, 0.078), (RIM_R-0.004, 0.072), (RIM_R-0.01, 0.06), (RIM_R-0.03, 0.05),
          (0.15, 0.04), (0.11, 0.03), (0.075, 0.035), (0.062, 0.055), (0.055, 0.07), (0.0, 0.07)]
    disc = lathe('WheelDisc', dp, M['silver'], 96, col_wheels)
    barrel = lathe('Rim', [(RIM_R+0.004, -0.075), (RIM_R+0.004, 0.072)], M['silver'], 64, col_wheels)
    # perforation holes as dark inset discs on the dish (ring of 16)
    holes = []
    for k in range(16):
        ang = 2*math.pi*k/16; r = 0.132
        h = add_prim('cyl', 'Hole', M['inner'], loc=(r*math.cos(ang), r*math.sin(ang), 0.041), vertices=16, radius=0.0115, depth=0.006)
        holes.append(h)
    # centre-lock spinner: hub cylinder + three ears
    hub = add_prim('cyl', 'Hub', M['chrome'], loc=(0, 0, 0.085), vertices=32, radius=0.048, depth=0.035)
    cap = add_prim('sphere', 'HubCap', M['chrome'], loc=(0, 0, 0.10), segments=24, ring_count=12, radius=0.034, scale=(1,1,0.5))
    ears = []
    for k in range(3):
        ang = 2*math.pi*k/3
        e = add_prim('cube', 'Ear', M['chrome'], loc=(0.055*math.cos(ang), 0.055*math.sin(ang), 0.093), rot=(0,0,ang), size=1, scale=(0.065, 0.016, 0.012))
        ears.append(e)
    parts = [tyre, disc, barrel, hub, cap] + holes + ears
    for p in parts: p.select_set(True)
    bpy.context.view_layer.objects.active = disc
    for ob in bpy.context.selected_objects:
        if ob not in parts: ob.select_set(False)
    bpy.ops.object.join(); w = bpy.context.active_object; w.name = 'Wheel'
    return w

wheel = build_wheel_mesh()
WHEELS = [('FL', 1.15, 0.635), ('FR', 1.15, -0.635), ('RL', -1.15, 0.61), ('RR', -1.15, -0.61)]
for nm, x, y in WHEELS:
    o = wheel if nm == 'FL' else bpy.data.objects.new('Wheel_'+nm, wheel.data)
    if nm != 'FL': col_wheels.objects.link(o)
    else: o.name = 'Wheel_FL'
    o.location = (x, y, TYRE_R)
    o.rotation_euler = (-math.pi/2 if y > 0 else math.pi/2, 0, 0)
# brake discs / wheel wells
for nm, x, y in WHEELS:
    a = ARCHES[0] if x > 0 else ARCHES[1]
    s = 1 if y > 0 else -1
    well = add_prim('cyl', 'WheelWell_'+nm, M['inner'], loc=(x, s*0.60, TYRE_R+0.02), rot=(math.pi/2, 0, 0), vertices=48, radius=0.40, depth=0.36, coll=col_parts)
    # remove the bottom half & caps -> keep as liner (just flip normals inward visually ok)
    bm = bmesh.new(); bm.from_mesh(well.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_center_median().y < -0.02 or len(f.verts) > 4], context='FACES')
    bm.to_mesh(well.data); bm.free()
    well.data.update()
    bd = add_prim('cyl', 'BrakeDisc_'+nm, M['steel'], loc=(x, s*(abs(y)-0.09), TYRE_R), rot=(math.pi/2, 0, 0), vertices=32, radius=0.15, depth=0.02, coll=col_parts)

# ---------------------------------------------------------------- front: headlamps, sidelamps, grille, bumperettes
def place_front(y, z, back=0.0):
    loc, nor = hit((2.5, y, z), (-1, 0, 0))
    return loc
for s in (1, -1):
    y, z = s*0.645, 0.515
    loc = place_front(y, z+0.15)
    x0 = loc.x if loc else 1.62
    # deep nacelle: dark cup, chrome bezel ring, reflector, lens
    cup = add_prim('cyl', 'HeadlampNacelle', M['inner'], loc=(x0-0.05, y, z), rot=(0, math.pi/2, 0), end_fill_type='NOTHING', vertices=48, radius=0.135, depth=0.12, coll=col_parts)
    ring = add_prim('torus', 'HeadlampBezel', M['chrome'], loc=(x0+0.005, y, z), rot=(0, math.pi/2, 0), major_radius=0.128, minor_radius=0.011, major_segments=64, minor_segments=12, coll=col_parts)
    ring2 = add_prim('torus', 'HeadlampRim', M['chrome'], loc=(x0-0.035, y, z), rot=(0, math.pi/2, 0), major_radius=0.094, minor_radius=0.007, major_segments=48, minor_segments=10, coll=col_parts)
    refl = add_prim('sphere', 'HeadlampReflector', M['reflector'], loc=(x0-0.06, y, z), segments=32, ring_count=16, radius=0.09, scale=(0.45, 1, 1), coll=col_parts)
    lens = add_prim('sphere', 'HeadlampLens', M['lens'], loc=(x0-0.04, y, z), segments=32, ring_count=16, radius=0.092, scale=(0.22, 1, 1), coll=col_parts)
    for o in (refl, lens): smooth(o)
    # sidelamp
    ys, zs_ = s*0.50, 0.37
    loc = place_front(ys, zs_); xs_ = loc.x if loc else 1.66
    sr = add_prim('torus', 'SidelampRing', M['chrome'], loc=(xs_+0.004, ys, zs_), rot=(0, math.pi/2, 0), major_radius=0.033, minor_radius=0.007, coll=col_parts)
    sl = add_prim('sphere', 'SidelampLens', M['amber'], loc=(xs_, ys, zs_), radius=0.031, scale=(0.4, 1, 1), coll=col_parts); smooth(sl)
GZ, GW, GH = GRILLE
loc = place_front(0, GZ+GH+0.03); gx = (loc.x if loc else 1.74) + 0.02
duct = add_prim('cyl', 'GrilleDuct', M['inner'], loc=(gx-0.10, 0, GZ), rot=(0, math.pi/2, 0), end_fill_type='NOTHING', vertices=64, radius=1, depth=0.22, scale=(GH+0.004, GW+0.004, 1), coll=col_parts)
lip = add_prim('torus', 'GrilleLip', M['paint'], loc=(gx-0.03, 0, GZ), rot=(0, math.pi/2, 0), major_radius=1, minor_radius=0.012, major_segments=64, scale=(GH, GW, 1), coll=col_parts)
lip.scale = (GH, GW, 1.0)
# grille mesh: vertical bars + horizontal wires inside the oval
gm = []
for k in range(-26, 27):
    yy = k*0.0102; hh = GH*math.sqrt(max(0, 1-(yy/GW)**2))
    if hh < 0.01: continue
    gm.append(add_prim('cube', 'GrilleBar', M['mesh'], loc=(gx-0.06, yy, GZ), size=1, scale=(0.004, 0.0025, 2*hh)))
for k in range(-8, 9):
    zz = k*0.011; ww = GW*math.sqrt(max(0, 1-(zz/GH)**2))
    if ww < 0.01: continue
    gm.append(add_prim('cube', 'GrilleWire', M['mesh'], loc=(gx-0.065, 0, GZ+zz), size=1, scale=(0.003, 2*ww, 0.0018)))
for o in gm: o.select_set(True)
bpy.context.view_layer.objects.active = gm[0]; bpy.ops.object.join(); gmesh = bpy.context.active_object; gmesh.name = 'GrilleMesh'
for c in gmesh.users_collection: c.objects.unlink(gmesh)
col_parts.objects.link(gmesh)

def wrap_curve(z, angles, center, offset, name, radius, mat_, flatz=0.35):
    """raycast inward from a ring of directions in the XY plane at height z around 'center'; offset outward"""
    pts = []
    for a in angles:
        d = Vector((math.cos(a), math.sin(a), 0))
        o = Vector(center) + d*3.0; o.z = z
        loc, nor = hit(o, -d)
        if loc is None: continue
        n2 = Vector((nor.x, nor.y, 0)).normalized()
        pts.append(tuple(loc + n2*offset))
    t = tube_path(name, pts, radius, mat_, col_parts)
    t.scale = (1, 1, 1)
    return t, pts
# front bumperettes (split, wrapping the corners)
for s in (1, -1):
    angs = [s*math.radians(a) for a in np.linspace(14, 78, 18)]
    t, pts = wrap_curve(0.31, angs, (1.25, 0, 0), 0.03, 'FrontBumperette', 0.017, M['chrome'])
    to_mesh(t); t.data.transform(Matrix.Translation((0, 0, -0.31)) ); t.scale = (1, 1, 1.6); t.location.z = 0.31
    # bumper mounts
    if pts:
        mid = Vector(pts[len(pts)//3])
        pass  # add_prim('cyl', 'BumperMount', M['chrome'], loc=(mid.x-0.03, mid.y, mid.z), rot=(0, math.pi/2, 0), radius=0.008, depth=0.06, coll=col_parts)

# ---------------------------------------------------------------- rear: bumpers, tail lamps, plate
for s in (1, -1):
    angs = [math.pi - s*math.radians(a) for a in np.linspace(8, 72, 18)]
    t, pts = wrap_curve(0.455, angs, (-1.55, 0, 0), 0.022, 'RearBumper', 0.012, M['chrome'])
    to_mesh(t); t.data.transform(Matrix.Translation((0, 0, -0.455))); t.scale = (1, 1, 1.5); t.location.z = 0.455
    # tail lamp on the haunch
    loc, nor = hit((-3.0, s*0.50, 0.555), (1, 0, 0))
    if loc:
        tl = add_prim('cyl', 'TailLampBody', M['chrome'], loc=loc, vertices=32, radius=0.034, depth=0.03, coll=col_parts); orient_to(tl, nor)
        tr = add_prim('sphere', 'TailLampLens', M['redlens'], loc=loc+nor*0.018, radius=0.032, coll=col_parts); orient_to(tr, nor); tr.scale = (1, 1, 0.5); smooth(tr)
loc, nor = hit((-3, 0, 0.40), (1, 0, 0))
if loc:
    pl = add_prim('cube', 'RearPlate', M['plate'], loc=loc+Vector((-0.012, 0, 0)), size=1, scale=(0.006, 0.26, 0.085), coll=col_parts)
    bpy.ops.object.text_add(location=(loc.x-0.016, 0, loc.z-0.02), rotation=(math.pi/2, 0, -math.pi/2))
    tx = bpy.context.active_object; tx.name = 'PlateText'; tx.data.body = 'XKSS'; tx.data.size = 0.05; tx.data.align_x = 'CENTER'
    tx.data.extrude = 0.001; tx.data.materials.append(M['white'])
    to_mesh(tx)
    for c in tx.users_collection: c.objects.unlink(tx)
    col_parts.objects.link(tx)
    # small jaguar badge above plate
    bg = add_prim('cyl', 'RearBadge', M['chrome'], loc=loc+Vector((-0.004, 0, 0.11)), rot=(0, math.pi/2, 0), radius=0.02, depth=0.006, coll=col_parts)

# ---------------------------------------------------------------- bonnet louvres (both sides)
for s in (1, -1):
    for k in range(12):
        x = 0.47 + k*0.017
        loc, nor = hit((x, s*0.43, 2.0), (0, 0, -1))
        if not loc: continue
        lv = add_prim('cube', 'Louvre', M['inner'], loc=loc, size=1, scale=(0.006, 0.11, 0.012), coll=col_parts)
        orient_to(lv, nor); lv.scale = (0.006, 0.11, 0.02)
        lp = add_prim('cube', 'LouvreLip', M['paint'], loc=loc+nor*0.004+Vector((0.004, 0, 0)), size=1, scale=(0.004, 0.11, 0.006), coll=col_parts)
        orient_to(lp, nor); lp.scale = (0.004, 0.11, 0.006)

# ---------------------------------------------------------------- rivets along seams (instanced mesh)
rv = add_prim('sphere', 'Rivet', M['silver'], segments=8, ring_count=4, radius=0.0035, coll=col_parts); rv.scale = (1, 1, 0.5)
rivet_mesh = rv.data; rv_count = 0
def rivet_at(origin, direction):
    global rv_count
    loc, nor = hit(origin, direction)
    if not loc: return
    o = bpy.data.objects.new('Rivet', rivet_mesh); col_parts.objects.link(o)
    o.location = loc; orient_to(o, nor); o.scale = (1, 1, 0.5); rv_count += 1
for s in (1, -1):
    for x in np.arange(-0.80, 0.74, 0.035):
        rivet_at((x, s*2.0, 0.448), (0, -s, 0))
    for x0 in (0.06, -0.56):
        for z in np.arange(0.49, 0.70, 0.04):
            rivet_at((x0, s*2.0, z), (0, -s, 0))
    for x in np.arange(-0.70, 0.17, 0.05):
        rivet_at((x, s*0.70, 1.5), (0, 0, -1)) if False else None
bpy.data.objects.remove(rv)

# ---------------------------------------------------------------- bonnet latch + leather strap (left wing, both sides)
for s in (1, -1):
    loc, nor = hit((0.33, s*2, 0.50), (0, -s, 0))
    if loc:
        st = add_prim('cube', 'BonnetStrap', M['strap'], loc=loc+nor*0.004, size=1, coll=col_parts)
        orient_to(st, nor); st.scale = (0.024, 0.20, 0.004)
        st.location.z -= 0.08
        bk = add_prim('cube', 'StrapBuckle', M['chrome'], loc=loc+nor*0.008+Vector((0, 0, -0.02)), size=1, coll=col_parts)
        orient_to(bk, nor); bk.scale = (0.034, 0.03, 0.004)
    loc, nor = hit((0.41, s*2, 0.55), (0, -s, 0))
    if loc:
        la = add_prim('cyl', 'BonnetLatch', M['chrome'], loc=loc+nor*0.01, radius=0.012, depth=0.02, coll=col_parts); orient_to(la, nor)
        lv = add_prim('cube', 'LatchLever', M['chrome'], loc=loc+nor*0.02+Vector((0.04, 0, 0)), size=1, coll=col_parts); orient_to(lv, nor); lv.scale = (0.07, 0.008, 0.005)

# ---------------------------------------------------------------- side step / exhaust heat shield + twin exhaust (left side)
yy = 0.64
shield = add_prim('cube', 'HeatShield', M['steel'], loc=(0.06, yy+0.04, 0.165), size=1, scale=(0.70, 0.05, 0.11), coll=col_parts)
bev = shield.modifiers.new('bev', 'BEVEL'); bev.width = 0.012; bev.segments = 3
for row, zr in enumerate((0.135, 0.19)):
    for x in np.arange(-0.27, 0.40, 0.045):
        add_prim('cyl', 'ShieldPerf', M['inner'], loc=(x + (0.022 if row else 0), yy+0.066, zr), rot=(math.pi/2, 0, 0), vertices=12, radius=0.009, depth=0.006, coll=col_parts)
for k, zz in enumerate((0.175, 0.175)):
    yk = yy + 0.0 + k*0.0
    ex = add_prim('cyl', 'ExhaustPipe', M['steel'], loc=(-0.40 - k*0.09, yy+0.03, 0.185), rot=(0, math.pi/2, 0), vertices=24, radius=0.035, depth=0.12, coll=col_parts)
    exi = add_prim('cyl', 'ExhaustBore', M['inner'], loc=(-0.46 - k*0.09, yy+0.03, 0.185), rot=(0, math.pi/2, 0), vertices=24, radius=0.029, depth=0.01, coll=col_parts)
# right side plain sill step
add_prim('cube', 'SillStep_R', M['inner'], loc=(0.06, -0.70, 0.17), size=1, scale=(0.7, 0.03, 0.06), coll=col_parts)

# ---------------------------------------------------------------- windscreen + side screens
SCR_BASE_X, SCR_TOP_Z = 0.235, 1.065
def screen_pts(t, level):
    """t in [-1,1] across, level 0 base / 1 top. plan: front arc wrapping back at the ends"""
    halfw = 0.62 - 0.03*level
    y = t*halfw
    wrap = 0.20*(abs(t)**3.2)
    x = SCR_BASE_X - wrap - 0.23*level
    zb = 0.765 - 0.045*abs(t)**2
    zt = SCR_TOP_Z - 0.10*abs(t)**2.4
    z = zb + (zt-zb)*level
    return (x, y, z)
bm = bmesh.new(); grid = []
NU, NV = 40, 6
for i in range(NU+1):
    t = -1 + 2*i/NU
    grid.append([bm.verts.new(screen_pts(t, j/NV)) for j in range(NV+1)])
for i in range(NU):
    for j in range(NV):
        bm.faces.new((grid[i][j], grid[i+1][j], grid[i+1][j+1], grid[i][j+1]))
me = bpy.data.meshes.new('Windscreen'); bm.to_mesh(me); bm.free()
ws = new_obj('Windscreen', me, M['glass'], col_parts); smooth(ws)
ws.modifiers.new('sol', 'SOLIDIFY').thickness = 0.005
# frame: top + sides + base
top = [screen_pts(-1+2*i/40, 1) for i in range(41)]
tube_path('ScreenFrameTop', top, 0.011, M['darkchrome'], col_parts)
for s in (-1, 1):
    tube_path('ScreenPillar', [screen_pts(s, j/6) for j in range(7)], 0.010, M['darkchrome'], col_parts)
tube_path('ScreenFrameBase', [screen_pts(-1+2*i/40, 0.02) for i in range(41)], 0.008, M['darkchrome'], col_parts)
# side screens: from pillar back to door top
for s in (-1, 1):
    p0 = Vector(screen_pts(s, 1)); p0b = Vector(screen_pts(s, 0))
    pts_top = []
    for k in range(13):
        u = k/12
        x = p0.x + (-0.56 - p0.x)*u
        z = p0.z + (0.73 - p0.z)*(u**1.6)
        y = s*(abs(p0.y) - 0.005 - 0.02*u)
        pts_top.append((x, y, z))
    pts_bot = [(p[0], p[1], 0.73 if i > 0 else p0b.z) for i, p in enumerate(pts_top)]
    bm = bmesh.new()
    vt = [bm.verts.new(p) for p in pts_top]; vb = [bm.verts.new((p[0], p[1], 0.715)) for p in pts_top]
    vb[0].co = Vector(p0b)
    for k in range(12):
        try: bm.faces.new((vb[k], vb[k+1], vt[k+1], vt[k]))
        except ValueError: pass
    me = bpy.data.meshes.new('SideScreen'); bm.to_mesh(me); bm.free()
    ss = new_obj('SideScreen', me, M['glass'], col_parts); ss.modifiers.new('sol', 'SOLIDIFY').thickness = 0.004
    tube_path('SideScreenFrame', pts_top, 0.008, M['darkchrome'], col_parts)
    tube_path('SideScreenRear', [pts_top[-2], pts_top[-1], (pts_top[-1][0], pts_top[-1][1], 0.70)], 0.007, M['darkchrome'], col_parts)
# mirror
add_prim('cube', 'MirrorStem', M['chrome'], loc=(SCR_BASE_X-0.21, -0.05, SCR_TOP_Z-0.02), size=1, scale=(0.01, 0.01, 0.05), coll=col_parts)
add_prim('cube', 'Mirror', M['chrome'], loc=(SCR_BASE_X-0.24, -0.05, SCR_TOP_Z-0.06), size=1, scale=(0.012, 0.16, 0.06), coll=col_parts)

# ---------------------------------------------------------------- interior: seats, tunnel, dash, steering wheel, hood bundle
for s in (-1, 1):
    ys = s*0.30
    cush = add_prim('cube', 'SeatCushion', M['leather'], loc=(-0.25, ys, 0.36), size=1, scale=(0.48, 0.44, 0.10), coll=col_int)
    back = add_prim('cube', 'SeatBack', M['leather'], loc=(-0.55, ys, 0.55), rot=(0, math.radians(-14), 0), size=1, scale=(0.10, 0.44, 0.42), coll=col_int)
    for o in (cush, back):
        b_ = o.modifiers.new('bev', 'BEVEL'); b_.width = 0.035; b_.segments = 4
        sd = o.modifiers.new('sub', 'SUBSURF'); sd.levels = 1; sd.render_levels = 2
        smooth(o)
tun = add_prim('cube', 'Tunnel', M['leather'], loc=(-0.1, 0, 0.38), size=1, scale=(0.9, 0.17, 0.14), coll=col_int)
b_ = tun.modifiers.new('bev', 'BEVEL'); b_.width = 0.04; b_.segments = 4
dash = add_prim('cube', 'Dashboard', M['leather'], loc=(0.12, 0, 0.66), size=1, scale=(0.08, 1.1, 0.16), coll=col_int)
b_ = dash.modifiers.new('bev', 'BEVEL'); b_.width = 0.02; b_.segments = 3
for k, yg in enumerate((-0.42, -0.28, -0.12, 0.05, 0.18)):
    add_prim('cyl', 'Gauge', M['gauge'], loc=(0.075, yg, 0.67), rot=(0, math.pi/2, 0), radius=0.045 if k in (1, 2) else 0.03, depth=0.01, coll=col_int)
    add_prim('torus', 'GaugeRing', M['chrome'], loc=(0.07, yg, 0.67), rot=(0, math.pi/2, 0), major_radius=0.046 if k in (1, 2) else 0.031, minor_radius=0.004, coll=col_int)
# steering wheel (RHD -> car's right = -Y)
sw_c = Vector((-0.06, -0.33, 0.76)); tilt = math.radians(60)
rim = add_prim('torus', 'SteeringRim', M['wood'], loc=sw_c, rot=(0, tilt, 0), major_radius=0.20, minor_radius=0.013, major_segments=64, minor_segments=12, coll=col_int)
hubw = add_prim('cyl', 'SteeringHub', M['chrome'], loc=sw_c, rot=(0, tilt, 0), radius=0.035, depth=0.03, coll=col_int)
for k in range(3):
    ang = math.radians(90 + 120*k)
    sp = add_prim('cube', 'SteeringSpoke', M['chrome'], loc=(0, 0, 0), size=1, coll=col_int)
    sp.scale = (0.19, 0.012, 0.004)
    sp.rotation_euler = (0, tilt, 0)
    local = Matrix.Rotation(tilt, 4, 'Y') @ Matrix.Rotation(ang, 4, 'Z')
    sp.matrix_world = Matrix.Translation(sw_c) @ local @ Matrix.Translation((0.10, 0, 0)) @ Matrix.Diagonal((0.19, 0.012, 0.004, 1))
col_ = add_prim('cyl', 'SteeringColumn', M['black'], loc=sw_c + Vector((0.14, 0, -0.07)), rot=(0, tilt, 0), radius=0.018, depth=0.32, coll=col_int)
# folded hood bundle behind seats
loc, nor = hit((-0.86, 0.0, 2.0), (0, 0, -1))
hz = loc.z if loc else 0.70
hood = add_prim('sphere', 'FoldedHood', M['fabric'], loc=(-0.86, 0.02, hz+0.05), segments=48, ring_count=24, radius=1, coll=col_parts)
hood.scale = (0.27, 0.60, 0.17)
lump = add_prim('sphere', 'FoldedHoodRoll', M['fabric'], loc=(-0.80, -0.12, hz+0.10), segments=32, ring_count=16, radius=1, coll=col_parts)
lump.scale = (0.16, 0.40, 0.10)
tex = bpy.data.textures.new('HoodNoise', 'CLOUDS'); tex.noise_scale = 0.10
for hh in (hood, lump):
    hd = hh.modifiers.new('disp', 'DISPLACE'); hd.texture = tex; hd.strength = 0.035
    smooth(hh)
tube_path('HoodPiping', [(-0.66 - 0.02*math.cos(t*math.pi), 0.55*math.cos(t*math.pi), hz+0.05 + 0.12*math.sin(t*math.pi)) for t in [i/20 for i in range(21)]], 0.005, M['leather'], col_parts)
# rear deck cover / tonneau behind seats in leather piping edge
# ---------------------------------------------------------------- luggage rack
deck = []
for x in (-1.02, -1.60):
    for y in (-0.30, 0.30):
        loc, nor = hit((x, y, 2), (0, 0, -1)); deck.append(loc.z if loc else 0.68)
zf = max(deck[0], deck[1]) + 0.035; zr = max(deck[2], deck[3]) + 0.07
for y in (-0.30, 0.30):
    tube_path('RackRail', [(-0.99, y, zf-0.02), (-1.02, y, zf), (-1.60, y, zr), (-1.63, y, zr-0.01)], 0.007, M['chrome'], col_parts)
for k in range(6):
    u = k/5; x = -1.04 + (-1.56+1.04)*u; z = zf + (zr-zf)*u + 0.004
    tube_path('RackSlat', [(x, -0.31, z), (x, 0.31, z)], 0.005, M['chrome'], col_parts)
# rear hoop
tube_path('RackHoop', [(-1.58, -0.30, zr), (-1.57, -0.30, zr+0.10), (-1.57, -0.24, zr+0.14), (-1.57, 0.24, zr+0.14), (-1.57, 0.30, zr+0.10), (-1.58, 0.30, zr)], 0.007, M['chrome'], col_parts)
# fuel filler cap on rear deck (left)
loc, nor = hit((-1.28, 0.52, 2), (0, 0, -1))
if loc:
    fc = add_prim('cyl', 'FuelCap', M['chrome'], loc=loc, radius=0.05, depth=0.03, coll=col_parts); orient_to(fc, nor)

# convert curves to meshes
for o in list(scene.objects):
    if o.type == 'CURVE': to_mesh(o)

# ---------------------------------------------------------------- studio
def studio():
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0)); fl = bpy.context.active_object; fl.name = 'StudioFloor'
    m = bpy.data.materials.new('StripedFloor'); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N['Principled BSDF']; b.inputs['Roughness'].default_value = 0.3
    tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, math.radians(35))
    L.new(tc.outputs['Object'], mp.inputs[0])
    wv = N.new('ShaderNodeTexWave'); wv.wave_profile = 'SAW'; wv.inputs['Scale'].default_value = 0.35; wv.inputs['Distortion'].default_value = 0
    L.new(mp.outputs[0], wv.inputs[0])
    cr = N.new('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'
    cr.color_ramp.elements[0].color = (0.45, 0.47, 0.48, 1); cr.color_ramp.elements[1].position = 0.5; cr.color_ramp.elements[1].color = (0.06, 0.065, 0.07, 1)
    L.new(wv.outputs['Fac'], cr.inputs[0]); L.new(cr.outputs[0], b.inputs['Base Color'])
    fl.data.materials.append(m)
    # back walls (white block wall)
    wm = bpy.data.materials.new('BlockWall'); wm.use_nodes = True; N = wm.node_tree.nodes; L = wm.node_tree.links
    b = N['Principled BSDF']; b.inputs['Roughness'].default_value = 0.6
    br = N.new('ShaderNodeTexBrick'); br.inputs['Color1'].default_value = (0.85, 0.86, 0.86, 1); br.inputs['Color2'].default_value = (0.82, 0.83, 0.83, 1)
    br.inputs['Mortar'].default_value = (0.62, 0.63, 0.63, 1); br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = 0.006
    br.offset = 0.5; br.inputs['Brick Width'].default_value = 0.44; br.inputs['Row Height'].default_value = 0.22
    tc = N.new('ShaderNodeTexCoord'); L.new(tc.outputs['Object'], br.inputs['Vector']); L.new(br.outputs['Color'], b.inputs['Base Color'])
    for nm, loc, rot in [('WallBack', (0, -5.0, 3), (math.pi/2, 0, 0)), ('WallSide', (-7.5, 0, 3), (math.pi/2, 0, math.pi/2)), ('WallFront', (9, 0, 3), (math.pi/2, 0, math.pi/2)), ('WallLeft', (0, 13, 3), (math.pi/2, 0, 0))]:
        bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); w = bpy.context.active_object; w.name = nm; w.scale = (30, 6, 1)
        w.data.materials.append(wm)
    # lights: big soft overhead + side fills
    for nm, loc, rot, size, en in [('KeyTop', (0, 0, 4.8), (0, 0, 0), (8, 4), 650), ('FillLeft', (0, 4.5, 4.2), (math.radians(-28), 0, 0), (7, 1.5), 140),
                                   ('FillRight', (0, -4, 4.0), (math.radians(30), 0, 0), (6, 1.5), 120), ('Rim', (-4, 0, 2.5), (0, math.radians(-60), 0), (2, 3), 300),
                                   ('FrontFill', (6, 0, 2.2), (0, math.radians(65), 0), (3, 1.5), 220)]:
        ld = bpy.data.lights.new(nm, 'AREA'); ld.shape = 'RECTANGLE'; ld.size, ld.size_y = size; ld.energy = en
        lo = bpy.data.objects.new(nm, ld); scene.collection.objects.link(lo); lo.location = loc; lo.rotation_euler = rot
        if nm in ('KeyTop', 'FrontFill'): lo.visible_glossy = False
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 5.5)); cl = bpy.context.active_object; cl.name = 'WallCeiling'; cl.scale = (30, 30, 1)
    cm = mat('Ceiling', (0.25, 0.26, 0.26), 0.0, 0.8); cl.data.materials.append(cm)
    w = bpy.data.worlds.new('World'); scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.8, 0.82, 0.83, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
studio()

# ---------------------------------------------------------------- cameras (fixed across rounds)
CAMS_DEF = {
  # name: (location, look-at, focal mm, aspect w/h, ref file)
  'side':   ((-0.065, 10.6, 1.05), (-0.065, 0.715, 0.67), 89.0, 2166/1026, 'side.jpg'),
  'front':  ((8.0, 0.0, 1.0), (1.66, 0.0, 0.523), 109.0, 1838/1224, 'front.jpg'),
  'rear34': ((-4.0, 4.4, 1.15), (-0.40, 0.10, 0.48), 48.0, 1796/982, 'rear34.jpg'),
  'hero':   ((5.6, 4.4, 1.35), (0.15, 0.0, 0.50), 55.0, 1600/1000, None),
}
for nm, (loc, tgt, f, asp, ref) in CAMS_DEF.items():
    cd = bpy.data.cameras.new('Cam_'+nm); cd.lens = f; cd.sensor_width = 36
    co = bpy.data.objects.new('Cam_'+nm, cd); scene.collection.objects.link(co); co.location = loc
    d = Vector(tgt) - Vector(loc); co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

# ---------------------------------------------------------------- render settings
scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True; scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.view_settings.view_transform = 'AgX'; scene.view_settings.look = 'AgX - Medium High Contrast'
scene.cycles.max_bounces = 8; scene.cycles.transmission_bounces = 8
scene.render.image_settings.file_format = 'PNG'

# stats
tris = 0; meshes = 0
dg = bpy.context.evaluated_depsgraph_get()
for o in scene.objects:
    if o.type == 'MESH' and not o.name.startswith(('Studio', 'Wall')):
        meshes += 1
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        me.calc_loop_triangles(); tris += len(me.loop_triangles); ev.to_mesh_clear()
stats = dict(round=ROUND, meshes=meshes, triangles_viewport=tris, rivets=rv_count)
print('STATS', json.dumps(stats))
json.dump(stats, open(OUT+f'/stats_r{ROUND}.json', 'w'))

bpy.ops.wm.save_as_mainfile(filepath=OUT+f'/xkss_r{ROUND}.blend')
if not NORENDER:
    for nm in CAMS:
        loc, tgt, f, asp, ref = CAMS_DEF[nm]
        scene.camera = bpy.data.objects['Cam_'+nm]
        scene.render.resolution_x = RES; scene.render.resolution_y = int(RES/asp)
        scene.render.filepath = OUT+f'/renders/r{ROUND}_{nm}.png'
        bpy.ops.render.render(write_still=True)
        print('RENDERED', nm)
