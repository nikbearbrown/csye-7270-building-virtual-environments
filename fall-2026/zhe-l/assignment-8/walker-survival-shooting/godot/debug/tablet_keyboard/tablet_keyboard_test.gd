extends Node

const TEST_DEVICE_UID := 1
const TEST_FILE_UID := 2
const MOME_WINDOW_SCENE := preload("res://computer_system/apps/thought_pad/mome_window.tscn")
const DEBUG_SOURCE_SCRIPT := preload("res://debug/thought_pad/debug_mome_source.gd")
const MOME_TRANSLATIONS: Array[Translation] = [
	preload("res://computer_system/apps/thought_pad/mome_text.en.translation"),
]

@onready var _window_layer: Control = $Base/Player/PlayerController/TabletOSViewport/TabletOS/WindowLayer

func _enter_tree() -> void:
	for translation in MOME_TRANSLATIONS:
		TranslationServer.add_translation(translation)


func _ready() -> void:
	var debug_source := Node.new()
	debug_source.set_script(DEBUG_SOURCE_SCRIPT)
	add_child(debug_source)
	var window: MomeWindow = MOME_WINDOW_SCENE.instantiate()
	_window_layer.add_child(window)
	window.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	window.open(TEST_DEVICE_UID, debug_source, TEST_FILE_UID)
