# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name TabletDevice  # Global class name: a tablet device (every character carries its own)
extends Node3D  # Extends Node3D: has a position and rotation and can be attached to a character
## Tablet device: the root script of tablet_device.tscn.
## Every character instances its own tablet, so every tablet has its own Screen node (there is no single global tablet).
## Presentation only: it neither stores nor changes the tablet state (the state is Humanoid's _tablet_hold, rule 5).

# ============================================================
# Constants: values for the screen glow, defined once and never changed
# ============================================================
const SCREEN_LIGHT_PARAM := &"pad_light_data"  # Name of the glow-strength parameter in the screen shader (pad_base_light.gdshader); must match the shader exactly
const SCREEN_OFF_STRENGTH := 0.0  # What pad_light_data is set to when the screen is off: 0 = fully black
const SCREEN_IMAGE_PARAM := &"screen_image"  # Name of the "picture to show" parameter in the screen shader; must match the shader exactly
const NOT_ON_SCREEN := Vector2(-1.0, -1.0)  # get_screen_uv() returns this when the line misses the screen; real screen positions are all between 0 and 1, so they cannot be confused with it
const UV_MIN := 0.0  # Smallest screen position value: the left edge, the top edge
const UV_MAX := 1.0  # Largest screen position value: the right edge, the bottom edge
const UV_CENTER := 0.5  # The screen's exact centre; the screen quad's centre point is at its own (0, 0), so we add this to turn it into 0 to 1

# ============================================================
# Exported variables (@export): feel values shown in the inspector and tuned there
# ============================================================
## Feel values (code rule 1a): tuned in the inspector, not hard-coded.
@export_range(0.0, 1.0) var light_strength_percentage: float = 0.39  # Brightness while the tablet is held; the value is a percentage

# ============================================================
# Node references (@onready): child nodes used in the scene
# ============================================================
# @onready: assigned after the node enters the scene tree and its children are ready
@onready var _screen: MeshInstance3D = $Screen  # Screen: a thin quad (QuadMesh) 1 mm in front of the model's screen; its material is swapped separately later


# ============================================================
# Feature functions: public functions for outside callers
# ============================================================
## Returns this tablet's screen node. In A5, changing the screen's material or parameters starts from here.
## The material on Screen has Local To Scene ticked: every time a tablet is instanced, Godot gives it its own copy of the material, so the tablets' screens do not affect each other.
## To light or darken the screen, call set_screen_lit() below; do not change the material parameter directly anywhere else.
func get_screen() -> MeshInstance3D:
	return _screen


## Lights or darkens this tablet's screen: when lit is true the screen glows at light_strength_percentage, when false it is fully black.
## Called by Humanoid every physics frame (Humanoid decides "has the tablet reached the hand"; this only displays it and decides nothing, rule 5).
## Changes only this tablet's own material (the material has Local To Scene, so every tablet has its own copy); other characters' screens are not affected.
func set_screen_lit(lit: bool) -> void:
	# Read the override material on Screen's surface 0 (the inspector's Surface Material Override → 0 slot), cast to ShaderMaterial so shader parameters can be set
	var screen_material := _screen.get_surface_override_material(0) as ShaderMaterial
	# Pick one: if lit is true take the lit strength, otherwise SCREEN_OFF_STRENGTH (0, fully black)
	var strength := light_strength_percentage if lit else SCREEN_OFF_STRENGTH
	# Write pad_light_data = strength into this material's parameter table; the next time the screen is drawn, pad_light_data in the shader has this value
	screen_material.set_shader_parameter(SCREEN_LIGHT_PARAM, strength)


## The player brain calls this when the game starts: it tells this tablet's screen which picture to show (the tablet OS canvas).
## Only the local player's tablets are handed the picture; nobody hands one to other characters' tablets, so when their screens light they show the original cool white.
func set_screen_image(image: Texture2D) -> void:
	var screen_material := _screen.get_surface_override_material(0) as ShaderMaterial  # First we get this tablet's own screen material (Local To Scene is ticked, so every tablet has its own copy)
	screen_material.set_shader_parameter(SCREEN_IMAGE_PARAM, image)  # Then we hand the picture to the shader's screen_image; from then on, every frame the screen draws takes its colours from this picture


## The player brain calls this when the player moves or clicks the mouse: it gives us a line shot from a camera (start + direction), and we work out where it hits this tablet's screen.
## The returned position is (0, 0) at the top-left and (1, 1) at the bottom-right; if the line misses the screen it returns NOT_ON_SCREEN. The brain then converts it to a pixel on the tablet OS canvas.
func get_screen_uv(ray_origin: Vector3, ray_direction: Vector3) -> Vector2:
	var to_screen := _screen.global_transform.affine_inverse()  # First we prepare a conversion "into the screen's own view": in the screen's own view, its centre is (0, 0, 0) and it lies flat on z = 0
	var origin := to_screen * ray_origin  # We convert the line's start to a position in the screen's view
	var direction := to_screen.basis * ray_direction  # We convert the line's direction too (a direction only turns and never moves, so we use only the basis)
	if is_zero_approx(direction.z):  # If this line is parallel to the screen, it can never reach the screen
		return NOT_ON_SCREEN  # we answer "missed" right away
	var distance := -origin.z / direction.z  # Then we work out how far forward the line must go to reach z = 0, that is, the plane the screen lies on
	if distance < 0.0:  # If it would have to go backwards to reach it, the screen is behind the camera
		return NOT_ON_SCREEN  # that also counts as a miss
	var hit := origin + direction * distance  # Going this far forward from the start gives the point where the line meets the screen's plane (a position in the screen's view, in metres)
	var screen_size := (_screen.mesh as QuadMesh).size  # How wide and tall the screen quad is (0.18 × 0.108 m), read from its mesh rather than written down a second time
	var uv := Vector2(hit.x / screen_size.x + UV_CENTER, UV_CENTER - hit.y / screen_size.y)  # Convert metres to 0 to 1: x grows to the right; y grows upward in the screen's view, but picture positions grow downward, so y is flipped
	if uv.x < UV_MIN or uv.x > UV_MAX or uv.y < UV_MIN or uv.y > UV_MAX:  # If the result is not between 0 and 1, the line hit the ring around the screen (the frame or empty air)
		return NOT_ON_SCREEN  # we answer "missed"; GDD 5.8 says only a click on the screen counts
	return uv  # Otherwise, we hand the position on the screen back to the brain
