extends "res://signal-garden/garden.gd"
# Isolated instructional derivative. Existing game authority stays in garden.gd.
var input_request := ""
var staged_player_hidden := false
var diagnostics:Label
var effect_events: Array[Dictionary] = []
func _ready():
 super._ready()
 var ambient_position=ambient.position
 remove_child(burst);burst.queue_free();remove_child(ambient);ambient.queue_free()
 burst=load("res://effects/burst.tscn").instantiate();ambient=load("res://effects/ambient.tscn").instantiate()
 add_child(burst);add_child(ambient);ambient.position=ambient_position
 audio_enabled=false;sound.enabled=false;sound.stop_all()
 hud.text="SIGNAL GARDEN · Isolated teaching copy"
 diagnostics=Label.new();diagnostics.position=Vector2(38,610);diagnostics.add_theme_font_size_override("font_size",19);hud.get_parent().add_child(diagnostics)
func fire_burst(at:Vector3):
 super.fire_burst(at)
 effect_events.append({"position":str(at),"ticks_msec":Time.get_ticks_msec(),"event":effect_events.size()+1})
func _process(_delta):
 if is_instance_valid(player):player.visible=not staged_player_hidden
 if is_instance_valid(diagnostics):diagnostics.text="Scripted-input diagnostics · events %d · burst %s · motes %s · paused %s"%[effect_events.size(),burst.emitting,ambient.emitting,get_tree().paused]
 var p="res://.lecture/input.json"
 if not FileAccess.file_exists(p):return
 var text=FileAccess.get_file_as_string(p)
 if text==input_request:return
 input_request=text
 var req=JSON.parse_string(text)
 if not req is Dictionary:return
 if req.has("key"):
  var event=InputEventKey.new();event.keycode=OS.find_keycode_from_string(req.key);event.physical_keycode=event.keycode;event.pressed=req.get("pressed",true);Input.parse_input_event(event)
 if req.has("property"):set(req.property,req.value)
 var f=FileAccess.open("res://.lecture/input-log.jsonl",FileAccess.READ_WRITE)
 if f==null:f=FileAccess.open("res://.lecture/input-log.jsonl",FileAccess.WRITE)
 f.seek_end();f.store_line(JSON.stringify({"request":req,"gate_open":gate_open,"won":won,"paused":get_tree().paused,"burst_emitting":burst.emitting,"ambient_emitting":ambient.emitting,"player":str(player.position),"events":effect_events}));f.close()
