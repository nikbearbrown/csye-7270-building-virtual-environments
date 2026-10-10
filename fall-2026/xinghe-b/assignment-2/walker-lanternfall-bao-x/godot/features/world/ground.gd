extends Node2D
## The night market, broken up (Bao: "整体地图应该破碎一点"): scattered clusters — ragged rows of stalls and noodle
## carts with gaps, lantern corners with puddles, abandoned crate piles, lone stalls — with alleys between them,
## plus stray posts and crates, puddles and leaves. Built from its own fixed seed (never the game rng); a plaza
## around the spawn stays clear; solid props never overlap one another.

const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

const PLAZA_RADIUS := 150.0
const CLUSTERS := 14
const CLUSTER_GAP := 230.0
const MIN_EACH := 4
const PUDDLES := 36
const LEAVES := 60
const PATHS := {
	"stall": Art.STALL, "cart": Art.CART, "post": Art.POST, "crates": Art.CRATES,
	"puddle": Art.PUDDLE, "leaves": Art.LEAVES,
}
const DECALS := ["puddle", "leaves"]
## Props that block the courier (Bao, 2026-09-29). Each box is relative to the prop's centre and is the sprite's
## opaque area inset by 2 px, measured from the generated PNG (test solid-boxes-match-sprites keeps them in sync);
## a lantern post blocks only at its pole. Layout and collision use the same fixed boxes, so the map is identical
## whether or not the textures are loaded. Enemies are not blocked: moths fly over, fog-wraiths drift through.
const SOLID_BOX := {
	"stall": Rect2(-19, -18, 39, 39),   # env_stall.png
	"cart": Rect2(-12, -19, 24, 41),    # env_noodle_cart.png (narrow, tall cart)
	"crates": Rect2(-17, -12, 34, 26),  # env_crates.png
	"post": Rect2(-6, -18, 4, 40),      # env_lantern_post.png: the pole is sprite columns 6-9
}
## Puddles and leaves are drawn at this opacity so they add texture without outshining the courier or the gems.
const DECAL_ALPHA := 0.55

var tile: Texture2D
var tex := {}
## [{kind, pos, layer}] — decals (layer 0) first, then props by y so lower ones overlap higher ones.
var props: Array = []
var solids: Array[Rect2] = []

func _ready() -> void:
	z_index = -10
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	tile = Art.texture(Art.GROUND)
	for k in PATHS:
		tex[k] = Art.texture(PATHS[k])
	build()
	queue_redraw()

func build() -> void:
	props.clear()
	solids.clear()
	var r := RandomNumberGenerator.new()
	r.seed = 1234
	var a := Tuning.ARENA
	var centres: Array[Vector2] = []
	var tries := 0
	while centres.size() < CLUSTERS and tries < 4000:
		tries += 1
		var c := Vector2(r.randf_range(a.position.x + 120, a.end.x - 120), r.randf_range(a.position.y + 100, a.end.y - 100))
		if c.length() < PLAZA_RADIUS + 110:
			continue
		var far := true
		for o in centres:
			far = far and o.distance_to(c) >= CLUSTER_GAP
		if far:
			centres.append(c)
	for c in centres:
		match r.randi_range(0, 3):
			0:  # a ragged row of stalls and carts, bent and with gaps
				var n := r.randi_range(2, 4)
				var step := Vector2(r.randf_range(72, 92), r.randf_range(-20, 20))
				for i in n:
					if r.randf() < 0.2:
						continue
					var at := c + step * (i - (n - 1) / 2.0) + _jitter(r, 8)
					_place("cart" if r.randf() < 0.35 else "stall", at)
					if r.randf() < 0.5:
						_place("crates", at + Vector2(r.randf_range(-24, 24), r.randf_range(34, 46)))
				_place("post", c + Vector2(r.randf_range(-50, 50), -52))
			1:  # a lantern corner: posts around a small wet square
				for i in r.randi_range(2, 4):
					_place("post", c + Vector2.from_angle(r.randf() * TAU) * r.randf_range(34, 72))
				for i in r.randi_range(1, 3):
					_place("puddle", c + _jitter(r, 40))
				if r.randf() < 0.6:
					_place("cart", c + _jitter(r, 16))
			2:  # an abandoned pile of crates, maybe a stall left behind
				for i in r.randi_range(2, 5):
					_place("crates", c + _jitter(r, 50))
				if r.randf() < 0.5:
					_place("stall", c + _jitter(r, 36))
			3:  # a lone stall with its lantern
				var at := c + _jitter(r, 20)
				_place("stall" if r.randf() < 0.6 else "cart", at)
				_place("post", at + Vector2(r.randf_range(40, 48) * (1 if r.randf() < 0.5 else -1), r.randf_range(-12, 12)))
	for kind in ["stall", "cart", "post", "crates"]:
		var guard := 0
		while _count(kind) < MIN_EACH and guard < 200:
			guard += 1
			_place(kind, Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	for i in 10:
		_place("post", Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	for i in 8:
		_place("crates", Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	for i in PUDDLES:
		_place("puddle", Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	for i in LEAVES:
		_place("leaves", Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	props.sort_custom(func(p, q): return p["layer"] < q["layer"] or (p["layer"] == q["layer"] and p["pos"].y < q["pos"].y))
	solids.clear()
	for p in props:
		if SOLID_BOX.has(p["kind"]):
			solids.append(_solid_box(p["kind"], p["pos"]))

func _jitter(r: RandomNumberGenerator, amount: float) -> Vector2:
	return Vector2(r.randf_range(-amount, amount), r.randf_range(-amount, amount))

func _count(kind: String) -> int:
	var n := 0
	for p in props:
		if p["kind"] == kind:
			n += 1
	return n

## Adds a prop if it is inside the arena and outside the plaza; a solid prop is skipped if it would overlap another.
func _place(kind: String, pos: Vector2) -> void:
	if pos.length() <= PLAZA_RADIUS or not Tuning.ARENA.grow(-24).has_point(pos):
		return
	if SOLID_BOX.has(kind):
		var box := _solid_box(kind, pos)
		for other in solids:
			if other.grow(4).intersects(box):
				return
		solids.append(box)
	props.append({"kind": kind, "pos": pos, "layer": 0 if kind in DECALS else 1})

func _solid_box(kind: String, pos: Vector2) -> Rect2:
	var box: Rect2 = SOLID_BOX[kind]
	return Rect2(pos + box.position, box.size)

## True when a circle at p with radius r overlaps any solid prop.
func blocks(p: Vector2, r: float) -> bool:
	for box in solids:
		if box.grow(r).has_point(p) and _overlap(box, p, r):
			return true
	return false

func _overlap(box: Rect2, p: Vector2, r: float) -> bool:
	var c := p.clamp(box.position, box.end)
	return p.distance_to(c) < r or box.has_point(p)

## Moves a circle out of every solid it overlaps, along the shortest way out, so the courier slides along edges.
func push_out(p: Vector2, r: float) -> Vector2:
	for pass_i in 2:
		for box in solids:
			if not box.grow(r).has_point(p):
				continue
			if box.has_point(p):
				var left := p.x - box.position.x
				var right := box.end.x - p.x
				var up := p.y - box.position.y
				var down := box.end.y - p.y
				var m := minf(minf(left, right), minf(up, down))
				if m == left:
					p.x = box.position.x - r
				elif m == right:
					p.x = box.end.x + r
				elif m == up:
					p.y = box.position.y - r
				else:
					p.y = box.end.y + r
				continue
			var c := p.clamp(box.position, box.end)
			var d := p - c
			if d.length() < r and d.length() > 0.0001:
				p = c + d.normalized() * r
	return p

func _draw() -> void:
	var a := Tuning.ARENA
	if tile:
		draw_texture_rect(tile, a, true)
	else:
		draw_rect(a, Color("#1F2540"))
		for x in range(int(a.position.x), int(a.end.x), 64):
			draw_line(Vector2(x, a.position.y), Vector2(x, a.end.y), Color("#3B4A6B", 0.35))
		for y in range(int(a.position.y), int(a.end.y), 64):
			draw_line(Vector2(a.position.x, y), Vector2(a.end.x, y), Color("#3B4A6B", 0.35))
	for p in props:
		var t: Texture2D = tex.get(p["kind"])
		var pos: Vector2 = p["pos"]
		if p["kind"] == "post":
			# a soft pool of lantern light on the cobbles (drawn, not generated)
			draw_circle(pos + Vector2(0, 18), 30.0, Color(0.95, 0.72, 0.29, 0.07))
		if t:
			draw_texture(t, pos - t.get_size() / 2, Color(1, 1, 1, DECAL_ALPHA if p["layer"] == 0 else 1.0))
		else:
			_draw_placeholder(p["kind"], pos)
	draw_rect(a, Color(0.95, 0.72, 0.29, 0.6), false, 2.0)

func _draw_placeholder(kind: String, p: Vector2) -> void:
	match kind:
		"stall":
			draw_rect(Rect2(p - Vector2(24, 16), Vector2(48, 32)), Color("#B5523B"))
			draw_circle(p - Vector2(0, 24), 6, Color("#F2B84B"))
		"cart":
			draw_rect(Rect2(p - Vector2(24, 12), Vector2(48, 24)), Color("#3B4A6B"))
			draw_circle(p - Vector2(10, 18), 5, Color("#F2B84B"))
		"post":
			draw_line(p + Vector2(0, 20), p - Vector2(0, 20), Color("#14121C"), 2.0)
			draw_circle(p - Vector2(0, 16), 5, Color("#F2B84B"))
		"crates":
			draw_rect(Rect2(p - Vector2(14, 10), Vector2(28, 20)), Color("#8A5A3C"))
		"puddle":
			draw_circle(p, 10, Color("#0E1020", 0.8))
		"leaves":
			draw_circle(p, 3, Color("#8A5A3C"))
