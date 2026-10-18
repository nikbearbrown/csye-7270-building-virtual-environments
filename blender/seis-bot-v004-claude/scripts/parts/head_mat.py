"""head_mat - head-private material 'pewter' (registered into seis_mat at import, no shared file edited).

ON-MODEL: the head is a WARM LIGHT PEWTER (f08 head median #867762..#A8A594, up-facing faces ~#E0E4E6) and reads soft, not
black chrome.  The shared 'silver' is metallic 1.0 and renders near black in a dark room, so the head uses this satin
pewter (metallic 0.62: a diffuse floor keeps it light, the metal part still takes the sky gradient).  Same noise bump as silver.
"""
import seis_mat as M


def _pewter():
    m, nt, b, out = M._simple("SEIS_pewter", M.hexlin("#7E7964"), metallic=0.62, rough=0.30)
    nb = M._NB(nt)
    tc = nb.n("ShaderNodeTexCoord")
    n = nb.noise(tc, 90.0, 5.0)
    nt.links.new(nb.mixf(n, 0.26, 0.34), b.inputs["Roughness"])
    bump = nb.n("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.05
    bump.inputs["Distance"].default_value = 0.0004
    nt.links.new(n, bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


M._BUILD.setdefault("pewter", _pewter)


def _pewter_shade():
    """the shaded / recessed pewter (muzzle shade #44432E .. #645E45): what shows in a seam or an uncovered recess"""
    m, nt, b, out = M._simple("SEIS_pewter_shade", M.hexlin("#6A6450"), metallic=0.45, rough=0.40)
    return m


def _yoke():
    """dark olive-grey chin yoke (#16160B in shade, lit olive-grey #3C3B2A): satin, not black"""
    m, nt, b, out = M._simple("SEIS_yoke", M.hexlin("#3A3929"), metallic=0.55, rough=0.34)
    return m


M._BUILD.setdefault("pewter_shade", _pewter_shade)
M._BUILD.setdefault("yoke", _yoke)


def _teal_deep():
    """the head's DARK teal (ear shell outer #163330, dome shade #1C3B3D in the frames): the same paint as 'teal' but a
    darker, greener, satin base so the ear shell and rear dome read dark gunmetal-teal next to the pewter face"""
    m, nt, b, out = M._simple("SEIS_teal_deep", M.hexlin("#12302F"), metallic=0.25, rough=0.30, coat=0.8, coat_rough=0.06)
    return m


M._BUILD.setdefault("teal_deep", _teal_deep)


def _eye_lens():
    """round 3: the eye lens is a softer satin red bulb (f07/f08: ONE white-pink hot spot, no window reflections on the dome):
    low coat, broader roughness, emission about 3 so it glows without bloom"""
    m, nt, b, out = M._simple("SEIS_eye_lens", M.hexlin("#7E0309"), metallic=0.0, rough=0.34, coat=0.12, coat_rough=0.30)
    b.inputs["Emission Color"].default_value = M.hexlin("#E0060E")
    b.inputs["Emission Strength"].default_value = 0.9
    return m


M._BUILD.setdefault("eye_lens", _eye_lens)
