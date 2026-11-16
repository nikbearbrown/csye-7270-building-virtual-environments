extends SceneTree
## Calibrates tests/normal_map_check.gd on the two Rock 01 normal maps, read from their source PNGs.
## Prints curl_ratio for each file under directx = false and directx = true, stride 4. Prints only, asserts nothing.
##   ./scripts/run-test.sh calibrate_normal_check.gd 60   (from fall-2026/zhefan-z/assignment-5/)
## Image.load_from_file prints an engine WARNING ("will not work on export"); it is expected here.

const NormalMapCheck := preload("res://tests/normal_map_check.gd")
const FILES := ["res://assets/textures/rock_01/rock_01_nor_gl_1k.png", "res://assets/textures/rock_01/rock_01_nor_dx_1k.png"]


func _initialize() -> void:
	for path: String in FILES:
		var img := Image.load_from_file(path)
		for directx: bool in [false, true]:
			var ratio := NormalMapCheck.curl_ratio(img, directx, 4)
			print(JSON.stringify({"file": path.get_file(), "size": [img.get_width(), img.get_height()],
				"format": img.get_format(), "directx": directx, "stride": 4, "curl_ratio": snappedf(ratio, 0.0001)}))
	quit(0)
