# gui_shots.py - Blender 5.1.2's OWN window, captured with Blender's own screenshot operator, on the assets built by
# ../assets/build_*.py. Scratch preferences only, UI scale 2 so crops stay sharp at 4K.
#   export BLENDER_USER_CONFIG=<reel>/evidence/blender_config
#   Blender --enable-event-simulate --python gui_shots.py -- <out.png> <mode>
#   mode: object  the finished lantern (one joined object), selected, sidebar open on the Item tab, Material tab in Properties
#         parts   the same lantern BEFORE joining: five objects in the Outliner, the roof active
#         edit    the finished crate in Edit Mode, vertices visible (nothing selected)
#         stats   the finished lantern with Scene Statistics switched on in the status bar
#         hand_before / hand_after   the five-object lantern, the flame selected; "after" = the flame nudged up 0.02 m and its colour changed
#                                    (made by script: no human is at the keyboard, so the film must call it illustrative)
#         orbit1 .. orbit4   the finished lantern from the front, three-quarter, top, and three-quarter zoomed in (same window, same layout)
# The window opens for about eight seconds, saves one PNG, prints the area/region rectangles, and quits by itself.
import bpy, sys, os, math, runpy
from mathutils import Euler

out, mode = sys.argv[sys.argv.index("--") + 1:][:2]
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "..", "assets")
prefs = bpy.context.preferences
prefs.view.ui_scale = 2.0                       # scratch prefs: bigger UI so crops stay sharp at 4K
prefs.view.show_splash = False                  # scratch prefs: no splash screen on the next start
# Scene Statistics in the status bar = right-click the status bar > Scene Statistics = Preferences > Interface > Status Bar > Scene Statistics
prefs.view.show_statusbar_stats = (mode == "stats")

asset = "crate" if mode == "edit" else "lantern"
PARTS_MODES = ("parts", "hand_before", "hand_after")
CENTRE = (0.0, 0.0, 0.4) if asset == "crate" else (0.0, 0.0, 0.25)       # world point to keep in the middle of the free viewport
VIEW_EULER_DEG = {"orbit1": (90, 0, 0), "orbit3": (0, 0, 0)}.get(mode, (68, 0, 35) if asset == "lantern" else (58, 0, 35))   # viewport angle (deg): tilt from straight down, roll, turn about Z
HEIGHT_PX = {"orbit3": 1100, "orbit4": 1100}.get(mode, 760 if asset == "lantern" else 360)                                  # on-screen size (px) of 0.5 m of the object
ns = runpy.run_path(os.path.join(assets, "build_%s.py" % asset), run_name="lib")   # defines build(); does not export
obj, n_shapes = ns["build"](join=(mode not in PARTS_MODES))
if mode in PARTS_MODES:
    parts = obj
    bpy.ops.object.select_all(action='DESELECT')
    active = [p for p in parts if p.name.endswith("Flame" if mode.startswith("hand") else "Roof")][0]
    if mode == "hand_after":
        active.location.z += 0.02                                   # nudged up by 0.02 m
        m = active.active_material
        lin = ns["srgb_to_linear"]
        blue = tuple(lin(int("#3FA9FF"[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1.0,)
        m.diffuse_color = blue                                     # viewport colour
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = blue   # exported colour: flame turns blue
    active.select_set(True)
    bpy.context.view_layer.objects.active = active
else:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
log = lambda *a: print("[gui]", *a, flush=True)


def view3d():
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == 'VIEW_3D':
            return win, area, [r for r in area.regions if r.type == 'WINDOW'][0]


def area_of(kind):
    win = bpy.context.window_manager.windows[0]
    for area in win.screen.areas:
        if area.type == kind:
            return win, area, [r for r in area.regions if r.type == 'WINDOW'][0]


def dismiss_splash():
    """The splash of the first start with a fresh scratch config: Escape, then move the pointer off it."""
    win = bpy.context.window_manager.windows[0]
    win.event_simulate(type='ESC', value='PRESS')
    win.event_simulate(type='ESC', value='RELEASE')
    win.event_simulate(type='MOUSEMOVE', value='NOTHING', x=3300, y=60)
    return None


def drag(x0, y0, x1, y1, steps=6):
    """Press on an area edge, pull it, release (window pixels, origin bottom-left). screen.area_move is not callable from a script here."""
    w = bpy.context.window_manager.windows[0]
    w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=x0, y=y0)
    w.event_simulate(type='LEFTMOUSE', value='PRESS', x=x0, y=y0)
    for i in range(1, steps + 1):
        w.event_simulate(type='MOUSEMOVE', value='NOTHING', x=int(x0 + (x1 - x0) * i / steps), y=int(y0 + (y1 - y0) * i / steps))
    w.event_simulate(type='LEFTMOUSE', value='RELEASE', x=x1, y=y1)
    log("drag", (x0, y0), "->", (x1, y1))


def layout_columns():
    """At UI scale 2 on a 1728-point window the default layout is cramped: widen the right-hand column ..."""
    w, a3, _ = view3d()
    drag(a3.x + a3.width + 7, 1000, a3.x + a3.width + 7 - 400, 1000)
    return None


def layout_outliner():
    """... and give the Outliner room (pull the Outliner/Properties edge down)."""
    ol = area_of('OUTLINER')[1]
    drag(ol.x + 150, ol.y - 7, ol.x + 150, ol.y - 7 - 500)
    return None


def layout_sidebar():
    """... and narrow the 3D viewport's sidebar (drag its left edge to the right)."""
    w, a3, _ = view3d()
    ui = [r for r in a3.regions if r.type == 'UI'][0]
    drag(ui.x + 34, 1000, ui.x + 34 + 420, 1000)
    return None


def place_object(centre, target_px, height_px):
    """Pan and zoom the viewport until the object's centre sits at target_px (region pixels) and 0.5 m of it spans ~height_px."""
    from bpy_extras.view3d_utils import location_3d_to_region_2d as proj
    from mathutils import Vector
    win, area, reg = view3d()
    r3 = area.spaces.active.region_3d
    for _ in range(1):
        c = Vector(centre)
        p = proj(reg, r3, c)
        right = r3.view_rotation @ Vector((1, 0, 0))
        up = r3.view_rotation @ Vector((0, 1, 0))
        ppm_x = proj(reg, r3, c + right).x - p.x
        ppm_y = proj(reg, r3, c + up).y - p.y
        r3.view_location -= right * ((target_px[0] - p.x) / ppm_x) + up * ((target_px[1] - p.y) / ppm_y)
        r3.view_distance *= (ppm_x * 0.5) / height_px          # nearer when the object is too small, and the other way round
    log("place_object: centre at region px", tuple(round(v) for v in p), "-> asked", tuple(round(v) for v in target_px), "view_distance", round(r3.view_distance, 3), "px per m", round(ppm_x))


def prep():
    win, area, reg = view3d()
    sp = area.spaces.active
    sp.shading.type = 'SOLID'
    sp.show_region_ui = True                    # the sidebar (N); it opens on its Item tab
    sp.show_region_toolbar = True
    sp.show_region_tool_header = False          # the 'select mode' row: not needed, and the sidebar needs the height
    r3 = sp.region_3d
    r3.view_perspective = 'PERSP'
    r3.view_rotation = Euler(VIEW_EULER_DEG and tuple(math.radians(v) for v in VIEW_EULER_DEG), 'XYZ').to_quaternion()
    log("prep done")
    return None


PLACE = None


def place_step():
    place_object(*PLACE)
    return None


def setup():
    win, area, reg = view3d()
    sp = area.spaces.active
    r3 = sp.region_3d
    with bpy.context.temp_override(window=win, area=area, region=reg):
        bpy.ops.view3d.view_selected()
    # free part of the viewport: right of the toolbar, left of the sidebar (they overlap it)
    tools = [r for r in area.regions if r.type == 'TOOLS'][0]
    ui = [r for r in area.regions if r.type == 'UI'][0]
    win_r = [r for r in area.regions if r.type == 'WINDOW'][0]
    free_x0, free_x1 = tools.x + tools.width - win_r.x, ui.x - win_r.x
    global PLACE
    PLACE = (CENTRE, ((free_x0 + free_x1) / 2, win_r.height * 0.5), HEIGHT_PX)
    # Properties editor: Material tab (or Object tab for the crate)
    w2, pa, pr = area_of('PROPERTIES')
    pa.spaces.active.context = 'MATERIAL' if mode != "edit" else 'OBJECT'
    # Outliner: open one level so the object's mesh data and materials show as a tree
    w3, oa, orr = area_of('OUTLINER')
    if mode in ("object", "stats"):
        with bpy.context.temp_override(window=w3, area=oa, region=orr):
            bpy.ops.outliner.show_one_level(open=True)
    win.cursor_warp(3300, 1900)      # park the pointer on the status bar, away from every panel
    log("setup done")
    return None


def edit_mode():
    win, area, reg = view3d()
    with bpy.context.temp_override(window=win, area=area, region=reg):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='DESELECT')
    import bmesh
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    for v in bm.verts:
        v.select_set(v.co.z > 0.79)             # the vertices of the top plane: selected = orange
    bm.select_flush_mode()
    bmesh.update_edit_mesh(me)
    log("mode ->", bpy.context.object.mode, "| selected verts", sum(v.select for v in bm.verts), "of", len(bm.verts))
    return None


def snap():
    win = bpy.context.window_manager.windows[0]
    log("window", win.width, win.height, "ui_scale", prefs.view.ui_scale)
    for a in win.screen.areas:
        log("area", a.type, "x", a.x, "y", a.y, "w", a.width, "h", a.height,
            [(r.type, r.x, r.y, r.width, r.height) for r in a.regions if r.width > 1 and r.height > 1])
    o = bpy.context.object
    log("active", o.name, "mode", o.mode, "dims", tuple(round(v, 4) for v in o.dimensions),
        "loc", tuple(o.location), "rot", tuple(o.rotation_euler), "scale", tuple(o.scale))
    st = bpy.context.scene.statistics(bpy.context.view_layer)
    log("scene statistics:", st)
    bpy.ops.screen.screenshot(filepath=out)
    log("SCREENSHOT", out)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(dismiss_splash, first_interval=1.0)
bpy.app.timers.register(prep, first_interval=2.0)
bpy.app.timers.register(layout_columns, first_interval=3.0)
bpy.app.timers.register(layout_outliner, first_interval=4.5)
bpy.app.timers.register(layout_sidebar, first_interval=6.0)
bpy.app.timers.register(setup, first_interval=8.0)
for _t in (8.8, 9.6, 10.4, 11.2):
    bpy.app.timers.register(place_step, first_interval=_t)       # one correction per redraw
if mode == "edit":
    bpy.app.timers.register(edit_mode, first_interval=11.8)
bpy.app.timers.register(snap, first_interval=15.0)
