# gui_prefs.py - Blender 5.1.2's own windows for the path "Edit > Preferences > Add-ons", scratch prefs, UI scale 2.
#   export BLENDER_USER_CONFIG=<reel>/evidence/blender_config
#   Blender --enable-event-simulate --python gui_prefs.py -- <out.png> menu     the Edit menu open (a click on "Edit" in the top bar)
#   Blender --enable-event-simulate --python gui_prefs.py -- <out.png> addons   the Preferences window on its Add-ons tab
# It also prints the Preferences tab names and the add-on categories this Blender knows. Nothing is installed or enabled.
import bpy, sys, os, runpy, addon_utils

out, mode = sys.argv[sys.argv.index("--") + 1:][:2]
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


def dismiss_splash():
    win = bpy.context.window_manager.windows[0]
    win.event_simulate(type='ESC', value='PRESS')
    win.event_simulate(type='ESC', value='RELEASE')
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=3300, y=60)
    return None


def facts():
    items = prefs.bl_rna.properties["active_section"].enum_items
    log("Preferences tabs (identifier = label):", [(i.identifier, i.name) for i in items])
    cats = {}
    for m in addon_utils.modules():
        bi = getattr(m, "bl_info", {}) or {}
        cats.setdefault(bi.get("category", "?"), []).append(bi.get("name", m.__name__))
    log("add-on categories among the modules this Blender lists:", sorted(cats))
    log("modules with category 'Interface':", cats.get("Interface"))
    log("enabled add-ons in this scratch config:", sorted(prefs.addons.keys()))
    log("use_online_access (System > Network > Allow Online Access):", bpy.context.preferences.system.use_online_access)
    return None


def frame_lantern():
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=win, area=area, region=reg):
                bpy.ops.view3d.view_selected()
            area.spaces.active.shading.type = 'SOLID'
    return None


def open_edit_menu():
    """The Edit menu of the top bar, opened as a click on the word 'Edit' would open it."""
    win = bpy.context.window_manager.windows[0]
    x, y = 289, 2006 - 52                    # the word "Edit" in the top bar (window pixels, origin bottom-left, UI scale 2)
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    for area in win.screen.areas:
        pass
    top = [a for a in bpy.context.window_manager.windows[0].screen.areas]
    log("areas", [a.type for a in top])
    return None


def call_edit_menu():
    win = bpy.context.window_manager.windows[0]
    with bpy.context.temp_override(window=win):
        r = bpy.ops.wm.call_menu(name='TOPBAR_MT_edit')
    log("call_menu TOPBAR_MT_edit ->", r)
    return None


def hover_preferences():
    win = bpy.context.window_manager.windows[0]
    x, y = 280, 864                          # the "Preferences..." row of the Edit menu (window pixels, origin bottom-left; calibrated by looking at the shot)
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x - 30, y=y)
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    return None


def open_prefs():
    win = bpy.context.window_manager.windows[0]
    prefs.active_section = 'ADDONS'                              # the tab the window opens on
    with bpy.context.temp_override(window=win):
        r = bpy.ops.screen.userpref_show('INVOKE_DEFAULT')       # = Edit > Preferences
    log("userpref_show ->", r)
    return None


def pick_tab():
    prefs.active_section = 'ADDONS'
    log("active_section =", prefs.active_section)
    for i, w in enumerate(bpy.context.window_manager.windows):
        log("window", i, w.width, w.height, [(a.type, a.x, a.y, a.width, a.height) for a in w.screen.areas])
    return None


def snap():
    wins = bpy.context.window_manager.windows
    w = wins[-1] if mode == "addons" else wins[0]
    with bpy.context.temp_override(window=w):
        bpy.ops.screen.screenshot(filepath=out)
    log("SCREENSHOT", out, "window", w.width, w.height)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(dismiss_splash, first_interval=1.0)
bpy.app.timers.register(facts, first_interval=2.0)
if mode == "menu":
    bpy.app.timers.register(frame_lantern, first_interval=2.5)
    bpy.app.timers.register(open_edit_menu, first_interval=3.5)
    bpy.app.timers.register(call_edit_menu, first_interval=4.5)
    bpy.app.timers.register(hover_preferences, first_interval=5.5)
    bpy.app.timers.register(snap, first_interval=9.0)
else:
    bpy.app.timers.register(open_prefs, first_interval=3.0)
    bpy.app.timers.register(pick_tab, first_interval=6.0)
    bpy.app.timers.register(snap, first_interval=8.0)
