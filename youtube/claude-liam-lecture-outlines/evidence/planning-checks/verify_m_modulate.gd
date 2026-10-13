extends SceneTree
# M: the node's modulate. A shader that assigns COLOR from texture(TEXTURE, UV) ignores it. Three sprites, each with modulate alpha 0.5 (a fade half done):
#    left   no shader: the sprite is half transparent
#    middle 06-pixel-steps (COLOR assigned from the texture): modulate ignored, the sprite and its line are fully opaque
#    right  14-modulate (vertex COLOR passed on as a varying and multiplied in): half transparent again, line included
# Each is rendered on black and on white so the alpha the shader wrote can be solved from the screen.
# Run: godot --path <scratch project> --script res://verify_m_modulate.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	root.size = Vector2i(640, 360)
	var line := Color(0.25, 0.25, 0.75, 1.0)
	var tex := ImageTexture.create_from_image(Lib.blob(128))
	var mats := [null, Lib.material("06-pixel-steps.gdshader", {"thickness": 2.0, "line_color": line}), Lib.material("14-modulate.gdshader", {"thickness": 2.0, "line_color": line})]
	var nodes: Array = []
	for k in range(3):
		var sp := Sprite2D.new()
		sp.texture = tex
		sp.centered = false
		sp.position = Vector2(20 + k * 200, 116)
		sp.scale = Vector2(1.5, 1.5)
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		sp.modulate = Color(1, 1, 1, 0.5)
		sp.material = mats[k]
		root.add_child(sp)
		nodes.append(sp)
	for bg in [["black", Color(0, 0, 0)], ["white", Color(1, 1, 1)]]:
		RenderingServer.set_default_clear_color(bg[1])
		await frames(3)
		Lib.save(Lib.snap(root), OUT + "/modulate-on-" + bg[0] + ".png")
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	quit(0)
