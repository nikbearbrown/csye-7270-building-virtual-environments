# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name PlayerController  # Global class name: the player brain
extends Node3D  # Extends Node3D: so the camera under it moves along with the body
## Player brain (code rule 7a): reads keyboard and mouse, turns the local camera, packs the input into an intent, and hands it to the body.
## Attached under the humanoid body (Humanoid); its parent is the body it drives.
## The mouse turns only the camera, not the character; the body decides its facing from the move direction.

# ============================================================
# Constants: values defined once that never change
# ============================================================
const PLAYER_GROUP := &"players"  # Every player body joins this group (rule 6: never assume there is only one player)
const THIRD_PERSON_BLEND := 0.0  # View blend value: camera fully at the third-person position
const FIRST_PERSON_BLEND := 1.0  # View blend value: camera fully at the first-person position

# ============================================================
# Exported variables (@export): feel parameters shown in the Inspector and tuned there
# ============================================================
## Camera feel parameters (code rule 1a): tuned in the Inspector, not hard-coded.
@export var mouse_sensitivity: float = 0.0025  # Radians the view turns per pixel of mouse movement
@export_range(-89.0, 0.0) var pitch_min_degrees: float = -70.0  # How far down you can look, in degrees
@export_range(0.0, 89.0) var pitch_max_degrees: float = 60.0  # How far up you can look, in degrees
@export var tablet_long_press_seconds: float = 0.4  # Seconds the tablet key must be held to count as a long press; released sooner = short press
@export var aim_transition_seconds: float = 0.15  # Seconds for the camera to move from third person to the eyes when aiming with the right button (0 = cut instantly)
@export var tablet_transition_seconds: float = 0.35  # Seconds for the camera to move from third person to the eyes when holding the tablet in both hands
@export_range(0.0, 1.0) var hide_body_at_blend: float = 0.7  # Hide your own body once the view blend passes this value (the camera is nearly inside the head)
@export_range(-89.0, 89.0) var tablet_view_pitch_degrees: float = -20.0  # First-person camera pitch while holding the tablet in both hands: -20 = looking down at the tablet a little (0 = level, negative = down)

# ============================================================
# Member variables: state used inside this script (leading underscore = internal to this script)
# ============================================================
var _look_delta := Vector2.ZERO  # Mouse movement accumulated between two physics frames, processed together in the physics frame
var _tablet_held_seconds := 0.0  # Seconds the tablet key has been held; reset on release
var _view_blend := THIRD_PERSON_BLEND  # View blend value (the "slider"): 0 = third person, 1 = first person, in between = mid-transition
var _view_target := THIRD_PERSON_BLEND  # Where the slider is heading: 0 or 1. The slider is pushed toward it a little every frame
var _view_transition_seconds := 0.0  # How long this transition takes. Set when entering first person, reused when going back (leave the way you came in)
var _view_is_tablet := false  # Whether this first-person view is because of the two-handed tablet: yes = the camera ends up level, facing the tablet. Reused when going back

# ============================================================
# Node references (@onready): nodes used in the scene
# ============================================================
# @onready: assigned after the node enters the scene tree and its children are ready
@onready var _body: Humanoid = get_parent() as Humanoid  # Parent node: the humanoid body this brain drives
@onready var _camera_pivot: Node3D = $CameraPivot  # Camera pivot: looking left/right turns its Y axis, up/down turns its X axis
@onready var _spring_arm: SpringArm3D = $CameraPivot/SpringArm3D  # The camera arm that shortens against walls
@onready var _third_person_position: Marker3D = $CameraPivot/SpringArm3D/ThirdPersonCameraPosition  # Where the camera belongs in third person: at the arm's end, dodging walls with it
@onready var _first_person_position: Marker3D = $CameraPivot/FirstPersonCameraPosition  # Where the camera belongs in first person: the eyes
@onready var _camera: Camera3D = $PlayerCamera  # The only camera that actually renders; placed between the two positions above every frame


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points; GDScript has no main)
# ============================================================
## Called by Godot: runs once after the node and its children have entered the scene tree; used for setup.
func _ready() -> void:
	_body.add_to_group(PLAYER_GROUP)  # Put the body in the players group; monsters will pick targets from this group
	_spring_arm.add_excluded_object(_body.get_rid())  # When the camera arm checks for walls, ignore the body's own capsule
	_camera.make_current()  # Render with the player camera (replaces preview_camera in the scene)
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED  # Lock and hide the mouse; mouse movement only turns the view
	_body.tablet_hold_changed.connect(_on_tablet_hold_changed)  # When the tablet state changes, switch the mouse (locked / visible)


## Called by Godot: runs for every input event (keyboard, mouse) that the UI or other nodes did not handle.
## Only handles the mouse here: records mouse movement, Esc frees the mouse, clicking the view locks it again (not while holding the tablet).
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		_look_delta += (event as InputEventMouseMotion).relative  # Accumulate mouse movement, processed in the physics frame
	elif event.is_action_pressed(&"ui_cancel"):  # ui_cancel is a built-in Godot action, Esc by default
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE  # Free the mouse
	elif event is InputEventMouseButton and event.pressed and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		if not _is_holding_tablet():  # While holding the tablet the mouse is for clicking the tablet, so a click must not lock it again
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED  # Click the view while the mouse is free to lock it again


## Called by Godot: runs once per physics frame (60 times a second by default); delta is the seconds since the last frame.
## First turns the local camera, then reads the intent and hands it to the body, and finally decides which view the camera heads for from the aim and tablet state.
func _physics_process(delta: float) -> void:
	_rotate_camera()
	var intent := _read_intent(delta)
	_body.apply_intent(intent, delta)
	_update_view(intent.aim)


## Called by Godot: runs once per rendered frame (follows the frame rate, so more or fewer times than physics frames), after this frame's physics frame.
## First pushes the slider toward its target a little, then places the camera. It is here rather than in the physics frame so the camera arm has finished dodging walls this frame.
func _process(delta: float) -> void:
	_move_view_blend(delta)
	_update_camera()


# ============================================================
# Feature functions: our own functions, called by the callbacks above
# ============================================================
## Turns the local camera by the mouse movement accumulated over this time: left/right turns the pivot's Y axis, up/down its X axis.
## Turns only the camera, not the character. The camera is local "presentation", so it is not part of the intent (rule 5).
func _rotate_camera() -> void:
	_camera_pivot.rotation.y -= _look_delta.x * mouse_sensitivity  # Mouse right, view right (negative direction around Y)
	_camera_pivot.rotation.x = clampf(  # clampf: limits a value between a minimum and a maximum
		_camera_pivot.rotation.x - _look_delta.y * mouse_sensitivity,  # Mouse up, look up
		deg_to_rad(pitch_min_degrees), deg_to_rad(pitch_max_degrees))  # Degrees converted to radians
	_look_delta = Vector2.ZERO  # The mouse movement is used up; reset and start accumulating again


## Reads this frame's keys and camera facing into a CharacterIntent. Reads input only, moves nothing.
## Filtered by the tablet state (design document section 5.8): whatever is not put in the intent, the body does not do this frame.
##   Not holding the tablet: everything is allowed.
##   One-handed: walking only; no sprint, jump or aim (shooting and using medicine will go here later too).
##   Two-handed: operating the tablet only; walk, sprint, jump and aim are not put in the intent.
func _read_intent(delta: float) -> CharacterIntent:
	var intent := CharacterIntent.new()  # Everything in a new intent defaults to "don't" (zero, false)
	var hold := _body.get_tablet_hold()  # Ask the body: is the tablet held now, and how?
	intent.look_yaw = _camera_pivot.global_rotation.y  # The player's "look direction" = the camera's left/right facing in the world
	if hold != Humanoid.TabletHold.TWO_HAND:  # Walking only when not holding the tablet in both hands
		# get_vector combines four direction keys into a 2D vector whose length stays at most 1 when moving diagonally
		intent.move = Input.get_vector(&"move_left", &"move_right", &"move_back", &"move_forward")
	if hold == Humanoid.TabletHold.NONE:  # Sprint, jump and aim only with no tablet in hand
		intent.sprint = Input.is_action_pressed(&"sprint")  # True for as long as it is held
		intent.jump = Input.is_action_just_pressed(&"jump")  # True only on the frame it was just pressed
		intent.aim = Input.is_action_pressed(&"aim")  # True for as long as the right button is held
	intent.tablet_press = _read_tablet_press(delta)  # The tablet key is read in every state, or the tablet could never be put away
	return intent


## Decides whether the tablet key (Tab) was a short press, a long press, or neither this frame. Called once per physics frame by _read_intent().
## While held, time accumulates; the frame that crosses the long-press time counts as one long press. Released before the long-press time, the release frame counts as a short press.
func _read_tablet_press(delta: float) -> CharacterIntent.TabletPress:
	if Input.is_action_pressed(&"tablet"):  # Still held
		var before := _tablet_held_seconds
		_tablet_held_seconds += delta
		if before < tablet_long_press_seconds and _tablet_held_seconds >= tablet_long_press_seconds:
			return CharacterIntent.TabletPress.LONG  # Only the crossing frame matches, so holding on does not count again
		return CharacterIntent.TabletPress.NONE
	# Not held: it was held (time above 0) but not for the long-press time, so it was just released as a short press
	var is_short := _tablet_held_seconds > 0.0 and _tablet_held_seconds < tablet_long_press_seconds
	_tablet_held_seconds = 0.0  # Reset, ready for the next press
	return CharacterIntent.TabletPress.SHORT if is_short else CharacterIntent.TabletPress.NONE


## Whether the local player is holding the tablet now (one-handed or two-handed both count).
## Called by _unhandled_input() and _on_tablet_hold_changed().
func _is_holding_tablet() -> bool:
	return _body.get_tablet_hold() != Humanoid.TabletHold.NONE


## Switches the mouse after the tablet state changes: holding the tablet = show the mouse (for clicking the tablet), tablet put away = lock the mouse (for turning the view).
## Called by the body's tablet_hold_changed signal (connected in _ready()). The mouse is only the local input method, not game state.
## Once the mouse is visible, _unhandled_input() stops accumulating mouse movement, so the view naturally stops turning.
func _on_tablet_hold_changed(_old_hold: Humanoid.TabletHold, _new_hold: Humanoid.TabletHold) -> void:
	_look_delta = Vector2.ZERO  # Drop mouse movement not yet used before the switch, so the view doesn't jerk when taking the tablet
	if _is_holding_tablet():
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE  # Show the mouse; it can move freely on screen
	else:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED  # Lock and hide the mouse; back to turning the view


## Decides whether the camera should head for first or third person (only sets the target, does not move the camera).
## Two-handed tablet or right button held = first person, otherwise third person. This only affects the local picture, not game state (rule 5).
func _update_view(aiming: bool) -> void:
	if _body.get_tablet_hold() == Humanoid.TabletHold.TWO_HAND:
		_view_target = FIRST_PERSON_BLEND
		_view_transition_seconds = tablet_transition_seconds  # Raising the tablet: a little slower
		_view_is_tablet = true  # Raising the tablet: the camera ends up level
	elif aiming:
		_view_target = FIRST_PERSON_BLEND
		_view_transition_seconds = aim_transition_seconds  # Aiming: must be fast, or shooting feels "sticky"
		_view_is_tablet = false  # Aiming: the camera keeps the player's own look direction
	else:
		_view_target = THIRD_PERSON_BLEND  # Back to third person: transition time and _view_is_tablet unchanged, leave the way you came in


## Pushes the slider (_view_blend) toward the target (_view_target) a little, and shows or hides your own body by the slider position.
## Called once per rendered frame by _process(). With a transition time of 0 it jumps straight to the target.
func _move_view_blend(delta: float) -> void:
	if _view_transition_seconds <= 0.0:
		_view_blend = _view_target  # Transition time 0: cut instantly (this also avoids dividing by 0 below)
	else:
		# Push 1 / transition time per second: e.g. finishing in 0.15 s means 6.67 per second, so 6.67 × delta this frame
		# move_toward: moves toward the target by this much, but never overshoots
		_view_blend = move_toward(_view_blend, _view_target, delta / _view_transition_seconds)
	# Hide your own body when the camera is nearly inside the head, or it would film the inside of the body
	_body.set_visual_visible(_view_blend < hide_body_at_blend)


## Places the one camera between the third-person and first-person positions: _view_blend 0 = third-person position, 1 = the eyes.
## Called once per rendered frame by _process(). Position and orientation are blended together, so the camera also turns as it moves.
func _update_camera() -> void:
	# smoothstep: turns the even slider into "slow start → fast middle → slow stop", so the camera moves more softly
	var eased := smoothstep(THIRD_PERSON_BLEND, FIRST_PERSON_BLEND, _view_blend)
	# Transform3D = position + rotation (+ scale); interpolate_with takes the in-between value of two Transform3Ds by a ratio
	_camera.global_transform = _third_person_position.global_transform.interpolate_with(
		_get_first_person_transform(), eased)


## Works out where the camera belongs, and how it faces, in first person. Called once per rendered frame by _update_camera().
## Aiming = the eye position (FirstPersonCameraPosition) as it is, following the player's look direction;
## two-handed tablet = pretend the camera pivot's pitch is tablet_view_pitch_degrees (yaw unchanged), then work out where the eyes are and where they look,
## so whether you looked up or down before taking the tablet, the camera ends at the same position and facing, square to the tablet in front of the eyes.
## Only changes where the camera sits this frame, not the camera pivot (_camera_pivot), so after putting the tablet down the camera returns to the old view angle.
func _get_first_person_transform() -> Transform3D:
	if not _view_is_tablet:
		return _first_person_position.global_transform  # Aiming: the eye position as it is, with the player's current look direction
	var pitch := deg_to_rad(tablet_view_pitch_degrees)  # Pitch: degrees to radians
	var yaw := _camera_pivot.global_rotation.y  # Yaw: the same as the camera pivot (with the two-handed tablet the body also faces this way)
	# A "levelled camera pivot": the same position as the real pivot, with its facing replaced by (pitch, yaw); the final 0.0 = no head tilt
	var level_pivot := Transform3D(Basis.from_euler(Vector3(pitch, yaw, 0.0)), _camera_pivot.global_position)
	# Then chain the eye's position relative to the pivot (FirstPersonCameraPosition's transform) to get the eye's position and facing in the world
	return level_pivot * _first_person_position.transform

