# ============================================================
# Class declaration: what it inherits from and what the whole script does
# ============================================================
extends Control  # The root of the demo scene is a Control that fills the screen
## Demo scene for This PC: needs neither the tablet OS nor the backend; press F6 to see the This PC window on its own (project rule 7b).
## It registers This PC's translation lookup tables itself, then opens the window with a fake data entry point. Copy the whole this_pc folder into a new project, open this scene, and it plays.

# ============================================================
# Constants: values defined once that never change
# ============================================================
const DEMO_DEVICE_UID := 1  # The ID of the tablet the demo pretends to show; the fake data entry point ignores it, so any value will do
const TEXT_TRANSLATIONS: Array[Translation] = [  # This PC's own translation lookup tables (the file generated when this_pc_text.csv is imported; this course copy has only the English one); the paths are relative to this script, so they are found wherever the whole folder is moved
	preload("../this_pc_text.en.translation"),  # English
]

# ============================================================
# Node references (@onready): child nodes in the scene that we use
# ============================================================
@onready var _window: ThisPCWindow = $ThisPCWindow  # The This PC window being demonstrated
@onready var _fake_source: Node = $FakeFileSource  # The fake data entry point, standing in for the backend

# ============================================================
# Engine callbacks: functions Godot calls automatically at certain moments (they act as the entry points; GDScript has no main)
# ============================================================
## Godot calls this once after the demo scene and its children are all ready: we register the translation lookup tables, then start listening for the window's ×, and finally open the window.
func _ready() -> void:
	for translation in TEXT_TRANSLATIONS:  # First we take out each of This PC's translation lookup tables
		TranslationServer.add_translation(translation)  # and register it with Godot; when run alone they are not registered in the project settings, and only then can the title show as text instead of the key (in the game they are already registered, and registering again does not duplicate them)
	_window.close_requested.connect(_on_window_close_requested)  # Then we put our _on_window_close_requested on the window's "I want to close" list; the demo has only this one window, so we do not need to attach which one
	_window.open(DEMO_DEVICE_UID, _fake_source)  # Finally we open the window with the fake data entry point, and the window lists C, D, E at once

# ============================================================
# Functions: called by others, or called inside this script
# ============================================================
## Called when the player clicks the window's × in the demo (the window emits close_requested): we simply end this demo run.
## The demo has no desktop and no taskbar, so once the window is closed nothing is left; like closing a standalone program, the whole run window closes with it.
func _on_window_close_requested() -> void:
	get_tree().quit()  # We tell Godot to end this run; the effect is the same as pressing Stop in the editor
