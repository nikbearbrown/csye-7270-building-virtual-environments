# GUI NOTES - real Blender 5.1.2 windows (and the Preferences window), where each interface part sits

**Every image here is Blender's own window, saved by Blender's own screenshot operator (`bpy.ops.screen.screenshot`), by a script, not by a person.**
No human was at the keyboard: the lantern or crate is built by `../assets/build_*.py`, then the window is laid out and photographed by `gui_shots.py` on timers, and
Blender quits by itself. The hand-edit pair (`ev_bl_hand_edit_before/after`) in particular is **produced by script and must be labelled illustrative**.

Settings for every shot: scratch config (`BLENDER_USER_CONFIG=evidence/blender_config`, never your real Blender prefs), `ui_scale = 2.0`, splash screen off
(`show_splash = False`; the first start with an empty scratch config shows the splash, which the script dismisses with Esc), `--enable-event-simulate`.
Window 3456 x 2006 px (1728 x 1003 points on this Mac). Coordinates below are **pixels in the saved PNG, origin top-left, x0,y0,x1,y1**.

Run all: `evidence/gui/run_gui_shots.sh` (one window at a time, each closes itself); logs `gui_<mode>.log` hold the area/region rectangles Blender reports and the
object numbers; export dialog `gui_export_gltf.py`; Edit menu and Preferences `gui_prefs.py`.

## How the layout was set (so it can be reproduced)

At UI scale 2 the default layout of a 1728-point window is cramped (the sidebar would cover the model, the Outliner shows one row). `gui_shots.py` therefore:
opens the sidebar (`space.show_region_ui = True` = pressing N; it opens on its **Item** tab), hides the tool-settings row, drags the right-hand column 400 px wider and the
Outliner/Properties edge 500 px lower using simulated mouse drags (the same as dragging the edges by hand), puts the Properties editor on its Material tab (Object tab for
the crate), expands the Outliner one level, and pans/zooms the viewport so the model sits between the toolbar and the sidebar. The sidebar stays at Blender's default width
(1122 px here; narrowing it by a simulated drag did not work). The Timeline strip under the viewport is left as it is.

## Where the six interface parts are (identical in every Blender-window shot below)

| part | box | notes |
|---|---|---|
| **3D viewport** | 8,107,2432,1798 (area incl. its header); the drawing area under the header is 8,211,2432,1798; the free part where the model sits is 234,211,1310,1798 | the sidebar and toolbar are drawn OVER the left and right of it (Region Overlap on, Blender's default) |
| **Toolbar** | region 8,211,234,1798; the visible icon strip is about 40,240,230,1570 | select box, cursor, move, rotate, scale, transform, annotate, measure, add cube |
| **Outliner** | 2447,107,3448,932 | Scene Collection > Collection > Lantern > mesh data (tree). In `ev_bl_object_mode_parts.png` it lists five objects |
| **Properties editor** | 2447,947,3448,1911 (its header is 2447,947,3448,1051 and its tab column is 2447,1051,2565,1911) | Material tab: DarkIron, WarmGlass, Flame (Object tab for the crate) |
| **Sidebar (N)** | region 1310,211,2432,1798; the visible panel is about 1322,222,2320,1780; the tab strip Item / Tool / View / Animation is about 2350,225,2432,1000 | Item tab, "Transform" panel |
| **Mode selector** | Object Mode: 190,120,612,196. Edit Mode: 190,120,558,196, with the three select-mode buttons beside it at 585,120,820,196 | in the viewport header (the editor-type dropdown to its left is 42,120,168,196) |

Inside the sidebar's Transform panel (object mode): **Location** 1378,365,2300,672; **Rotation** 1378,700,2300,1095 (incl. the "XYZ Euler" dropdown); **Scale** 1378,1105,2300,1408;
**Dimensions** 1378,1440,2300,1748. Top bar (File, Edit, Render, Window, Help, workspace tabs): y 0 to 105. Timeline strip: 8,1813,2432,1911. Status bar: y 1911 to 2006.

## The images

**(a) `pantry/ev_bl_object_mode.png`** - the finished lantern (one joined object "Lantern", selected: orange selection outline, origin dot at the centre of its underside), sidebar open on
the Item tab. All six parts visible at the boxes above. The sidebar reads Location 0 m, 0 m, 0 m; Rotation 0, 0, 0; Scale 1.000 x3; **Dimensions 0.3 m, 0.3 m, 0.5 m**.
Mode selector shows "Object Mode". Status bar shows no statistics (they are off here). Source numbers: `gui_object.log`.

**(a2) `pantry/ev_bl_object_mode_parts.png`** - the same window before the parts are joined: the Outliner lists the five objects Lantern_Base, Lantern_Finial, Lantern_Flame, Lantern_Glass,
Lantern_Roof (use it for "the Outliner lists every object"). The Lantern_Roof is active: Location Z 0.42 m, Dimensions 0.28 x 0.28 x 0.1 m. Status bar shows statistics here too only if they are
on; they are off.

**(b) `pantry/ev_bl_edit_mode.png`** - the finished crate in **Edit Mode**: the header's mode selector reads "Edit Mode" (190,120,558,196) and vertex select mode is on; vertices are the black
dots, and the 12 vertices of the top plane are selected (orange). The sidebar shows "Median" 0 m, 0 m, 0.8 m for the selection; the Outliner shows Crate; the Properties editor is on its Object tab.
Edit-mode statistics (log): Verts 12/40, Edges 12/60, Faces 3/30, Tris 60.

**(c) `pantry/ev_bl_status_stats.png`** - Scene Statistics switched on in the status bar. The status bar reads **"Collection | Lantern | Verts:111 | Faces:91 | Tris:202 | Objects:1/1"**: the text
spans about 1853,1936,3160,1984 and the Tris item about 2722,1936,2895,1984. **Tris:202 equals the script's printed 202.** How it is switched on: Blender's status-bar right-click menu
> Scene Statistics toggles the preference `bpy.context.preferences.view.show_statusbar_stats` (Preferences > Interface > Status Bar > Scene Statistics). The script sets that preference directly
(`prefs.view.show_statusbar_stats = True`); the right-click menu itself was not clicked in these runs. In the other shots the script sets it to False so they are comparable.

**(d) `pantry/ev_bl_export_gltf.png`** - the glTF export dialog, which is a second Blender window (file browser with the exporter options), made by invoking the operator that File > Export > glTF 2.0
runs (`bpy.ops.export_scene.gltf('INVOKE_DEFAULT')`; the menu entry itself was not clicked), Transform panel opened by a simulated click. Image is the dialog window only (3456 x 2006):
Format "glTF Binary (.glb)" at 2905,300,3420,385 (the default in 5.1.2), the panels Include / Transform / Data / Animation in the right-hand column, the Transform panel at 2560,700,3456,900 with the **"+Y Up" checkbox, ticked, at 2895,800,3110,885** (the default), the file name field "lantern.glb" bottom left, and the blue **"Export glTF 2.0"** button bottom right (2916,1870,3421,1970). Nothing is written: Export is never clicked.
Not visible in this image: the six interface parts of the main window (it is a different window).

## Extra images asked for in the second brief

**(E11) `pantry/ev_bl_edit_menu.png`** - the top bar's **Edit** menu open over the lantern, "Preferences..." highlighted (shortcut shown as Cmd+,). Menu box about 13,58,731,1196; the Preferences row about
13,1098,718,1190. (Opened with `bpy.ops.wm.call_menu(name='TOPBAR_MT_edit')`, the same menu a click on "Edit" opens. In this default layout the Properties editor's value fields look blank only because that column is too
narrow at UI scale 2.)

**(E11) `pantry/ev_bl_prefs_addons.png`** - the Preferences window (3360 x 2006) on the tab called **"Add-ons"**. In Blender 5.1.2 the left column reads: Interface, Viewport, Lights, Editing, Animation | **Get Extensions** |
**Add-ons**, Themes | Input, Navigation, Keymap | System, Save & Load, File Paths (Developer Tools and Experimental appear only with Developer Extras on). The "Add-ons" button is at about 36,843,605,938.
The list (about 677,155,3327,1810) has a "Search Add-ons" box, an "Enabled Only" checkbox and a tag filter; **each row shows only the add-on's name (for example "glTF 2.0 format", "Cycles Render Engine", "Node Wrangler", "Rigify"),
with no "Category:" prefix**. Rows in this scratch config: BioVision Motion Capture (BVH) format, Cycles Render Engine, FBX format, glTF 2.0 format, Hydra Storm render engine, Manage UI translations, Node Wrangler,
Pose Library, Rigify, Scalable Vector Graphics (SVG) 1.1 format, UV Layout, VR Scene Inspection. Printed by the script (`gui_prefs_addons.log`): the tab identifiers are INTERFACE, VIEWPORT, LIGHTS, EDITING, ANIMATION,
EXTENSIONS ("Get Extensions"), ADDONS ("Add-ons"), THEMES, INPUT, NAVIGATION, KEYMAP, SYSTEM, SAVE_LOAD, FILE_PATHS, DEVELOPER_TOOLS, EXPERIMENTAL; the add-on categories among the modules this Blender lists are
3D View, Animation, Import-Export, Node, Render, Rigging, System (no "Interface"); `System > Network > Allow Online Access` is **False** by default.
**Would "Interface: MCP for Blender" appear?** The MCP add-on declares `"name": "MCP for Blender"`, `"category": "Interface"` (`../mcp/addon-0927.py` lines 31-40). Blender 5.1.2's list shows the name without a category
prefix, so a student should look for a row named **"MCP for Blender"** (this is an inference from the code and this list; the add-on was not installed or enabled).

**(E12) `pantry/ev_bl_hand_edit_before.png` / `ev_bl_hand_edit_after.png`** - the five-object lantern with **Lantern_Flame** selected. Before: Location Z 0.32 m, flame orange. After: the flame nudged up 0.02 m
(Location Z **0.34 m**) and its colour changed to blue (#3FA9FF; visible on the flame in the viewport and as the blue swatch in the Properties material list). Both are Blender's own window, same layout as (a), with
the Outliner listing the five objects. **Made by script, so the film should label them illustrative**, not a recording of a person.

**(E13) `pantry/ev_bl_orbit_1.png`, `_2.png`, `_3.png`, `_4.png`** - the finished lantern, selected, same window and layout, viewport angle changed: 1 front (view rotation 90, 0, 0), 2 three-quarter (68, 0, 35), 3 top
(0, 0, 0), 4 the three-quarter view zoomed in. The model sits in 234,211,1310,1798 in each; everything else is unchanged, so they cross-fade cleanly. (Blender's header still says "User Perspective"
because the view was set by script, not by a numpad key.)
