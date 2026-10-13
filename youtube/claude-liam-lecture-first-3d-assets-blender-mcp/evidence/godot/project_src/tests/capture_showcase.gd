# capture_showcase.gd - ONE brief windowed run: loads showcase.tscn into a 2400x1350 SubViewport, lets it settle, saves PNGs, quits.
# Three candidate looks (same scene; only the sun strength / lens differ) are saved in the same run so the best can be chosen by eye.
#   godot --path <project> --script res://tests/capture_showcase.gd --resolution 640x360 --fixed-fps 60 -- <out_dir>
extends SceneTree

var frames := 0
var vp: SubViewport
var scene: Node
var out_dir := "."
# [name, sun energy, camera fov]
var looks := [["A", 1.2, 40.0], ["B", 1.7, 40.0], ["C", 1.4, 32.0]]      # C was chosen by eye and baked into showcase.tscn (sun 1.4, fov 32)
const SETTLE := 30


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	if a.size() > 0:
		out_dir = a[0]
	vp = SubViewport.new()
	vp.size = Vector2i(2400, 1350)
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = (load("res://showcase.tscn") as PackedScene).instantiate()
	vp.add_child(scene)


func _process(_delta: float) -> bool:
	frames += 1
	var i := (frames - 1) / SETTLE
	var phase := (frames - 1) % SETTLE
	if i >= looks.size():
		return true
	var look: Array = looks[i]
	if phase == 0:
		(scene.get_node("Sun") as DirectionalLight3D).light_energy = look[1]
		(scene.get_node("Camera") as Camera3D).fov = look[2]
	if phase == SETTLE - 1:
		var img := vp.get_texture().get_image()
		var path := "%s/godot_showcase_%s.png" % [out_dir, look[0]]
		img.save_png(path)
		print("look ", look[0], ": sun ", look[1], " fov ", look[2], " -> ", path, " ", img.get_size())
	return false
