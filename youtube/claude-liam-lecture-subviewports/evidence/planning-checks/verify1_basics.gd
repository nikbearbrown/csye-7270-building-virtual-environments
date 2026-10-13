extends SceneTree
# SubViewports film, check 1: the basics, measured in a real window of Godot 4.7.2, at the film's own sizes (512 px picture, 448 px test sprite).
#  A1  a child of a SubViewport is NOT drawn on the screen
#  A2  the ViewportTexture on a Sprite2D shows the picture, upright
#  A3  a new SubViewport is 512 x 512
#  B1  size is the picture's resolution: a 128 px picture drawn 4x is soft with the linear filter and blocky with the nearest filter
#  C1  the origin is the top-left corner: a centred sprite at (0,0) shows a quarter (and no eyes); in the middle it is whole; on an edge, half; far outside, none
#  D1  transparent_bg off: the empty parts hold the default clear colour; on: alpha 0 and the stage shows through
#  E1-E5  update modes: default follows changes; a hidden display stops the picture; UPDATE_ONCE draws once; UPDATE_DISABLED never draws
#  X2  a Camera2D inside the viewport makes (0,0) the middle of the picture
# Run: godot --path <project> --fixed-fps 30 --script res://verify1_basics.gd      (add --rendering-method gl_compatibility for the second renderer)

const CLEAR := Common.CLEAR
const STAGE := Common.STAGE

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func sprite(pos: Vector2, size: int = 448, bleed: bool = true) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = ImageTexture.create_from_image(CaptureScene.blob_image(size, bleed))
	s.position = pos
	return s

func count_color(img: Image, target: Color, tol: float = 0.03) -> int:
	var n := 0
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			if c.a > 0.5 and Common.diff(c, target) < tol:
				n += 1
	return n

func first_x(img: Image, target: Color, tol: float = 0.03) -> int:
	for x in img.get_width():
		for y in img.get_height():
			var c := img.get_pixel(x, y)
			if c.a > 0.5 and Common.diff(c, target) < tol:
				return x
	return -1

func run() -> void:
	RenderingServer.set_default_clear_color(CLEAR)
	root.size = Vector2i(1280, 720)
	var info := Engine.get_version_info()
	Common.out("env", {"engine": info["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "clear_colour": Common.rgba(CLEAR)})
	var eye := Color("#FAF9F5")

	var stage_rect := ColorRect.new()
	stage_rect.color = STAGE
	stage_rect.size = Vector2(1280, 720)
	root.add_child(stage_rect)

	# ---------------------------------------------------------------- A3: the default size
	var fresh := SubViewport.new()
	Common.out("A3-default-size", {"new_SubViewport_size": [fresh.size.x, fresh.size.y], "default_update_mode": fresh.render_target_update_mode, "default_clear_mode": fresh.render_target_clear_mode, "default_transparent_bg": fresh.transparent_bg, "reading": "docs: size defaults to Vector2i(512, 512); update mode 2 = when visible; clear mode 0 = always"})
	fresh.free()

	# ---------------------------------------------------------------- A1, A2
	var sub := SubViewport.new()
	sub.size = Vector2i(512, 512)
	root.add_child(sub)
	var inner := sprite(Vector2(256, 256))
	sub.add_child(inner)
	var marker := ColorRect.new()          # a red 32 px marker at the picture's top-left, to test orientation
	marker.color = Color(1, 0, 0, 1)
	marker.size = Vector2(32, 32)
	sub.add_child(marker)
	await frames(3)
	var img := main_img()
	Common.out("A1-child-not-on-screen", {"main_pixel_where_the_sprite_would_be": Common.rgb(img.get_pixel(256, 256)), "stage": Common.rgb(STAGE), "reading": "equal to the stage colour: the SubViewport's child is not drawn on the main screen"})
	var disp := Sprite2D.new()
	disp.centered = false
	disp.position = Vector2(384, 104)
	disp.texture = sub.get_texture()
	root.add_child(disp)
	await frames(3)
	img = main_img()
	var tex := sub.get_texture()
	Common.out("A2-viewporttexture-shows-the-picture", {"class": tex.get_class(), "texture_size": [tex.get_width(), tex.get_height()],
		"display_centre": Common.rgb(img.get_pixel(384 + 256, 104 + 256)), "display_marker_at_top_left": Common.rgb(img.get_pixel(384 + 8, 104 + 8)),
		"display_bottom_left_is_not_the_marker": Common.rgb(img.get_pixel(384 + 8, 104 + 504)), "display_empty_corner": Common.rgb(img.get_pixel(384 + 500, 104 + 500)),
		"reading": "teal at the centre = the picture shows the sprite; red at the top-left = upright; the empty corner is the clear colour (the box)"})

	# ---------------------------------------------------------------- C1: origin, quarter, eyes, cut off
	marker.visible = false
	var sizes: Dictionary = {}
	for k: Array in [["whole_in_middle", Vector2(256, 256)], ["at_0_0", Vector2(0, 0)], ["centre_on_right_edge", Vector2(512, 256)], ["far_outside", Vector2(800, 256)]]:
		inner.position = k[1]
		await frames(3)
		var pic := tex.get_image()
		sizes[k[0]] = {"teal_pixels": count_color(pic, Common.TEAL), "eye_pixels": count_color(pic, eye)}
	var whole: int = sizes["whole_in_middle"]["teal_pixels"]
	Common.out("C1-origin-and-cut-off", {"counts": sizes, "fraction_of_the_whole_blob_at_0_0": snappedf(float(sizes["at_0_0"]["teal_pixels"]) / float(whole), 0.001), "fraction_on_the_right_edge": snappedf(float(sizes["centre_on_right_edge"]["teal_pixels"]) / float(whole), 0.001),
		"reading": "at (0,0) about a quarter of the blob is in the picture and none of the eyes; on the right edge about half; far outside none"})

	# ---------------------------------------------------------------- D1: transparent_bg
	inner.position = Vector2(256, 256)
	sub.transparent_bg = false
	await frames(3)
	var pic_off := tex.get_image().get_pixel(20, 20)
	var scr_off := main_img().get_pixel(384 + 20, 104 + 20)
	sub.transparent_bg = true
	await frames(3)
	var pic_on := tex.get_image().get_pixel(20, 20)
	var scr_on := main_img().get_pixel(384 + 20, 104 + 20)
	Common.out("D1-transparent-bg", {"picture_empty_pixel_off": Common.rgba(pic_off), "screen_there_off": Common.rgb(scr_off), "picture_empty_pixel_on": Common.rgba(pic_on), "screen_there_on": Common.rgb(scr_on), "stage": Common.rgb(STAGE), "clear": Common.rgb(CLEAR),
		"reading": "off: the empty part is the clear colour with alpha 1; on: alpha 0 and the stage shows through"})

	# ---------------------------------------------------------------- E: update modes
	inner.position = Vector2(100, 256)
	await frames(3)
	var xa := first_x(tex.get_image(), Common.TEAL)
	inner.position = Vector2(300, 256)
	await frames(3)
	var xb := first_x(tex.get_image(), Common.TEAL)
	Common.out("E1-default-follows-changes", {"update_mode": sub.render_target_update_mode, "first_teal_x_before": xa, "first_teal_x_after_moving_200px": xb, "reading": "default (When Visible): the picture follows the sprite"})
	disp.visible = false
	await frames(3)
	inner.position = Vector2(200, 256)
	await frames(3)
	var x_hidden := first_x(tex.get_image(), Common.TEAL)
	disp.visible = true
	await frames(3)
	var x_shown := first_x(tex.get_image(), Common.TEAL)
	Common.out("E2-hidden-display-stops-the-picture", {"x_before_hiding": xb, "x_while_the_display_is_hidden": x_hidden, "x_after_showing_again": x_shown, "reading": "while hidden the picture keeps its last drawing (x unchanged); shown again it catches up (sprite now at 200, so its left edge is 200 - 134 = 66)"})
	sub.render_target_update_mode = SubViewport.UPDATE_ONCE
	await frames(3)
	var o1 := first_x(tex.get_image(), Common.TEAL)
	inner.position = Vector2(350, 256)
	await frames(3)
	var o2 := first_x(tex.get_image(), Common.TEAL)
	Common.out("E3-update-once", {"property_reads": sub.render_target_update_mode, "x_after_once": o1, "x_after_moving_the_sprite": o2, "reading": "the picture drew once and then stopped following (x unchanged); the property still reads 1 (Once)"})
	sub.render_target_update_mode = SubViewport.UPDATE_ONCE
	await frames(3)
	Common.out("E4-update-once-again", {"x_after_a_second_once": first_x(tex.get_image(), Common.TEAL), "reading": "setting Once again redraws exactly once: the picture catches up (sprite at 350, left edge 350 - 134 = 216)"})
	# ---------------------------------------------------------------- B1: size is resolution
	var small := SubViewport.new()
	small.size = Vector2i(128, 128)
	root.add_child(small)
	small.add_child(sprite(Vector2(64, 64), 128))
	var big_disp := Sprite2D.new()
	big_disp.centered = false
	big_disp.position = Vector2(700, 100)
	big_disp.scale = Vector2(4, 4)
	big_disp.texture = small.get_texture()
	big_disp.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	root.add_child(big_disp)
	await frames(4)
	var row_y := 100 + 4 * 64
	var results: Dictionary = {}
	for mode: Array in [["linear", CanvasItem.TEXTURE_FILTER_LINEAR], ["nearest", CanvasItem.TEXTURE_FILTER_NEAREST]]:
		big_disp.texture_filter = mode[1]
		await frames(3)
		img = main_img()
		# along the row through the blob's centre, count pixels that are neither the clear colour nor teal (the soft edge), and list run lengths
		var soft := 0
		var runs: Array = []
		var cur := Color(-1, -1, -1, -1)
		var l := 0
		for x in range(700, 700 + 512):
			var c := img.get_pixel(x, row_y)
			if Common.diff(c, CLEAR) > 0.02 and Common.diff(c, Common.TEAL) > 0.02:
				soft += 1
			if c.is_equal_approx(cur):
				l += 1
			else:
				if l > 0: runs.append(l)
				cur = c
				l = 1
		runs.append(l)
		var mult4 := true
		for r: int in runs:
			if r % 4 != 0:
				mult4 = false
		results[mode[0]] = {"soft_edge_pixels_on_the_row": soft, "run_lengths": runs.slice(0, 8), "every_run_a_multiple_of_4": mult4}
	Common.out("B1-size-is-resolution", {"viewport_size": [small.size.x, small.size.y], "texture_size": [small.get_texture().get_width(), small.get_texture().get_height()], "drawn_at_scale": 4, "by_filter": results, "reading": "the 128 px picture drawn 4x: with Linear the edge is a soft ramp of several pixels; with Nearest it is a hard step and every run is a multiple of 4 screen pixels"})

	# ---------------------------------------------------------------- X2: Camera2D inside the viewport
	var sub3 := SubViewport.new()
	sub3.size = Vector2i(512, 512)
	sub3.transparent_bg = true
	root.add_child(sub3)
	var s3 := sprite(Vector2(0, 0))
	sub3.add_child(s3)
	var d3 := Sprite2D.new()                 # something must draw the picture, or (By default) the viewport never renders
	d3.texture = sub3.get_texture()
	d3.scale = Vector2(0.1, 0.1)
	d3.position = Vector2(60, 60)
	root.add_child(d3)
	await frames(4)
	var c_none := count_color(sub3.get_texture().get_image(), Common.TEAL)
	var cam := Camera2D.new()
	sub3.add_child(cam)
	cam.make_current()
	await frames(4)
	var c_cam := count_color(sub3.get_texture().get_image(), Common.TEAL)
	s3.position = Vector2(256, 256)
	cam.enabled = false
	await frames(4)
	var c_whole := count_color(sub3.get_texture().get_image(), Common.TEAL)
	Common.out("X2-camera2d-inside-the-viewport", {"anchor_mode": cam.anchor_mode, "teal_at_0_0_without_camera": c_none, "teal_at_0_0_with_camera_at_0_0": c_cam, "teal_whole_sprite": c_whole, "reading": "a Camera2D inside the viewport makes (0, 0) the middle of the picture: the whole sprite shows (same count as the whole sprite)"})
	# ---------------------------------------------------------------- X4: text and interface can go inside (a Label and a Button, drawn into the picture)
	var sub4 := SubViewport.new()
	sub4.size = Vector2i(320, 120)
	sub4.transparent_bg = true
	root.add_child(sub4)
	var lbl := Label.new()
	lbl.text = "SubViewport"
	lbl.add_theme_font_size_override("font_size", 40)
	lbl.add_theme_color_override("font_color", Common.TEAL)
	sub4.add_child(lbl)
	var btn := Button.new()
	btn.text = "button"
	btn.position = Vector2(10, 60)
	sub4.add_child(btn)
	var d4 := Sprite2D.new()
	d4.texture = sub4.get_texture()
	d4.scale = Vector2(0.5, 0.5)
	d4.position = Vector2(1000, 650)
	root.add_child(d4)
	await frames(5)
	var pic4 := sub4.get_texture().get_image()
	var text_px := count_color(pic4, Common.TEAL, 0.05)
	var non_empty := 0
	for y in pic4.get_height():
		for x in pic4.get_width():
			if pic4.get_pixel(x, y).a > 0.5:
				non_empty += 1
	Common.out("X4-text-and-interface-inside-a-viewport", {"label_pixels_in_the_label_colour": text_px, "pixels_with_alpha_above_half_in_the_picture": non_empty, "reading": "a Label and a Button drawn inside a SubViewport appear in its picture (teal text pixels and button pixels are present)"})
	# ---------------------------------------------------------------- E5 (kept last: in an early run, with waiting-only frames, a viewport created AFTER an opaque UPDATE_DISABLED one stopped updating; with one forced draw per step the order no longer matters, RESULTS.md)
	var sub2 := SubViewport.new()
	sub2.size = Vector2i(64, 64)
	sub2.render_target_update_mode = SubViewport.UPDATE_DISABLED
	root.add_child(sub2)
	sub2.add_child(sprite(Vector2(32, 32), 64))
	var d2 := Sprite2D.new()
	d2.texture = sub2.get_texture()
	d2.position = Vector2(100, 600)
	root.add_child(d2)
	await frames(4)
	Common.out("E5-update-disabled", {"teal_pixels": count_color(sub2.get_texture().get_image(), Common.TEAL), "reading": "Disabled from the start: nothing was ever drawn into the picture"})

	quit(0)
