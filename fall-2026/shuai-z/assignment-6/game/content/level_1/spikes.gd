class_name Spikes
extends Area2D
## A row of spikes (ENV-SPIKES). Touching them costs Rudy a heart. They check
## every physics tick, so standing on them hurts again once his invulnerability
## ends. The art is five iron spikes on a wooden plank, 106 px wide with the
## tips 63 px up, drawn at half scale from props.json's origin with the outer
## outline. The box that hurts covers the row of spikes (80 px), not the
## plank's ends, and stops 11 px below the tips, so a graze of a tip is a miss.
## Each row stands between two of the ground's tall wheat tufts, so no tuft
## shows behind it. The origin is at the middle of the plank, on the ground.

const WIDTH := 80.0 ## the box that hurts


func _physics_process(_delta: float) -> void:
	for body in get_overlapping_bodies():
		if body is Rudy:
			(body as Rudy).take_hit(global_position)
