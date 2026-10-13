# Renders the real checkpoint post (built by the final agent script) with Blender's own Workbench engine.
# Run:  Blender -b --factory-startup --python-exit-code 1 --python render_post.py -- <out_dir>
import bpy, sys, os, math, runpy
out = sys.argv[sys.argv.index("--") + 1]
here = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(here, "scratch", "tools", "blender", "build_checkpoint_post.py"), run_name="__main__")
sc = bpy.context.scene
col = bpy.data.objects["Collision-convcolonly"]
for m in bpy.data.materials:
    if m.name == "PostMetal": m.diffuse_color = (0.50, 0.52, 0.58, 1.0)
    if m.name == "FlagCloth": m.diffuse_color = (0.85, 0.30, 0.20, 1.0)
def render(name, show_collision=False, only_collision=False, loc=(3.9, -4.6, 2.0), target=(0.12, 0, 0.9), res=(2400, 1350), lens=42):
    col.hide_render = not (show_collision or only_collision)
    for n in ("Base", "Pole", "Pennant"):
        bpy.data.objects[n].hide_render = only_collision
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sh = sc.display.shading
    sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_cavity = False; sh.show_object_outline = True
    sh.object_outline_color = (0.24, 0.22, 0.16)
    cam = bpy.data.objects.get("RenderCam")
    if cam is None:
        cd = bpy.data.cameras.new("RenderCam"); cam = bpy.data.objects.new("RenderCam", cd)
        bpy.context.collection.objects.link(cam)
    cam.data.lens = lens
    cam.location = loc
    tgt = bpy.data.objects.get("RenderTarget")
    if tgt is None:
        tgt = bpy.data.objects.new("RenderTarget", None); bpy.context.collection.objects.link(tgt)
    tgt.location = target
    for c in list(cam.constraints): cam.constraints.remove(c)
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    sc.camera = cam
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", sc.render.filepath)
render("post_visual")
render("post_collider_only", only_collision=True)
render("post_front")
render("post_front_collider", only_collision=True, loc=(0.0, -6.0, 1.0), target=(0.12, 0, 0.9), lens=50)
