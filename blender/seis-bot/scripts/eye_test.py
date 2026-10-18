import bpy, sys, bmesh
from mathutils import Vector as V
argv = sys.argv[sys.argv.index('--') + 1:]
var, out = argv[0], argv[1]
sc = bpy.context.scene
def mat_orb(strength):
    m = bpy.data.materials.new('Eye_Orb_T'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); p = nt.nodes.new('ShaderNodeBsdfPrincipled')
    lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.4
    cr = nt.nodes.new('ShaderNodeValToRGB'); el = cr.color_ramp.elements
    el[0].position = 0; el[0].color = (1, 0, 0, 1); el[1].position = 1; el[1].color = (0.02, 0, 0, 1)
    e = el.new(0.45); e.color = (0.35, 0, 0, 1)
    nt.links.new(lw.outputs['Facing'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], p.inputs['Emission Color'])
    p.inputs['Emission Strength'].default_value = strength
    p.inputs['Base Color'].default_value = (0.03, 0, 0, 1); p.inputs['Roughness'].default_value = 0.25
    nt.links.new(p.outputs[0], o.inputs[0]); return m
def mat_em(name, col, s):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = s
    nt.links.new(e.outputs[0], o.inputs[0]); return m
ostr, cstr, glare = {'A': (1.2, 30, 1), 'B': (2.0, 30, 1), 'C': (5, 40, 1)}[var[0]]
orb = mat_orb(ostr); core = mat_em('Eye_CoreT', (1, 0.55, 0.45), cstr)
if var.endswith('S'):
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'Medium High Contrast'; sc.view_settings.exposure = -1.0
for s in ('L', 'R'):
    eo = bpy.data.objects['Head_Eye.' + s]
    eo.data.materials.clear(); eo.data.materials.append(orb)
    c = eo.matrix_world @ (sum((v.co for v in eo.data.vertices), V()) / len(eo.data.vertices))
    co = eo.copy(); co.data = eo.data.copy(); co.name = 'Head_EyeCore.' + s; eo.users_collection[0].objects.link(co)
    co.data.materials.clear(); co.data.materials.append(core)
    lc = sum((v.co for v in co.data.vertices), V()) / len(co.data.vertices)
    ymin = min(v.co.y for v in co.data.vertices)
    for v in co.data.vertices:
        v.co = lc + (v.co - lc) * 0.42 + V((0, (ymin - lc.y) * 0.78, 0))
if glare:
    sc.use_nodes = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new('CompositorNodeRLayers'); g = nt.nodes.new('CompositorNodeGlare'); cp = nt.nodes.new('CompositorNodeComposite')
    g.glare_type = 'FOG_GLOW'; g.quality = 'HIGH'; g.threshold = 4.0; g.size = 7; g.mix = 0.0
    nt.links.new(rl.outputs['Image'], g.inputs['Image']); nt.links.new(g.outputs['Image'], cp.inputs['Image'])
arm = bpy.data.objects['RobotRig']; arm.animation_data.action = bpy.data.actions['Standing']; sc.frame_set(1)
for p in bpy.data.objects:
    if p.name.startswith('Pedestal'): p.hide_render = True
sc.camera = bpy.data.objects['Cam_HeadFront']
sc.render.resolution_x = 1200; sc.render.resolution_y = 1500; sc.render.resolution_percentage = 50
sc.render.use_border = True; sc.render.border_min_x = 0.2; sc.render.border_max_x = 0.8; sc.render.border_min_y = 0.35; sc.render.border_max_y = 0.75
sc.render.use_crop_to_border = True
sc.cycles.samples = 24; sc.render.threads_mode = 'FIXED'; sc.render.threads = 8
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
