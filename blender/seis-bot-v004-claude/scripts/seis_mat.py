"""seis_mat - the SEIS bot materials (Blender 5.1, Cycles-first node trees).  ON-MODEL version (2026-10-18):
clean glossy blue-teal gunmetal with thin champagne-gold trim lines, per spec/ONMODEL.md section 2 (Bear's 12 video frames).

Names every part module may use with seis_lib.finish(obj, "<name>") / seis_lib.mat("<name>"):
    teal      glossy blue-teal gunmetal paint (the armour).  Thin champagne-gold trim line on bevelled edges.
    bronze    clean olive-gold metal for bands, bezels, arch faces, rib blades, spine bars (alias: gold_band)
    gold      bright champagne-gold for thin trim pieces, bezel lines, stripes
    red       candy-red lacquer (eye lenses, throat, ab pods, arm windows, leg lens plates)
    silver    warm pewter satin metal (head, collar fork and pads, muzzle)
    gunmetal  near-black olive gunmetal (hands, wrist rings, dish interiors)
    dark      black matte rubber / voids / cavities
    darkdisc  the dark speaker / elbow / hub discs (olive-black)
    white     glossy white enamel (the "6")
    eye       red glowing eye lens        eyecore  the small hot spot in the eye
    stone     limestone plinth (alias: concrete)        dais  pale cream slab under the plinth
    backdrop  the white-grey seamless (QA renders)
TRIM CONTROL: the teal material reads the object's custom property "wear" (default 1.0) as the GOLD TRIM strength:
    obj["wear"] = 0.0  -> no gold line on this object's edges (e.g. the chest plates: groove + white glint only)
    obj["wear"] = 1.0  -> thin gold line on every bevelled edge.   L.finish(obj, "teal", wear=0.0) sets it.
There is NO craquelure, chipping or bronze reveal: the on-model frames are clean paint.  Gold lines follow BEVELS (the
Bevel node), so an edge that should catch gold needs a real bevel of >= 0.0015 m.
Object-space texture coordinates are used, so patterns ride with a part when it is posed.
"""
import bpy


def hexlin(h, a=1.0):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b), a)


# measured from Bear's video frames (spec/ONMODEL.md section 2)
C_TEAL = hexlin("#122F36")
C_TEAL_SHEEN = hexlin("#1D4650")
C_GOLD_TRIM = hexlin("#C2A266")
C_GOLD_LIGHT = hexlin("#CDB178")
C_BAND = hexlin("#8A7344")
C_BAND_SHADE = hexlin("#604A20")
C_RED = hexlin("#A0061A")
C_RED_DEEP = hexlin("#59010B")
C_SILVER = hexlin("#8F8A78")
C_GUNMETAL = hexlin("#1A1F18")
C_DARK = hexlin("#070704")
C_DARKDISC = hexlin("#1F251E")
C_WHITE = hexlin("#E0E0E0")
C_STONE = hexlin("#86846C")
C_DAIS = hexlin("#CFC8BE")
C_BACKDROP = hexlin("#E3E3E1")


class _NB:
    def __init__(self, nt):
        self.nt = nt
        self.x = -1200
        self.y = 0

    def n(self, kind, **props):
        node = self.nt.nodes.new(kind)
        for k, v in props.items():
            setattr(node, k, v)
        node.location = (self.x, self.y)
        self.x += 190
        return node

    def math(self, op, a=None, b=None, clamp=False):
        m = self.n("ShaderNodeMath", operation=op, use_clamp=clamp)
        for idx, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[idx].default_value = v
            else:
                self.nt.links.new(v, m.inputs[idx])
        return m.outputs[0]

    def maprange(self, val, a0, a1, b0=0.0, b1=1.0, clamp=True):
        m = self.n("ShaderNodeMapRange")
        m.clamp = clamp
        if isinstance(val, (int, float)):
            m.inputs["Value"].default_value = val
        else:
            self.nt.links.new(val, m.inputs["Value"])
        m.inputs["From Min"].default_value = a0
        m.inputs["From Max"].default_value = a1
        m.inputs["To Min"].default_value = b0
        m.inputs["To Max"].default_value = b1
        return m.outputs["Result"]

    def mixc(self, fac, a, b):
        m = self.n("ShaderNodeMix", data_type="RGBA", blend_type="MIX")
        ids = {s.identifier: s for s in m.inputs}
        for key, v in (("Factor_Float", fac), ("A_Color", a), ("B_Color", b)):
            s = ids[key]
            if isinstance(v, (int, float, tuple, list)):
                s.default_value = v
            else:
                self.nt.links.new(v, s)
        return [o for o in m.outputs if o.identifier == "Result_Color"][0]

    def mixf(self, fac, a, b):
        m = self.n("ShaderNodeMix", data_type="FLOAT", blend_type="MIX")
        ids = {s.identifier: s for s in m.inputs}
        for key, v in (("Factor_Float", fac), ("A_Float", a), ("B_Float", b)):
            s = ids[key]
            if isinstance(v, (int, float)):
                s.default_value = v
            else:
                self.nt.links.new(v, s)
        return [o for o in m.outputs if o.identifier == "Result_Float"][0]

    def noise(self, tex, scale, detail=3.0, rough=0.55):
        n = self.n("ShaderNodeTexNoise", noise_dimensions="3D", noise_type="FBM", normalize=True)
        n.inputs["Scale"].default_value = scale
        n.inputs["Detail"].default_value = detail
        n.inputs["Roughness"].default_value = rough
        self.nt.links.new(tex.outputs["Object"], n.inputs["Vector"])
        return n.outputs["Fac"]


def _fresh(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(b.outputs["BSDF"], out.inputs["Surface"])
    return m, nt, b, out


def _simple(name, color, metallic=0.0, rough=0.5, coat=0.0, coat_rough=0.03, spec=0.5):
    m, nt, b, out = _fresh(name)
    b.inputs["Base Color"].default_value = color
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = coat_rough
    b.inputs["Specular IOR Level"].default_value = spec
    m.diffuse_color = color
    return m, nt, b, out


def _edge_and_trim(nb, bevel_radius=0.0026):
    """edge: 1 on hard bevels.  trim: edge * object 'wear' strength (default 1)."""
    nt = nb.nt
    attr = nb.n("ShaderNodeAttribute", attribute_type="OBJECT", attribute_name="wear")
    present = nb.math("GREATER_THAN", attr.outputs["Fac"], 0.0000001)
    # property absent -> 1.0 ; present (an explicit 0.0 is stored as 1e-6 by the lib) -> its value
    strength = nb.mixf(present, 1.0, attr.outputs["Fac"])
    bev = nb.n("ShaderNodeBevel", samples=10)
    bev.inputs["Radius"].default_value = bevel_radius
    geo = nb.n("ShaderNodeNewGeometry")
    dot = nb.n("ShaderNodeVectorMath", operation="DOT_PRODUCT")
    nt.links.new(bev.outputs["Normal"], dot.inputs[0])
    nt.links.new(geo.outputs["Normal"], dot.inputs[1])
    edge = nb.maprange(dot.outputs["Value"], 0.9985, 0.94, 0.0, 1.0)
    trim = nb.math("MULTIPLY", edge, strength, clamp=True)
    ao = nb.n("ShaderNodeAmbientOcclusion", samples=8, inside=False, only_local=True)
    ao.inputs["Distance"].default_value = 0.03
    cavity = nb.math("SUBTRACT", 1.0, ao.outputs["AO"], clamp=True)
    return edge, trim, cavity


def _teal():
    m, nt, b, out = _fresh("SEIS_teal")
    nb = _NB(nt)
    tc = nb.n("ShaderNodeTexCoord")
    edge, trim, cavity = _edge_and_trim(nb)
    sheen_n = nb.noise(tc, 6.0, 2.0)
    paint = nb.mixc(nb.math("MULTIPLY", sheen_n, 0.5), C_TEAL, C_TEAL_SHEEN)
    paint = nb.mixc(nb.math("MULTIPLY", cavity, 0.35, clamp=True), paint, C_DARK)       # soft occlusion in crevices
    # thin champagne-gold trim line on the bevel, with a very light mottle inside the gold
    mottle = nb.noise(tc, 40.0, 3.0)
    gold = nb.mixc(nb.math("MULTIPLY", nb.math("SUBTRACT", mottle, 0.5), 0.9), C_GOLD_TRIM, C_BAND)
    gline = nb.maprange(trim, 0.35, 0.75, 0.0, 1.0)
    base = nb.mixc(gline, paint, gold)
    nt.links.new(base, b.inputs["Base Color"])
    nt.links.new(nb.math("MULTIPLY", gline, 1.0, clamp=True), b.inputs["Metallic"])
    nt.links.new(nb.mixf(gline, 0.25, 0.30), b.inputs["Roughness"])
    nt.links.new(nb.math("SUBTRACT", 1.0, gline, clamp=True), b.inputs["Coat Weight"])
    b.inputs["Coat Roughness"].default_value = 0.04
    b.inputs["Specular IOR Level"].default_value = 0.5
    m.diffuse_color = C_TEAL
    return m


def _bronze():
    """clean olive-gold band metal, polished along the edges"""
    m, nt, b, out = _fresh("SEIS_bronze")
    nb = _NB(nt)
    tc = nb.n("ShaderNodeTexCoord")
    edge, trim, cavity = _edge_and_trim(nb)
    mottle = nb.noise(tc, 40.0, 3.0)
    col = nb.mixc(nb.math("MULTIPLY", nb.math("SUBTRACT", mottle, 0.5), 0.9), C_BAND, C_BAND_SHADE)
    col = nb.mixc(nb.math("MULTIPLY", cavity, 0.5, clamp=True), col, C_BAND_SHADE)
    col = nb.mixc(nb.math("MULTIPLY", edge, 0.7, clamp=True), col, C_GOLD_LIGHT)
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Metallic"].default_value = 1.0
    nt.links.new(nb.mixf(edge, 0.38, 0.26), b.inputs["Roughness"])
    m.diffuse_color = C_BAND
    return m


def _gold():
    m, nt, b, out = _simple("SEIS_gold", C_GOLD_TRIM, metallic=1.0, rough=0.28)
    return m


def _red():
    m, nt, b, out = _simple("SEIS_red", C_RED, metallic=0.0, rough=0.12, coat=1.0, coat_rough=0.03)
    nb = _NB(nt)
    b.inputs["IOR"].default_value = 1.5
    b.inputs["Subsurface Weight"].default_value = 0.05
    b.inputs["Subsurface Radius"].default_value = (0.8, 0.12, 0.05)
    b.inputs["Subsurface Scale"].default_value = 0.01
    lw = nb.n("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    nt.links.new(nb.mixc(lw.outputs["Facing"], C_RED, C_RED_DEEP), b.inputs["Base Color"])
    return m


def _silver():
    m, nt, b, out = _simple("SEIS_silver", C_SILVER, metallic=1.0, rough=0.26)
    nb = _NB(nt)
    tc = nb.n("ShaderNodeTexCoord")
    n = nb.noise(tc, 90.0, 5.0)
    nt.links.new(nb.mixf(n, 0.22, 0.32), b.inputs["Roughness"])
    bump = nb.n("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.06
    bump.inputs["Distance"].default_value = 0.0004
    nt.links.new(n, bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def _gunmetal():
    m, nt, b, out = _simple("SEIS_gunmetal", C_GUNMETAL, metallic=0.8, rough=0.30)
    return m


def _dark():
    m, nt, b, out = _simple("SEIS_dark", C_DARK, metallic=0.35, rough=0.62)
    return m


def _darkdisc():
    m, nt, b, out = _simple("SEIS_darkdisc", C_DARKDISC, metallic=0.6, rough=0.38)
    return m


def _white():
    m, nt, b, out = _simple("SEIS_white", C_WHITE, metallic=0.0, rough=0.15, coat=1.0, coat_rough=0.04)
    return m


def _eye():
    m, nt, b, out = _simple("SEIS_eye", hexlin("#B4050C"), rough=0.10, coat=1.0, coat_rough=0.02)
    b.inputs["Emission Color"].default_value = hexlin("#FF1018")
    b.inputs["Emission Strength"].default_value = 3.0
    return m


def _eyecore():
    m, nt, b, out = _simple("SEIS_eyecore", hexlin("#ECD5CE"), rough=0.1)
    b.inputs["Emission Color"].default_value = hexlin("#ECD5CE")
    b.inputs["Emission Strength"].default_value = 6.0
    return m


def _stone():
    m, nt, b, out = _simple("SEIS_stone", C_STONE, metallic=0.0, rough=0.80, spec=0.2)
    nb = _NB(nt)
    tc = nb.n("ShaderNodeTexCoord")
    n1 = nb.noise(tc, 6.0, 7.0)
    n2 = nb.noise(tc, 160.0, 6.0)
    pits = nb.n("ShaderNodeTexVoronoi", voronoi_dimensions="3D", feature="F1")
    pits.inputs["Scale"].default_value = 220.0
    nt.links.new(tc.outputs["Object"], pits.inputs["Vector"])
    pit = nb.maprange(pits.outputs["Distance"], 0.16, 0.07, 0.0, 1.0)
    pit = nb.math("MULTIPLY", pit, nb.maprange(n2, 0.5, 0.65, 0.0, 1.0), clamp=True)
    col = nb.mixc(n1, hexlin("#77755F"), hexlin("#948F78"))
    col = nb.mixc(nb.math("MULTIPLY", pit, 0.6, clamp=True), col, hexlin("#3C3B33"))
    nt.links.new(col, b.inputs["Base Color"])
    bh = nb.math("SUBTRACT", nb.math("MULTIPLY", n2, 0.5), nb.math("MULTIPLY", pit, 1.2))
    bump = nb.n("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.5
    bump.inputs["Distance"].default_value = 0.002
    nt.links.new(bh, bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def _dais():
    m, nt, b, out = _simple("SEIS_dais", C_DAIS, metallic=0.0, rough=0.6, spec=0.3)
    return m


def _backdrop():
    m, nt, b, out = _simple("SEIS_backdrop", C_BACKDROP, rough=0.95, spec=0.1)
    return m


_BUILD = {"teal": _teal, "bronze": _bronze, "gold": _gold, "red": _red, "silver": _silver, "gunmetal": _gunmetal,
          "dark": _dark, "darkdisc": _darkdisc, "white": _white, "eye": _eye, "eyecore": _eyecore, "stone": _stone,
          "dais": _dais, "backdrop": _backdrop}
_ALIAS = {"concrete": "stone", "gold_band": "bronze"}


def get(name):
    """Return (creating if needed) the material called `name`."""
    name = _ALIAS.get(name, name)
    m = bpy.data.materials.get("SEIS_" + name)
    if m is not None:
        return m
    if name not in _BUILD:
        raise KeyError("unknown SEIS material: %r (have %s)" % (name, sorted(_BUILD) + sorted(_ALIAS)))
    return _BUILD[name]()
