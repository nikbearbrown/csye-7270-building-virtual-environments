extends "res://tools/harness.gd"
# TRAPS: every Cg-to-Godot trap the conversion met at run time, each measured. One line per measurement: "TRAP-n <what> | <result>".
# (Compile-time traps, the ones the compiler reports, are in tools/cg_isms.sh.)
# Run:  tools/run_godot.sh res://tools/traps.gd <forward_plus|gl_compatibility> <abs log path>

func run() -> void:
	await warm()
	await calibrate()
	await t1_mesh_arrays()
	await t2_colour_space()
	await t3_time()
	await t4_position()
	await t5_texture_decode()
	await t6_matrices()
	await t7_normal_spaces()
	await t8_repeat()
	await t9_normal_hint()
	await t10_cube_orientation()

# ------------------------------------------------------------------ TRAP-1 what the built-in meshes carry
func t1_mesh_arrays() -> void:
	var sm := SphereMesh.new()
	sm.radius = 1.0; sm.height = 2.0; sm.radial_segments = 128; sm.rings = 64
	var arr := sm.surface_get_arrays(0)
	var V: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var N: PackedVector3Array = arr[Mesh.ARRAY_NORMAL]
	var T: PackedFloat32Array = arr[Mesh.ARRAY_TANGENT]
	var UV: PackedVector2Array = arr[Mesh.ARRAY_TEX_UV]
	say("TRAP-1 sphere mesh arrays | vertices %d, tangent floats %d (4 per vertex = %s), uv %d" % [V.size(), T.size(), str(T.size() == V.size() * 4), UV.size()])
	var worst_u := 0.0
	var worst_v := 0.0
	var t_along_u := 0
	var b_up := 0
	var checked := 0
	for k in range(0, V.size(), 7):
		var p := V[k]
		var u := fposmod(atan2(p.x, p.z) / TAU, 1.0)
		var v := acos(clampf(p.y, -1, 1)) / PI
		var du := absf(u - UV[k].x)
		du = minf(du, 1.0 - du)
		if absf(p.x) + absf(p.z) > 1e-4:
			worst_u = maxf(worst_u, du)
		worst_v = maxf(worst_v, absf(v - UV[k].y))
		var tt := Vector3(T[k * 4], T[k * 4 + 1], T[k * 4 + 2])
		var du_dir := Vector3(cos(TAU * UV[k].x), 0.0, -sin(TAU * UV[k].x))
		if absf(p.y) < 0.95:
			checked += 1
			if tt.dot(du_dir) > 0.99:
				t_along_u += 1
			var bb := N[k].cross(tt) * T[k * 4 + 3]       # Godot's BINORMAL = cross(NORMAL, TANGENT) * tangent.w
			var north := Vector3(-p.y * p.x, 1.0 - p.y * p.y, -p.y * p.z).normalized()   # along the meridian toward the +Y pole = image-up (against +v)
			if bb.dot(north) > 0.99:
				b_up += 1
	say("TRAP-1 sphere uv formula u = atan2(x, z) / 2pi, v = acos(y / r) / pi | max |du| %.6f, max |dv| %.6f (every 7th vertex)" % [worst_u, worst_v])
	say("TRAP-1 sphere TANGENT points along +u | %d of %d non-polar sampled vertices agree (dot > 0.99); tangent.w = %.1f" % [t_along_u, checked, T[100 * 4 + 3]])
	say("TRAP-1 sphere cross(NORMAL, TANGENT) points along the meridian toward the +Y pole (image-up, against +v) | %d of %d" % [b_up, checked])
	var tm := TorusMesh.new()
	var tarr := tm.surface_get_arrays(0)
	say("TRAP-1 torus mesh arrays | vertices %d, has tangents = %s" % [tarr[Mesh.ARRAY_VERTEX].size(), str(tarr[Mesh.ARRAY_TANGENT] != null)])

# ------------------------------------------------------------------ TRAP-2 colour numbers going IN to a shader
func t2_colour_space() -> void:
	var code := """shader_type spatial; render_mode unshaded;
uniform vec3 a : source_color = vec3(0.15);
uniform vec3 b : source_color = vec3(0.15);
uniform vec3 c : source_color = vec3(0.15);
uniform vec3 d = vec3(0.15);
uniform vec3 e = vec3(0.15);
uniform vec4 f : source_color = vec4(0.15);
uniform vec4 g = vec4(0.15);
void fragment() {
	float x = FRAGCOORD.x;
	vec3 o = x < 183.0 ? a : x < 366.0 ? b : x < 549.0 ? c : x < 732.0 ? d : x < 915.0 ? e : x < 1098.0 ? f.rgb : g.rgb;
	ALBEDO = o;
}
"""
	var dd := flat(code, {"b": Color(0.15, 0.15, 0.15), "c": Vector3(0.15, 0.15, 0.15), "e": Color(0.15, 0.15, 0.15), "f": Color(0.15, 0.15, 0.15), "g": Color(0.15, 0.15, 0.15)})
	await warm()
	var img := await shoot()
	var names := ["A vec3 source_color, default 0.15", "B vec3 source_color, set from code with Color(0.15)", "C vec3 source_color, set from code with Vector3(0.15)",
		"D plain vec3, default 0.15", "E plain vec3, set from code with Color(0.15)", "F vec4 source_color, set with Color(0.15)", "G plain vec4, set with Color(0.15)"]
	var xs := [90, 270, 460, 640, 820, 1000, 1180]
	for k in range(7):
		var c := px(img, xs[k], 360)
		say("TRAP-2 colour number the shader sees | %s -> %.4f  (typed 0.15; linear value of sRGB 0.15 is %.4f)" % [names[k], inv(c.r), Rig.srgb_to_lin(0.15)])
	await drop(dd)

# ------------------------------------------------------------------ TRAP-3 TIME under a manual clock
func t3_time() -> void:
	var code := "shader_type spatial; render_mode unshaded;\nvoid fragment() { ALBEDO = vec3((floor(TIME * 8.0) + 40.0) / 255.0, (fract(TIME * 8.0) * 200.0 + 40.0) / 255.0, 0.0); }\n"
	var d := flat(code)
	await warm(2)
	var seq: Array = []
	var prev := -1.0
	for step in [0.0, 0.5, 0.5, 1.0, 0.0, 0.25]:
		var img := await shoot(step)
		var c := px(img, 640, 360)
		var t := ((roundf(inv(c.r) * 255.0) - 40.0) + (inv(c.g) * 255.0 - 40.0) / 200.0) / 8.0
		seq.append("step %.2f -> TIME %.3f%s" % [step, t, "" if prev < 0 else " (moved %.3f)" % (t - prev)])
		prev = t
	say("TRAP-3 TIME with the render loop off | " + " ; ".join(seq))
	await drop(d)

# ------------------------------------------------------------------ TRAP-4 writing POSITION by hand vs Godot's own
func t4_position() -> void:
	var with_pos := FileAccess.get_file_as_string("res://shaders/00_super_simple.gdshader")
	var without := with_pos.replace("	POSITION = PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX * vec4(VERTEX, 1.0);\n", "")
	var imgs: Array[Image] = []
	for code in [with_pos, without]:
		var d := scene_with_camera()
		var sph := MeshInstance3D.new()
		var sm := SphereMesh.new()
		sm.radial_segments = 64; sm.rings = 32
		sph.mesh = sm
		sph.position = Rig.SPHERE_POS
		sph.rotation_degrees = Vector3(20, 35, 0)
		sph.scale = Vector3(1.0, 0.7, 1.3)
		var sh := Shader.new(); sh.code = code
		var m := ShaderMaterial.new(); m.shader = sh
		m.set_shader_parameter("shader_color", Color("#5FA391"))
		sph.material_override = m
		d["scene"].add_child(sph)
		await warm(2)
		imgs.append(await shoot())
		await drop(d)
	var diff := 0
	var covered := 0
	var bg := imgs[0].get_pixel(5, 5)
	for y in range(0, 720):
		for x in range(0, 1280):
			var a := imgs[0].get_pixel(x, y)
			if not a.is_equal_approx(imgs[1].get_pixel(x, y)):
				diff += 1
			if absf(a.r - bg.r) > 0.02 or absf(a.g - bg.g) > 0.02:
				covered += 1
	say("TRAP-4 POSITION written by hand as PROJECTION * VIEW * MODEL * vec4(VERTEX, 1) vs left to Godot | differing pixels %d of %d (the object covers %d px; rotated and non-uniformly scaled sphere)" % [diff, 1280 * 720, covered])

# ------------------------------------------------------------------ TRAP-5 texture numbers going IN: source_color on a sampler
func t5_texture_decode() -> void:
	var code := """shader_type spatial; render_mode unshaded;
uniform sampler2D tex_plain : filter_nearest;
uniform sampler2D tex_srgb : source_color, filter_nearest;
void fragment() {
	vec2 uv = vec2(0.3125, 0.3125);   // the middle of the sand cell (column 2, row 2): sRGB bytes (226, 200, 140)
	ALBEDO = FRAGCOORD.x < 640.0 ? texture(tex_plain, uv).rgb : texture(tex_srgb, uv).rgb;
}
"""
	var tex := Lessons.load_texture("diffuse_checker.png")
	var d := flat(code, {"tex_plain": tex, "tex_srgb": tex})
	await warm()
	var img := await shoot()
	var l := inv3(px(img, 300, 360))
	var r := inv3(px(img, 980, 360))
	say("TRAP-5 texel (226,200,140) read by a sampler | plain sampler -> shader sees (%.3f, %.3f, %.3f); source_color sampler -> (%.3f, %.3f, %.3f). Raw = (0.886, 0.784, 0.549); decoded to linear = (0.760, 0.578, 0.262)" % [l.x, l.y, l.z, r.x, r.y, r.z])
	await drop(d)

# ------------------------------------------------------------------ TRAP-6 matrices: operator order, row vs column indexing, normal matrix
func t6_matrices() -> void:
	var code := """shader_type spatial; render_mode unshaded;
varying vec3 v_a;      // MODEL_NORMAL_MATRIX * n         (the converted shaders' world normal)
varying vec3 v_b;      // transpose(inverse(mat3(MODEL_MATRIX))) * n   (the textbook inverse transpose)
varying vec3 v_c;      // mat3(MODEL_MATRIX) * n          (the WRONG matrix for normals)
varying float v_row;   // naive port of Cg ViewInverse[0].w, [1].w, [2].w  -> length of that vector
varying float v_col;   // INV_VIEW_MATRIX[3].xyz minus CAMERA_POSITION_WORLD -> length of the difference
varying float v_mv;    // (MODEL_MATRIX * vec4(1,0,0,1)).x       Cg mul(M, v)
varying float v_vm;    // (vec4(1,0,0,1) * MODEL_MATRIX).x       Cg mul(v, M)
void vertex() {
	vec3 n = normalize(vec3(1.0, 1.0, 1.0));
	mat3 m3 = mat3(MODEL_MATRIX[0].xyz, MODEL_MATRIX[1].xyz, MODEL_MATRIX[2].xyz);
	v_a = MODEL_NORMAL_MATRIX * n;
	v_b = transpose(inverse(m3)) * n;
	v_c = m3 * n;
	v_row = length(vec3(INV_VIEW_MATRIX[0].w, INV_VIEW_MATRIX[1].w, INV_VIEW_MATRIX[2].w));
	v_col = length(INV_VIEW_MATRIX[3].xyz - CAMERA_POSITION_WORLD);
	v_mv = (MODEL_MATRIX * vec4(1.0, 0.0, 0.0, 1.0)).x;
	v_vm = (vec4(1.0, 0.0, 0.0, 1.0) * MODEL_MATRIX).x;
}
void fragment() {
	float x = FRAGCOORD.x;
	float o = 0.0;
	if (x < 160.0) o = length(v_a - v_b) * 10.0;
	else if (x < 320.0) o = length(normalize(v_a) - normalize(v_b)) * 10.0;
	else if (x < 480.0) o = length(normalize(v_a) - normalize(v_c)) * 0.5;
	else if (x < 640.0) o = length(v_a) / 4.0;
	else if (x < 800.0) o = length(v_b) / 4.0;
	else if (x < 960.0) o = v_row / 8.0;
	else if (x < 1120.0) o = v_col * 10.0;
	else o = (v_mv + 4.0) / 8.0;
	ALBEDO = vec3(o);
}
"""
	var d := flat(code)
	var node: MeshInstance3D = d["mesh"]
	node.position = Vector3(-1.3, 0.2, 0.4)
	node.rotation_degrees = Vector3(25, 40, 10)
	node.scale = Vector3(2.0, 0.5, 3.0)
	await warm()
	var img := await shoot()
	var vals: Array = []
	for k in range(8):
		vals.append(inv(px(img, k * 160 + 80, 360).r))
	var xf := node.transform
	var m3 := xf.basis
	var n := Vector3(1, 1, 1).normalized()
	var ex_a := (m3.inverse().transposed() * n)          # exact inverse transpose, CPU
	var ex_c := m3 * n
	var P := Projection(xf)
	var vrow := Vector4(1, 0, 0, 1)
	var ex_mv := (P * vrow).x
	var ex_vm := vrow.dot(P.x)
	say("TRAP-6 normal matrix | |MODEL_NORMAL_MATRIX*n - transpose(inverse(mat3(MODEL)))*n| = %.4f (0 = same matrix); directions differ by %.4f; length of MODEL_NORMAL_MATRIX*n = %.3f (CPU inverse-transpose length %.3f; node scale is (2, 0.5, 3), so it is NOT normalised)" % [
		vals[0] / 10.0, vals[1] / 10.0, vals[3] * 4.0, ex_a.length()])
	say("TRAP-6 normal matrix | using plain mat3(MODEL_MATRIX) on a normal instead of the inverse transpose turns the direction by %.3f (unit-vector distance; CPU expected %.3f)" % [vals[2] * 2.0, (ex_a.normalized() - ex_c.normalized()).length()])
	say("TRAP-6 camera position | naive port of Cg ViewInverse[0].w, [1].w, [2].w read as GLSL INV_VIEW_MATRIX[0].w, [1].w, [2].w has length %.3f (camera is %.1f from the origin: the port reads the zero 4th ROW of three COLUMNS); INV_VIEW_MATRIX[3].xyz differs from CAMERA_POSITION_WORLD by %.4f" % [vals[5] * 8.0, Rig.CAM_POS.length(), vals[6] / 10.0])
	say("TRAP-6 operator order | (MODEL * vec4(1,0,0,1)).x = %.3f (CPU %.3f) is Cg mul(M, v); the reversed product (v * MODEL).x would be %.3f on the CPU: it reads the matrix transposed" % [vals[7] * 8.0 - 4.0, ex_mv, ex_vm])
	await drop(d)

# ------------------------------------------------------------------ TRAP-7 what NORMAL means in vertex() and in fragment()
func t7_normal_spaces() -> void:
	var code := """shader_type spatial; render_mode unshaded;
uniform int mode = 0;
varying vec3 obj_n;
void vertex() { obj_n = NORMAL; }
void fragment() { ALBEDO = (mode == 0 ? NORMAL : obj_n) * 0.5 + 0.5; }
"""
	var res: Array = []
	for mode in [0, 1]:
		var d := scene_with_camera()
		var sph := MeshInstance3D.new()
		var sm := SphereMesh.new()
		sm.radial_segments = 64; sm.rings = 32
		sph.mesh = sm
		sph.rotation_degrees = Vector3(90, 0, 0)       # the sphere's +Y pole now faces the camera
		var sh := Shader.new(); sh.code = code
		var m := ShaderMaterial.new(); m.shader = sh
		m.set_shader_parameter("mode", mode)
		sph.material_override = m
		d["scene"].add_child(sph)
		await warm(2)
		var img := await shoot()
		var c := inv3(px(img, 640, 360))
		res.append(c * 2.0 - Vector3.ONE)
		await drop(d)
	say("TRAP-7 NORMAL at the pixel facing the camera, sphere turned 90 degrees about X | fragment() NORMAL = (%.2f, %.2f, %.2f) (view space: toward the camera is +Z); vertex() NORMAL carried in a varying = (%.2f, %.2f, %.2f) (object space: the sphere's own +Y)" % [
		res[0].x, res[0].y, res[0].z, res[1].x, res[1].y, res[1].z])

# ------------------------------------------------------------------ TRAP-8 Wrap addressing: what the default sampler does past the edge
func t8_repeat() -> void:
	var code := """shader_type spatial; render_mode unshaded;
uniform sampler2D t_default : filter_nearest;
uniform sampler2D t_disable : filter_nearest, repeat_disable;
uniform sampler2D t_enable : filter_nearest, repeat_enable;
void fragment() {
	vec2 uv = vec2(1.0625, 0.4375);   // one tile past the right edge of the red cell (column 0, row 3); the last column of row 3 is the magenta cell
	float x = FRAGCOORD.x;
	ALBEDO = x < 427.0 ? texture(t_default, uv).rgb : x < 854.0 ? texture(t_disable, uv).rgb : texture(t_enable, uv).rgb;
}
"""
	var tex := Lessons.load_texture("diffuse_checker.png")
	var d := flat(code, {"t_default": tex, "t_disable": tex, "t_enable": tex})
	await warm()
	var img := await shoot()
	var a := inv3(px(img, 200, 360))
	var b := inv3(px(img, 640, 360))
	var c := inv3(px(img, 1080, 360))
	say("TRAP-8 uv.x = 1.0625 (one tile past the edge); red cell raw (0.80, 0.24, 0.20), edge cell raw magenta (0.75, 0.24, 0.67) | no repeat hint -> (%.2f, %.2f, %.2f); repeat_disable -> (%.2f, %.2f, %.2f); repeat_enable -> (%.2f, %.2f, %.2f)" % [a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z])
	await drop(d)

# ------------------------------------------------------------------ TRAP-9 a normal map read with source_color
func t9_normal_hint() -> void:
	var code := """shader_type spatial; render_mode unshaded;
uniform sampler2D n_plain : filter_nearest;
uniform sampler2D n_srgb : source_color, filter_nearest;
void fragment() {
	vec2 uv = vec2(0.234375, 0.3125);   // texel (120, 160): 24 px right of the centre of dome cell (column 1, row 2)
	ALBEDO = FRAGCOORD.x < 640.0 ? vec3(texture(n_plain, uv).r) : vec3(texture(n_srgb, uv).r);
}
"""
	var tex := Lessons.load_texture("normal_gl.png")
	var d := flat(code, {"n_plain": tex, "n_srgb": tex})
	await warm()
	var img := await shoot()
	var l := inv(px(img, 300, 360).r)
	var r := inv(px(img, 980, 360).r)
	var im := Lessons.load_image("normal_gl.png")
	var byte_r := im.get_pixel(int(0.234375 * 512.0), int(0.3125 * 512.0)).r
	say("TRAP-9 normal map red channel (file byte %d = %.3f) | plain sampler -> %.3f = decoded x %.3f; with source_color -> %.3f = decoded x %.3f (the tilt is wrong by %.0f%%)" % [
		int(roundf(byte_r * 255.0)), byte_r, l, l * 2.0 - 1.0, r, r * 2.0 - 1.0, 100.0 * absf((r * 2.0 - 1.0) - (l * 2.0 - 1.0)) / maxf(absf(l * 2.0 - 1.0), 1e-6)])
	await drop(d)

# ------------------------------------------------------------------ TRAP-10 cube map: face order, orientation, hint
func cube_ref(d: Vector3) -> Color:
	# OpenGL cube-map face selection (the table the six PNGs were written with), nearest texel, RAW file bytes
	var ax := absf(d.x); var ay := absf(d.y); var az := absf(d.z)
	var face := ""; var sc := 0.0; var tc := 0.0; var ma := 1.0
	if ax >= ay and ax >= az:
		ma = ax
		if d.x > 0: face = "px"; sc = -d.z; tc = -d.y
		else: face = "nx"; sc = d.z; tc = -d.y
	elif ay >= az:
		ma = ay
		if d.y > 0: face = "py"; sc = d.x; tc = d.z
		else: face = "ny"; sc = d.x; tc = -d.z
	else:
		ma = az
		if d.z > 0: face = "pz"; sc = d.x; tc = -d.y
		else: face = "nz"; sc = -d.x; tc = -d.y
	var s := (sc / ma + 1.0) * 0.5
	var t := (tc / ma + 1.0) * 0.5
	var im := Lessons.load_image("cube_%s.png" % face)
	return im.get_pixel(clampi(int(s * im.get_width()), 0, im.get_width() - 1), clampi(int(t * im.get_height()), 0, im.get_height() - 1))

func t10_cube_orientation() -> void:
	var code := """shader_type spatial; render_mode unshaded;
uniform samplerCube cm : filter_nearest;
uniform samplerCube cm_srgb : source_color, filter_nearest;
uniform vec3 dir;
uniform bool use_srgb = false;
void fragment() { ALBEDO = use_srgb ? texture(cm_srgb, normalize(dir)).rgb : texture(cm, normalize(dir)).rgb; }
"""
	var cube := Lessons.load_cubemap()
	var sun := Rig.LIGHT_TRAVEL.normalized() * -1.0
	var dirs := {
		"+X axis": Vector3(1, 0, 0), "-X axis": Vector3(-1, 0, 0), "+Y axis": Vector3(0, 1, 0), "-Y axis": Vector3(0, -1, 0), "+Z axis": Vector3(0, 0, 1), "-Z axis": Vector3(0, 0, -1),
		"toward the sun": sun, "sun mirrored in x": Vector3(-sun.x, sun.y, sun.z), "sun mirrored in z": Vector3(sun.x, sun.y, -sun.z),
		"sky ahead (0.3, 0.6, 1)": Vector3(0.3, 0.6, 1), "floor ahead (0.3, -0.6, 1)": Vector3(0.3, -0.6, 1), "yellow wall (0.4, 0.05, 1)": Vector3(0.4, 0.05, 1),
		"floor right (1, -0.5, 0.3)": Vector3(1, -0.5, 0.3), "floor left (-1, -0.5, -0.3)": Vector3(-1, -0.5, -0.3)}
	var d := flat(code, {"cm": cube, "cm_srgb": cube})
	var bad := 0
	var lines: Array = []
	for name in dirs:
		d["material"].set_shader_parameter("dir", dirs[name])
		d["material"].set_shader_parameter("use_srgb", false)
		await warm(2)
		var img := await shoot()
		var got := inv3(px(img, 640, 360))
		var ex := cube_ref(dirs[name])
		var diff := maxf(absf(got.x - ex.r), maxf(absf(got.y - ex.g), absf(got.z - ex.b)))
		if diff > 0.02:
			bad += 1
		lines.append("%s: GPU (%d,%d,%d) vs file (%d,%d,%d)%s" % [name, roundf(got.x * 255), roundf(got.y * 255), roundf(got.z * 255), roundf(ex.r * 255), roundf(ex.g * 255), roundf(ex.b * 255), "" if diff <= 0.02 else " <-- MISMATCH"])
	say("TRAP-10 cube map built with Cubemap.create_from_images([+X, -X, +Y, -Y, +Z, -Z]) and faces written to the OpenGL table | %d of %d directions match the file texel; %s" % [dirs.size() - bad, dirs.size(), " | ".join(lines)])
	d["material"].set_shader_parameter("dir", Vector3(1, 0, 0))
	d["material"].set_shader_parameter("use_srgb", true)
	await warm(2)
	var img2 := await shoot()
	var g2 := inv3(px(img2, 640, 360))
	say("TRAP-10 cube map read through a source_color samplerCube, direction +X (file texel raw (220,40,40)) | shader sees (%.3f, %.3f, %.3f); raw would be (0.863, 0.157, 0.157), decoded to linear (0.716, 0.021, 0.021)" % [g2.x, g2.y, g2.z])
	await drop(d)
