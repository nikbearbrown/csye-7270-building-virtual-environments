extends SceneTree
# verify1: Act I claims about the screen texture, checked in a real window of Godot 4.7.2.
#  A  the smallest reader (01-window) makes a rect vanish: its pixels equal what is behind it
#  B  the same shader keeps the sprite's own alpha when only COLOR.rgb is written (padding stays untouched)
#  C  texture(screen_texture, UV) (02-miniature) shows the whole screen shrunk into the rect; SCREEN_UV does not
#  D  03-invert: exactly 1 - what is behind
#  E  the screen uniform is not listed among the shader's parameters; setting it by hand changes nothing
#  F  the uniform's name is free; texture() and textureLod(..., 0.0) read the same pixels
# Run: ./run.sh verify1 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
const SIZE := Vector2(1280, 720)

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func same(a: Image, b: Image, rect: Rect2i, tol: float = 0.006) -> Dictionary:
	var worst := 0.0
	var n := 0
	for y in range(rect.position.y, rect.end.y, 3):
		for x in range(rect.position.x, rect.end.x, 3):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			worst = maxf(worst, maxf(absf(ca.r - cb.r), maxf(absf(ca.g - cb.g), absf(ca.b - cb.b))))
			n += 1
	return {"samples": n, "worst_channel_diff": snappedf(worst, 0.0001), "within_tol": worst <= tol}

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	var main := Node2D.new()
	main.name = "Main"
	root.add_child(main)
	L.build_world(main, SIZE)
	await frames(3)
	var base := L.grab(root)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "size": [base.get_width(), base.get_height()]})

	# A: the window vanishes
	var win := L.rect(Vector2(0.55 * SIZE.x, 0.20 * SIZE.y), Vector2(384, 216), L.TEAL, "Win")
	main.add_child(win)
	await frames(3)
	var plain := L.grab(root)
	var wr := Rect2i(int(win.position.x) + 4, int(win.position.y) + 4, 376, 208)
	L.out("A0-plain-rect-differs-from-world", {"centre_world": L.px_abs(base, int(win.position.x) + 192, int(win.position.y) + 108), "centre_with_plain_rect": L.px_abs(plain, int(win.position.x) + 192, int(win.position.y) + 108)})
	win.material = L.mat_file("01-window.gdshader")
	await frames(3)
	var with_shader := L.grab(root)
	L.out("A-window-vanishes", {"compare": "rect interior with 01-window vs the world alone", "result": same(with_shader, base, wr)})

	# B: alpha is kept (sprite with transparent padding): the padding stays the world, the blob becomes a window
	win.queue_free()
	await frames(2)
	var spr := L.make_player(Vector2(0.30 * SIZE.x, 0.55 * SIZE.y), 1.5)
	main.add_child(spr)
	await frames(3)
	var with_blob := L.grab(root)
	spr.material = L.mat_file("01-window.gdshader")
	await frames(3)
	var blob_window := L.grab(root)
	var sr := Rect2i(int(spr.position.x - 96), int(spr.position.y - 96), 192, 192)
	L.out("B-sprite-window", {"plain_blob_centre": L.px_abs(with_blob, int(spr.position.x), int(spr.position.y + 40)), "after_shader_centre": L.px_abs(blob_window, int(spr.position.x), int(spr.position.y + 40)),
		"world_centre": L.px_abs(base, int(spr.position.x), int(spr.position.y + 40)), "whole_sprite_rect_equals_world": same(blob_window, base, sr)})
	spr.queue_free()
	await frames(2)

	# C: miniature (UV) vs window (SCREEN_UV) on a 16:9 rect: which one equals the world at the SAME place, which one equals it at the SAME FRACTION
	var mini := L.rect(Vector2(0.62 * SIZE.x, 0.10 * SIZE.y), Vector2(320, 180), Color.WHITE, "Mini")
	mini.material = L.mat_file("02-miniature.gdshader")
	main.add_child(mini)
	await frames(3)
	var m_img := L.grab(root)
	var fr: Array = []
	for f in [[0.15, 0.2], [0.5, 0.5], [0.85, 0.8], [0.3, 0.7]]:
		var inside: Array = L.px_abs(m_img, int(mini.position.x + f[0] * 320), int(mini.position.y + f[1] * 180))
		var as_fraction: Array = L.px(base, f[0], f[1])
		var as_place: Array = L.px_abs(base, int(mini.position.x + f[0] * 320), int(mini.position.y + f[1] * 180))
		fr.append({"fraction": f, "inside_rect": inside, "world_at_same_fraction_of_screen": as_fraction, "world_at_same_place": as_place,
			"matches_fraction": L.close(inside, as_fraction, 0.02), "matches_place": L.close(inside, as_place, 0.02)})
	L.out("C-miniature", {"rows": fr})
	mini.material = L.mat_file("01-window.gdshader")
	await frames(3)
	var w_img := L.grab(root)
	var fr2: Array = []
	for f in [[0.15, 0.2], [0.5, 0.5], [0.85, 0.8], [0.3, 0.7]]:
		var inside2: Array = L.px_abs(w_img, int(mini.position.x + f[0] * 320), int(mini.position.y + f[1] * 180))
		var as_place2: Array = L.px_abs(base, int(mini.position.x + f[0] * 320), int(mini.position.y + f[1] * 180))
		fr2.append({"fraction": f, "inside_rect": inside2, "world_at_same_place": as_place2, "matches_place": L.close(inside2, as_place2, 0.01)})
	L.out("C2-same-rect-with-SCREEN_UV", {"rows": fr2})
	mini.queue_free()
	await frames(2)

	# D: invert
	var inv := L.rect(Vector2(0.10 * SIZE.x, 0.30 * SIZE.y), Vector2(320, 180), Color.WHITE, "Inv")
	inv.material = L.mat_file("03-invert.gdshader")
	main.add_child(inv)
	await frames(3)
	var i_img := L.grab(root)
	var worst := 0.0
	for y in range(int(inv.position.y) + 2, int(inv.position.y) + 178, 3):
		for x in range(int(inv.position.x) + 2, int(inv.position.x) + 318, 3):
			var a := base.get_pixel(x, y)
			var b := i_img.get_pixel(x, y)
			worst = maxf(worst, maxf(absf((1.0 - a.r) - b.r), maxf(absf((1.0 - a.g) - b.g), absf((1.0 - a.b) - b.b))))
	L.out("D-invert", {"worst_channel_diff_from_1_minus_world": snappedf(worst, 0.0001), "sample_world": L.px_abs(base, int(inv.position.x) + 40, int(inv.position.y) + 40), "sample_inverted": L.px_abs(i_img, int(inv.position.x) + 40, int(inv.position.y) + 40)})

	# E: not listed as a parameter; hand-setting it is ignored
	var sh: Shader = inv.material.shader
	var names: Array = []
	for u in sh.get_shader_uniform_list():
		names.append(u["name"])
	var hand := Image.create(4, 4, false, Image.FORMAT_RGBA8)
	hand.fill(Color(1, 0, 1, 1))
	(inv.material as ShaderMaterial).set_shader_parameter("screen_texture", ImageTexture.create_from_image(hand))
	await frames(3)
	var h_img := L.grab(root)
	L.out("E-not-a-parameter", {"uniform_list_of_03-invert": names, "after_hand_set_magenta_texture_pixel": L.px_abs(h_img, int(inv.position.x) + 40, int(inv.position.y) + 40), "same_as_before": L.close(L.px_abs(h_img, int(inv.position.x) + 40, int(inv.position.y) + 40), L.px_abs(i_img, int(inv.position.x) + 40, int(inv.position.y) + 40), 0.01)})
	inv.queue_free()
	await frames(2)

	# F: another name, and texture() against textureLod()
	var f1 := L.rect(Vector2(0.10 * SIZE.x, 0.55 * SIZE.y), Vector2(200, 120), Color.WHITE, "F1")
	f1.material = L.mat_from("shader_type canvas_item;\nuniform sampler2D behind : hint_screen_texture;\nvoid fragment() { COLOR.rgb = texture(behind, SCREEN_UV).rgb; }\n")
	var f2 := L.rect(Vector2(0.35 * SIZE.x, 0.55 * SIZE.y), Vector2(200, 120), Color.WHITE, "F2")
	f2.material = L.mat_from("shader_type canvas_item;\nuniform sampler2D screen_texture : hint_screen_texture;\nvoid fragment() { COLOR.rgb = textureLod(screen_texture, SCREEN_UV, 0.0).rgb; }\n")
	main.add_child(f1)
	main.add_child(f2)
	await frames(3)
	var f_img := L.grab(root)
	L.out("F-name-free-and-texture-vs-textureLod", {"renamed_uniform_vanishes": same(f_img, base, Rect2i(int(f1.position.x) + 3, int(f1.position.y) + 3, 194, 114)),
		"textureLod_lod0_vanishes": same(f_img, base, Rect2i(int(f2.position.x) + 3, int(f2.position.y) + 3, 194, 114))})
	quit(0)
