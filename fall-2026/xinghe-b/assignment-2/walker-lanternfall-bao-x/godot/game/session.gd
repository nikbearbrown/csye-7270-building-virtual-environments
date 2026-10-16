extends Node2D
## Owns one run. Fixed-tick and deterministic for a given seed: tick() is the whole simulation step.

const Tuning = preload("res://features/tuning.gd")
const GameState = preload("res://game/game_state.gd")
const Progression = preload("res://features/progression/progression.gd")
const PlayerScript = preload("res://features/player/player.gd")
const EnemyScript = preload("res://features/enemies/enemy.gd")
const GemScript = preload("res://features/pickups/gem.gd")
const BeamShot = preload("res://features/weapons/beam_shot.gd")
const WeaponFx = preload("res://features/weapons/weapon_fx.gd")
const Spawner = preload("res://features/enemies/spawner.gd")
const Ground = preload("res://features/world/ground.gd")
const CameraFx = preload("res://features/world/camera_fx.gd")
const AudioBusScript = preload("res://audio/audio_bus.gd")
const Hud = preload("res://ui/hud.gd")

signal run_started
signal enemy_killed(pos: Vector2)
signal gem_collected(value: int)
signal player_hurt(hp: int)
signal leveled_up(level: int)
signal evolved

var test_mode := false
var test_axis := Vector2.ZERO
var test_no_spawn := false

var state = GameState.new()
var prog
var rng := RandomNumberGenerator.new()
var spawner = Spawner.new()
var player
var ground
var actors: Node2D
var fx
var camera
var audio
var hud

var enemies: Array = []
var gems: Array = []
var shots: Array = []
var offered: Array[String] = []
var tick_count := 0
var kills := 0
var beam_timer := 0
var orbit_angle := 0.0
var orbit_hit := {}
var sunflare_timer := 0
var sunflare_ring := 0
var pose_override_ticks := 0
var banner_ticks := 0
var last_dir := Vector2.RIGHT

func _ready() -> void:
	_ensure_inputs()
	ground = Ground.new()
	add_child(ground)
	actors = Node2D.new()
	add_child(actors)
	player = PlayerScript.new()
	player.blocker = ground
	add_child(player)
	fx = WeaponFx.new()
	fx.session = self
	add_child(fx)
	camera = CameraFx.new()
	camera.limit_left = int(Tuning.ARENA.position.x)
	camera.limit_top = int(Tuning.ARENA.position.y)
	camera.limit_right = int(Tuning.ARENA.end.x)
	camera.limit_bottom = int(Tuning.ARENA.end.y)
	player.add_child(camera)
	camera.setup(self)
	player.damaged.connect(func(hp): player_hurt.emit(hp))
	player.died.connect(_on_player_died)
	audio = AudioBusScript.new()
	add_child(audio)
	audio.setup(self)
	hud = Hud.new()
	add_child(hud)
	hud.setup(self)

func start_run(seed_value: int = -1) -> void:
	if seed_value < 0:
		rng.randomize()
	else:
		rng.seed = seed_value
	for n in actors.get_children():
		n.free()
	enemies.clear(); gems.clear(); shots.clear(); offered.clear(); orbit_hit.clear()
	prog = Progression.new()
	prog.leveled_up.connect(func(l): leveled_up.emit(l))
	player.reset()
	tick_count = 0; kills = 0; beam_timer = 0; orbit_angle = 0.0
	sunflare_timer = 0; sunflare_ring = 0; pose_override_ticks = 0; banner_ticks = 0
	last_dir = Vector2.RIGHT
	if state.current == GameState.MENU:
		state.go(GameState.PLAYING)
	else:
		state.restart()
	run_started.emit()

func _physics_process(_d: float) -> void:
	if test_mode or state.current != GameState.PLAYING:
		return
	player.input_axis = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	tick()

func step_ticks(n: int) -> void:
	for i in n:
		tick()

func tick() -> void:
	if state.current != GameState.PLAYING:
		return
	tick_count += 1
	if test_mode:
		player.input_axis = test_axis
	if player.input_axis.length() > 0.1:
		last_dir = player.input_axis.normalized()
	player.step()
	_step_weapons()
	_step_enemies()
	if state.current != GameState.PLAYING:
		return
	_step_gems()
	camera.on_tick()
	if not test_no_spawn:
		spawn_wave(spawner.step(tick_count, rng))
	if banner_ticks > 0:
		banner_ticks -= 1
	if pose_override_ticks > 0:
		pose_override_ticks -= 1
		if pose_override_ticks == 0:
			player.set_override("")
	if tick_count >= Tuning.RUN_SECONDS * Tuning.TICK_HZ:
		player.set_override("victory")
		state.go(GameState.WON)
		return
	if prog.pending_levelups > 0:
		offered = prog.offer_cards(rng)
		player.set_override("levelup")
		state.go(GameState.LEVELUP)

## The rectangle the player can see: the camera follows the courier but stops at the arena edge.
func view_rect() -> Rect2:
	var centre: Vector2 = player.position.clamp(Tuning.ARENA.position + Tuning.VIEW_HALF, Tuning.ARENA.end - Tuning.VIEW_HALF)
	return Rect2(centre - Tuning.VIEW_HALF, Tuning.VIEW_HALF * 2)

## Places a wave of [{kind, angle}] on a ring around the courier and returns the spawned enemies. A spawn
## always lands off-screen: near a wall or in a corner the ring point can fall inside the view, so its angle is
## re-rolled (seeded rng) a few times, then it falls back to the widest strip of arena outside the view.
func spawn_wave(spawns: Array) -> Array:
	var out := []
	var keep_out: Rect2 = view_rect().grow(Tuning.SPAWN_MARGIN)
	var inner: Rect2 = Tuning.ARENA.grow(-8)
	for s in spawns:
		var angle: float = s["angle"]
		var at := _ring_point(angle, inner)
		var tries := 0
		while keep_out.has_point(at) and tries < 6:
			angle = rng.randf() * TAU
			at = _ring_point(angle, inner)
			tries += 1
		if keep_out.has_point(at):
			at = _outside_view(keep_out, inner)
		var e = spawn_enemy(s["kind"], at)
		if e:
			out.append(e)
	return out

func _ring_point(angle: float, inner: Rect2) -> Vector2:
	return (player.position + Vector2.from_angle(angle) * Tuning.SPAWN_DISTANCE).clamp(inner.position, inner.end)

func _outside_view(keep_out: Rect2, inner: Rect2) -> Vector2:
	var strips := [
		Rect2(inner.position, Vector2(keep_out.position.x - inner.position.x, inner.size.y)),
		Rect2(Vector2(keep_out.end.x, inner.position.y), Vector2(inner.end.x - keep_out.end.x, inner.size.y)),
		Rect2(inner.position, Vector2(inner.size.x, keep_out.position.y - inner.position.y)),
		Rect2(Vector2(inner.position.x, keep_out.end.y), Vector2(inner.size.x, inner.end.y - keep_out.end.y)),
	]
	var best: Rect2 = strips[0]
	for strip in strips:
		if strip.get_area() > best.get_area():
			best = strip
	return Vector2(rng.randf_range(best.position.x, best.end.x), rng.randf_range(best.position.y, best.end.y))

func spawn_enemy(kind: String, at: Vector2) -> Node2D:
	if enemies.size() >= Tuning.MAX_ENEMIES:
		return null
	var e = EnemyScript.new()
	e.setup(kind, at)
	e.hp *= hp_scale()
	actors.add_child(e)
	enemies.append(e)
	return e

func drop_gem(at: Vector2, value: int) -> Node2D:
	var g = GemScript.new()
	g.setup(at, value)
	actors.add_child(g)
	gems.append(g)
	return g

## Later monsters are tougher in proportion to the whole minutes survived (x1.5 from 1:00, x2 from 2:00, x2.5 at 3:00).
## Stepped, not continuous: a continuous curve made every moth need two Beam hits from the first second.
func hp_scale() -> float:
	return 1.0 + Tuning.ENEMY_HP_GROWTH_PER_MINUTE * floorf(float(tick_count) / Tuning.TICK_HZ / 60.0)

func weapon_damage(base: float) -> float:
	return base * prog.damage_mult()

func beam_cooldown() -> int:
	return maxi(4, roundi(prog.beam_cooldown_ticks / prog.attack_rate_mult()))

func damage(e, amount: float) -> void:
	if e.dead:
		return
	e.hp -= amount
	e.flash = 3
	if e.hp <= 0:
		e.dead = true
		kills += 1
		enemies.erase(e)
		orbit_hit.erase(e.get_instance_id())
		enemy_killed.emit(e.position)
		drop_gem(e.position, e.xp)
		e.queue_free()

## Beam target: the nearest living enemy; with none on screen, the last movement direction.
func aim_dir() -> Vector2:
	var best = null
	var best_d := INF
	for e in enemies:
		var d: float = e.position.distance_squared_to(player.position)
		if d < best_d:
			best_d = d
			best = e
	if best == null or best_d < 0.01:
		return last_dir
	return (best.position - player.position).normalized()

func orbit_positions() -> Array[Vector2]:
	var out: Array[Vector2] = []
	if prog == null or prog.evolved_sunflare or prog.moth_count == 0:
		return out
	for i in prog.moth_count:
		out.append(player.position + Vector2.from_angle(orbit_angle + TAU * i / prog.moth_count) * prog.moth_radius)
	return out

func _step_weapons() -> void:
	if prog.evolved_sunflare:
		sunflare_timer -= 1
		if sunflare_timer <= 0:
			sunflare_timer = roundi(Tuning.SUNFLARE_PERIOD / prog.attack_rate_mult())
			sunflare_ring = Tuning.SUNFLARE_RING_TICKS
			player.cast_ticks = 12
			for e in enemies.duplicate():
				if e.position.distance_to(player.position) <= Tuning.SUNFLARE_RADIUS:
					damage(e, weapon_damage(Tuning.SUNFLARE_DAMAGE))
		if sunflare_ring > 0:
			sunflare_ring -= 1
		return
	beam_timer -= 1
	if beam_timer <= 0:
		beam_timer = beam_cooldown()
		var s = BeamShot.new()
		s.setup(player.position, aim_dir(), prog.beam_pierce)
		actors.add_child(s)
		shots.append(s)
		player.cast_ticks = Tuning.CAST_POSE_TICKS
	for s in shots.duplicate():
		s.step()
		for e in enemies.duplicate():
			if e.dead or s.hit_ids.has(e.get_instance_id()):
				continue
			if e.touches_segment(s.position - s.dir * Tuning.BEAM_HALF_LENGTH, s.position + s.dir * Tuning.BEAM_HALF_LENGTH, Tuning.BEAM_HALF_WIDTH):
				s.hit_ids[e.get_instance_id()] = true
				damage(e, weapon_damage(Tuning.BEAM_DAMAGE))
				s.pierce -= 1
				if s.pierce <= 0:
					s.dead = true
					break
		if s.dead or s.life <= 0:
			shots.erase(s)
			s.queue_free()
	if prog.moth_count > 0:
		orbit_angle += Tuning.MOTH_SPIN * prog.attack_rate_mult() / Tuning.TICK_HZ
		var moths := orbit_positions()
		for e in enemies.duplicate():
			var id: int = e.get_instance_id()
			if tick_count - int(orbit_hit.get(id, -9999)) < roundi(Tuning.MOTH_HIT_COOLDOWN / prog.attack_rate_mult()):
				continue
			for p in moths:
				if e.touches(p, Tuning.MOTH_HIT_RADIUS):
					orbit_hit[id] = tick_count
					damage(e, weapon_damage(Tuning.MOTH_DAMAGE))
					break

func _step_enemies() -> void:
	for e in enemies.duplicate():
		if state.current != GameState.PLAYING:
			return
		if e.dead:
			continue
		e.step(player.position)
		if e.position.distance_to(player.position) < e.radius + Tuning.PLAYER_RADIUS:
			player.take_hit(e.position, e.damage)

func _step_gems() -> void:
	var magnet: float = Tuning.PICKUP_RADIUS + int(prog.passive["magnet"]) * Tuning.PICKUP_RADIUS_PER_LEVEL
	for g in gems.duplicate():
		if g.step(player.position, magnet):
			gems.erase(g)
			g.queue_free()
			prog.add_xp(g.value)
			gem_collected.emit(g.value)

func choose_card(index: int) -> bool:
	if state.current != GameState.LEVELUP or index < 0 or index >= offered.size():
		return false
	var card: String = offered[index]
	prog.apply(card)
	prog.pending_levelups -= 1
	player.set_override("")
	match card:
		"heal":
			player.hp = mini(player.max_hp, player.hp + Tuning.HEAL_AMOUNT)
		"pass_speed":
			player.speed = Tuning.PLAYER_SPEED + int(prog.passive["speed"]) * Tuning.SPEED_PER_LEVEL
		"pass_hp":
			player.max_hp += Tuning.HP_PER_LEVEL
			player.hp += Tuning.HP_PER_LEVEL
		"sunflare":
			_evolve()
	offered = []
	state.go(GameState.PLAYING)
	return true

func _evolve() -> void:
	for s in shots:
		s.queue_free()
	shots.clear()
	sunflare_timer = Tuning.SUNFLARE_FIRST_DELAY
	player.empowered = true
	player.set_override("sunflare")
	pose_override_ticks = Tuning.EVOLVE_POSE_TICKS
	banner_ticks = Tuning.BANNER_TICKS
	evolved.emit()

func toggle_pause() -> void:
	if state.current == GameState.PLAYING:
		state.go(GameState.PAUSED)
	elif state.current == GameState.PAUSED:
		state.go(GameState.PLAYING)

func _on_player_died() -> void:
	player.set_override("defeat")
	state.go(GameState.LOST)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("start") and state.current == GameState.MENU:
		start_run()
	elif event.is_action_pressed("restart") and state.current != GameState.MENU:
		start_run()
	elif event.is_action_pressed("pause"):
		toggle_pause()
	elif event.is_action_pressed("mute_all"):
		audio.toggle_bus("Master")
	elif event.is_action_pressed("mute_music"):
		audio.toggle_bus("Music")
	elif event.is_action_pressed("mute_sfx"):
		audio.toggle_bus("SFX")
	elif event.is_action_pressed("debug_collision"):
		player.show_collision = not player.show_collision
		player.queue_redraw()
	elif state.current == GameState.LEVELUP:
		for i in 3:
			if event.is_action_pressed("card_%d" % (i + 1)):
				choose_card(i)
				return
		if event.is_action_pressed("ui_left"):
			hud.move_card(-1)
		elif event.is_action_pressed("ui_right"):
			hud.move_card(1)
		elif event.is_action_pressed("ui_accept"):
			choose_card(hud.card_cursor)

func _ensure_inputs() -> void:
	if InputMap.has_action("move_left"):
		return
	var keys := {
		"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT],
		"move_up": [KEY_W, KEY_UP], "move_down": [KEY_S, KEY_DOWN],
		"start": [KEY_ENTER, KEY_SPACE], "restart": [KEY_R], "pause": [KEY_ESCAPE, KEY_P],
		"mute_all": [KEY_M], "mute_music": [KEY_9], "mute_sfx": [KEY_0],
		"card_1": [KEY_1], "card_2": [KEY_2], "card_3": [KEY_3], "debug_collision": [KEY_F3],
	}
	for action in keys:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action, 0.2)
		for k in keys[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)
	var axes := {"move_left": [JOY_AXIS_LEFT_X, -1.0], "move_right": [JOY_AXIS_LEFT_X, 1.0], "move_up": [JOY_AXIS_LEFT_Y, -1.0], "move_down": [JOY_AXIS_LEFT_Y, 1.0]}
	for action in axes:
		var m := InputEventJoypadMotion.new()
		m.axis = axes[action][0]
		m.axis_value = axes[action][1]
		InputMap.action_add_event(action, m)
	var buttons := {"start": JOY_BUTTON_A, "pause": JOY_BUTTON_START, "restart": JOY_BUTTON_Y}
	for action in buttons:
		var b := InputEventJoypadButton.new()
		b.button_index = buttons[action]
		InputMap.action_add_event(action, b)
