# Opens the real Blender window on the real post, saves Blender's own screenshot of its UI, quits.
import bpy, os, runpy, sys
out = sys.argv[sys.argv.index("--") + 1]
here = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(here, "scratch", "tools", "blender", "build_checkpoint_post.py"), run_name="__main__")
def shot():
    win = bpy.context.window_manager.windows[0]
    # frame the 3D view on the post
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(window=win, area=area, region=[r for r in area.regions if r.type == 'WINDOW'][0]):
                bpy.ops.view3d.view_all()
            space = area.spaces.active
            space.shading.type = 'SOLID'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Collision-convcolonly'].hide_set(True)
    win.cursor_warp(3300, 1900)
    def snap():
        bpy.ops.screen.screenshot(filepath=out)
        print("SCREENSHOT", out)
        bpy.ops.wm.quit_blender()
        return None
    bpy.app.timers.register(snap, first_interval=2.5)
    return None
bpy.app.timers.register(shot, first_interval=2.0)
