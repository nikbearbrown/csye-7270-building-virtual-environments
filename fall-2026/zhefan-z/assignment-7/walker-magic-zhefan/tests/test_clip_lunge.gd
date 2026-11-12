extends SceneTree
## Assignment 7 read-back of clip 2, the wolf lunge rig (CHANGE-BRIEF Clip 2, the revision of 2026-11-10 and Tests).
## Loads features/wolf/wolf.tscn (not added to the tree, so nothing plays) and reads back: every track of patrol, lunge
## and dead resolves to a real node and property (anim_checks.gd track_problems); lunge's key times equal the revised
## table's frames / 60 to 1e-6, its length 89/60, LOOP_NONE, its poses and easing; the rig's structure, regions,
## pivots and material; and that each part draws exactly where the whole Sprite2D draws the lunge image at rest.
## From fall-2026/zhefan-z/assignment-7/:
##   ./scripts/run-test.sh test_clip_lunge.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Lines with "observation" instead of "status" are printed, not asserted. Image.load_from_file prints an engine
## WARNING ("will not work on export"); it is expected here.

const AnimChecks := preload("res://tests/anim_checks.gd")
const SCENE := "res://features/wolf/wolf.tscn"
const LUNGE_PNG := "res://assets/sprites/wolf/wolf_lunge.png"
const EPS := 1e-6
## Revised phase table (CHANGE-BRIEF revision 2026-11-10): key frames and the rig pose at each.
const FRAMES := [0, 25, 31, 37, 53, 65, 89]
const POSES := {
	"Facing/Rig:position": [Vector2(0, 0), Vector2(-4, 0), Vector2(-4, 0), Vector2(3, 0), Vector2(3, 0), Vector2(0, 0), Vector2(0, 0)],
	"Facing/Rig:scale": [Vector2(1, 1), Vector2(1.08, 0.86), Vector2(1.08, 0.86), Vector2(1.22, 0.84), Vector2(1.22, 0.84),
		Vector2(0.94, 1.06), Vector2(1, 1)],
	"Facing/Rig/FrontPivot:rotation": [0.0, 10.0, 10.0, -12.0, -12.0, 0.0, 0.0],   # degrees
	"Facing/Rig/RearPivot:rotation": [0.0, 0.0, 0.0, 8.0, 8.0, 0.0, 0.0],          # degrees
}
## Measured on wolf_lunge.png (80x40) from alpha: split at the waist, hip and shoulder in image pixels.
const REAR_REGION := Rect2(0, 0, 40, 40)
const FRONT_REGION := Rect2(36, 0, 44, 40)
const HIP := Vector2(29, 16)
const SHOULDER := Vector2(55, 16)
const SPRITE_OFFSET := Vector2(-40, -38)   # wolf.tscn Sprite2D: image pixel p draws at p + offset

var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func observe(id: String, observed: Dictionary) -> void:
	print(JSON.stringify({"id": id, "observation": observed}))


## Transform from `node` up to (not including) `top`, from the nodes' local transforms (works outside the tree).
func to_ancestor(node: Node2D, top: Node) -> Transform2D:
	var t := Transform2D.IDENTITY
	var n: Node = node
	while n != top:
		t = (n as Node2D).transform * t
		n = n.get_parent()
	return t


func near(a: Variant, b: Variant, eps: float) -> bool:
	if a is Vector2:
		return (a as Vector2).distance_to(b) <= eps
	return absf(float(a) - float(b)) <= eps


func run() -> void:
	var wolf: Node = load(SCENE).instantiate()
	var aps := AnimChecks.players(wolf)
	var ap: AnimationPlayer = aps[0] if aps.size() == 1 else null
	check("one-animation-player-physics-no-autoplay", ap != null and ap.get_parent() == wolf
		and ap.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS and ap.autoplay == "",
		{"animation_players": aps.size(), "callback_mode_process": ap.callback_mode_process if ap else -1,
		"autoplay": ap.autoplay if ap else null})
	if ap == null:
		print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
		quit(1)
		return

	var names := Array(ap.get_animation_list())
	check("clips-patrol-lunge-dead", names.size() == 3 and ["patrol", "lunge", "dead"].all(func(n: String) -> bool:
		return n in names), {"clips": names})
	var problems := []
	for n: String in names:
		problems.append_array(AnimChecks.track_problems(ap, ap.get_animation(n)))
	check("every-track-resolves-to-a-real-node-and-property", problems.is_empty(), {"problems": problems})

	var lunge := ap.get_animation("lunge")
	check("lunge-length-89-over-60-loop-none", absf(lunge.length - 89.0 / 60.0) < EPS
		and lunge.loop_mode == Animation.LOOP_NONE, {"length": lunge.length, "expected": 89.0 / 60.0,
		"loop_mode": lunge.loop_mode})

	# Key times and poses, track by track, against the revised table.
	var time_errors := {}
	var pose_errors := {}
	var table := []
	for path: String in POSES:
		var i := AnimChecks.track(lunge, path)
		if i < 0 or lunge.track_get_key_count(i) != FRAMES.size():
			time_errors[path] = "missing or %d keys" % (lunge.track_get_key_count(i) if i >= 0 else 0)
			continue
		var is_rot := path.ends_with(":rotation")
		for k in FRAMES.size():
			var t := lunge.track_get_key_time(i, k)
			if absf(t - FRAMES[k] / 60.0) > EPS:
				time_errors["%s@%d" % [path, FRAMES[k]]] = t
			var v: Variant = lunge.track_get_key_value(i, k)
			var got: Variant = rad_to_deg(v) if is_rot else v
			if not near(got, POSES[path][k], 1e-3 if is_rot else 1e-4):
				pose_errors["%s@%d" % [path, FRAMES[k]]] = {"got": got, "expected": POSES[path][k]}
		if path == "Facing/Rig:scale":
			for k in FRAMES.size():
				table.append("frame %d -> %.6f s (key %.9f)" % [FRAMES[k], FRAMES[k] / 60.0, lunge.track_get_key_time(i, k)])
	check("lunge-key-times-equal-frames-over-60", time_errors.is_empty(), {"frames": FRAMES, "errors": time_errors})
	check("lunge-poses-match-table", pose_errors.is_empty(), {"errors": pose_errors})
	observe("lunge-key-times", {"table": table})

	# Transitions into each key (Godot ease curve on the key before): ease in > 1, ease out in (0, 1).
	var ri := AnimChecks.track(lunge, "Facing/Rig:scale")
	var tr := []
	for k in lunge.track_get_key_count(ri):
		tr.append(lunge.track_get_key_transition(ri, k))
	var same_everywhere := POSES.keys().all(func(p: String) -> bool:
		var i := AnimChecks.track(lunge, p)
		for k in lunge.track_get_key_count(i):
			if lunge.track_get_key_transition(i, k) != tr[k]:
				return false
		return true)
	check("lunge-easing-into-crouch-in-stretch-accelerating-overshoot-out", tr.size() == 7 and tr[0] > 1.0
		and tr[2] > 1.0 and tr[4] > 0.0 and tr[4] < 1.0 and same_everywhere,
		{"transition_from_key_at_frame": FRAMES, "transitions": tr, "same_on_every_pose_track": same_everywhere})

	# Visibility: patrol and dead show the whole Sprite2D, lunge shows the rig.
	var vis := {}
	for n: String in names:
		var anim := ap.get_animation(n)
		var si := AnimChecks.track(anim, "Sprite2D:visible")
		var fi := AnimChecks.track(anim, "Facing:visible")
		vis[n] = [anim.track_get_key_value(si, 0) if si >= 0 else null, anim.track_get_key_value(fi, 0) if fi >= 0 else null]
	var discrete := names.all(func(n: String) -> bool:
		var anim := ap.get_animation(n)
		for p: String in ["Sprite2D:visible", "Facing:visible"]:
			var i := AnimChecks.track(anim, p)
			if i < 0 or anim.value_track_get_update_mode(i) != Animation.UPDATE_DISCRETE or anim.track_get_key_time(i, 0) != 0.0:
				return false
		return true)
	check("visibility-patrol-dead-sprite-lunge-rig", vis.get("patrol") == [true, false] and vis.get("dead") == [true, false]
		and vis.get("lunge") == [false, true] and discrete, {"sprite2d_and_facing_visible": vis, "discrete_at_0": discrete})

	# Rig structure, material and parts.
	var facing := wolf.get_node_or_null("Facing") as Node2D
	var rig := wolf.get_node_or_null("Facing/Rig") as Node2D
	var rear_pivot := wolf.get_node_or_null("Facing/Rig/RearPivot") as Node2D
	var front_pivot := wolf.get_node_or_null("Facing/Rig/FrontPivot") as Node2D
	var rear := wolf.get_node_or_null("Facing/Rig/RearPivot/Rear") as Sprite2D
	var front := wolf.get_node_or_null("Facing/Rig/FrontPivot/Front") as Sprite2D
	var sprite := wolf.get_node("Sprite2D") as Sprite2D
	var nodes_ok := facing != null and rig != null and rear_pivot != null and front_pivot != null and rear != null \
		and front != null and facing.get_class() == "Node2D" and rig.get_class() == "Node2D" \
		and rear_pivot.get_class() == "Node2D" and front_pivot.get_class() == "Node2D"
	check("rig-structure", nodes_ok, {"paths": ["Facing", "Facing/Rig", "Facing/Rig/RearPivot", "Facing/Rig/FrontPivot",
		"Facing/Rig/RearPivot/Rear", "Facing/Rig/FrontPivot/Front"]})
	if not nodes_ok:
		print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
		quit(1)
		return
	check("rig-hidden-at-rest-facing-and-rig-neutral", not facing.visible and sprite.visible
		and facing.transform == Transform2D.IDENTITY and rig.transform == Transform2D.IDENTITY,
		{"facing_visible": facing.visible, "sprite_visible": sprite.visible, "facing": facing.transform, "rig": rig.transform})
	var chain := [rig, rear_pivot, front_pivot, rear, front].all(func(n: CanvasItem) -> bool: return n.use_parent_material)
	check("flash-material-on-facing-parts-use-parent", facing.material is ShaderMaterial
		and (facing.material as ShaderMaterial).shader == (sprite.material as ShaderMaterial).shader and chain,
		{"facing_material_shader": (facing.material as ShaderMaterial).shader.resource_path if facing.material else null,
		"use_parent_material_chain": chain})
	var lunge_tex := load(LUNGE_PNG)
	check("parts-are-regions-of-wolf-lunge", rear.texture == lunge_tex and front.texture == lunge_tex
		and rear.region_enabled and front.region_enabled and rear.region_rect == REAR_REGION
		and front.region_rect == FRONT_REGION and not rear.centered and not front.centered,
		{"rear": rear.region_rect, "front": front.region_rect, "overlap_px": REAR_REGION.end.x - FRONT_REGION.position.x})
	check("pivots-at-measured-hip-and-shoulder", rear_pivot.position == HIP + SPRITE_OFFSET
		and front_pivot.position == SHOULDER + SPRITE_OFFSET,
		{"hip_image_px": HIP, "rear_pivot": rear_pivot.position, "shoulder_image_px": SHOULDER,
		"front_pivot": front_pivot.position})

	# At rest each part draws exactly where the whole Sprite2D draws the same pixels.
	var align := {}
	for part: Sprite2D in [rear, front]:
		var t := to_ancestor(part, wolf)
		var top_left := t * part.offset
		var expected := sprite.offset + part.region_rect.position
		align[part.name] = {"top_left": top_left, "expected": expected, "unrotated_unscaled": t.x == Vector2.RIGHT and t.y == Vector2.DOWN}
	check("parts-draw-where-the-sprite-draws-at-rest", sprite.offset == SPRITE_OFFSET and not sprite.centered
		and align.values().all(func(a: Dictionary) -> bool: return a.top_left == a.expected and a.unrotated_unscaled), align)
	# Facing.scale.x = -1 mirrors about x = 0; flip_h mirrors the Sprite2D's rect about its centre, also x = 0 here.
	var tex_w := float(lunge_tex.get_width())
	check("facing-mirror-equals-flip-h", facing.position == Vector2.ZERO and sprite.offset.x == -tex_w / 2.0,
		{"facing_position": facing.position, "sprite_offset_x": sprite.offset.x, "texture_width": tex_w})

	# The measurements, re-derived from alpha: the split straddles the thinnest torso column, the pivots are on the body.
	var img := Image.load_from_file(ProjectSettings.globalize_path(LUNGE_PNG))
	img.convert(Image.FORMAT_RGBA8)
	var thick := {}
	for x in range(30, 47):
		var y := 0
		while y < img.get_height() and img.get_pixel(x, y).a8 == 0:
			y += 1
		var n := 0
		while y < img.get_height() and img.get_pixel(x, y).a8 > 0:
			n += 1
			y += 1
		thick[x] = n
	var waist: int = thick.keys().reduce(func(a: int, b: int) -> int: return a if thick[a] <= thick[b] else b)
	var on_body := img.get_pixelv(Vector2i(HIP)).a8 > 0 and img.get_pixelv(Vector2i(SHOULDER)).a8 > 0
	check("split-at-waist-pivots-on-body", waist >= FRONT_REGION.position.x and waist < REAR_REGION.end.x and on_body,
		{"torso_thickness_by_column": thick, "waist_x": waist, "overlap_x": [FRONT_REGION.position.x, REAR_REGION.end.x - 1],
		"hip_and_shoulder_opaque": on_body})

	wolf.free()
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
