extends SceneTree
# Fixed-camera native renderer experiment. No shipped scene or material is edited.
var viewport: SubViewport
var camera: Camera3D
var world: Node3D
var output: String
var rows := []
func _initialize() -> void: call_deferred("run")
func snapshot(name: String) -> Image:
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	var image := viewport.get_texture().get_image()
	assert(image.get_size() == Vector2i(3840,2160))
	assert(image.save_png(output + "/" + name + ".png") == OK)
	return image
func run() -> void:
	output = OS.get_cmdline_user_args()[0]
	viewport = SubViewport.new(); viewport.size = Vector2i(3840,2160)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport); world = Node3D.new(); viewport.add_child(world)
	camera = Camera3D.new(); camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 4.0; camera.position = Vector3(0,0,5); world.add_child(camera); camera.make_current()
	var environment := Environment.new(); environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color("14262d"); environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	environment.tonemap_exposure = 1.0; environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color.WHITE; environment.ambient_light_energy = 0.35
	var sky := WorldEnvironment.new(); sky.environment = environment; world.add_child(sky)
	var light := DirectionalLight3D.new(); light.rotation_degrees = Vector3(-30,-30,0); world.add_child(light)
	var quad := MeshInstance3D.new(); var mesh := QuadMesh.new(); mesh.size = Vector2(3,2); quad.mesh = mesh
	var signal_material := ShaderMaterial.new(); signal_material.shader = load("res://course-series/shaders/signal.gdshader")
	quad.material_override = signal_material; world.add_child(quad)
	# UV.x=.15625 lies in a dark stripe; .21875 lies in the adjacent light stripe.
	for value in [0.0,0.5,1.0,2.0]:
		signal_material.set_shader_parameter("activation",value)
		var image: Image = await snapshot("signal-" + str(value))
		var pixels := []
		for u in [0.15625,0.21875]:
			var pos := camera.unproject_position(Vector3((u-0.5)*3.0,0,0))
			var color := image.get_pixel(int(pos.x),int(pos.y))
			pixels.append({"uv_x":u,"pixel":[int(pos.x),int(pos.y)],"rgb8":[roundi(color.r*255),roundi(color.g*255),roundi(color.b*255)]})
		rows.append({"case":"signal","set_value":value,"readback":signal_material.get_shader_parameter("activation"),"samples":pixels})
	quad.queue_free(); await process_frame
	var objects := []
	for i in range(2):
		var node := MeshInstance3D.new(); var sphere := SphereMesh.new(); sphere.radius = 0.6; sphere.height = 1.2
		node.mesh = sphere; node.position.x = -0.8 if i == 0 else 0.8
		node.material_override = load("res://course-series/materials/" + ("matte.tres" if i==0 else "coated.tres")).duplicate()
		world.add_child(node); objects.append(node)
	await snapshot("materials-baseline")
	var shared: Shader = objects[0].material_override.shader.duplicate()
	shared.code = shared.code.replace("* tint.rgb;", "* tint.rgb * vec3(1.0, 0.25, 0.25);")
	for node in objects: node.material_override.shader = shared
	await snapshot("materials-shared-shader-edit")
	for node in objects: node.material_override.shader = load("res://course-series/shaders/surface.gdshader")
	objects[0].material_override.set_shader_parameter("tint",Color(0.2,0.2,1.0))
	await snapshot("materials-one-value-edit")
	objects[1].visible = false; objects[0].position.x = 0
	for parameter in ["tint","roughness_gain","uv_scale","metallic_gain"]:
		var values: Array
		match parameter:
			"tint": values = [Color.BLACK,Color.WHITE,Color(1,0.2,0.2)]
			"roughness_gain": values = [0.0,0.8,1.0]
			"uv_scale": values = [0.25,1.0,4.0]
			_: values = [0.0,0.0,1.0]
		for i in range(3):
			var material := ShaderMaterial.new(); material.shader = load("res://course-series/shaders/surface.gdshader")
			material.set_shader_parameter("color_map",load("res://course-series/material-textures/gate-color.png"))
			material.set_shader_parameter("roughness_map",load("res://course-series/material-textures/gate-roughness.png"))
			material.set_shader_parameter(parameter,values[i]); objects[0].material_override = material
			await snapshot("sweep-"+parameter+"-"+str(i))
			rows.append({"case":"sweep","parameter":parameter,"index":i,"value":str(values[i])})
	var file := FileAccess.open(output+"/material-native-results.json",FileAccess.WRITE)
	assert(file != null)
	file.store_string(JSON.stringify({"engine":Engine.get_version_info(),"renderer":RenderingServer.get_video_adapter_name(),"method":"gl_compatibility","tonemap":"Linear","exposure":1.0,"size":[3840,2160],"rows":rows},"\t"));file.close()
	print("PASS native controlled values and 12 interface settings")
	viewport.queue_free(); await process_frame; quit()
