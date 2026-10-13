# gui_origin.py - ACT III evidence (B25B): Blender 5.1.2's OWN window, captured with Blender's own screenshot operator.
# The finished crate (built by ../assets/build_crate.py, unchanged) sits at the world origin. The viewport shows
# X-ray on (so the crate's origin dot and the world axes can be seen through it), the Z axis line switched on, the
# sidebar closed. Nobody is at the keyboard: the window lays itself out on timers, saves one PNG and quits.
#   export BLENDER_USER_CONFIG=<reel>/evidence/act3/blender_config        (a private copy of the scratch prefs)
#   Blender --enable-event-simulate --python-exit-code 1 --python gui_origin.py -- <out.png>
import bpy, sys, os, math, runpy
from mathutils import Euler, Vector

out = sys.argv[sys.argv.index("--") + 1]
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "..", "assets")
prefs = bpy.context.preferences
prefs.view.ui_scale = 2.0
prefs.view.show_splash = False
prefs.view.show_statusbar_stats = False

ns = runpy.run_path(os.path.join(assets, "build_crate.py"), run_name="lib")   # defines build(); does not export
obj, n_shapes = ns["build"](join=True)
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
log = lambda *a: print("[gui]", *a, flush=True)
VIEW_EULER_DEG = (64, 0, 35)          # tilt from straight down, roll, turn about Z (same turn as the film's crate render)
CENTRE = (0.0, 0.0, 0.32)             # world point kept in the middle of the viewport
HEIGHT_PX = 520                       # on-screen size (px) of 0.5 m


def view3d():
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            return win, area, [r for r in area.regions if r.type == 'WINDOW'][0]


def dismiss_splash():
    win = bpy.context.window_manager.windows[0]
    win.event_simulate(type='ESC', value='PRESS')
    win.event_simulate(type='ESC', value='RELEASE')
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=3300, y=60)
    return None


def prep():
    win, area, reg = view3d()
    sp = area.spaces.active
    sp.shading.type = 'SOLID'
    sp.shading.show_xray = True                 # X-ray: see the origin and the axes through the crate
    sp.shading.xray_alpha = 0.5
    sp.overlay.show_axis_x = True
    sp.overlay.show_axis_y = True
    sp.overlay.show_axis_z = True               # the Z axis line is off by default; switched on here
    sp.show_region_ui = False                   # sidebar closed
    sp.show_region_toolbar = False
    sp.show_region_tool_header = False
    r3 = sp.region_3d
    r3.view_perspective = 'PERSP'
    r3.view_rotation = Euler(tuple(math.radians(v) for v in VIEW_EULER_DEG), 'XYZ').to_quaternion()
    log("prep done | xray", sp.shading.show_xray, "| axes x/y/z", sp.overlay.show_axis_x, sp.overlay.show_axis_y, sp.overlay.show_axis_z)
    return None


def place():
    from bpy_extras.view3d_utils import location_3d_to_region_2d as proj
    win, area, reg = view3d()
    r3 = area.spaces.active.region_3d
    c = Vector(CENTRE)
    p = proj(reg, r3, c)
    right = r3.view_rotation @ Vector((1, 0, 0))
    up = r3.view_rotation @ Vector((0, 1, 0))
    ppm_x = proj(reg, r3, c + right).x - p.x
    ppm_y = proj(reg, r3, c + up).y - p.y
    tx, ty = reg.width / 2, reg.height / 2
    r3.view_location -= right * ((tx - p.x) / ppm_x) + up * ((ty - p.y) / ppm_y)
    r3.view_distance *= (ppm_x * 0.5) / HEIGHT_PX
    log("place: centre at region px", tuple(round(v) for v in p), "-> asked", (round(tx), round(ty)), "view_distance", round(r3.view_distance, 3))
    return None


def snap():
    from bpy_extras.view3d_utils import location_3d_to_region_2d as proj
    win, area, reg = view3d()
    r3 = area.spaces.active.region_3d
    o = bpy.context.object
    log("window", win.width, win.height, "ui_scale", prefs.view.ui_scale)
    log("viewport WINDOW region x", reg.x, "y", reg.y, "w", reg.width, "h", reg.height, "(window px, origin bottom-left)")
    for name, pt in (("world origin (0,0,0)", (0, 0, 0)), ("crate top centre (0,0,0.8)", (0, 0, 0.8)),
                     ("X axis +1 m", (1, 0, 0)), ("Y axis +1 m", (0, 1, 0))):
        q = proj(reg, r3, Vector(pt))
        H = win.height * 2                      # window is in points; regions and the screenshot are in pixels (2x on this Mac)
        log("projected", name, "-> screenshot px x", round(reg.x + q.x), "y_from_top", round(H - (reg.y + q.y)))
    zs = [(o.matrix_world @ v.co).z for v in o.data.vertices]
    log("active", o.name, "mode", o.mode, "dims", tuple(round(v, 4) for v in o.dimensions), "origin at", tuple(round(v, 4) for v in o.location),
        "lowest point z", round(min(zs), 4), "rot", tuple(o.rotation_euler), "scale", tuple(o.scale))
    bpy.ops.screen.screenshot(filepath=out)
    log("SCREENSHOT", out)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(dismiss_splash, first_interval=1.0)
bpy.app.timers.register(prep, first_interval=2.0)
for _t in (3.5, 4.3, 5.1, 5.9):
    bpy.app.timers.register(place, first_interval=_t)
bpy.app.timers.register(snap, first_interval=8.0)
