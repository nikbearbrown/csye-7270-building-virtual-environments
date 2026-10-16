extends Camera2D
## The storyboard's camera moves. Visual only: the simulation never reads the camera.
## P1 slow push-in on the title · P5 Dutch tilt on a hit · P6 zoom-out on Sunflare · P9 pull-back as the fog lifts.
## P5/P6 are driven by simulation ticks (deterministic); P1/P9 by real time, because the simulation is stopped then.

const Tuning = preload("res://features/tuning.gd")
const GameState = preload("res://game/game_state.gd")

const MENU_FROM := 0.8
const MENU_SECONDS := 3.0
const TILT_RAD := 0.07
const SUNFLARE_ZOOM := 0.72
const SUNFLARE_OUT_TICKS := 20
const SUNFLARE_BACK_TICKS := 70
const WIN_ZOOM := 0.82
const WIN_SECONDS := 2.0

var session
var evolve_tick := -1
var _menu_t := 0.0
var _end_t := 0.0

func setup(s) -> void:
	session = s
	ignore_rotation = false
	zoom = Vector2.ONE * MENU_FROM
	s.evolved.connect(func(): evolve_tick = s.tick_count)
	s.run_started.connect(_on_run_started)

func _on_run_started() -> void:
	evolve_tick = -1
	_end_t = 0.0
	rotation = 0.0
	zoom = Vector2.ONE

func zoom_for_tick(t: int) -> float:
	if evolve_tick < 0 or t < evolve_tick:
		return 1.0
	var dt := t - evolve_tick
	if dt <= SUNFLARE_OUT_TICKS:
		return lerpf(1.0, SUNFLARE_ZOOM, float(dt) / SUNFLARE_OUT_TICKS)
	if dt <= SUNFLARE_OUT_TICKS + SUNFLARE_BACK_TICKS:
		return lerpf(SUNFLARE_ZOOM, 1.0, float(dt - SUNFLARE_OUT_TICKS) / SUNFLARE_BACK_TICKS)
	return 1.0

func tilt_for(player) -> float:
	var k: int = player.iframes - (Tuning.IFRAME_TICKS - Tuning.HURT_POSE_TICKS)
	if k <= 0:
		return 0.0
	return TILT_RAD * float(k) / Tuning.HURT_POSE_TICKS * -player.facing

## Called by the session at the end of every simulation tick.
func on_tick() -> void:
	zoom = Vector2.ONE * zoom_for_tick(session.tick_count)
	rotation = tilt_for(session.player)

## 0..1: how far the fog has lifted after a win (the HUD washes the screen with mist by this much).
func fog_lift() -> float:
	return smoothstep(0.0, 1.0, _end_t / WIN_SECONDS)

func _process(delta: float) -> void:
	if session == null:
		return
	match session.state.current:
		GameState.MENU:
			_menu_t = minf(_menu_t + delta, MENU_SECONDS)
			zoom = Vector2.ONE * lerpf(MENU_FROM, 1.0, smoothstep(0.0, 1.0, _menu_t / MENU_SECONDS))
		GameState.WON:
			_end_t = minf(_end_t + delta, WIN_SECONDS)
			rotation = 0.0
			zoom = Vector2.ONE * lerpf(1.0, WIN_ZOOM, fog_lift())
		GameState.LOST:
			rotation = 0.0
