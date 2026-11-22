extends Node3D
## Fixture (agent, 2026-11-22): the wave_release rig alone, before wiring, on a
## plain grey ground, so the keys can be seen moving. The clip is advanced by
## 1/30 s each frame (the brief's manual clock), starting at capture frame 10.
## Capture: godot --path . res://previews/wave_rig_turntable.tscn --write-movie <abs>/f.png --fixed-fps 30 --quit-after 40

const RIG := preload("res://animations/lappland_wave_rig.tscn")
var rig: Node3D
var player: AnimationPlayer
var frame := 0

func _ready() -> void:
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 8.0
	cam.position = Vector3(0, 0.3, 5)
	add_child(cam)
	var ground := MeshInstance3D.new()
	var plane := PlaneMesh.new()
	plane.size = Vector2(20, 20)
	ground.mesh = plane
	ground.position.y = -0.65
	add_child(ground)
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-50, 30, 0)
	add_child(light)
	rig = RIG.instantiate()
	add_child(rig)
	(rig.get_node("Billboard") as Sprite3D).visible = true
	player = rig.get_node("AnimationPlayer")
	player.play(&"RESET")
	player.advance(0.0)

func _process(_delta: float) -> void:
	if frame == 10:
		player.play(&"wave_release")
		player.advance(0.0)
	elif frame > 10 and frame <= 30:
		player.advance(1.0 / 30.0)
	frame += 1
