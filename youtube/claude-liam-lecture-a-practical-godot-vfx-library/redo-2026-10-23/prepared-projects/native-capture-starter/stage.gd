@tool
extends Node3D
@export var heading := "Build An Explosion"
@export_enum("Explosion","Campfire","Rain","Magic") var selected_effect := "Explosion"
var spawned := 0
var cleaned := 0
var input_request := ""
func _ready():
 var camera=get_node_or_null("Camera")
 if camera:camera.position=Vector3(7,5,8);camera.look_at(Vector3(0,1,0))
func _process(_delta):
 var title=get_node_or_null("Title")
 if title:title.text=heading
 if Engine.is_editor_hint():return
 var p="res://.lecture/input.json"
 if FileAccess.file_exists(p):
  var text=FileAccess.get_file_as_string(p)
  if text!=input_request:
   input_request=text;var req=JSON.parse_string(text)
   if req is Dictionary and req.has("key"):
    var event=InputEventKey.new();event.keycode=OS.find_keycode_from_string(req.key);event.physical_keycode=event.keycode;event.pressed=req.get("pressed",true);Input.parse_input_event(event)
func _unhandled_input(event):
 if event is InputEventKey and event.pressed and not event.echo and event.keycode==KEY_SPACE:spawn_effect()
func spawn_effect():
 var file="res://effects/"+selected_effect.to_snake_case()+".tscn"
 if not ResourceLoader.exists(file):return
 var effect=load(file).instantiate();effect.name="Instance"+str(spawned);effect.preview_loop=false;effect.auto_free=true;add_child(effect);effect.position=Vector3(0,.15,0)
 effect.tree_exited.connect(func():cleaned+=1;update_status());effect.play();spawned+=1;update_status()
func update_status():
 var label=get_node_or_null("Status")
 if label:label.text="SPACE · play saved scene | spawned %d · cleaned %d · active %d"%[spawned,cleaned,spawned-cleaned]
