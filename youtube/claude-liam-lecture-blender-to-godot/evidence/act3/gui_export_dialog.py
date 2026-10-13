# ACT III capture (B24): Blender 5.1.2's own glTF 2.0 export dialog (File > Export > glTF 2.0), Transform panel open.
#   export BLENDER_USER_CONFIG=<reel>/evidence/blender_config
#   Blender --enable-event-simulate --python gui_export_dialog.py -- <out.png> [off]     ('off' clicks the +Y Up checkbox once, before the shot)
#   then crop the options sidebar:  python3 -c "from PIL import Image; Image.open('<out.png>').crop((2494,170,3456,1100)).save('<crop.png>')"
import bpy, sys, os
args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0.9))
o = bpy.context.active_object; o.name = "Column"; o.scale = (0.1, 0.1, 0.9)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.context.preferences.use_preferences_save = False   # never write the scratch prefs back on quit
bpy.context.preferences.view.ui_scale = 2.0     # scratch prefs: bigger UI so a crop of the options panel stays sharp at 4K
log = lambda *a: print("[gui]", *a, flush=True)
def open_dialog():
    wm = bpy.context.window_manager
    win = wm.windows[0]
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=win, area=area, region=reg):
                r = bpy.ops.export_scene.gltf('INVOKE_DEFAULT', filepath=os.path.join(os.path.dirname(out), 'column.glb'))
                log("invoke ->", r)
    return None
def inspect():
    wm = bpy.context.window_manager
    for i, w in enumerate(wm.windows):
        log("window", i, w.width, w.height, [ (a.type, a.x, a.y, a.width, a.height, [(r.type, r.x, r.y, r.width, r.height) for r in a.regions]) for a in w.screen.areas])
    return None
def click_transform():
    wm = bpy.context.window_manager
    w = wm.windows[-1]
    x, y = 2742, 2006 - 723          # the "Transform" panel header in the options sidebar (window pixels, origin bottom-left; UI scale 2)
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    w.event_simulate(type='LEFTMOUSE', value='PRESS', x=x, y=y)
    w.event_simulate(type='LEFTMOUSE', value='RELEASE', x=x, y=y)
    log("clicked Transform")
    return None
def click_yup():
    w = bpy.context.window_manager.windows[-1]
    x, y = 2931, 2006 - 842          # the +Y Up checkbox (window pixels, origin bottom-left)
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    w.event_simulate(type='LEFTMOUSE', value='PRESS', x=x, y=y)
    w.event_simulate(type='LEFTMOUSE', value='RELEASE', x=x, y=y)
    log("clicked +Y Up")
    return None
def snap():
    wm = bpy.context.window_manager
    w = wm.windows[-1]
    with bpy.context.temp_override(window=w):
        bpy.ops.screen.screenshot(filepath=out)
    log("SCREENSHOT", out)
    bpy.ops.wm.quit_blender()
    return None
bpy.app.timers.register(open_dialog, first_interval=2.0)
bpy.app.timers.register(inspect, first_interval=4.0)
bpy.app.timers.register(click_transform, first_interval=4.5)
if 'off' in args:
    bpy.app.timers.register(click_yup, first_interval=6.0)
bpy.app.timers.register(snap, first_interval=8.0)
