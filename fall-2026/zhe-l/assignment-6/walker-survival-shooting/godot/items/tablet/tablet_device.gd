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
