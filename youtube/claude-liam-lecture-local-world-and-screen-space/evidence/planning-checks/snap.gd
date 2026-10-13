extends SceneTree
# snap.gd: frames for looking at (not for numbers): world-field blob with faint backdrop; sky with repeat on / off; pan scene with the corner dot.
const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
var lib
var out_dir := "/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/"


func _initialize() -> void:
	call_deferred("run")


func clear_all() -> void:
	for c in root.get_children():
		c.queue_free()


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)

	# 1. world field on the blob (256 art, scale 1) at x = 700, faint backdrop of the same field
	var back := Scn.sky_rect(Rect2(0, 0, 1280, 720), 0.35, "05-world-field.gdshader")
	back.material = Scn.material("05-world-field.gdshader")
	root.add_child(back)
	var s := Scn.sprite(Scn.blob_texture(256), Vector2(700, 360), 1.0, Scn.material("05-world-field.gdshader"))
	root.add_child(s)
	await lib.frames(4)
	lib.grab().save_png(out_dir + "world-field.png")
	clear_all()
	await lib.frames(2)

	# 2. sky with repeat on / off, whole stage
	var sky: Texture2D = Scn.sky_texture(1536)
	var r1 := ColorRect.new()
	r1.size = Vector2(1280, 720)
	r1.material = Scn.material("02-sky-world.gdshader", {"sky": sky})
	root.add_child(r1)
	await lib.frames(4)
	lib.grab().save_png(out_dir + "sky-repeat-on.png")
	r1.material = Scn.material("06-sky-no-repeat.gdshader", {"sky": sky})
	await lib.frames(4)
	lib.grab().save_png(out_dir + "sky-repeat-off.png")
	clear_all()
	await lib.frames(2)

	# 3. pan scene: world sky backdrop (full opacity), the 128 px sprite at (600,400) with a box outline, camera at (890,460)
	var bg := ColorRect.new()
	bg.position = Vector2(-200, -200)
	bg.size = Vector2(2400, 1400)
	bg.material = Scn.material("02-sky-world.gdshader", {"sky": sky})
	root.add_child(bg)
	var sp := Scn.sprite(Scn.blob_texture(128), Vector2(600, 400), 1.0)
	root.add_child(sp)
	var box := Node2D.new()
	sp.add_child(box)
	box.draw.connect(func():
		box.draw_rect(Rect2(-64, -64, 128, 128), Color("#EDE8DA"), false, 2.0)
		box.draw_circle(Vector2(-64, -64), 6.0, Color("#D97757")))
	box.queue_redraw()
	var cam := Camera2D.new()
	cam.position = Vector2(890, 460)
	root.add_child(cam)
	cam.make_current()
	await lib.frames(5)
	lib.grab().save_png(out_dir + "pan-start.png")
	quit(0)
