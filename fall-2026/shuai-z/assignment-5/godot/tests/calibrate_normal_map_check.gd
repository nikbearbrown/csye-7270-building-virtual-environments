extends SceneTree
## Calibrates normal_map_check.gd before anything trusts it (the assignment's
## Build It, Step 3) on a known pair: Poly Haven's Rock 01 normal map in both
## green conventions. The OpenGL file should come out low with directx = false
## and near 2 with directx = true, and the DirectX file the other way round.
## Each, read in its own convention, must come out under THRESHOLD.
## Prints the four ratios and one PASS or FAIL line per expectation, and exits 1
## if any fails. Run from assignment-5/:
##   scripts/run-test.sh godot calibrate_normal_map_check.gd 60

const NormalMapCheck := preload("res://tests/normal_map_check.gd")
const GL := "res://assets/textures/rock_01/rock_01_nor_gl_1k.png"
const DX := "res://assets/textures/rock_01/rock_01_nor_dx_1k.png"
# Chosen by the human on 2026-10-28, from this pair: Rock 01 read in its own
# convention gives 0.1444, and the assignment puts a map with no surface behind
# it near 1.
const THRESHOLD := 0.5

var _failures := 0


func _init() -> void:
	var ratio := {}
	for path: String in [GL, DX]:
		# The source file, decoded as it is on disk, not the compressed import.
		var image := Image.load_from_file(ProjectSettings.globalize_path(path))
		if image == null:
			_check("%s decodes" % path.get_file(), false)
			continue
		for directx: bool in [false, true]:
			ratio[[path, directx]] = NormalMapCheck.curl_ratio(image, directx)
			print("RATIO %s, directx = %s: %.4f" % [path.get_file(), directx, ratio[[path, directx]]])
	if ratio.size() == 4:
		_check("the OpenGL map is lower with directx = false than with true",
			ratio[[GL, false]] < ratio[[GL, true]])
		_check("the DirectX map is lower with directx = true than with false",
			ratio[[DX, true]] < ratio[[DX, false]])
		_check("the OpenGL map with directx = false is under the threshold, %.1f" % THRESHOLD,
			ratio[[GL, false]] < THRESHOLD)
		_check("the DirectX map with directx = true is under the threshold, %.1f" % THRESHOLD,
			ratio[[DX, true]] < THRESHOLD)
	print("all checks passed" if _failures == 0 else "%d check(s) FAILED" % _failures)
	quit(1 if _failures > 0 else 0)


func _check(what: String, ok: bool) -> void:
	print("%s  %s" % ["PASS" if ok else "FAIL", what])
	if not ok:
		_failures += 1
