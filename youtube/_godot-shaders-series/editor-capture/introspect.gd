extends SceneTree
# Prints ClassDB facts about the editor-facing classes of THIS Godot build, so the driver only uses APIs that exist.
# Run:  godot --headless --path <any dir> --script res://introspect.gd   (no window; no editor)

func _initialize() -> void:
	print("VERSION ", Engine.get_version_info()["string"])
	for cls in ["EditorInterface", "EditorInspector", "EditorPlugin", "EditorProperty", "EditorResourcePicker", "EditorSelection",
			"EditorSettings", "ScrollContainer", "ColorPickerButton", "EditorUndoRedoManager", "EditorScript", "EditorToaster",
			"ShaderMaterial", "Shader", "EditorFileSystem", "ProjectSettings"]:
		print("")
		print("=== CLASS ", cls, "  exists=", ClassDB.class_exists(cls), "  parent=", ClassDB.get_parent_class(cls))
		if not ClassDB.class_exists(cls):
			continue
		for m in ClassDB.class_get_method_list(cls, true):
			var args := []
			for a in m["args"]:
				args.append("%s:%s" % [a["name"], type_string(a["type"]) if a["type"] != TYPE_OBJECT else String(a["class_name"])])
			var ret = m["return"]
			var rt: String = type_string(ret["type"]) if ret["type"] != TYPE_OBJECT else String(ret["class_name"])
			print("  m ", m["name"], "(", ", ".join(args), ") -> ", rt)
		for p in ClassDB.class_get_property_list(cls, true):
			print("  p ", p["name"], " : ", type_string(p["type"]))
		for s in ClassDB.class_get_signal_list(cls, true):
			print("  s ", s["name"])
	# classes that may exist but are not scriptable
	for cls in ["ShaderCreateDialog", "TextShaderEditor", "ShaderEditorPlugin", "EditorInspectorSection", "EditorPropertyResource", "EditorSpinSlider",
			"EditorPropertyColor", "EditorZoomWidget", "CanvasItemEditor", "EditorBottomPanel", "EditorNode", "ShaderEditor", "EditorDock", "EditorDockManager"]:
		print("EXISTS? ", cls, " ", ClassDB.class_exists(cls), "  instantiable=", ClassDB.can_instantiate(cls) if ClassDB.class_exists(cls) else "n/a")
	quit()
