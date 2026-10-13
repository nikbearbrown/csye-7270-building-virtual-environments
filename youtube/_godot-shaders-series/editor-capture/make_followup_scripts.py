#!/usr/bin/env python3
"""make_followup_scripts.py <out_dir>
Writes the state scripts of the renderer-path follow-up (section 11 of the README):
  rp-editor.json  the editor session: Project Settings, Editor Settings, title bar OFF/ON, renderer selector menu and its restart prompt
  rp-pm.json      the Project Manager session: Create New Project dialog with the renderer radio buttons
  rp-fresh.json   a brand-new editor HOME: default value of the selector setting, title bar of a factory-default editor
"""
import json, os, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)

PS = {"class": "ProjectSettingsEditor"}
ES = {"class": "EditorSettingsDialog"}

editor = {
    "note": "Renderer path: Project Settings > Rendering > Renderer > Rendering Method; Editor Settings > Interface > Editor > Appearance > Show Renderer Selector; title-bar OFF vs ON; selector menu and restart prompt.",
    "boot_frames": 25, "window": [3456, 1944], "window_settle": 40,
    "steps": [
        {"op": "open_scene", "path": "res://scenes/e1_sprite.tscn", "settle": 12},
        {"op": "select_node", "node": ".", "settle": 12},
        {"op": "editor_setting_info", "names": ["interface/editor/appearance/show_renderer_selector", "interface/editor/appearance/use_embedded_menu", "interface/editor/display/single_window_mode", "project_manager/default_renderer"], "name": "settings-at-start"},
        {"op": "mark", "name": "R3-A_title-bar_selector-OFF-default"},
        # ---- Project > Project Settings... > General > Rendering > Renderer
        {"op": "menubar_open", "menu": "Project", "settle": 10},
        {"op": "mark", "name": "R1-A_Project-menu-open"},
        {"op": "menubar_pick", "menu": "Project", "contains": "Project Settings", "settle": 40},
        {"op": "dump_windows", "name": "windows-project-settings"},
        {"op": "mark", "name": "R1-B_Project-Settings-dialog-opens"},
        {"op": "select_tree_item", "within": PS, "path": ["Rendering", "Renderer"], "settle": 25},
        {"op": "dump_texts", "within": PS, "name": "project-settings-renderer-page"},
        {"op": "dump_rows", "within": PS, "name": "project-settings-renderer-rows"},
        {"op": "mark", "name": "R1-C_Project-Settings_Rendering-Renderer_menu-closed"},
        {"op": "open_option_button", "within": PS, "index": 0, "settle": 12},
        {"op": "mark", "name": "R1-D_Project-Settings_Rendering-Method_menu-open"},
        {"op": "close_popups", "settle": 6},
        {"op": "select_option", "within": PS, "index": 0, "text": "gl_compatibility", "settle": 20},
        {"op": "dump_texts", "within": PS, "name": "project-settings-after-change"},
        {"op": "mark", "name": "R1-E_Project-Settings_restart-note"},
        {"op": "select_option", "within": PS, "index": 0, "text": "forward_plus", "settle": 20},
        {"op": "close_dialog", "within": PS, "settle": 20},
        # ---- Editor > Editor Settings...
        {"op": "menubar_open", "menu": "Editor", "settle": 10},
        {"op": "mark", "name": "R2-A_Editor-menu-open"},
        {"op": "menubar_pick", "menu": "Editor", "contains": "Editor Settings", "settle": 40},
        {"op": "dump_texts", "within": ES, "name": "editor-settings-default-view"},
        {"op": "mark", "name": "R2-B_Editor-Settings-dialog-opens"},
        {"op": "set_toggle", "within": ES, "text": "Advanced Settings", "value": True, "settle": 25},
        {"op": "dump_rows", "within": ES, "name": "editor-settings-advanced-on-rows"},
        {"op": "mark", "name": "R2-C_Editor-Settings_Advanced-on_Interface-Editor-Appearance"},
        {"op": "set_toggle", "within": ES, "text": "Advanced Settings", "value": False, "settle": 25},
        {"op": "set_text", "within": ES, "index": 0, "text": "renderer", "settle": 25},
        {"op": "dump_texts", "within": ES, "name": "editor-settings-search-renderer"},
        {"op": "dump_rows", "within": ES, "name": "editor-settings-search-renderer-rows"},
        {"op": "mark", "name": "R2-D_Editor-Settings_search-renderer_Show-Renderer-Selector"},
        {"op": "select_tree_item", "within": ES, "path": ["Project Manager"], "settle": 25},
        {"op": "dump_texts", "within": ES, "name": "editor-settings-search-renderer-project-manager"},
        {"op": "dump_rows", "within": ES, "name": "editor-settings-search-renderer-project-manager-rows"},
        {"op": "mark", "name": "R2-E_Editor-Settings_search-renderer_Project-Manager-Default-Renderer"},
        {"op": "select_tree_item", "within": ES, "path": ["Interface", "Editor"], "settle": 25},
        {"op": "toggle_check", "within": ES, "property": "appearance/show_renderer_selector", "value": True, "settle": 20},
        {"op": "editor_setting_info", "names": ["interface/editor/appearance/show_renderer_selector"], "name": "setting-after-tick"},
        {"op": "mark", "name": "R2-F_Editor-Settings_Show-Renderer-Selector_ticked"},
        {"op": "close_dialog", "within": ES, "settle": 30},
        {"op": "mark", "name": "R3-B_title-bar_selector-ON"},
        # ---- the selector itself
        {"op": "open_option_button", "contains": "Forward", "focus": "Mobile", "settle": 8},
        {"op": "mark", "name": "R3-C_title-bar_selector-menu-open"},
        {"op": "close_popups", "settle": 8},
        {"op": "select_option", "within": {"class": "EditorTitleBar"}, "index": 0, "text": "Compatibility", "settle": 30},
        {"op": "dump_windows", "name": "windows-restart-prompt"},
        {"op": "mark", "name": "R3-D_title-bar_selector-restart-prompt"},
        {"op": "press_cancel", "within": {"class": "ConfirmationDialog"}, "settle": 25},
        {"op": "dump_windows", "name": "windows-after-cancel"},
        {"op": "mark", "name": "R3-E_after-Cancel"},
        {"op": "wait_frames", "n": 2},
    ],
}

pm = {
    "note": "Project Manager (real, hosted by --project-manager --script): Create New Project dialog, renderer radio buttons. Nothing is created.",
    "boot_frames": 25, "window": [3456, 1944], "window_settle": 40,
    "steps": [
        {"op": "wait_frames", "n": 10},
        {"op": "mark", "name": "R4-A_Project-Manager-empty"},
        {"op": "press", "text": "Create", "index": 0, "settle": 30},
        {"op": "dump_windows", "name": "windows-after-create"},
        {"op": "dump_texts", "within": {"class": "ProjectDialog"}, "name": "create-dialog-forward-plus"},
        {"op": "mark", "name": "R4-B_Create-New-Project_Forward-selected"},
        {"op": "click", "text": "Mobile", "within_class": "ProjectDialog", "settle": 12},
        {"op": "dump_texts", "within": {"class": "ProjectDialog"}, "name": "create-dialog-mobile"},
        {"op": "mark", "name": "R4-C_Create-New-Project_Mobile-selected"},
        {"op": "click", "text": "Compatibility", "within_class": "ProjectDialog", "settle": 12},
        {"op": "dump_texts", "within": {"class": "ProjectDialog"}, "name": "create-dialog-compatibility"},
        {"op": "mark", "name": "R4-D_Create-New-Project_Compatibility-selected"},
        {"op": "press_cancel", "within": {"class": "ProjectDialog"}, "settle": 20},
        {"op": "dump_windows", "name": "windows-after-cancel"},
        {"op": "mark", "name": "R4-E_after-Cancel-nothing-created"},
        {"op": "wait_frames", "n": 2},
    ],
}

fresh = {
    "note": "A brand-new HOME (no settings file): the editor writes its own factory settings. Title bar of a factory-default editor and the default of the selector setting.",
    "boot_frames": 25, "window": [3456, 1944], "window_settle": 40,
    "steps": [
        {"op": "open_scene", "path": "res://scenes/e1_sprite.tscn", "settle": 12},
        {"op": "select_node", "node": ".", "settle": 12},
        {"op": "editor_setting_info", "names": ["interface/editor/appearance/show_renderer_selector", "interface/editor/appearance/use_embedded_menu", "interface/editor/display/single_window_mode", "project_manager/default_renderer"], "name": "settings-fresh-home"},
        {"op": "probe_window", "name": "window-fresh-home"},
        {"op": "mark", "name": "R5-A_fresh-home_title-bar-factory-default"},
        {"op": "wait_frames", "n": 2},
    ],
}

for name, obj in (("rp-editor", editor), ("rp-pm", pm), ("rp-fresh", fresh)):
    path = os.path.join(out, name + ".json")
    json.dump(obj, open(path, "w"), indent=1)
    print("wrote", path, len(obj["steps"]), "steps")
