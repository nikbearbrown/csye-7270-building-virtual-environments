extends RefCounted
# vscene.gd: the test objects of the Vertex Shaders film, built in code (no assets), shared by every planning check.
# The capture harness for the build can reuse these builders: they are the exact node setups the captures describe.
# Stage colour and the two texture colours match the Shader Lab (lab/runner.gd).

const STAGE := Color("#D9D5CA")
const TEAL := Color("#5FA391")
const CREAM := Color("#FAF9F5")


# ---- paths: this project lives in <film>/evidence/planning-checks/scratch-project/ ----
static func film_dir() -> String:
	return ProjectSettings.globalize_path("res://").path_join("../../..").simplify_path()

static func lab_shader(n: String) -> String:
	return film_dir().path_join("lab-shaders").path_join(n + ".gdshader")

static func check_shader(n: String) -> String:
	return film_dir().path_join("evidence/planning-checks/check-shaders").path_join(n + ".gdshader")

static func png_dir() -> String:
	return film_dir().path_join("evidence/planning-checks/png")

static func setup(root: Window, w: int, h: int) -> void:
	RenderingServer.set_default_clear_color(STAGE)
	root.size = Vector2i(w, h)
	# Keep the window on top: a covered window stops being drawn, and a shader's TIME stops advancing with it (seen twice when other Godot windows opened).
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)
	DisplayServer.window_move_to_foreground()

static func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

static func checker_image(w: int, h: int, cell: int = 16) -> Image:
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	for y in h:
		for x in w:
			var on := (int(x / cell) + int(y / cell)) % 2 == 0
			img.set_pixel(x, y, CREAM if on else TEAL)
	return img

static func white_image(w: int, h: int) -> Image:
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	return img

# The Lab's "sprite": a teal blob with two cream eyes (above the middle) and transparent padding.
static func blob_image(n: int = 128) -> Image:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			var d := Vector2(x, y).distance_to(c)
			if d < n * 0.30:
				img.set_pixel(x, y, TEAL)
			var e1 := Vector2(x, y).distance_to(c + Vector2(-n * 0.10, -n * 0.06))
			var e2 := Vector2(x, y).distance_to(c + Vector2(n * 0.10, -n * 0.06))
			if e1 < n * 0.035 or e2 < n * 0.035:
				img.set_pixel(x, y, CREAM)
	return img

static func material_from(path: String, uniforms: Dictionary = {}) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(path)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	for k in uniforms:
		mat.set_shader_parameter(k, uniforms[k])
	return mat

static func sprite(img: Image, pos: Vector2, scale: float = 1.0, mat: Material = null) -> Sprite2D:
	var sp := Sprite2D.new()
	sp.texture = ImageTexture.create_from_image(img)
	sp.position = pos
	sp.scale = Vector2(scale, scale)
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.material = mat
	return sp

# A flat QuadMesh drawn by a MeshInstance2D. size is in pixels; sub_w / sub_d are the QuadMesh subdivide_width / subdivide_depth.
static func quad(size: Vector2, sub_w: int, sub_d: int, img: Image, pos: Vector2, mat: Material = null) -> MeshInstance2D:
	var q := QuadMesh.new()
	q.size = size
	q.subdivide_width = sub_w
	q.subdivide_depth = sub_d
	var mi := MeshInstance2D.new()
	mi.mesh = q
	mi.texture = ImageTexture.create_from_image(img)
	mi.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	mi.position = pos
	mi.material = mat
	return mi

static func grab(root: Window) -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

static func frames(tree: SceneTree, n: int) -> void:
	for i in range(n):
		await tree.process_frame
