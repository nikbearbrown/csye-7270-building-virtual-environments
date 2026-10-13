extends SceneTree
# verify2: what do LIGHT_DIRECTION, LIGHT_POSITION and LIGHT_VERTEX contain? A big sprite whose light() writes the number as a colour (ambient black, one white light, opaque white light texture).
# Encoding: direction r,g = (x,y)*0.5+0.5; position r,g = xy/320, xy/180 (b = z*0.01+0.5); vertex the same.
# Run: godot --path <project dir> --script res://verify2.gd
const LL := preload("res://lightlab.gd")

func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func frames(n: int) -> void:
	for i in range(n): await process_frame
func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()
func clear() -> void:
	for c in root.get_children(): c.queue_free()
	await frames(2)

func lcode(body: String) -> String:
	return "shader_type canvas_item;\nvoid light() {\n\t" + body + "\n}\n"

func big_sprite(code: String) -> Sprite2D:
	return LL.sprite(LL.solid_tex(Color.WHITE, 64), Vector2(160, 90), Vector2(6, 6), LL.shader_mat(code))

func dec(v: float) -> float:
	return snappedf(v * 2.0 - 1.0, 0.01)

func run() -> void:
	root.size = Vector2i(320, 180)
	var white := LL.solid_tex(Color.WHITE, 128)
	var pts := {"E": Vector2(60, 0), "SE": Vector2(60, 60), "S": Vector2(0, 60), "SW": Vector2(-60, 60), "W": Vector2(-60, 0), "NW": Vector2(-60, -60), "N": Vector2(0, -60), "NE": Vector2(60, -60)}

	# ---- D: LIGHT_DIRECTION from a PointLight2D at (160,90), light height 0, then 50 ----
	for h in [0.0, 50.0]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(big_sprite(lcode("LIGHT = vec4(LIGHT_DIRECTION.xy * 0.5 + 0.5, LIGHT_DIRECTION.z * 0.5 + 0.5, 1.0);")))
		root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 1.0, Color.WHITE, h))
		await frames(4)
		var im := grab()
		var res := {}
		for k in pts:
			var p: Vector2 = pts[k]
			var c := im.get_pixel(int(160 + p.x), int(90 + p.y))
			res[k] = [dec(c.r), dec(c.g), dec(c.b)]
		out("D-point-light-direction-height-%d" % int(h), {"light_at": [160, 90], "sample_offsets_from_light": "E=(+60,0) S=(0,+60) etc, y down", "direction_xyz_by_compass": res,
			"reading": "if the vector points from the pixel TO the light, the pixel at E (+60,0) shows x=-1 (points back west)"})

	# ---- P: LIGHT_POSITION and LIGHT_VERTEX in screen space (no camera), then with camera zoom 2 ----
	for zoom in [1.0, 2.0]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(big_sprite(lcode("LIGHT = vec4(LIGHT_POSITION.x / 320.0, LIGHT_POSITION.y / 180.0, LIGHT_POSITION.z * 0.01 + 0.5, 1.0);")))
		root.add_child(LL.point_light(Vector2(200, 100), white, 4.0, 1.0, Color.WHITE, 0.0))
		if zoom != 1.0:
			var cam := Camera2D.new()
			cam.position = Vector2(160, 90)
			cam.zoom = Vector2(zoom, zoom)
			root.add_child(cam)
			cam.make_current()
		await frames(4)
		var im := grab()
		var c := im.get_pixel(10, 10)
		out("P-light-position-zoom-%d" % int(zoom), {"light_world": [200, 100], "camera_zoom": zoom, "position_xy_px_decoded": [snappedf(c.r * 320.0, 0.5), snappedf(c.g * 180.0, 0.5)], "position_z_decoded": snappedf((c.b - 0.5) / 0.01, 0.5),
			"reading": "world (200,100) with zoom 1 would sit at screen (200,100); with zoom 2 centred on (160,90) at (240,110)"})
		# LIGHT_VERTEX
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(big_sprite(lcode("LIGHT = vec4(LIGHT_VERTEX.x / 320.0, LIGHT_VERTEX.y / 180.0, LIGHT_VERTEX.z * 0.01 + 0.5, 1.0);")))
		root.add_child(LL.point_light(Vector2(160, 90), white, 4.0, 1.0, Color.WHITE, 0.0))
		if zoom != 1.0:
			var cam2 := Camera2D.new()
			cam2.position = Vector2(160, 90)
			cam2.zoom = Vector2(zoom, zoom)
			root.add_child(cam2)
			cam2.make_current()
		await frames(4)
		var im2 := grab()
		var rows := []
		for q in [Vector2i(10, 10), Vector2i(100, 40), Vector2i(300, 170), Vector2i(160, 90)]:
			var c2 := im2.get_pixel(q.x, q.y)
			rows.append({"pixel": [q.x, q.y], "vertex_xy_decoded": [snappedf(c2.r * 320.0, 0.5), snappedf(c2.g * 180.0, 0.5)], "z": snappedf((c2.b - 0.5) / 0.01, 0.5)})
		out("V-light-vertex-zoom-%d" % int(zoom), {"camera_zoom": zoom, "samples": rows})

	# ---- Q: a DirectionalLight2D (rotation 0 = light emitted down +Y) ----
	for rot in [0.0, 90.0]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(big_sprite(lcode("LIGHT = vec4(LIGHT_DIRECTION.xy * 0.5 + 0.5, LIGHT_DIRECTION.z * 0.5 + 0.5, 1.0);")))
		var dl := LL.dir_light(rot)
		root.add_child(dl)
		await frames(4)
		var im3 := grab()
		var res3 := {}
		for k in ["E", "S", "W", "N"]:
			var p: Vector2 = pts[k]
			var c3 := im3.get_pixel(int(160 + p.x), int(90 + p.y))
			res3[k] = [dec(c3.r), dec(c3.g), dec(c3.b)]
		out("Q-directional-direction-rot-%d" % int(rot), {"rotation_deg": rot, "direction_xyz_at_compass": res3, "is_directional_pixel": "see next case"})
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(big_sprite(lcode("LIGHT = vec4(LIGHT_POSITION.x / 320.0 + 0.1, LIGHT_POSITION.y / 180.0 + 0.1, float(LIGHT_IS_DIRECTIONAL) * 0.5, 1.0);")))
		root.add_child(LL.dir_light(rot))
		await frames(4)
		var c4 := grab().get_pixel(100, 60)
		out("Q2-directional-position-rot-%d" % int(rot), {"position_xy_plus_0.1": [snappedf(c4.r - 0.1, 0.001), snappedf(c4.g - 0.1, 0.001)], "is_directional_flag_x2": snappedf(c4.b * 2.0, 0.01)})
	quit(0)
