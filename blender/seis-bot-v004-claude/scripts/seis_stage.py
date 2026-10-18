"""seis_stage - studio lighting, cameras and a render helper for the SEIS bot.

    st.studio(size=1.0)                  white-grey seamless + big key softbox + fill + rim + top (like the references)
    st.camera_for(objs, view, ...)       frame a set of objects from a named view; view is one of
                                         front back left right top three_q three_q_r three_q_back low
                                         (or a (direction_to_camera, up) pair)
    st.render(path, w, h, samples)       Cycles on the Apple GPU with denoise; AgX tone mapping
    st.render_views(objs, outdir, views, ...)   one PNG per view;  clay=True renders matte grey form-check images
Safe to call in a background (-b) Blender and in the live MCP-driven one.
"""
import math
import os
import bpy
from mathutils import Vector

import seis_lib as L

_VIEWS = {
    #            direction FROM the subject TO the camera, up
    "front":        ((0, -1, 0), (0, 0, 1)),
    "back":         ((0, 1, 0), (0, 0, 1)),
    "left":         ((1, 0, 0), (0, 0, 1)),      # the robot's LEFT (+X) side
    "right":        ((-1, 0, 0), (0, 0, 1)),
    "top":          ((0, -0.001, 1), (0, 1, 0)),
    "three_q":      ((0.62, -0.78, 0.14), (0, 0, 1)),    # front, robot's left
    "three_q_r":    ((-0.62, -0.78, 0.14), (0, 0, 1)),   # front, robot's right
    "three_q_back": ((0.62, 0.78, 0.14), (0, 0, 1)),
    "low":          ((0.35, -0.9, -0.12), (0, 0, 1)),
}


def _cyclorama(size):
    """Floor + curved wall: one surface from the front of the floor, along z=0, round a radius, up the wall."""
    R = 2.5 * size
    y0, yw = -3.2 * size, 7 * size       # floor start (short, so nothing bright sits behind the camera), wall plane
    floor_len = yw - R - y0
    wall_h = 14 * size
    arc_len = R * math.pi / 2
    total = floor_len + arc_len + wall_h

    def prof(s):                          # s in [0,1] -> (y, z)
        d = s * total
        if d <= floor_len:
            return (y0 + d, 0.0)
        d -= floor_len
        if d <= arc_len:
            a = d / R
            return (yw - R + R * math.sin(a), R * (1 - math.cos(a)))
        d -= arc_len
        return (yw, R + d)

    def fn(u, v):
        y, z = prof(v)
        return ((u - 0.5) * 36 * size, y, z)

    ob = L.grid_surface("backdrop", fn, 2, 60, flip=False)
    L.set_material(ob, "backdrop")
    return ob


def studio(backdrop=True, key_power=320.0, world_strength=0.06, size=1.0, exposure=0.0):
    """Cyclorama + softbox lights tuned for a ~2 m subject at the origin (pass size=0.5 for a 1 m subject)."""
    sc = bpy.context.scene
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.75, 0.76, 0.78, 1)
    bg.inputs["Strength"].default_value = world_strength
    prev = L._COLL
    L.set_collection(L.collection("STAGE"))
    if backdrop:
        _cyclorama(size)

    def area(name, loc, target, power, sx, sy, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = power
        ld.shape = "RECTANGLE"
        ld.size, ld.size_y = sx, sy
        ld.color = color
        ob = bpy.data.objects.new(name, ld)
        L._link(ob)
        ob.location = loc
        ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        return ob

    s = size
    area("key", (2.8 * s, -3.4 * s, 3.2 * s), (0, 0, 1.0 * s), key_power * s * s, 2.6 * s, 3.4 * s, (1.0, 0.97, 0.93))
    area("fill", (-3.6 * s, -2.6 * s, 1.4 * s), (0, 0, 1.0 * s), key_power * 0.30 * s * s, 3.0 * s, 3.0 * s, (0.92, 0.96, 1.0))
    area("rim", (-1.8 * s, 3.2 * s, 3.2 * s), (0, 0, 1.2 * s), key_power * 0.9 * s * s, 1.4 * s, 3.2 * s, (1, 1, 1))
    area("top", (0.0, -0.5 * s, 4.8 * s), (0, 0, 1.0 * s), key_power * 0.45 * s * s, 3.2 * s, 3.2 * s)
    sc.view_settings.exposure = exposure
    if prev:
        L.set_collection(prev)
    return sc


def workshop(size=1.0, key_power=380.0):
    """On-model HERO lighting (spec/ONMODEL.md section 5): a brick workshop, dark warm world, a big cool window key,
    an overhead white card, a warm tungsten kicker, a cyan monitor spill, brick wall + concrete floor + window panels
    that glossy paint can mirror.  Pair with camera_for(..., fstop=2.8) for the soft background."""
    sc = bpy.context.scene
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.20, 0.15, 0.12, 1)
    bg.inputs["Strength"].default_value = 0.03
    prev = L._COLL
    L.set_collection(L.collection("STAGE"))
    s = size
    # concrete floor
    fl = L.grid_surface("backdrop_floor", lambda u, v: ((u - 0.5) * 24 * s, -6 * s + v * 14 * s, 0.0), 1, 1)
    fm = bpy.data.materials.new("SEIS_floor"); fm.use_nodes = True
    fb = fm.node_tree.nodes["Principled BSDF"]
    fb.inputs["Base Color"].default_value = (0.30, 0.30, 0.26, 1); fb.inputs["Roughness"].default_value = 0.55
    fl.data.materials.append(fm)
    # brick wall behind (procedural bricks)
    wall = L.grid_surface("backdrop_wall", lambda u, v: ((u - 0.5) * 24 * s, 5.0 * s, v * 8 * s), 1, 1, flip=True)
    wm = bpy.data.materials.new("SEIS_brick"); wm.use_nodes = True
    nt = wm.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.inputs["Color1"].default_value = (0.38, 0.14, 0.06, 1)
    brick.inputs["Color2"].default_value = (0.30, 0.10, 0.045, 1)
    brick.inputs["Mortar"].default_value = (0.42, 0.38, 0.32, 1)
    brick.inputs["Scale"].default_value = 2.2 / s
    brick.inputs["Mortar Size"].default_value = 0.012
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    com = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["X"], com.inputs["X"])
    nt.links.new(sep.outputs["Z"], com.inputs["Y"])           # the wall lies in the XZ plane: use (x, z)
    nt.links.new(com.outputs["Vector"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    wall.data.materials.append(wm)
    # glowing arched-window panels on the wall (what the glossy teal mirrors)
    def panel(name, cx, cz, w_, h_, strength):
        ob = L.grid_surface(name, lambda u, v: (cx + (u - 0.5) * w_, 4.95 * s, cz + (v - 0.5) * h_), 1, 1, flip=True)
        m = bpy.data.materials.new("SEIS_" + name); m.use_nodes = True
        nt2 = m.node_tree
        for n in list(nt2.nodes):
            if n.type != "OUTPUT_MATERIAL":
                nt2.nodes.remove(n)
        em = nt2.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (1.0, 0.97, 0.92, 1); em.inputs["Strength"].default_value = strength
        out = [n for n in nt2.nodes if n.type == "OUTPUT_MATERIAL"][0]
        nt2.links.new(em.outputs["Emission"], out.inputs["Surface"])
        ob.data.materials.append(m)
        return ob
    panel("window_l", -2.6 * s, 2.2 * s, 1.4 * s, 2.6 * s, 3.0)
    panel("window_r", 2.6 * s, 2.2 * s, 1.4 * s, 2.6 * s, 3.0)
    panel("window_c", 0.0, 3.4 * s, 1.2 * s, 1.8 * s, 2.0)

    def area(name, loc, target, power, sx, sy, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = power
        ld.shape = "RECTANGLE"
        ld.size, ld.size_y = sx, sy
        ld.color = color
        ob = bpy.data.objects.new(name, ld)
        L._link(ob)
        ob.location = loc
        ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        return ob
    # overhead-front window key (cool) + overhead white card
    area("key_window", (0.6 * s, -2.8 * s, 3.4 * s), (0, 0, 1.0 * s), key_power * s * s, 3.0 * s, 2.2 * s, (0.90, 0.95, 1.0))
    area("top_card", (0.0, -0.8 * s, 3.8 * s), (0, 0, 1.0 * s), key_power * 0.55 * s * s, 2.4 * s, 2.4 * s, (1.0, 1.0, 1.0))
    # warm tungsten kicker behind-left and low
    area("kicker_warm", (-2.4 * s, 1.6 * s, 0.9 * s), (0, 0, 1.2 * s), key_power * 0.50 * s * s, 1.0 * s, 1.6 * s, (1.0, 0.62, 0.30))
    # cyan monitor spill front-right low
    area("monitor_spill", (1.5 * s, -1.2 * s, 0.9 * s), (0, 0, 1.1 * s), key_power * 0.16 * s * s, 0.8 * s, 0.6 * s, (0.55, 0.85, 1.0))
    # big soft front card behind the camera: what flat front-facing glossy plates mirror (the pale sky of the frames)
    area("front_card", (0.0, -4.2 * s, 2.0 * s), (0, 0, 1.1 * s), key_power * 0.30 * s * s, 4.0 * s, 2.6 * s, (0.85, 0.93, 1.0))
    # soft warm bounce from the left
    area("brick_bounce", (-2.6 * s, -1.2 * s, 1.0 * s), (0, 0, 1.0 * s), key_power * 0.18 * s * s, 2.0 * s, 2.0 * s, (1.0, 0.72, 0.5))
    if prev:
        L.set_collection(prev)
    return sc


def camera_for(objs, view="front", focal=85.0, margin=1.12, aspect=0.75, target=None, name="cam", fstop=None):
    """Create/replace the scene camera so every bounding-box corner of objs fits in frame."""
    d, up = _VIEWS[view] if isinstance(view, str) else view
    d = Vector(d).normalized()
    up = Vector(up)
    lo, hi = L.bbox_world(objs)
    c = Vector(target) if target is not None else (lo + hi) / 2
    fwd = -d
    right = fwd.cross(up).normalized()
    upv = right.cross(fwd).normalized()
    sensor = 36.0
    half = (sensor / 2 / focal) / margin               # tangent of the half field of view on the fitted axis
    if aspect >= 1:
        tx, ty, fit = half, half / aspect, "HORIZONTAL"
    else:
        tx, ty, fit = half * aspect, half, "VERTICAL"
    dist = 0.1
    for xi in (lo.x, hi.x):
        for yi in (lo.y, hi.y):
            for zi in (lo.z, hi.z):
                rel = Vector((xi, yi, zi)) - c
                dist = max(dist, abs(rel.dot(right)) / tx + rel.dot(d), abs(rel.dot(upv)) / ty + rel.dot(d))
    cam_ob = bpy.data.objects.get(name)
    if cam_ob is None:
        cam_ob = bpy.data.objects.new(name, bpy.data.cameras.new(name))
        bpy.context.scene.collection.objects.link(cam_ob)
    cam_ob.data.lens = focal
    cam_ob.data.sensor_width = sensor
    cam_ob.data.sensor_height = sensor
    cam_ob.data.sensor_fit = fit
    cam_ob.data.clip_start = 0.02
    cam_ob.data.clip_end = 300
    cam_ob.location = c + d * dist
    cam_ob.data.dof.use_dof = fstop is not None
    if fstop is not None:
        cam_ob.data.dof.focus_distance = dist
        cam_ob.data.dof.aperture_fstop = fstop
    q = (-d).to_track_quat("-Z", "Y")
    cam_ob.rotation_euler = q.to_euler()
    bpy.context.scene.camera = cam_ob
    return cam_ob


def configure(w=900, h=1200, samples=48, engine="CYCLES", denoise=True, gpu=True):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "8"
    for vt, lk in (("AgX", "AgX - Medium High Contrast"), ("AgX", "None"), ("Standard", "None")):
        try:
            sc.view_settings.view_transform = vt
            sc.view_settings.look = lk
            break
        except Exception:
            continue
    sc.render.engine = engine
    if engine == "CYCLES":
        cy = sc.cycles
        cy.samples = samples
        cy.use_denoising = denoise
        cy.use_adaptive_sampling = True
        cy.adaptive_threshold = 0.02
        cy.max_bounces = 8
        cy.sample_clamp_indirect = 8.0
        cy.device = "CPU"
        if gpu:
            try:
                prefs = bpy.context.preferences.addons["cycles"].preferences
                prefs.compute_device_type = "METAL"
                prefs.get_devices()
                for dv in prefs.devices:
                    dv.use = dv.type != "CPU"
                cy.device = "GPU"
            except Exception:
                cy.device = "CPU"
    else:
        try:
            sc.eevee.taa_render_samples = samples
        except Exception:
            pass
    return sc


_CLAY = None


def set_clay(on=True):
    """Override every material with matte mid-grey so only FORM shows (for shape checks)."""
    global _CLAY
    vl = bpy.context.view_layer
    if not on:
        vl.material_override = None
        return
    if _CLAY is None or _CLAY.name not in bpy.data.materials:
        _CLAY = bpy.data.materials.new("CLAY")
        _CLAY.use_nodes = True
        b = _CLAY.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.42, 0.42, 0.42, 1)
        b.inputs["Roughness"].default_value = 0.55
        b.inputs["Specular IOR Level"].default_value = 0.35
    vl.material_override = _CLAY


def render(path, w=900, h=1200, samples=48, engine="CYCLES", gpu=True):
    configure(w, h, samples, engine, gpu=gpu)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def render_views(objs, outdir, views=("front", "three_q", "left"), w=700, h=900, samples=32, prefix="", focal=85.0,
                 margin=1.12, engine="CYCLES", gpu=True, clay=False):
    outs = []
    set_clay(clay)
    for v in views:
        camera_for(objs, v, focal=focal, margin=margin, aspect=w / h)
        outs.append(render(os.path.join(outdir, f"{prefix}{v}.png"), w, h, samples, engine, gpu))
    set_clay(False)
    return outs
