extends SceneTree
# verify2b: how far does "one copy" reach? Two overlapping invert windows (A, then B drawn after A). Where they overlap, an
# honest double inversion gives back the original colours. A stale copy leaves the overlap inverted once.
#  P1 same canvas (the default 2D canvas, layer 0)        P2 BackBufferCopy between A and B
#  P3 both inside one CanvasLayer (layer 1)               P4 A on layer 1, B on layer 2
#  P5 A and B nested in different Node2D parents, same canvas
#  P6 BackBufferCopy with its default settings (rect mode) between A and B, to see what the defaults do
# Run: ./run.sh verify2b [forward_plus|gl_compatibility]
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
	L.build_world(main, SIZE)

func win(parent: Node, fx: float, fy: float, name: String) -> ColorRect:
	var r := L.rect(Vector2(fx * SIZE.x, fy * SIZE.y), Vector2(0.30 * SIZE.x, 0.30 * SIZE.y), Color.WHITE, name)
	r.material = L.mat_file("03-invert.gdshader")
	parent.add_child(r)
	return r

func report(label: String, base: Image, img: Image) -> void:
	# spots: only A, overlap of A and B, only B, outside both. world colour from the base render of the same spot.
	var spots := {"only_A": Vector2(0.32, 0.30), "overlap": Vector2(0.45, 0.45), "only_B": Vector2(0.58, 0.60), "outside": Vector2(0.15, 0.85)}
	var rows := {}
	for k in spots.keys():
		var p: Vector2 = spots[k]
		var world := L.px(base, p.x, p.y)
		var now := L.px(img, p.x, p.y)
		var inv := [snappedf(1.0 - world[0], 0.0001), snappedf(1.0 - world[1], 0.0001), snappedf(1.0 - world[2], 0.0001)]
		var kind := "other"
		if L.close(now, world, 0.012):
			kind = "world (not inverted, or inverted twice)"
		elif L.close(now, inv, 0.012):
			kind = "inverted once"
		rows[k] = {"world": world, "now": now, "reads_as": kind}
	L.out(label, rows)

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	await fresh()
	await frames(3)
	var base := L.grab(root)

	await fresh()
	win(main, 0.30, 0.20, "A")
	win(main, 0.42, 0.40, "B")
	await frames(4)
	report("P1-same-canvas-no-fix", base, L.grab(root))

	await fresh()
	win(main, 0.30, 0.20, "A")
	var bbc := BackBufferCopy.new()
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	main.add_child(bbc)
	win(main, 0.42, 0.40, "B")
	await frames(4)
	report("P2-same-canvas-with-BackBufferCopy-viewport", base, L.grab(root))

	await fresh()
	var cl := CanvasLayer.new()
	cl.layer = 1
	main.add_child(cl)
	win(cl, 0.30, 0.20, "A")
	win(cl, 0.42, 0.40, "B")
	await frames(4)
	report("P3-both-inside-one-CanvasLayer", base, L.grab(root))

	await fresh()
	var cl1 := CanvasLayer.new()
	cl1.layer = 1
	main.add_child(cl1)
	var cl2 := CanvasLayer.new()
	cl2.layer = 2
	main.add_child(cl2)
	win(cl1, 0.30, 0.20, "A")
	win(cl2, 0.42, 0.40, "B")
	await frames(4)
	report("P4-A-on-layer-1-B-on-layer-2", base, L.grab(root))

	await fresh()
	var n1 := Node2D.new()
	main.add_child(n1)
	var n2 := Node2D.new()
	main.add_child(n2)
	win(n1, 0.30, 0.20, "A")
	win(n2, 0.42, 0.40, "B")
	await frames(4)
	report("P5-nested-in-different-Node2D-parents-same-canvas", base, L.grab(root))

	await fresh()
	win(main, 0.30, 0.20, "A")
	var bbc2 := BackBufferCopy.new()      # all defaults: copy_mode RECT, rect (-100,-100,200,200) around the node's position (origin)
	main.add_child(bbc2)
	win(main, 0.42, 0.40, "B")
	await frames(4)
	L.out("P6-defaults", {"copy_mode_default": bbc2.copy_mode, "rect_default": [bbc2.rect.position.x, bbc2.rect.position.y, bbc2.rect.size.x, bbc2.rect.size.y]})
	report("P6-default-BackBufferCopy-between", base, L.grab(root))

	# P7: z_index. A has z_index 5 although it comes first in the tree; B comes second with z_index 0: B is drawn first.
	await fresh()
	var a7 := win(main, 0.30, 0.20, "A")
	a7.z_index = 5
	win(main, 0.42, 0.40, "B")
	await frames(4)
	report("P7-A-has-z_index-5-so-B-is-drawn-first", base, L.grab(root))
	quit(0)
