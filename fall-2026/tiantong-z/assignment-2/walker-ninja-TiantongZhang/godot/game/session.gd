extends Node2D

const Player = preload("res://features/player/player.gd")
const Hud = preload("res://ui/hud.gd")
enum State { MENU, PLAYING, PAUSED, DYING, COMPLETE }
var state: State = State.MENU
var player: CharacterBody2D
var camera: Camera2D
var hud: Control
var level: Dictionary
var hazard_areas: Array[Area2D] = []
var goal: Area2D
var deaths: int = 0
var elapsed: float = 0.0
var retry_remaining: float = 0.0
var death_reason: String = ""
var last_finish_time: float = 0.0
var test_mode: bool = false
var contact_settle_ticks: int = 0
# Death reaction (CHANGE-BRIEF revision 0.4.0). The overlay's lifetime is
# derived from the laugh's own length rather than a hand-set timer, so the
# image cannot outlive or undercut the sound.
# Pop-up traps (CHANGE-BRIEF revision 0.5.0). Spikes rise by MOVING their
# Area2D from buried to exposed, which makes the lethal part exactly the
# visible part without rebuilding any collision polygon: a grounded player
# occupies y 292..320, so anything below y=320 cannot reach them, and anything
# above it is the part the ground does not cover.
const SPIKE_PITCH := 8.0
const TRAP_RISE_TICKS := 15
var trap_areas: Array[Area2D] = []
var trap_rects: Array[Rect2] = []
var trap_triggers: Array[float] = []
var trap_risen: Array[int] = []
var laugh: AudioStreamPlayer
var death_fx_remaining: float = 0.0
# C4/C6 (CHANGE-BRIEF revision 2.1.0).
const MUSIC_BUS := "Music"
var music: AudioStreamPlayer
var muted: bool = false
# C5 (CHANGE-BRIEF revision 2.4.0). Four effects on their own bus, and a log of
# WHEN each fired. The log is what makes the trap's timing assertable: the
# assignment's fairness argument is that the warning arrives before the hazard
# can kill, and "a sound played at some point during the death" would pass a
# test while being useless to the player.
const SFX_BUS := "Sfx"
var sfx: Dictionary = {}
var sfx_log: Array = []
var frame_tick: int = 0
var last_jumps: int = 0
var last_attacks: int = 0
var death_fx_total: float = 0.0
var cat_texture: Texture2D

func _ready() -> void:
	process_physics_priority = 10
	level = JSON.parse_string(FileAccess.get_file_as_string("res://levels/first_steps.json"))
	_setup_input()
	for entry in level.solids:
		_add_solid(Rect2(entry[0], entry[1], entry[2], entry[3]))
	_add_solid(Rect2(-32, 0, 32, 430))
	_add_solid(Rect2(level.width, 0, 32, 430))
	for entry in level.hazards:
		hazard_areas.append(_add_area(Rect2(entry[0], entry[1], entry[2], entry[3]), 8, true))
	for entry in level.get("traps", []):
		var trap_rect := Rect2(entry.spike[0], entry.spike[1], entry.spike[2], entry.spike[3])
		var trap := _add_area(trap_rect, 8, true)
		trap_areas.append(trap)
		trap_rects.append(trap_rect)
		trap_triggers.append(float(entry.trigger_x))
		trap_risen.append(0)
		# Layer 4 (Hazard), same as the starter's spike, so traps join the
		# existing overlap loop and add no new death path.
		hazard_areas.append(trap)
	reset_traps()
	for entry in level.get("enemies", []):
		var kind: String = entry.get("kind", "slime")
		var anchor_pos := Vector2(entry.spawn[0], entry.spawn[1])
		enemy_areas.append(_add_enemy(kind, anchor_pos))
		enemy_kinds.append(kind)
		enemy_anchor.append(anchor_pos)
		enemy_from.append(float(entry.from))
		enemy_to.append(float(entry.to))
		enemy_start_dir.append(float(entry.dir))
		enemy_dir.append(float(entry.dir))
		enemy_x.append(anchor_pos.x)
		enemy_alive.append(true)
	reset_enemies()
	var f: Array = level.finish
	goal = _add_area(Rect2(f[0], f[1], f[2], f[3]), 16, false)
	player = Player.new()
	add_child(player)
	player.reset_at(Vector2(level.spawn[0], level.spawn[1]))
	camera = Camera2D.new()
	camera.position = Vector2(320, 180)
	add_child(camera)
	var layer := CanvasLayer.new()
	add_child(layer)
	hud = Hud.new()
	hud.game = self
	layer.add_child(hud)
	# Loaded straight off disk rather than through Godot's import pipeline.
	# `.godot/` is a generated cache and is not committed, and a
	# `--headless --script` run does not rescan the filesystem, so `load()` on
	# an unimported asset fails in exactly the situation the assignment asks
	# us to verify: a fresh checkout. Reading the files directly means the two
	# assets work with no import step at all.
	laugh = AudioStreamPlayer.new()
	laugh.name = "DeathLaugh"
	laugh.stream = AudioStreamOggVorbis.load_from_file(
		ProjectSettings.globalize_path("res://assets/death-laugh.ogg"))
	add_child(laugh)
	death_fx_total = laugh.stream.get_length() if laugh.stream else 0.0
	# C4. A dedicated bus, not the master: the music has to be duckable and
	# balanceable against the sound effects without touching them, and the
	# `[TZ DECIDE] #3` question about the 0.55 s retry is a bus-level answer.
	if AudioServer.get_bus_index(MUSIC_BUS) < 0:
		AudioServer.add_bus(1)
		AudioServer.set_bus_name(1, MUSIC_BUS)
	music = AudioStreamPlayer.new()
	music.name = "Music"
	music.bus = MUSIC_BUS
	# -3 dB of headroom for the effects to land in. See the limiter note above.
	music.volume_db = -3.0
	var music_stream := AudioStreamOggVorbis.load_from_file(
		ProjectSettings.globalize_path("res://assets/music-loop.ogg"))
	if music_stream:
		# The file is already an exact 16-bar loop with a 20 ms crossfade at
		# the wrap (ASSET-LOG 2026-10-04); this flag is what makes the engine
		# wrap it rather than stop.
		music_stream.loop = true
		music.stream = music_stream
	add_child(music)
	# C5. A second bus, so the effects can be balanced against the music without
	# touching either one's own level, and so the masking question from CONCEPT
	# revision 1.1 is one slider rather than four.
	if AudioServer.get_bus_index(SFX_BUS) < 0:
		AudioServer.add_bus(2)
		AudioServer.set_bus_name(2, SFX_BUS)
	# A limiter on MASTER, because two sources at 0 dB clip.
	#
	# Measured: the music loop peaks at 0.702 and SFX-TRAP at 0.810 after its
	# trim, so if those peaks land on the same sample the sum is 1.512 -- half
	# again over full scale. Pulling the music down does not fix it: even at
	# -9 dB the bound is still 1.059, and a -9 dB bed is not the "music supplies
	# the pressure" of CONCEPT revision 1.1. So the music keeps a modest -3 dB
	# of headroom and the rare alignment is caught here instead of being traded
	# for a quiet score.
	#
	# Found while building an offline mix of the trap over the music to run the
	# masking check -- the render clipped at 1.172. Playing the game would not
	# have shown it: a few clipped samples inside a 0.26 s sweep are not
	# something an ear reliably catches, and nothing in the suite was listening.
	var master := AudioServer.get_bus_index("Master")
	var has_limiter := false
	for i in range(AudioServer.get_bus_effect_count(master)):
		if AudioServer.get_bus_effect(master, i) is AudioEffectHardLimiter:
			has_limiter = true
	if not has_limiter:
		var lim := AudioEffectHardLimiter.new()
		lim.ceiling_db = -0.5
		AudioServer.add_bus_effect(master, lim)
	# Per-sound trim in dB. The trap is loudest on purpose: it is the only one
	# of the four that has to be HEARD rather than merely noticed, because the
	# player is supposed to act on it.
	var sfx_files := {"jump": -7.0, "slash": -5.0, "trap": 0.0, "death": -2.0}
	for id in sfx_files:
		var pl := AudioStreamPlayer.new()
		pl.name = "Sfx_" + str(id)
		pl.bus = SFX_BUS
		pl.volume_db = sfx_files[id]
		pl.stream = AudioStreamOggVorbis.load_from_file(
			ProjectSettings.globalize_path("res://assets/sfx-%s.ogg" % id))
		add_child(pl)
		sfx[id] = pl
	var cat_image := Image.load_from_file(
		ProjectSettings.globalize_path("res://assets/death-laugh-cat.png"))
	cat_texture = ImageTexture.create_from_image(cat_image) if cat_image else null
	get_window().focus_exited.connect(_on_focus_lost)
	queue_redraw()

func _setup_input() -> void:
	var actions := {"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT], "jump": [KEY_SPACE], "pause": [KEY_ESCAPE, KEY_P], "restart": [KEY_R], "confirm": [KEY_ENTER], "menu": [KEY_M], "dash": [KEY_SHIFT], "mute": [KEY_0]}
	for action in actions:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action)
		for key in actions[action]:
			var event := InputEventKey.new()
			event.physical_keycode = key
			InputMap.action_add_event(action, event)
	# D3 — the swing is a mouse button, so it needs an InputEventMouseButton
	# rather than a key event. Left click already drives the HUD start button
	# in _unhandled_input; that stays safe because the player is disabled in
	# every state where the button is live, and test_keyboard.gd asserts it.
	if not InputMap.has_action("attack"):
		InputMap.add_action("attack")
		var click := InputEventMouseButton.new()
		click.button_index = MOUSE_BUTTON_LEFT
		InputMap.action_add_event("attack", click)

func _add_solid(rect: Rect2) -> void:
	var body := StaticBody2D.new()
	body.position = rect.position + rect.size / 2
	body.collision_layer = 1
	body.collision_mask = 2
	var shape := RectangleShape2D.new()
	shape.size = rect.size
	var collision := CollisionShape2D.new()
	collision.shape = shape
	body.add_child(collision)
	add_child(body)

static func spike_count(rect: Rect2) -> int:
	return maxi(1, int(rect.size.x / SPIKE_PITCH))

## How far below its risen position trap `i` currently sits. 0 = fully up.
func _trap_rise_offset(i: int) -> float:
	var t := float(trap_risen[i]) / float(TRAP_RISE_TICKS)
	return trap_rects[i].size.y * (1.0 - t)

## A blind arch set into the wall. Drawn at the x positions the cream
## backdrop used for hills, so `level.hills` keeps its meaning and its data.
func _draw_alcove(cx: float) -> void:
	var half := 28.0
	var top := 150.0
	# Drawn twice: once 2 px larger in a lighter stone, then the recess on top.
	# The 2 px that survive are the arch's own masonry edge, which is what makes
	# it read as cut into the wall rather than as a dark blob on it.
	for pass_i in range(2):
		var grow: float = 2.0 if pass_i == 0 else 0.0
		var pts := PackedVector2Array()
		pts.append(Vector2(cx - half - grow, 320.0))
		var steps := 14
		for i in range(steps + 1):
			var a: float = PI - PI * float(i) / float(steps)
			pts.append(Vector2(cx + cos(a) * (half + grow), top + half - sin(a) * (half + grow)))
		pts.append(Vector2(cx + half + grow, 320.0))
		draw_colored_polygon(pts, Color("352c40") if pass_i == 0 else Color("241e2c"))

## A wall torch: four nested translucent discs for the pool, then the bracket
## and the flame. Static on purpose -- see the note at the call site.
func _draw_torch(cx: float, cy: float) -> void:
	# 16 nested discs rather than 4: at four the rings were visible as banding
	# in the rendered frame, which a screenshot caught and the code did not.
	for i in range(16):
		draw_circle(Vector2(cx, cy), 60.0 - float(i) * 3.6, Color(1.0, 0.60, 0.24, 0.018))
	draw_rect(Rect2(cx - 1.0, cy, 2.0, 10.0), Color("3a2f26"))
	draw_colored_polygon(PackedVector2Array([
		Vector2(cx - 3.0, cy + 1.0), Vector2(cx, cy - 7.0), Vector2(cx + 3.0, cy + 1.0)]),
		Color("ff9a3c"))
	draw_colored_polygon(PackedVector2Array([
		Vector2(cx - 1.5, cy), Vector2(cx, cy - 4.0), Vector2(cx + 1.5, cy)]),
		Color("ffe08a"))

func _draw_spikes(rect: Rect2, rise_offset: float) -> void:
	# Count, pitch, base and tip all come from the rect, so what is drawn and
	# what kills are derived from the same numbers (P12).
	var base := rect.end.y + rise_offset
	var tip := rect.position.y + rise_offset
	for i in range(spike_count(rect)):
		var x := rect.position.x + float(i) * SPIKE_PITCH
		draw_colored_polygon(PackedVector2Array([
			Vector2(x, base), Vector2(x + 4.0, tip), Vector2(x + 8.0, base)]), Color("d24e42"))

func reset_traps() -> void:
	for i in range(trap_areas.size()):
		trap_risen[i] = 0
		trap_areas[i].position = trap_rects[i].position + Vector2(0.0, _trap_rise_offset(i))
	queue_redraw()

## One-way: once a trap has started rising it finishes and never retracts, so
## the same inputs always produce the same attempt.
func advance_traps() -> void:
	var moved := false
	for i in range(trap_areas.size()):
		if trap_risen[i] == 0 and player.position.x < trap_triggers[i]:
			continue
		if trap_risen[i] < TRAP_RISE_TICKS:
			# C5. The warning fires on the tick the spike STARTS to rise -- the
			# tick trap_risen leaves 0 -- not on the contact. Hung off the
			# damage instead it would be a death sound arriving after the
			# information is useless, and it would still pass a test that only
			# asserted "a sound played when the trap killed me".
			if trap_risen[i] == 0:
				play_sfx("trap")
			trap_risen[i] += 1
			moved = true
		trap_areas[i].position = trap_rects[i].position + Vector2(0.0, _trap_rise_offset(i))
	if moved:
		# The starter drew the level exactly once, from _ready(), because it was
		# static; only the HUD and the player redraw per frame. Rising traps
		# break that assumption, and without this the spike becomes lethal while
		# still painted underground — the player dies to thin air, which is the
		# single thing this design must not do. Found by playtest, not by any of
		# the 69 checks, because none of them looked at what was drawn.
		queue_redraw()

## Enemies (CHANGE-BRIEF revision 0.6.0). Two kinds, one behaviour: patrol
## between fixed bounds from the level data at a fixed speed, turn at the
## bounds, never chase, never randomise. Slimes hold platforms; horses hold the
## gaps and ignore gravity.
##
## ONE Area2D per enemy does both jobs P17 is about: collision_layer 4 is
## layer 3 (Enemy), which is what the swing hitbox masks, and collision_mask 2
## is layer 2 (Player), which is what lets overlaps_body() see the player. A
## second area would only have created a way for the two to disagree.
const ENEMY_SPEED := 60.0
const SLIME_SIZE := Vector2(22.0, 16.0)
const HORSE_SIZE := Vector2(26.0, 18.0)
var enemy_areas: Array[Area2D] = []
var enemy_kinds: Array[String] = []
var enemy_anchor: Array[Vector2] = []
var enemy_from: Array[float] = []
var enemy_to: Array[float] = []
var enemy_dir: Array[float] = []
var enemy_x: Array[float] = []
var enemy_alive: Array[bool] = []
var enemy_start_dir: Array[float] = []
var enemy_anim: float = 0.0
var enemies_killed: int = 0

static func enemy_size(kind: String) -> Vector2:
	return HORSE_SIZE if kind == "horse" else SLIME_SIZE

func _add_enemy(kind: String, anchor: Vector2) -> Area2D:
	var size := enemy_size(kind)
	var area := Area2D.new()
	area.name = "Enemy_" + kind + "_" + str(enemy_areas.size())
	area.collision_layer = 4
	area.collision_mask = 2
	var shape := RectangleShape2D.new()
	shape.size = size
	var collision := CollisionShape2D.new()
	collision.shape = shape
	# The anchor is bottom-centre, matching the level data's spawn, so a slime's
	# spawn y is the platform surface it stands on.
	collision.position = Vector2(0.0, -size.y / 2.0)
	area.add_child(collision)
	area.position = anchor
	add_child(area)
	return area

func reset_enemies() -> void:
	for i in range(enemy_areas.size()):
		enemy_alive[i] = true
		enemy_x[i] = enemy_anchor[i].x
		enemy_dir[i] = enemy_start_dir[i]
		enemy_areas[i].position = enemy_anchor[i]
		enemy_areas[i].monitoring = true
		enemy_areas[i].monitorable = true
	enemies_killed = 0
	enemy_anim = 0.0
	queue_redraw()

func advance_enemies(delta: float) -> void:
	enemy_anim += delta
	var moved := false
	for i in range(enemy_areas.size()):
		if not enemy_alive[i]:
			continue
		enemy_x[i] += enemy_dir[i] * ENEMY_SPEED * delta
		if enemy_x[i] <= enemy_from[i]:
			enemy_x[i] = enemy_from[i]
			enemy_dir[i] = 1.0
		elif enemy_x[i] >= enemy_to[i]:
			enemy_x[i] = enemy_to[i]
			enemy_dir[i] = -1.0
		# y is taken from the anchor every frame, so a horse cannot be pulled
		# down by anything (P20).
		enemy_areas[i].position = Vector2(enemy_x[i], enemy_anchor[i].y)
		moved = true
	if moved:
		# Enemies move EVERY frame, not on a state change. Revision 0.5.1 shipped
		# traps that were lethal while drawn underground for exactly this reason
		# (P16).
		queue_redraw()

## Exact segment-vs-rect test, expanded by the blade's half-thickness.
static func segment_hits_rect(a: Vector2, b: Vector2, box: Rect2) -> bool:
	if box.has_point(a) or box.has_point(b):
		return true
	var d := b - a
	var t0 := 0.0
	var t1 := 1.0
	for axis in 2:
		var origin: float = a[axis]
		var delta: float = d[axis]
		var lo: float = box.position[axis]
		var hi: float = box.end[axis]
		if absf(delta) < 0.00001:
			if origin < lo or origin > hi:
				return false
			continue
		var near := (lo - origin) / delta
		var far := (hi - origin) / delta
		if near > far:
			var swap := near
			near = far
			far = swap
		t0 = maxf(t0, near)
		t1 = minf(t1, far)
		if t0 > t1:
			return false
	return true

## One slash kills. Returns true if anything died this tick.
##
## The hit is computed from the blade's own geometry rather than from
## Area2D.overlaps_area(). That query reports the previous physics step, and the
## only active tick whose angle brings the blade down to a ground-level enemy is
## the LAST one - monitoring is already off by the step that could report it, so
## a geometrically certain hit was never observable. Deriving the kill from the
## same pivot, angle and reach the drawing uses removes the frame lag entirely
## and keeps "what you see is what kills" exact.
func resolve_slash() -> bool:
	if player.attack_phase() != 2:
		return false
	var seg: PackedVector2Array = player.attack_segment()
	var half: float = player.attack_shape.shape.size.y * 0.5
	var killed := false
	for i in range(enemy_areas.size()):
		if not enemy_alive[i]:
			continue
		var size := enemy_size(enemy_kinds[i])
		var box := Rect2(
			enemy_x[i] - size.x * 0.5 - half,
			enemy_anchor[i].y - size.y - half,
			size.x + half * 2.0,
			size.y + half * 2.0)
		if segment_hits_rect(seg[0], seg[1], box):
			enemy_alive[i] = false
			enemy_areas[i].monitoring = false
			enemy_areas[i].monitorable = false
			enemies_killed += 1
			killed = true
	if killed:
		queue_redraw()
	return killed

func enemy_touching_player() -> bool:
	for i in range(enemy_areas.size()):
		if enemy_alive[i] and enemy_areas[i].overlaps_body(player):
			return true
	return false

## Points are written facing right and mirrored for dir < 0, the same way the
## player's own art is drawn.
func _epoly(at: Vector2, dir: float, pts: Array, c: Color) -> void:
	var out := PackedVector2Array()
	if dir >= 0.0:
		for p in pts:
			out.append(at + Vector2(p[0], p[1]))
	else:
		for i in range(pts.size() - 1, -1, -1):
			out.append(at + Vector2(-pts[i][0], pts[i][1]))
	draw_colored_polygon(out, c)

func _draw_slime(at: Vector2, dir: float, phase: float) -> void:
	# Squash and stretch: wider and flatter at the extremes of the cycle. This
	# is the whole motion language of a slime, so it is worth the two lines.
	var squash := sin(phase * 6.0) * 1.6
	var half := SLIME_SIZE.x * 0.5 + squash
	var high := SLIME_SIZE.y - squash * 0.7
	var body := Color("7ab648")
	var shade := Color("55913a")
	var dome := PackedVector2Array()
	var steps := 14
	for i in range(steps + 1):
		var th := PI * float(i) / float(steps)
		dome.append(at + Vector2(cos(th) * half, -sin(th) * high))
	draw_colored_polygon(dome, body)
	# A darker base band reads as weight without needing a gradient.
	draw_rect(Rect2(at.x - half * 0.86, at.y - 3.0, half * 1.72, 3.0), shade)
	var eye := 4.0 * dir
	draw_rect(Rect2(at.x + eye - 3.0, at.y - high * 0.72, 2.0, 3.0), Color("17300d"))
	draw_rect(Rect2(at.x + eye + 1.0, at.y - high * 0.72, 2.0, 3.0), Color("17300d"))

func _draw_horse(at: Vector2, dir: float, phase: float) -> void:
	# The first version packed a body, neck, head, tail, wings and four legs
	# into 26x18 and read as a purple lump. This one keeps the SAME 26x18
	# collider and spends the drawing on the three things that actually carry a
	# horse silhouette at this size: a long level back, a raised head on a
	# clear neck, and wings big enough to see. The wings and the tail reach
	# outside the collider, like the player's own scarf and blade, and that
	# overhang is measured in CHANGE-BRIEF 0.6.0.
	var flap := sin(phase * 9.0) * 4.5
	var body := Color("965aa0")
	var shade := Color("6d3f76")
	var wing := Color("c9a6d0")
	var mane := Color("4d2b55")
	# Far wing, behind the body.
	_epoly(at, dir, [[-4.0, -12.0], [-19.0, -21.0 - flap], [-6.0, -24.0 - flap * 0.5], [3.0, -14.0]], shade)
	# Tail streaming back.
	_epoly(at, dir, [[-10.0, -13.0], [-22.0, -18.0 + flap * 0.6], [-20.0, -6.0], [-10.0, -8.0]], mane)
	# Back and barrel: one long horizontal mass is what reads as "horse".
	_epoly(at, dir, [[-11.0, -14.0], [7.0, -15.0], [11.0, -10.0], [8.0, -4.0], [-9.0, -5.0]], body)
	# Neck, rising forward, then the head with a muzzle.
	_epoly(at, dir, [[4.0, -14.0], [10.0, -24.0], [15.0, -23.0], [12.0, -12.0], [6.0, -10.0]], body)
	_epoly(at, dir, [[10.0, -26.0], [18.0, -25.0], [19.0, -20.0], [11.0, -21.0]], body)
	_epoly(at, dir, [[17.0, -25.0], [21.0, -24.0], [21.0, -20.0], [17.0, -20.0]], shade)
	# Mane along the neck, and two ears.
	_epoly(at, dir, [[5.0, -15.0], [10.0, -25.0], [13.0, -25.0], [8.0, -14.0]], mane)
	_epoly(at, dir, [[11.0, -26.0], [12.0, -30.0], [14.0, -26.0]], mane)
	# Legs tucked, front pair forward.
	_epoly(at, dir, [[4.0, -5.0], [8.0, -5.0], [7.0, 1.0], [3.0, 0.0]], shade)
	_epoly(at, dir, [[-6.0, -5.0], [-2.0, -5.0], [-3.0, 1.0], [-7.0, 0.0]], shade)
	# Near wing, over the body, beating opposite the far one.
	_epoly(at, dir, [[-2.0, -13.0], [-16.0, -24.0 + flap], [-1.0, -27.0 + flap * 0.5], [6.0, -15.0]], wing)
	draw_rect(Rect2(at.x + (16.0 * dir) - 1.0, at.y - 24.0, 2.0, 2.0), Color("1d0d22"))

func _draw_enemies() -> void:
	for i in range(enemy_areas.size()):
		if not enemy_alive[i]:
			continue
		var at := Vector2(enemy_x[i], enemy_anchor[i].y)
		if enemy_kinds[i] == "horse":
			_draw_horse(at, enemy_dir[i], enemy_anim + float(i))
		else:
			_draw_slime(at, enemy_dir[i], enemy_anim + float(i))

func _add_area(rect: Rect2, layer: int, spikes: bool) -> Area2D:
	var area := Area2D.new()
	area.position = rect.position
	area.collision_layer = layer
	area.collision_mask = 2
	if spikes:
		# One exact triangular trigger silhouette per 8 px of width, derived from
		# the rect so these polygons and _draw_spikes() are the same shape by
		# construction. The starter hard-coded three of these AND three drawn
		# ones; for its 24 px rect both rules agree, but only one of them
		# generalises (CHANGE-BRIEF 0.5.0 P13). No oversized invisible box.
		for i in range(spike_count(rect)):
			var triangle := CollisionPolygon2D.new()
			var x := float(i) * SPIKE_PITCH
			triangle.polygon = PackedVector2Array([Vector2(x, rect.size.y), Vector2(x + 4, 0), Vector2(x + 8, rect.size.y)])
			area.add_child(triangle)
	else:
		var collision := CollisionShape2D.new()
		var shape := RectangleShape2D.new()
		shape.size = rect.size
		collision.shape = shape
		collision.position = rect.size / 2.0
		area.add_child(collision)
	add_child(area)
	return area

func stop_death_fx() -> void:
	death_fx_remaining = 0.0
	if laugh:
		laugh.stop()
		laugh.stream_paused = false

## Fire one effect and record the tick it fired on. The log is cleared per
## attempt, so it is bounded and so a test can read it without subtracting a
## previous life's events.
func play_sfx(id: String) -> void:
	sfx_log.append({"id": id, "tick": frame_tick})
	var pl = sfx.get(id)
	if pl and pl.stream:
		pl.play()

func stop_music() -> void:
	if music:
		music.stop()
		music.stream_paused = false

## C6. Master bus, not per-stream. Muting each stream individually leaves
## anything added later audible, which is the failure the brief predicted; a
## bus mute cannot be forgotten by a stream that did not exist when it was
## written.
func set_muted(value: bool) -> void:
	muted = value
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"), value)

func start_session() -> void:
	if state == State.PLAYING:
		return
	deaths = 0
	stop_death_fx()
	restart_attempt()

func restart_attempt() -> void:
	state = State.PLAYING
	elapsed = 0.0
	retry_remaining = 0.0
	# Area2D overlaps are physics-step snapshots. Discard pre-teleport contacts
	# until the broadphase has observed the reset, preventing a phantom second death.
	contact_settle_ticks = 2
	reset_traps()
	reset_enemies()
	player.reset_at(Vector2(level.spawn[0], level.spawn[1]))
	player.death_pose = false
	player.enabled = true
	sfx_log.clear()
	# Synced AFTER reset_at, so whether reset_at zeroes these counters or leaves
	# them running makes no difference here -- a question I would otherwise have
	# had to answer correctly twice.
	last_jumps = player.jumps
	last_attacks = player.attacks
	camera.position = Vector2(320, 180)
	# C4. restart_attempt() runs on EVERY death, so this guard is the whole
	# point of the line: a loop that jumps back to bar 1 every 0.55 s is worse
	# than no music at all. Retries leave the track running.
	if music and music.stream:
		if music.playing or music.stream_paused:
			# Already running, or frozen by a pause. Resume where it was.
			# `playing` reports FALSE while `stream_paused` is true, so testing
			# `playing` alone made R-while-paused restart the track at bar 1.
			music.stream_paused = false
		else:
			music.play()

func set_paused(value: bool) -> void:
	if laugh and (state == State.PLAYING or state == State.PAUSED):
		# Freeze the reaction with the game so the sound and the image stay in
		# step with the countdown that drives the overlay.
		laugh.stream_paused = value
	if music and (state == State.PLAYING or state == State.PAUSED):
		music.stream_paused = value
	if value and state == State.PLAYING:
		state = State.PAUSED
		player.enabled = false
	elif not value and state == State.PAUSED:
		state = State.PLAYING
		player.enabled = true
		player.require_jump_release = true
		player.jump_request_tick = -1000

func _on_focus_lost() -> void:
	if not test_mode:
		set_paused(true)

func resolve_contacts(fatal: bool, finished: bool) -> void:
	if state != State.PLAYING:
		return
	if fatal:
		state = State.DYING
		deaths += 1
		retry_remaining = 0.55
		player.enabled = false
		player.velocity = Vector2.ZERO
		# C3. Keyed off the session state, not off movement: a disabled body
		# keeps whatever `is_on_floor()` last returned, so a movement-derived
		# pose would differ depending on how the player died.
		player.death_pose = true
		play_sfx("death")
		# One reaction per death: the laugh restarts from the top and the
		# overlay lives exactly as long as the laugh. The 0.55 s retry is
		# unchanged, so the overlay outlasts the respawn on purpose.
		death_fx_remaining = death_fx_total
		if laugh:
			laugh.stream_paused = false
			laugh.play()
	elif finished:
		state = State.COMPLETE
		last_finish_time = elapsed
		stop_music()
		player.enabled = false
		player.velocity = Vector2.ZERO

func _physics_process(delta: float) -> void:
	frame_tick += 1
	if death_fx_remaining > 0.0 and state != State.PAUSED:
		death_fx_remaining = maxf(0.0, death_fx_remaining - delta)
	if state == State.DYING:
		retry_remaining -= delta
		if retry_remaining <= 0:
			restart_attempt()
	elif state == State.PLAYING:
		elapsed += delta
		# C5. The jump and the slash are read off the player's own counters
		# rather than fired from inside player.gd: the player stays pure
		# gameplay, and a counter that moved is a fact the test can check
		# against the same number.
		if player.jumps != last_jumps:
			last_jumps = player.jumps
			play_sfx("jump")
		if player.attacks != last_attacks:
			last_attacks = player.attacks
			play_sfx("slash")
		advance_traps()
		advance_enemies(delta)
		resolve_slash()
		var fell := player.position.y > float(level.fall_y)
		var fatal := fell
		for hazard in hazard_areas:
			fatal = fatal or hazard.overlaps_body(player)
		# Enemies feed the SAME fatal flag and the same resolve_contacts() call,
		# so the retry timing, the death reaction and the results screen are the
		# starter's, not a parallel path. Only the message is new.
		var touched := enemy_touching_player()
		fatal = fatal or touched
		death_reason = "Missed the landing" if fell else ("It got you" if touched else "Watch the spikes")
		if contact_settle_ticks > 0:
			contact_settle_ticks -= 1
		else:
			resolve_contacts(fatal, goal.overlaps_body(player))
		camera.position.x = clampf(player.position.x + 100, 320, float(level.width) - 320)
	if is_instance_valid(hud):
		hud.queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.echo:
		return
	if event.is_action_pressed("confirm"):
		if state in [State.MENU, State.COMPLETE]:
			start_session()
		elif state == State.PAUSED:
			set_paused(false)
	elif event.is_action_pressed("pause"):
		set_paused(state != State.PAUSED)
	elif event.is_action_pressed("restart") and state in [State.PLAYING, State.PAUSED, State.DYING]:
		restart_attempt()
	elif event.is_action_pressed("mute"):
		# Checked before the state branches on purpose: mute has to work on the
		# menu and the results screen too, not only mid-run.
		set_muted(not muted)
	elif event.is_action_pressed("menu") and state in [State.PAUSED, State.COMPLETE]:
		state = State.MENU
		player.enabled = false
		stop_death_fx()
		stop_music()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if Rect2(220, 215, 200, 34).has_point(hud.get_local_mouse_position()):
			if state in [State.MENU, State.COMPLETE]:
				start_session()
			elif state == State.PAUSED:
				set_paused(false)

func _draw() -> void:
	if level.is_empty():
		return
	var font := ThemeDB.fallback_font
	var ink := Color("25354a")
	# Anything that has to be legible AGAINST THE WALL is drawn in chalk, not
	# ink. Before revision 1.3 the backdrop was a cream sky and ink did both
	# jobs; in a dungeon ink against the wall is 1.43:1 and disappears.
	var chalk := Color("9aa7bd")
	# All visual assets are original Godot vector drawing, not recovered art.
	# Every extent below is derived from level.width, so widening the level in
	# the JSON no longer leaves the backdrop, grid or labels behind
	# (CHANGE-BRIEF 0.5.0).
	var width: float = level.width
	# --- Dungeon backdrop (CONCEPT revision 1.3) ---------------------------
	# The wall is deliberately the quietest surface on screen: mortar is
	# 1.18:1 against it and the alcoves 1.10:1. The strong contrast is spent
	# on what the player interacts with -- the lit platform edge at 6.96:1,
	# the spikes at 4.15:1 and the character's own light rim at 7.31:1.
	draw_rect(Rect2(-400, -200, width + 800.0, 900), Color("1b1620"))
	var mortar := Color("2b2430")
	var course := 0
	for y in range(96, 321, 32):
		draw_line(Vector2(0, y), Vector2(width, y), mortar, 1)
		# Staggered vertical joints, so the wall reads as masonry rather than
		# as the graph paper the cream version was.
		var off: int = 0 if course % 2 == 0 else 32
		for x in range(off, int(width) + 1, 64):
			draw_line(Vector2(x, y), Vector2(x, minf(float(y) + 32.0, 320.0)), mortar, 1)
		course += 1
	# The alcoves stand where the cream version's hills stood, so the level
	# file is unchanged: the same x values, a different thing drawn at them.
	for x in level.hills:
		_draw_alcove(float(x))
	# Torches are placed off a fixed stride rather than off elapsed time, and
	# they do NOT flicker. A flicker would make two renders of the same frame
	# differ, and the capture pipeline diffs frames pixel-exactly.
	for tx in range(120, int(width) + 1, 240):
		_draw_torch(float(tx), 150.0)
	# Hazards are drawn BEFORE the solids so a trap that is still rising has the
	# part still underground hidden by the ground it is rising through. The
	# original spike sits at y 304..320 and the ground at 320..384, so they do
	# not overlap and this reordering leaves it untouched — verified by a
	# pixel-exact diff of the captured frames, not by argument (P11).
	for entry in level.hazards:
		_draw_spikes(Rect2(entry[0], entry[1], entry[2], entry[3]), 0.0)
	for i in range(trap_rects.size()):
		_draw_spikes(trap_rects[i], _trap_rise_offset(i))
	for entry in level.solids:
		var r := Rect2(entry[0], entry[1], entry[2], entry[3])
		draw_rect(r, ink)
		# The lit top edge, warm against the cold stone body: 6.96:1 against
		# the wall and 4.88:1 against the platform it caps. In the dungeon the
		# floor is read from this 4 px strip, not from the body, which is only
		# 1.43:1 against the wall.
		draw_rect(Rect2(r.position, Vector2(r.size.x, 4)), Color("c89a5a"))
		# The hatch marks run from y+12 to y+19, so they need a block at least
		# 16 px tall. The starter's 16 px step already overhangs by 3 px onto the
		# dark ground beneath it, where it cannot be seen; the 8 px high-road
		# planks have open sky beneath them and would show the overhang.
		if r.size.y >= 16.0:
			for x in range(int(r.position.x)+12, int(r.end.x), 24):
				draw_line(Vector2(x, r.position.y+12), Vector2(x+7, r.position.y+19), Color("405166"), 1)
	_draw_enemies()
	var finish_x: float = level.finish[0]
	draw_line(Vector2(finish_x+3, 320), Vector2(finish_x+3, 250), chalk, 3)
	draw_colored_polygon(PackedVector2Array([Vector2(finish_x+5,250),Vector2(finish_x+32,260),Vector2(finish_x+5,274)]), Color("287c68"))
	for entry in level.labels:
		draw_string(font, Vector2(entry[0], entry[1]), entry[3], HORIZONTAL_ALIGNMENT_LEFT, -1, int(entry[2]), chalk)
