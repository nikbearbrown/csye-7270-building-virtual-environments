extends SceneTree
var game:Node3D
var checks:Array[Dictionary]=[]
func _initialize():call_deferred("run")
func check(id,ok,details=""):
 checks.append({"id":id,"pass":ok,"details":details});print(JSON.stringify(checks.back()))
func steps(n):
 for i in range(n):await physics_frame;await process_frame
func key(code,pressed):
 var e=InputEventKey.new();e.keycode=code;e.physical_keycode=code;e.pressed=pressed;Input.parse_input_event(e)
func press(code,n):key(code,true);await steps(n);key(code,false);await steps(1)
func open_gate():
 await press(KEY_RIGHT,40);await press(KEY_E,1);await steps(38)
func run():
 game=load("res://main.tscn").instantiate();root.add_child(game);current_scene=game;await steps(4)
 check("startup-inactive",not game.burst.emitting and not game.ambient.emitting)
 await open_gate();check("ordinary-input-gate-event",game.gate_open and game.effect_events.size()==1 and game.burst.emitting)
 check("root-owned-visible-burst",game.burst.get_parent()==game and game.burst.is_visible_in_tree())
 check("route-motes-start",game.ambient.emitting)
 key(KEY_P,true);await steps(2);key(KEY_P,false);await steps(1)
 check("pause-retains-emission-property",paused and game.ambient.emitting)
 check("pause-stops-effect-processing",not game.ambient.can_process() and not game.burst.can_process())
 key(KEY_P,true);await steps(2);key(KEY_P,false);await steps(2)
 check("resume-processing",not paused and game.ambient.can_process())
 game.hide();await steps(2);check("hidden-stops-new-motes",not game.ambient.emitting)
 game.show();await steps(2);check("show-restores-route-condition",game.ambient.emitting)
 await press(KEY_R,1);check("reset-stops-both",not game.burst.emitting and not game.ambient.emitting and not game.gate_open)
 await open_gate();await press(KEY_RIGHT,140)
 check("ordinary-input-finish",game.won and game.finish_count==1)
 check("three-burst-events",game.effect_events.size()>=3,game.effect_events)
 check("two-event-positions",game.effect_events[0].position!=game.effect_events[-1].position)
 check("finish-stops-motes",not game.ambient.emitting)
 await steps(130);check("finish-burst-ages-out",not game.burst.emitting)
 game.fire_burst(Vector3(-2,0,0));await steps(3);game.fire_burst(Vector3(2,0,0));await steps(2)
 check("intentional-single-emitter-replacement",game.burst.position.distance_to(Vector3(2,.4,0))<.001 and game.burst.emitting)
 await steps(60);check("replacement-also-finishes",not game.burst.emitting)
 var failed=checks.filter(func(x):return not x.pass).size()
 print("RESULT ",checks.size()," checks / ",failed," failures; state checks are not visual approval")
 game.queue_free();await process_frame;quit(1 if failed else 0)
