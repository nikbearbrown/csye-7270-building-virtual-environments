extends SceneTree
# verify2: what the screen texture can see (Act IV), checked in a real window of Godot 4.7.2.
# The miniature shader (02-miniature: texture(screen_texture, UV)) is used as an X-ray of the copy: it shows exactly what the copy holds.
#  M1 one reader: the copy holds what was drawn BEFORE the reader (X yes), not what is drawn after it (Y no)
#  M2 a second reader reuses the first reader's copy: it lacks the first reader's own output (A) and everything drawn in between
#  M3 a BackBufferCopy (viewport mode) placed before the second reader gives it a fresh copy
#  M4 the same story across CanvasLayers (first reader on layer 0, second on layer 1): the second reader gets its OWN copy (this overturned the plan)
#  M5 a full-screen identity reader on layer 1 after another reader: it changes nothing, so it saw everything (no stale copy across layers)
#  M6 CanvasLayer facts: default layer value, draw order of layers, HUD above / below an effect, tree order inside one layer
#  M7 Full Rect: a ColorRect covers the viewport only when its anchors are set
# Run: ./run.sh verify2 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
const SIZE := Vector2(1280, 720)

var main: Node2D

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func fresh() -> void:
	if main != null:
		main.queue_free()
	await frames(2)
	main = Node2D.new()
	main.name = "Main"
	root.add_child(main)

func block(parent: Node, fx: float, fy: float, fw: float, fh: float, color: Color, name: String) -> ColorRect:
	var r := L.rect(Vector2(fx * SIZE.x, fy * SIZE.y), Vector2(fw * SIZE.x, fh * SIZE.y), color, name)
	parent.add_child(r)
	return r

func reader(parent: Node, fx: float, fy: float, fw: float, fh: float, shader: String, name: String) -> ColorRect:
	var r := block(parent, fx, fy, fw, fh, Color.WHITE, name)
	r.material = L.mat_file(shader)
	return r

func at_frac(img: Image, rect: Rect2, fx: float, fy: float) -> Array:
	return L.px_abs(img, int(rect.position.x + fx * rect.size.x), int(rect.position.y + fy * rect.size.y))

func lens_rows(img: Image, lens: ColorRect, items: Dictionary) -> Dictionary:
	# for each named item, the colour inside the lens where that item's centre would be, and what that colour is
	var rect := Rect2(lens.position, lens.size)
	var out := {}
	for k in items.keys():
		var c: Vector2 = items[k]
		out[k] = at_frac(img, rect, c.x, c.y)
	return out

func scene_order(use_bbc: bool, second_layer: bool) -> Dictionary:
	# world, X (before A), A = invert window, Y (after A), [BackBufferCopy], M = the miniature lens
	await fresh()
	L.build_world(main, SIZE)
	var X := block(main, 0.10, 0.68, 0.10, 0.14, Color("#E0402F"), "X")           # red block, drawn BEFORE every reader
	var A := reader(main, 0.30, 0.20, 0.20, 0.20, "03-invert.gdshader", "A")       # the first reader
	var Y := block(main, 0.70, 0.68, 0.10, 0.14, Color("#2F6FE0"), "Y")           # blue block, drawn AFTER the first reader
	var parent: Node = main
	var cl: CanvasLayer = null
	if second_layer:
		cl = CanvasLayer.new()
		cl.layer = 1
		main.add_child(cl)
		parent = cl
	if use_bbc:
		var bbc := BackBufferCopy.new()
		bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
		parent.add_child(bbc)
	var M := reader(parent, 0.64, 0.04, 0.30, 0.30, "02-miniature.gdshader", "M")
	await frames(4)
	var img := L.grab(root)
	var items := {"X_red": Vector2(0.15, 0.75), "A_window_inverted_world": Vector2(0.40, 0.30), "Y_blue": Vector2(0.75, 0.75), "world_only_spot": Vector2(0.55, 0.55)}
	var world_ref := {}
	for k in items.keys():
		world_ref[k + "_on_screen"] = L.px(img, items[k].x, items[k].y)
	return {"lens": lens_rows(img, M, items), "screen_itself": world_ref}

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	var cl_default := CanvasLayer.new()
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"CanvasLayer_default_layer": cl_default.layer})

	# M1: one reader only (no A): the lens sees X but not Y
	await fresh()
	L.build_world(main, SIZE)
	block(main, 0.10, 0.68, 0.10, 0.14, Color("#E0402F"), "X")
	var M1 := reader(main, 0.64, 0.04, 0.30, 0.30, "02-miniature.gdshader", "M")
	block(main, 0.70, 0.68, 0.10, 0.14, Color("#2F6FE0"), "Y")        # drawn after the lens
	await frames(4)
	var img1 := L.grab(root)
	var items1 := {"X_red_drawn_before": Vector2(0.15, 0.75), "Y_blue_drawn_after": Vector2(0.75, 0.75)}
	L.out("M1-one-reader-sees-only-earlier-nodes", {"lens": lens_rows(img1, M1, items1),
		"screen_itself": {"X": L.px(img1, 0.15, 0.75), "Y": L.px(img1, 0.75, 0.75)}, "reading": "inside the lens, X shows red; where Y would be it shows the world (Y was not drawn yet when the copy was taken)"})

	# M2: second reader reuses the first reader's copy
	var r2 := await scene_order(false, false)
	L.out("M2-second-reader-reuses-first-copy", r2)
	# M3: BackBufferCopy before the second reader
	var r3 := await scene_order(true, false)
	L.out("M3-backbuffercopy-gives-a-fresh-copy", r3)
	# M4: across layers
	var r4 := await scene_order(false, true)
	L.out("M4-second-reader-on-a-higher-layer-gets-its-own-copy", r4)
	var r4b := await scene_order(true, true)
	L.out("M4b-backbuffercopy-inside-the-higher-layer", r4b)

	# M5: a full-screen identity reader on layer 1 after another reader (the plan expected it to erase what was drawn after the first reader's copy; it changed nothing)
	await fresh()
	L.build_world(main, SIZE)
	var Xb := block(main, 0.10, 0.68, 0.10, 0.14, Color("#E0402F"), "X")
	var Ab := reader(main, 0.30, 0.20, 0.20, 0.20, "03-invert.gdshader", "A")
	var Yb := block(main, 0.70, 0.68, 0.10, 0.14, Color("#2F6FE0"), "Y")
	await frames(3)
	var before := L.grab(root)
	var layer1 := CanvasLayer.new()
	layer1.layer = 1
	main.add_child(layer1)
	var full := L.rect(Vector2.ZERO, SIZE, Color.WHITE, "FullScreenReader")
	full.material = L.mat_file("01-window.gdshader")        # the identity reader: should change NOTHING if it saw everything
	layer1.add_child(full)
	await frames(4)
	var after := L.grab(root)
	L.out("M5-full-screen-identity-reader-after-another-reader", {"X_before": L.px(before, 0.15, 0.75), "X_after": L.px(after, 0.15, 0.75),
		"A_before": L.px(before, 0.40, 0.30), "A_after": L.px(after, 0.40, 0.30), "Y_before": L.px(before, 0.75, 0.75), "Y_after": L.px(after, 0.75, 0.75),
		"reading": "an identity reader that saw the whole screen leaves all three unchanged, and it did: a CanvasLayer takes its own copy"})
	var bbc := BackBufferCopy.new()
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	layer1.add_child(bbc)
	layer1.move_child(bbc, 0)
	await frames(4)
	var fixed := L.grab(root)
	L.out("M5b-with-backbuffercopy-first-in-the-layer", {"X": L.px(fixed, 0.15, 0.75), "A": L.px(fixed, 0.40, 0.30), "Y": L.px(fixed, 0.75, 0.75),
		"all_unchanged": L.close(L.px(fixed, 0.15, 0.75), L.px(before, 0.15, 0.75)) and L.close(L.px(fixed, 0.40, 0.30), L.px(before, 0.40, 0.30)) and L.close(L.px(fixed, 0.75, 0.75), L.px(before, 0.75, 0.75))})

	# M6: layers and HUD. World on layer 0; gray-ish effect = invert full-screen on layer 1; HUD in several places
	await fresh()
	L.build_world(main, SIZE)
	var hud0 := block(main, 0.05, 0.05, 0.10, 0.05, Color("#E6B840"), "HudOnLayer0")
	var eff_layer := CanvasLayer.new()
	eff_layer.layer = 1
	main.add_child(eff_layer)
	var hud1_before := block(eff_layer, 0.20, 0.05, 0.10, 0.05, Color("#E6B840"), "HudLayer1BeforeEffect")
	var eff := reader(eff_layer, 0, 0, 1, 1, "03-invert.gdshader", "Effect")
	var hud1_after := block(eff_layer, 0.35, 0.05, 0.10, 0.05, Color("#E6B840"), "HudLayer1AfterEffect")
	var hud_layer := CanvasLayer.new()
	hud_layer.layer = 2
	main.add_child(hud_layer)
	var hud2 := block(hud_layer, 0.50, 0.05, 0.10, 0.05, Color("#E6B840"), "HudOnLayer2")
	var low_layer := CanvasLayer.new()
	low_layer.layer = -1
	main.add_child(low_layer)
	var hud_m1 := block(low_layer, 0.65, 0.05, 0.10, 0.05, Color("#E6B840"), "HudOnLayerMinus1")
	await frames(4)
	var img6 := L.grab(root)
	var mustard := [0.902, 0.7216, 0.251]
	L.out("M6-layers-and-hud", {"effect_is_invert_so_mustard_becomes": [snappedf(1.0 - mustard[0], 0.001), snappedf(1.0 - mustard[1], 0.001), snappedf(1.0 - mustard[2], 0.001)],
		"hud_on_layer0 (below the effect)": L.px(img6, 0.10, 0.075), "hud_layer1_before_effect (drawn before it)": L.px(img6, 0.25, 0.075),
		"hud_layer1_after_effect (drawn after it)": L.px(img6, 0.40, 0.075), "hud_on_layer2 (above)": L.px(img6, 0.55, 0.075),
		"block_on_layer_minus1 (behind the game layer; hidden by the world?)": L.px(img6, 0.70, 0.075)})

	# M7: Full Rect
	await fresh()
	var cl7 := CanvasLayer.new()
	main.add_child(cl7)
	var plain := ColorRect.new()
	cl7.add_child(plain)
	var anchored := ColorRect.new()
	cl7.add_child(anchored)
	anchored.set_anchors_preset(Control.PRESET_FULL_RECT)
	await frames(3)
	L.out("M7-full-rect", {"viewport_size": [root.size.x, root.size.y], "colorrect_without_layout_size": [plain.size.x, plain.size.y], "colorrect_full_rect_size": [anchored.size.x, anchored.size.y], "full_rect_position": [anchored.position.x, anchored.position.y]})
	quit(0)
