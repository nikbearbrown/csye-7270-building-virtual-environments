extends Node3D

@export var body: Humanoid

@onready var _dust: GPUParticles3D = $Dust
@onready var _ground_ring: GPUParticles3D = $GroundRing


func _ready() -> void:
	if body == null:
		return
	body.landed.connect(_on_body_landed)


func _on_body_landed() -> void:
	global_position = body.global_position
	_dust.restart()
	_ground_ring.restart()
