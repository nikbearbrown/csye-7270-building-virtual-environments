class_name Humanoid
extends CharacterBody3D

enum TabletHold {
	NONE,
	ONE_HAND,
	TWO_HAND,
}
const STATE_RAISE_ONE_HAND := &"raise_1h"
const STATE_HOLD_ONE_HAND := &"hold_1h"
const STATE_RAISE_TWO_HAND := &"raise_2h"
const STATE_HOLD_TWO_HAND := &"hold_2h"
const RAISE_TWO_HAND_SEEK := &"parameters/raise_2h/seek/seek_request"
const FROM_ONE_HAND_START := 16.0 / 30.0
const INTERACTABLE_GROUP := &"interactables"

signal tablet_hold_changed(old_hold: TabletHold, new_hold: TabletHold)
signal landed

@export var walk_speed: float = 3.5
@export var sprint_speed: float = 6.0
@export var turn_speed_degrees: float = 720.0
@export var acceleration: float = 42.0
@export var jump_velocity: float = 4.5

var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var _facing_yaw := 0.0
var _tablet_hold := TabletHold.NONE
var _tablet_screen_lit := false
var _raising_tablet := false
var _was_on_floor := true
var _has_touched_floor := false

@onready var _visual: Node3D = $Visual
@onready var _human_model: Node3D = $Visual/human_model
@onready var _tablet: TabletDevice = $Visual/human_model/main_character/rig/Skeleton3D/TabletBone/TabletMount/TabletDevice
@onready var _first_person_head: SkeletonModifier3D = $Visual/human_model/main_character/rig/Skeleton3D/FirstPersonHead
@onready var _animation_tree: AnimationTree = $AnimationTree
@onready var _tablet_states: AnimationNodeStateMachinePlayback = _animation_tree.get("parameters/playback")


func apply_intent(intent: CharacterIntent, delta: float) -> void:
	_apply_tablet_press(intent.tablet_press)
	if intent.interact:
		_try_interact()

	if not is_on_floor():
		velocity.y -= _gravity * delta
	elif intent.jump:
		velocity.y = jump_velocity

	var wish := Vector3(intent.move.x, 0.0, -intent.move.y).rotated(Vector3.UP, intent.look_yaw)
	var target := wish.normalized() * (sprint_speed if intent.sprint else walk_speed) * minf(wish.length(), 1.0)
	var horizontal := Vector3(velocity.x, 0.0, velocity.z).move_toward(target, acceleration * delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.z
	if intent.aim or _tablet_hold == TabletHold.TWO_HAND:
		_facing_yaw = intent.look_yaw
	else:
		_update_facing(wish, delta)
	move_and_slide()
	_notify_landing()
	_update_visual(delta)


func _notify_landing() -> void:
	var on_floor := is_on_floor()
	if _has_touched_floor and on_floor and not _was_on_floor:
		landed.emit()
	_was_on_floor = on_floor
	_has_touched_floor = _has_touched_floor or on_floor


func _update_facing(direction: Vector3, delta: float) -> void:
	if direction.is_zero_approx():
		return
	var target_yaw := atan2(-direction.x, -direction.z)
	_facing_yaw = rotate_toward(_facing_yaw, target_yaw, deg_to_rad(turn_speed_degrees) * delta)


func _update_visual(_delta: float) -> void:
	_visual.rotation.y = _facing_yaw
	_update_tablet_screen()


func _update_tablet_screen() -> void:
	var state := _tablet_states.get_current_node()
	var blending := _tablet_states.get_fading_from_node() != &""
	if _raising_tablet and state == STATE_HOLD_ONE_HAND:
		_raising_tablet = false
	if _tablet_hold == TabletHold.NONE:
		_tablet_screen_lit = false
	else:
		var target := STATE_HOLD_ONE_HAND if _tablet_hold == TabletHold.ONE_HAND else STATE_HOLD_TWO_HAND
		_tablet_screen_lit = state == target and not blending
	_tablet.set_screen_lit(_tablet_screen_lit)


func _try_interact() -> void:
	var nearest: Node3D = null
	var nearest_distance := INF
	for target in get_tree().get_nodes_in_group(INTERACTABLE_GROUP):
		if not target.can_interact(self):
			continue
		var distance := global_position.distance_to(target.global_position)
		if distance < nearest_distance:
			nearest = target
			nearest_distance = distance
	if nearest != null:
		nearest.interact(self)


func set_visual_visible(visible_locally: bool) -> void:
	_first_person_head.active = not visible_locally


func get_tablet_hold() -> TabletHold:
	return _tablet_hold


func is_raising_tablet() -> bool:
	return _raising_tablet


func is_tablet_screen_lit() -> bool:
	return _tablet_screen_lit


func get_tablet() -> TabletDevice:
	return _tablet


func _apply_tablet_press(press: CharacterIntent.TabletPress) -> void:
	if press == CharacterIntent.TabletPress.NONE:
		return
	var old_hold := _tablet_hold
	_tablet_hold = _next_tablet_hold(old_hold, press)
	_raising_tablet = old_hold == TabletHold.NONE and _tablet_hold == TabletHold.ONE_HAND
	if _raising_tablet:
		_tablet_states.start(STATE_RAISE_ONE_HAND, true)
	if _tablet_hold == TabletHold.TWO_HAND and old_hold != TabletHold.TWO_HAND:
		_animation_tree.set(RAISE_TWO_HAND_SEEK, _two_hand_start_time(old_hold))
	tablet_hold_changed.emit(old_hold, _tablet_hold)


func _next_tablet_hold(current: TabletHold, press: CharacterIntent.TabletPress) -> TabletHold:
	var is_long := press == CharacterIntent.TabletPress.LONG
	match current:
		TabletHold.NONE:
			return TabletHold.TWO_HAND if is_long else TabletHold.ONE_HAND
		TabletHold.ONE_HAND:
			return TabletHold.TWO_HAND if is_long else TabletHold.NONE
		_:
			return TabletHold.NONE if is_long else TabletHold.ONE_HAND


func _two_hand_start_time(old_hold: TabletHold) -> float:
	if old_hold == TabletHold.NONE:
		return 0.0
	if _tablet_states.get_current_node() == STATE_RAISE_ONE_HAND:
		return minf(_tablet_states.get_current_play_position(), FROM_ONE_HAND_START)
	return FROM_ONE_HAND_START
