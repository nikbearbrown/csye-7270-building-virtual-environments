# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends Node3D  # Root-node script of the preview scene landing_dust_preview.tscn
## A6 preview for Effect A (landing dust), for the rendered frame strip (not an automated test, and not gameplay).
## It loads the real base (its floor, furniture, ceiling lights and environment), stands the real player on the landing point as the scale reference,
## places a camera where the in-game third-person camera would be, and triggers the effect with restart() at frame 10,
## and again 0.5 m to the side at frame 25 when retrigger is on (CHANGE-BRIEF "Effect A: Frame strip").
## Nothing listens to the player's landing here: the frames are fixed, so the strip is the same on every run.
## The two captures: retrigger off (read frames 10-60) and retrigger on (read frames 25, 27, 30, 35), once each over each background.
## Command-line switches after "--" override the exports: "dark" picks the dark background, "retrigger" turns the second landing on.
## The preview's instance of the effect has use_fixed_seed on (seed 7270, set in landing_dust_preview.tscn), so every capture round scatters the
## particles the same way and before/after comparisons only show the settings change. The effect scene itself keeps random seeds, so repeats vary in the game.

# ============================================================
# Constants: the frames and the in-game camera rig, from CHANGE-BRIEF and player.tscn
# ============================================================
enum Background { BRIGHT, DARK }  # The two backgrounds the brief names
const TRIGGER_FRAME := 10  # The first landing (CHANGE-BRIEF: trigger at frame 10)
const RETRIGGER_FRAME := 25  # The second landing, inside the first burst's 1.6 s life (CHANGE-BRIEF: frame 25)
const RETRIGGER_OFFSET := Vector3(0.5, 0.0, 0.0)  # The second landing is 0.5 m to the side, so the old and new bursts can be told apart
const PIVOT_HEIGHT := 1.45  # player.tscn CameraPivot: 1.45 m above the feet
const ARM_SIDE := 0.45  # player.tscn SpringArm3D: 0.45 m to the right of the pivot
const ARM_LENGTH := 2.2  # player.tscn SpringArm3D spring_length: the camera sits 2.2 m behind along the arm

# ============================================================
# Exported variables (@export): the preview's switches, set in the Inspector or from the command line
# ============================================================
@export var background: Background = Background.BRIGHT  # Which landing point (and so which background) we preview
@export var retrigger := false  # Off: one landing at frame 10. On: a second landing at frame 25
## Bright candidate: the open floor near ceiling light 1 (light 1 is at (0.02, 2.60, -3.66); the desks start at z = -4).
@export var bright_point := Vector3(0.0, 0.25, -2.6)
## Dark candidate: beside the L-shaped desk on the side away from light 1, in its shadow. A candidate only; confirm in the real picture.
@export var dark_point := Vector3(-2.6, 0.25, -3.3)
## Camera pitch of the in-game rig, degrees (negative = looking down). Level (0) cuts the near half of the dust off the bottom of the frame,
## so we look down as a player would to watch their feet; the player controller allows down to -70.
@export_range(-70.0, 60.0) var view_pitch_degrees := -30.0

# ============================================================
# Node references (@onready): nodes used in the scene
# ============================================================
@onready var _player: Node3D = $Base/Player  # The real player body in base.tscn: our scale reference at the landing point
@onready var _player_brain: Node = $Base/Player/PlayerController  # The player brain: it reads input and moves its own camera, so we switch it off
@onready var _effect: Node3D = $LandingDust  # The effect root; we move it to the landing point and restart its two emitters
@onready var _camera: Camera3D = $PreviewCamera  # Our fixed camera at the in-game third-person position

var _frame := 0  # How many frames we have processed; the triggers fire when it reaches their frame numbers
var _landing_point := Vector3.ZERO  # Where the first landing happens; set in _ready() from the chosen background


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times
# ============================================================
## Called by Godot once, after Base, the effect and the camera are ready (children are ready before their parent).
## We read the command-line switches, switch the player brain off, stand the player on the landing point and fix the camera there.
func _ready() -> void:
	_read_command_line()  # First we let the command line override the exports, so one scene file serves all four captures
	_landing_point = bright_point if background == Background.BRIGHT else dark_point  # Then we pick the landing point for this capture
	_player_brain.process_mode = Node.PROCESS_MODE_DISABLED  # We stop the brain: no input, no movement, no camera turning, so every run is the same
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE  # The brain captured the mouse in its own _ready(); we give it back
	_player.global_position = _landing_point  # We stand the player where the dust will rise, so the strip shows it at character scale
	_effect.global_position = _landing_point  # The effect root sits on the landing point; its emitters are raised 0.04 m and 0.01 m by the scene
	_camera.global_transform = _third_person_view(_landing_point)  # We place the camera where the in-game rig would put it for a player standing here
	_camera.make_current()  # And render through it (the brain had made the player camera current; we take over after it)
	print("[preview] background %s, retrigger %s, landing at %s" % [Background.keys()[background], retrigger, _landing_point])


## Called by Godot once per rendered frame. Fires the landing at frame 10, and the second landing at frame 25 when retrigger is on.
func _process(_delta: float) -> void:
	if _frame == TRIGGER_FRAME:  # If this is the first landing frame, we land on the chosen point
		_land(_landing_point)
	elif retrigger and _frame == RETRIGGER_FRAME:  # Otherwise, if retrigger is on and this is frame 25, we land again 0.5 m to the side
		_land(_landing_point + RETRIGGER_OFFSET)
	_frame += 1  # Then we count this frame; the next call is the next frame


# ============================================================
# Feature functions: called by the callbacks above
# ============================================================
## Called by _process() on a landing frame. Moves the player and the effect to the landing point and replays both emitters.
## restart(), not emitting = true: restart clears a burst still alive and plays again, so at most one burst exists (CHANGE-BRIEF retrigger rule).
func _land(point: Vector3) -> void:
	_player.global_position = point  # The player is now standing on the new landing point
	_effect.global_position = point  # We move the effect first; with local_coords off, the new particles are born here, and restart() clears the old ones
	for emitter in _effect.get_children():  # Then for both emitters, Dust and GroundRing
		(emitter as GPUParticles3D).restart()  # We clear what is left and start a new burst
	print("[preview] frame %d: landing at %s" % [_frame, point])  # We print the frame, so the strip's file numbers can be matched to it


## Called by _ready(). Works out the in-game third-person camera for a player standing at feet, the same chain as player.tscn:
## pivot 1.45 m above the feet, turned by (pitch, yaw 0); then the arm 0.45 m to the right and 2.2 m back along it.
func _third_person_view(feet: Vector3) -> Transform3D:
	var pivot := Transform3D(Basis.from_euler(Vector3(deg_to_rad(view_pitch_degrees), 0.0, 0.0)), feet + Vector3(0.0, PIVOT_HEIGHT, 0.0))  # The camera pivot, looking toward -Z and down by the pitch
	return pivot * Transform3D(Basis.IDENTITY, Vector3(ARM_SIDE, 0.0, ARM_LENGTH))  # The end of the arm, in the world: this is where the camera sits and how it faces


## Called by _ready(). Reads the user arguments after "--": "dark" picks the dark background, "retrigger" turns the second landing on.
func _read_command_line() -> void:
	var args := OS.get_cmdline_user_args()  # Only the arguments after "--"; Godot's own arguments are not in here
	if args.has("dark"):  # If "dark" is given, we preview over the dark background
		background = Background.DARK
	if args.has("bright"):  # If "bright" is given, we preview over the bright background
		background = Background.BRIGHT
	if args.has("retrigger"):  # If "retrigger" is given, we add the second landing at frame 25
		retrigger = true
