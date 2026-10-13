extends SceneTree
# verify5.gd: the hook / sky-window scenes (captures C01, C05, C06): is the sky really locked to the world, and the other really locked
# to its sprite? Uses the real shader files from the film's lab-shaders/ folder and the procedural sky (seed 7, 1536 px, one tile = 512 world px).
#   W1  world sprite: the colour at a fixed screen pixel does not change when the sprite slides; it equals the faint backdrop's sky at that pixel
#   W2  local sprite: the colour at a fixed sprite-relative pixel does not change when the sprite slides; at a fixed screen pixel it does
#   W3  the world sprite turned 45 degrees and stretched: still the same colours at the same screen pixels
#   W4  the planet: the world sprite shows it when it sits over the planet (a landmark reveal), the local sprite never does
# Run: godot --path <project dir> --script res://verify5.gd

const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
var lib
var out_dir := "/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/"


func _initialize() -> void:
	call_deferred("run")


func px(pos: Vector2i) -> Color:
	return lib.grab().get_pixel(pos.x, pos.y)


func rgb8(c: Color) -> Array:
	return [roundi(c.r * 255.0), roundi(c.g * 255.0), roundi(c.b * 255.0)]


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)
	var sky: Texture2D = Scn.sky_texture(1536)
	var backdrop := Scn.sky_rect(Rect2(0, 0, 1280, 720), 0.35)
	root.add_child(backdrop)
	var blob: Texture2D = Scn.blob_texture(128)
	var mat_l := Scn.material("01-sky-local.gdshader", {"sky": sky})
	var mat_w := Scn.material("02-sky-world.gdshader", {"sky": sky})
	var spr_l := Scn.sprite(blob, Vector2(330, 240), 2.0, mat_l)
	var spr_w := Scn.sprite(blob, Vector2(950, 240), 2.0, mat_w)
	root.add_child(spr_l)
	root.add_child(spr_w)
	await lib.frames(4)
	lib.grab().save_png(out_dir + "hook-start.png")

	# a full-opacity reference of the sky (what the world shader should show anywhere): the same shader on a stage-sized rect
	var ref := Scn.sky_rect(Rect2(0, 0, 1280, 720), 1.0)
	ref.visible = false
	root.add_child(ref)
	root.move_child(ref, 0)

	# sample points inside the blob (radius 77 at scale 2), relative offsets
	var offsets := [Vector2i(0, 0), Vector2i(20, -15), Vector2i(-30, 25), Vector2i(45, 10), Vector2i(-50, -20), Vector2i(10, 55), Vector2i(-15, -55), Vector2i(60, -30)]

	# ---- W1: world sprite at x=950, then at x=1000. Pixels at fixed SCREEN positions that stay inside the blob at both x.
	var screen_pts: Array = []
	for o in [Vector2i(0, 0), Vector2i(20, -15), Vector2i(-30, 25), Vector2i(10, 40), Vector2i(-20, -35), Vector2i(35, 5)]:
		screen_pts.append(Vector2i(975, 240) + o)     # inside the blob at x=950 (distance 25+) and at x=1000 (distance 25+)
	spr_w.position.x = 950
	await lib.frames(3)
	var a: Array = []
	for p in screen_pts:
		a.append(rgb8(px(p)))
	spr_w.position.x = 1000
	await lib.frames(3)
	var b: Array = []
	for p in screen_pts:
		b.append(rgb8(px(p)))
	# reference sky at the same pixels
	spr_w.visible = false
	spr_l.visible = false
	backdrop.visible = false
	ref.visible = true
	await lib.frames(3)
	var r_sky: Array = []
	for p in screen_pts:
		r_sky.append(rgb8(px(p)))
	spr_w.visible = true
	spr_l.visible = true
	backdrop.visible = true
	ref.visible = false
	var same_ab := a == b
	var same_ref := a == r_sky
	lib.out("W1-world-sprite-sky-stays-put", {"screen_pixels": screen_pts.map(func(v): return [v.x, v.y]), "colour_when_sprite_at_950": a, "colour_when_sprite_at_1000": b,
		"reference_sky_same_pixels": r_sky, "identical_before_and_after_slide": same_ab, "identical_to_reference_sky": same_ref})

	# ---- W2: local sprite: fixed sprite-relative pixel vs fixed screen pixel, sprite at x=330 then x=380
	spr_l.position.x = 330
	await lib.frames(3)
	var rel_a: Array = []
	var scr_a: Array = []
	for o in offsets:
		rel_a.append(rgb8(px(Vector2i(330, 240) + o)))
		scr_a.append(rgb8(px(Vector2i(355, 240) + o)))   # a screen pixel that stays inside the blob after a 50 px slide
	spr_l.position.x = 380
	await lib.frames(3)
	var rel_b: Array = []
	var scr_b: Array = []
	for o in offsets:
		rel_b.append(rgb8(px(Vector2i(380, 240) + o)))
		scr_b.append(rgb8(px(Vector2i(355, 240) + o)))
	var rel_same := rel_a == rel_b
	var scr_changed := 0
	for i in scr_a.size():
		if scr_a[i] != scr_b[i]:
			scr_changed += 1
	lib.out("W2-local-sprite-sky-rides-along", {"sprite_relative_pixels_identical_after_slide": rel_same, "screen_pixels_changed_of": [scr_changed, scr_a.size()],
		"sample_rel_before": rel_a.slice(0, 3), "sample_rel_after": rel_b.slice(0, 3)})
	lib.grab().save_png(out_dir + "hook-local-moved.png")

	# ---- W3: world sprite as a turned, stretched square
	spr_w.texture = Scn.white_texture(128)
	spr_w.position = Vector2(950, 240)
	spr_w.rotation = 0.0
	spr_w.scale = Vector2(2, 2)
	await lib.frames(3)
	var pts3: Array = [Vector2i(950, 240), Vector2i(960, 250), Vector2i(940, 232), Vector2i(965, 228), Vector2i(938, 255)]
	var c0: Array = []
	for p in pts3:
		c0.append(rgb8(px(p)))
	spr_w.rotation = deg_to_rad(45.0)
	spr_w.scale = Vector2(2.5, 1.6)
	await lib.frames(3)
	var c1: Array = []
	for p in pts3:
		c1.append(rgb8(px(p)))
	lib.out("W3-world-sprite-turned-and-stretched-same-sky", {"before": c0, "after": c1, "identical": c0 == c1})
	lib.grab().save_png(out_dir + "world-square-turned.png")
	spr_w.rotation = 0.0
	spr_w.scale = Vector2(2, 2)
	spr_w.texture = blob

	# ---- W4: planet reveal. Planet centre in tile = (340,240): on stage at x = 340 and 852 (row y=240). Sprite over it shows cream-ish pixels.
	spr_w.position = Vector2(852, 240)
	spr_l.position = Vector2(340, 240)
	await lib.frames(3)
	var c_world := rgb8(px(Vector2i(852, 240)))
	var c_local := rgb8(px(Vector2i(340, 240)))
	lib.out("W4-planet-reveal", {"world_sprite_over_planet_centre_rgb": c_world, "local_sprite_over_planet_centre_rgb": c_local,
		"note": "planet body is cream (about 240,230,207 at the light side); indigo sky is about 91,106,163"})
	lib.grab().save_png(out_dir + "hook-over-planets.png")
	quit(0)
