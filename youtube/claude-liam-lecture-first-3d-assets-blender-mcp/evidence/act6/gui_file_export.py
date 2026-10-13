# gui_file_export.py - Blender 5.1.2's own window with the top bar's File menu open and its Export submenu showing
# "glTF 2.0 (.glb/.gltf)": the route the narration names (File > Export > glTF 2.0). Scratch prefs (a COPY of the reel's
# evidence/blender_config, kept in evidence/act6/blender_config), UI scale 2, same lantern and same window as act II's shots.
#   export BLENDER_USER_CONFIG=<reel>/evidence/act6/blender_config
#   Blender --enable-event-simulate --python gui_file_export.py -- <out.png> <x1> <y1> [<x2> <y2> ...]
# The run that made pantry/a6_bl_file_export.png is run_file_export.sh: A6_OPEN=click (a simulated left click on the word
# "File"), the pointer glides to (200,1880) then to the "Export" row (300,738) (window pixels, origin bottom-left), and
# A6_KEYS=RIGHT_ARROW opens the Export submenu (a glide or a click on the row did not open it under event simulation).
# Other switches, kept because the calibration runs used them: A6_OPEN=call (wm.call_menu; never showed the File menu),
# A6_CLICK=<i> (click at hover point i), A6_HOVER0 / A6_SNAPWAIT (timer delays). Nothing inside the submenu is clicked;
# nothing is exported; Blender quits by itself.
import bpy, sys, os, runpy

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
hov = [float(a) for a in args[1:]]
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
win = lambda: bpy.context.window_manager.windows[0]


def dismiss_splash():
    w = win()
    w.event_simulate(type='ESC', value='PRESS')
    w.event_simulate(type='ESC', value='RELEASE')
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=3300, y=60)
    return None


def frame_lantern():
    w = win()
    for area in w.screen.areas:
        if area.type == 'VIEW_3D':
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=w, area=area, region=reg):
                bpy.ops.view3d.view_selected()
            area.spaces.active.shading.type = 'SOLID'
    log("window", w.width, w.height, "areas", [(a.type, a.x, a.y, a.width, a.height) for a in w.screen.areas])
    return None


def to_file_word():
    w = win()
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=int(os.environ.get('A6_WX', 159)), y=int(os.environ.get('A6_WY', 2006 - 52)))     # the word "File" in the top bar
    return None


def call_file_menu():
    """Open the File menu. A6_OPEN=click (default): a simulated left click on the word "File", as a person opens it;
    A6_OPEN=call: wm.call_menu (the way act II's Edit-menu shot was made)."""
    w = win()
    if os.environ.get('A6_OPEN', 'click') == 'click':
        w.event_simulate(type='LEFTMOUSE', value='PRESS', x=int(os.environ.get('A6_WX', 159)), y=2006 - 52)
        w.event_simulate(type='LEFTMOUSE', value='RELEASE', x=int(os.environ.get('A6_WX', 159)), y=2006 - 52)
        log("clicked File")
    else:
        with bpy.context.temp_override(window=w):
            r = bpy.ops.wm.call_menu(name=os.environ.get('A6_MENU', 'TOPBAR_MT_file'))
        log("call_menu ->", r)
    return None


def hover(i):
    """Glide the mouse to hover point i in small steps (a pointer that jumps can close a Blender menu)."""
    def f():
        w = win()
        x0, y0 = (159, 2006 - 52) if i == 0 else (hov[2 * i - 2], hov[2 * i - 1])
        x1, y1 = hov[2 * i], hov[2 * i + 1]
        for k in range(1, 13):
            w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=int(x0 + (x1 - x0) * k / 12), y=int(y0 + (y1 - y0) * k / 12))
        if str(i) in os.environ.get('A6_CLICK', '').split(','):        # a click on that row (opens a submenu; never an exporter)
            w.event_simulate(type='LEFTMOUSE', value='PRESS', x=int(x1), y=int(y1))
            w.event_simulate(type='LEFTMOUSE', value='RELEASE', x=int(x1), y=int(y1))
        log("hover", i, x1, y1, "click" if str(i) in os.environ.get('A6_CLICK', '').split(',') else "")
        return None
    return f


def keys():
    """Optional key presses after the last hover (A6_KEYS, e.g. RIGHT_ARROW: open the highlighted submenu, as the arrow key does)."""
    w = win()
    for k in [k for k in os.environ.get('A6_KEYS', '').split(',') if k]:
        w.event_simulate(type=k, value='PRESS')
        w.event_simulate(type=k, value='RELEASE')
        log("key", k)
    return None


def snap():
    with bpy.context.temp_override(window=win()):
        bpy.ops.screen.screenshot(filepath=out)
    log("SCREENSHOT", out, "window", win().width, win().height)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(dismiss_splash, first_interval=1.0)
bpy.app.timers.register(frame_lantern, first_interval=2.5)
bpy.app.timers.register(to_file_word, first_interval=3.5)
bpy.app.timers.register(call_file_menu, first_interval=4.5)
t = 4.5 + float(os.environ.get('A6_HOVER0', 1.0))
for i in range(len(hov) // 2):
    bpy.app.timers.register(hover(i), first_interval=t)
    t += 2.0
bpy.app.timers.register(keys, first_interval=t)
bpy.app.timers.register(snap, first_interval=t + float(os.environ.get('A6_SNAPWAIT', 1.5)))
