@tool
extends EditorPlugin
var last_request := ""
var elapsed := 0.0
var busy := false
var scripted_view := false
var view_angle := 0.7854
var view_orbit := false
var badge: Label
func _enter_tree() -> void:
	EditorInterface.get_base_control().get_window().position = Vector2i(0,66)
	badge = Label.new()
	badge.text = "SCRIPTED ACTIONS · Real Godot"
	add_control_to_container(CONTAINER_TOOLBAR, badge)
	EditorInterface.get_editor_settings().set_setting("text_editor/appearance/font_size", 34)
	set_process(true)
func _exit_tree() -> void:
	remove_control_from_container(CONTAINER_TOOLBAR, badge)
	badge.queue_free()
func _process(delta: float) -> void:
	if scripted_view:
		if view_orbit:view_angle+=delta*.35
		var camera=EditorInterface.get_editor_viewport_3d(0).get_camera_3d()
		if camera:
			camera.global_position=Vector3(cos(view_angle)*9,5,sin(view_angle)*9)
			camera.look_at(Vector3(0,1.8,0))
	if busy:return
	elapsed += delta
	if elapsed < 0.15: return
	elapsed = 0.0
	var path := "res://.lecture/request.json"
	if not FileAccess.file_exists(path): return
	var text := FileAccess.get_file_as_string(path)
	if text == last_request: return
	if EditorInterface.get_edited_scene_root() == null: return
	last_request = text
	var req = JSON.parse_string(text)
	if not req is Dictionary:return
	var action = load("res://addons/lecture_capture/actions.gd").new()
	busy=true
	var result = await action.run(self, req)
	busy=false
	var record = {"request":req, "result":result, "ticks_msec":Time.get_ticks_msec()}
	var f := FileAccess.open("res://.lecture/actions.jsonl", FileAccess.READ_WRITE)
	if f == null: f = FileAccess.open("res://.lecture/actions.jsonl",FileAccess.WRITE)
	f.seek_end();f.store_line(JSON.stringify(record));f.close()
	print("LECTURE_ACTION ", JSON.stringify(record))
