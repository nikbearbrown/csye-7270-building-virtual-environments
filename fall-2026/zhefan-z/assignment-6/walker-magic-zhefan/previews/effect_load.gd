extends Node
## Effect load for the price measurements (CHANGE-BRIEF "Price predictions and budget"), shared by the headless cost
## script (tests/cost_effects.gd) and the windowed GPU price scene (previews/gpu_price.tscn), so both price the same
## load. It instances, moves, stops and frees the effect scenes; it never sets a particle or material value.
## - OFF: nothing.
## - A: Effect A at its bound, 6 FireballImpact instances alive (A4: 6 fireballs landing within one 0.9 s window).
##   The first 6 are spawned 0.15 s apart (0.9 s / 6); each one that frees itself is replaced on the next frame.
## - B: Effect B at its heaviest. 6 carriers fly at the fireball's 260 px/s with one trail each and never stop, so they
##   always carry a full trail (6 x 32 particles). 6 more carriers each carry a trail for one trail lifetime (0.3 s, so
##   it is full), then release it as fireball.gd does (moved to the parent with its global transform kept, emitting off,
##   freed one lifetime later) and start a new one: about 6 detached trails are always fading. Those 6 refilling trails
##   are on top of the brief's "6 + 6", so B is an upper bound. Carriers are plain Node2D, not Fireball (no Area2D, no
##   physics), so the case prices the trails, not the fireballs.
## - `dry`: the same driver doing the same bookkeeping, moves and frees, with a bare Node2D in place of every effect
##   instance. A case minus its dry case is the effects' own price, without this driver's.

enum Mode { OFF, A, B }

const IMPACT := preload("res://effects/fireball_impact.tscn")
const IMPACT_SCRIPT := preload("res://effects/fireball_impact.gd")   # its LIFETIME, for the dry placeholders
const TRAIL := preload("res://effects/fireball_trail.tscn")
const BOUND := 6               # CHANGE-BRIEF A4 and the price table: 6 alive
const IMPACT_SPACING := 0.15   # 0.9 s / 6
const SPEED := 260.0           # features/fireball/fireball.gd SPEED

## Where the effects go, in the target's coordinates (the 640x360 view of the game scene at its start).
var area := Rect2(60, 110, 520, 200)
var target: Node2D
var mode := Mode.OFF
var dry := false
var spawns := 0          # effect instances created so far (lets a caller tag the frames that spawned)

var _t := 0.0
var _next_impact := 0.0
var _impacts: Array[Node] = []
var _spawned := 0
var _flyers: Array[Node2D] = []     # carriers that keep their trail
var _feeders: Array[Node2D] = []    # carriers that release their trail every lifetime
var _feeder_age: Array[float] = []
var _detached: Array[Node] = []
var _life := 0.3         # replaced by the trail scene's lifetime in set_mode()


func set_mode(m: Mode) -> void:
	clear()
	mode = m
	_t = 0.0
	_next_impact = 0.0
	if mode == Mode.B:
		var probe := TRAIL.instantiate() as GPUParticles2D
		_life = probe.lifetime
		probe.free()
		for i in BOUND:
			_flyers.append(_carrier(i, false))
			_feeders.append(_carrier(i, true))
		# Stagger the releases evenly over one trail lifetime (read from the scene), so detached trails overlap.
		for i in BOUND:
			_feeder_age.append(_life * i / BOUND)


func clear() -> void:
	for n in _impacts + _detached + _flyers + _feeders:   # untyped: the lists can hold freed instances
		if is_instance_valid(n):
			n.queue_free()
	_impacts.clear()
	_detached.clear()
	_flyers.clear()
	_feeders.clear()
	_feeder_age.clear()


## Counts for the report and the on-screen text.
func counts() -> Dictionary:
	_prune()
	return {"impacts": _impacts.size(), "flying_trails": _flyers.size(), "refilling_trails": _feeders.size(),
		"detached_trails": _detached.size()}


## Drops freed instances. A plain loop: a typed lambda cannot take a freed instance, and filter() returns an untyped Array.
func _prune() -> void:
	for list: Array[Node] in [_impacts, _detached]:
		for i in range(list.size() - 1, -1, -1):
			if not is_instance_valid(list[i]) or not list[i].is_inside_tree():
				list.remove_at(i)


func _carrier(i: int, feeder: bool) -> Node2D:
	var c := Node2D.new()
	c.name = ("Feeder%d" if feeder else "Flyer%d") % i
	# Lanes across the area; each carrier starts at a different x so they do not move in step.
	var lanes := BOUND * 2
	var lane := i * 2 + (1 if feeder else 0)
	c.position = Vector2(area.position.x + fmod(97.0 * lane, area.size.x), area.position.y + area.size.y * (lane + 0.5) / lanes)
	c.set_meta("dir", 1.0 if lane % 2 == 0 else -1.0)
	c.rotation = 0.0 if c.get_meta("dir") > 0.0 else PI
	target.add_child(c)
	c.add_child(_new_trail())
	return c


func _new_trail() -> Node2D:
	spawns += 1
	return Node2D.new() if dry else TRAIL.instantiate()


func _new_impact() -> Node2D:
	spawns += 1
	if not dry:
		return IMPACT.instantiate()
	var n := Node2D.new()
	# Connected to the node's own method, so the connection goes away if the node is freed first (scene teardown).
	n.ready.connect(func() -> void: n.get_tree().create_timer(IMPACT_SCRIPT.LIFETIME, false).timeout.connect(n.queue_free))
	return n


func _process(delta: float) -> void:
	_t += delta
	if mode == Mode.A:
		_prune()
		if _impacts.size() < BOUND and (_t >= _next_impact or _spawned >= BOUND):
			var fx := _new_impact()
			# Spread over the area with a fixed step, so every run places them the same way.
			fx.position = area.position + Vector2(fmod(137.0 * _spawned, area.size.x), fmod(53.0 * _spawned, area.size.y))
			target.add_child(fx)
			_impacts.append(fx)
			_spawned += 1
			_next_impact = _t + IMPACT_SPACING
	elif mode == Mode.B:
		_prune()
		for i in _feeders.size():
			_feeder_age[i] += delta
			var c := _feeders[i]
			var trail := c.get_child(0) as Node2D
			if trail and _feeder_age[i] >= _life:
				_feeder_age[i] -= _life
				# As fireball.gd _release_trail(): move, stop, free one lifetime later.
				trail.reparent(target, true)
				if trail is GPUParticles2D:
					(trail as GPUParticles2D).emitting = false
				get_tree().create_timer(_life, false).timeout.connect(trail.queue_free)
				_detached.append(trail)
				c.add_child(_new_trail())


## Carriers move on physics ticks, like fireballs, back and forth across the area, turned to face the way they fly.
func _physics_process(delta: float) -> void:
	if mode != Mode.B:
		return
	for c: Node2D in _flyers + _feeders:
		var dir: float = c.get_meta("dir")
		c.position.x += dir * SPEED * delta
		if c.position.x > area.end.x or c.position.x < area.position.x:
			c.position.x = clampf(c.position.x, area.position.x, area.end.x)
			c.set_meta("dir", -dir)
			c.rotation = 0.0 if -dir > 0.0 else PI
