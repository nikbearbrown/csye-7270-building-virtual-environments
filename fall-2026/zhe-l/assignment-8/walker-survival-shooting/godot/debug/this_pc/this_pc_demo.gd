extends Control

const DEMO_DEVICE_UID := 1
const TEXT_TRANSLATIONS: Array[Translation] = [
	preload("res://computer_system/apps/this_pc/this_pc_text.en.translation"),
]

@onready var _window: ThisPCWindow = $ThisPCWindow
@onready var _debug_source: Node = $DebugFileSource

func _ready() -> void:
	for translation in TEXT_TRANSLATIONS:
		TranslationServer.add_translation(translation)
	_window.close_requested.connect(_on_window_close_requested)
	_window.open(DEMO_DEVICE_UID, _debug_source)

func _on_window_close_requested() -> void:
	get_tree().quit()
