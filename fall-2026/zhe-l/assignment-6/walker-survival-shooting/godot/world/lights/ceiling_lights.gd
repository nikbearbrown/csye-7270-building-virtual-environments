# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name CeilingLights  # Global class name: the keeper of the base's ceiling lights
extends Node  # Extends Node: it only holds state and needs no position
## Keeper of the base's ceiling lights: remembers "are the lights on or off" and makes every light in the ceiling_lights group follow it.
## The light state changes only through set_lights_on() / toggle() (code rule 4).
## After a change it emits lights_changed; the ambient dust effect will only listen to this signal and never decides the light state (rule 5).

# ============================================================
# Constants: the name of the ceiling-light group
# ============================================================
const LIGHT_GROUP := &"ceiling_lights"  # Every ceiling light in base.tscn joins this group; a new ceiling light only needs to join it too

# ============================================================
# Signals: announce "what has already happened", for presentation and side effects only (rule 3)
# ============================================================
## Emitted after the light state has really changed. The ambient dust effect will listen to it to start or stop.
signal lights_changed(lights_on: bool)

# ============================================================
# Exported variables (@export): values shown in the Inspector that can be tuned directly
# ============================================================
@export var start_on: bool = true  # Whether the lights are on when the scene loads; we decided they are on

# ============================================================
# Member variables: the state this node remembers
# ============================================================
var _lights_on: bool = true  # Whether the lights are on now; this is the only place in the whole game that remembers it

# ============================================================
# Engine callbacks: called automatically by Godot at certain times
# ============================================================
## Godot calls this once after this node and its children have entered the scene tree.
## Here we set the lights up the way they start.
func _ready() -> void:
	_lights_on = start_on  # First, we set the light state to the starting state
	_apply_to_lights()  # Then we make every ceiling light turn on or off to match it

# ============================================================
# Functions
# ============================================================
## The wall switch calls this through toggle() to set the lights on or off.
## This is the only way in to change the light state.
func set_lights_on(on: bool) -> void:
	if on == _lights_on:  # If the state asked for is the same as now,
		return  # we do nothing and emit nothing, so the dust is not triggered twice
	_lights_on = on  # Otherwise, we change the light state to the new state
	_apply_to_lights()  # we make every ceiling light turn on or off to match the new state
	lights_changed.emit(_lights_on)  # Finally we announce "the light state changed"; the dust will start or stop when it hears this

## Called when the wall switch is pressed: lights on become off, lights off become on.
func toggle() -> void:
	set_lights_on(not _lights_on)  # We hand "the opposite of now" to the only way in

## Called once by the dust effect when it has just loaded and has not received any signal yet, to ask "are the lights on now?".
func is_lights_on() -> bool:
	return _lights_on  # We tell the caller the current light state; read only, nothing changes

## _ready() and set_lights_on() call this to make every ceiling light match the state.
func _apply_to_lights() -> void:
	for light in get_tree().get_nodes_in_group(LIGHT_GROUP):  # We find every ceiling light in the group,
		(light as Light3D).visible = _lights_on  # and show it (it lights) when the lights are on, hide it (no light) when they are off
