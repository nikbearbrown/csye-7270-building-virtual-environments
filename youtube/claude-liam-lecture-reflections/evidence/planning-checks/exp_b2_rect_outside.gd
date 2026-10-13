extends SceneTree
# Experiment B2 (Reflections layout): what does a shader read OUTSIDE a rect-mode BackBufferCopy's rectangle?
# Docs (screen-reading shaders): "If set to only a region ... and your shader uses pixels not in the region copied, the result of that
# read is undefined (most likely garbage from previous frames)." So the answer on one machine is only an observation, never a rule.
#
# First run in a fresh process: B2 is the very first thing drawn, so there are no 'previous frames' to leak. Then the sprite colors are
# changed while the rect stays put, to see whether the outside region follows (current) or lags (stale).
# Run: godot --path <scratch project> --script res://exp_b2_rect_outside.gd

const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"
const CLEAR := Color("#D9D5CA")
const SPOTS := {"A_only": Vector2(95, 120), "B_only": Vector2(170, 220), "C_only": Vector2(245, 150)}

var scene: Node2D
var sprites := {}

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, data: Dictionary) -> void:
	data["case"] = id
	print("RESULT " + JSON.stringify(data))

func flat(c: Color, n: int = 100) -> ImageTexture:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(c)
	return ImageTexture.create_from_image(img)

func read(img: Image) -> Dictionary:
	var d := {}
	for k in SPOTS:
		var p: Vector2 = SPOTS[k]
		var pp := Vector2(420 + p.x / 640.0 * 192.0, 20 + p.y / 360.0 * 108.0)
		var c := img.get_pixel(int(pp.x), int(pp.y))
		d[k] = [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]
	return d

func run() -> void:
	RenderingServer.set_default_clear_color(CLEAR)
	root.size = Vector2i(640, 360)
	scene = Node2D.new()
	root.add_child(scene)
	var cols := {"A": Color("#4F8F7E"), "B": Color("#7FA7C9"), "C": Color("#B7A6D9")}
	var posn := {"A": Vector2(120, 150), "B": Vector2(170, 190), "C": Vector2(220, 150)}
	for n in ["A", "B", "C"]:
		var s := Sprite2D.new()
		s.name = n
		s.texture = flat(cols[n])
		s.position = posn[n]
		scene.add_child(s)
		sprites[n] = s
	var b := BackBufferCopy.new()
	b.copy_mode = BackBufferCopy.COPY_MODE_RECT      # node at (0,0), default rect (-100,-100,200,200): copies screen x 0..100, y 0..100 only
	scene.add_child(b)
	var r := ColorRect.new()
	r.position = Vector2(420, 20)
	r.size = Vector2(192, 108)
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(SHADERS + "01-screen-preview.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	r.material = mat
	scene.add_child(r)
	out("env", {"renderer": RenderingServer.get_current_rendering_method(), "clear": [CLEAR.r, CLEAR.g, CLEAR.b]})
	for f in range(1, 5):
		await process_frame
		out("R1-first-frames-rect-default-at-origin-frame-%d" % f, {"preview_reads": read(grab())})
	# change the colors of A and C; the rect still covers none of them
	sprites["A"].texture = flat(Color("#D97757"))
	sprites["C"].texture = flat(Color("#2F6FB0"))
	for f in range(1, 4):
		await process_frame
		out("R2-after-recolouring-A-and-C-frame-%d" % f, {"preview_reads": read(grab()), "expected_if_current": {"A_only": "terracotta-ish 0.851,0.467,0.341", "C_only": "blue 0.184,0.435,0.690"}})
	# same scene, switch the node to viewport mode
	b.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	for f in range(1, 3):
		await process_frame
		out("R3-same-scene-viewport-mode-frame-%d" % f, {"preview_reads": read(grab())})
	# stale-data check: back to rect mode (box still far from the sprites), recolour A again, see whether the OLD colour is read
	b.copy_mode = BackBufferCopy.COPY_MODE_RECT
	sprites["A"].texture = flat(Color("#4F8F7E"))      # teal again
	for f in range(1, 4):
		await process_frame
		out("R4-back-to-rect-A-recoloured-teal-frame-%d" % f, {"preview_reads": read(grab()), "expected_if_current_A": [0.31, 0.561, 0.494], "old_value_A_was": [0.851, 0.467, 0.341]})
	quit(0)
