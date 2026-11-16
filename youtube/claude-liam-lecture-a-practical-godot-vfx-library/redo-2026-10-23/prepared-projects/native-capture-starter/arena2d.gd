@tool
extends Node2D
@export var heading := "Dust And Trails"
@export var moving := false
@export var stream_enabled := true
@export var repeat_preview := true
var clock:=0.0
var last_burst:=0.0
func _process(delta):
 clock+=delta
 var trail=get_node_or_null("Trail")
 if trail:trail.position=Vector2(sin(clock)*260 if moving else 0,100);trail.emitting=stream_enabled
 var dust=get_node_or_null("Dust")
 if dust and repeat_preview and clock-last_burst>2.8:dust.restart();last_burst=clock
 queue_redraw()
func _draw():
 draw_rect(Rect2(-620,-340,1240,680),Color("10151d"))
 draw_line(Vector2(-560,110),Vector2(560,110),Color("a7b3b9"),2)
 draw_string(ThemeDB.fallback_font,Vector2(-560,-280),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,36,Color.WHITE)
 draw_string(ThemeDB.fallback_font,Vector2(-560,280),"Scripted preview · world-space motion · same ground line",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("a7b3b9"))
