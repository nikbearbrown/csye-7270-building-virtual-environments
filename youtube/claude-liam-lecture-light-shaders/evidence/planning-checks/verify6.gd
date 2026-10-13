extends SceneTree
# verify6: position. LIGHT_POSITION and LIGHT_VERTEX: exact values, screen space under a camera zoom and under a SubViewport stretch,
# the distance, a ring made of two steps, and a mod() pattern that stays on the screen while the sprite moves.
# Run: godot --path <project dir> --script res://verify6.gd
const LL := preload("res://lightlab.gd")

func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func frames(n: int) -> void:
	for i in range(n): await process_frame
func grab_root() -> Image:
	RenderingServer.force_draw(false)
	var im := root.get_texture().get_image()
	im.convert(Image.FORMAT_RGBA8)
	return im
func clear() -> void:
	for c in root.get_children(): c.queue_free()
	await frames(2)

const RING := "shader_type canvas_item;\nuniform float radius = 150.0;\nuniform float thickness = 20.0;\nvoid light() {\n\tfloat d = length(LIGHT_VERTEX.xy - LIGHT_POSITION.xy);\n\tfloat ring = step(radius - thickness, d) - step(radius, d);\n\tLIGHT = vec4(vec3(ring), 1.0);\n}\n"

func floor_sprite(code: String, pos: Vector2, scl: float = 12.0) -> Sprite2D:
	return LL.sprite(LL.solid_tex(Color.WHITE, 64), pos, Vector2(scl, scl), LL.shader_mat(code))

func lit_at_distances(im: Image, c: Vector2, ds: Array) -> Dictionary:
	var r := {}
	for d in ds:
		r[str(d)] = 1 if im.get_pixel(int(c.x + d), int(c.y)).r > 0.5 else 0
	return r

func run() -> void:
	root.size = Vector2i(640, 360)
	var white := LL.solid_tex(Color.WHITE, 128)
	var C := Vector2(320, 180)

	# ---- exact values: is LIGHT_POSITION at the node's position, and is LIGHT_VERTEX at the pixel centre? fract(x/2) and fract(x/4) tell the fractions ----
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	root.add_child(floor_sprite("shader_type canvas_item;\nvoid light() {\n\tLIGHT = vec4(fract(LIGHT_VERTEX.x / 2.0), fract(LIGHT_VERTEX.y / 2.0), fract(LIGHT_POSITION.x / 4.0), 1.0);\n}\n", C))
	root.add_child(LL.point_light(Vector2(200, 100), white, 6.0, 1.0))
	await frames(4)
	var im := grab_root()
	var rows := []
	for q in [Vector2i(100, 40), Vector2i(101, 41), Vector2i(102, 42), Vector2i(103, 43)]:
		var c := im.get_pixel(q.x, q.y)
		rows.append({"pixel": [q.x, q.y], "fract(vertex.x/2)": snappedf(c.r, 0.01), "fract(vertex.y/2)": snappedf(c.g, 0.01), "fract(light_pos.x/4)": snappedf(c.b, 0.01)})
	out("X-exact-values", {"samples": rows, "reading": "vertex = pixel + 0.5 gives fract(x/2) of 0.25 for even x and 0.75 for odd x; light at node x=200 gives fract(200/4)=0 if exact"})

	# ---- distance as a grey ramp: d / 300 ----
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	root.add_child(floor_sprite("shader_type canvas_item;\nvoid light() {\n\tfloat d = length(LIGHT_VERTEX.xy - LIGHT_POSITION.xy);\n\tLIGHT = vec4(vec3(d / 300.0), 1.0);\n}\n", C))
	root.add_child(LL.point_light(C, white, 6.0, 1.0))
	await frames(4)
	im = grab_root()
	out("DM-distance-map", {"red_at_distance_0_75_150_225_(pixels_right_of_light)": [0, 75, 150, 225].map(func(d): return snappedf(im.get_pixel(int(C.x + d), int(C.y)).r, 0.001)), "expected_d_over_300": [0.0, 0.25, 0.5, 0.75]})

	# ---- ring: two steps; radius 150, thickness 20 -> lit where 130 <= d < 150 ----
	var ds := [0, 50, 100, 120, 128, 132, 140, 148, 152, 160, 200]
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	root.add_child(floor_sprite(RING, C))
	root.add_child(LL.point_light(C, white, 6.0, 1.0))
	await frames(4)
	im = grab_root()
	out("G-ring-no-zoom", {"lit_at_distance_px": lit_at_distances(im, C, ds), "radius": 150, "thickness": 20})
	# vertical check: same radius upward
	var vert := {}
	for d in [100, 140, 160]:
		vert[str(d)] = 1 if im.get_pixel(int(C.x), int(C.y - d)).r > 0.5 else 0
	out("G2-ring-vertical", {"lit_above_light_at_px": vert})

	# ---- camera zoom 2: world doubles, the ring (screen pixels) does not ----
	await clear()
	root.add_child(LL.canvas_mod(Color.BLACK))
	root.add_child(floor_sprite(RING, C))
	root.add_child(LL.point_light(C, white, 6.0, 1.0))
	var cam := Camera2D.new()
	cam.position = C
	cam.zoom = Vector2(2, 2)
	root.add_child(cam)
	cam.make_current()
	await frames(4)
	im = grab_root()
	out("Z-ring-camera-zoom-2", {"lit_at_distance_px": lit_at_distances(im, C, ds), "reading": "same screen pixels as without zoom: the ring does not follow the world scale"})

	# ---- SubViewport 1920x1080 over a 640x360 canvas (the 3x capture route): are the numbers in logical or physical pixels? ----
	await clear()
	var sv := SubViewport.new()
	sv.size = Vector2i(1920, 1080)
	sv.size_2d_override = Vector2i(640, 360)
	sv.size_2d_override_stretch = true
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	sv.add_child(LL.canvas_mod(Color.BLACK))
	sv.add_child(floor_sprite(RING, C))
	sv.add_child(LL.point_light(C, white, 6.0, 1.0))
	await frames(6)
	RenderingServer.force_draw(false)
	var svim := sv.get_texture().get_image()
	svim.convert(Image.FORMAT_RGBA8)
	var Cp := C * 3.0
	var phys := {}
	for d in [0, 100, 128, 140, 160, 300, 420, 440, 460, 480]:
		phys[str(d)] = 1 if svim.get_pixel(int(Cp.x + d), int(Cp.y)).r > 0.5 else 0
	out("SV-subviewport-3x-stretch", {"image": [svim.get_width(), svim.get_height()], "lit_at_physical_px_from_light": phys,
		"reading": "if the numbers are PHYSICAL pixels the ring sits at 130-150 px from the light; if LOGICAL (x3) at 390-450 px"})
	sv.queue_free()
	await frames(2)

	# ---- mod(): stripes anchored to the screen, not the sprite ----
	var STRIPES := "shader_type canvas_item;\nvoid light() {\n\tfloat s = step(mod(LIGHT_VERTEX.x, 64.0), 8.0);\n\tLIGHT = vec4(vec3(s), 1.0);\n}\n"
	var cols_a := []
	var cols_b := []
	for shift in [Vector2(0, 0), Vector2(23, 17)]:
		await clear()
		root.add_child(LL.canvas_mod(Color.BLACK))
		root.add_child(floor_sprite(STRIPES, C + shift))
		root.add_child(LL.point_light(C, white, 6.0, 1.0))
		await frames(4)
		im = grab_root()
		var cols := []
		for x in range(0, 640):
			if im.get_pixel(x, 180).r > 0.5: cols.append(x)
		(cols_a if shift == Vector2.ZERO else cols_b).append_array(cols)
	out("MOD-stripes-anchored-to-screen", {"same_columns_when_sprite_moved": cols_a == cols_b, "first_lit_columns_unmoved": cols_a.slice(0, 20), "first_lit_columns_moved": cols_b.slice(0, 20),
		"reading": "step(mod(x,64), 8) -> lit where mod(x+0.5, 64) <= 8 : columns 0-7, 64-71, ..."})
	quit(0)
