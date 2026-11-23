# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Node3D  # The preview's root: it loads the real base scene under itself
## A7 frame-strip preview for the committing action (the one-handed raise), for a windowed Movie Maker run that I start (CHANGE-BRIEF "The frame strip").
## It loads the real subway base, waits a moment, then takes the tablet out with one short Tab press sent like a real key, and prints one log line per
## rendered frame (movie frame, physics frame, hold state, animation state, clip position, screen lit), so frame N of the capture lines up with log line N.
## Camera: the player's own game camera. With the user argument --front, the same camera turned 180 degrees around the player (my decision: the player's own
## camera seen from the front, not a separate camera); standing still, the character does not turn with it, so it films her front.
## Run (from the walker-survival-shooting folder):
##   godot --path godot res://previews/tablet_raise_preview.tscn --write-movie "$PWD/captures/tablet_raise/r0/frame.png" --fixed-fps 30 --quit-after 90 > logs/tablet_raise_r0.log
##   (add "-- --front" at the end for the front view, into another folder)

# ============================================================
# Constants: when to press, and which node turns the camera for the front view
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The real game scene
const PRESS_AT_FRAME := 30  # The rendered frame on which we press Tab (1 s in at 30 fps), so the player has landed and everything has started
const TAP_FRAMES := 2  # How many rendered frames the key stays down: a short press
const CAMERA_PIVOT_PATH := "PlayerController/CameraPivot"  # The pivot the player's camera orbits on (player.tscn)

# ============================================================
# Member variables: what the preview keeps while it runs
# ============================================================
var _player: Humanoid  # The player body in the base scene
var _playback: AnimationNodeStateMachinePlayback  # The tablet state machine's playback, read only for the log
var _frame := 0  # Rendered frames since the start

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Godot calls this once when the preview starts: we load the base scene, find the player, and turn its camera to the front if asked for.
func _ready() -> void:
	process_priority = 1000  # We run after every other node in each frame, so the log line shows the pose the AnimationTree has just set, the one this frame renders (found after r1: at the default priority the line showed the previous frame's clip position)
	var base: Node = load(BASE_SCENE).instantiate()  # First we build the real subway base under the preview
	add_child(base)
	_player = base.get_node("Player") as Humanoid
	await get_tree().process_frame  # We let the player run _ready() before we read its AnimationTree
	_playback = _player.get_node("AnimationTree").get("parameters/playback")
	if "--front" in OS.get_cmdline_user_args():  # If the run asks for the front view,
		var pivot := _player.get_node(CAMERA_PIVOT_PATH) as Node3D
		pivot.rotation.y += PI  # we turn the player's own camera half a turn around her, so it looks at her front
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
