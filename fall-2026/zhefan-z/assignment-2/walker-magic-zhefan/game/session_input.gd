extends Node
## Keeps processing while the tree is paused (process_mode ALWAYS), so Esc can resume and R can
## restart. It only forwards actions to Main; Main and the level stay pausable.


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		get_parent().toggle_pause()
	elif event.is_action_pressed("restart"):
		get_parent().restart_if_cleared()
