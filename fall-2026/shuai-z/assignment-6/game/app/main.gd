class_name Main
extends Node2D
## Runs Level 1. It places Rudy, keeps the camera on him, and runs the level's
## states (CHANGE-BRIEF.md, STORYBOARD.md panels 1 and 4–7):
## - TITLE: the game opens on the start of the level with the title on top
##   (UI-TITLE) and Rudy idle, out of the player's control; the hearts are
##   hidden. Enter fades the title out and the hearts in, and play starts on the
##   same screen. The title shows once each time the game starts: Enter on the
##   end card plays again without it;
## - PLAYING;
## - DYING: a fall below a cliff, which costs a heart, or a hit that takes his
##   last heart. After a fade every monster is back where it started, even the
##   defeated ones, and so is the sword-and-shield pickup. After a fall that leaves him hearts, Rudy gets back up at
##   the last checkpoint, the lit waystone or else the start, with the hearts he
##   has left. Once his last heart is gone, by a hit or a fall, the level starts
##   over from the opening: he is at the start with full hearts, and the
##   waystone is dark;
## - COMPLETE: entered once, on the teleport circle. Input stops, Rudy
##   celebrates, the light rises, the camera pulls back, and the screen fades to
##   the end card, where Enter plays the level again from the opening.
## The camera follows Rudy sideways only, so the ground stays at the same height
## on screen and a fall drops him out of the frame. It shakes briefly on a hit.
##
## In play, Esc pauses everything but the music, which drops 12 dB and keeps
## its place, and shows "Paused"; Esc again resumes. Only in play: not on the
## title, through a death and the respawn, or from the teleport circle on.
## SystemKeys reads the key, since this node stops while the game is paused.
##
## The music (Music, CHANGE-BRIEF.md): it starts on the title and plays on when
## Enter starts play; it dips under a hit and through a death and the respawn,
## and never restarts from the top; on the teleport circle it fades out, and
## the end card is silent. A fall plays the hurt sound as he crosses the kill
## line, since it costs a heart.

signal restart_requested ## only when Main is not the current scene, as in the checks

enum State { TITLE, PLAYING, DYING, COMPLETE }

const KILL_Y := 1300.0 ## below this line he has fallen out of the level
const FALL_HOLD := 0.25 ## s after he crosses the kill line, before the fade
const DEFEAT_HOLD := 0.8 ## s in CHAR-DEFEAT before the fade
const FADE_TIME := 0.35 ## s each way
const CELEBRATE_TIME := 2.0 ## s on the circle before the fade to the end card
const END_ZOOM := Vector2(0.8, 0.8)
const ZOOM_TIME := 1.5
const SHAKE_TIME := 0.2 ## s the camera shakes on a hit
const SHAKE_PX := 8.0

static var title_shown := false ## once the title has shown, a restart goes straight to play

var state := State.PLAYING
var checkpoint_name := "start"

var _checkpoint: Vector2
var _end_card_shown := false
var _shake_left := 0.0

@onready var _level: Node2D = $Level1
@onready var _rudy: Rudy = $Rudy
@onready var _camera: Camera2D = $Camera
@onready var _hud: Hud = $Hud
@onready var _waystone: Waystone = $Level1/Waystone
@onready var _portal: Portal = $Level1/Portal
@onready var _pickup: SwordPickup = $Level1/SwordPickup


func _ready() -> void:
	_checkpoint = (_level.get_node("StartPoint") as Marker2D).global_position
	_rudy.global_position = _checkpoint
	# The right-hand bound marks the end of the level.
	var right_bound: Node2D = _level.get_node("Bounds/Right")
	_camera.limit_right = roundi(right_bound.global_position.x)
	_snap_camera()
	_waystone.activated.connect(_on_waystone_activated)
	_portal.reached.connect(_on_portal_reached)
	_rudy.hit.connect(_on_rudy_hit)
	_rudy.defeated.connect(_on_rudy_defeated)
	_hud.track(_rudy)
	Music.start()
	if not title_shown:
		state = State.TITLE
		_rudy.mode = Rudy.Mode.WAITING
		_hud.show_title()
	_show_status()


func _physics_process(_delta: float) -> void:
	_camera.position.x = _rudy.global_position.x
	if state == State.PLAYING and _rudy.global_position.y > KILL_Y:
		_die(&"fall")


func _process(delta: float) -> void:
	if _shake_left > 0.0:
		_shake_left -= delta
		var shaking := _shake_left > 0.0
		_camera.offset = Vector2(randf_range(-SHAKE_PX, SHAKE_PX), randf_range(-SHAKE_PX, SHAKE_PX)) if shaking else Vector2.ZERO
	if state == State.TITLE and Input.is_action_just_pressed(&"restart"):
		_start_play()
	if _end_card_shown and Input.is_action_just_pressed(&"restart"):
		_end_card_shown = false
		_restart()


## Enter on the title: it fades out, the hearts fade in, and he is the player's.
func _start_play() -> void:
	title_shown = true
	state = State.PLAYING
	_rudy.mode = Rudy.Mode.PLAY
	_hud.hide_title(FADE_TIME)
	_show_status()


## A fall below a cliff, or a defeat at zero hearts. Once his last heart is
## gone, the level starts over from the opening.
func _die(cause: StringName) -> void:
	state = State.DYING # set first, so the kill line ignores him from now on
	var start_over := true # a defeat: his last heart is gone
	if cause == &"fall":
		start_over = _rudy.fall_out() # only if the fall took his last heart
		Sfx.play(&"hurt")
	Music.dip(&"death", Music.DEATH_DIP)
	_show_status()
	await get_tree().create_timer(FALL_HOLD if cause == &"fall" else DEFEAT_HOLD).timeout
	await _hud.fade_to(1.0, FADE_TIME)
	if start_over:
		_back_to_the_opening()
	_rudy.respawn_at(_checkpoint, start_over)
	for monster in _level.get_node("Enemies").get_children():
		monster.reset()
	_pickup.reset() # he gets back up without gear, so the pickup is back where it was
	_shake_left = 0.0
	_camera.offset = Vector2.ZERO
	_snap_camera()
	await _hud.fade_to(0.0, FADE_TIME)
	if _rudy.mode == Rudy.Mode.RESPAWNING:
		await _rudy.respawned
	state = State.PLAYING
	Music.end_dip(&"death")
	_show_status()


## As if the level had just begun: the start is the checkpoint again, and the
## waystone is dark.
func _back_to_the_opening() -> void:
	_checkpoint = (_level.get_node("StartPoint") as Marker2D).global_position
	checkpoint_name = "start"
	_waystone.reset()


## Esc: pauses play, or resumes it. Only in play.
func toggle_pause() -> void:
	var tree := get_tree()
	if tree.paused:
		tree.paused = false
		Music.end_dip(&"pause")
		_hud.show_paused(false)
	elif state == State.PLAYING:
		tree.paused = true
		Music.dip(&"pause", Music.PAUSE_DIP)
		_hud.show_paused(true)


func is_paused() -> bool:
	return get_tree().paused


func _on_rudy_hit() -> void:
	_shake_left = SHAKE_TIME
	Music.dip(&"hurt", Music.HURT_DIP, Music.HURT_TIME)


func _on_rudy_defeated() -> void:
	if state == State.PLAYING:
		_die(&"defeat")


func _on_waystone_activated(waystone: Waystone) -> void:
	_checkpoint = waystone.spawn_point.global_position
	checkpoint_name = "waystone"
	_show_status()


func _on_portal_reached() -> void:
	if state != State.PLAYING:
		return
	state = State.COMPLETE # entered once; input stops
	_rudy.celebrate()
	Sfx.play(&"portal")
	Music.fade_out()
	_show_status()
	_portal.light_up(CELEBRATE_TIME)
	create_tween().tween_property(_camera, "zoom", END_ZOOM, ZOOM_TIME).set_trans(Tween.TRANS_SINE)
	await get_tree().create_timer(CELEBRATE_TIME).timeout
	await _hud.fade_to(1.0, FADE_TIME)
	_hud.show_end_card(FADE_TIME) # Enter works from its first frame
	_end_card_shown = true


## A level that goes away never leaves the game paused.
func _exit_tree() -> void:
	if get_tree().paused:
		get_tree().paused = false
		Music.end_dip(&"pause")


func _restart() -> void:
	if get_tree().current_scene == self:
		get_tree().reload_current_scene()
	else:
		restart_requested.emit()


func _snap_camera() -> void:
	_camera.position.x = _rudy.global_position.x
	_camera.reset_smoothing()


func _show_status() -> void:
	_hud.set_status("%s, checkpoint: %s" % [State.keys()[state], checkpoint_name])
