# render_spheres.py - a default UV sphere and a 12-segment x 6-ring sphere, side by side, Workbench render with the TRIANGLES drawn.
# Each sphere is triangulated (so the wire is the triangle count the course budget counts), and the same triangulated mesh is
# drawn a second time with a Wireframe modifier over the solid one (Workbench renders do not draw the viewport's wire overlay).
#   Blender -b --factory-startup --python-exit-code 1 --python render_spheres.py -- <out.png>
import bpy, sys, os, math
from mathutils import Vector

out = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def colour(name, hexs, wire=False):
    rgb = tuple(lin(int(hexs[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1.0,)
    m = bpy.data.materials.new(name)
    m.diffuse_color = rgb
    return m


solid = colour("SphereFill", "#E8C27A")
wire_m = colour("SphereWire", "#2B2B30")


def sphere(name, x, **kw):
    bpy.ops.mesh.primitive_uv_sphere_add(location=(x, 0, 0), radius=1.0, **kw)
    o = bpy.context.active_object
    o.name = name
    tri = o.modifiers.new("Triangulate", 'TRIANGULATE')
    bpy.ops.object.modifier_apply(modifier=tri.name)
    n = len(o.data.polygons)                       # every face is a triangle now
    o.data.materials.append(solid)
    w = o.copy()                                    # a second copy of the same triangulated mesh, drawn as a Wireframe-modifier mesh
    w.data = o.data.copy()
    w.name = name + "_wire"
    sc.collection.objects.link(w)
    w.data.materials.clear()
    w.data.materials.append(wire_m)
    wm = w.modifiers.new("Wire", 'WIREFRAME')       # every triangle edge becomes a thin strip: the triangles can be counted by eye
    wm.thickness = 0.016
    wm.offset = 1.0
    wm.use_replace = True
    wm.use_even_offset = True
    print("%-22s %d triangles" % (name, n))
    return o, w, n


a, aw, na = sphere("UV sphere default", -1.15)                         # 32 segments x 16 rings
b, bw, nb = sphere("UV sphere 12x6", 1.15, segments=12, ring_count=6)

sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = 2400, 1350
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'
sh = sc.display.shading
sh.light = 'STUDIO'
sh.studio_light = 'paint.sl'
sh.color_type = 'MATERIAL'
sh.show_cavity = False
sh.show_object_outline = False
sh.show_specular_highlight = False

cam = bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam"))
sc.collection.objects.link(cam)
cam.data.lens = 60
cam.location = Vector((0.0, -10.5, 1.6))
tgt = bpy.data.objects.new("T", None)
sc.collection.objects.link(tgt)
tgt.location = (0, 0, 0)
c = cam.constraints.new('TRACK_TO')
c.target = tgt
c.track_axis = 'TRACK_NEGATIVE_Z'
c.up_axis = 'UP_Y'
sc.camera = cam
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("rendered %s (%d bytes)" % (os.path.basename(out), os.path.getsize(out)))
