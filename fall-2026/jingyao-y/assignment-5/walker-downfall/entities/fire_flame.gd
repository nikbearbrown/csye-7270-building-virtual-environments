class_name FireFlame
extends MeshInstance3D

## The flames over a burning bottle's fire (CHANGE-BRIEF.md, A5): a quad facing
## the camera on res://shaders/burning_bottle_fire.gdshader, beside the hazard's
## Decal scorch. It only reads the hazard: `fire_remaining` is
## lasting / initial lasting, written each physics step after the hazard has
## counted down. It never writes game state and keeps no timer of its own.

const SHADER := preload("res://shaders/burning_bottle_fire.gdshader")

var hazard: GroundHazard
## The hazard's `lasting` before its first countdown; the denominator.
var initial_lasting := 0.0
var _material: ShaderMaterial

func _init() -> void:
	name = "Flame"
	# The hazard counts down at priority 0; this reads after it.
	process_physics_priority = 10

func _ready() -> void:
	hazard = get_parent() as GroundHazard
	initial_lasting = hazard.lasting
	var r := hazard.radius
	var quad := QuadMesh.new()
	quad.size = Vector2(2.0 * r, 1.6 * r)
	# Bottom edge on the node's origin.
	quad.center_offset = Vector3(0.0, 0.8 * r, 0.0)
	mesh = quad
	position.y = 0.04
	cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	# Its own material on the shared shader, so each fire keeps its own value.
	_material = ShaderMaterial.new()
	_material.shader = SHADER
	_material.set_shader_parameter("fire_remaining", 1.0)
	material_override = _material
	_face_camera()

func _physics_process(_delta: float) -> void:
	if not is_instance_valid(hazard) or not is_instance_valid(hazard.game): return
	if not hazard.game.simulation_active(): return
	_material.set_shader_parameter("fire_remaining", clampf(hazard.lasting / initial_lasting, 0.0, 1.0))

func _process(_delta: float) -> void:
	_face_camera()

## The shader has no billboard of its own; the camera turns and tilts.
func _face_camera() -> void:
	if not is_inside_tree() or not is_instance_valid(hazard) or not is_instance_valid(hazard.game): return
	var cam := hazard.game.camera
	if is_instance_valid(cam): global_basis = cam.global_basis
