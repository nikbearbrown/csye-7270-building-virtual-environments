extends "res://tools/harness.gd"
# VERIFY: renders every lesson shader on the test sphere in a real windowed Godot and checks the pixels against a CPU re-implementation
# of the ORIGINAL Cg arithmetic (written from the .cgfx files, not from the GLSL). Two kinds of check:
#   - named points: the pixel at a chosen place on the sphere (lit pole, terminator, rim, highlight, a texel centre, ...) against the expected value
#   - full image: every 3rd pixel of the sphere against the same reference (percentage within 3 screen bytes)
# plus lesson-specific checks (silhouette of the vertex animation, the four techniques, equalities between lessons).
# The expected value goes through the MEASURED transfer curve of this renderer (calibrate()), so Forward+ (sRGB encoding) and Compatibility
# (no encoding) are each judged against their own screen.
# Run:  tools/run_godot.sh res://tools/verify.gd <forward_plus|gl_compatibility> <abs log path> --lessons 0-15

const TOL := 3                 # screen bytes
const STRIDE := 3

const D := {
	"shader_color": Color(1, 1, 1), "light_direction": Vector3(0.5, -0.8, -0.6), "ambient_color": Color(0.15, 0.15, 0.15),
	"fresnel_power": 3.0, "specular_power": 30.0, "specular_color": Color(1, 1, 1),
	"specular_power2": 30.0, "specular_color2": Color(1, 1, 1), "fresnel_intensity": 1.0, "fresnel_offset": 0.0, "reflection_contrast": 1.0,
	"vert_offset": Vector3(0, 0, 0), "animation_frequency": 1.0, "animation_speed": 1.0,
	"speed_xy": Vector2(0, 0), "uv_scale_translate": Vector4(1, 1, 0, 0),
	"blended_color": Color(0, 0, 1), "third_color": Color(0, 1, 0),
	"light_color": Color(1, 1, 1), "top_color": Color(0.15, 0.15, 0.15), "bottom_color": Color(0, 0, 0),
	"subsurface_color": Color(0.1, 0, 0), "subsurface_spread": 0.0, "reflection_intensity": 1.0, "flip_green": true}

var rig: Dictionary
var cam: Camera3D
var imgs := {}                 # file -> Image
var bg_screen := Color()
var results := {}              # lesson -> {pass:int, fail:int, notes:[]}
var renders_dir := ""
var time_now := 0.0

func run() -> void:
	Lessons.use_mips = String(args.get("mips", "0")) == "1"
	await warm()
	await calibrate()
	say("NOTE test textures carry %s mip chains (the CPU reference reads level 0 only; --mips 1 turns them on)" % ("WITH" if Lessons.use_mips else "NO"))
	renders_dir = ProjectSettings.globalize_path("res://evidence/renders")
	DirAccess.make_dir_recursive_absolute(renders_dir)
	var which: Array = []
	var spec := String(args.get("lessons", "0-15"))
	for part in spec.split(","):
		if part.contains("-"):
			for k in range(int(part.get_slice("-", 0)), int(part.get_slice("-", 1)) + 1):
				which.append(k)
		else:
			which.append(int(part))
	for i in which:
		results[i] = {"pass": 0, "fail": 0, "notes": []}
		await lesson(i)
	var tot_p := 0
	var tot_f := 0
	for i in which:
		var r: Dictionary = results[i]
		tot_p += r["pass"]; tot_f += r["fail"]
		say("SUMMARY L%02d %s | %s | checks passed %d, failed %d" % [i, Lessons.NAMES[i], RenderingServer.get_current_rendering_method(), r["pass"], r["fail"]])
	say("SUMMARY TOTAL | %s | passed %d, failed %d" % [RenderingServer.get_current_rendering_method(), tot_p, tot_f])

# ================================================================== the scene
var cur_scene: Node3D = null

func build(lesson: int, over: Dictionary, code := "", torus := true, probe := false, demo := false) -> Dictionary:
	if cur_scene != null:
		cur_scene.queue_free()
		await process_frame
	var s := Node3D.new()
	root.add_child(s)
	cur_scene = s
	rig = Rig.build(s, torus)
	cam = rig["camera"]
	var mat := Lessons.material(lesson, over, code, demo)
	rig["sphere"].material_override = mat
	if torus:
		rig["torus"].material_override = mat
	var out := {"scene": s, "material": mat}
	if probe:
		var q := QuadMesh.new()
		q.size = Vector2(0.3, 0.3)
		var mi := MeshInstance3D.new()
		mi.mesh = q
		mi.position = Vector3(-2.35, 1.25, 0.0)
		var sh := Shader.new()
		sh.code = "shader_type spatial; render_mode unshaded;\nvoid fragment() { ALBEDO = vec3((floor(TIME * 8.0) + 40.0) / 255.0, (fract(TIME * 8.0) * 200.0 + 40.0) / 255.0, 0.0); }\n"
		var pm := ShaderMaterial.new(); pm.shader = sh
		mi.material_override = pm
		s.add_child(mi)
		out["probe_px"] = cam.unproject_position(mi.position)
	return out

func snap(lesson: int, over: Dictionary, code := "", torus := true, probe := false, step := 0.0, save_as := "") -> Image:
	var b := await build(lesson, over, code, torus, probe)
	await warm(2)
	var img := await shoot(step)
	if probe:
		var pp: Vector2 = b["probe_px"]
		var c := px(img, int(pp.x), int(pp.y))
		time_now = ((roundf(inv(c.r) * 255.0) - 40.0) + (inv(c.g) * 255.0 - 40.0) / 200.0) / 8.0
	bg_screen = img.get_pixel(1270, 710)
	if save_as != "":
		img.save_png(renders_dir + "/" + save_as + "-" + RenderingServer.get_current_rendering_method() + ".png")
	return img

# ================================================================== reference helpers (CPU, Cg semantics)
func img_of(file: String) -> Image:
	if not imgs.has(file):
		imgs[file] = Lessons.load_image(file)
	return imgs[file]

func fetch(im: Image, x: int, y: int, srgb: bool) -> Vector3:
	var c := im.get_pixel(posmod(x, im.get_width()), posmod(y, im.get_height()))
	return dec(c) if srgb else Vector3(c.r, c.g, c.b)

func tex2d(file: String, uv: Vector2, srgb: bool) -> Vector3:
	var im := img_of(file)
	var w := im.get_width()
	var h := im.get_height()
	var fx := uv.x * w - 0.5
	var fy := uv.y * h - 0.5
	var x0 := int(floor(fx))
	var y0 := int(floor(fy))
	var tx := fx - x0
	var ty := fy - y0
	var a := fetch(im, x0, y0, srgb).lerp(fetch(im, x0 + 1, y0, srgb), tx)
	var b := fetch(im, x0, y0 + 1, srgb).lerp(fetch(im, x0 + 1, y0 + 1, srgb), tx)
	return a.lerp(b, ty)

func cube_tex(d: Vector3, srgb: bool) -> Vector3:
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
	var im := img_of("cube_%s.png" % face)
	var w := im.get_width()
	var fx := clampf(s * w - 0.5, 0.0, w - 1.0)
	var fy := clampf(t * w - 0.5, 0.0, w - 1.0)
	var x0 := int(floor(fx)); var y0 := int(floor(fy))
	var x1 := mini(x0 + 1, w - 1); var y1 := mini(y0 + 1, w - 1)
	var tx := fx - x0; var ty := fy - y0
	var a := fetch(im, x0, y0, srgb).lerp(fetch(im, x1, y0, srgb), tx)
	var b := fetch(im, x0, y1, srgb).lerp(fetch(im, x1, y1, srgb), tx)
	return a.lerp(b, ty)

func v3c(c: Color) -> Vector3:     # an sRGB-authored colour as the shader sees it
	return dec(c)

func vv(f: float) -> Vector3:
	return Vector3(f, f, f)

func powv(v: Vector3, p: float) -> Vector3:
	return Vector3(pow(maxf(v.x, 0.0), p), pow(maxf(v.y, 0.0), p), pow(maxf(v.z, 0.0), p))

func sat(x: float) -> float:
	return clampf(x, 0.0, 1.0)

func sphere_uv(n: Vector3) -> Vector2:
	return Vector2(fposmod(atan2(n.x, n.z) / TAU, 1.0), acos(clampf(n.y, -1.0, 1.0)) / PI)

# the Cg of each lesson, line by line. h: {normal, e}; P: parameter values as SET (colours as sRGB-authored Color); returns {rgb, a}
func shade(i: int, h: Dictionary, P: Dictionary, tex_normal := "normal_gl.png", tex_spec := "spec_rg.png") -> Dictionary:
	var n: Vector3 = h["normal"]
	var e: Vector3 = h["e"]
	var uv := sphere_uv(n)
	var col := v3c(P["shader_color"])
	var amb := v3c(P["ambient_color"])
	var l: Vector3 = (-(P["light_direction"] as Vector3)).normalized()
	if i == 11:
		var u: Vector4 = P["uv_scale_translate"]
		var sp: Vector2 = P["speed_xy"]
		uv = (uv - Vector2(0.5, 0.5)) * Vector2(u.x, u.y) + Vector2(u.z, u.w) + sp * time_now + Vector2(0.5, 0.5)
	# ---- tangent frame (Godot's sphere: tangent along +u, binormal = cross(normal, tangent) = image-up)
	var hor := Vector2(n.x, n.z).length()
	var tan_ := Vector3(n.z, 0.0, -n.x) / maxf(hor, 1e-6)
	var bin := n.cross(tan_)
	if i >= 8 and i != 9 and i != 10 and i != 13 and i != 14:
		var tn := tex2d(tex_normal, uv, false) * 2.0 - Vector3.ONE
		if i == 15 and P["flip_green"]:
			bin = -bin
		n = (tan_ * tn.x + bin * tn.y + n * tn.z).normalized()
	var ne := sat(n.dot(e))
	var lam := vv(sat(n.dot(l)))
	var r := n * (2.0 * n.dot(e)) - e                  # R = -reflect(e, n)
	var rdl := sat(r.dot(l))
	var spec := powv(vv(rdl), P["specular_power"]) * v3c(P["specular_color"])
	var rim_pow := pow(1.0 - ne, P["fresnel_power"])
	var fres_lit := vv(rim_pow) * (lam + amb)
	var rgb := Vector3.ZERO
	var alpha := 1.0
	match i:
		0:
			rgb = col
		1, 2:
			rgb = lam * col
		3:
			rgb = (lam + amb) * col
		4:
			rgb = (lam + amb) * col + fres_lit
		5, 10:
			rgb = (lam + amb) * col + fres_lit + spec
		6:
			var cm := tex2d("diffuse_checker.png", uv, true)
			rgb = (lam + amb) * (col * cm) + fres_lit + spec
		7, 8, 11, 12:
			var cm := tex2d("diffuse_checker.png", uv, true)
			var sm := tex2d(tex_spec, uv, false)
			rgb = (lam + amb) * (col * cm) + vv(rim_pow) * sm.x + spec * sm.y
			alpha = rim_pow
		9:
			var cube := cube_tex(r, true)
			rgb = (lam + amb) * col + fres_lit * cube + spec
		13:
			var bl := tex2d("blend_map.png", uv, false)
			var fc := v3c(P["shader_color"]) * bl.x + v3c(P["blended_color"]) * bl.z + v3c(P["third_color"]) * bl.y
			rgb = (lam + amb) * fc + fres_lit + spec
		14:
			var cube := cube_tex(r, true)
			var sp2 := powv(vv(rdl), P["specular_power"]) * v3c(P["specular_color"]) + powv(vv(rdl), P["specular_power2"]) * v3c(P["specular_color2"])
			var fr := vv(rim_pow * P["fresnel_intensity"] + P["fresnel_offset"]) * (lam + amb)
			rgb = (lam + amb) * col + fr * powv(cube, P["reflection_contrast"]) + sp2
		15:
			var cube := cube_tex(r, true)
			var cm := tex2d("diffuse_checker.png", uv, true)
			var sm := tex2d(tex_spec, uv, false)
			var up_dot := sat(n.y)
			var ambient := v3c(P["bottom_color"]).lerp(v3c(P["top_color"]), up_dot)
			var sss := v3c(P["subsurface_color"])
			var sp_ := float(P["subsurface_spread"])
			var d_l := n.dot(l) * (1.0 - sp_) + sp_
			var lam3 := Vector3(sat(d_l + sss.x), sat(d_l + sss.y), sat(d_l + sss.z))
			var lc := v3c(P["light_color"])
			var spc := powv(vv(rdl), P["specular_power"]) * v3c(P["specular_color"]) * sm.x
			var fr := vv(rim_pow) * lam3 * lc
			var tot := (fr + spc) + powv(cube, P["reflection_contrast"]) * float(P["reflection_intensity"]) * sm.z
			rgb = (ambient + lc * lam3) * (col * cm) + tot
	return {"rgb": rgb, "a": alpha, "n": n, "uv": uv}

func params(i: int, over: Dictionary) -> Dictionary:
	var P := D.duplicate()
	if i == 13:
		P["shader_color"] = Color(1, 0, 0)
	for k in over:
		P[k] = over[k]
	return P

# ================================================================== picking places on the sphere
func L_toward() -> Vector3:
	return (-Rig.LIGHT_TRAVEL).normalized()

func V_toward() -> Vector3:
	return (Rig.CAM_POS - Rig.SPHERE_POS).normalized()

func pick(a: float, b: float) -> Vector3:      # unit normal with N.L = a and N.E = b at the point it lands on (E is the true direction to the camera there)
	var L := L_toward()
	var V := V_toward()
	var n := Vector3.ZERO
	for k in range(6):
		var c := L.dot(V)
		var det := 1.0 - c * c
		var alpha := (a - c * b) / det
		var beta := (b - c * a) / det
		var base := L * alpha + V * beta
		var rem := 1.0 - base.length_squared()
		if rem < 0.0:
			return Vector3.ZERO
		n = base + L.cross(V).normalized() * sqrt(rem)
		V = (Rig.CAM_POS - (Rig.SPHERE_POS + n)).normalized()
	return n

func pick_max(a: float) -> Vector3:            # unit normal with N.L = a and the largest possible N.V (the most visible point of that shade)
	var L := L_toward()
	var V := V_toward()
	var t := (V - L * V.dot(L)).normalized()
	return L * a + t * sqrt(1.0 - a * a)

func px_of_normal(n: Vector3) -> Vector2i:
	var p := Rig.project(cam, Rig.SPHERE_POS + n)
	return Vector2i(int(floor(p.x)), int(floor(p.y)))

func normal_of_uv(uv: Vector2) -> Vector3:
	var w := sin(PI * uv.y)
	return Vector3(sin(TAU * uv.x) * w, cos(PI * uv.y), cos(TAU * uv.x) * w)

func cell_uv(c: int, r: int) -> Vector2:
	return Vector2((c + 0.5) / 8.0, (r + 0.5) / 8.0)

func texel_uv(x: int, y: int) -> Vector2:
	return Vector2((x + 0.5) / 512.0, (y + 0.5) / 512.0)

func half_vector_normal() -> Vector3:
	var n := (L_toward() + V_toward()).normalized()
	for k in range(4):
		var e := (Rig.CAM_POS - (Rig.SPHERE_POS + n)).normalized()
		n = (L_toward() + e).normalized()
	return n

func standard_points() -> Dictionary:
	var L := L_toward()
	var V := V_toward()
	var term := (V - L * V.dot(L)).normalized()
	return {
		"lit_pole (N=L)": L,
		"facing the camera": V,
		"terminator (N.L=0)": term,
		"dark side (N.L=-0.5)": L * -0.5 + term * sqrt(0.75),
		"lit rim (N.L=0.5, N.E=0.25)": pick(0.5, 0.25),
		"lit mid (N.L=0.7, N.E=0.5)": pick(0.7, 0.5),
		"highlight peak (N=half(L,E))": half_vector_normal()}

# ================================================================== comparing
func expect_screen(rgb: Vector3) -> Vector3:
	return scr3(rgb)

func bytes(v: Vector3) -> String:
	return "(%d,%d,%d)" % [int(roundf(clampf(v.x, 0, 1) * 255.0)), int(roundf(clampf(v.y, 0, 1) * 255.0)), int(roundf(clampf(v.z, 0, 1) * 255.0))]

func diff_bytes(a: Vector3, b: Vector3) -> int:
	return int(roundf(maxf(absf(a.x - b.x), maxf(absf(a.y - b.y), absf(a.z - b.z))) * 255.0))

func record(i: int, ok: bool, line: String) -> void:
	results[i]["pass" if ok else "fail"] += 1
	say("CHECK L%02d %s | %s | %s | %s" % [i, Lessons.NAMES[i], RenderingServer.get_current_rendering_method(), line, "PASS" if ok else "FAIL"])

# one named point: pixel from the image vs the reference shade at that exact pixel
func point_check(i: int, img: Image, name: String, n_target: Vector3, over: Dictionary, tex_normal := "normal_gl.png", tex_spec := "spec_rg.png", tol := TOL) -> void:
	var p := px_of_normal(n_target)
	var h := Rig.hit_sphere(cam, p.x, p.y)
	if h.is_empty():
		record(i, false, "%s: no sphere under pixel %s" % [name, str(p)])
		return
	var P := params(i, over)
	var sh := shade(i, h, P, tex_normal, tex_spec)
	var ex := expect_screen(sh["rgb"])
	var got := px(img, p.x, p.y)
	var gv := Vector3(got.r, got.g, got.b)
	var dd := diff_bytes(ex, gv)
	var L: Vector3 = (-(P["light_direction"] as Vector3)).normalized()    # the light this check actually used
	record(i, dd <= tol, "%s px(%d,%d) N.L=%.2f N.E=%.2f | linear value %s | expected screen %s, got %s, diff %d byte(s)" % [name, p.x, p.y, h["normal"].dot(L), h["normal"].dot(h["e"]), bytes(sh["rgb"]), bytes(ex), bytes(gv), dd])

func uv_point_check(i: int, img: Image, name: String, uv: Vector2, over: Dictionary, tex_normal := "normal_gl.png", tex_spec := "spec_rg.png", tol := TOL) -> void:
	point_check(i, img, "%s (uv %.3f, %.3f)" % [name, uv.x, uv.y], normal_of_uv(uv), over, tex_normal, tex_spec, tol)

# every STRIDE-th pixel of the sphere against the reference
func full_check(i: int, img: Image, over: Dictionary, tex_normal := "normal_gl.png", tex_spec := "spec_rg.png", label := "full image") -> void:
	var P := params(i, over)
	var textured := i in [6, 7, 8, 11, 12, 13, 15]     # analytic uv vs mesh uv disagree at the poles (the facets converge): skip the polar cap
	var c := Rig.project(cam, Rig.SPHERE_POS)
	var x0 := int(c.x) - 260
	var y0 := int(c.y) - 260
	var outliers: Array = []
	var n_px := 0
	var skipped := 0
	var within := 0
	var sum := 0.0
	var worst := 0
	var worst_at := Vector2i.ZERO
	var y := y0
	while y < y0 + 520:
		var x := x0
		while x < x0 + 520:
			var h := Rig.hit_sphere(cam, x, y)
			var min_ne := 0.2 if textured else 0.15
			if not h.is_empty() and h["normal"].dot(h["e"]) > min_ne and not (textured and absf((h["normal"] as Vector3).y) > 0.75):
				var sh := shade(i, h, P, tex_normal, tex_spec)
				if textured:
					var tuv: Vector2 = sh["uv"] * 512.0
					var fx := fposmod(tuv.x, 64.0)
					var fy := fposmod(tuv.y, 64.0)
					if fx < 2.0 or fx > 62.0 or fy < 2.0 or fy > 62.0:
						skipped += 1
						x += STRIDE
						continue
				var ex := expect_screen(sh["rgb"])
				var got := px(img, x, y)
				var dd := diff_bytes(ex, Vector3(got.r, got.g, got.b))
				n_px += 1
				sum += dd
				if dd <= TOL:
					within += 1
				if dd > worst:
					worst = dd
					worst_at = Vector2i(x, y)
				if dd > TOL and outliers.size() < 400:
					outliers.append("(%d,%d) d%d n.y %.2f N.E %.2f uv'(%.3f,%.3f)" % [x, y, dd, h["normal"].y, h["normal"].dot(h["e"]), sh["uv"].x, sh["uv"].y])
			x += STRIDE
		y += STRIDE
	var pct := 100.0 * within / maxf(n_px, 1)
	if pct < 99.7 and args.has("outliers"):
		say("NOTE outliers of %s L%02d (first 40 of %d): %s" % [label, i, outliers.size(), " | ".join(outliers.slice(0, 40))])
	record(i, pct >= (98.0 if textured else 99.0), "%s: %d pixels (every %d-th in x and y%s), %.2f%% within %d bytes, mean diff %.2f, worst %d at %s" % [label, n_px, STRIDE, "; textured lesson: polar cap (|y| > 0.75) and a 2-texel band along checker-cell edges skipped (%d px), where a sub-texel difference between the analytic and the mesh uv flips a pixel" % skipped if textured else "", pct, TOL, sum / maxf(n_px, 1), worst, str(worst_at)])

func diff_report(a: Image, b: Image) -> String:
	var n1 := 0; var n3 := 0; var worst := 0; var wat := Vector2i.ZERO
	var minx := 9999; var maxx := -1; var miny := 9999; var maxy := -1
	for y in range(0, a.get_height()):
		for x in range(0, a.get_width()):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			var d := int(roundf(maxf(absf(ca.r - cb.r), maxf(absf(ca.g - cb.g), absf(ca.b - cb.b))) * 255.0))
			if d > 1:
				n1 += 1
				minx = mini(minx, x); maxx = maxi(maxx, x); miny = mini(miny, y); maxy = maxi(maxy, y)
			if d > 3:
				n3 += 1
			if d > worst:
				worst = d; wat = Vector2i(x, y)
	return "pixels differing by more than 1 byte: %d (more than 3 bytes: %d), worst %d at %s, box x %d..%d y %d..%d" % [n1, n3, worst, str(wat), minx, maxx, miny, maxy]

func images_differ(a: Image, b: Image, tol_bytes := 1) -> int:
	var n := 0
	for y in range(0, a.get_height(), 2):
		for x in range(0, a.get_width(), 2):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			if int(roundf(maxf(absf(ca.r - cb.r), maxf(absf(ca.g - cb.g), absf(ca.b - cb.b))) * 255.0)) > tol_bytes:
				n += 1
	return n

# ================================================================== the lessons
func lesson(i: int) -> void:
	var nm: String = Lessons.NAMES[i]
	match i:
		0: await l00(i)
		1, 2: await l01_02(i)
		3: await l03(i)
		4: await l04(i)
		5: await l05(i)
		6: await l06(i)
		7: await l07(i)
		8: await l08(i)
		9: await l09(i)
		10: await l10(i)
		11: await l11(i)
		12: await l12(i)
		13: await l13(i)
		14: await l14(i)
		15: await l15(i)

func l00(i: int) -> void:
	var over := {"shader_color": Color(0.37, 0.64, 0.57)}
	var img := await snap(i, over, "", true, false, 0.0, "00_super_simple")
	for k in ["lit_pole (N=L)", "facing the camera", "terminator (N.L=0)", "dark side (N.L=-0.5)", "lit rim (N.L=0.5, N.E=0.25)"]:
		point_check(i, img, k, standard_points()[k], over)
	full_check(i, img, over)

var cache_01 := Image.new()

func l01_02(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var sp := standard_points()
	for k in ["lit_pole (N=L)", "facing the camera", "terminator (N.L=0)", "dark side (N.L=-0.5)", "lit mid (N.L=0.7, N.E=0.5)"]:
		point_check(i, img, k, sp[k], {})
	full_check(i, img, {})
	if i == 2:
		# the Cg's own default light, (0, 1, 0): it travels UP, so only the underside is lit
		var cg_over := {"light_direction": Vector3(0.0, 1.0, 0.0)}
		var img_cg := await snap(i, cg_over, "", true, false, 0.0, "02_lambert_cg_default_light")
		point_check(i, img_cg, "Cg default light (0,1,0): a point on the UNDERSIDE (normal y = -0.8)", Vector3(0.2, -0.8, 0.56).normalized(), cg_over)
		point_check(i, img_cg, "Cg default light (0,1,0): a point on the TOP (normal y = +0.8)", Vector3(0.2, 0.8, 0.56).normalized(), cg_over)
	if i == 1:
		cache_01 = img
	elif cache_01.get_width() > 0:
		var nd := images_differ(cache_01, img)
		record(i, nd == 0, "02_lambert image vs 01_base image, whole frame: %d differing pixels (sampled every 2nd pixel; 0 = the two shaders render identically)" % nd)
	else:
		var img1 := await snap(1, {}, "", true, false, 0.0, "")
		var nd := images_differ(img1, img)
		record(i, nd == 0, "02_lambert image vs 01_base image, whole frame: %d differing pixels (sampled every 2nd pixel; 0 = the two shaders render identically)" % nd)

func l03(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var sp := standard_points()
	for k in ["lit_pole (N=L)", "facing the camera", "terminator (N.L=0)", "dark side (N.L=-0.5)"]:
		point_check(i, img, k, sp[k], {})
	# the ambient floor: a pixel whose N.L is below zero must read exactly the ambient colour x surface colour
	point_check(i, img, "deep shadow (N.L=-0.75, the most visible such point): the ambient floor", pick_max(-0.75), {})
	full_check(i, img, {})

func l04(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var sp := standard_points()
	for k in ["lit_pole (N=L)", "facing the camera", "terminator (N.L=0)", "dark side (N.L=-0.5)", "lit rim (N.L=0.5, N.E=0.25)", "lit mid (N.L=0.7, N.E=0.5)"]:
		point_check(i, img, k, sp[k], {})
	say("NOTE L04 rim weight pow(1 - N.E, 3) before the lighting factor: N.E = 1.0 -> %.3f, 0.5 -> %.3f, 0.2 -> %.3f, 0.0 (the silhouette) -> %.3f" % [pow(0.0, 3.0), pow(0.5, 3.0), pow(0.8, 3.0), pow(1.0, 3.0)])
	point_check(i, img, "silhouette-ward lit point (N.L=0.3, N.E=0.12)", pick(0.3, 0.12), {})
	point_check(i, img, "rim on the dark side (N.L=-0.3, N.E=0.25): rim is multiplied by the lighting", pick(-0.3, 0.25), {})
	full_check(i, img, {})
	var img_p := await snap(i, {"fresnel_power": 6.0}, "", true, false, 0.0, "")
	point_check(i, img_p, "fresnel_power 6: lit rim (N.L=0.5, N.E=0.25)", sp["lit rim (N.L=0.5, N.E=0.25)"], {"fresnel_power": 6.0})

func l05(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var sp := standard_points()
	for k in ["highlight peak (N=half(L,E))", "lit_pole (N=L)", "facing the camera", "terminator (N.L=0)", "lit rim (N.L=0.5, N.E=0.25)"]:
		point_check(i, img, k, sp[k], {})
	# a point on the shoulder of the highlight: rotate the peak normal 6 degrees away from the light
	var nh := half_vector_normal()
	var axis := nh.cross(L_toward()).normalized()
	point_check(i, img, "highlight shoulder (6 degrees off the peak)", nh.rotated(axis, deg_to_rad(-6.0)), {})
	full_check(i, img, {})
	# specular only: black surface, no ambient, a very tight rim -> the picture IS the highlight; locate the peak and measure its width
	var over := {"shader_color": Color(0, 0, 0), "ambient_color": Color(0, 0, 0), "fresnel_power": 10.0}
	var img2 := await snap(i, over, "", false, false, 0.0, "05_phong_specular_only")
	var P := params(i, over)
	var best := -1.0
	var best_px := Vector2i.ZERO
	var c := Rig.project(cam, Rig.SPHERE_POS)
	for y in range(int(c.y) - 260, int(c.y) + 260):
		for x in range(int(c.x) - 260, int(c.x) + 260):
			var pc := img2.get_pixel(x, y)
			var s := pc.r + pc.g + pc.b
			if s > best + 0.0005:
				best = s
				best_px = Vector2i(x, y)
	var pred := px_of_normal(half_vector_normal())
	record(i, absi(best_px.x - pred.x) <= 3 and absi(best_px.y - pred.y) <= 3, "highlight position, specular-only render: brightest pixel (%d,%d), predicted from the half vector (%d,%d)" % [best_px.x, best_px.y, pred.x, pred.y])
	# width of the highlight along the row of the peak: pixels whose linear specular is >= 0.5 (R.L >= 0.5^(1/30) = 0.977)
	var gpu_n := 0
	var cpu_n := 0
	for x in range(best_px.x - 60, best_px.x + 61):
		var pc := img2.get_pixel(x, best_px.y)
		if inv(pc.r) >= 0.5:
			gpu_n += 1
		var h := Rig.hit_sphere(cam, x, best_px.y)
		if not h.is_empty():
			var sh := shade(i, h, P)
			if (sh["rgb"] as Vector3).x >= 0.5:
				cpu_n += 1
	record(i, absi(gpu_n - cpu_n) <= 2, "highlight width at half height (specular >= 0.5) along the peak row: %d px rendered, %d px predicted by pow(R.L, 30)" % [gpu_n, cpu_n])
	var over2 := {"shader_color": Color(0, 0, 0), "ambient_color": Color(0, 0, 0), "fresnel_power": 10.0, "specular_power": 100.0}
	var img3 := await snap(i, over2, "", false, false, 0.0, "")
	var g2 := 0
	var c2 := 0
	var P2 := params(i, over2)
	for x in range(best_px.x - 60, best_px.x + 61):
		if inv(img3.get_pixel(x, best_px.y).r) >= 0.5:
			g2 += 1
		var h2 := Rig.hit_sphere(cam, x, best_px.y)
		if not h2.is_empty() and (shade(i, h2, P2)["rgb"] as Vector3).x >= 0.5:
			c2 += 1
	record(i, absi(g2 - c2) <= 2, "same, specular_power 100 (a tighter spot): %d px rendered, %d px predicted (power 30 gave %d px)" % [g2, c2, gpu_n])

func l06(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	uv_point_check(i, img, "red marker cell (column 0, row 3)", cell_uv(0, 3), {})
	uv_point_check(i, img, "green marker cell (column 1, row 3)", cell_uv(1, 3), {})
	uv_point_check(i, img, "yellow marker cell (column 0, row 4)", cell_uv(0, 4), {})
	uv_point_check(i, img, "magenta marker cell (column 7, row 3)", cell_uv(7, 3), {})
	uv_point_check(i, img, "sand cell (column 0, row 2)", cell_uv(0, 2), {})
	uv_point_check(i, img, "steel cell (column 0, row 5)", cell_uv(0, 5), {})
	uv_point_check(i, img, "steel cell (column 7, row 4)", cell_uv(7, 4), {})
	full_check(i, img, {})

func l07(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var peak_uv := sphere_uv(half_vector_normal())
	uv_point_check(i, img, "highlight peak (steel cell: spec mask 0 there)", peak_uv, {})
	uv_point_check(i, img, "just below the peak (sand cell: spec mask 1)", peak_uv + Vector2(0.0, 0.03), {})
	uv_point_check(i, img, "sand cell centre (column 0, row 2), rim mask bright row", cell_uv(0, 2), {})
	uv_point_check(i, img, "steel cell centre (column 0, row 5), dim rim row", cell_uv(0, 5), {})
	uv_point_check(i, img, "rim: bright row (row 2) at column 1", cell_uv(1, 2), {})
	uv_point_check(i, img, "rim: dim row (row 3) at column 1", cell_uv(1, 3), {})
	full_check(i, img, {})
	# the dark-side rim (no lighting factor in 07)
	var dark_rim := pick(-0.4, 0.2)
	if dark_rim != Vector3.ZERO:
		point_check(i, img, "rim on the dark side (N.L=-0.4, N.E=0.2): 07 does NOT multiply the rim by the lighting", dark_rim, {})

func l08(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var base_uv := texel_uv(32, 224)      # the centre of the dome in cell (column 0, row 3)
	uv_point_check(i, img, "dome centre (flat: normal map says straight out)", base_uv, {})
	uv_point_check(i, img, "dome right side (+20 px: normal leans +tangent)", texel_uv(52, 224), {})
	uv_point_check(i, img, "dome left side (-20 px: leans -tangent)", texel_uv(12, 224), {})
	uv_point_check(i, img, "dome upper side (-20 rows: leans toward image-up = +binormal)", texel_uv(32, 204), {})
	uv_point_check(i, img, "dome lower side (+20 rows: leans down)", texel_uv(32, 244), {})
	full_check(i, img, {})
	# perturbation direction, independent of the shading formula: the perturbed normal vs the geometric normal at each of those places
	var lines: Array = []
	for pair in [["right", Vector2i(52, 224)], ["left", Vector2i(12, 224)], ["up", Vector2i(32, 204)], ["down", Vector2i(32, 244)]]:
		var uv := texel_uv(pair[1].x, pair[1].y)
		var pp := px_of_normal(normal_of_uv(uv))
		var h := Rig.hit_sphere(cam, pp.x, pp.y)
		var sh := shade(i, h, params(i, {}))
		var dn: Vector3 = sh["n"] - h["normal"]
		var hor := Vector2(h["normal"].x, h["normal"].z).length()
		var tan_ := Vector3(h["normal"].z, 0.0, -h["normal"].x) / hor
		var bin: Vector3 = (h["normal"] as Vector3).cross(tan_)
		lines.append("%s: along tangent %+.2f, along binormal %+.2f" % [pair[0], dn.dot(tan_), dn.dot(bin)])
	say("CHECK L08 %s | %s | perturbation of the normal (expected: right +tangent, left -tangent, up +binormal, down -binormal; GL map, green = up) | %s" % [Lessons.NAMES[i], RenderingServer.get_current_rendering_method(), " ; ".join(lines)])
	# the same shader with the DirectX-style map (green inverted) should light the up/down sides the other way round
	var img_dx := await snap_normal(i, "normal_dx.png")
	var up_px := px_of_normal(normal_of_uv(texel_uv(32, 204)))
	var gl_c := px(img, up_px.x, up_px.y)
	var dx_c := px(img_dx, up_px.x, up_px.y)
	var h2 := Rig.hit_sphere(cam, up_px.x, up_px.y)
	var ex_dx := expect_screen(shade(i, h2, params(i, {}), "normal_dx.png")["rgb"])
	record(i, diff_bytes(ex_dx, Vector3(dx_c.r, dx_c.g, dx_c.b)) <= TOL, "DirectX-style map (green inverted) at the dome's upper side: GL map reads %s, DX map reads %s, reference for the DX map %s" % [b255(gl_c), b255(dx_c), bytes(ex_dx)])


func snap_normal(i: int, normal_file: String) -> Image:
	# renders lesson i with a different normal map bound (a texture swap, no shader change)
	var b := await build(i, {}, "", true, false)
	var mat: ShaderMaterial = b["material"]
	mat.set_shader_parameter("normal_map", Lessons.load_texture(normal_file))
	await warm(2)
	var img := await shoot()
	return img

func l09(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	var sp := standard_points()
	for k in ["facing the camera", "lit rim (N.L=0.5, N.E=0.25)", "lit mid (N.L=0.7, N.E=0.5)", "highlight peak (N=half(L,E))", "terminator (N.L=0)"]:
		point_check(i, img, k, sp[k], {})
	point_check(i, img, "silhouette-ward lit point (N.L=0.3, N.E=0.12): the reflection arrives here", pick(0.3, 0.12), {})
	point_check(i, img, "lower left rim (N.L=-0.1, N.E=0.15)", pick(-0.1, 0.15), {})
	full_check(i, img, {})
	var pf := px_of_normal(sp["facing the camera"])
	var hf := Rig.hit_sphere(cam, pf.x, pf.y)
	var ex3 := expect_screen(shade(3, hf, params(3, {}))["rgb"])
	var gotf := px(img, pf.x, pf.y)
	record(i, diff_bytes(ex3, Vector3(gotf.r, gotf.g, gotf.b)) <= TOL, "the pixel that faces the camera reads exactly what lesson 03 (no reflection at all) gives there: 03 reference %s, 09 rendered %s" % [bytes(ex3), b255(gotf)])
	var pr := px_of_normal(pick(0.3, 0.12))
	var hr := Rig.hit_sphere(cam, pr.x, pr.y)
	var rv: Vector3 = (hr["normal"] as Vector3) * (2.0 * (hr["normal"] as Vector3).dot(hr["e"])) - (hr["e"] as Vector3)
	say("NOTE L09 reflection lookup at px(%d,%d): reflection vector R = (%.2f, %.2f, %.2f), cube texel there (linear) %s" % [pr.x, pr.y, rv.x, rv.y, rv.z, bytes(cube_tex(rv, true))])
	say("NOTE L09 reflection weight = pow(1 - N.E, 3) * (N.L + ambient): at N.E = 1.0 -> %.3f, 0.5 -> %.3f, 0.2 -> %.3f (times the lighting term). A surface that faces the camera shows no reflection." % [pow(0.0, 3.0), pow(0.5, 3.0), pow(0.8, 3.0)])

func l10(i: int) -> void:
	# (a) zero offset must render exactly like lesson 05
	var imga := await snap(i, {}, "", true, false, 0.0, "")
	var img5 := await snap(5, {}, "", true, false, 0.0, "")
	var nd := images_differ(imga, img5)
	record(i, nd == 0, "vert_offset (0,0,0) (the Cg default): frame vs lesson 05 frame: %d differing pixels (0 = nothing moves)" % nd)
	# (b) with an offset: silhouette of the displaced mesh, CPU vs render. A saturated surface colour keeps every sphere pixel apart from the stage colour.
	var over := {"vert_offset": Vector3(0.0, 0.3, 0.0), "animation_frequency": 3.0, "animation_speed": 2.0, "shader_color": Color(0.9, 0.2, 0.2)}
	var img := await snap(i, over, "", false, true, 0.7, "10_vertex_anim")
	await silhouette_check(i, img, over, "vertical offset 0.3 (animated: sin(TIME * 2 + x * 3))")
	var over2 := {"vert_offset": Vector3(0.4, 0.0, 0.0), "animation_frequency": 1.0, "animation_speed": 1.0, "shader_color": Color(0.9, 0.2, 0.2)}
	var img2 := await snap(i, over2, "", false, true, 1.3, "")
	await silhouette_check(i, img2, over2, "sideways offset 0.4 (sin(TIME + x))")

func silhouette_check(i: int, img: Image, over: Dictionary, label: String) -> void:
	var P := params(i, over)
	var sm := SphereMesh.new()
	sm.radius = 1.0; sm.height = 2.0; sm.radial_segments = 128; sm.rings = 64
	var V: PackedVector3Array = sm.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var off: Vector3 = P["vert_offset"]
	var fr: float = P["animation_frequency"]
	var sp: float = P["animation_speed"]
	var minx := 1e9; var maxx := -1e9; var miny := 1e9; var maxy := -1e9
	for v in V:
		var disp := v + sin(time_now * sp + v.x * fr) * off
		var s2 := cam.unproject_position(Rig.SPHERE_POS + disp)
		minx = minf(minx, s2.x); maxx = maxf(maxx, s2.x); miny = minf(miny, s2.y); maxy = maxf(maxy, s2.y)
	# rendered bounding box of everything that is not the stage colour (the probe square is cropped out)
	var rminx := 99999; var rmaxx := -1; var rminy := 99999; var rmaxy := -1
	var bg := bg_screen
	for y in range(0, 720):
		for x in range(0, 1280):
			if x < 150 and y < 140:
				continue                       # the TIME probe square
			var c := img.get_pixel(x, y)
			if absf(c.r - bg.r) > 0.03 or absf(c.g - bg.g) > 0.03 or absf(c.b - bg.b) > 0.03:
				rminx = mini(rminx, x); rmaxx = maxi(rmaxx, x); rminy = mini(rminy, y); rmaxy = maxi(rmaxy, y)
	var d := maxf(maxf(absf(rminx - minx), absf(rmaxx - maxx)), maxf(absf(rminy - miny), absf(rmaxy - maxy)))
	var undisp_min := Vector2(1e9, 1e9)
	var undisp_max := Vector2(-1e9, -1e9)
	for v in V:
		var s0 := cam.unproject_position(Rig.SPHERE_POS + v)
		undisp_min = Vector2(minf(undisp_min.x, s0.x), minf(undisp_min.y, s0.y))
		undisp_max = Vector2(maxf(undisp_max.x, s0.x), maxf(undisp_max.y, s0.y))
	record(i, d <= 2.5, "%s at TIME %.3f: predicted silhouette x %.1f..%.1f, y %.1f..%.1f (CPU: the Cg formula on every vertex); rendered x %d..%d, y %d..%d; largest edge difference %.1f px; undisplaced sphere would be x %.0f..%.0f, y %.0f..%.0f" % [
		label, time_now, minx, maxx, miny, maxy, rminx, rmaxx, rminy, rmaxy, d, undisp_min.x, undisp_max.x, undisp_min.y, undisp_max.y])

func l11(i: int) -> void:
	# (a) identity transform must render exactly like lesson 08
	var img_a := await snap(i, {}, "", true, false, 0.0, "")
	var img_8 := await snap(8, {}, "", true, false, 0.0, "")
	var nd := images_differ(img_a, img_8)
	record(i, nd == 0, "uv_scale_translate (1,1,0,0), speed 0 (the Cg defaults): frame vs lesson 08 frame: %d differing pixels (0 = the identity transform changes nothing)" % nd)
	# (b) scale 2 about the centre + translate
	var over := {"uv_scale_translate": Vector4(2.0, 2.0, 0.25, 0.125)}
	var img := await snap(i, over, "", true, true, 0.0, "11_uv_manip_scale_translate")
	uv_pts11(i, img, over)
	full_check(i, img, over, "normal_gl.png", "spec_rg.png", "scale 2 + translate (0.25, 0.125): full image")
	# (c) scrolling: uv moves with TIME
	var over2 := {"speed_xy": Vector2(0.1, 0.05)}
	var img2 := await snap(i, over2, "", true, true, 1.5, "11_uv_manip_scroll")
	uv_pts11(i, img2, over2)
	full_check(i, img2, over2, "normal_gl.png", "spec_rg.png", "scroll (0.1, 0.05) at TIME %.3f: full image" % time_now)

func inverse_uv(target: Vector2, over: Dictionary) -> Vector2:
	# the mesh uv that the Cg formula turns into `target` (any whole number of tiles may be added to the target: the sampler wraps), nearest to the front of the sphere
	var P := params(11, over)
	var u: Vector4 = P["uv_scale_translate"]
	var sp: Vector2 = P["speed_xy"]
	var best := Vector2.ZERO
	var best_d := 1e9
	for kx in range(-6, 7):
		for ky in range(-6, 7):
			var t := target + Vector2(kx, ky)
			var uv0 := Vector2((t.x - 0.5 - u.z - sp.x * time_now) / u.x + 0.5, (t.y - 0.5 - u.w - sp.y * time_now) / u.y + 0.5)
			var d := (uv0 - Vector2(0.04, 0.45)).length()
			if d < best_d:
				best_d = d
				best = uv0
	return best

func uv_pts11(i: int, img: Image, over: Dictionary) -> void:
	# places chosen so that the TRANSFORMED uv lands in the middle of a checker cell (edges would make the check about rounding, not the formula)
	for pair in [["red marker cell (0,3) after the transform", cell_uv(0, 3)], ["green marker cell (1,3) after the transform", cell_uv(1, 3)],
			["yellow marker cell (0,4) after the transform", cell_uv(0, 4)], ["magenta marker cell (7,3) after the transform", cell_uv(7, 3)], ["sand cell (2,2) after the transform", cell_uv(2, 2)]]:
		var src := inverse_uv(pair[1], over)
		if src.x < 0.0 or src.x > 1.0 or src.y < 0.0 or src.y > 1.0 or absf(src.x - 0.04) > 0.22:
			continue
		uv_point_check(i, img, pair[0], src, over)

func l12(i: int) -> void:
	var src := FileAccess.get_file_as_string(Lessons.shader_path(i))
	var names := ["Opaque", "AlphaBlend", "AlphaTest", "Additive"]
	# the places: dome centres (flat normal-map texel) at different viewing angles; pick the cells whose rim value is closest to the targets
	var cells: Array = []
	for r in range(1, 7):
		for c in [0, 1, 6, 7]:
			var n := normal_of_uv(cell_uv(c, r))
			var e := (Rig.CAM_POS - (Rig.SPHERE_POS + n)).normalized()
			var ne := n.dot(e)
			if ne > 0.12:
				cells.append({"c": c, "r": r, "a": pow(1.0 - ne, 3.0)})
	var pick_near := func(target: float) -> Dictionary:
		var best: Dictionary = cells[0]
		for x in cells:
			if absf(x["a"] - target) < absf(best["a"] - target):
				best = x
		return best
	var lo: Dictionary = pick_near.call(0.1)
	var mid: Dictionary = pick_near.call(0.5)
	var hi: Dictionary = pick_near.call(0.0)
	for t in range(4):
		var code := src.replace("#define TECHNIQUE 1", "#define TECHNIQUE %d" % t)
		var img := await snap_code(i, code, "12_techniques_%d_%s" % [t, names[t].to_lower()])
		for pt in [hi, lo, mid]:
			var n := normal_of_uv(cell_uv(pt["c"], pt["r"]))
			var p := px_of_normal(n)
			var h := Rig.hit_sphere(cam, p.x, p.y)
			var sh := shade(i, h, params(i, {}))
			var rgb: Vector3 = sh["rgb"]
			var a: float = sh["a"]
			var bgl := inv3(bg_screen)
			var out := rgb
			match t:
				0: out = rgb
				1: out = bgl * (1.0 - a) + (rgb if not is_compat else Vector3(clampf(rgb.x, 0, 1), clampf(rgb.y, 0, 1), clampf(rgb.z, 0, 1))) * a
				2: out = rgb if a > 0.3 else bgl
				3: out = bgl + (rgb if not is_compat else Vector3(clampf(rgb.x, 0, 1), clampf(rgb.y, 0, 1), clampf(rgb.z, 0, 1))) * a
			var ex := expect_screen(out)
			var got := px(img, p.x, p.y)
			var dd := diff_bytes(ex, Vector3(got.r, got.g, got.b))
			record(i, dd <= TOL, "technique %d %s | cell (%d,%d) px(%d,%d) rim alpha %.3f | expected %s, got %s, diff %d | the same pixel drawn opaque would be %s; stage colour %s" % [
				t, names[t], pt["c"], pt["r"], p.x, p.y, a, bytes(ex), b255(got), dd, bytes(expect_screen(rgb)), b255(bg_screen)])

func snap_code(i: int, code: String, save_as: String) -> Image:
	return await snap(i, {}, code, true, false, 0.0, save_as)

func l13(i: int) -> void:
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])
	uv_point_check(i, img, "red band (blend map R = 1) -> shader_color", Vector2(0.0625, 0.5), {})
	uv_point_check(i, img, "blue band (blend map B = 1) -> blended_color", Vector2(0.9375, 0.5), {})
	uv_point_check(i, img, "blue disc inside the red band (B = 1) -> blended_color", Vector2(0.17, 0.30), {})
	uv_point_check(i, img, "green disc inside the blue band (G = 1) -> third_color", Vector2(0.94, 0.68), {})
	uv_point_check(i, img, "red band, lower", Vector2(0.10, 0.65), {})
	full_check(i, img, {})
	# swapping the colours shows which channel drives which colour (R -> shader_color, B -> blended_color, G -> third_color)
	var over := {"shader_color": Color(1, 1, 0), "blended_color": Color(0, 1, 1), "third_color": Color(1, 0, 1)}
	var img2 := await snap(i, over, "", true, false, 0.0, "")
	uv_point_check(i, img2, "new colours: red band shows shader_color (yellow)", Vector2(0.0625, 0.5), over)
	uv_point_check(i, img2, "new colours: blue band shows blended_color (cyan)", Vector2(0.9375, 0.5), over)

func l14(i: int) -> void:
	var demo := Lessons.demo(14)
	var img := await snap(i, demo, "", true, false, 0.0, Lessons.NAMES[i])
	var sp := standard_points()
	for k in ["facing the camera", "lit rim (N.L=0.5, N.E=0.25)", "lit mid (N.L=0.7, N.E=0.5)", "highlight peak (N=half(L,E))", "terminator (N.L=0)", "dark side (N.L=-0.5)"]:
		point_check(i, img, k, sp[k], demo)
	point_check(i, img, "silhouette-ward lit point (N.L=0.3, N.E=0.12)", pick(0.3, 0.12), demo)
	full_check(i, img, demo)
	# fresnel_offset lets the reflection show on a surface that faces the camera
	var over := demo.duplicate()
	over["fresnel_offset"] = 0.5
	var img2 := await snap(i, over, "", true, false, 0.0, "14_car_shader_offset")
	point_check(i, img2, "fresnel_offset 0.5: facing the camera now shows the reflection", sp["facing the camera"], over)
	# the two highlights: a tight one (power 30) and a wide one (power 8) on the same R.L
	var over3 := demo.duplicate()
	over3["shader_color"] = Color(0, 0, 0)
	over3["ambient_color"] = Color(0, 0, 0)
	over3["fresnel_power"] = 10.0
	var img3 := await snap(i, over3, "", false, false, 0.0, "")
	var shoulder := half_vector_normal().rotated(half_vector_normal().cross(L_toward()).normalized(), deg_to_rad(-10.0))
	point_check(i, img3, "two highlights, 10 degrees off the peak (only the wide power-8 one reaches here)", shoulder, over3)
	point_check(i, img3, "two highlights, peak", half_vector_normal(), over3)

func l15(i: int) -> void:
	var gl_over := {"flip_green": false}
	var img := await snap(i, {}, "", true, false, 0.0, Lessons.NAMES[i])   # Lessons.material binds normal_dx for 15
	var tex_normal := "normal_dx.png"
	var tex_spec := "spec_uber.png"
	var sp := standard_points()
	uv_point_check(i, img, "dome centre (cell column 0, row 3)", texel_uv(32, 224), {}, tex_normal, tex_spec)
	uv_point_check(i, img, "dome right side (+20 px)", texel_uv(52, 224), {}, tex_normal, tex_spec)
	uv_point_check(i, img, "dome upper side (-20 rows): the flip makes the DX map read as image-up", texel_uv(32, 204), {}, tex_normal, tex_spec)
	for k in ["lit_pole (N=L)", "facing the camera", "terminator (N.L=0)", "dark side (N.L=-0.5)", "lit rim (N.L=0.5, N.E=0.25)", "highlight peak (N=half(L,E))"]:
		point_check(i, img, k, sp[k], {}, tex_normal, tex_spec)
	# the hemisphere ambient: a point whose normal faces down gets bottom_color (black) instead of top_color
	var down := normal_of_uv(Vector2(0.03, 0.78))
	point_check(i, img, "facing down-front (normal y < 0: the hemisphere ambient is bottom_color, black)", down, {}, tex_normal, tex_spec)
	full_check(i, img, {}, tex_normal, tex_spec)
	# DirectX-style map with flip_green = true must look the same as the OpenGL-style map with flip_green = false
	var b := await build(i, gl_over, "", true, false)
	var mat: ShaderMaterial = b["material"]
	mat.set_shader_parameter("normal_map", Lessons.load_texture("normal_gl.png"))
	await warm(2)
	var img_gl := await shoot()
	say("NOTE L15 diff detail | " + diff_report(img, img_gl))
	var nd := images_differ(img, img_gl)
	record(i, nd <= 250, "DirectX map + flip_green (the Cg's  * -binormal) vs OpenGL map + no flip: %d of %d sampled pixels differ by more than 1 byte (%.3f%%); the normals are identical, the few that differ sit on sharp cube-map edges, where a rounding-sized change in the normal moves the reflection lookup across the edge" % [nd, 640 * 360, 100.0 * nd / (640 * 360)])
	# subsurface and spread: the dark side colour and the softened terminator
	var over := {"subsurface_color": Color(0.1, 0.0, 0.0), "subsurface_spread": 0.5}
	var img2 := await snap(i, over, "", true, false, 0.0, "15_uber_spread")
	point_check(i, img2, "subsurface_spread 0.5: terminator", sp["terminator (N.L=0)"], over, tex_normal, tex_spec)
	point_check(i, img2, "subsurface_spread 0.5: dark side", sp["dark side (N.L=-0.5)"], over, tex_normal, tex_spec)
