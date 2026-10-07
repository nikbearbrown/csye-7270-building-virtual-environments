class_name Waystone
extends Area2D
## The checkpoint (ENV-WAYSTONE). The first time Rudy touches it, it lights,
## once, and the level brings him back to its spawn point after a death. It is
## dark again only if the level starts over from the opening. It lights without
## a sound: the light is the cue (CHANGE-BRIEF.md revision, six sounds).
## Its art is the standing stone with its carved rune, dark, then lit with a
## pale glow (ENV-WAYSTONE-LIT), drawn at half scale from props.json's origin.
## It gets no outline, which would follow the glow. To show that the game is
## saved, a lit waystone also has a halo of the rune's pale blue light behind
## it, gently pulsing, and as it lights, a ring of that light spreads out from
## it once. The halo and the ring are drawn by code. The origin is at the foot
## of the stone.

signal activated(waystone: Waystone)

const DARK := preload("res://content/level_1/art/ENV-WAYSTONE.png")
const LIT := preload("res://content/level_1/art/ENV-WAYSTONE-LIT.png")
const GLOW := Color(0.6, 0.88, 1.0) ## the halo's and the ring's light
const MIDDLE := Vector2(0, -58) ## the middle of the stone
const PULSE_PERIOD := 1.6 ## s
const RING_TIME := 0.7 ## s the ring takes to spread out and fade
const RING_FROM := 50.0 ## px: its radius as it starts...
const RING_TO := 190.0 ## ...and as it fades out

var lit := false

var _clock := 0.0
var _ring_age := -1.0 ## s since the ring started; below 0 when there is none

@onready var spawn_point: Marker2D = $SpawnPoint
@onready var _art: Sprite2D = $Art
@onready var _halo: Sprite2D = $Halo


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	set_process(false)


func _on_body_entered(body: Node2D) -> void:
	if lit or not body is Rudy:
		return
	lit = true
	_art.texture = LIT
	_halo.visible = true
	_ring_age = 0.0
	set_process(true)
	activated.emit(self)


## Dark again, as at the opening; touching it lights it again.
func reset() -> void:
	lit = false
	_art.texture = DARK
	_halo.visible = false
	_ring_age = -1.0
	set_process(false)
	queue_redraw()


func is_ringing() -> bool:
	return _ring_age >= 0.0


func _process(delta: float) -> void:
	_clock += delta
	_halo.modulate.a = 0.8 + 0.2 * sin(_clock * TAU / PULSE_PERIOD)
	if is_ringing():
		_ring_age += delta
		if _ring_age >= RING_TIME:
			_ring_age = -1.0
		queue_redraw()


## The ring of light, behind the halo and the stone.
func _draw() -> void:
	if not is_ringing():
		return
	var t := _ring_age / RING_TIME
	var radius := lerpf(RING_FROM, RING_TO, 1.0 - pow(1.0 - t, 2.0))
	draw_arc(MIDDLE, radius, 0.0, TAU, 96, Color(GLOW, 0.9 * (1.0 - t)), lerpf(10.0, 3.0, t), true)
