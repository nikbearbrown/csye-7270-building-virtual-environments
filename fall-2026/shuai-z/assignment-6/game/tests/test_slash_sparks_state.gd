extends Node
## Headless state checks for Effect A, the sword-swing sparks (CHANGE-BRIEF.md,
## section 2, rules A1–A5). Run from this folder:
##   scripts/run-test.sh test_slash_sparks_state.tscn 60
## It plays Main through the real game loop: every cut comes from the slash
## action, the sword from walking into the pickup, the pause from the pause
## action. It never calls the driver. The only game state it writes is Rudy's
## place, as checks.gd's _teleport does, to put him next to the pickup, a
## goblin or open ground.
## A recorder reads, each physics tick, the sword hitbox's disabled flag and
## every burst the driver adds to Effects/SlashBursts. This node runs before
## Main's nodes in each tick, so what it reads is the state at the end of the
## tick before: an edge it sees on tick N happened on tick N - 1.
## Headless, the dummy renderer draws nothing and runs no particle process, so
## these checks read node state only (CLAUDE.md, Headless facts).
## Prints one line per check and exits with code 1 if any check fails.

const MAIN := preload("res://app/main.tscn")


## One burst as the recorder saw it.
class Burst:
	var node: Node2D
	var born := -1 ## the tick the driver added it
	var exited := -1 ## the tick it left the tree
	var in_container := false ## its parent is Effects/SlashBursts, and no Rudy or goblin is its ancestor
	var sampled := false
	# Read on the tick after its birth, before anything else moves:
	var pos: Vector2
	var shape_pos: Vector2
	var x_axis_x := 0.0 ## global_transform.x.x: its mirror sign
	var facing := 0
	var others: Array[Dictionary] = [] ## every other live burst then: node, pos, emitting


var _failures := 0
var _main: Main
var _rudy: Rudy
var _box: CollisionShape2D
var _slash_bursts: Node2D
var _tick := 0
var _was_disabled := true
var _edges: Array[int] = [] ## ticks on which the hitbox went from disabled to live
var _bursts: Array[Burst] = []
var _max_alive := 0


func _ready() -> void:
	await _run_load()
	await _run_play()
	print("all checks passed" if _failures == 0 else "%d check(s) FAILED" % _failures)
	get_tree().quit(1 if _failures > 0 else 0)


func _physics_process(_delta: float) -> void:
	if not is_instance_valid(_rudy):
		return
	_tick += 1
	var disabled := _box.disabled
	if _was_disabled and not disabled:
		_edges.append(_tick - 1)
	_was_disabled = disabled
	for b in _bursts:
		if not b.sampled and is_instance_valid(b.node) and b.node.is_inside_tree():
			b.sampled = true
			b.pos = b.node.global_position
			b.shape_pos = _box.global_position
			b.x_axis_x = b.node.global_transform.x.x
			b.facing = _rudy.facing
			for other in _bursts:
				if other != b and is_instance_valid(other.node) and other.node.is_inside_tree():
					b.others.append({
						"node": other.node,
						"pos": other.node.global_position,
						"emitting": (other.node.get_node("Sparks") as GPUParticles2D).emitting,
					})
	_max_alive = maxi(_max_alive, _alive())


## A fresh level; without `with_title` it skips the title and starts in play.
func _start_level(with_title := false) -> void:
	Main.title_shown = not with_title
	_main = MAIN.instantiate()
	add_child(_main)
	_rudy = _main.get_node("Rudy")
	_box = _rudy.get_node("SwordHitbox/Shape")
	_slash_bursts = _main.get_node("Effects/SlashBursts")
	_slash_bursts.child_entered_tree.connect(_on_burst_entered)
	_was_disabled = _box.disabled


func _on_burst_entered(node: Node) -> void:
	var b := Burst.new()
	b.node = node
	b.born = _tick
	var ancestor_is_game := _rudy.is_ancestor_of(node)
	for goblin in _main.get_node("Level1/Enemies").get_children():
		ancestor_is_game = ancestor_is_game or goblin.is_ancestor_of(node)
	b.in_container = node.get_parent() == _slash_bursts and not ancestor_is_game
	node.tree_exited.connect(func() -> void: b.exited = _tick)
	_bursts.append(b)


## S1, S2: nothing fires on load or on the title.
func _run_load() -> void:
	_start_level(true)
	await _frames(60)
	await _tap(&"slash")
	await _frames(30)
	_check("S1 on load and on the title, with slash pressed there: no burst",
		_bursts.is_empty() and _main.state == Main.State.TITLE,
		"bursts %d, state %s" % [_bursts.size(), Main.State.keys()[_main.state]])
	_main.queue_free()
	await _frames(1)

	_start_level()
	await _frames(60)
	_check("S2 on load with the title skipped, after 60 ticks: no burst", _bursts.is_empty(),
		"bursts %d" % _bursts.size())


func _run_play() -> void:
	var level: Node2D = _main.get_node("Level1")
	var pickup: SwordPickup = level.get_node("SwordPickup")
	var goblin_a: Goblin = level.get_node("Enemies/GoblinA")
	var goblin_b: Goblin = level.get_node("Enemies/GoblinB")
	var ground_y := (level.get_node("StartPoint") as Marker2D).global_position.y

	# S3: slash without the sword.
	var n := _bursts.size()
	var e := _edges.size()
	await _tap(&"slash")
	await _frames(30)
	_check("S3 slash without the sword: no burst, no live edge",
		_bursts.size() == n and _edges.size() == e and _rudy.gear == Rudy.Gear.NONE,
		"bursts %d, edges %d" % [_bursts.size() - n, _edges.size() - e])

	# The sword, by walking into the pickup.
	_teleport(Vector2(pickup.global_position.x - 200.0, ground_y))
	await _frames(2)
	await _hold_until(&"move_right", func() -> bool: return _rudy.gear == Rudy.Gear.SWORD, 120)
	await _wait_until(func() -> bool: return _rudy.is_on_floor() and _rudy.velocity.x == 0.0, 60)

	# S4, S5: one cut facing right.
	n = _bursts.size()
	e = _edges.size()
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	await _frames(2)
	var new_bursts := _bursts.slice(n)
	var new_edges := _edges.slice(e)
	_check("S4 one cut: exactly one burst, born on the tick the hitbox went live",
		new_bursts.size() == 1 and new_edges.size() == 1 and new_bursts[0].born == new_edges[0],
		"bursts born on %s, edges on %s" % [_born_ticks(new_bursts), new_edges])
	if new_bursts.size() == 1:
		var b: Burst = new_bursts[0]
		_check("S5 facing right: the burst is on the hitbox within 1 px, and not mirrored",
			b.sampled and b.pos.distance_to(b.shape_pos) <= 1.0 and b.x_axis_x > 0.0 and b.facing == 1,
			"burst %s, hitbox %s, x.x %.2f, facing %d" % [b.pos, b.shape_pos, b.x_axis_x, b.facing])
	else:
		_check("S5 facing right: the burst is on the hitbox within 1 px, and not mirrored", false, "no single burst")

	# S6: turned on the spot, one cut facing left.
	await _tap(&"move_left")
	await _frames(2)
	n = _bursts.size()
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	await _frames(2)
	new_bursts = _bursts.slice(n)
	if new_bursts.size() == 1:
		var b: Burst = new_bursts[0]
		_check("S6 facing left: the burst is on the hitbox within 1 px, and mirrored",
			b.sampled and b.pos.distance_to(b.shape_pos) <= 1.0 and b.x_axis_x < 0.0 and b.facing == -1,
			"burst %s, hitbox %s, x.x %.2f, facing %d" % [b.pos, b.shape_pos, b.x_axis_x, b.facing])
	else:
		_check("S6 facing left: the burst is on the hitbox within 1 px, and mirrored", false,
			"%d bursts" % new_bursts.size())
	await _frames(40)

	# S7, S8: a second cut right after the first swing ends, inside the first burst's life.
	n = _bursts.size()
	e = _edges.size()
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	await _tap(&"slash")
	await _frames(45)
	new_bursts = _bursts.slice(n)
	new_edges = _edges.slice(e)
	if new_bursts.size() == 2 and new_edges.size() == 2:
		var first: Burst = new_bursts[0]
		var second: Burst = new_bursts[1]
		var seen: Dictionary = {}
		for other in second.others:
			if other.node == first.node:
				seen = other
		_check("S7 two cuts %d ticks apart: two bursts alive at the second cut; the first is the same node, not moved, still emitting"
				% (new_edges[1] - new_edges[0]),
			second.born == new_edges[1] and second.others.size() == 1 and not seen.is_empty()
			and (seen.pos as Vector2).distance_to(first.pos) <= 0.01 and seen.emitting,
			"alive with the second %d, first seen %s, first at %s then %s, emitting %s"
			% [second.others.size() + 1, not seen.is_empty(), first.pos, seen.get("pos"), seen.get("emitting")])
		_check("S8 the first burst leaves the tree 25–30 ticks after its birth: not restarted, not cut short",
			first.exited - first.born >= 25 and first.exited - first.born <= 30,
			"born %d, left %d: %d ticks" % [first.born, first.exited, first.exited - first.born])
	else:
		_check("S7 two cuts: two bursts alive at the second cut", false,
			"bursts born on %s, edges on %s" % [_born_ticks(new_bursts), new_edges])
		var life: int = (new_bursts[0].exited - new_bursts[0].born) if not new_bursts.is_empty() else -1
		_check("S8 the first burst leaves the tree 25–30 ticks after its birth: not restarted, not cut short",
			life >= 25 and life <= 30, "%d ticks" % life)

	# S9: mashing slash for 2 s.
	n = _bursts.size()
	e = _edges.size()
	_max_alive = 0
	var swings := 0
	var was_slashing := false
	for i in 120:
		if i % 2 == 0:
			Input.action_press(&"slash")
		else:
			Input.action_release(&"slash")
		await _frames(1)
		if _rudy.is_slashing() and not was_slashing:
			swings += 1
		was_slashing = _rudy.is_slashing()
	Input.action_release(&"slash")
	await _frames(45)
	_check("S9 mashing slash: one burst per live edge per swing, and never more than 2 alive",
		swings >= 3 and _bursts.size() - n == swings and _edges.size() - e == swings and _max_alive <= 2,
		"%d swings, %d edges, %d bursts, at most %d alive" % [swings, _edges.size() - e, _bursts.size() - n, _max_alive])

	# S10: where every burst so far lives.
	var outside := _bursts.filter(func(b: Burst) -> bool: return not b.in_container)
	_check("S10 every burst's parent is Effects/SlashBursts, and no Rudy or goblin is its ancestor",
		not _bursts.is_empty() and outside.is_empty(), "%d bursts, %d outside" % [_bursts.size(), outside.size()])

	# S11: a cut that defeats a goblin.
	await _tap(&"move_right")
	await _frames(2)
	_teleport(Vector2(goblin_b.global_position.x - 70.0, ground_y))
	await _frames(2)
	n = _bursts.size()
	await _tap(&"slash")
	await _wait_until(func() -> bool: return _bursts.size() > n, 30)
	var visible_ticks := 0
	var hidden_ticks := 0
	var goblin_gone_while_visible := false
	if _bursts.size() > n:
		var b: Burst = _bursts[n]
		for i in 30:
			if is_instance_valid(b.node) and b.node.is_inside_tree():
				if b.node.is_visible_in_tree():
					visible_ticks += 1
					goblin_gone_while_visible = goblin_gone_while_visible or not goblin_b.visible
				else:
					hidden_ticks += 1
			await _frames(1)
	_check("S11 a cut defeats a goblin: the goblin hides while the burst is still visible, and the burst is visible every tick of its life",
		goblin_b.dead and goblin_gone_while_visible and hidden_ticks == 0 and visible_ticks >= 25,
		"goblin dead %s, hidden while the burst showed %s; burst visible %d ticks, hidden %d"
		% [goblin_b.dead, goblin_gone_while_visible, visible_ticks, hidden_ticks])

	# S12: a stomp with the sword.
	await _wait_until(func() -> bool:
		return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable(), 120)
	n = _bursts.size()
	e = _edges.size()
	_teleport(Vector2(goblin_a.global_position.x, ground_y - Goblin.HEIGHT - 60.0))
	_rudy.velocity = Vector2(0, 200)
	await _frames(1)
	await _wait_until(func() -> bool: return goblin_a.dead or _rudy.is_on_floor(), 60)
	await _frames(30)
	_check("S12 a stomp with the sword: no burst, no live edge",
		goblin_a.dead and _rudy.gear == Rudy.Gear.SWORD and _bursts.size() == n and _edges.size() == e,
		"goblin dead %s, gear %s, bursts %d, edges %d"
		% [goblin_a.dead, Rudy.Gear.keys()[_rudy.gear], _bursts.size() - n, _edges.size() - e])

	# S13: slash while paused.
	await _wait_until(func() -> bool: return _rudy.is_on_floor(), 60)
	await _frames(10)
	n = _bursts.size()
	await _tap(&"pause")
	var paused := _main.is_paused()
	await _tap(&"slash")
	await _frames(30)
	var while_paused := _bursts.size() - n
	await _tap(&"pause")
	var resumed := not _main.is_paused()
	await _frames(10)
	_check("S13 slash while paused: no burst then, and none in the 10 ticks after resuming",
		paused and resumed and while_paused == 0 and _bursts.size() == n,
		"paused %s, resumed %s; bursts while paused %d, after %d" % [paused, resumed, while_paused, _bursts.size() - n - while_paused])

	# S14: a burst alive when the tree pauses.
	n = _bursts.size()
	await _tap(&"slash")
	await _wait_until(func() -> bool: return _bursts.size() > n, 30)
	await _tap(&"pause")
	await _frames(30)
	var ok := false
	var detail := "no burst"
	if _bursts.size() > n:
		var b: Burst = _bursts[n]
		var alive := is_instance_valid(b.node) and b.node.is_inside_tree()
		var sparks: GPUParticles2D = b.node.get_node("Sparks") if alive else null
		var shown := alive and b.node.is_visible_in_tree()
		var emitting := alive and sparks.emitting
		var processing := alive and sparks.can_process()
		await _tap(&"pause")
		var runs_again := alive and is_instance_valid(sparks) and sparks.can_process()
		ok = not _main.is_paused() and shown and emitting and not processing and runs_again
		detail = "while paused: in the tree %s, visible %s, emitting %s, processing %s; after resuming: processing %s" % [
			alive, shown, emitting, processing, runs_again]
	_check("S14 a burst alive at a pause stays in the tree and visible, still emitting, and stops processing until resumed",
		ok, detail)


func _alive() -> int:
	var count := 0
	for child in _slash_bursts.get_children():
		if not child.is_queued_for_deletion():
			count += 1
	return count


func _born_ticks(bursts: Array) -> Array[int]:
	var ticks: Array[int] = []
	for b: Burst in bursts:
		ticks.append(b.born)
	return ticks


func _check(what: String, ok: bool, detail: String = "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", what, "" if detail.is_empty() else "  (%s)" % detail])
	if not ok:
		_failures += 1


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


## Waits until `condition` is true, for at most `max_ticks`; returns the ticks waited.
func _wait_until(condition: Callable, max_ticks: int) -> int:
	for t in max_ticks:
		if condition.call():
			return t
		await get_tree().physics_frame
	return max_ticks


func _hold_until(action: StringName, condition: Callable, max_ticks: int) -> void:
	Input.action_press(action)
	await _wait_until(condition, max_ticks)
	Input.action_release(action)


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _frames(2)
	Input.action_release(action)


func _teleport(spot: Vector2) -> void:
	_rudy.global_position = spot
	_rudy.velocity = Vector2.ZERO
