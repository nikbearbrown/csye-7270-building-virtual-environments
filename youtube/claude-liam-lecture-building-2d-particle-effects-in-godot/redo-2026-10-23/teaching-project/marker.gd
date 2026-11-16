@tool
extends Node2D
func _draw():
	draw_circle(Vector2.ZERO,18,Color("d97757"))
	draw_arc(Vector2.ZERO,24,0,TAU,40,Color.WHITE,2)
