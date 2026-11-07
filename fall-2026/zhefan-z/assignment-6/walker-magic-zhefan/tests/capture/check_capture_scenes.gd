extends SceneTree
## Headless parse check for the capture scenes only; a headless run uses a dummy renderer and cannot capture.
## Loads each scene, adds it to the tree for two frames (its _ready runs and prints the key bindings), frees it.
## From fall-2026/zhefan-z/assignment-5/:
##   Godot_v4.7.2-stable_win64_console.exe --headless --path walker-magic-zhefan --script res://tests/capture/check_capture_scenes.gd

const SCENES := ["res://tests/capture/capture_hurt_tint.tscn", "res://tests/capture/capture_hint.tscn",
	"res://tests/capture/capture_rock_sweep.tscn"]


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	var failed := 0
	for path: String in SCENES:
		var packed := load(path) as PackedScene
		var node: Node = packed.instantiate() if packed != null else null
		if node == null or node.get_script() == null:
			failed += 1
			print(JSON.stringify({"scene": path, "status": "FAIL", "why": "did not load or has no script"}))
			continue
		root.add_child(node)
		await process_frame
		await process_frame
		print(JSON.stringify({"scene": path, "status": "PASS", "script": node.get_script().resource_path,
			"children": node.get_children().map(func(c: Node) -> String: return c.name)}))
		node.free()
		await process_frame
	print("CAPTURE SCENES: %d loaded / %d failed" % [SCENES.size() - failed, failed])
	quit(1 if failed else 0)
