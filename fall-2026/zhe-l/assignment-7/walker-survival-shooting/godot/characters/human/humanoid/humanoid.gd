# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name Humanoid  # Global class name: humanoid body
extends CharacterBody3D  # Extends CharacterBody3D: moved by code, handles its own collisions
## Humanoid body: shared by the player and human enemies (code rule 7a).
## Its only job is to "carry out the intent": gravity and jumping, movement, turning, showing the visuals.
## It reads no input and has no camera. A brain (PlayerController, later AI) calls apply_intent() every physics frame.

# ============================================================
# Constants: the three tablet states (design document section 5.8) and the animation states that show them
# ============================================================
enum TabletHold {
	NONE,  # Not holding the tablet: the tablet is put away on the body, switched off
	ONE_HAND,  # Holding the tablet one-handed: the character holds the tablet in one hand; an operable tablet slides in at the bottom right of the screen
	TWO_HAND,  # Holding the tablet two-handed: first person, the tablet raised in front of the eyes, the character cannot move
}
const STATE_HOLD_ONE_HAND := &"hold_1h"  # Animation state (AnimationTree): the one-handed hold pose (CHANGE-BRIEF, state machine)
const STATE_HOLD_TWO_HAND := &"hold_2h"  # Animation state: the two-handed hold pose
const INTERACTABLE_GROUP := &"interactables"  # Everything you can press F at (now the wall light switch; later maybe doors and crates) joins this group

# ============================================================
# Signals: announce "what already happened", for presentation and side effects only (rule 3)
# ============================================================
## Emitted after the tablet state changes. The brain listens to it; the animation state machine reads get_tablet_hold() on its own.
signal tablet_hold_changed(old_hold: TabletHold, new_hold: TabletHold)
## Emitted once on the physics frame the body comes back to the floor from the air (is_on_floor() goes false -> true). Notify-only: it changes nothing.
## The landing dust (effects/landing_dust_trigger.gd) listens to it and replays the dust at the feet.
signal landed

# ============================================================
# Exported variables (@export): feel parameters shown in the Inspector and tuned there
# ============================================================
## Feel parameters (code rule 1a): tuned in the Inspector, not hard-coded.
@export var walk_speed: float = 3.5  # Walk speed, m/s
@export var sprint_speed: float = 6.0  # Sprint speed, m/s
@export var turn_speed_degrees: float = 720.0  # Turn speed, degrees/s: larger = faster turning
@export var acceleration: float = 42.0  # Horizontal acceleration, m/s^2: the most the speed can change per second; larger = snappier starts and stops
@export var jump_velocity: float = 4.5  # Upward speed at take-off, m/s

# ============================================================
# Member variables: state used inside this script (leading underscore = internal to this script)
# ============================================================
var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")  # Gravity from the project settings (default 9.8)
var _facing_yaw := 0.0  # Character facing (radians, around Y). This is "state"; Visual only displays it (rule 5)
var _tablet_hold := TabletHold.NONE  # The current tablet state. Changed only through _apply_tablet_press() (rule 4)
var _tablet_screen_lit := false  # Whether the screen is lit (and clickable); worked out every physics frame by _update_tablet_screen() from the animation state
var _raising_tablet := false  # Whether the one-handed raise is under way: set when a short press takes the tablet out, cleared when the raise has finished; the brain asks is_raising_tablet()
# Last physics frame's floor state, only for the landed notification. It starts true: a body placed on the floor has not "landed" on scene load
var _was_on_floor := true
# Whether the body has stood on the floor at least once, only for the landed notification. Until then nothing counts as "coming back":
# on scene load the first move can leave the body just inside the floor (not on it) for one frame before it is pushed out onto it
var _has_touched_floor := false

# ============================================================
# Node references (@onready): child nodes used in the scene
# ============================================================
# @onready: assigned after the node enters the scene tree and its children are ready
@onready var _visual: Node3D = $Visual  # Visual node: the character model and the tablet are under it; rotating it shows the facing
@onready var _human_model: Node3D = $Visual/human_model  # Character model: the main character imported from main_character.glb
@onready var _tablet: TabletDevice = $Visual/human_model/main_character/rig/Skeleton3D/TabletBone/TabletMount/TabletDevice  # This character's own tablet; it hangs on the rig's "tablet" bone, so only the animation decides where it is
@onready var _animation_tree: AnimationTree = $AnimationTree  # The one authority over the skeleton (and so over the tablet): its state machine follows _tablet_hold
@onready var _tablet_states: AnimationNodeStateMachinePlayback = _animation_tree.get("parameters/playback")  # The state machine's playback: which animation state it is in, and whether a blend is still running


# ============================================================
# Functions: called by a brain, or from inside this script
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
	# Target speed = direction x walk or sprint speed; a half-pushed stick gives half the speed
	var target := wish.normalized() * (sprint_speed if intent.sprint else walk_speed) * minf(wish.length(), 1.0)
	# The current horizontal speed approaches the target gradually (not instantly), so starts and stops have a short transition
	var horizontal := Vector3(velocity.x, 0.0, velocity.z).move_toward(target, acceleration * delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.z
	if intent.aim or _tablet_hold == TabletHold.TWO_HAND:
		# While aiming: the body faces the look direction at once, and WASD becomes strafing and backing up
		# While holding the tablet two-handed: the body also faces the look direction, so the tablet in front of it sits right in front of the camera
		_facing_yaw = intent.look_yaw
	else:
		_update_facing(wish, delta)  # Normally: with movement input, the facing turns gradually toward the move direction
	move_and_slide()  # Built into CharacterBody3D: moves by velocity, slides along walls, stops on landing
	_notify_landing()  # Now that the move has updated is_on_floor(), we tell the listeners if this frame is a landing
	_update_visual(delta)  # Finally, show the new state on the visuals


## apply_intent() calls this right after move_and_slide(), once per physics frame. If the body was in the air last frame and is on the floor now, we emit landed once.
## Notify-only: it only reads the floor state, and changes neither the movement nor any state.
func _notify_landing() -> void:
	var on_floor := is_on_floor()  # First we read where the move just left us: on the floor or in the air
	# If we have stood on the floor before, are on it now, and were in the air last frame, we have come back to the floor: this frame is the landing
	if _has_touched_floor and on_floor and not _was_on_floor:
		landed.emit()  # So we announce it once; the landing dust hears it and plays at the feet
	_was_on_floor = on_floor  # Then we remember this frame's state, so next frame standing still does not count as landing again
	_has_touched_floor = _has_touched_floor or on_floor  # Once we have stood on the floor, later landings count; the first touch on load does not


## Turns the character facing (_facing_yaw) smoothly toward direction at turn_speed_degrees.
## When direction is zero (no movement input) it does nothing, and the character keeps its facing.
func _update_facing(direction: Vector3, delta: float) -> void:
	if direction.is_zero_approx():
		return
	# A node turned theta around Y faces (-sin theta, 0, -cos theta); solve back for theta
	var target_yaw := atan2(-direction.x, -direction.z)
	# rotate_toward: turns at most one step each time and automatically takes the shorter way (never the long way round)
	_facing_yaw = rotate_toward(_facing_yaw, target_yaw, deg_to_rad(turn_speed_degrees) * delta)


## Shows the state on the visuals: the facing, and the tablet screen. Where the tablet is comes from the AnimationTree, not from here.
## Called once at the end of apply_intent() every physics frame.
func _update_visual(_delta: float) -> void:
	_visual.rotation.y = _facing_yaw  # We turn the model to the stored facing
	_update_tablet_screen()  # Then we work out whether the screen may be lit this frame


## Works out, every physics frame, whether the tablet screen is lit (and clickable), hands that to the tablet, and notices when the raise has finished.
## The rule (CHANGE-BRIEF, "light once in place"): put away = dark at once; otherwise lit only when the animation state machine is in the hold pose
## that matches the tablet state and no blend is running. So the one-handed raise lights on its last frame (frame 20), and every 0.2 s cross-fade is dark.
## It reads the animation state; it never writes it, and it never moves the tablet. Called by _update_visual() every physics frame.
func _update_tablet_screen() -> void:
	var state := _tablet_states.get_current_node()  # First we ask the state machine which animation state it is in now
	var blending := _tablet_states.get_fading_from_node() != &""  # and whether it is still blending away from an earlier state
	if _raising_tablet and state == STATE_HOLD_ONE_HAND:  # If we were raising and the machine has reached the one-handed hold pose (the raise clip has finished),
		_raising_tablet = false  # from this frame the brain lets the player walk again
	if _tablet_hold == TabletHold.NONE:  # If the tablet is put away,
		_tablet_screen_lit = false  # the screen is dark from this very frame
	else:  # Otherwise it is lit only once the matching hold pose is reached with no blend running
		var target := STATE_HOLD_ONE_HAND if _tablet_hold == TabletHold.ONE_HAND else STATE_HOLD_TWO_HAND
		_tablet_screen_lit = state == target and not blending
	_tablet.set_screen_lit(_tablet_screen_lit)  # Finally we hand lit or dark to the tablet, which sets its screen material's brightness


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


## Shows or hides this body's character model. Only the model's meshes are hidden, not the skeleton: the tablet hangs on a bone inside the model,
## so hiding the skeleton would hide the tablet too, and in first person the tablet in hand must stay visible (CHANGE-BRIEF revision 2026-11-22).
## Only affects the picture on the machine that calls it; not game state (rule 5).
## Called by the player brain when switching to first person; in co-op, teammates' machines don't call it, so they still see you.
func set_visual_visible(visible_locally: bool) -> void:
	for mesh in _human_model.find_children("*", "MeshInstance3D", true, false):  # We go through every mesh of the character model,
		if not _tablet.is_ancestor_of(mesh):  # skipping the tablet's own meshes,
			mesh.visible = visible_locally  # and show or hide it


## Returns the current tablet state. The brain uses it to decide which inputs may go into the intent this frame; the animation state machine reads it in its transition expressions.
func get_tablet_hold() -> TabletHold:
	return _tablet_hold


## Query point (rule 3): is the one-handed raise still under way? From the short press that takes the tablet out until the raise clip has finished.
## The brain asks it every physics frame: while it is true the player may not walk, run, jump, aim or interact (CHANGE-BRIEF phase table).
func is_raising_tablet() -> bool:
	return _raising_tablet


## Returns whether the tablet screen is lit (and clickable) this physics frame. The brain passes it to the demo tablet, whose screen follows the same moment.
func is_tablet_screen_lit() -> bool:
	return _tablet_screen_lit


## The player brain calls this at the start of the game to get the tablet in this character's hand, so it can hand the tablet system's picture to its screen.
## The brain uses it only to hand over the picture (presentation); where the tablet is held and whether it is lit are still decided only by the body itself.
func get_tablet() -> TabletDevice:
	return _tablet  # We hand out the tablet in this character's hand


## Switches the tablet state by this frame's tablet key result, and emits tablet_hold_changed when the state changed.
## Called by apply_intent() every physics frame; does nothing when press is NONE.
func _apply_tablet_press(press: CharacterIntent.TabletPress) -> void:
	if press == CharacterIntent.TabletPress.NONE:
		return
	var old_hold := _tablet_hold
	_tablet_hold = _next_tablet_hold(old_hold, press)
	_raising_tablet = old_hold == TabletHold.NONE and _tablet_hold == TabletHold.ONE_HAND  # Only a short press from put away starts the raise; any other change ends or skips it
	tablet_hold_changed.emit(old_hold, _tablet_hold)


## Looks up the switching table (design document section 5.8): current state + short or long press -> new state. Calculation only, changes nothing.
func _next_tablet_hold(current: TabletHold, press: CharacterIntent.TabletPress) -> TabletHold:
	var is_long := press == CharacterIntent.TabletPress.LONG
	match current:  # match is the switch of other languages
		TabletHold.NONE:
			return TabletHold.TWO_HAND if is_long else TabletHold.ONE_HAND
		TabletHold.ONE_HAND:
			return TabletHold.TWO_HAND if is_long else TabletHold.NONE
		_:  # The remaining case: TWO_HAND (_ is switch's default)
			return TabletHold.NONE if is_long else TabletHold.ONE_HAND

