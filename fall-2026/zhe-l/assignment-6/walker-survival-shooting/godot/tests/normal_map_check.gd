# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: can run directly with --script (calibration), or be preloaded by test_materials.gd to call its static functions
## A5 normal-map check (the curl check given in the assignment's Step 3; the function bodies are copied verbatim from the assignment).
## A real tangent-space normal map is the slope field of some height surface, so its two mixed partial derivatives agree (curl about 0).
## curl_ratio about 0: a real surface behind it in this convention; about 1: no surface behind it; about 2: the surface is real but the green convention is the other one.
## Run directly, it calibrates: for the NormalGL and NormalDX of the same Metal041C set, it computes the ratio under both conventions and prints it.
## Run: ./scripts/run-test.sh normal_map_check.gd 60
## What it cannot prove: a curl of 0 only says a surface exists behind the map, not that it is the "right" surface (a normal map computed from an albedo with Sobel also passes).

# ============================================================
# Constants: the two calibration textures
# ============================================================
const GL_MAP := "res://assets/shader/metal041c/Metal041C_1K-PNG_NormalGL.png"  # OpenGL convention (the one the game uses)
const DX_MAP := "res://assets/shader/metal041c/Metal041C_1K-PNG_NormalDX.png"  # DirectX convention (calibration only)
const STRIDE := 4  # Sampling stride: 4 for 1K textures (the assignment: 8 for 4K textures)

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## When Godot calls it: once, when run with --script and the scene tree is created.
## Reads the source files of both normal maps (not through the importer) and prints the four curl ratios.
## Check: each map is lower under its own convention than under the other (GL lower with directx=false, DX lower with directx=true).
## No threshold is set here: the assignment says to set it from the values measured on this known-good pair.
func _init() -> void:
	var gl := Image.load_from_file(ProjectSettings.globalize_path(GL_MAP))
	var dx := Image.load_from_file(ProjectSettings.globalize_path(DX_MAP))
	var gl_as_gl := curl_ratio(gl, false, STRIDE)
	var gl_as_dx := curl_ratio(gl, true, STRIDE)
	var dx_as_gl := curl_ratio(dx, false, STRIDE)
	var dx_as_dx := curl_ratio(dx, true, STRIDE)
	print("image format GL=", gl.get_format(), " DX=", dx.get_format(), " size=", gl.get_size())
	print("curl_ratio NormalGL  directx=false: %.4f" % gl_as_gl)
	print("curl_ratio NormalGL  directx=true : %.4f" % gl_as_dx)
	print("curl_ratio NormalDX  directx=false: %.4f" % dx_as_gl)
	print("curl_ratio NormalDX  directx=true : %.4f" % dx_as_dx)
	var failures := 0
	failures += _check("NormalGL is lower under its own (GL) convention", gl_as_gl < gl_as_dx)
	failures += _check("NormalDX is lower under its own (DX) convention", dx_as_dx < dx_as_gl)
	print("== ALL PASS: 0 failure(s) ==" if failures == 0 else "== FAILED: %d failure(s) ==" % failures)
	quit(1 if failures > 0 else 0)

# ============================================================
# Feature functions: the curl check given in the assignment (bodies copied, unchanged)
# ============================================================
## Computes the curl ratio of a normal map. With directx = true the green channel is read flipped (DirectX convention).
## Called by _init() for calibration; test_materials.gd also preloads this file and calls it.
# ~0: slope field of a real surface in this convention.
# ~1: no surface behind it.
# ~2: real surface, other green convention.
static func curl_ratio(source: Image, directx := false, stride := 4) -> float:
	var img := source.duplicate() as Image
	if img.is_compressed():
		img.decompress()
	var s: float = -1.0 if directx else 1.0
	var curl_sq := 0.0
	var terms_sq := 0.0
	for v in range(1, img.get_height() - 1, stride):
		for u in range(1, img.get_width() - 1, stride):
			var t1 := (_dh_du(img, u, v + 1) - _dh_du(img, u, v - 1)) * 0.5
			var t2 := (_dh_dv(img, u + 1, v, s) - _dh_dv(img, u - 1, v, s)) * 0.5
			curl_sq += (t1 - t2) * (t1 - t2)
			terms_sq += t1 * t1 + t2 * t2
	return curl_sq / maxf(terms_sq, 1e-12)


## Reads one pixel and turns the 0–1 colour back into a -1–1 normal vector. Called by _dh_du() / _dh_dv().
static func _normal(img: Image, u: int, v: int) -> Vector3:
	var c := img.get_pixel(u, v)
	return Vector3(c.r, c.g, c.b) * 2.0 - Vector3.ONE


## Computes the height's slope along u from the normal. Called by curl_ratio().
static func _dh_du(img: Image, u: int, v: int) -> float:
	var n := _normal(img, u, v)
	return -n.x / maxf(n.z, 0.05)


## Computes the height's slope along v from the normal; with s = -1 the green is flipped for the DirectX convention. Called by curl_ratio().
static func _dh_dv(img: Image, u: int, v: int, s: float) -> float:
	var n := _normal(img, u, v)
	return s * n.y / maxf(n.z, 0.05)


## Prints one PASS / FAIL line and returns 1 on failure. Called by _init().
static func _check(label: String, ok: bool) -> int:
	print(("  PASS  " if ok else "  FAIL  ") + label)
	return 0 if ok else 1
