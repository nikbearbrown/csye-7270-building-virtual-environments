@tool
extends EditorPlugin
const OUT := "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-6/evidence/use-it-code/supplement"
var visual: Node
var monitors: Node
var records: Array=[]
func _enter_tree(): call_deferred("run")
func find_class(n:Node, klass:String):
	if n.get_class()==klass: return n
	for c in n.get_children(true):
		var found=find_class(c,klass)
		if found!=null: return found
	return null
func rows(item:TreeItem,cols:int,output:Array):
	if item==null: return
	var cells=[]
	for i in cols: cells.append(item.get_text(i))
	output.append(cells)
	var c=item.get_first_child()
	while c!=null:
		rows(c,cols,output)
		c=c.get_next()
func read_panel(panel:Node):
	var output=[]
	for tree in panel.find_children("*","Tree",true,false): rows(tree.get_root(),tree.columns,output)
	return output
func show_panel(panel:Node):
	var n=panel
	while n.get_parent()!=null:
		var parent=n.get_parent()
		if parent is TabContainer: parent.current_tab=n.get_index()
		n=parent
	for b in EditorInterface.get_base_control().find_children("*","Button",true,false):
		if b.text.begins_with("Debugger") and b.get_parent().get_class()!="TabBar":
			if b.toggle_mode and not b.button_pressed:
				b.button_pressed=true
				b.pressed.emit()
func snap(name):
	show_panel(visual)
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var img=EditorInterface.get_base_control().get_viewport().get_texture().get_image()
	if img!=null: img.save_png(OUT.path_join(name+"_editor.png"))
func run():
	for i in 60: await get_tree().process_frame
	while EditorInterface.get_resource_filesystem().is_scanning(): await get_tree().process_frame
	visual=find_class(get_tree().root,"EditorVisualProfiler")
	monitors=find_class(get_tree().root,"EditorPerformanceProfiler")
	if visual==null or monitors==null:
		printerr("PROFILER_NODES_MISSING")
		get_tree().quit(1)
		return
	EditorInterface.get_resource_filesystem().scan()
	for i in 20: await get_tree().process_frame
	while EditorInterface.get_resource_filesystem().is_scanning(): await get_tree().process_frame
	EditorInterface.play_custom_scene("res://use_it_runner.tscn")
	var started=false
	var previous=""
	var since=0.0
	var photographed=false
	var end=Time.get_ticks_msec()+240000
	while Time.get_ticks_msec()<end:
		await get_tree().create_timer(0.5).timeout
		if not started:
			for b in visual.find_children("*","Button",true,false):
				if b.text=="Start" and not b.disabled:
					b.button_pressed=true
					b.pressed.emit()
					started=true
					print("VISUAL_PROFILER_STARTED")
		var phase=FileAccess.get_file_as_string("/tmp/a6-use-it/phase.txt") if FileAccess.file_exists("/tmp/a6-use-it/phase.txt") else "waiting"
		if phase!=previous:
			previous=phase
			since=0
			photographed=false
		since+=0.5
		var record={"phase":phase,"visual_started":started,"visual":read_panel(visual),"monitors":read_panel(monitors)}
		records.append(record)
		FileAccess.open(OUT.path_join("editor-profiler.json"),FileAccess.WRITE).store_string(JSON.stringify(records,"\t"))
		if phase.begins_with("0") and since>=0.5 and not photographed:
			await snap(phase)
			photographed=true
		if phase=="done": break
		if phase!="waiting" and not EditorInterface.is_playing_scene(): break
	print("PROFILER_FINAL ",JSON.stringify(records.back() if not records.is_empty() else {}))
	EditorInterface.stop_playing_scene()
	await get_tree().create_timer(1.0).timeout
	get_tree().quit()
