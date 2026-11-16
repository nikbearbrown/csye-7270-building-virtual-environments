@tool
extends Node2D
## Original 2D teaching arena. Rendering and all particles belong to Godot.
@export var heading := "Make The First Particle Visible"
@export var move_source := false
@export var stream_enabled := true
@export var staged_hidden_owner := false
var clock := 0.0
var trigger_count := 0
var completed_count := 0
var last_note := "SPACE burst · arrows move · T stream · H marker · R reset"
var runtime_input_id := ""

func _ready() -> void:
	set_process(true)
	if not Engine.is_editor_hint():
		for pair in [["burst",KEY_SPACE],["stream",KEY_T],["hide_marker",KEY_H],["reset",KEY_R],["left",KEY_LEFT],["right",KEY_RIGHT]]:
			if not InputMap.has_action(pair[0]):
				InputMap.add_action(pair[0]);var e=InputEventKey.new();e.physical_keycode=pair[1];InputMap.action_add_event(pair[0],e)

func _process(delta: float) -> void:
	clock += delta
	var marker=get_node_or_null("Marker")
	if marker:
		if move_source:marker.position.x=sin(clock*1.3)*200.0
		if not Engine.is_editor_hint():marker.position.x=clampf(marker.position.x+Input.get_axis("left","right")*260*delta,-350,350)
	var stream=get_node_or_null("Trail")
	if stream and marker:
		stream.position=marker.position
		stream.emitting=stream_enabled
	if not Engine.is_editor_hint():read_scripted_input()
	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("burst") and not event.is_echo():spawn_burst()
	if event.is_action_pressed("stream") and not event.is_echo():stream_enabled=not stream_enabled
	if event.is_action_pressed("hide_marker") and not event.is_echo():get_node("Marker").visible=not get_node("Marker").visible
	if event.is_action_pressed("reset") and not event.is_echo():
		get_node("Marker").visible=true;get_node("Marker").position=Vector2(0,100);stream_enabled=false
		for n in get_tree().get_nodes_in_group("temporary_effect"):n.queue_free()

func spawn_burst() -> void:
	var marker=get_node("Marker")
	var effect=load("res://effects/pickup_burst.tscn").instantiate()
	var host=marker if staged_hidden_owner else self
	host.add_child(effect)
	effect.global_position=marker.global_position
	effect.add_to_group("temporary_effect")
	trigger_count+=1
	effect.finished.connect(func():completed_count+=1;effect.queue_free())
	effect.emitting=true
	if staged_hidden_owner:marker.hide()
	last_note="Input burst %d · owner %s · visible %s" % [trigger_count,host.name,effect.is_visible_in_tree()]

func read_scripted_input() -> void:
	var path="res://.lecture/input.json"
	if not FileAccess.file_exists(path):return
	var req=JSON.parse_string(FileAccess.get_file_as_string(path))
	if not req is Dictionary or str(req.get("id",""))==runtime_input_id:return
	runtime_input_id=str(req.id)
	if req.has("property"):set(req.property,req.value)
	if req.has("key"):
		var key=OS.find_keycode_from_string(str(req.key))
		var event=InputEventKey.new();event.physical_keycode=key;event.keycode=key;event.pressed=req.get("pressed",true)
		Input.parse_input_event(event)
	var f=FileAccess.open("res://.lecture/input-log.jsonl",FileAccess.READ_WRITE)
	if f==null:f=FileAccess.open("res://.lecture/input-log.jsonl",FileAccess.WRITE)
	f.seek_end();f.store_line(JSON.stringify({"request":req,"ticks":Time.get_ticks_msec(),"method":"Input.parse_input_event; scripted ordinary input path"}));f.close()

func _draw() -> void:
	draw_rect(Rect2(-540,-360,1080,720),Color("111721"))
	draw_rect(Rect2(0,-240,500,450),Color("dce3de"))
	for x in range(-500,501,100):draw_line(Vector2(x,-240),Vector2(x,250),Color("43505a"),1)
	draw_line(Vector2(-500,250),Vector2(500,250),Color("83919e"),2)
	var font=ThemeDB.fallback_font
	draw_string(font,Vector2(-505,-305),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,32,Color.WHITE)
	draw_string(font,Vector2(-505,-267),"DARK / LIGHT · same texture, same motion",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("c2cbd1"))
	draw_string(font,Vector2(-505,300),last_note,HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
	var count=0
	if is_inside_tree():count=get_tree().get_nodes_in_group("temporary_effect").size()
	draw_string(font,Vector2(-505,337),"TRIGGERED %d   FINISHED %d   INSTANCES %d" % [trigger_count,completed_count,count],HORIZONTAL_ALIGNMENT_LEFT,-1,21,Color("7ce5c0"))
