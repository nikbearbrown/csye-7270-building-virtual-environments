# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name LightSwitch  # Global class name: the light switch on the wall
extends Node3D  # Extends Node3D: it hangs on the wall and has a position
## The light switch on the wall: when a character walks up to it and presses F, it asks CeilingLights to turn the ceiling lights on or off.
## It does not remember the light state itself; that lives only in CeilingLights (rule 4).
## It joins the interactables group; when the body presses F it asks can_interact(), then calls interact().

# ============================================================
# Exported variables (@export): nodes connected in the Inspector
# ============================================================
@export var ceiling_lights: CeilingLights  # The ceiling lights this switch controls; drag CeilingLights in here in the Inspector of base.tscn

# ============================================================
# Node references (@onready): child nodes used in the scene
# ============================================================
@onready var _interact_area: Area3D = $InteractArea  # A space in front of the switch: a character's body can press the switch only inside it

# ============================================================
# Engine callbacks: called automatically by Godot at certain times
# ============================================================
## Godot calls this once after the switch has entered the scene tree.
## Here we register the switch as "something you can interact with", so the body can find it when it presses F.
func _ready() -> void:
	add_to_group(Humanoid.INTERACTABLE_GROUP)  # Join the group the body uses to find things to interact with

# ============================================================
# Functions
# ============================================================
## The body calls this when F is pressed, to ask the switch "may I interact with you?" (a query point, rule 3).
## It only answers and changes nothing.
func can_interact(actor: Node3D) -> bool:
	if ceiling_lights == null:  # If the switch is not connected to the ceiling lights,
		return false  # we say no, because pressing it would do nothing
	return _interact_area.overlaps_body(actor)  # Otherwise, only a character whose body is in the space in front of the switch can interact

## The body calls this after it has confirmed it may interact and that this switch is the nearest one.
## The switch does not change the lights itself; it hands the request to CeilingLights, which decides how the lights change.
func interact(_actor: Node3D) -> void:
	ceiling_lights.toggle()  # We ask the keeper of the ceiling lights to flip them: on becomes off, off becomes on
