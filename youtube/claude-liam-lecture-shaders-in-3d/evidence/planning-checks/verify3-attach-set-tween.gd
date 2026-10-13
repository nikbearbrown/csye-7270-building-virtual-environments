extends SceneTree
# Claims checked (Shaders in 3D), with the GDScript lines exactly as the film shows them:
#   ATTACH   : a MeshInstance3D takes a ShaderMaterial in its material_override slot, and the shader draws the mesh
#              var material := ShaderMaterial.new()
#              material.shader = load("res://pad.gdshader")
#              $Pad.material_override = material
#   SET      : $Pad.material_override.set_shader_parameter("activation", 1.0) changes what is drawn
#   CASE     : the uniform's name is case-sensitive ("Activation" does nothing, "activation" works)
#   HINT     : a hint_range(0.0, 1.0) shapes the editor, not the math: a value of 7.0 set from code is stored as 7.0
#   TWEEN    : set the start value, then tween "shader_parameter/activation" and the surface follows
#              material.set_shader_parameter("activation", 0.0)
#              var tween := create_tween()
#              tween.tween_property(material, "shader_parameter/activation", 1.0, 2.0)
# (The tween WITHOUT the first line is verify3b-tween-without-set.gd, kept as a labelled failure.)
# res://pad.gdshader is the film's copy of lab-shaders/12-signal-pad.gdshader, placed there by run-script.sh.
# Run:  ./run-script.sh verify3-attach-set-tween.gd run-3-attach-set-tween.log

const HOLDER := "extends Node3D\n\nfunc attach():\n\tvar material := ShaderMaterial.new()\n\tmaterial.shader = load(\"res://pad.gdshader\")\n\t$Pad.material_override = material\n\nfunc set_one():\n\t$Pad.material_override.set_shader_parameter(\"activation\", 1.0)\n\nfunc set_wrong_case():\n\t$Pad.material_override.set_shader_parameter(\"Activation\", 0.5)\n\nfunc animate():\n\tvar material = $Pad.material_override\n\tmaterial.set_shader_parameter(\"activation\", 0.0)\n\tvar tween := create_tween()\n\ttween.tween_property(material, \"shader_parameter/activation\", 1.0, 2.0)\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func has_prop(cls: String, prop: String) -> bool:
	for d in ClassDB.class_get_property_list(cls):
		if d["name"] == prop:
			return true
	return false

func frames(n: int) -> void:
	for i in range(n): await process_frame

# a light-stripe pixel of the pad on the front-facing quad (UV.x about 0.09375 of a 1.8 unit quad centred in a 2 unit view)
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
	stage.add_child(pad)
	out("0-setup", {"script_reload_error": err, "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"MeshInstance3D_has_material_override": has_prop("GeometryInstance3D", "material_override"),
		"MeshInstance3D_has_a_material_property": has_prop("MeshInstance3D", "material"),
		"Sprite2D_has_a_material_property": has_prop("CanvasItem", "material")})
	await frames(3)
	var before := probe()
	stage.attach()
	await frames(3)
	var attached := probe()
	out("ATTACH", {"before_any_material (default grey-white look)": before, "after_attach (rust, activation 0)": attached,
		"material_override_is_a_ShaderMaterial": pad.material_override is ShaderMaterial,
		"get_shader_parameter_before_any_set": str(pad.material_override.get_shader_parameter("activation"))})
	stage.set_one()
	await frames(3)
	var one := probe()
	out("SET", {"after_set_activation_1.0 (flat green)": one, "stored_value": pad.material_override.get_shader_parameter("activation")})
	pad.material_override.set_shader_parameter("activation", 0.0)
	await frames(2)
	var zero := probe()
	stage.set_wrong_case()
	await frames(3)
	var wrong := probe()
	out("CASE", {"activation_0": zero, "after_set_Activation_0.5_wrong_case": wrong, "unchanged": zero == wrong,
		"stored_under_wrong_name": str(pad.material_override.get_shader_parameter("Activation")), "stored_under_right_name": pad.material_override.get_shader_parameter("activation")})
	pad.material_override.set_shader_parameter("activation", 7.0)
	await frames(2)
	out("HINT", {"hint": "hint_range(0.0, 1.0)", "stored_after_set_7.0": pad.material_override.get_shader_parameter("activation")})
	pad.material_override.set_shader_parameter("activation", 0.0)
	await frames(2)
	stage.animate()
	await frames(2)
	var t0 := probe()
	await create_timer(1.0).timeout
	var mid := probe()
	await create_timer(1.3).timeout
	await frames(2)
	var end := probe()
	out("TWEEN", {"start": t0, "after_about_1_s": mid, "end (flat green)": end, "stored_end": pad.material_override.get_shader_parameter("activation")})
	quit(0)
