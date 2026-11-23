# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Node3D  # Script on the LandingDust instance in base.tscn (the root of effects/landing_dust.tscn)
## A6 Effect A trigger: listens to one body's landed signal and replays the landing dust at its feet (CHANGE-BRIEF "Effect A").
## The effect lives in the world, not under the player, so the dust stays where it landed while the player walks off.
## Presentation only: it reads the body's position and never writes game state. The effect's settings stay in landing_dust.tscn.

# ============================================================
# Exported variables (@export): wired in base.tscn
# ============================================================
## The body whose landings we show; in base.tscn this is ../Player. Left empty, the effect never plays.
@export var body: Humanoid

# ============================================================
# Node references (@onready): the two emitters in landing_dust.tscn
# ============================================================
@onready var _dust: GPUParticles3D = $Dust  # The dust cloud: 24 specks, 1.6 s
@onready var _ground_ring: GPUParticles3D = $GroundRing  # The ring on the floor: 1 quad, 0.45 s


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot once, when the effect enters the scene. We start listening to the body's landings; nothing plays now.
func _ready() -> void:
	if body == null:  # If no body is wired (for example the preview's own copy), we listen to nothing and stay quiet
		return
	body.landed.connect(_on_body_landed)  # Otherwise, every landing of that body now calls _on_body_landed()


# ============================================================
# Feature functions: called by the signal above
# ============================================================
## Called by the body's landed signal, once on the physics frame it lands. We move to the feet and replay both emitters.
## restart(), not emitting = true (CHANGE-BRIEF retrigger rule): a landing during a live burst clears it and plays again here,
## so at most one burst exists. emitting = true would do nothing to a burst that is still alive.
func _on_body_landed() -> void:
	global_position = body.global_position  # First we stand on the landing point (the body's origin is at its feet); with local_coords off, the new burst is born here
	_dust.restart()  # Then we clear what is left of the old dust and start a new cloud
	_ground_ring.restart()  # And the same for the ring on the floor, so both layers start on the same frame
