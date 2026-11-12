# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends GPUParticles3D  # Script on the LightDust instance in base.tscn (the root of effects/light_dust.tscn is the emitter itself)
## A6 Effect B listener: shows the dust under ceiling light 1 while the ceiling lights are on, and hides it while they are off (CHANGE-BRIEF "Effect B").
## It asks CeilingLights once at start (the keeper does not emit in its _ready()), then follows lights_changed.
## Every start is restart(), not emitting = true, so the old progress is thrown away and preprocess fills the box again:
## on lights on, and when the node is shown again while the lights are on. Each of those runs restart() exactly once.
## Presentation only: it reads the light state and never writes it. The effect's settings stay in light_dust.tscn.

# ============================================================
# Exported variables (@export): wired in base.tscn
# ============================================================
## The keeper of the light state; in base.tscn this is ../CeilingLights. Left empty, the dust stays as the scene file has it (not emitting).
@export var ceiling_lights: CeilingLights

# ============================================================
# Member variables: what this listener remembers
# ============================================================
## How many times we have restarted the dust. Only for observation (the state test reads it to check one restart per lights-on); nothing reads it to decide anything.
var restart_count := 0


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot once, when the effect enters the scene. We wait for the keeper to be ready, ask it once, and start listening.
func _ready() -> void:
	if ceiling_lights == null:  # If no keeper is wired (for example a copy of the effect on its own), we listen to nothing and stay quiet
		return
	if not ceiling_lights.is_node_ready():  # If the keeper has not run its _ready() yet, its state is still the field default, not start_on
		await ceiling_lights.ready  # So we wait until it has set its start state
	visibility_changed.connect(_on_visibility_changed)  # From now on, being hidden or shown by anyone reaches us
	ceiling_lights.lights_changed.connect(_on_lights_changed)  # And every real change of the light state reaches us
	_on_lights_changed(ceiling_lights.is_lights_on())  # The keeper does not emit at start, so we ask once (on, in the game) and follow it


# ============================================================
# Feature functions: called by the signals above
# ============================================================
## Called by CeilingLights.lights_changed, and once by _ready() with the queried state.
## Lights on: shown and restarted once. Lights off: invisible at once and no new births, so no glowing specks are left after the light.
func _on_lights_changed(lights_on: bool) -> void:
	if lights_on:  # If the lights are on, the dust under them shows
		if visible:  # If we are already shown (scene load), showing again would not fire visibility_changed, so we restart here ourselves
			_restart()
		else:  # Otherwise we only show; visibility_changed then calls _on_visibility_changed(), which restarts once, so restart() does not run twice
			visible = true
	else:  # Otherwise the dust goes away with the light
		visible = false  # Hidden from this frame on; visibility_changed also stops births
		emitting = false  # And we stop births here too, in case we were already hidden and no visibility_changed came


## Called by visibility_changed: when we (or a parent) are hidden or shown, by the lights handler above or by any other code.
## Hidden: stop births; the next show throws the old progress away. Shown while the lights are on: restart once, so preprocess fills the box again.
func _on_visibility_changed() -> void:
	if not is_visible_in_tree():  # If we can no longer be seen, we stop making new specks
		emitting = false
	elif ceiling_lights.is_lights_on():  # Otherwise, if we are shown again and the lights are on, we start from scratch
		_restart()


## Called by the two handlers above, the only place that restarts the dust. Counts each restart for the state test.
func _restart() -> void:
	restart_count += 1  # One more start; the state test checks this goes up by exactly one per lights-on and per show
	restart()  # Clear the old specks, turn emitting on, and run preprocess (whether restart() re-runs preprocess in 4.7.2 is a brief "Unconfirmed" item)
