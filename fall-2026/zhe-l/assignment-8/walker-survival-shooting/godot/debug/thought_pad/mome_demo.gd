extends Control

const DEMO_DEVICE_UID := 1
const TEXT_TRANSLATIONS: Array[Translation] = [
	preload("res://computer_system/apps/thought_pad/mome_text.en.translation"),
]

@export var demo_file_uid: int = 1

@onready var _window: MomeWindow = $MomeWindow
@onready var _debug_source: Node = $DebugMomeSource

func _enter_tree() -> void:
	for translation in TEXT_TRANSLATIONS:
		TranslationServer.add_translation(translation)


func _ready() -> void:
	_window.close_requested.connect(_on_window_close_requested)
	_window.open(DEMO_DEVICE_UID, _debug_source, demo_file_uid)

func _on_window_close_requested() -> void:
	get_tree().quit()
