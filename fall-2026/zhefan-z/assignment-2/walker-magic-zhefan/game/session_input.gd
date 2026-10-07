extends Node
## Keeps processing while the tree is paused (process_mode ALWAYS), so Esc can resume, R can
## restart and M / N can mute at any time. It only forwards actions to Main; the level stays pausable.


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		get_parent().toggle_pause()
	elif event.is_action_pressed("restart"):
		get_parent().restart_if_cleared()
	elif event.is_action_pressed("mute_music"):
		get_parent().toggle_mute("Music")
	elif event.is_action_pressed("mute_sfx"):
		get_parent().toggle_mute("SFX")
