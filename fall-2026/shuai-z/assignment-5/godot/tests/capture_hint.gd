extends SceneTree
## Windowed capture of the hint experiment for TEST-REPORT.md (CHANGE-BRIEF.md
## section 4): renders res://scenes/hint_experiment.tscn, saves the frame as the
## engine drew it, and prints the value at the centre of each of the six bands
## beside the brief's prediction. Not headless: the headless renderer draws
## nothing. Run from assignment-5/:
##   godot --path godot --resolution 1920x1080 --always-on-top --script res://tests/capture_hint.gd
## The PNG goes to evidence/use-it/.

const SCENE := "res://scenes/hint_experiment.tscn"
## quad, then the displayed value predicted for each band (section 4); the file holds 64, 128 and 192
const QUADS := [
	["QuadA", [64, 128, 192]],
	["QuadB", [137, 188, 225]],
]
const FILE_VALUES := [64, 128, 192]
const BAND_WIDTH := 0.5 ## m, a third of the 1.5 m quad
const NEAR := 4 ## px around each centre, to show the band is flat there
const STEPS := 2 ## "more than a step or two per channel is a finding"


func _initialize() -> void:
	if DisplayServer.get_name() == "headless":
		printerr("STOP this needs a window: a headless run draws no frame to read")
		quit(1)
		return
	var out_dir := ProjectSettings.globalize_path("res://").path_join("../evidence/use-it").simplify_path()
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene := (load(SCENE) as PackedScene).instantiate() as Node3D
	root.add_child(scene)
	for i in 10:
		await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	if image == null:
		printerr("STOP no frame to read: run this in a window, not with --headless")
		quit(1)
		return
	var path := out_dir.path_join("hint-experiment.png")
	image.save_png(path)
	print("SAVED %s, %d x %d as drawn" % [path.get_file(), image.get_width(), image.get_height()])

	var camera := scene.get_node("Camera") as Camera3D
	for q: Array in QUADS:
		var quad := scene.get_node(q[0] as String) as Node3D
		for band in 3:
			var centre := quad.global_position + Vector3((band - 1) * BAND_WIDTH, 0.0, 0.0)
			var at := Vector2i(camera.unproject_position(centre).round())
			var c := image.get_pixelv(at)
			var want: int = q[1][band]
			var off := maxi(maxi(absi(c.r8 - want), absi(c.g8 - want)), absi(c.b8 - want))
			var lo := 255
			var hi := 0
			for dy in range(-NEAR, NEAR + 1):
				for dx in range(-NEAR, NEAR + 1):
					var n := image.get_pixelv(at + Vector2i(dx, dy))
					lo = mini(lo, mini(mini(n.r8, n.g8), n.b8))
					hi = maxi(hi, maxi(maxi(n.r8, n.g8), n.b8))
			print("BAND %s %d (file %d) at %s: shows %d, %d, %d; predicted %d, off by %d (%s); %d x %d around it spans %d to %d" % [
				q[0], band + 1, FILE_VALUES[band], at, c.r8, c.g8, c.b8, want, off,
				"within %d" % STEPS if off <= STEPS else "a finding", 2 * NEAR + 1, 2 * NEAR + 1, lo, hi])
	quit(0)
