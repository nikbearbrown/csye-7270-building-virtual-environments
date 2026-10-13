@tool
extends EditorPlugin
# Scratch only (SubViewports film planning): drives the Inspector while Movie Maker records, and prints the REAL label of every
# property the Inspector shows (EditorProperty.label), so label wording is read from the editor, not remembered.
# SHOT_MODE (environment variable) picks the pass: default (main.tscn), shaders (shaders.tscn), mesh (mesh.tscn). The driver opens the scene it needs, prints, and quits the editor.

func _enter_tree() -> void:
	call_deferred("_run")

func _select(node: Node) -> void:
	EditorInterface.get_selection().clear()
	EditorInterface.get_selection().add_node(node)
	EditorInterface.edit_node(node)

func _widen() -> void:
	var n: Node = EditorInterface.get_inspector()
	while n:
		if String(n.name) == "DockHSplitMain":
			(n as SplitContainer).split_offset = -360
			print("SHOT widened DockHSplitMain")
			return
		n = n.get_parent()

func _find_filter(node: Node) -> LineEdit:
	for c in node.get_children():
		if c is LineEdit and (c as LineEdit).placeholder_text == "Filter Properties":
			return c
		var r := _find_filter(c)
		if r: return r
	return null

func _filter(text: String) -> void:
	var le := _find_filter(EditorInterface.get_base_control())
	if le:
		le.text = text
		le.text_changed.emit(text)

func _dump(tag: String) -> void:
	var rows: Array = []
	for p in EditorInterface.get_inspector().find_children("*", "EditorProperty", true, false):
		var ep := p as EditorProperty
		rows.append("%s=%s" % [ep.get_edited_property(), ep.label])
	print("SHOT labels[%s]: %s" % [tag, ", ".join(rows)])

func _wait(s: float) -> void:
	await get_tree().create_timer(s).timeout

func _shot(name: String) -> void:
	# say which Movie Maker frame shows this state; run-editor-labels.sh copies that frame (1920 x 1080) to editor-frames/<name>.png
	# (the editor window itself is bigger than the movie, so a screenshot of the window would not be 16:9)
	await get_tree().process_frame
	RenderingServer.force_draw(false)
	print("SHOT state %s frame=%d" % [name, Engine.get_process_frames()])

func _open_and_wait(path: String) -> void:
	# open the scene this mode needs and wait until it really is the edited one (a scene named on the command line can open later than the 2 s the first runs waited)
	var root := EditorInterface.get_edited_scene_root()
	if root == null or root.scene_file_path != path:
		EditorInterface.open_scene_from_path(path)
	var tries := 0
	while tries < 100:
		root = EditorInterface.get_edited_scene_root()
		if root != null and root.scene_file_path == path:
			break
		await _wait(0.2)
		tries += 1
	root = EditorInterface.get_edited_scene_root()
	print("SHOT edited scene: %s (after %d waits)" % [root.scene_file_path if root else "none", tries])
	await _wait(0.5)

func _finish() -> void:
	print("SHOT done")
	await _wait(0.5)
	get_tree().quit()

func _run() -> void:
	var mode := OS.get_environment("SHOT_MODE")
	await _wait(2.0)
	EditorInterface.set_main_screen_editor("2D")
	var scenes := {"shaders": "res://shaders.tscn", "mesh": "res://mesh.tscn"}
	await _open_and_wait(scenes.get(mode, "res://main.tscn"))
	if mode == "shaders":
		var r := EditorInterface.get_edited_scene_root()
		var inner := r.get_node("SubViewport/Sprite2D") as Sprite2D
		var disp := r.get_node("Display") as Sprite2D
		var dp := r.get_node("DisplayPremul") as Sprite2D
		_select(inner)
		_filter("material")
		await _wait(1.5)
		_dump("inner Sprite2D, filter material")
		await _shot("e4-inner-sprite-material")
		_select(disp)
		await _wait(1.5)
		_dump("Display, filter material")
		await _shot("e4b-display-material")
		EditorInterface.edit_resource(disp.material)
		_filter("")
		await _wait(1.5)
		_dump("Display's ShaderMaterial")
		await _shot("e4c-display-shadermaterial")
		_filter("count")
		await _wait(1.0)
		_dump("Display's ShaderMaterial, filter count")
		await _shot("e4e-shader-parameters-count")
		_filter("")
		await _wait(0.5)
		EditorInterface.edit_resource((disp.material as ShaderMaterial).shader)
		await _wait(2.0)
		_dump("Display's Shader resource")
		await _shot("e4d-shader-editor")
		EditorInterface.edit_resource(dp.material)
		await _wait(1.5)
		_dump("DisplayPremul's CanvasItemMaterial")
		await _shot("e5-canvasitemmaterial-premultiplied")
		# the enum text the Inspector shows for a few properties
		for pair in [["CanvasItemMaterial", "blend_mode"], ["SubViewport", "render_target_update_mode"], ["SubViewport", "render_target_clear_mode"], ["Sprite2D", "texture_filter"]]:
			for pi in ClassDB.class_get_property_list(pair[0]):
				if pi["name"] == pair[1]:
					print("SHOT enum %s.%s hint_string: %s" % [pair[0], pair[1], pi["hint_string"]])
		await _finish()
		return
	if mode == "mesh":
		var mroot := EditorInterface.get_edited_scene_root()
		var mi := mroot.get_node("Wobble") as MeshInstance2D
		_select(mi)
		await _wait(1.5)
		_dump("MeshInstance2D")
		EditorInterface.edit_resource(mi.mesh)
		await _wait(2.0)
		_dump("QuadMesh")
		await _shot("e3-quadmesh-inspector")
		await _finish()
		return
	_widen()
	var root := EditorInterface.get_edited_scene_root()
	var sv := root.get_node("SubViewport")
	var disp := root.get_node("Display")
	_select(sv)
	await _wait(1.0)
	_dump("SubViewport, no filter")
	await _shot("e1-subviewport-inspector")
	for kw in ["size", "update", "clear", "transparent"]:
		_filter(kw)
		await _wait(1.0)
		_dump("SubViewport, filter " + kw)
		await _shot({"size": "e1a-size-filter", "update": "e1b-update-mode", "clear": "e1c-clear-mode", "transparent": "e1d-transparent-bg"}[kw])
	_filter("")
	await _wait(1.0)
	_select(disp)
	await _wait(1.5)
	_dump("Display (Sprite2D)")
	await _shot("e2-display-texture-slot")
	EditorInterface.edit_resource((disp as Sprite2D).texture)
	await _wait(1.5)
	_dump("Display's ViewportTexture")
	await _shot("e2b-viewport-texture-path")
	await _finish()
