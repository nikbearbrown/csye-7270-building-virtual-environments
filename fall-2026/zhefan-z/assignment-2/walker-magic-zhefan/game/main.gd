extends Node2D
## The asset slice: about two screens of cave with one pit. Owns the camera and the
## fail -> reload flow; game objects only emit signals.

const LEVEL_WIDTH := 1280
const VIEW := Vector2(640, 360)
const RELOAD_DELAY := 1.2   # longer than SFX-FAIL (trimmed to 1.0 s), CHANGE-BRIEF failure case 6

## Tests set this so a fail does not reload the scene underneath them.
var test_mode := false
var failed_reason := ""

@onready var camera: Camera2D = $Camera2D
@onready var player: CharacterBody2D = get_node_or_null("Player")


func _enter_tree() -> void:
	Controls.ensure()


func _ready() -> void:
	camera.limit_left = 0
	camera.limit_right = LEVEL_WIDTH
	camera.limit_top = 0
	camera.limit_bottom = int(VIEW.y)
	camera.position = VIEW / 2
	if player:
		player.failed.connect(_on_player_failed)


func _process(_delta: float) -> void:
	# Follow horizontally; freeze once the player fails (storyboard P4: the camera stops at the pit edge).
	if player and failed_reason.is_empty():
		camera.position.x = clampf(roundf(player.global_position.x), VIEW.x / 2, LEVEL_WIDTH - VIEW.x / 2)


func _on_player_failed(reason: String) -> void:
	failed_reason = reason
	if test_mode:
		return
	await get_tree().create_timer(RELOAD_DELAY).timeout
	get_tree().reload_current_scene()
