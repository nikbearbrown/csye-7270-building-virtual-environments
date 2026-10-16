# Prepares Blender's window for the "Learn the window" session (A3, step 2).
# It changes the view only, not the scene: sidebar (N) open, viewport statistics
# overlay on, Scene Statistics in the status bar, the default Cube selected.
# Optional: "-- --shot <path>" saves a window screenshot for checking the setup.
#
#   blender <scene.blend> --python tools/blender/learn_window_setup.py [-- --shot <png>]
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SHOT = argv[argv.index("--shot") + 1] if "--shot" in argv else None


def _view3d(win):
    return next(a for a in win.screen.areas if a.type == 'VIEW_3D')


def setup():
    win = bpy.context.window_manager.windows[0]
    space = _view3d(win).spaces.active
    space.show_region_ui = True          # the sidebar, same as pressing N
    space.overlay.show_stats = True      # object/vertex/face/triangle counts in the viewport
    bpy.context.preferences.view.show_statusbar_stats = True  # status bar > Scene Statistics

    cube = bpy.data.objects.get("Cube")
    if cube:
        for obj in bpy.context.view_layer.objects:
            obj.select_set(False)
        cube.select_set(True)
        bpy.context.view_layer.objects.active = cube

    if SHOT:
        bpy.app.timers.register(lambda: shot(win), first_interval=1.5)
    return None


def shot(win):
    with bpy.context.temp_override(window=win, area=_view3d(win)):
        bpy.ops.screen.screenshot(filepath=SHOT)
    print("SHOT=" + SHOT)
    return None


bpy.app.timers.register(setup, first_interval=1.0)
