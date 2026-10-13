extends Node

var selected := false

func _ready():
	$Sprite.material.set_shader_parameter("thickness", 0.0)

func _unhandled_key_input(event):
	if event.pressed:
		selected = not selected
		$Sprite.material.set_shader_parameter("thickness", 2.0 if selected else 0.0)
