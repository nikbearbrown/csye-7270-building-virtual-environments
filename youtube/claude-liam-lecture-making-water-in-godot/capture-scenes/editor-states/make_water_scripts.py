#!/usr/bin/env python3
"""make_water_scripts.py: writes the state scripts for the 'Making Water in Godot' editor frames (scripted editor session).

Scene: res://scenes/water.tscn (root Cove). Node: Water (MeshInstance3D, PlaneMesh 127 x 127 cuts, Material Override = ShaderMaterial of
res://shaders/06-shore-foam.gdshader). One script per run; the driver is the series' addons/driver plugin (unchanged).
Usage: python3 make_water_scripts.py <out_dir>
"""
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "state-scripts/water"
W = "Water"
MAT = {"target": "chain", "chain": ["material_override"], "node": W}          # the ShaderMaterial in the Material Override slot
NA = {"target": "chain", "chain": ["material_override", "shader_parameter/normal_a"], "node": W}   # normal_a's NoiseTexture2D
DOCK = [560, -1300]   # DockHSplitMain split offsets: a wider Inspector dock so the Shader slot's file name and the labels fit

# Inspector scroll margins (native window px, i.e. the 3456x1944 window): a row's header sits ~45 px above its first row.
HDR = 49  # puts a group header about 4 px under the top of the Inspector viewport when the scroll aligns on the group's first row


def S(op, **kw):
    d = {"op": op}
    d.update(kw)
    return d


def scroll_to(prop, obj, margin=8, settle=6):
    return S("scroll_inspector", property=prop, object=obj, align="top", margin=margin, settle=settle)


def mark(name):
    return S("mark", name=name)


def common_open():
    return [
        S("open_scene", path="res://scenes/water.tscn", settle=12),
        S("select_node", node=W, settle=12),
        S("dock_split", name="DockHSplitMain", offsets=DOCK, settle=20),
    ]


def unfold_all_folders():
    groups = ["shader_parameter/water_color", "shader_parameter/opacity", "shader_parameter/foam_color",
              "shader_parameter/normal_a", "shader_parameter/wave_height", "shader_parameter/shore_width"]
    return [S("unfold_group", property=g, object=MAT, settle=6) for g in groups]


def water_all():
    st = common_open()
    st += [
        S("dump_scene_tree", name="scene-tree"),
        S("dump_inspector", name="water-node-initial"),
        # ---- W1: the Water node: Mesh slot, Geometry group, Material Override slot
        S("unfold_group", property="material_override", object="node", node=W, settle=14),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W1-water-node"),
        mark("W1_Water-selected_Mesh-slot_Geometry-Material-Override"),
        mark("W1b_Scene-dock-tree_Water-selected"),
        # ---- W2: inspect the ShaderMaterial
        S("unfold_resource", property="material_override", object="node", node=W, settle=24),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W2-shadermaterial-folders-as-opened"),
        mark("W2-0_ShaderMaterial_folders-as-the-editor-opens-them"),
    ]
    st += unfold_all_folders()
    st += [
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W2-shadermaterial-six-folders-unfolded-top"),
        mark("W2a_ShaderMaterial_top_Shader-slot_and_folders"),
        scroll_to("shader_parameter/water_color", MAT, margin=HDR),
        S("dump_inspector", name="W2-six-folders-one-frame"),
        mark("W2-all_six-folder-headers-and-all-widgets-in-one-frame"),
        scroll_to("shader_parameter/normal_a", MAT, margin=HDR + 4),
        mark("W2b_ShaderMaterial_bottom_Ripples_Waves_Shore"),
        # ---- W3: Opacity to 0.5 with set_property (and the Water Color swatch row)
        S("scroll_inspector", to="top", settle=6),
        S("set_property", node=W, target="chain", chain=["material_override"], property="shader_parameter/opacity", value=0.5, settle=20),
        S("dump_inspector", name="W3-opacity-0.5"),
        mark("W3a_Opacity-0.5_row-with-revert-arrow"),
        scroll_to("shader_parameter/water_color", MAT, margin=HDR),
        mark("W3b_Water-Color-swatch-row_Opacity-0.5"),
        # ---- W4: the PlaneMesh
        S("inspect_object", node=W, target="node", settle=20),
        S("unfold_resource", property="mesh", object="node", node=W, settle=24),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W4-planemesh"),
        mark("W4_PlaneMesh_Size-Subdivide-Width-Depth-Orientation"),
        # ---- W5: normal_a's NoiseTexture2D, then its FastNoiseLite
        S("inspect_object", node=W, target="node", settle=20),
        S("unfold_resource", property="material_override", object="node", node=W, settle=24),
        S("unfold_resource", property="shader_parameter/normal_a", object=MAT, settle=24),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W5a-noisetexture2d-normal_a"),
        mark("W5a_normal_a_NoiseTexture2D_As-Normal-Map_Seamless_Bump-Strength"),
        S("unfold_resource", property="noise", object=NA, settle=100),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W5b-fastnoiselite-as-opened"),
        mark("W5b-0_normal_a_FastNoiseLite_as-the-editor-opens-it"),
        S("unfold_group", property="fractal_octaves", object={"target": "chain", "chain": ["material_override", "shader_parameter/normal_a", "noise"], "node": W}, settle=12),
        S("dump_inspector", name="W5b-fastnoiselite-fractal-unfolded"),
        mark("W5b_normal_a_FastNoiseLite_Noise-Type_Frequency_Fractal"),
        S("wait_frames", n=2),
    ]
    return st


def colour_picker():
    st = common_open()
    st += [
        S("unfold_resource", property="material_override", object="node", node=W, settle=24),
        S("unfold_group", property="shader_parameter/water_color", object=MAT, settle=10),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W3c-before-click"),
        mark("W3c-0_Water-Color-swatch_before-click"),
        S("click_control", find={"class": "ColorPickerButton"}, within="inspector", settle=14),
        mark("W3c_Water-Color-swatch-clicked_colour-picker-open"),
        S("wait_frames", n=2),
    ]
    return st


def unfold_sequence():
    # the folders unfolded one after another, a mark after each (what a student sees when clicking the headers in order)
    st = common_open()
    st += [
        S("unfold_resource", property="material_override", object="node", node=W, settle=24),
        S("scroll_inspector", to="top", settle=6),
        mark("W2s-0_as-opened_only-Ripples-open"),
        S("unfold_group", property="shader_parameter/water_color", object=MAT, settle=14),
        mark("W2s-1_Color-unfolded"),
        S("unfold_group", property="shader_parameter/opacity", object=MAT, settle=14),
        mark("W2s-2_Clarity-unfolded"),
        S("unfold_group", property="shader_parameter/foam_color", object=MAT, settle=14),
        mark("W2s-3_Foam-unfolded"),
        scroll_to("shader_parameter/normal_a", MAT, margin=HDR + 4),
        S("unfold_group", property="shader_parameter/wave_height", object=MAT, settle=14),
        mark("W2s-4_Waves-unfolded"),
        S("unfold_group", property="shader_parameter/shore_width", object=MAT, settle=14),
        mark("W2s-5_Shore-unfolded_all-six-open"),
        S("wait_frames", n=2),
    ]
    return st


def ungrouped_compare():
    # scratch-only comparison (not the film's shader): the same kind of material with NO group_uniforms: does a 'Shader Parameters' header appear?
    return [
        S("open_scene", path="res://scenes/zz_ungrouped_compare.tscn", settle=12),
        S("select_node", node=W, settle=12),
        S("dock_split", name="DockHSplitMain", offsets=DOCK, settle=20),
        S("unfold_resource", property="material_override", object="node", node=W, settle=24),
        S("scroll_inspector", to="top", settle=6),
        S("dump_inspector", name="W6-ungrouped-shadermaterial"),
        mark("W6a_comparison_NO-group_uniforms_Shader-Parameters-header-folded"),
        S("unfold_group", property="shader_parameter/opacity", object=MAT, settle=10),
        S("dump_inspector", name="W6-ungrouped-shadermaterial-unfolded"),
        mark("W6b_comparison_NO-group_uniforms_Shader-Parameters-unfolded"),
        S("wait_frames", n=2),
    ]


SCRIPTS = {"water-W": ("Water node, ShaderMaterial folders, Opacity 0.5, PlaneMesh, normal_a noise texture", water_all),
           "water-W3c-colour-picker": ("Water Color swatch clicked (scripted click): the colour picker", colour_picker),
           "water-W2-unfold-sequence": ("the six folders unfolded one after another, a mark after each", unfold_sequence),
           "water-W6-ungrouped-compare": ("comparison scene: a shader without group_uniforms (scratch file, not the film's shader)", ungrouped_compare)}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, (note, fn) in SCRIPTS.items():
        json.dump({"note": "scripted editor session: " + note, "boot_frames": 25, "window": [3456, 1944], "window_settle": 40, "steps": fn()},
                  open(os.path.join(OUT, name + ".json"), "w"), indent=1)
        print("wrote", os.path.join(OUT, name + ".json"))
