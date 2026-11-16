extends Node
# One clock, one set of numbers, for the shader and for everything that floats. The vertex shader moves the drawing; the engine's nodes do not know,
# so this script gives the shader its numbers and runs the same wave function to put each floater on the surface.
const WaveMath = preload("wave_math.gd")

@export var water: MeshInstance3D
@export var floaters: Array[Node3D] = []
@export var wave_height := 0.12
@export var wave_length := 3.0
@export var wave_speed := 0.8
var clock := 0.0

func _process(delta: float) -> void:
	set_clock(clock + delta)

func set_clock(t: float) -> void:
	clock = t
	var mat := water.material_override as ShaderMaterial
	mat.set_shader_parameter("wave_clock", t)
	mat.set_shader_parameter("wave_height", wave_height)
	mat.set_shader_parameter("wave_length", wave_length)
	mat.set_shader_parameter("wave_speed", wave_speed)
	for f in floaters:
		var p := Vector2(f.position.x, f.position.z)
		f.position.y = WaveMath.height(p, t, wave_height, wave_length, wave_speed)
