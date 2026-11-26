class_name DesktopIcon
extends VBoxContainer

signal activated

@export var icon_texture: Texture2D
@export var name_key: String

@onready var _icon: TextureRect = $Icon
@onready var _name_label: Label = $NameLabel

func _ready() -> void:
	_icon.texture = icon_texture
	_name_label.text = name_key


func _gui_input(event: InputEvent) -> void:
	var mouse_button := event as InputEventMouseButton
	if mouse_button == null:
		return
	if mouse_button.button_index == MOUSE_BUTTON_LEFT and mouse_button.pressed and mouse_button.double_click:
		accept_event()
		activated.emit()
