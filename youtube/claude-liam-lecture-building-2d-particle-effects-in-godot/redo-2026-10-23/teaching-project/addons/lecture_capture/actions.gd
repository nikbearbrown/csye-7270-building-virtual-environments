@tool
extends RefCounted
func value(v):
	if v is Dictionary:
		if v.has("v2"): return Vector2(v.v2[0],v.v2[1])
		if v.has("v3"): return Vector3(v.v3[0],v.v3[1],v.v3[2])
		if v.has("color"): return Color(v.color)
		if v.has("resource"): return load(v.resource)
		if v.has("rect"): return Rect2(v.rect[0],v.rect[1],v.rect[2],v.rect[3])
		if v.has("aabb"): return AABB(Vector3(v.aabb[0],v.aabb[1],v.aabb[2]),Vector3(v.aabb[3],v.aabb[4],v.aabb[5]))
		if v.has("new"):
			var obj=ClassDB.instantiate(v.new)
			for key in v.get("props",{}):obj.set(key,value(v.props[key]))
			return obj
	return v
func run(plugin, req):
	plugin.hide_bottom_panel()
	if req.get("op","")=="ui_dump":
		var rows=[]
		for c in EditorInterface.get_base_control().find_children("*","BaseButton",true,false):
			if c.is_visible_in_tree():
				var row={"name":str(c.get_path()),"text":c.text if c is Button else "","tooltip":c.tooltip_text}
				if c is MenuButton:
					row["items"]=[]
					for i in range(c.get_popup().item_count):row["items"].append({"id":c.get_popup().get_item_id(i),"text":c.get_popup().get_item_text(i)})
				rows.append(row)
		return {"buttons":rows}

	if req.get("op","")=="game_input":
		var f=FileAccess.open("res://.lecture/input.json",FileAccess.WRITE);f.store_string(JSON.stringify(req));f.close()
		plugin.badge.text="SCRIPTED · ordinary game input " + str(req.get("key",req.get("property","")))
		return {"input_request_written":req.id}
	var root = EditorInterface.get_edited_scene_root()
	var target = root.get_node_or_null(NodePath(req.get("node",".")))
	var op = req.get("op","select")
	if op == "open":
		EditorInterface.open_scene_from_path(req.path)
		return {"opened":req.path}
	if target == null: return {"error":"missing node"}
	if op=="call":
		plugin.badge.text="SCRIPTED · "+req.get("label",op)
		return {"returned":target.callv(req.method,req.get("args",[]))}
	var screen = req.get("screen","3D" if target is Node3D else "2D")
	EditorInterface.set_main_screen_editor(screen)
	EditorInterface.get_selection().clear()
	EditorInterface.get_selection().add_node(target)
	EditorInterface.edit_node(target)
	await plugin.get_tree().process_frame
	await plugin.get_tree().process_frame
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
		for key in req.get("resource_chain",[]):
			obj=obj.get(key)
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
			if c.is_visible_in_tree() and "EditorZoomWidget" in str(c.get_parent().name) and "%" in c.text:
				c.emit_signal("pressed")
		for c in EditorInterface.get_base_control().find_children("*","MenuButton",true,false):
			if c.is_visible_in_tree() and c.text=="View":
				for i in range(c.get_popup().item_count):
					if c.get_popup().get_item_text(i)=="Frame Selection":c.get_popup().emit_signal("id_pressed",c.get_popup().get_item_id(i))
	elif op == "save":EditorInterface.save_scene()
	elif op == "save_branch":
		var packed=PackedScene.new();packed.pack(target);result["save_error"]=ResourceSaver.save(packed,req.path)
	elif op == "unique":
		var original=target.get(req.property)
		target.set(req.property,original.duplicate(true));EditorInterface.edit_resource(target.get(req.property))
		result={"shared_before":original.get_instance_id(),"unique_after":target.get(req.property).get_instance_id()}
	elif op == "duplicate":
		var copy=target.duplicate();copy.name=req.name;target.get_parent().add_child(copy);copy.owner=root
		for key in req.get("properties",{}):copy.set(key,value(req.properties[key]))
		EditorInterface.edit_node(copy);result["added"]=str(copy.get_path())
	elif op == "cpu_convert":
		var cpu=CPUParticles2D.new();cpu.convert_from_particles(target);cpu.name=req.name;target.get_parent().add_child(cpu);cpu.owner=root;cpu.position=target.position
		target.hide();EditorInterface.edit_node(cpu);result["converted"]=str(cpu.get_path())
	elif op == "play":EditorInterface.play_current_scene()
	elif op == "play_custom":EditorInterface.play_custom_scene(req.path)
	elif op == "stop":EditorInterface.stop_playing_scene()
	elif op == "resource":
		var resource=target.get(req.property)
		for key in req.get("resource_chain",[]):resource=resource.get(key)
		EditorInterface.edit_resource(resource)
	await plugin.get_tree().process_frame
	plugin.badge.text = "SCRIPTED · " + req.get("label",op)
	if true:
		var inspector = EditorInterface.get_inspector()
		for c in EditorInterface.get_base_control().find_children("*","LineEdit",true,false):
			if is_instance_valid(c) and c.placeholder_text == "Filter Properties":
				var query=req.get("filter",str(req.get("property","")).replace("_"," ") if op=="set" else "")
				if c.text!=query:c.text=query;c.emit_signal("text_changed",query)
				break
	if req.get("checkpoint",false):
		var packed=PackedScene.new();packed.pack(root)
		ResourceSaver.save(packed,"res://.lecture/checkpoint-"+str(req.id)+".tscn")
	return result
