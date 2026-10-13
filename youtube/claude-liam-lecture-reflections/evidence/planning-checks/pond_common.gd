extends RefCounted
# pond_common.gd: the "pond" scene shared by the Reflections planning checks (and the scene the capture harness should rebuild).
#
# Logical canvas 1280 x 720. One geometry function (kind) paints BOTH the visible art and the hidden mask, so they can never drift apart.
#
#   y <  190            sky
#   190 <= y < 350      grass (land); the shoreline is the straight line y = 350
#   y >= 350            water, except a SANDBAR (the part of an ellipse centred (880, 440), radii (200, 105) that lies below the shoreline: a spit of land)
#   a 40 px COAST ring runs around the sandbar, on the water side (no coast along the straight shoreline)
#
# Label-map colours (the hidden layer):  water = pure red (255, 0, 0)   coast = pure green (0, 255, 0)   land/sky = left empty (transparent)
# Visible colours (the art):        sky #C9DCE8   grass #A9BF94   water #6E9CC4   sand #E3D2A6 (sandbar and coast)
# Character: the series' test sprite (teal blob, two cream eyes, transparent padding), 240 px square, body radius 72 px.
#   Stands with its feet on the shoreline: centre y = 278, feet y = 350. Its reflection (flipped copy) has centre y = 494 (offset 144).

const W := 1280
const H := 720
const SHORE_Y := 350
const SKY_Y := 190
const BAR_C := Vector2(880, 440)
const BAR_R := Vector2(200, 105)
const COAST_W := 40.0
const SPRITE_N := 240
const BODY_R := 72.0                     # 0.30 * 240
const PLAYER_Y := 278.0                  # feet on the shoreline (278 + 72 = 350)
const REFLECT_OFFSET := 144.0            # 2 * BODY_R

const KIND_LAND := 0
const KIND_WATER := 1
const KIND_COAST := 2
const KIND_SAND := 3

const COL_SKY := Color("#C9DCE8")
const COL_GRASS := Color("#A9BF94")
const COL_WATER := Color("#6E9CC4")
const COL_SAND := Color("#E3D2A6")
const MASK_WATER := Color(1.0, 0.0, 0.0, 1.0)
const MASK_COAST := Color(0.0, 1.0, 0.0, 1.0)

static func kind(x: int, y: int) -> int:
	if y < SHORE_Y:
		return KIND_LAND
	var dx := (x + 0.5 - BAR_C.x) / BAR_R.x
	var dy := (y + 0.5 - BAR_C.y) / BAR_R.y
	if dx * dx + dy * dy <= 1.0:
		return KIND_SAND
	var dx2 := (x + 0.5 - BAR_C.x) / (BAR_R.x + COAST_W)
	var dy2 := (y + 0.5 - BAR_C.y) / (BAR_R.y + COAST_W)
	if dx2 * dx2 + dy2 * dy2 <= 1.0:
		return KIND_COAST
	return KIND_WATER

static func ground_color(x: int, y: int, k: int) -> Color:
	var c: Color
	match k:
		KIND_WATER:
			c = COL_WATER
			# faint horizontal wave rows so the art does not look like the mask
			if (y / 14) % 2 == 0:
				c = c.lightened(0.05)
		KIND_COAST, KIND_SAND:
			c = COL_SAND
		_:
			c = COL_SKY if y < SKY_Y else COL_GRASS
	return c

static func make_mask_image(water: Color = MASK_WATER, coast: Color = MASK_COAST) -> Image:
	var img := Image.create(W, H, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in range(SHORE_Y, H):
		for x in range(W):
			var k := kind(x, y)
			if k == KIND_WATER:
				img.set_pixel(x, y, water)
			elif k == KIND_COAST:
				img.set_pixel(x, y, coast)
	return img

static func make_ground_image() -> Image:
	var img := Image.create(W, H, false, Image.FORMAT_RGBA8)
	for y in range(H):
		for x in range(W):
			img.set_pixel(x, y, ground_color(x, y, kind(x, y)))
	return img

static func make_character_image(n: int = SPRITE_N) -> Image:
	# Same drawing as lab/runner.gd's "sprite": teal blob, two cream eyes, transparent padding.
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			var d := Vector2(x, y).distance_to(c)
			if d < n * 0.30:
				img.set_pixel(x, y, Color("#5FA391"))
			var e1 := Vector2(x, y).distance_to(c + Vector2(-n * 0.10, -n * 0.06))
			var e2 := Vector2(x, y).distance_to(c + Vector2(n * 0.10, -n * 0.06))
			if e1 < n * 0.035 or e2 < n * 0.035:
				img.set_pixel(x, y, Color("#FAF9F5"))
	return img

static func load_shader(file: String, dir: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(dir + file)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	return mat

# Fast, resolution-independent art: both layers painted row by row from the same ellipse spans (so they cannot disagree).
# S = texture pixels per logical pixel (1 for the checks, 3 for a 3840 x 2160 capture over the 1280 x 720 canvas).
static func _spans(y: int, S: int) -> Dictionary:
	# x spans (texture pixels, inclusive-exclusive) of the sandbar and of its coast ring in texture row y (y >= shoreline row)
	var cx := BAR_C.x * S
	var cy := BAR_C.y * S
	var dy := (y + 0.5 - cy) / (BAR_R.y * S)
	var out := {"sand": Vector2i(0, 0), "coast": Vector2i(0, 0)}
	if absf(dy) <= 1.0:
		var hw := BAR_R.x * S * sqrt(1.0 - dy * dy)
		out["sand"] = Vector2i(int(ceil(cx - hw - 0.5)), int(floor(cx + hw - 0.5)) + 1)
	var dy2 := (y + 0.5 - cy) / ((BAR_R.y + COAST_W) * S)
	if absf(dy2) <= 1.0:
		var hw2 := (BAR_R.x + COAST_W) * S * sqrt(1.0 - dy2 * dy2)
		out["coast"] = Vector2i(int(ceil(cx - hw2 - 0.5)), int(floor(cx + hw2 - 0.5)) + 1)
	return out

static func make_layers(S: int, water: Color = MASK_WATER, coast: Color = MASK_COAST) -> Dictionary:
	var w := W * S
	var h := H * S
	var mask := Image.create(w, h, false, Image.FORMAT_RGBA8)
	mask.fill(Color(0, 0, 0, 0))
	var ground := Image.create(w, h, false, Image.FORMAT_RGBA8)
	ground.fill_rect(Rect2i(0, 0, w, SKY_Y * S), COL_SKY)
	ground.fill_rect(Rect2i(0, SKY_Y * S, w, (SHORE_Y - SKY_Y) * S), COL_GRASS)
	for y in range(SHORE_Y * S, h):
		var wc := COL_WATER
		if (y / (14 * S)) % 2 == 0:
			wc = wc.lightened(0.05)
		var sp := _spans(y, S)
		var sand: Vector2i = sp["sand"]
		var ring: Vector2i = sp["coast"]
		var has_sand := sand.y > sand.x
		var has_ring := ring.y > ring.x
		if not has_ring:
			ground.fill_rect(Rect2i(0, y, w, 1), wc)
			mask.fill_rect(Rect2i(0, y, w, 1), water)
			continue
		# water left and right of the ring
		ground.fill_rect(Rect2i(0, y, ring.x, 1), wc)
		mask.fill_rect(Rect2i(0, y, ring.x, 1), water)
		ground.fill_rect(Rect2i(ring.y, y, w - ring.y, 1), wc)
		mask.fill_rect(Rect2i(ring.y, y, w - ring.y, 1), water)
		# the ring itself (sand colour in the art, coast colour in the mask), minus the sandbar inside it
		ground.fill_rect(Rect2i(ring.x, y, ring.y - ring.x, 1), COL_SAND)
		if has_sand:
			mask.fill_rect(Rect2i(ring.x, y, sand.x - ring.x, 1), coast)
			mask.fill_rect(Rect2i(sand.y, y, ring.y - sand.y, 1), coast)
		else:
			mask.fill_rect(Rect2i(ring.x, y, ring.y - ring.x, 1), coast)
	return {"mask": mask, "ground": ground}

# The whole scene in one call (used by the experiments; the capture harness should build the same tree).
#   returns {"scene", "mask", "bbc", "ground", "player", "reflection", "rt"}
#   opts: order ("good" | "copy_after_ground" | "mask_over_ground" | "no_copy_node"), ground_alpha, copy_mode, mask_tex, ground_tex, char_tex
static func build_pond(parent: Node, shaders_dir: String, shader_file: String, x: float, opts: Dictionary) -> Dictionary:
	var scene := Node2D.new()
	scene.name = "Pond"
	parent.add_child(scene)
	var mask := Sprite2D.new()
	mask.name = "LabelMap"
	mask.texture = opts["mask_tex"]
	mask.centered = false
	var ground := Sprite2D.new()
	ground.name = "Ground"
	ground.texture = opts["ground_tex"]
	ground.centered = false
	ground.modulate.a = opts.get("ground_alpha", 1.0)
	var bbc := BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = opts.get("copy_mode", BackBufferCopy.COPY_MODE_VIEWPORT)
	var player := Sprite2D.new()
	player.name = "Player"
	player.texture = opts["char_tex"]
	player.position = Vector2(x, PLAYER_Y)
	var rt := RemoteTransform2D.new()
	rt.name = "RemoteTransform2D"
	rt.position = Vector2(0, REFLECT_OFFSET)
	player.add_child(rt)
	var reflection := Sprite2D.new()
	reflection.name = "Reflection"
	reflection.texture = opts["char_tex"]
	reflection.flip_v = true
	reflection.material = load_shader(shader_file, shaders_dir)
	var order: Array
	match opts.get("order", "good"):
		"copy_after_ground":
			order = [mask, ground, bbc, player, reflection]
		"mask_over_ground":
			order = [ground, mask, bbc, player, reflection]
		"no_copy_node":
			order = [mask, ground, player, reflection]
		_:
			order = [mask, bbc, ground, player, reflection]
	for n in order:
		scene.add_child(n)
	rt.remote_path = rt.get_path_to(reflection)
	return {"scene": scene, "mask": mask, "bbc": bbc, "ground": ground, "player": player, "reflection": reflection, "rt": rt}
