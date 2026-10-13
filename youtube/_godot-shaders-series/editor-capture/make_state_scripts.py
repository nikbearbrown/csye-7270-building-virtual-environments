#!/usr/bin/env python3
"""Writes the final state scripts (state-scripts/final/*.json). One script = one editor session = one scene group.
Mark names are the final PNG names: <film>_<row>-<n>_<state>. Run order and settings are in run_all.sh."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state-scripts", "final")
os.makedirs(OUT, exist_ok=True)
WIN = [3456, 1944]


def wait(n):
    return {"op": "wait_frames", "n": n}


def mark(name):
    return {"op": "mark", "name": name}


def head(scene, widen=None, frame=True):
    steps = [{"op": "open_scene", "path": scene, "settle": 12}, {"op": "select_node", "node": ".", "settle": 12}]
    if frame:
        steps.append({"op": "menu_item", "button": "View", "item": "Frame Selection", "settle": 12})
    if widen:
        steps.append({"op": "dock_split", "name": "DockHSplitMain", "offsets": [560, -widen], "settle": 20})
    return steps


def save(name, steps, note=""):
    d = {"note": note, "boot_frames": 25, "window": WIN, "window_settle": 40, "steps": steps}
    json.dump(d, open(os.path.join(OUT, name + ".json"), "w"), indent=1)


# ----------------------------------------------------------------------------------------------------------------- pilot E1
S = head("res://scenes/e1_sprite.tscn")
S += [
    {"op": "unfold_group", "property": "material", "object": "node", "settle": 12},
    mark("godot-shaders_E1-1_material-empty"),
    {"op": "open_picker_menu", "property": "material", "object": "node", "settle": 6},
    {"op": "focus_menu_item", "text": "ShaderMaterial", "settle": 6},
    {"op": "dump_popup", "name": "material-dropdown-items"},
    mark("godot-shaders_E1-2a_material-dropdown-open"),
    {"op": "pick_menu_item", "text": "ShaderMaterial", "settle": 24},
    mark("godot-shaders_E1-2b_shadermaterial-in-slot"),
    {"op": "unfold_resource", "property": "material", "object": "node", "settle": 24},
    mark("godot-shaders_E1-3a_inside-shadermaterial-shader-empty"),
    {"op": "open_picker_menu", "property": "shader", "object": "material", "settle": 6},
    {"op": "focus_menu_item", "text": "New Shader...", "settle": 6},
    {"op": "dump_popup", "name": "shader-dropdown-items"},
    mark("godot-shaders_E1-3b_shader-dropdown-open"),
    {"op": "pick_menu_item", "text": "New Shader...", "settle": 30},
    {"op": "dump_windows", "name": "dialog-window"},
    mark("godot-shaders_E1-3c_create-shader-dialog-defaults"),
    {"op": "select_option", "within": {"class": "ShaderCreateDialog"}, "index": 1, "text": "Canvas Item", "settle": 8},
    {"op": "set_text", "within": {"class": "ShaderCreateDialog"}, "index": 0, "text": "res://created/dial.gdshader", "settle": 8},
    mark("godot-shaders_E1-3d_create-shader-dialog-filled"),
    {"op": "press_ok", "within": {"class": "ShaderCreateDialog"}, "settle": 50},
    mark("godot-shaders_E1-4_shader-editor-open-after-Create"),
    {"op": "dump_inspector", "name": "after-create"},
    {"op": "hide_bottom_panel", "settle": 14},
    mark("godot-shaders_E1-3e_shader-in-slot-editor-closed"),
    wait(2),
]
save("pilot-E1", S, "Sprite2D: Material empty -> ShaderMaterial -> Shader slot -> New Shader... dialog -> shader editor. Real handlers, scripted.")

# ----------------------------------------------------------------------------------------------------------------- pilot E2
S = head("res://scenes/e2_dial.tscn")
S += [
    {"op": "unfold_resource", "property": "material", "object": "node", "settle": 24},
    mark("godot-shaders_E2-0_inside-shadermaterial-group-collapsed"),
    {"op": "unfold_group", "property": "shader_parameter/red", "object": "material", "settle": 12},
    mark("godot-shaders_E2-1_red-0.5-default"),
    {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/red", "value": 0.2, "settle": 20},
    mark("godot-shaders_E2-2_red-0.2"),
    {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/red", "value": 0.5, "settle": 20},
    mark("godot-shaders_E2-3_red-0.5-after-0.2"),
    {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/red", "value": 0.9, "settle": 20},
    mark("godot-shaders_E2-4_red-0.9"),
    {"op": "dump_inspector", "name": "red-0.9"},
    wait(2),
]
save("pilot-E2", S, "ColorRect + ShaderMaterial(06-dial): red at 0.5 (default), 0.2, 0.5, 0.9 in the Shader Parameters group.")

# ----------------------------------------------------------------------------------------------------------------- pilot E3
S = head("res://scenes/e3_tint.tscn")
S += [
    {"op": "unfold_resource", "property": "material", "object": "node", "settle": 24},
    {"op": "unfold_group", "property": "shader_parameter/red", "object": "material", "settle": 12},
    {"op": "dump_inspector", "name": "red-and-tint"},
    mark("godot-shaders_E3-1_source-color-swatch-next-to-red-slider"),
    {"op": "click_control", "find": {"class": "ColorPickerButton"}, "within": "inspector", "settle": 14},
    mark("godot-shaders_E3-2_color-picker-popup-open"),
    wait(2),
]
save("pilot-E3", S, "ColorRect + ShaderMaterial(red hint_range float + tint source_color vec4): the swatch, and its picker popup opened by a scripted click.")

# ----------------------------------------------------------------------------------------------------------------- drawing-shapes E1 / E2
for tag, widen in (("default-width", None), ("wide-inspector", 760)):
    S = head("res://scenes/ds_crosshair.tscn", widen=widen)
    S += [
        {"op": "unfold_resource", "property": "material", "object": "node", "settle": 24},
        {"op": "unfold_group", "property": "shader_parameter/dot_size", "object": "material", "settle": 24},
        {"op": "dump_inspector", "name": "six-uniforms"},
        mark("drawing-shapes_E1-1_defaults-%s" % tag),
        {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/dot_size", "value": 1.0, "settle": 30},
        mark("drawing-shapes_E1-2_dot_size-1.0-%s" % tag),
        {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/dot_size", "value": 0.5},
        {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/ring_distance", "value": 0.2, "settle": 30},
        mark("drawing-shapes_E1-3_ring_distance-0.2-%s" % tag),
        {"op": "set_property", "node": ".", "target": "material", "property": "shader_parameter/dot_size", "value": 1.0, "settle": 30},
        mark("drawing-shapes_E1-3b_dot_size-1.0-and-ring_distance-0.2-%s" % tag),
        wait(2),
    ]
    if tag == "wide-inspector":
        S[-1:] = [
            {"op": "edit_resource_file", "path": "res://shaders/16-uv-inside-function-FAILS.gdshader", "settle": 40},
            mark("drawing-shapes_E2_shader-editor-error-16-uv-inside-function"),
            {"op": "dump_tree", "name": "shader-editor-with-error", "root": "main_screen", "max_depth": 2},
            {"op": "dump_tree", "name": "bottom-panel-with-error", "root": {"class": "TextShaderEditor"}, "max_depth": 8, "only_visible": True},
            wait(2),
        ]
    save("drawing-shapes-E1-" + tag, S, "ColorRect + ShaderMaterial(17-crosshair), %s." % tag)

# ----------------------------------------------------------------------------------------------------------------- local-world E1 / E2
for tag, scene, child, parent in (("clean-root", "res://scenes/lw_scene_parent_child.tscn", "Parent/Child", "Parent"),
                                  ("plan-exact-root-is-Parent", "res://scenes/lw_parent_child.tscn", "Child", ".")):
    S = [{"op": "open_scene", "path": scene, "settle": 12}, {"op": "set_main_screen", "name": "2D", "settle": 12}]
    nodes = [".", child] if parent == "." else [parent, child]
    S += [
        {"op": "select_nodes", "nodes": nodes, "settle": 12},
        {"op": "menu_item", "button": "View", "item": "Frame Selection", "settle": 12},
        {"op": "select_node", "node": child, "settle": 14},
        {"op": "unfold_group", "property": "position", "object": "node", "node": child, "settle": 12},
        {"op": "scroll_inspector", "to": "top", "settle": 8},
        {"op": "dump_inspector", "name": "child-selected"},
        mark("local-world_E1-1_child-selected-%s" % tag),
        {"op": "select_node", "node": parent, "settle": 14},
        {"op": "unfold_group", "property": "position", "object": "node", "node": parent, "settle": 12},
        {"op": "scroll_inspector", "to": "top", "settle": 8},
        {"op": "dump_inspector", "name": "parent-selected"},
        mark("local-world_E1-2_parent-selected-%s" % tag),
    ]
    if tag == "clean-root":
        S += [
            {"op": "edit_resource_file", "path": "res://shaders/04-broken-matrix-in-fragment.gdshader", "settle": 40},
            mark("local-world_E2_shader-editor-error-04-broken-matrix-in-fragment"),
        ]
    S += [wait(2)]
    save("local-world-E1-" + tag, S, "Parent/Child positions in the Inspector, %s." % tag)

# ----------------------------------------------------------------------------------------------------------------- Textures and Color E1 / E2 / E3
S = head("res://scenes/tc_dissolve.tscn", widen=760)
S += [
    {"op": "unfold_resource", "property": "material", "object": "node", "settle": 24},
    {"op": "unfold_group", "property": "shader_parameter/noise_tex", "object": "material", "settle": 14},
    mark("textures-and-color_E1-1a_noise_tex-slot-empty"),
    {"op": "open_picker_menu", "property": "shader_parameter/noise_tex", "object": "material", "settle": 8},
    {"op": "dump_popup", "name": "noise_tex-dropdown-items"},
    mark("textures-and-color_E1-1b_noise_tex-dropdown-open"),
    {"op": "pick_menu_item", "text": "NoiseTexture2D", "settle": 30},
    mark("textures-and-color_E1-2a_noise_tex-holds-NoiseTexture2D"),
    {"op": "unfold_resource", "property": "shader_parameter/noise_tex", "object": "material", "settle": 24},
    mark("textures-and-color_E1-2b_inside-NoiseTexture2D-noise-empty"),
    {"op": "open_picker_menu", "property": "noise", "object": {"target": "chain", "chain": ["material", "shader_parameter/noise_tex"]}, "settle": 8},
    {"op": "dump_popup", "name": "noise-dropdown-items"},
    mark("textures-and-color_E1-2c_noise-dropdown-open"),
    {"op": "pick_menu_item", "text": "FastNoiseLite", "settle": 40},
    {"op": "dump_inspector", "name": "noisetexture2d-with-fastnoiselite"},
    mark("textures-and-color_E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite"),
    {"op": "unfold_resource", "property": "noise", "object": {"target": "chain", "chain": ["material", "shader_parameter/noise_tex"]}, "settle": 100},
    {"op": "dump_inspector", "name": "inside-fastnoiselite"},
    mark("textures-and-color_E1-3b_inside-FastNoiseLite-preview-clouds"),
    wait(2),
]
save("tc-E1", S, "Sprite2D + ShaderMaterial(18-dissolve): the noise_tex slot, its dropdown, NoiseTexture2D, its Noise dropdown, FastNoiseLite.")

S = head("res://scenes/tc_picker.tscn", widen=760)
S += [
    {"op": "unfold_resource", "property": "material", "object": "node", "settle": 24},
    {"op": "unfold_group", "property": "shader_parameter/picked", "object": "material", "settle": 14},
    {"op": "dump_inspector", "name": "picked-and-typed"},
    mark("textures-and-color_E2_picked-swatch-and-typed-four-boxes"),
    wait(2),
]
save("tc-E2", S, "ColorRect + ShaderMaterial(22-picker): Picked (source_color vec4) and Typed (plain vec4) in the Inspector.")

S = head("res://scenes/tc_dissolve.tscn", frame=True)
S += [
    {"op": "dump_tree", "name": "title-bar", "root": {"class": "EditorTitleBar"}, "max_depth": 4, "only_visible": False},
    mark("textures-and-color_E3-1_renderer-name-upper-right"),
    {"op": "open_option_button", "contains": "Forward", "focus": "Mobile", "settle": 8},
    mark("textures-and-color_E3-2_renderer-menu-open"),
    wait(2),
]
save("tc-E3", S, "The renderer selector (needs Editor Settings > Interface > Editor > Appearance > Show Renderer Selector): name button, then its menu.")
print("wrote", sorted(os.listdir(OUT)))
