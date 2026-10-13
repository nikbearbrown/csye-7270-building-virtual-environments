# render_assets.py - real Blender Workbench renders (transparent PNG, 2400x1350) of the three assets built by
# ../assets/build_*.py. Method follows the sibling film's render_post.py. No window.
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 \
#       --python render_assets.py -- <out_dir>
import bpy, sys, os, math, runpy
from mathutils import Vector

out_dir = sys.argv[sys.argv.index("--") + 1]
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "..", "assets")
sc = bpy.context.scene


def load(name):
    ns = runpy.run_path(os.path.join(assets, "build_%s.py" % name), run_name="lib")    # defines build(); does not export
    ns["build"].__globals__["clear_scene"] = lambda: None        # keep what is already in the scene
    return ns


def clear_all():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)


def setup_render():
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = 2400, 1350
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'     # Blender 5's default (AgX) washes flat colours out; Standard shows the material colours as set
    sh = sc.display.shading
    sh.light = "STUDIO"; sh.studio_light = "paint.sl"
    sh.color_type = 'MATERIAL'
    sh.show_cavity = False
    sh.show_object_outline = True
    sh.object_outline_color = (0.16, 0.13, 0.10)
    sh.show_specular_highlight = False


def camera_at(loc, target, lens=50):
    cam = bpy.data.objects.get("RenderCam")
    if cam is None:
        cam = bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam"))
        sc.collection.objects.link(cam)
    cam.data.lens = lens
    cam.location = loc
    tgt = bpy.data.objects.get("RenderTarget")
    if tgt is None:
        tgt = bpy.data.objects.new("RenderTarget", None)
        sc.collection.objects.link(tgt)
    tgt.location = target
    for c in list(cam.constraints):
        cam.constraints.remove(c)
    c = cam.constraints.new('TRACK_TO')
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    sc.camera = cam


def orbit(target, dist, azimuth_deg, elevation_deg):
    """Camera position on a sphere round the target. azimuth 0 = looking along +Y from the -Y side (the 'front')."""
    a, e = math.radians(azimuth_deg), math.radians(elevation_deg)
    t = Vector(target)
    return t + Vector((dist * math.cos(e) * math.sin(a), -dist * math.cos(e) * math.cos(a), dist * math.sin(e)))


def shoot(name):
    path = os.path.join(out_dir, name + ".png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered %s (%d bytes)" % (os.path.basename(path), os.path.getsize(path)), flush=True)


def single(asset, target, dist, views, **kw):
    clear_all()
    ns = load(asset)
    ns["build"]()
    for name, az, el in views:
        camera_at(orbit(target, dist, az, el), target, **kw)
        shoot(name)


setup_render()
# three-quarter views: camera 35 deg round from the front, a little above
single("crate", (0, 0, 0.40), 3.6, [("ev_crate_34", 35, 22)])
single("lantern", (0, 0, 0.25), 2.3, [("ev_lantern_34", 35, 22), ("ev_lantern_back", 215, 22), ("ev_lantern_below", 35, -38)])
single("coin", (0, 0, 0.02), 1.0, [("ev_coin_34", 35, 30)])

# all three side by side on a floor plane
clear_all()
placed = {"crate": -0.65, "lantern": 0.05, "coin": 0.50}
for asset, x in placed.items():
    ns = load(asset)
    o, n = ns["build"]()
    o.location = (x, 0.0, 0.0)
    print("placed %s at x = %+.2f m (origin on the floor)" % (o.name, x))
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0))
fl = bpy.context.active_object
fl.name = "Floor"
fl.scale = (8.0, 5.0, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
m = bpy.data.materials.new("FloorGrey")
m.diffuse_color = (0.30, 0.31, 0.28, 1.0)
fl.data.materials.append(m)
camera_at(orbit((-0.12, 0, 0.22), 3.7, 12, 20), (-0.12, 0, 0.22))
shoot("ev_three_side_by_side")
