# v2 procedural materials: one Principled BSDF per material with layered inputs (bakeable)
import bpy

class NB:
    def __init__(self, mat):
        self.nt = mat.node_tree; self.n = self.nt.nodes; self.l = self.nt.links
    def node(self, t, **kw):
        nd = self.n.new(t)
        inputs = kw.pop('inputs', {})
        for k, v in kw.items(): setattr(nd, k, v)
        for k, v in inputs.items(): nd.inputs[k].default_value = v
        return nd
    def link(self, a, b): self.l.new(a, b)
    def _set(self, sock, v):
        if isinstance(v, (int, float)): sock.default_value = v
        elif isinstance(v, tuple): sock.default_value = (*v, 1.0) if len(v) == 3 else v
        else: self.link(v, sock)
    def math(self, op, a, b=None, clamp=False):
        m = self.node('ShaderNodeMath', operation=op, use_clamp=clamp)
        for i, v in enumerate((a, b)):
            if v is not None: self._set(m.inputs[i], v)
        return m.outputs[0]
    def maprange(self, v, a, b, c=0.0, d=1.0):
        m = self.node('ShaderNodeMapRange', clamp=True)
        self._set(m.inputs['Value'], v)
        m.inputs['From Min'].default_value = a; m.inputs['From Max'].default_value = b
        m.inputs['To Min'].default_value = c; m.inputs['To Max'].default_value = d
        return m.outputs[0]
    def mixc(self, fac, a, b):
        m = self.node('ShaderNodeMix', data_type='RGBA', blend_type='MIX', clamp_result=True)
        self._set(m.inputs[0], fac); self._set(m.inputs[6], a); self._set(m.inputs[7], b)
        return m.outputs[2]
    def mixf(self, fac, a, b):
        m = self.node('ShaderNodeMix', data_type='FLOAT', clamp_result=True)
        self._set(m.inputs[0], fac); self._set(m.inputs[2], a); self._set(m.inputs[3], b)
        return m.outputs[0]
    def noise(self, vec, scale, detail=6, rough=0.6, dist=0.0):
        n = self.node('ShaderNodeTexNoise', inputs={'Scale': scale, 'Detail': detail, 'Roughness': rough, 'Distortion': dist})
        self.link(vec, n.inputs['Vector']); return n.outputs['Fac']
    def vor(self, vec, scale, feature='F1'):
        n = self.node('ShaderNodeTexVoronoi', feature=feature, inputs={'Scale': scale})
        self.link(vec, n.inputs['Vector']); return n.outputs['Distance']

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes.clear()
    return m, NB(m)

def masks(b, seed=0.0, edge_amt=1.0, bake_safe=False):
    tc = b.node('ShaderNodeTexCoord')
    vm = b.node('ShaderNodeVectorMath', operation='ADD', inputs={1: (seed, seed * 1.7, seed * 0.3)})
    b.link(tc.outputs['Object'], vm.inputs[0]); co = vm.outputs[0]
    geo = b.node('ShaderNodeNewGeometry')
    bev = b.node('ShaderNodeBevel', samples=8, inputs={'Radius': 0.010})
    dot = b.node('ShaderNodeVectorMath', operation='DOT_PRODUCT')
    b.link(bev.outputs['Normal'], dot.inputs[0]); b.link(geo.outputs['Normal'], dot.inputs[1])
    edge = b.maprange(b.math('SUBTRACT', 1.0, dot.outputs['Value']), 0.004, 0.05)
    edge = b.math('MAXIMUM', edge, b.maprange(geo.outputs['Pointiness'], 0.53, 0.62))
    n1 = b.noise(co, 14.0, 12, 0.7); n2 = b.noise(co, 55.0, 8, 0.6)
    brk = b.math('ADD', b.math('MULTIPLY', n1, 0.75), b.math('MULTIPLY', n2, 0.35))
    wear = b.maprange(b.math('ADD', b.math('MULTIPLY', edge, 1.4 * edge_amt), b.math('MULTIPLY', b.math('SUBTRACT', brk, 0.58), min(1.0, edge_amt + 0.3))), 0.2, 0.36)
    # scratches: wiggly noise cracks + brushed streaks
    cn = b.noise(co, 5.0, 10, 0.62, dist=0.4)
    crack = b.maprange(b.math('ABSOLUTE', b.math('SUBTRACT', cn, 0.5)), 0.0, 0.005, 1.0, 0.0)
    crack = b.math('MULTIPLY', crack, b.maprange(b.noise(co, 3.0, 4, 0.5), 0.5, 0.64))
    sc = b.node('ShaderNodeVectorMath', operation='MULTIPLY', inputs={1: (1.0, 1.0, 0.15)}); b.link(co, sc.inputs[0])
    streak = b.math('MULTIPLY', b.maprange(b.noise(sc.outputs[0], 110.0, 3, 0.5), 0.67, 0.74), b.maprange(b.noise(co, 3.0, 3, 0.5), 0.42, 0.6))
    scratch = b.math('MAXIMUM', crack, streak)
    ao = b.node('ShaderNodeAmbientOcclusion', samples=8, only_local=True, inputs={'Distance': 0.035})
    grime = b.math('MULTIPLY', b.maprange(ao.outputs['AO'], 0.97, 0.45), b.maprange(b.noise(co, 9.0, 6, 0.6), 0.3, 0.7, 0.6, 1.0))
    smudge = b.math('MULTIPLY', b.maprange(b.noise(co, 6.0, 8, 0.7), 0.55, 0.75, 0.0, 0.5), b.maprange(ao.outputs['AO'], 1.0, 0.75))
    grime = b.math('MAXIMUM', grime, smudge)
    dents = b.vor(co, 18.0, 'SMOOTH_F1')
    hgt = b.math('SUBTRACT', b.math('ADD', b.math('MULTIPLY', dents, 0.6), b.math('MULTIPLY', n2, 0.25)), b.math('MULTIPLY', scratch, 0.4))
    bump = b.node('ShaderNodeBump', inputs={'Strength': 0.12, 'Distance': 0.002}); b.link(hgt, bump.inputs['Height'])
    return dict(co=co, edge=edge, wear=wear, scratch=scratch, grime=grime, bump=bump.outputs['Normal'], n1=n1, n2=n2)

def finish(b, p):
    out = b.node('ShaderNodeOutputMaterial', target='ALL'); b.link(p.outputs[0], out.inputs['Surface'])

def principled(b, color, metal, rough, normal=None, coat=0.0, coat_r=0.05, aniso=0.0, emis=None, emis_s=0.0):
    p = b.node('ShaderNodeBsdfPrincipled'); p.name = 'MAIN'
    b._set(p.inputs['Base Color'], color); b._set(p.inputs['Metallic'], metal); b._set(p.inputs['Roughness'], rough)
    p.inputs['Coat Weight'].default_value = coat; p.inputs['Coat Roughness'].default_value = coat_r
    p.inputs['Anisotropic'].default_value = aniso
    if normal is not None: b.link(normal, p.inputs['Normal'])
    if emis is not None:
        b._set(p.inputs['Emission Color'], emis); p.inputs['Emission Strength'].default_value = emis_s
    return p

def gunmetal(name, base=(0.035, 0.07, 0.07), base2=(0.065, 0.118, 0.115), seed=0.0, bronze_amt=0.35, edge_amt=1.0, wear_mix=1.0):
    m, b = new_mat(name); W = masks(b, seed, edge_amt)
    col = b.mixc(W['n1'], base, base2)
    steel = b.mixc(W['n2'], (0.34, 0.35, 0.36), (0.55, 0.56, 0.57))
    bronze = b.mixc(W['n2'], (0.33, 0.25, 0.14), (0.52, 0.42, 0.27))
    bmask = b.maprange(b.noise(W['co'], 2.5, 5, 0.6), 0.5, 0.62, 0.0, bronze_amt * 2)
    wearcol = b.mixc(bmask, steel, bronze)
    col = b.mixc(b.math('MULTIPLY', W['wear'], wear_mix), col, wearcol)
    col = b.mixc(b.math('MULTIPLY', W['scratch'], 0.35), col, (0.36, 0.37, 0.37))
    col = b.mixc(W['grime'], col, (0.018, 0.014, 0.01))
    rough = b.maprange(W['n2'], 0.2, 0.8, 0.26, 0.46)
    rough = b.math('ADD', rough, b.math('MULTIPLY', W['grime'], 0.45))
    rough = b.math('ADD', rough, b.maprange(b.noise(W['co'], 1.5, 4, 0.5), 0.4, 0.7, -0.06, 0.14))
    rough = b.mixf(b.math('MULTIPLY', W['wear'], wear_mix), rough, 0.3)
    metal = b.mixf(W['grime'], 0.95, 0.55)
    finish(b, principled(b, col, metal, rough, W['bump'], coat=0.25, coat_r=0.12))
    return m

def silver(name, seed=7.0):
    m, b = new_mat(name); W = masks(b, seed, 0.8)
    col = b.mixc(W['n1'], (0.30, 0.315, 0.325), (0.45, 0.465, 0.475))
    col = b.mixc(b.maprange(W['n2'], 0.55, 0.75, 0, 0.55), col, (0.24, 0.22, 0.18))
    col = b.mixc(b.math('MULTIPLY', W['scratch'], 0.5), col, (0.72, 0.72, 0.73))
    col = b.mixc(b.math('MULTIPLY', W['grime'], 1.2), col, (0.03, 0.025, 0.02))
    rough = b.math('ADD', b.maprange(W['n2'], 0.2, 0.8, 0.27, 0.44), b.math('MULTIPLY', W['grime'], 0.35))
    finish(b, principled(b, col, b.mixf(W['grime'], 1.0, 0.6), rough, W['bump'], aniso=0.3))
    return m

def bronze(name, seed=17.0):
    m, b = new_mat(name); W = masks(b, seed, 0.9)
    col = b.mixc(W['n1'], (0.26, 0.22, 0.15), (0.42, 0.36, 0.25))
    col = b.mixc(W['wear'], col, (0.62, 0.55, 0.42))
    col = b.mixc(W['grime'], col, (0.02, 0.016, 0.01))
    rough = b.math('ADD', b.maprange(W['n2'], 0.2, 0.8, 0.25, 0.45), b.math('MULTIPLY', W['grime'], 0.35))
    finish(b, principled(b, col, 0.95, rough, W['bump']))
    return m

def muscle(name, seed=3.0):
    m, b = new_mat(name); W = masks(b, seed, 0.6)
    wave = b.node('ShaderNodeTexWave', wave_type='BANDS', bands_direction='Z', inputs={'Scale': 30.0, 'Distortion': 6.0, 'Detail': 4.0})
    b.link(W['co'], wave.inputs['Vector'])
    col = b.mixc(W['n1'], (0.17, 0.006, 0.012), (0.30, 0.018, 0.024))
    col = b.mixc(b.math('MULTIPLY', wave.outputs['Fac'], 0.35), col, (0.09, 0.004, 0.008))
    col = b.mixc(b.math('MULTIPLY', W['wear'], 0.6), col, (0.08, 0.03, 0.03))
    col = b.mixc(W['grime'], col, (0.03, 0.006, 0.006))
    rough = b.math('ADD', b.maprange(W['n2'], 0.2, 0.8, 0.2, 0.4), b.math('MULTIPLY', W['grime'], 0.4))
    bump = b.node('ShaderNodeBump', inputs={'Strength': 0.2, 'Distance': 0.002})
    b.link(wave.outputs['Fac'], bump.inputs['Height']); b.link(W['bump'], bump.inputs['Normal'])
    finish(b, principled(b, col, 0.0, rough, bump.outputs['Normal'], coat=0.6, coat_r=0.08))
    return m

def red_paint(name, seed=4.0):
    m, b = new_mat(name); W = masks(b, seed, 0.9)
    col = b.mixc(W['n1'], (0.25, 0.008, 0.008), (0.40, 0.018, 0.014))
    chip = b.maprange(b.math('ADD', W['wear'], b.math('MULTIPLY', b.maprange(b.noise(W['co'], 11.0, 10, 0.75), 0.6, 0.66), 0.8)), 0.2, 0.7)
    under = b.mixc(W['n2'], (0.05, 0.06, 0.065), (0.45, 0.46, 0.47))
    col = b.mixc(chip, col, under)
    col = b.mixc(W['grime'], col, (0.04, 0.01, 0.006))
    rough = b.mixf(chip, b.math('ADD', b.maprange(W['n2'], 0.3, 0.75, 0.08, 0.28), b.math('MULTIPLY', W['grime'], 0.4)), 0.35)
    finish(b, principled(b, col, b.mixf(chip, 0.0, 0.9), rough, W['bump'], coat=0.85, coat_r=0.04))
    return m

def dark(name, seed=11.0):
    return gunmetal(name, base=(0.012, 0.014, 0.015), base2=(0.025, 0.028, 0.03), seed=seed, bronze_amt=0.2)

def groove(name):
    m, b = new_mat(name)
    finish(b, principled(b, (0.008, 0.009, 0.009), 0.3, 0.7))
    return m

def eye_orb(name, strength=1.6):
    """Deep red orb: hot white-red core where it faces the viewer, dark red falloff at grazing angles."""
    m, b = new_mat(name)
    lw = b.node('ShaderNodeLayerWeight', inputs={'Blend': 0.4})
    cr = b.node('ShaderNodeValToRGB')
    el = cr.color_ramp.elements
    el[0].position = 0.0; el[0].color = (1.0, 0.0, 0.0, 1)
    el[1].position = 1.0; el[1].color = (0.02, 0.0, 0.0, 1)
    e2 = el.new(0.45); e2.color = (0.35, 0.0, 0.0, 1)
    
    b.link(lw.outputs['Facing'], cr.inputs['Fac'])
    p = principled(b, (0.05, 0.0, 0.0), 0.0, 0.45)
    b.link(cr.outputs['Color'], p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value = strength
    p.inputs['Specular IOR Level'].default_value = 0.1
    finish(b, p)
    return m

def emissive(name, color=(1.0, 0.02, 0.01), strength=12.0):
    m, b = new_mat(name)
    finish(b, principled(b, (0.6, 0.02, 0.01), 0.0, 0.2, emis=color, emis_s=strength))
    return m

def decal_white(name):
    m, b = new_mat(name); W = masks(b, 21.0, 0.6)
    col = b.mixc(b.math('MULTIPLY', W['grime'], 0.45), (0.88, 0.87, 0.82), (0.3, 0.26, 0.2))
    col = b.mixc(b.math('MULTIPLY', W['scratch'], 0.6), col, (0.1, 0.1, 0.1))
    finish(b, principled(b, col, 0.0, 0.32, W['bump'], coat=0.5))
    return m

def stone(name):
    m, b = new_mat(name)
    tc = b.node('ShaderNodeTexCoord'); co = tc.outputs['Object']
    n1 = b.noise(co, 5.0, 8, 0.6); n2 = b.noise(co, 120.0, 4, 0.7)
    pits = b.maprange(b.vor(co, 90.0), 0.0, 0.12, 1.0, 0.0)
    col = b.mixc(n1, (0.30, 0.27, 0.22), (0.44, 0.40, 0.33))
    col = b.mixc(b.math('MULTIPLY', pits, 0.6), col, (0.16, 0.14, 0.12))
    bump = b.node('ShaderNodeBump', inputs={'Strength': 0.35, 'Distance': 0.003})
    b.link(b.math('SUBTRACT', b.math('MULTIPLY', n2, 0.5), b.math('MULTIPLY', pits, 0.6)), bump.inputs['Height'])
    finish(b, principled(b, col, 0.0, 0.85, bump.outputs['Normal']))
    return m

def backdrop(name):
    m, b = new_mat(name); finish(b, principled(b, (0.3, 0.3, 0.3), 0.0, 0.7)); return m

def build_all():
    M = {}
    M['teal'] = gunmetal('Armor_Gunmetal')
    M['teal2'] = gunmetal('Armor_Gunmetal_B', base=(0.034, 0.044, 0.048), base2=(0.06, 0.074, 0.08), seed=5.0)
    M['tealflat'] = gunmetal('Armor_Gunmetal_Flat', seed=9.0, bronze_amt=0.1, edge_amt=0.15, wear_mix=0.1)
    M['dark'] = dark('Mech_Dark')
    M['black'] = dark('Socket_Black', seed=13.0)
    M['red'] = red_paint('Paint_Red')
    M['muscle'] = muscle('Muscle_Red')
    M['silver'] = silver('Face_Silver')
    M['bronze'] = bronze('Bronze_Worn')
    M['eye'] = eye_orb('Eye_Glow', 1.2)
    M['eyecore'] = emissive('Eye_Core', (1.0, 0.72, 0.66), 40.0)
    M['eyeglow'] = eye_orb('Eye_SocketGlow', 0.6)
    M['white'] = decal_white('Decal_White')
    M['groove'] = groove('Panel_Groove')
    M['concrete'] = stone('Stone_Plinth')
    M['backdrop'] = backdrop('Backdrop')
    return M
