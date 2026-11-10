# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name Humanoid  # Global class name: humanoid body
extends CharacterBody3D  # Extends CharacterBody3D: moved by code, handles its own collisions
## Humanoid body: shared by the player and human enemies (code rule 7a).
## Its only job is to "carry out the intent": gravity and jumping, movement, turning, showing the visuals.
## It reads no input and has no camera. A brain (PlayerController, later AI) calls apply_intent() every physics frame.

# ============================================================
# Constants: the three tablet states (design document section 5.8) and the two ends of the tablet move progress
# ============================================================
enum TabletHold {
	NONE,  # Not holding the tablet: the tablet is stowed on the body, switched off
	ONE_HAND,  # One-handed: the character holds the tablet in one hand; an operable tablet slides in at the bottom right of the screen
	TWO_HAND,  # Two-handed: first person, the tablet raised in front of the eyes, the character cannot move
}
const TABLET_MOVE_START := 0.0  # Tablet move progress: just started
const TABLET_MOVE_DONE := 1.0  # Tablet move progress: arrived at the target slot
const INTERACTABLE_GROUP := &"interactables"  # Everything you can press F at (now the wall light switch; later maybe doors and crates) joins this group

# ============================================================
# Signals: announce "what already happened", for presentation and side effects only (rule 3)
# ============================================================
## Emitted after the tablet state changes. Later power-on/off sounds, the slide-in animation and the raise animation listen to it.
signal tablet_hold_changed(old_hold: TabletHold, new_hold: TabletHold)

# ============================================================
# Exported variables (@export): feel parameters shown in the Inspector and tuned there
# ============================================================
## Feel parameters (code rule 1a): tuned in the Inspector, not hard-coded.
@export var walk_speed: float = 3.5  # Walk speed, m/s
@export var sprint_speed: float = 6.0  # Sprint speed, m/s
@export var turn_speed_degrees: float = 720.0  # Turn speed, degrees/s: larger = faster turning
@export var acceleration: float = 42.0  # Horizontal acceleration, m/s²: the most the speed can change per second; larger = snappier starts and stops
@export var jump_velocity: float = 4.5  # Upward speed at take-off, m/s
@export var tablet_move_seconds: float = 0.35  # Seconds for the tablet to move from one slot to another: smaller = faster, 0 = jump there instantly

# ============================================================
# Member variables: state used inside this script (leading underscore = internal to this script)
# ============================================================
var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")  # Gravity from the project settings (default 9.8)
var _facing_yaw := 0.0  # Character facing (radians, around Y). This is "state"; Visual only displays it (rule 5)
var _tablet_hold := TabletHold.NONE  # The current tablet state. Changed only through _apply_tablet_press() (rule 4)
# The next few only describe "where the tablet visual has moved to": presentation, not game state (rule 5)
var _tablet_shown_hold := TabletHold.NONE  # Which state's slot the tablet is moving to (or has reached)
var _tablet_move_from := Transform3D.IDENTITY  # The start of this move: the tablet's position and rotation when the move began
var _tablet_move_progress := TABLET_MOVE_DONE  # How far this move has gone: TABLET_MOVE_START = just started, TABLET_MOVE_DONE = arrived
var _tablet_screen_lit := false #Tracks whether the screen is in the lit state

# ============================================================
# Node references (@onready): child nodes used in the scene
# ============================================================
# @onready: assigned after the node enters the scene tree and its children are ready
@onready var _visual: Node3D = $Visual  # Visual node: the character model and the tablet are under it; rotating it shows the facing
@onready var _human_model: Node3D = $Visual/human_model  # Character model: a capsule and a small orange box for now, a real model later
@onready var _tablet: TabletDevice = $Visual/TabletDevice  # This character's own tablet (every character has one)
@onready var _tablet_hip_slot: Marker3D = $Visual/TabletHipSlot  # Slot: when not held, the tablet hangs on the hip
@onready var _tablet_one_hand_slot: Marker3D = $Visual/TabletOneHandSlot  # Slot: held in one hand
@onready var _tablet_two_hand_slot: Marker3D = $Visual/TabletTwoHandSlot  # Slot: held in both hands, raised in front of the eyes


# ============================================================
# Feature functions: called by a brain, or from inside this script
# ============================================================
## Carries out one intent: gravity and jumping, horizontal movement along the look direction, turning (facing the look direction while aiming), collisions, then updates the visuals.
## Called once per physics frame by the brain (no underscore = a public function for outside callers).
## The body (CharacterBody3D) itself never rotates; the facing is only stored in _facing_yaw.
func apply_intent(intent: CharacterIntent, delta: float) -> void:
	_apply_tablet_press(intent.tablet_press)  # Tablet key first: the turning later in this frame uses the new tablet state
	if intent.interact:  # If the brain says "I want to interact this frame",
		_try_interact()  # we look for something nearby we can interact with and ask it to do its thing (for example, switch the lights)

	# Gravity and jumping: accelerate down when off the floor; on the floor with jump pressed, give an upward speed
	if not is_on_floor():
		velocity.y -= _gravity * delta
	elif intent.jump:
		velocity.y = jump_velocity

	# Horizontal movement: turn "forward/back/left/right" into a world direction along the look direction (Godot's forward is -Z)
	var wish := Vector3(intent.move.x, 0.0, -intent.move.y).rotated(Vector3.UP, intent.look_yaw)
	# Target speed = direction × walk or sprint speed; a half-pushed stick gives half the speed
	var target := wish.normalized() * (sprint_speed if intent.sprint else walk_speed) * minf(wish.length(), 1.0)
	# The current horizontal speed approaches the target gradually (not instantly), so starts and stops have a short transition
	var horizontal := Vector3(velocity.x, 0.0, velocity.z).move_toward(target, acceleration * delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.z
	if intent.aim or _tablet_hold == TabletHold.TWO_HAND:
		# While aiming: the body faces the look direction at once, and WASD becomes strafing and backing up
		# While holding the tablet in both hands: the body also faces the look direction, so the tablet in front of it sits right in front of the camera
		_facing_yaw = intent.look_yaw
	else:
		_update_facing(wish, delta)  # Normally: with movement input, the facing turns gradually toward the move direction
	move_and_slide()  # Built into CharacterBody3D: moves by velocity, slides along walls, stops on landing
	_update_visual(delta)  # Finally, show the new state on the visuals


## Turns the character facing (_facing_yaw) smoothly toward direction at turn_speed_degrees.
## When direction is zero (no movement input) it does nothing, and the character keeps its facing.
func _update_facing(direction: Vector3, delta: float) -> void:
	if direction.is_zero_approx():
		return
	# A node turned θ around Y faces (-sin θ, 0, -cos θ); solve back for θ
	var target_yaw := atan2(-direction.x, -direction.z)
	# rotate_toward: turns at most one step each time and automatically takes the shorter way (never the long way round)
	_facing_yaw = rotate_toward(_facing_yaw, target_yaw, deg_to_rad(turn_speed_degrees) * delta)


## Shows the state on the visuals: the facing and the tablet's position. A character model and animations will read the state here too.
## Called once at the end of apply_intent() every physics frame.
func _update_visual(delta: float) -> void:
	_visual.rotation.y = _facing_yaw
	_update_tablet_visual(delta)


## Moves the tablet smoothly, over tablet_move_seconds, from where it was to the slot for the current tablet state (the raise / lower animation).
## When the tablet state changes, the move restarts from where the tablet is "right now", so pressing Tab mid-move does not jump.
## Reads _tablet_hold only and never changes it: presentation does not write state (rule 5). Called by _update_visual() every physics frame.
func _update_tablet_visual(delta: float) -> void:
	# State changed: remember where the tablet is now as the start, and restart the progress
	if _tablet_shown_hold != _tablet_hold:
		_tablet_shown_hold = _tablet_hold
		_tablet_move_from = _tablet.transform
		_tablet_move_progress = TABLET_MOVE_START
	# Advance the progress toward "arrived": 1 / tablet_move_seconds per second, so it finishes in exactly tablet_move_seconds, independent of frame rate
	if tablet_move_seconds <= 0.0:
		_tablet_move_progress = TABLET_MOVE_DONE  # Set to 0 seconds: arrive at once
	else:
		_tablet_move_progress = move_toward(_tablet_move_progress, TABLET_MOVE_DONE, delta / tablet_move_seconds)
	# smoothstep: turns the even progress into "slow start, fast middle, slow stop", so it looks like a hand moving, not a machine
	var eased := smoothstep(TABLET_MOVE_START, TABLET_MOVE_DONE, _tablet_move_progress)
	var target := _get_tablet_slot(_tablet_shown_hold).transform
	# The tablet and the slots are all children of Visual, the same frame of reference, so interpolate directly between the two transforms (position and rotation together)
	_tablet.transform = _tablet_move_from.interpolate_with(target, eased)
	_update_tablet_screen()

##Checks the current state (not held, one hand, two hands) and sends it to the tablet, so the tablet lights up or not
##Called once every physics frame by _update_tablet_visual().
##Reads _tablet_hold only, never changes it (rule 5)
func _update_tablet_screen() -> void:
	if _tablet_hold == TabletHold.NONE:
		_tablet_screen_lit = false
	elif _tablet_move_progress == TABLET_MOVE_DONE:
		_tablet_screen_lit = true
	_tablet.set_screen_lit(_tablet_screen_lit)



## Lookup: tablet state → which slot the tablet belongs in. Calculation only, changes nothing. Called by _update_tablet_visual().
func _get_tablet_slot(hold: TabletHold) -> Marker3D:
	match hold:
		TabletHold.ONE_HAND:
			return _tablet_one_hand_slot
		TabletHold.TWO_HAND:
			return _tablet_two_hand_slot
		_:  # The remaining case: NONE (not holding the tablet)
			return _tablet_hip_slot


## apply_intent() calls this when the intent's interact is true: find something nearby to interact with and ask it to do its thing.
## Whether interaction is allowed is answered by that thing's own can_interact() (a query point, rule 3); what happens is decided by its own interact().
## If several are nearby at once, we interact only with the nearest one, so one press of F does exactly one thing.
func _try_interact() -> void:
	var nearest: Node3D = null  # First, we have not found anything to interact with yet
	var nearest_distance := INF  # The nearest distance starts at infinity, so the first one we find is always nearer
	for target in get_tree().get_nodes_in_group(INTERACTABLE_GROUP):  # We look at everything in the interactable group,
		if not target.can_interact(self):  # and if it says "you are too far away to interact with me",
			continue  # we skip it and look at the next one
		var distance := global_position.distance_to(target.global_position)  # Otherwise, we work out how far it is from the body
		if distance < nearest_distance:  # If it is nearer than everything found so far,
			nearest = target  # we remember it as "the nearest one"
			nearest_distance = distance  # and remember its distance, for the next ones to compare against
	if nearest != null:  # Finally, if we found one,
		nearest.interact(self)  # we ask it to do its thing; the switch receives this request and then switches the lights


## Shows or hides this body's character model (only human_model is hidden, not the tablet, so the tablet in hand stays visible in first person).
## Only affects the picture on the machine that calls it; not game state (rule 5).
## Called by the player brain when switching to first person; in co-op, teammates' machines don't call it, so they still see you.
func set_visual_visible(visible_locally: bool) -> void:
	_human_model.visible = visible_locally


## Returns the current tablet state. The brain uses it to decide which inputs may go into the intent this frame.
func get_tablet_hold() -> TabletHold:
	return _tablet_hold


## Switches the tablet state by this frame's tablet key result, and emits tablet_hold_changed when the state changed.
## Called by apply_intent() every physics frame; does nothing when press is NONE.
func _apply_tablet_press(press: CharacterIntent.TabletPress) -> void:
	if press == CharacterIntent.TabletPress.NONE:
		return
	var old_hold := _tablet_hold
	_tablet_hold = _next_tablet_hold(old_hold, press)
	tablet_hold_changed.emit(old_hold, _tablet_hold)


## Looks up the switching table (design document section 5.8): current state + short or long press → new state. Calculation only, changes nothing.
func _next_tablet_hold(current: TabletHold, press: CharacterIntent.TabletPress) -> TabletHold:
	var is_long := press == CharacterIntent.TabletPress.LONG
	match current:  # match is the switch of other languages
		TabletHold.NONE:
			return TabletHold.TWO_HAND if is_long else TabletHold.ONE_HAND
		TabletHold.ONE_HAND:
			return TabletHold.TWO_HAND if is_long else TabletHold.NONE
		_:  # The remaining case: TWO_HAND (_ is switch's default)
			return TabletHold.NONE if is_long else TabletHold.ONE_HAND

