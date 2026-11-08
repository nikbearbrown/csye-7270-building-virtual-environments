class_name EffectsDriver
extends Node2D
## Starts the presentation effects from the game's state (CHANGE-BRIEF.md).
## It only reads game state, and it only places, mirrors, starts and frees the
## effects: their settings live in their scene files.
##
## Effect A, the sword-swing sparks: each tick that Rudy's sword hitbox goes
## from disabled to live, a new SlashSparks burst starts at the hitbox, facing
## his way. Every cut gets its own burst, so a fast second cut leaves the first
## one running (rule A3), and each burst frees itself once its sparks finish.
## It sits after Rudy in Main, so it sees the edge on the tick _swing() makes it.
##
## Effect B, the running dust trail: RunDust sits in DustTrail, before Rudy in
## Main so it draws behind him, and this driver keeps it at his soles every tick.
## It emits while he runs on the ground under control and the emitter is visible
## in the tree (rules B1, B2, B4). While the tree is paused this driver does not
## run, so emitting keeps its value (B3).

const SLASH_SPARKS := preload("res://effects/slash_sparks.tscn")
const RUN_DUST_OFFSET := Vector2(0, -4)

var _box_was_disabled: bool

@onready var _rudy: Rudy = get_node("../Rudy")
@onready var _sword_box: CollisionShape2D = _rudy.get_node("SwordHitbox/Shape")
@onready var _slash_bursts: Node2D = $SlashBursts
@onready var _run_dust: GPUParticles2D = get_node("../DustTrail/RunDust")


func _ready() -> void:
	_box_was_disabled = _sword_box.disabled # so a load never fires a burst


func _physics_process(_delta: float) -> void:
	var disabled := _sword_box.disabled
	if _box_was_disabled and not disabled:
		_fire_slash_sparks()
	_box_was_disabled = disabled
	_drive_run_dust()


func _fire_slash_sparks() -> void:
	var burst: Node2D = SLASH_SPARKS.instantiate() # a new burst per cut: overlap (A3)
	_slash_bursts.add_child(burst)
	burst.global_position = _sword_box.global_position
	burst.scale.x = _rudy.facing
	(burst.get_node("Sparks") as GPUParticles2D).finished.connect(burst.queue_free)
	for emitter: GPUParticles2D in burst.get_children():
		emitter.emitting = true


func _drive_run_dust() -> void:
	# It follows him even when idle, so a respawn's jump lays down nothing (B5).
	_run_dust.global_position = _rudy.global_position + RUN_DUST_OFFSET
	var running := _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() \
			and absf(_rudy.velocity.x) > 1.0
	var want := running and _run_dust.is_visible_in_tree() # hidden: no unseen puffs (B4)
	if _run_dust.emitting != want:
		_run_dust.emitting = want
