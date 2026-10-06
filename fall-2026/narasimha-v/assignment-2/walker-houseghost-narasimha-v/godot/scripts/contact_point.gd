extends Area2D
## The music box. The core verb: reach across and be noticed.
##
## Two kinds of contact, from CHANGE-BRIEF: a kind contact (tap) is slow and
## safe, a scary contact (hold) is faster recognition but costs more days.
## Both only work from the remembered side, because that is where the boy can
## still touch things.
##
## Double-trigger prevention: the contact is armed on the input EDGE
## (just_pressed), resolved once, and then locked out for COOLDOWN seconds, so
## a held key or a mashed key cannot emit contact_landed more than once.

signal contact_landed(kind: String, days_cost: int)

const HOLD_FOR_SCARY := 0.45
const COOLDOWN := 1.2

@export var days_cost_kind := 1
@export var days_cost_scary := 2
@export var recognition_kind := 1
@export var recognition_scary := 2

var _player_inside := false
var _world_inverted := false
var _held_for := 0.0
var _arming := false
var _locked_until := 0.0

@onready var _glow: Sprite2D = $Glow


func _ready() -> void:
	body_entered.connect(func(_b): _player_inside = true)
	body_exited.connect(func(_b): _player_inside = false)


func set_inverted(is_inverted: bool) -> void:
	_world_inverted = is_inverted
	if not is_inverted:
		_arming = false
		_held_for = 0.0
	_update_glow()


func _process(delta: float) -> void:
	_update_glow()
	if _locked_until > 0.0:
		_locked_until = maxf(0.0, _locked_until - delta)
		return
	if not _available():
		return

	if Input.is_action_just_pressed("contact"):
		_arming = true
		_held_for = 0.0
	elif _arming and Input.is_action_pressed("contact"):
		_held_for += delta
	elif _arming and Input.is_action_just_released("contact"):
		_resolve(_held_for >= HOLD_FOR_SCARY)


func _available() -> bool:
	return _player_inside and _world_inverted


## Changes state first, then announces it. Audio listens to the signal, so a
## muted or missing sound can never change what the contact did.
##
## The cooldown is enforced here rather than only at the call site, so a second
## resolve inside the window is refused no matter who asks. An automated check
## caught this: the guard used to live in _process alone, which left the
## function itself able to fire twice.
func _resolve(scary: bool) -> void:
	if _locked_until > 0.0:
		return
	_arming = false
	_held_for = 0.0
	_locked_until = COOLDOWN
	if scary:
		contact_landed.emit("scary", days_cost_scary)
	else:
		contact_landed.emit("kind", days_cost_kind)


func _update_glow() -> void:
	var ready_now := _available() and _locked_until <= 0.0
	_glow.visible = ready_now
	if ready_now:
		var pulse := 0.55 + 0.45 * sin(Time.get_ticks_msec() / 260.0)
		_glow.modulate.a = pulse
		if _arming:
			# Winding up toward the scary contact: the glow hardens as it charges.
			var charge := clampf(_held_for / HOLD_FOR_SCARY, 0.0, 1.0)
			_glow.modulate = Color(1.0, 1.0 - 0.5 * charge, 1.0 - 0.7 * charge, 1.0)
		else:
			_glow.modulate = Color(1, 1, 1, pulse)
