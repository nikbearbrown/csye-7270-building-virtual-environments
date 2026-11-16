@tool
extends Node3D
@export var heading := "Read The Game And Its Contract"
@export var preview_burst := false
@export var preview_motes := false
var clock:=0.0
func _process(delta):
 clock+=delta
 var title=get_node_or_null("LectureTitle")
 if title:title.text=heading+"\nDerived editor lab · gameplay remains in main.tscn"
 var burst=get_node_or_null("Burst")
 if burst and preview_burst and clock>2:
  burst.restart();burst.emitting=true;clock=0
 var motes=get_node_or_null("Motes")
 if motes:motes.emitting=preview_motes
