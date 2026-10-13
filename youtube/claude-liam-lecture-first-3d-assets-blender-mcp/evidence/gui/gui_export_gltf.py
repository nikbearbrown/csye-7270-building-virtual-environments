# gui_export_gltf.py - Blender 5.1.2's own File > Export > glTF 2.0 dialog over the finished lantern, scratch prefs, UI scale 2.
# Method follows the sibling film's gui_export_dialog.py (the dialog is a second window; its screenshot is taken with that window as context).
#   export BLENDER_USER_CONFIG=<reel>/evidence/blender_config
#   Blender --enable-event-simulate --python gui_export_gltf.py -- <out.png> [open_transform] [click_transform_at=x,y]
import bpy, sys, os, runpy

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
here = os.path.dirname(os.path.abspath(__file__))
prefs = bpy.context.preferences
prefs.view.ui_scale = 2.0
prefs.view.show_splash = False
prefs.view.show_statusbar_stats = False
ns = runpy.run_path(os.path.join(here, "..", "assets", "build_lantern.py"), run_name="lib")
obj, n = ns["build"]()
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
log = lambda *a: print("[gui]", *a, flush=True)
dest = os.path.join(here, "lantern.glb")                                            # this folder holds no .glb, so the button reads "Export glTF 2.0";           # the dialog is only looked at: Export is never clicked


def dismiss_splash():
    win = bpy.context.window_manager.windows[0]
    win.event_simulate(type='ESC', value='PRESS')
    win.event_simulate(type='ESC', value='RELEASE')
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=3300, y=60)
    return None


def open_dialog():
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=win, area=area, region=reg):
                r = bpy.ops.export_scene.gltf('INVOKE_DEFAULT', filepath=dest)      # = File > Export > glTF 2.0 (.glb/.gltf)
                log("invoke ->", r)
    return None


def inspect():
    for i, w in enumerate(bpy.context.window_manager.windows):
        log("window", i, w.width, w.height, [(a.type, a.x, a.y, a.width, a.height,
                                              [(r.type, r.x, r.y, r.width, r.height) for r in a.regions if r.width > 1 and r.height > 1]) for a in w.screen.areas])
    return None


def click(x, y, what):
    w = bpy.context.window_manager.windows[-1]
    h = w.height
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    w.event_simulate(type='LEFTMOUSE', value='PRESS', x=x, y=y)
    w.event_simulate(type='LEFTMOUSE', value='RELEASE', x=x, y=y)
    log("clicked", what, (x, y))


def snap():
    w = bpy.context.window_manager.windows[-1]
    with bpy.context.temp_override(window=w):
        bpy.ops.screen.screenshot(filepath=out)
    log("SCREENSHOT", out, "window", w.width, w.height)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(dismiss_splash, first_interval=1.0)
bpy.app.timers.register(open_dialog, first_interval=2.5)
bpy.app.timers.register(inspect, first_interval=5.0)
for a in args[1:]:
    if a.startswith("click="):                        # click=x,y,label   (window pixels, origin bottom-left)
        x, y, label = a[6:].split(",")
        bpy.app.timers.register(lambda x=int(x), y=int(y), label=label: click(x, y, label), first_interval=6.0)
bpy.app.timers.register(snap, first_interval=9.0)
