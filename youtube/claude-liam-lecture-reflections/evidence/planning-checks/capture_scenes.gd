extends RefCounted
# capture_scenes.gd: every custom Godot scene the Reflections film records, as data plus a small timeline.
# Written at the layout stage and CHECKED by scene_runner.gd (frames dumped and probed); the build session's capture harness
# (lab/capture.gd, not built yet) should load this file unchanged.
#
# Contract (all times are scripted seconds, 30 fps, offline fixed tick):
#   var cs = preload("res://capture_scenes.gd").new()
#   var info = cs.setup("C08", shaders_dir, art_scale)   # {"duration": s, "label": text, "family": "pond" | "three"}
#   cs.build(parent)                                      # adds the nodes under `parent` (a SubViewport for the 4K route)
#   for i in range(int(info.duration * 30)): cs.tick(i / 30.0); draw and save frame i
# Logical canvas 1280 x 720. art_scale = texture pixels per logical pixel: 3 for a 3840 x 2160 capture (SubViewport with
# size_2d_override = 1280 x 720 and stretch on), 1 for the planning checks.
# EVERY capture must run in a FRESH Godot process: a rect-mode BackBufferCopy (C08) reads whatever history left in the back buffer.

const P = preload("res://pond_common.gd")

var id := ""
var shaders := ""
var S := 1
var duration := 10.0
var label := ""
var family := "pond"
var N := {}                       # named nodes
var done := {}                    # one-shot events already fired
var art := {}
var char_tex: ImageTexture
var win := {}                     # window geometry (three-sprite family)

const STAGE := Color("#D9D5CA")
const COL_A := Color("#4F8F7E")
const COL_B := Color("#7FA7C9")
const COL_C := Color("#B7A6D9")
const TEAL := Color("#5FA391")

# id -> [duration seconds, label]. Durations are the estimated beat length plus margin; the harness may trim or hold the last frame.
const TABLE := {
	"C01": [13.5, "walk, opaque reflection, hidden label map"],
	"C02": [13.0, "the label map alone, fading in"],
	"C03": [10.5, "label map drawn over the art"],
	"C04": [14.5, "three sprites, then the window appears"],
	"C05": [14.0, "copy after C, then between B and C"],
	"C06": [10.5, "copy between A and B, then before A"],
	"C07": [15.0, "two readers, then a copy between"],
	"C08": [14.5, "window in rect mode (black outside the box), then viewport"],
	"C09": [11.0, "flipped copy placed under the feet"],
	"C10": [11.5, "the copy hangs in the sand"],
	"C11": [12.5, "reflection shader, the walk"],
	"C12": [13.0, "label map switched off and on"],
	"C13": [13.5, "wrong orders: copy after art, label map over art"],
	"C14": [13.0, "art at 90 percent opacity"],
	"C15": [12.0, "equals on a half-strength label map"],
	"C16": [10.5, "distance on a half-strength label map"],
	"C17": [13.0, "coast and water alpha"],
	"C18": [10.5, "tint toggled"],
	"C19": [10.5, "jump"],
}

func setup(capture_id: String, shaders_dir: String, art_scale: int) -> Dictionary:
	id = capture_id
	shaders = shaders_dir
	S = art_scale
	duration = TABLE[id][0]
	label = TABLE[id][1]
	family = "three" if id in ["C04", "C05", "C06", "C07", "C08"] else "pond"
	return {"duration": duration, "label": label, "family": family}

func tex_from(img: Image) -> ImageTexture:
	return ImageTexture.create_from_image(img)

func sprite_of(img_tex: Texture2D, name: String) -> Sprite2D:
	var s := Sprite2D.new()
	s.name = name
	s.texture = img_tex
	s.centered = false
	s.scale = Vector2(1.0 / S, 1.0 / S)
	return s

# ---------------------------------------------------------------------------------------------------------------- pond family
func shader_for() -> String:
	match id:
		"C15":
			return "04-compare-equal.gdshader"
		"C16":
			return "05-compare-distance.gdshader"
		"C17", "C18", "C19":
			return "03-reflection-final.gdshader"
		_:
			return "02-reflection.gdshader"

func build_pond(parent: Node) -> void:
	var half_red := id in ["C15", "C16"]
	var layers := P.make_layers(S, Color(128.0 / 255.0, 0.0, 0.0, 1.0) if half_red else P.MASK_WATER, P.MASK_COAST)
	var ch := P.make_character_image(P.SPRITE_N * S)
	char_tex = tex_from(ch)
	var scene := Node2D.new()
	scene.name = "Pond"
	parent.add_child(scene)
	N["scene"] = scene
	var mask := sprite_of(tex_from(layers["mask"]), "LabelMap")
	var ground := sprite_of(tex_from(layers["ground"]), "Ground")
	var bbc := BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	var player := sprite_of(char_tex, "Player")
	player.centered = true
	player.position = Vector2(300, P.PLAYER_Y)
	var rt := RemoteTransform2D.new()
	rt.name = "RemoteTransform2D"
	rt.position = Vector2(0, P.REFLECT_OFFSET * S)           # the player's own scale is 1/S, so the offset is in texture pixels
	player.add_child(rt)
	var refl := sprite_of(char_tex, "Reflection")
	refl.centered = true
	refl.flip_v = true
	var plain := id in ["C09", "C10"]
	if not plain:
		refl.material = P.load_shader(shader_for(), shaders)
		if id in ["C17"]:
			refl.material.set_shader_parameter("tint", TEAL)         # neutral tint: this beat is about the coast alpha only
		if id in ["C18"]:
			refl.material.set_shader_parameter("tint", TEAL)
	var order := ["mask", "bbc", "ground", "player", "refl"]
	if id == "C03":
		order = ["ground", "mask", "bbc", "player", "refl"]
	for k in order:
		scene.add_child({"mask": mask, "bbc": bbc, "ground": ground, "player": player, "refl": refl}[k])
	rt.remote_path = rt.get_path_to(refl)
	N.merge({"mask": mask, "ground": ground, "bbc": bbc, "player": player, "refl": refl, "rt": rt}, true)
	# per-capture starting state
	match id:
		"C02":
			ground.visible = false
			player.visible = false
			refl.visible = false
			mask.modulate.a = 0.0
		"C09":
			refl.modulate.a = 0.0
			player.position.x = 520.0

func x_at(t: float, x0: float, x1: float, t0: float, t1: float) -> float:
	return lerpf(x0, x1, clampf((t - t0) / (t1 - t0), 0.0, 1.0))

func once(key: String, t: float, at: float, f: Callable) -> void:
	if t >= at and not done.has(key):
		done[key] = true
		f.call()

func tick_pond(t: float) -> void:
	var player: Sprite2D = N["player"]
	match id:
		"C01":
			player.position.x = x_at(t, 150, 1200, 0.0, 11.5)
		"C02":
			N["mask"].modulate.a = clampf(t / 2.5, 0.0, 1.0)
		"C03":
			player.position.x = x_at(t, 300, 620, 0.0, 10.0)
		"C09":
			N["refl"].modulate.a = clampf((t - 2.0) / 1.0, 0.0, 1.0)
		"C10":
			player.position.x = x_at(t, 300, 1000, 0.0, 10.5)
		"C11":
			player.position.x = x_at(t, 300, 1000, 0.0, 11.5)
		"C12":
			player.position.x = x_at(t, 180, 620, 0.0, 12.5)
			N["mask"].visible = not (t >= 4.5 and t < 9.5)
		"C13":
			player.position.x = x_at(t, 300, 560, 0.0, 13.0)
			once("copy_after_art", t, 4.0, func(): N["scene"].move_child(N["bbc"], N["ground"].get_index()))
			once("mask_over_art", t, 9.5, func(): N["scene"].move_child(N["mask"], N["ground"].get_index()))
		"C14":
			player.position.x = x_at(t, 300, 560, 0.0, 12.5)
			var a := 1.0
			if t >= 3.0 and t < 9.5:
				a = lerpf(1.0, 0.9, clampf((t - 3.0) / 1.0, 0.0, 1.0))
			N["ground"].modulate.a = a
		"C15", "C16":
			player.position.x = x_at(t, 250, 700, 0.0, 10.5)
		"C17":
			player.position.x = 420.0 if t < 7.0 else x_at(t, 420, 900, 7.0, 12.5)
		"C18":
			player.position.x = 420.0
			var blue := (t >= 1.8 and t < 3.2) or t >= 4.6
			N["refl"].material.set_shader_parameter("tint", Color(0.2, 0.5, 1.0, 1.0) if blue else TEAL)
		"C19":
			player.position.x = 300.0
			var up := 0.0
			for w in [[3.0, 4.0], [6.5, 7.5]]:
				if t >= w[0] and t < w[1]:
					up = 80.0 * sin(PI * (t - w[0]) / (w[1] - w[0]))
			player.position.y = P.PLAYER_Y - up

# ---------------------------------------------------------------------------------------------------------------- three-sprite family
func flat_sprite(name: String, c: Color, pos: Vector2, size: float) -> Sprite2D:
	var img := Image.create(1, 1, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	var s := Sprite2D.new()
	s.name = name
	s.texture = tex_from(img)
	s.centered = false
	s.position = pos
	s.scale = Vector2(size, size)
	s.modulate = c
	return s

func make_window(prefix: String, top_left: Vector2) -> Dictionary:
	# preview (shows the WHOLE screen texture, 480 x 270) then a border drawn AFTER it, so the border is never in a copy
	var pv := ColorRect.new()
	pv.name = prefix + "Preview"
	pv.position = top_left + Vector2(12, 12)
	pv.size = Vector2(480, 270)
	pv.material = P.load_shader("01-screen-preview.gdshader", shaders)
	var border := Panel.new()
	border.name = prefix + "Border"
	border.position = top_left
	border.size = Vector2(504, 294)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0, 0, 0, 0)
	sb.set_border_width_all(8)
	sb.border_color = Color("#FAF9F5")
	border.add_theme_stylebox_override("panel", sb)
	return {"preview": pv, "border": border}

func build_three(parent: Node) -> void:
	var scene := Node2D.new()
	scene.name = "Scene"
	parent.add_child(scene)
	N["scene"] = scene
	var a := flat_sprite("A", COL_A, Vector2(110, 300), 210)
	var b := flat_sprite("B", COL_B, Vector2(230, 380), 210)
	var c := flat_sprite("C", COL_C, Vector2(350, 460), 210)
	var bbc := BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	N.merge({"A": a, "B": b, "C": c, "bbc": bbc}, true)
	var w1 := make_window("", Vector2(728, 44))
	N["w1"] = w1
	match id:
		"C04":
			for n in [a, b, c, w1["preview"], w1["border"]]:
				scene.add_child(n)
			w1["preview"].visible = false
			w1["border"].visible = false
		"C05":
			for n in [a, b, c, w1["preview"], w1["border"]]:
				scene.add_child(n)
		"C06":
			for n in [a, b, bbc, c, w1["preview"], w1["border"]]:
				scene.add_child(n)
		"C08":
			bbc.copy_mode = BackBufferCopy.COPY_MODE_RECT
			bbc.position = Vector2(100, 100)          # default rect (-100,-100,200,200): the box does not follow the node (exp H), it copies screen 0..100 x 0..100 only; none of A, B, C is in it
			for n in [a, b, c, bbc, w1["preview"], w1["border"]]:
				scene.add_child(n)
		"C07":
			var w2 := make_window("Second", Vector2(728, 372))
			N["w2"] = w2
			for n in [a, b, w1["preview"], w1["border"], c, w2["preview"], w2["border"]]:
				scene.add_child(n)

func tick_three(t: float) -> void:
	var scene: Node2D = N["scene"]
	match id:
		"C04":
			once("window", t, 3.5, func():
				N["w1"]["preview"].visible = true
				N["w1"]["border"].visible = true)
		"C05":
			once("add_copy_after_C", t, 2.5, func():
				scene.add_child(N["bbc"])
				scene.move_child(N["bbc"], N["C"].get_index() + 1))            # after C, before the window
			once("between_B_and_C", t, 5.5, func(): scene.move_child(N["bbc"], N["C"].get_index()))
		"C06":
			once("between_A_and_B", t, 1.0, func(): scene.move_child(N["bbc"], N["B"].get_index()))
			once("before_A", t, 3.6, func(): scene.move_child(N["bbc"], 0))
		"C08":
			once("mode_becomes_viewport", t, 9.0, func(): N["bbc"].copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT)
		"C07":
			once("copy_between_C_and_second_window", t, 10.5, func():
				scene.add_child(N["bbc"])
				scene.move_child(N["bbc"], N["w2"]["preview"].get_index()))

# ---------------------------------------------------------------------------------------------------------------- entry points
func build(parent: Node) -> void:
	if family == "three":
		build_three(parent)
	else:
		build_pond(parent)

func tick(t: float) -> void:
	if family == "three":
		tick_three(t)
	else:
		tick_pond(t)
