# render_act1.py - Act I renders (real Blender 5.1.2 Workbench, transparent PNG 2400x1350), same look as ../renders/render_assets.py.
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python render_act1.py -- <raw_out_dir>
# then:  python3 crop_act1.py <raw_out_dir>      (crops into ../../pantry/a1_*.png)
#
# B04  the five DEFAULT basic shapes (cube, cylinder, cone, UV sphere, plane), one camera for all five so their sizes compare,
#      in one neutral "clay" colour; and the lantern built shape by shape in clay (isolated part + running total after each part),
#      from the SAME camera as pantry/ev_lantern_34.png, so the pictures stack exactly.
# B12  the crate built shape by shape, in its real colours (isolated part + running total), same camera as pantry/ev_crate_34.png.
# B03  four EXAMPLE assets of the kinds the narration names (platform, tree, rock, gem), each built only from basic shapes with
#      flat colours, like the three real assets. They are examples for the picture, not part of the assignment's three.
import bpy, sys, os, math, runpy
from mathutils import Vector

out_dir = sys.argv[sys.argv.index("--") + 1]
os.makedirs(out_dir, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "..", "assets")
sc = bpy.context.scene
CLAY = "#BFA67E"


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def mat(name, hexs):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = tuple(lin(int(hexs[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1.0,)
    return m


def clear_all():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def setup_render():
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = 2400, 1350
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'
    sh = sc.display.shading
    sh.light = "STUDIO"; sh.studio_light = "paint.sl"
    sh.color_type = 'MATERIAL'
    sh.show_cavity = False
    sh.show_object_outline = True
    sh.object_outline_color = (0.16, 0.13, 0.10)
    sh.show_specular_highlight = False


def orbit(target, dist, az, el):
    a, e = math.radians(az), math.radians(el)
    t = Vector(target)
    return t + Vector((dist * math.cos(e) * math.sin(a), -dist * math.cos(e) * math.cos(a), dist * math.sin(e)))


def camera(target, dist, az=35, el=22, lens=50):
    for nm in ("RenderCam", "RenderTarget"):            # a fresh camera each time (the build scripts' clear_scene deletes objects)
        old = bpy.data.objects.get(nm)
        if old is not None:
            bpy.data.objects.remove(old, do_unlink=True)
    cam = bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam"))
    sc.collection.objects.link(cam)
    cam.data.lens = lens
    cam.location = orbit(target, dist, az, el)
    tgt = bpy.data.objects.new("RenderTarget", None)
    sc.collection.objects.link(tgt)
    tgt.location = target
    for c in list(cam.constraints):
        cam.constraints.remove(c)
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    sc.camera = cam


def shoot(name):
    path = os.path.join(out_dir, name + ".png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered %s" % name, flush=True)


def tris(o):
    o.data.calc_loop_triangles()
    return len(o.data.loop_triangles)


def only(objs, visible):
    for o in objs:
        o.hide_render = o not in visible


setup_render()

# ── B04: the five default basic shapes, one camera, clay ──────────────────────────────────────────────────────────────
clay = mat("Clay", CLAY)
for name, op in [("cube", bpy.ops.mesh.primitive_cube_add), ("cylinder", bpy.ops.mesh.primitive_cylinder_add),
                 ("cone", bpy.ops.mesh.primitive_cone_add), ("sphere", bpy.ops.mesh.primitive_uv_sphere_add),
                 ("plane", bpy.ops.mesh.primitive_plane_add)]:
    clear_all()
    op()                                    # Blender's defaults: size 2 / radius 1, depth 2, at the world origin
    o = bpy.context.active_object
    o.data.materials.append(clay)
    print("primitive %-9s default: dimensions %.2f x %.2f x %.2f m, %d triangles" % (name, *o.dimensions, tris(o)))
    camera((0, 0, 0), 9.0)
    shoot("prim_" + name)

# ── B04: the lantern, shape by shape, in clay (same camera as ev_lantern_34) ─────────────────────────────────────────
lan = runpy.run_path(os.path.join(assets, "build_lantern.py"), run_name="lib")
clear_all()
parts, n = lan["build"](join=False)
clay = mat("Clay", CLAY)                    # the build script's clear_scene removed every material; make the clay again
for p in parts:
    p.data.materials.clear(); p.data.materials.append(clay)
camera((0, 0, 0.25), 2.3)
for i, p in enumerate(parts, 1):
    only(parts, [p]); shoot("lpart_%d" % i)
    only(parts, parts[:i]); shoot("lcum_%d" % i)
print("lantern parts:", ", ".join("%s %d tris" % (p.name, tris(p)) for p in parts))

# ── B12: the crate, shape by shape, real colours (same camera as ev_crate_34) ───────────────────────────────────────
cra = runpy.run_path(os.path.join(assets, "build_crate.py"), run_name="lib")
clear_all()
parts, n = cra["build"](join=False)
camera((0, 0, 0.40), 3.6)
for i, p in enumerate(parts, 1):
    only(parts, [p]); shoot("cpart_%d" % i)
    only(parts, parts[:i]); shoot("ccum_%d" % i)
print("crate parts:", ", ".join("%s %d tris" % (p.name, tris(p)) for p in parts))


# ── B03: example assets of the other kinds the narration names (basic shapes, flat colours) ──────────────────────────
def cyl(name, r, d, z0, m, v=8, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=(0, 0, z0 + d / 2))
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r, radius2=r2, depth=d, location=(0, 0, z0 + d / 2))
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m); return o


def example(label, build, target, dist, el=22):
    clear_all()
    objs = build()
    t = sum(tris(o) for o in objs)
    zs = [(o.matrix_world @ v.co).z for o in objs for v in o.data.vertices]
    xs = [(o.matrix_world @ v.co).x for o in objs for v in o.data.vertices]
    ys = [(o.matrix_world @ v.co).y for o in objs for v in o.data.vertices]
    print("example %-9s %d shapes, %d triangles, %.2f x %.2f x %.2f m" % (label, len(objs), t, max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)))
    camera(target, dist, el=el)
    shoot("ex_" + label)


def platform():
    stone, grass = mat("Stone", "#9A8F7E"), mat("Grass", "#6E9A4A")
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.09)); a = bpy.context.active_object
    a.scale = (1.6, 0.8, 0.18); bpy.ops.object.transform_apply(scale=True); a.data.materials.append(stone)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.205)); b = bpy.context.active_object
    b.scale = (1.62, 0.82, 0.05); bpy.ops.object.transform_apply(scale=True); b.data.materials.append(grass)
    return [a, b]


def tree():
    bark, leaf = mat("Bark", "#7E5128"), mat("Leaf", "#4F8A3A")
    return [cyl("Trunk", 0.07, 0.40, 0.0, bark), cyl("Crown_Low", 0.34, 0.55, 0.30, leaf, r2=0.0),
            cyl("Crown_High", 0.25, 0.45, 0.65, leaf, r2=0.0)]


def rock():
    grey = mat("RockGrey", "#8A8780")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=1.0, location=(0, 0, 0.0))
    o = bpy.context.active_object; o.name = "Rock"
    o.scale = (0.42, 0.32, 0.26); o.rotation_euler = (0.0, 0.18, 0.5)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    zmin = min(v.co.z for v in o.data.vertices); o.location.z = -zmin
    bpy.ops.object.transform_apply(location=True)
    o.data.materials.append(grey)
    return [o]


def gem():
    blue = mat("GemBlue", "#2F8FD8")
    pav = cyl("Pavilion", 0.12, 0.14, 0.0, blue, v=6, r2=0.0)
    pav.rotation_euler = (math.pi, 0, 0); bpy.ops.object.transform_apply(rotation=True)
    crown = cyl("Crown", 0.12, 0.06, 0.14, blue, v=6, r2=0.07)     # sits on the pavilion's wide top (z 0.14 .. 0.20)
    return [pav, crown]


example("platform", platform, (0, 0, 0.12), 4.2)
example("tree", tree, (0, 0, 0.55), 3.4)
example("rock", rock, (0, 0, 0.18), 2.4)
example("gem", gem, (0, 0, 0.07), 1.3)
print("done")
