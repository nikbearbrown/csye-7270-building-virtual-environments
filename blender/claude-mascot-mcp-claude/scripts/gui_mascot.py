# gui_mascot.py - real Blender 5.1.2 window screenshots of the MCP-built mascot (the .blend Claude saved through the MCP), with the real MCP for Blender add-on enabled.
# Scratch profile only. Usage (from mcp-run/):
#   BLENDER_USER_CONFIG=<scratch>/blender-config BLENDER_USER_SCRIPTS=<scratch>/blender-scripts \
#   Blender <claude_mascot_mcp.blend> --enable-event-simulate --python gui_mascot.py -- <out.png> [click=x,y,label ...] [prefs]
import bpy, sys, math

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
clicks = [a[6:].split(",") for a in args[1:] if a.startswith("click=")]
want_prefs = "prefs" in args
prefs = bpy.context.preferences
prefs.view.ui_scale = 2.0
prefs.view.show_splash = False
log = lambda *a: print("[gui]", *a, flush=True)
win0 = lambda: bpy.context.window_manager.windows[0]


def dismiss():
    w = win0()
    w.event_simulate(type='ESC', value='PRESS'); w.event_simulate(type='ESC', value='RELEASE')
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=1700, y=900)
    return None


def enable_addon():
    try:
        bpy.ops.preferences.addon_enable(module="blender_mcp")
        log("addon enabled:", "blender_mcp" in bpy.context.preferences.addons)
    except Exception as e:
        log("addon enable error", repr(e))
    return None


def setup_view():
    w = win0()
    for area in w.screen.areas:
        if area.type == 'VIEW_3D':
            sp = area.spaces[0]
            sp.show_region_ui = ("nosidebar" not in args)
            sp.shading.type = 'SOLID'; sp.shading.color_type = 'MATERIAL'; sp.shading.light = 'STUDIO'
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=w, area=area, region=reg):
                bpy.ops.view3d.view_axis(type='FRONT')
                bpy.ops.view3d.view_orbit(angle=math.radians(28), type='ORBITRIGHT')
                bpy.ops.view3d.view_orbit(angle=math.radians(14), type='ORBITUP')
            sp.region_3d.view_perspective = 'PERSP'
            sp.region_3d.view_location = (0, 0, 0.43)
            sp.region_3d.view_distance = 3.4
        if area.type == 'OUTLINER':
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=w, area=area, region=reg):
                for _ in range(2):
                    bpy.ops.outliner.expanded_toggle()
    for a in w.screen.areas:
        log("area", a.type, a.x, a.y, a.width, a.height, [(r.type, r.x, r.y, r.width, r.height) for r in a.regions if r.width > 1 and r.height > 1])
    return None


def do_click(x, y, what):
    x, y = int(x), int(y)
    ev = lambda typ, val: (win0().event_simulate(type=typ, value=val, x=x, y=y), None)[1]
    bpy.app.timers.register(lambda: ev('MOUSEMOVE', 'NOTHING'), first_interval=0.05)
    bpy.app.timers.register(lambda: ev('MOUSEMOVE', 'NOTHING'), first_interval=0.35)
    bpy.app.timers.register(lambda: ev('LEFTMOUSE', 'PRESS'), first_interval=0.7)
    bpy.app.timers.register(lambda: ev('LEFTMOUSE', 'RELEASE'), first_interval=0.9)
    log("clicking", what, (x, y))
    return None


def open_prefs():
    with bpy.context.temp_override(window=win0()):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
    return None


def probe():
    w = win0()
    for a in w.screen.areas:
        if a.type == 'VIEW_3D':
            for r in a.regions:
                if r.type == 'UI': log('UI region category now:', r.active_panel_category, '| window', w.width, w.height)
    return None


def redraw():
    w = win0()
    for a in w.screen.areas:
        a.tag_redraw()
    with bpy.context.temp_override(window=w):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
    return None


def snap():
    ws = bpy.context.window_manager.windows
    w = ws[-1]
    with bpy.context.temp_override(window=w):
        bpy.ops.screen.screenshot(filepath=out)
    log("screenshot ->", out, "windows:", len(ws))
    return None


def quit_():
    bpy.ops.wm.quit_blender()
    return None


t = 2.0
bpy.app.timers.register(dismiss, first_interval=t); t += 1.5
bpy.app.timers.register(enable_addon, first_interval=t); t += 2.5
bpy.app.timers.register(setup_view, first_interval=t); t += 2.0
if want_prefs:
    bpy.app.timers.register(open_prefs, first_interval=t); t += 2.5
for x, y, what in clicks:
    bpy.app.timers.register(lambda x=x, y=y, what=what: do_click(x, y, what), first_interval=t); t += 1.5
bpy.app.timers.register(probe, first_interval=t); t += 0.5
bpy.app.timers.register(redraw, first_interval=t); t += 1.0
bpy.app.timers.register(snap, first_interval=t); t += 2.0
bpy.app.timers.register(quit_, first_interval=t)
