extends SceneTree
func _initialize() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280,720)
	root.content_scale_size = Vector2i(1280,720)
	var stage := Node3D.new()
	root.add_child(stage)
	var cam := Camera3D.new()
	cam.position = Vector3(0,0,6)
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 5.5
	stage.add_child(cam)
	cam.current = true
	var points: Array = []
	for row in range(2):
		for col in range(3):
			var mat := ShaderMaterial.new()
			mat.shader = load("res://signal-garden/signal.gdshader" if row == 0 else "res://signal-garden/audit/signal-seeded.gdshader")
			mat.set_shader_parameter("activation", col * 0.5)
			var mesh := MeshInstance3D.new()
			var quad := QuadMesh.new()
			quad.size = Vector2(1.7,1.1)
			mesh.mesh = quad
			mesh.material_override = mat
			mesh.position = Vector3((col-1)*2.3,0.8-row*1.5,0)
			stage.add_child(mesh)
			for stripe in range(2):
				var offset := -0.85 + 1.7 * (0.03125 + stripe*0.0625)
				points.append({"kind":"garden","variant":"fixed" if row==0 else "seeded","activation":col*0.5,"stripe":stripe,"point":cam.unproject_position(mesh.position+Vector3(offset,0,0))})
	var canvas := CanvasLayer.new()
	root.add_child(canvas)
	for item in [[Vector2(50,30), "SHADER AUDIT / actual Godot output"], [Vector2(50,245), "Correct"], [Vector2(50,440), "Seeded"], [Vector2(290,130), "activation 0"], [Vector2(570,130), "activation 0.5"], [Vector2(880,130), "activation 1"], [Vector2(50,580), "Course: correct"], [Vector2(50,635), "Course: seeded"]]:
		var label := Label.new()
		label.position = item[0]
		label.text = item[1]
		label.add_theme_font_size_override("font_size", 20)
		label.add_theme_color_override("font_color", Color("172830"))
		canvas.add_child(label)
	for row in range(2):
		for col in range(3):
			for part in range(2):
				var obj := Polygon2D.new()
				obj.polygon = PackedVector2Array([Vector2(0,0),Vector2(55,0),Vector2(55,35),Vector2(0,35)])
				obj.color = Color("dd775b") if part==0 else Color.BLACK
				obj.position = Vector2(270+col*240+part*65,575+row*55)
				var mat := ShaderMaterial.new()
				mat.shader = load("res://signal-garden/audit/course-fixed.gdshader" if row==0 else "res://signal-garden/audit/course-seeded.gdshader")
				mat.set_shader_parameter("flash_amount",col*0.5)
				obj.material = mat
				canvas.add_child(obj)
				points.append({"kind":"course","variant":"fixed" if row==0 else "seeded","activation":col*0.5,"part":part,"point":obj.position+Vector2(20,15)})
	for i in range(5): await process_frame
	RenderingServer.force_draw(false)
	var image := root.get_texture().get_image()
	var output := ProjectSettings.globalize_path("res://../evidence/assignments/shader-audit")
	DirAccess.make_dir_recursive_absolute(output)
	image.save_png(output+"/bench.png")
	for p in points:
		var xy: Vector2 = p.point
		var color := image.get_pixel(int(xy.x),int(xy.y))
		p["xy"] = [int(xy.x),int(xy.y)]
		p["rgb"] = [color.r,color.g,color.b]
		p.erase("point")
	var f := FileAccess.open(output+"/samples.json",FileAccess.WRITE)
	f.store_string(JSON.stringify(points,"  "))
	f.close()
	print("Rendered real shader bench: ",points.size()," samples")
	stage.queue_free()
	canvas.queue_free()
	await process_frame
	quit()
