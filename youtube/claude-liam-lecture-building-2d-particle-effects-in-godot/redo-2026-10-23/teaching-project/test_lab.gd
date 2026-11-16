extends SceneTree
var arena:Node2D
var rows:Array=[]
var failures:=0
func _initialize():call_deferred("run")
func frames(n:int):
	for i in range(n):await process_frame
func check(label:String,ok:bool,details:Variant=""):
	rows.append({"check":label,"pass":ok,"details":details});print(JSON.stringify(rows.back()))
	if not ok:failures+=1
func key(code:Key,down:bool):
	var e=InputEventKey.new();e.keycode=code;e.physical_keycode=code;e.pressed=down;Input.parse_input_event(e)
func tap(code:Key):
	key(code,true);await frames(2);key(code,false);await frames(2)
func run():
	arena=load("res://arena.tscn").instantiate();root.add_child(arena);arena.position=Vector2(640,360)
	await frames(4)
	check("starts-without-temporary-bursts",get_nodes_in_group("temporary_effect").is_empty())
	await tap(KEY_SPACE)
	var effects=get_nodes_in_group("temporary_effect")
	check("ordinary-space-input-spawns",effects.size()==1,effects.size())
	if not effects.is_empty():check("spawn-at-marker",effects[0].global_position.distance_to(arena.get_node("Marker").global_position)<.01)
	await create_timer(2.2).timeout;print("DIAG ",effects[0].emitting if is_instance_valid(effects[0]) else "freed");check("finished-removes-instance",get_nodes_in_group("temporary_effect").is_empty())
	arena.staged_hidden_owner=true;await tap(KEY_SPACE);effects=get_nodes_in_group("temporary_effect")
	check("staged-hidden-owner-is-invisible",effects.size()==1 and not effects[0].is_visible_in_tree())
	await create_timer(2.2).timeout;arena.staged_hidden_owner=false;await tap(KEY_SPACE);effects=get_nodes_in_group("temporary_effect")
	check("repaired-owner-visible-with-hidden-marker",effects.size()==1 and effects[0].is_visible_in_tree())
	await create_timer(2.2).timeout;await tap(KEY_R)
	var x=arena.get_node("Marker").position.x
	key(KEY_RIGHT,true);await frames(60);key(KEY_RIGHT,false);await frames(2)
	check("ordinary-arrow-input-moves-marker",arena.get_node("Marker").position.x>x+100,arena.get_node("Marker").position.x)
	for i in range(3):await tap(KEY_SPACE);await create_timer(2.2).timeout
	check("repeated-bursts-bounded",get_nodes_in_group("temporary_effect").is_empty() and arena.completed_count==arena.trigger_count,{"finished":arena.completed_count,"triggered":arena.trigger_count})
	print("RESULT %d checks / %d failures" % [rows.size(),failures]);quit(1 if failures else 0)
