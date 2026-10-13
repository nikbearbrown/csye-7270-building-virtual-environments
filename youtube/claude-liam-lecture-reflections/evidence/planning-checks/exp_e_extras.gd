extends SceneTree
# Experiment E (Reflections layout): the claims that sit around the main effect.
#
#   E1  hiding the LabelMap node changes the picture ONLY where the reflection is (the label map is invisible, yet it does the work)
#   E2  a Camera2D that pans and zooms: the reflection still lands only on water (checked in screen space, no geometry formulas)
#   E3  a jump: RemoteTransform2D pushes the same movement to the reflection (it goes UP with the character, not down)
#   E4  a see-through ground: how much of the mask leaks at ground alpha 0.9 and 0.8
#   E5  RemoteTransform2D numbers: the reflection's position is the player's plus the offset, each frame, after the move
#   E6  Inspector wording: property names, hint strings and defaults straight from ClassDB (what the editor would show)
#
# Run: godot --path <scratch project> [--rendering-method gl_compatibility] --script res://exp_e_extras.gd
const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"

var tex := {}
var cur := {}

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["case"] = id
	d["renderer"] = RenderingServer.get_current_rendering_method()
	print("RESULT " + JSON.stringify(d))

func new_pond(shader_file: String, x: float, opts: Dictionary = {}) -> void:
	if cur.has("scene"):
		cur["scene"].queue_free()
		await process_frame
	var o := {"mask_tex": tex["mask"], "ground_tex": tex["ground"], "char_tex": tex["char"]}
	o.merge(opts, true)
	cur = P.build_pond(root, SHADERS, shader_file, x, o)

func diff_set(a: Image, b: Image, thr: float = 0.004) -> Dictionary:
	var s := {}
	for y in range(a.get_height()):
		for x in range(a.get_width()):
			var pa := a.get_pixel(x, y)
			var pb := b.get_pixel(x, y)
			if absf(pa.r - pb.r) + absf(pa.g - pb.g) + absf(pa.b - pb.b) > thr:
				s[Vector2i(x, y)] = true
	return s

func bounds(s: Dictionary) -> Array:
	if s.is_empty():
		return []
	var x0 := 99999
	var y0 := 99999
	var x1 := -1
	var y1 := -1
	for k in s:
		x0 = mini(x0, k.x)
		y0 = mini(y0, k.y)
		x1 = maxi(x1, k.x)
		y1 = maxi(y1, k.y)
	return [x0, y0, x1, y1]

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(P.W, P.H)
	await frames(3)
	tex["mask"] = ImageTexture.create_from_image(P.make_mask_image())
	tex["ground"] = ImageTexture.create_from_image(P.make_ground_image())
	tex["char"] = ImageTexture.create_from_image(P.make_character_image())

	# ---- E1: toggle the mask, reflection visible
	await new_pond("02-reflection.gdshader", 300.0)
	await frames(3)
	var with_mask := grab()
	cur["mask"].visible = false
	await frames(3)
	var no_mask := grab()
	cur["mask"].visible = true
	var d1 := diff_set(with_mask, no_mask)
	cur["reflection"].visible = false
	await frames(3)
	var no_refl := grab()
	cur["reflection"].visible = true
	var refl_set := diff_set(with_mask, no_refl)
	var outside := 0
	for k in d1:
		if not refl_set.has(k):
			outside += 1
	out("E1-toggle-the-mask", {"pixels_changed_by_hiding_the_mask": d1.size(), "pixels_the_reflection_occupies": refl_set.size(), "changed_pixels_outside_the_reflection": outside, "changed_bounds": bounds(d1)})

	# ---- E2: camera pan + zoom
	await new_pond("02-reflection.gdshader", 300.0)
	var cam := Camera2D.new()
	cam.position = Vector2(P.W / 2.0 - 120.0, P.H / 2.0 + 40.0)
	cam.zoom = Vector2(1.4, 1.4)
	cur["scene"].add_child(cam)
	cam.make_current()
	await frames(4)
	var frame_all := grab()
	cur["reflection"].visible = false
	await frames(3)
	var frame_none := grab()
	var visible_set := diff_set(frame_all, frame_none, 0.03)
	# the reflection body drawn WITHOUT the mask test (plain sprite): where the reflection would be if everything were water
	cur["reflection"].material = null
	cur["reflection"].visible = true
	await frames(3)
	var frame_plain := grab()
	var body_set := diff_set(frame_plain, frame_none, 0.03)
	# the mask in screen space: render with Ground hidden and the player/reflection hidden: mask-red pixels
	cur["reflection"].visible = false
	cur["player"].visible = false
	cur["ground"].visible = false
	await frames(3)
	var mask_only := grab()
	var red_ok := 0
	var outside_red := 0
	for k in visible_set:
		var c := mask_only.get_pixel(k.x, k.y)
		if Vector3(c.r - 1.0, c.g, c.b).length() < 0.1:
			red_ok += 1
		else:
			outside_red += 1
	var body_on_red := 0
	var body_on_red_but_hidden := 0
	for k in body_set:
		var c2 := mask_only.get_pixel(k.x, k.y)
		if Vector3(c2.r - 1.0, c2.g, c2.b).length() < 0.1:
			body_on_red += 1
			if not visible_set.has(k):
				body_on_red_but_hidden += 1
	out("E2-camera-pan-and-zoom-1.4", {"reflection_pixels_visible": visible_set.size(), "of_which_on_mask_red": red_ok, "visible_but_not_on_red": outside_red,
		"plain_body_pixels": body_set.size(), "plain_body_pixels_on_red": body_on_red, "on_red_but_hidden": body_on_red_but_hidden})

	# ---- E3: a jump (player 80 px up)
	await new_pond("02-reflection.gdshader", 300.0)
	await frames(3)
	var flat_img := grab()
	var rpos0: Vector2 = cur["reflection"].global_position
	cur["player"].position.y -= 80.0
	await frames(3)
	var jump_img := grab()
	var rpos1: Vector2 = cur["reflection"].global_position
	cur["reflection"].visible = false
	await frames(3)
	var jump_none := grab()
	var jump_visible := diff_set(jump_img, jump_none, 0.03)
	out("E3-jump-80-px", {"reflection_y_before": rpos0.y, "reflection_y_after": rpos1.y, "moved_by": rpos1.y - rpos0.y, "player_moved_by": -80.0,
		"visible_reflection_bounds_after_jump": bounds(jump_visible), "visible_pixels_after_jump": jump_visible.size(), "shoreline_y": P.SHORE_Y})

	# ---- E4: see-through ground
	for a in [1.0, 0.9, 0.8]:
		await new_pond("02-reflection.gdshader", 300.0, {"ground_alpha": a})
		cur["reflection"].visible = false
		cur["mask"].visible = true
		await frames(3)
		var m_on := grab()
		cur["mask"].visible = false
		await frames(3)
		var m_off := grab()
		var worst := 0.0
		var px := Vector2i(100, 600)
		var c_on := m_on.get_pixel(px.x, px.y)
		var c_off := m_off.get_pixel(px.x, px.y)
		for y in range(0, P.H, 4):
			for x in range(0, P.W, 4):
				var a1 := m_on.get_pixel(x, y)
				var b1 := m_off.get_pixel(x, y)
				worst = maxf(worst, maxf(absf(a1.r - b1.r), maxf(absf(a1.g - b1.g), absf(a1.b - b1.b))))
		out("E4-ground-alpha-%.1f" % a, {"largest_channel_change_when_mask_is_shown": snappedf(worst, 0.001), "water_pixel_with_mask": [snappedf(c_on.r, 0.001), snappedf(c_on.g, 0.001), snappedf(c_on.b, 0.001)],
			"water_pixel_without_mask": [snappedf(c_off.r, 0.001), snappedf(c_off.g, 0.001), snappedf(c_off.b, 0.001)]})

	# ---- E5: RemoteTransform2D bookkeeping
	await new_pond("02-reflection.gdshader", 300.0)
	var worst_gap := 0.0
	for i in range(30):
		cur["player"].position += Vector2(7.0, 0.0)
		await process_frame
		var expect: Vector2 = cur["player"].global_position + Vector2(0.0, P.REFLECT_OFFSET)
		worst_gap = maxf(worst_gap, (cur["reflection"].global_position - expect).length())
	out("E5-remote-transform-follows", {"frames": 30, "largest_gap_px_between_reflection_and_player_plus_offset": worst_gap})

	# ---- E6: Inspector wording from ClassDB
	var props := {}
	for cls in ["BackBufferCopy", "RemoteTransform2D", "Sprite2D"]:
		var list := ClassDB.class_get_property_list(cls, true)
		var keep := []
		for p in list:
			if p["name"] in ["copy_mode", "rect", "remote_path", "update_position", "update_rotation", "update_scale", "use_global_coordinates", "flip_v", "flip_h"]:
				keep.append({"name": p["name"], "label_by_capitalize": String(p["name"]).capitalize(), "type": p["type"], "hint": p["hint"], "hint_string": p["hint_string"]})
		props[cls] = keep
	out("E6-inspector-properties-from-ClassDB", props)
	quit(0)
