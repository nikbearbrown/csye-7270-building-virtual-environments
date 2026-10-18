# blender -b robot_standing.blend -P bake.py -- [scale]
# Bakes the procedural materials (base colour, ORM = occlusion/roughness/metallic, tangent normal) into texture atlases,
# swaps in glTF-ready image materials and saves robot_baked.blend (used by export_glb.py).
import bpy, sys, os, time
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SCALE = float(argv[0]) if argv else 1.0
ONLY = argv[1].split(',') if len(argv) > 1 else None
OUT = '/workspace/robot/v4'; TEX = os.path.join(OUT, 'textures')
SIZES = {'Armor_Gunmetal': 2048, 'Armor_Gunmetal_B': 2048, 'Mech_Dark': 2048, 'Muscle_Red': 2048, 'Face_Silver': 2048,
         'Paint_Red': 1024, 'Bronze_Worn': 1024, 'Socket_Black': 1024, 'Decal_White': 512, 'Armor_Gunmetal_Flat': 1024}
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(os.environ.get('BT', '8'))
sc.render.bake.margin = 6; sc.render.bake.use_selected_to_active = False; sc.render.bake.target = 'IMAGE_TEXTURES'
arm = bpy.data.objects['RobotRig']
arm.animation_data.action = bpy.data.actions['Standing']; sc.frame_set(1)
robot = [o for o in bpy.data.objects if o.type == 'MESH' and o.parent == arm]
groups = {}
for o in robot:
    groups.setdefault(o.material_slots[0].material.name, []).append(o)
print('GROUPS', {k: len(v) for k, v in groups.items()})

def select_only(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]

def new_img(name, size, noncolor):
    img = bpy.data.images.new(name, size, size, alpha=False)
    img.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    return img

def src(sock):
    return sock.links[0].from_socket if sock.is_linked else None

t0 = time.time()
baked = {}
for mname, objs in groups.items():
    if mname not in SIZES or (ONLY and mname not in ONLY): continue
    size = max(256, int(SIZES[mname] * SCALE))
    mat = bpy.data.materials[mname]; nt = mat.node_tree; N = nt.nodes; L = nt.links
    # --- UV atlas shared by every object of this material
    for o in objs:
        while o.data.uv_layers: o.data.uv_layers.remove(o.data.uv_layers[0])
        o.data.uv_layers.new(name='UVMap')
    select_only(objs)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.0015, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    print('UV', mname, 't=%.0fs' % (time.time() - t0), flush=True)
    main = N['MAIN']; out = [n for n in N if n.type == 'OUTPUT_MATERIAL'][0]
    orig = src(out.inputs['Surface'])
    em = N.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.0
    imgn = N.new('ShaderNodeTexImage'); N.active = imgn
    res = {}
    for kind in ('color', 'orm', 'normal'):
        img = new_img('%s_%s' % (mname, kind), size, kind != 'color'); imgn.image = img
        for l in list(out.inputs['Surface'].links): L.remove(l)
        if kind == 'color':
            s = src(main.inputs['Base Color'])
            if s: L.new(s, em.inputs['Color'])
            else: em.inputs['Color'].default_value = main.inputs['Base Color'].default_value
            L.new(em.outputs[0], out.inputs['Surface']); btype = 'EMIT'
        elif kind == 'orm':
            cc = N.new('ShaderNodeCombineColor'); cc.inputs[0].default_value = 1.0
            for i, nm in ((1, 'Roughness'), (2, 'Metallic')):
                s = src(main.inputs[nm])
                if s: L.new(s, cc.inputs[i])
                else: cc.inputs[i].default_value = main.inputs[nm].default_value
            for l in list(em.inputs['Color'].links): L.remove(l)
            L.new(cc.outputs[0], em.inputs['Color']); L.new(em.outputs[0], out.inputs['Surface']); btype = 'EMIT'
        else:
            L.new(orig, out.inputs['Surface']); btype = 'NORMAL'
        select_only(objs)
        bpy.ops.object.bake(type=btype, normal_space='TANGENT') if btype == 'NORMAL' else bpy.ops.object.bake(type=btype)
        img.filepath_raw = os.path.join(TEX, '%s_%s.%s' % (mname, kind, 'png' if kind == 'normal' else 'jpg'))
        img.file_format = 'PNG' if kind == 'normal' else 'JPEG'
        sc.render.image_settings.quality = 88
        img.save()
        res[kind] = img
        print('BAKED', mname, kind, size, 'objs', len(objs), 't=%.0fs' % (time.time() - t0), flush=True)
    for l in list(out.inputs['Surface'].links): L.remove(l)
    L.new(orig, out.inputs['Surface'])
    N.remove(em); N.remove(imgn)
    baked[mname] = res

# --- glTF-ready materials using the baked maps
def gltf_mat(mname, res):
    m = bpy.data.materials.new('GLB_' + mname); m.use_nodes = True
    N = m.node_tree.nodes; L = m.node_tree.links; p = N['Principled BSDF']
    c = N.new('ShaderNodeTexImage'); c.image = res['color']; L.new(c.outputs['Color'], p.inputs['Base Color'])
    o = N.new('ShaderNodeTexImage'); o.image = res['orm']; o.image.colorspace_settings.name = 'Non-Color'
    sp = N.new('ShaderNodeSeparateColor'); L.new(o.outputs['Color'], sp.inputs[0])
    L.new(sp.outputs[1], p.inputs['Roughness']); L.new(sp.outputs[2], p.inputs['Metallic'])
    n = N.new('ShaderNodeTexImage'); n.image = res['normal']; n.image.colorspace_settings.name = 'Non-Color'
    nm = N.new('ShaderNodeNormalMap'); L.new(n.outputs['Color'], nm.inputs['Color']); L.new(nm.outputs['Normal'], p.inputs['Normal'])
    return m
def emis_mat(mname, col, strength):
    m = bpy.data.materials.new('GLB_' + mname); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*col, 1); p.inputs['Emission Color'].default_value = (*col, 1)
    p.inputs['Emission Strength'].default_value = strength; p.inputs['Roughness'].default_value = 0.2
    return m
rep = {k: gltf_mat(k, v) for k, v in baked.items()}
rep['Eye_Glow'] = emis_mat('Eye_Glow', (1.0, 0.006, 0.003), 2.5)
rep['Eye_Core'] = emis_mat('Eye_Core', (1.0, 0.05, 0.025), 5.0)
for o in robot:
    for s in o.material_slots:
        if s.material and s.material.name in rep: s.material = rep[s.material.name]
for img in bpy.data.images:
    if img.filepath_raw: img.filepath = img.filepath_raw; img.reload()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'robot_baked.blend'))
print('BAKE_DONE t=%.0fs' % (time.time() - t0))
