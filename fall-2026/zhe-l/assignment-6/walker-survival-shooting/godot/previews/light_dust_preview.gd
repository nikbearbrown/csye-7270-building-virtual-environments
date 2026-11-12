# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Node3D  # Root-node script of the preview scene light_dust_preview.tscn
## A6 preview for Effect B (dust under the ceiling light), for the rendered frame strip (not an automated test, and not gameplay).
## It loads the real base (its walls, furniture, ceiling lights, CeilingLights keeper and environment), places the effect at the brief's
## (0, 1.45, -3.20) under ceiling light 1, stands the real player near it as the scale reference, and puts a camera where the in-game
## third-person camera would be for that player.
## The timing follows CHANGE-BRIEF "Effect B: Frame strip": the lights start off (a test fixture; in the game they start on),
## frame 10 lights on, frame 45 pause, frame 55 unpause, frame 60 hide, frame 65 show again, frame 70 lights off; capture with --quit-after 100.
## The preview stands in for the wall switch: it calls CeilingLights.set_lights_on() at frames 10 and 70, as a press of F would.
## It also stands in for the effect's listener, which is not written yet: it listens to lights_changed, queries is_lights_on() once at start,
## and shows / hides / restart()s the emitter. That listener code is preview-only; nothing here is wired into gameplay.
## Command-line switches after "--": "dark" (the default) views the wall behind ceiling light 1, "bright" views a lit wall.
## The preview's instance of the effect has use_fixed_seed on (seed 7270, set in light_dust_preview.tscn), so capture rounds can be compared.

# ============================================================
# Constants: the frames and the in-game camera rig, from CHANGE-BRIEF and player.tscn
# ============================================================
enum Background { DARK, BRIGHT }  # The two backgrounds the brief names
const LIGHTS_ON_FRAME := 10  # The condition starts: the ceiling lights come on
const PAUSE_FRAME := 45  # The tree is paused (the game has no pause feature yet, so we set it directly, as the brief says)
const UNPAUSE_FRAME := 55  # The tree runs again
const HIDE_FRAME := 60  # The effect node is hidden while the light is still on
const SHOW_FRAME := 65  # The effect node is shown again, light still on
const LIGHTS_OFF_FRAME := 70  # The condition ends: the ceiling lights go off
const PIVOT_HEIGHT := 1.45  # player.tscn CameraPivot: 1.45 m above the feet
const ARM_SIDE := 0.45  # player.tscn SpringArm3D: 0.45 m to the right of the pivot
const ARM_LENGTH := 2.2  # player.tscn SpringArm3D spring_length: the camera sits 2.2 m behind along the arm

# ============================================================
# Exported variables (@export): the preview's switches, set in the Inspector or from the command line
# ============================================================
@export var background: Background = Background.DARK  # Which view (and so which background) we preview
## Dark candidate: the player stands 2 m in front of the dust, 0.45 m to its left, facing -Z, so the camera looks straight at
## the dust with the back wall behind ceiling light 1 behind it (about 4.2 m from camera to dust). A candidate only; confirm in the real picture.
@export var dark_feet := Vector3(-0.45, 0.25, -1.2)
@export var dark_yaw_degrees := 0.0  # Facing -Z, toward the back wall
## Bright candidate: the player stands west of the dust facing +X, so the background is the east end of the room, lit by ceiling light 2
## (at x = 5.38, about 2 m from the east wall). About 4.2 m from camera to dust. A candidate only; confirm in the real picture.
@export var bright_feet := Vector3(-2.0, 0.25, -2.8)
@export var bright_yaw_degrees := -90.0  # Facing +X, toward the east wall
## Camera pitch of the in-game rig, degrees (negative = looking down). Level, because the dust hangs at head height (0.65-2.25 m).
@export_range(-70.0, 60.0) var view_pitch_degrees := 0.0

# ============================================================
# Node references (@onready): nodes used in the scene
# ============================================================
@onready var _player: Node3D = $Base/Player  # The real player body in base.tscn: our scale reference
@onready var _player_brain: Node = $Base/Player/PlayerController  # The player brain: it reads input and moves its own camera, so we switch it off
@onready var _ceiling_lights: CeilingLights = $Base/CeilingLights  # The only keeper of the light state; we press its switch and listen to it
@onready var _dust: GPUParticles3D = $LightDust  # The effect: one emitter, placed under ceiling light 1 by this scene
@onready var _camera: Camera3D = $PreviewCamera  # Our fixed camera at the in-game third-person position

var _frame := 0  # How many frames we have processed; the steps fire when it reaches their frame numbers


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot once, after Base, the effect and the camera are ready (children are ready before their parent),
## so CeilingLights has already set its start state. We place the player and camera, start listening, and turn the lights off for the fixture.
func _ready() -> void:
	_read_command_line()  # First we let the command line override the exports, so one scene file serves both captures
	var feet := dark_feet if background == Background.DARK else bright_feet  # Then we pick where the player stands for this view
	var yaw := dark_yaw_degrees if background == Background.DARK else bright_yaw_degrees  # And which way the player faces
	_player_brain.process_mode = Node.PROCESS_MODE_DISABLED  # We stop the brain: no input, no movement, no camera turning, so every run is the same
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE  # The brain captured the mouse in its own _ready(); we give it back
	_player.global_position = feet  # We stand the player there, so the strip shows the specks at character scale
	_player.global_rotation = Vector3(0.0, deg_to_rad(yaw), 0.0)  # Facing away from the camera, as in the game
	_camera.global_transform = _third_person_view(feet, yaw)  # We place the camera where the in-game rig would put it for a player standing here
	_camera.make_current()  # And render through it (the brain had made the player camera current; we take over after it)
	_ceiling_lights.lights_changed.connect(_on_lights_changed)  # From now on every real change of the light state reaches the dust
	_on_lights_changed(_ceiling_lights.is_lights_on())  # The keeper does not emit at start, so we ask once (on in the game) and follow it
	_ceiling_lights.set_lights_on(false)  # Fixture start: the lights go off before the first frame, so frame 9 has no dust (the switch would do this)
	print("[preview] background %s, feet %s, yaw %.0f, dust at %s" % [Background.keys()[background], feet, yaw, _dust.global_position])


## Called by Godot once per rendered frame, also while the tree is paused (this root's process_mode is ALWAYS; Base and the dust are PAUSABLE).
## Fires the brief's steps on their frames.
func _process(_delta: float) -> void:
	if _frame == LIGHTS_ON_FRAME:  # If this is frame 10, we press the switch: the lights come on, and lights_changed starts the dust
		_ceiling_lights.set_lights_on(true)
	elif _frame == PAUSE_FRAME:  # If this is frame 45, we pause the tree; the dust should freeze in place
		get_tree().paused = true
	elif _frame == UNPAUSE_FRAME:  # If this is frame 55, we let it run again; the dust should drift and twinkle again
		get_tree().paused = false
	elif _frame == HIDE_FRAME:  # If this is frame 60, we hide the node while the light stays on
		_hide_dust()
	elif _frame == SHOW_FRAME:  # If this is frame 65, we show it again; with the light on it should be full at once
		_show_dust_if_lit()
	elif _frame == LIGHTS_OFF_FRAME:  # If this is frame 70, we press the switch again: the lights go off, and lights_changed hides the dust
		_ceiling_lights.set_lights_on(false)
	if _frame in [LIGHTS_ON_FRAME, PAUSE_FRAME, UNPAUSE_FRAME, HIDE_FRAME, SHOW_FRAME, LIGHTS_OFF_FRAME]:  # On a step frame
		print("[preview] frame %d: lights %s, paused %s, dust visible %s, emitting %s" % [_frame, _ceiling_lights.is_lights_on(), get_tree().paused, _dust.visible, _dust.emitting])  # We print the state, so the strip's file numbers can be matched to it
	_frame += 1  # Then we count this frame; the next call is the next frame


# ============================================================
# Feature functions: the stand-in listener, called by the callbacks above
# ============================================================
## Called by CeilingLights.lights_changed, and once by _ready() with the queried state. Reads the light state and never writes it.
## Lights on: show and restart the dust. Lights off: hide it and stop emitting at once, so no glowing specks are left after the light.
func _on_lights_changed(lights_on: bool) -> void:
	if lights_on:  # If the lights are on, the dust under them shows, preprocessed again
		_show_dust_if_lit()
	else:  # Otherwise it goes away with the light
		_hide_dust()


## Called on lights off and at frame 60. Invisible at once, and no new specks are born (CHANGE-BRIEF: "stops and its old progress is thrown away").
func _hide_dust() -> void:
	_dust.visible = false  # First we hide it, so nothing is drawn from this frame on
	_dust.emitting = false  # Then we stop births; restart() on the next show throws away whatever is left


## Called on lights on and at frame 65. Only when the lights are on: visible again, and restart() so preprocess runs again
## (whether restart() re-runs preprocess in 4.7.2 is a brief "Unconfirmed" item; frames 11 and 66 of the strip show it).
func _show_dust_if_lit() -> void:
	if not _ceiling_lights.is_lights_on():  # If the lights are off, the dust stays hidden even when the node is "shown"
		return
	_dust.visible = true  # We show it ...
	_dust.restart()  # ... and start it from scratch: the old progress is dropped, emitting turns on, and preprocess fills the box


## Called by _ready(). Works out the in-game third-person camera for a player standing at feet and facing yaw, the same chain as player.tscn:
## pivot 1.45 m above the feet, turned by (pitch, yaw); then the arm 0.45 m to the right and 2.2 m back along it.
func _third_person_view(feet: Vector3, yaw_degrees: float) -> Transform3D:
	var turn := Basis.from_euler(Vector3(deg_to_rad(view_pitch_degrees), deg_to_rad(yaw_degrees), 0.0))  # The pivot's turn: yaw first, then pitch, as the rig does
	var pivot := Transform3D(turn, feet + Vector3(0.0, PIVOT_HEIGHT, 0.0))  # The camera pivot above the feet
	return pivot * Transform3D(Basis.IDENTITY, Vector3(ARM_SIDE, 0.0, ARM_LENGTH))  # The end of the arm, in the world: this is where the camera sits and how it faces


## Called by _ready(). Reads the user arguments after "--": "dark" or "bright" picks the background.
func _read_command_line() -> void:
	var args := OS.get_cmdline_user_args()  # Only the arguments after "--"; Godot's own arguments are not in here
	if args.has("dark"):  # If "dark" is given, we view the wall behind ceiling light 1
		background = Background.DARK
	if args.has("bright"):  # If "bright" is given, we view the lit wall
		background = Background.BRIGHT
