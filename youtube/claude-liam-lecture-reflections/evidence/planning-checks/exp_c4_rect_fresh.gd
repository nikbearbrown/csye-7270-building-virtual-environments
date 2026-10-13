extends SceneTree
# Experiment C4 (Reflections layout): the pond reflection with the BackBufferCopy in RECT mode, in a FRESH process.
# A fresh process matters: a rect copy leaves everything outside its box untouched, and what is "untouched" depends on history.
# Docs (screen-reading shaders): reads outside the copied region are "undefined (most likely garbage from previous frames)".
#
#   F1  rect mode, the default rect (-100,-100,200,200). Exp H shows the node's position does not move the box, so it copies screen x 0..100, y 0..100
#       only. The shader reads y >= 350.
#   F2  the same node switched to viewport mode at run time.
#   F3  (second fresh process, pass --cover) rect mode with a rect that covers the water: Rect2(0, 300, 1280, 420) (screen coordinates).
#
# Run: godot --path <scratch project> --script res://exp_c4_rect_fresh.gd           (F1, F2)
#      godot --path <scratch project> --script res://exp_c4_rect_fresh.gd -- --cover (F3)
const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"

var char_img: Image
var player: Sprite2D
var reflection: Sprite2D
var bbc: BackBufferCopy

func _initialize() -> void:
	call_deferred("run")

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["case"] = id
	print("RESULT " + JSON.stringify(d))

func visible_reflection_pixels(x: float) -> Array:
	# frame with the reflection vs frame without it, counted in the reflection's own square
	var a := grab()
	reflection.visible = false
	return [a]

func count_diff(a: Image, b: Image, x: float) -> int:
	var n := 0
	var left := int(round(x)) - P.SPRITE_N / 2
	var top := int(round(P.PLAYER_Y + P.REFLECT_OFFSET)) - P.SPRITE_N / 2
	for sy in range(top, top + P.SPRITE_N):
		for sx in range(left, left + P.SPRITE_N):
			var pa := a.get_pixel(sx, sy)
			var pb := b.get_pixel(sx, sy)
			if absf(pa.r - pb.r) + absf(pa.g - pb.g) + absf(pa.b - pb.b) > 0.03:
				n += 1
	return n

func measure(id: String, x: float, extra: Dictionary = {}) -> void:
	for i in range(3):
		await process_frame
	var with_r := grab()
	reflection.visible = false
	for i in range(2):
		await process_frame
	var without_r := grab()
	reflection.visible = true
	var d := {"reflection_pixels_visible": count_diff(with_r, without_r, x), "reference_pixels_if_it_worked": 16237, "renderer": RenderingServer.get_current_rendering_method()}
	d.merge(extra)
	out(id, d)

func run() -> void:
	var cover := "--cover" in OS.get_cmdline_user_args()
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(P.W, P.H)
	char_img = P.make_character_image()
	var scene := Node2D.new()
	root.add_child(scene)
	var mask := Sprite2D.new()
	mask.texture = ImageTexture.create_from_image(P.make_mask_image())
	mask.centered = false
	bbc = BackBufferCopy.new()
	bbc.copy_mode = BackBufferCopy.COPY_MODE_RECT
	if cover:
		bbc.rect = Rect2(0, 300, 1280, 420)
	else:
		bbc.position = Vector2(100, 100)
	var ground := Sprite2D.new()
	ground.texture = ImageTexture.create_from_image(P.make_ground_image())
	ground.centered = false
	player = Sprite2D.new()
	player.texture = ImageTexture.create_from_image(char_img)
	player.position = Vector2(300, P.PLAYER_Y)
	var rt := RemoteTransform2D.new()
	rt.position = Vector2(0, P.REFLECT_OFFSET)
	player.add_child(rt)
	reflection = Sprite2D.new()
	reflection.texture = player.texture
	reflection.flip_v = true
	reflection.material = P.load_shader("02-reflection.gdshader", SHADERS)
	for n in [mask, bbc, ground, player, reflection]:
		scene.add_child(n)
	rt.remote_path = rt.get_path_to(reflection)
	if cover:
		await measure("F3-fresh-rect-box-covers-the-water", 300.0, {"rect": [0, 300, 1280, 420]})
	else:
		await measure("F1-fresh-rect-default-box-far-from-the-mask", 300.0, {"box": "x 0..100, y 0..100 (the default rect, node position ignored)", "reads": "y 350..494"})
		bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
		await measure("F2-same-scene-switched-to-viewport", 300.0)
	quit(0)
