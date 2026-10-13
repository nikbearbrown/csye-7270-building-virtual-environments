extends SceneTree
# Check 13: the call of beat B25 runs exactly as shown, and the picture answers on the next frame.
#   $Flag.material.set_shader_parameter("amplitude", 40.0)
# A MeshInstance2D named Flag (QuadMesh 384 x 168 cut 31 x 7) with lab-shaders/07-flag-dials.gdshader. To take TIME out of the measurement the speed dial is
# first set to 0 (also by set_shader_parameter), so the ripple is frozen at sin(8u) and the top edge at a given column is predictable:
#   top_edge_y(x) = 276 + sin(8 u) * amplitude * u,  u = (x - 448 + 0.5) / 384
# Columns 830, 790 and 760 are read before and after the call; each is compared with the formula.
# (Side note, kept: an earlier version read a frame every frame for four seconds and TIME stopped advancing after about a second; this one reads few frames.)
const V = preload("res://vscene.gd")
const CS = preload("res://capture_scenes.gd")
const SRC := "extends Node2D\nfunc call_it():\n\t$Flag.material.set_shader_parameter(\"amplitude\", 40.0)\n"

func _initialize() -> void:
	call_deferred("run")

func top_at(im: Image, x: int) -> int:
	for y in range(0, 720):
		var c := im.get_pixel(x, y)
		if absf(c.r - V.STAGE.r) > 0.05 or absf(c.g - V.STAGE.g) > 0.05:
			return y
	return -1

func expected(x: int, amp: float) -> float:
	var u := (x - 448 + 0.5) / 384.0
	return 276.0 + sin(8.0 * u) * amp * u

func run() -> void:
	V.setup(root, 1280, 720)
	var holder := Node2D.new()
	var s := GDScript.new()
	s.source_code = SRC
	var err := s.reload()
	holder.set_script(s)
	var flag := V.quad(Vector2(CS.FLAG_W, CS.FLAG_H), 31, 7, CS.flag_image(CS.FLAG_W, CS.FLAG_H), Vector2(640, 360), V.material_from(V.lab_shader("07-flag-dials")))
	flag.name = "Flag"
	holder.add_child(flag)
	root.add_child(holder)
	await V.frames(self, 5)
	flag.material.set_shader_parameter("speed", 0.0)
	await V.frames(self, 3)
	var im0 := V.grab(root)
	var before := {}
	for x in [830, 790, 760]:
		before[str(x)] = {"measured": top_at(im0, x), "formula_amplitude_24": snappedf(expected(x, 24.0), 0.1)}
	var read_before = flag.material.get_shader_parameter("amplitude")
	holder.call_it()
	var read_after = flag.material.get_shader_parameter("amplitude")
	await V.frames(self, 3)
	var im1 := V.grab(root)
	var after := {}
	for x in [830, 790, 760]:
		after[str(x)] = {"measured": top_at(im1, x), "formula_amplitude_40": snappedf(expected(x, 40.0), 0.1)}
	V.out("13-b25-call-as-shown", {"script_reload_error": err, "amplitude_before_call": read_before, "amplitude_after_call": read_after, "before": before, "after": after})
	quit(0)
