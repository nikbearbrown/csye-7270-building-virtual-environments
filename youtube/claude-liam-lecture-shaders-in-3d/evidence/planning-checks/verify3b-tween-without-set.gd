extends SceneTree
# EXPECTED TO FAIL (kept on purpose): the same tween as verify3-attach-set-tween.gd, but WITHOUT the first line
# (material.set_shader_parameter("activation", 0.0)). In 2D, Godot 4.7.2 refused such a tween ("The tweened property ... does not exist");
# this run checks that a 3D mesh's ShaderMaterial behaves the same way.
# Run:  ./run-script.sh verify3b-tween-without-set.gd run-3b-tween-without-set-FAILS-as-expected.log

const HOLDER := "extends Node3D\n\nfunc animate_without_the_first_line():\n\tvar material = $Pad.material_override\n\tvar tween := create_tween()\n\ttween.tween_property(material, \"shader_parameter/activation\", 1.0, 1.0)\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func probe() -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var ppu := img.get_height() / 2.0
	var x := int(img.get_width() / 2.0 + (0.09375 - 0.5) * 1.8 * ppu)
	var c := img.get_pixel(x, img.get_height() / 2)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(640, 360)
	var stage := Node3D.new()
	var scr := GDScript.new()
	scr.source_code = HOLDER
	var err := scr.reload()
	stage.set_script(scr)
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 2.0
	cam.position = Vector3(0, 0, 3)
	stage.add_child(cam)
	cam.current = true
	var pad := MeshInstance3D.new()
	pad.name = "Pad"
	var q := QuadMesh.new()
	q.size = Vector2(1.8, 1.8)
	pad.mesh = q
	var m := ShaderMaterial.new()
	m.shader = load("res://pad.gdshader")
	pad.material_override = m
	stage.add_child(pad)
	await frames(3)
	var before := probe()
	stage.animate_without_the_first_line()
	await create_timer(1.3).timeout
	var after := probe()
	out("TWEEN-WITHOUT-SET", {"script_reload_error": err, "before": before, "after_1.3_s": after, "unchanged": before == after,
		"get_shader_parameter": str(m.get_shader_parameter("activation")), "expected": "an engine error line above this RESULT, and an unchanged pixel"})
	quit(0)
