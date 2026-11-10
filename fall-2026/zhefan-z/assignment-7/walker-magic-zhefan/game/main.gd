extends Node2D
## The asset slice: about two screens of cave with one pit, one wolf and the exit. Owns the camera,
## the HUD wiring and the session flow (fail -> reload, exit -> Cleared, Esc pause, R restart).
## Game objects only emit signals; nothing here reacts to sound.

const LEVEL_WIDTH := 1280
const VIEW := Vector2(640, 360)
const RELOAD_DELAY := 1.2   # longer than SFX-FAIL (trimmed to 1.0 s), CHANGE-BRIEF failure case 6

## Tests set this so a fail or restart does not reload the scene underneath them.
var test_mode := false
var failed_reason := ""
var cleared := false
var restart_requested := false

@onready var camera: Camera2D = $Camera2D
@onready var player: CharacterBody2D = get_node_or_null("Player")
@onready var hud: Control = get_node_or_null("UI/HUD")
@onready var audio: AudioDirector = get_node_or_null("AudioDirector")


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
		player.cleared.connect(_on_player_cleared)
		player.hurt.connect(_on_player_hurt)
		var wolves := get_tree().get_nodes_in_group("wolves")
		for wolf in wolves:
			wolf.target = player
		if hud:
			hud.set_hp(player.hp, Tuning.MAX_HP)
		if audio:
			audio.connect_game(player, wolves)
	if hud:
		hud.set_mutes(is_bus_muted("Music"), is_bus_muted("SFX"))


func _process(_delta: float) -> void:
	# Follow horizontally; freeze once the player fails (storyboard P4: the camera stops at the pit edge).
	if player and failed_reason.is_empty():
		camera.position.x = clampf(roundf(player.global_position.x), VIEW.x / 2, LEVEL_WIDTH - VIEW.x / 2)


func toggle_pause() -> void:
	if cleared or not failed_reason.is_empty():
		return
	var tree := get_tree()
	tree.paused = not tree.paused
	if hud:
		hud.show_paused(tree.paused)
	if audio:
		audio.set_paused(tree.paused)


## M / N. Bus mutes are global, so they also hold across a restart.
func toggle_mute(bus_name: String) -> void:
	var idx := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_mute(idx, not AudioServer.is_bus_mute(idx))
	if hud:
		hud.set_mutes(is_bus_muted("Music"), is_bus_muted("SFX"))


func is_bus_muted(bus_name: String) -> bool:
	return AudioServer.is_bus_mute(AudioServer.get_bus_index(bus_name))


func restart_if_cleared() -> void:
	if not cleared:
		return
	if test_mode:
		restart_requested = true
		return
	get_tree().paused = false
	get_tree().reload_current_scene()


func _on_player_hurt(hp: int) -> void:
	if hud:
		hud.set_hp(hp, Tuning.MAX_HP)


func _on_player_failed(reason: String) -> void:
	failed_reason = reason
	if hud:
		hud.show_fail(reason)
	if test_mode:
		return
	await get_tree().create_timer(RELOAD_DELAY).timeout
	get_tree().reload_current_scene()


func _on_player_cleared() -> void:
	cleared = true
	if hud:
		hud.show_cleared()
