@tool
extends EditorPlugin
# Prints, from the real Godot 4.7.2 editor UI, the labels the film names: the Layout presets, the Inspector's section and property names for a
# ColorRect, a CanvasLayer, a BackBufferCopy and a ShaderMaterial with uniforms, and the kind of widget the Inspector builds for each uniform.

func _enter_tree() -> void:
	call_deferred("_start")

func _walk(n: Node, depth: int, out: Array) -> void:
	out.append([depth, n])
	for c in n.get_children():
		_walk(c, depth + 1, out)

func _dump_inspector(tag: String) -> void:
	var insp := EditorInterface.get_inspector()
	var items: Array = []
	_walk(insp, 0, items)
	var lines: Array = []
	for it in items:
		var n: Node = it[1]
		var cls := n.get_class()
		if cls.begins_with("EditorProperty") or cls.begins_with("EditorInspectorSection") or cls.begins_with("EditorInspectorCategory") or cls == "EditorSpinSlider" or cls == "ColorPickerButton":
			var label := ""
			if n.has_method("get_label"):
				label = String(n.call("get_label"))
			elif "label" in n:
				label = String(n.get("label"))
			elif "text" in n:
				label = String(n.get("text"))
			var prop := ""
			if n.has_method("get_edited_property"):
				prop = String(n.call("get_edited_property"))
			lines.append("%s%s | label=%s | prop=%s" % ["  ".repeat(it[0]), cls, label, prop])
	print("INSPECTOR[" + tag + "] " + str(lines.size()) + " lines")
	for l in lines:
		print("  " + l)

func _groups(node: Object, tag: String) -> void:
	var rows: Array = []
	for p in node.get_property_list():
		var u: int = int(p["usage"])
		if u & PROPERTY_USAGE_CATEGORY:
			rows.append("CATEGORY " + String(p["name"]))
		elif u & PROPERTY_USAGE_GROUP:
			rows.append("GROUP " + String(p["name"]) + " (prefix '" + String(p["hint_string"]) + "')")
		elif u & PROPERTY_USAGE_SUBGROUP:
			rows.append("  SUBGROUP " + String(p["name"]))
	print("GROUPS[" + tag + "] " + " ; ".join(rows))

func _dump_widget(tag: String, prop: String) -> void:
	var insp := EditorInterface.get_inspector()
	var items: Array = []
	_walk(insp, 0, items)
	for it in items:
		var n: Node = it[1]
		if n.has_method("get_edited_property") and String(n.call("get_edited_property")) == prop:
			var sub: Array = []
			_walk(n, 0, sub)
			var lines: Array = []
			for s2 in sub:
				var m: Node = s2[1]
				var extra := ""
				if m is OptionButton:
					var ob: OptionButton = m
					var names: Array = []
					for i in ob.item_count:
						names.append(ob.get_item_text(i))
					extra = " items=" + str(names)
				elif m is PopupMenu:
					var pm: PopupMenu = m
					var names2: Array = []
					for i in pm.item_count:
						names2.append(pm.get_item_text(i))
					extra = " items=" + str(names2)
				elif m is Button:
					extra = " text=" + (m as Button).text
				lines.append("%s%s%s" % ["  ".repeat(s2[0]), m.get_class(), extra])
			print("WIDGET[" + tag + " / " + prop + "]")
			for l in lines:
				print("  " + l)
			return
	print("WIDGET[" + tag + " / " + prop + "] not found")

func _find_popups(base: Node, needle: String) -> void:
	var items: Array = []
	_walk(base, 0, items)
	for it in items:
		var n: Node = it[1]
		if n is PopupMenu:
			var pm: PopupMenu = n
			for i in pm.item_count:
				var t := pm.get_item_text(i)
				if t.findn(needle) != -1:
					print("POPUP item '%s' (index %d) in popup %s, parent chain: %s" % [t, i, pm.name, str(pm.get_parent().name) + "/" + str(pm.get_parent().get_parent().name if pm.get_parent().get_parent() else "")])

func _start() -> void:
	for i in 40:
		await get_tree().process_frame
	print("RESULT " + JSON.stringify({"id": "env", "engine": Engine.get_version_info()["string"], "headless": DisplayServer.get_name() == "headless"}))
	EditorInterface.open_scene_from_path("res://main.tscn")
	for i in 30:
		await get_tree().process_frame
	var root := EditorInterface.get_edited_scene_root()
	print("NOTE edited scene root: " + str(root))
	var color_rect: Node = root.get_node("Layer/Filter")
	EditorInterface.edit_node(color_rect)
	for i in 30:
		await get_tree().process_frame
	_dump_inspector("ColorRect Filter")
	_groups(color_rect, "ColorRect Filter")
	_dump_widget("ColorRect Filter", "anchors_preset")
	_dump_widget("ColorRect Filter", "mouse_filter")
	print("NOTE popups containing 'Full Rect' in the whole editor UI:")
	_find_popups(EditorInterface.get_base_control(), "Full Rect")
	print("NOTE popups containing 'Anchor' in the whole editor UI:")
	_find_popups(EditorInterface.get_base_control(), "Anchor")
	EditorInterface.edit_node(root.get_node("Layer"))
	for i in 20:
		await get_tree().process_frame
	_dump_inspector("CanvasLayer")
	_groups(root.get_node("Layer"), "CanvasLayer")
	EditorInterface.edit_node(root.get_node("BackBufferCopy"))
	for i in 20:
		await get_tree().process_frame
	_dump_inspector("BackBufferCopy")
	_groups(root.get_node("BackBufferCopy"), "BackBufferCopy")
	_dump_widget("BackBufferCopy", "copy_mode")
	var pm_enum: Array = []
	for p in root.get_node("BackBufferCopy").get_property_list():
		if p["name"] == "copy_mode":
			pm_enum.append(p)
	print("RESULT " + JSON.stringify({"id": "copy_mode-property", "info": pm_enum}))
	var mf: Array = []
	for p in color_rect.get_property_list():
		if p["name"] == "mouse_filter":
			mf.append(p)
	print("RESULT " + JSON.stringify({"id": "mouse_filter-property", "info": mf}))
	# a ShaderMaterial with the film's gray shader
	var mat: ShaderMaterial = color_rect.material
	EditorInterface.edit_resource(mat)
	for i in 30:
		await get_tree().process_frame
	_dump_inspector("ShaderMaterial (05-gray)")
	_groups(mat, "ShaderMaterial (05-gray)")
	var uni_rows: Array = []
	for p in mat.get_property_list():
		if String(p["name"]).begins_with("shader_parameter/"):
			uni_rows.append(p)
	print("RESULT " + JSON.stringify({"id": "shader-parameter-properties", "info": uni_rows}))
	var pool_mat: ShaderMaterial = root.get_node("Pool").material
	EditorInterface.edit_resource(pool_mat)
	for i in 30:
		await get_tree().process_frame
	_dump_inspector("ShaderMaterial (12-pool)")
	var water_rows: Array = []
	for p in pool_mat.get_property_list():
		if String(p["name"]).begins_with("shader_parameter/"):
			water_rows.append(p)
	print("RESULT " + JSON.stringify({"id": "pool-shader-parameter-properties", "info": water_rows}))
	get_tree().quit()
