# ACT III capture (B26, B29): Blender 5.1.2's own window over the real column: the Properties > Object > Transform panel
# (Location / Rotation / Scale), and the Object > Apply menu (Ctrl+A opens this same menu).
#   export BLENDER_USER_CONFIG=<reel>/evidence/blender_config
#   Blender --python gui_blender_shots.py -- <out.png> before|menu|after|props_cube|props_before|props_after [cursor_x cursor_y]
#   (props_*: the Properties editor maximised, so the Transform panel is wide and sharp)
import bpy, sys, os
_a = sys.argv[sys.argv.index("--") + 1:]
out, mode = _a[:2]
CUR = (int(_a[2]), int(_a[3])) if len(_a) > 3 else (900, 900)   # where the pointer rests before the menu opens (window px)
bpy.context.preferences.use_preferences_save = False   # never write the scratch prefs back on quit
bpy.context.preferences.view.ui_scale = 2.0          # scratch prefs: bigger UI so crops stay sharp at 4K
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0.9))
o = bpy.context.active_object; o.name = "Column"
if mode != "props_cube":                              # props_cube: the 2 m cube as added, scale 1
    o.scale = (0.1, 0.1, 0.9)
if mode in ("after", "props_after"):
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
o.select_set(True)
def view_area():
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            return win, area, [r for r in area.regions if r.type == 'WINDOW'][0]
def frame():
    win, area, reg = view_area()
    with bpy.context.temp_override(window=win, area=area, region=reg):
        bpy.ops.view3d.view_selected()
    area.spaces.active.shading.type = 'SOLID'
    win.cursor_warp(CUR[0], CUR[1])
    return None
def open_menu():
    win, area, reg = view_area()
    with bpy.context.temp_override(window=win, area=area, region=reg):
        bpy.ops.wm.call_menu(name="VIEW3D_MT_object_apply")
    return None
def hover_item():
    w = bpy.context.window_manager.windows[0]
    x, y = 420, 2006 - 653           # the 'Apply' title row of the menu: the pointer rests there, so no item is highlighted
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x - 40, y=y)
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x, y=y)
    return None
def maximise_props():
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == 'PROPERTIES':
            reg = [r for r in area.regions if r.type == 'WINDOW'][0]
            with bpy.context.temp_override(window=win, area=area, region=reg):
                bpy.ops.screen.screen_full_area()
            return None
    return None
def snap():
    bpy.ops.screen.screenshot(filepath=out)
    print("SCREENSHOT", out, flush=True)
    bpy.ops.wm.quit_blender()
    return None
bpy.app.timers.register(frame, first_interval=1.5)
if mode == "menu":
    bpy.app.timers.register(open_menu, first_interval=3.0)
if mode.startswith("props"):
    bpy.app.timers.register(maximise_props, first_interval=3.0)
bpy.app.timers.register(snap, first_interval=6.0)
