# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Node3D  # The preview's root: it loads the real base scene under itself
## A7 frame-strip preview for the committing action (the one-handed raise), for a windowed Movie Maker run that I start (CHANGE-BRIEF "The frame strip").
## It loads the real subway base, waits a moment, then takes the tablet out with one short Tab press sent like a real key, and prints one log line per
## rendered frame (movie frame, physics frame, hold state, animation state, clip position, screen lit), so frame N of the capture lines up with log line N.
## Camera: the player's own game camera by default; with the user argument --front, a front camera close to the hand, tablet and face.
## Run (from the walker-survival-shooting folder):
##   godot --path godot res://previews/tablet_raise_preview.tscn --write-movie "$PWD/captures/tablet_raise/r0/frame.png" --fixed-fps 30 --quit-after 90 > logs/tablet_raise_r0.log
##   (add "-- --front" at the end for the front camera strip, into another folder)

# ============================================================
# Constants: when to press, and where the front camera stands
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The real game scene
const PRESS_AT_FRAME := 30  # The rendered frame on which we press Tab (1 s in at 30 fps), so the player has landed and everything has started
const TAP_FRAMES := 2  # How many rendered frames the key stays down: a short press
const FRONT_OFFSET := Vector3(-0.9, 1.35, -1.5)  # Front camera, relative to the player's feet: in front of her and to her left, where the tablet comes up
const FRONT_LOOK_AT := Vector3(-0.15, 1.05, -0.2)  # Where the front camera looks, relative to the player's feet: between the left hand and the face

# ============================================================
# Member variables: what the preview keeps while it runs
# ============================================================
var _player: Humanoid  # The player body in the base scene
var _playback: AnimationNodeStateMachinePlayback  # The tablet state machine's playback, read only for the log
var _frame := 0  # Rendered frames since the start

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Godot calls this once when the preview starts: we load the base scene, find the player, and set up the front camera if asked for.
func _ready() -> void:
	var base: Node = load(BASE_SCENE).instantiate()  # First we build the real subway base under the preview
	add_child(base)
	_player = base.get_node("Player") as Humanoid
	await get_tree().process_frame  # We let the player run _ready() before we read its AnimationTree
	_playback = _player.get_node("AnimationTree").get("parameters/playback")
	if "--front" in OS.get_cmdline_user_args():  # If the run asks for the front camera,
		var camera := Camera3D.new()  # we add one in front of the player, looking at the hand and the face,
		add_child(camera)
		camera.global_position = _player.global_position + FRONT_OFFSET
		camera.look_at(_player.global_position + FRONT_LOOK_AT)
		camera.make_current()  # and make it the camera the movie records
	print("FRAME movie physics hold state clip_pos lit")


## Godot calls this once per rendered frame: we press Tab at the set frame, release it two frames later, and print this frame's log line.
func _process(_delta: float) -> void:
	if _frame == PRESS_AT_FRAME:
		_send_tab(true)  # The key goes down, like a real Tab press
	elif _frame == PRESS_AT_FRAME + TAP_FRAMES:
		_send_tab(false)  # and comes up again before the long-press time: a short press, which takes the tablet out
	if _playback != null:
		print("FRAME %d %d %d %s %.4f %s" % [_frame, Engine.get_physics_frames(), _player.get_tablet_hold(), _playback.get_current_node(), _playback.get_current_play_position(), _player.is_tablet_screen_lit()])
	_frame += 1


# ============================================================
# Functions: the parts of the preview
# ============================================================
## Sends a Tab press or release through Input.parse_input_event, the way a real key reaches the game.
func _send_tab(pressed: bool) -> void:
	var event := InputEventAction.new()
	event.action = &"tablet"
	event.pressed = pressed
	Input.parse_input_event(event)
