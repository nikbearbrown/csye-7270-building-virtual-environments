class_name TabletDevice
extends Node3D

const SCREEN_LIGHT_PARAM := &"pad_light_data"
const SCREEN_OFF_STRENGTH := 0.0
const SCREEN_IMAGE_PARAM := &"screen_image"
const NOT_ON_SCREEN := Vector2(-1.0, -1.0)
const UV_MIN := 0.0
const UV_MAX := 1.0
const UV_CENTER := 0.5

@export_range(0.0, 1.0) var light_strength_percentage: float = 0.39

@onready var _screen: MeshInstance3D = $Screen


func get_screen() -> MeshInstance3D:
	return _screen


func set_screen_lit(lit: bool) -> void:
	var screen_material := _screen.get_surface_override_material(0) as ShaderMaterial
	var strength := light_strength_percentage if lit else SCREEN_OFF_STRENGTH
	screen_material.set_shader_parameter(SCREEN_LIGHT_PARAM, strength)


func set_screen_image(image: Texture2D) -> void:
	var screen_material := _screen.get_surface_override_material(0) as ShaderMaterial
	screen_material.set_shader_parameter(SCREEN_IMAGE_PARAM, image)


func get_screen_uv(ray_origin: Vector3, ray_direction: Vector3) -> Vector2:
	var to_screen := _screen.global_transform.affine_inverse()
	var origin := to_screen * ray_origin
	var direction := to_screen.basis * ray_direction
	if is_zero_approx(direction.z):
		return NOT_ON_SCREEN
	var distance := -origin.z / direction.z
	if distance < 0.0:
		return NOT_ON_SCREEN
	var hit := origin + direction * distance
	var screen_size := (_screen.mesh as QuadMesh).size
	var uv := Vector2(hit.x / screen_size.x + UV_CENTER, UV_CENTER - hit.y / screen_size.y)
	if uv.x < UV_MIN or uv.x > UV_MAX or uv.y < UV_MIN or uv.y > UV_MAX:
		return NOT_ON_SCREEN
	return uv
