@tool
extends RefCounted
func value(v):
	if v is Dictionary:
		if v.has("v2"): return Vector2(v.v2[0],v.v2[1])
		if v.has("v3"): return Vector3(v.v3[0],v.v3[1],v.v3[2])
		if v.has("color"): return Color(v.color)
		if v.has("resource"): return load(v.resource)
		if v.has("rect"): return Rect2(v.rect[0],v.rect[1],v.rect[2],v.rect[3])
	return v
func run(plugin, req):
	var root = EditorInterface.get_edited_scene_root()
	var target = root.get_node_or_null(NodePath(req.get("node",".")))
	var op = req.get("op","select")
	if op == "open":
		EditorInterface.open_scene_from_path(req.path)
		return {"opened":req.path}
	if target == null: return {"error":"missing node"}
	var screen = req.get("screen","3D" if target is Node3D else "2D")
	EditorInterface.set_main_screen_editor(screen)
	EditorInterface.get_selection().clear()
	EditorInterface.get_selection().add_node(target)
	EditorInterface.edit_node(target)
	var result = {}
	if op == "add":
		var n = ClassDB.instantiate(req.class_name)
		n.name = req.name
		var undo = plugin.get_undo_redo()
		undo.create_action("Lecture: add " + req.name)
		undo.add_do_method(target,"add_child",n)
		undo.add_do_property(n,"owner",root)
		undo.add_undo_method(target,"remove_child",n)
		undo.add_do_reference(n)
		undo.commit_action()
		target=n
		for key in req.get("properties",{}): target.set(key,value(req.properties[key]))
		EditorInterface.edit_node(target)
		EditorInterface.get_selection().clear();EditorInterface.get_selection().add_node(target)
		result["added"]=str(target.get_path())
	elif op == "set":
		var obj = target
		if req.has("resource_property"):
			obj = target.get(req.resource_property)
			EditorInterface.edit_resource(obj)
		if obj == null:return {"error":"missing resource"}
		var old = obj.get(req.property)
		var v = value(req.value)
		var undo = plugin.get_undo_redo()
		undo.create_action("Lecture: " + req.property)
		undo.add_do_property(obj,req.property,v);undo.add_undo_property(obj,req.property,old);undo.commit_action()
		obj.notify_property_list_changed()
		if req.property == "script":target.set_process(true)
		if req.has("resource_property"):EditorInterface.edit_resource(obj)
		else:EditorInterface.edit_node(target)
		if target.has_method("restart") and req.get("restart",false):target.restart()
		result={"property":req.property,"before":str(old),"after":str(obj.get(req.property))}
	elif op == "script":
		EditorInterface.edit_script(load(req.path),req.get("line",1),0,true)
		EditorInterface.set_main_screen_editor("Script")
		var ce = EditorInterface.get_script_editor().get_current_editor().get_base_editor()
		if ce is CodeEdit:
			ce.set_caret_line(int(req.get("line",1))-1)
			ce.center_viewport_to_caret()
	elif op == "call":
		result["returned"]=target.callv(req.method,req.get("args",[]))
	elif op == "zoom":
		for c in EditorInterface.get_base_control().find_children("*","Button",true,false):
			if c.is_visible_in_tree() and c.tooltip_text == "Center View":c.emit_signal("pressed")
		for c in EditorInterface.get_base_control().find_children("*","Button",true,false):
			if c.is_visible_in_tree() and "EditorZoomWidget" in str(c.get_parent().name) and "%" in c.text:
				c.emit_signal("pressed")
	elif op == "save":EditorInterface.save_scene()
	elif op == "play":EditorInterface.play_current_scene()
	elif op == "stop":EditorInterface.stop_playing_scene()
	elif op == "resource":EditorInterface.edit_resource(target.get(req.property))
	plugin.badge.text = "SCRIPTED · " + req.get("label",op)
	if req.has("filter"):
		var inspector = EditorInterface.get_inspector()
		for c in inspector.get_parent().find_children("*","LineEdit",true,false):
			if c.placeholder_text == "Filter Properties":
				c.text=req.filter;c.emit_signal("text_changed",req.filter)
	if req.get("checkpoint",false):
		var packed=PackedScene.new();packed.pack(root)
		ResourceSaver.save(packed,"res://.lecture/checkpoint-"+str(req.id)+".tscn")
	return result
