@tool
extends EditorPlugin
# Planning-check driver for "Drawing Shapes with Math" (not part of the film). Two seconds after the editor has loaded the scene, it switches the
# main screen to 2D and shows the ColorRect's ShaderMaterial in the Inspector, so the "Shader Parameters" group (the six uniforms) is on screen.
# Proven 2026-10-13, Godot 4.7.2, Apple M4 Pro. See README.md next to this file.

func _enter_tree() -> void:
	call_deferred("_drive")

func _drive() -> void:
	await get_tree().create_timer(2.0).timeout
	EditorInterface.set_main_screen_editor("2D")
	var rect := EditorInterface.get_edited_scene_root() as ColorRect
	EditorInterface.edit_resource(rect.material)
