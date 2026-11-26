extends Control

const TEST_ITEMS: Array[Dictionary] = [
	{"id": 0, "text": "Cut (greyed-out test)", "disabled": true},
	{"id": 1, "text": "Copy"},
	{"id": 2, "text": "Paste"},
]

@onready var _menu: ContextMenu = $ContextMenu
@onready var _result_label: Label = $ResultLabel

func _ready() -> void:
	_menu.id_pressed.connect(_on_menu_id_pressed)


func _gui_input(event: InputEvent) -> void:
	var mouse := event as InputEventMouseButton
	if mouse != null and mouse.pressed and mouse.button_index == MOUSE_BUTTON_RIGHT:
		_menu.open_at(TEST_ITEMS, mouse.global_position)

func _on_menu_id_pressed(item_id: int) -> void:
	_result_label.text = "You clicked item %d: %s" % [item_id, TEST_ITEMS[item_id]["text"]]
