"""Render review views of one teaching prop: matte model on a plain floor, one sun + soft fill, EEVEE.

  Blender -b <prop>.blend --python render_props.py -- --out-dir renders --tag crate [--size 1200x900] [--samples 64]

The source .blend holds one mesh and no camera or light, so this script adds a floor, lights and cameras at render
time and never saves the .blend. Views: front34, back34, side, top, close (a detail view chosen per prop).
Distances scale with the prop's longest side, so one script serves the crate, lantern and coin.
"""
import argparse, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out-dir", required=True)
ap.add_argument("--tag", required=True)
ap.add_argument("--size", default="1200x900")
ap.add_argument("--samples", type=int, default=64)
a = ap.parse_args(argv)
out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
W, H = map(int, a.size.split("x"))

sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = a.samples
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = -1.0

meshes = [o for o in sc.objects if o.type == "MESH"]
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
ctr = (lo + hi) / 2; size = max(hi - lo)

# world: soft neutral grey
sc.world = sc.world or bpy.data.worlds.new("W"); sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.72, 0.74, 0.78, 1); bg.inputs[1].default_value = 0.9

# floor (a big plane at z=0, light warm grey)
bpy.ops.mesh.primitive_plane_add(size=size * 40, location=(0, 0, -0.0005))
fl = bpy.context.object; fl.name = "StageFloor"
m = bpy.data.materials.new("StageFloor"); m.use_nodes = True
m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.53, 0.50, 1)
m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
fl.data.materials.append(m)

def light(kind, loc, energy, **kw):
    d = bpy.data.lights.new(kind, kind); d.energy = energy
    for k, v in kw.items(): setattr(d, k, v)
    o = bpy.data.objects.new(kind, d); sc.collection.objects.link(o); o.location = loc
    return o
sun = light("SUN", (0, 0, 5), 3.5, angle=math.radians(8)); sun.rotation_euler = (math.radians(50), 0, math.radians(35))
fill = light("AREA", (-size * 3, -size * 2, size * 3), 80 * size * size * 4, size=size * 4)
fill.rotation_euler = (math.radians(55), 0, math.radians(-55))

tgt = bpy.data.objects.new("T", None); sc.collection.objects.link(tgt)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); sc.collection.objects.link(cam); sc.camera = cam
tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"

def shoot(name, direction, dist, target, lens=50):
    cam.data.lens = lens; tgt.location = target
    cam.location = target + Vector(direction).normalized() * dist
    sc.render.filepath = str(out / f"{a.tag}_{name}.png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", sc.render.filepath)

k = size
shoot("front34", (-0.8, -1.0, 0.7), k * 4.2, ctr)
shoot("back34", (0.9, 0.9, 0.7), k * 4.2, ctr)
shoot("side", (0.0, -1.0, 0.12), k * 4.0, ctr)
shoot("top", (0.001, -0.15, 1.0), k * 4.0, ctr)
# close-up per prop: crate = a top corner with band and lid; lantern = flame gap under the roof; coin = medallion edge
close = {"crate": ((-0.9, -1.0, 0.5), 1.6, Vector((-0.3, -0.4, 0.72)), 50),
         "lantern": ((-0.8, -1.0, 0.25), 0.85, Vector((0, 0, 0.32)), 60),
         "coin": ((-0.6, -1.0, 0.8), 0.6, Vector((0, 0, 0.04)), 60)}[a.tag]
shoot("close", close[0], close[1], close[2], close[3])
