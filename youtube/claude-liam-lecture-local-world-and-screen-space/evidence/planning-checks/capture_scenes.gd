extends RefCounted
# capture_scenes.gd: the reference scene scripts of this film's Godot captures C01 to C11b (CAPTURE-PLAN.md).
#
# Contract (one object per capture, made by CaptureScenes.make("C01")):
#   build(parent: Node, audio_length: float)   create the nodes under `parent` (a node already in the tree: the logical canvas, or the SubViewport
#                                              of the scene's route()); `audio_length` is the measured audio of the beat in
#                                              seconds, every motion window below is a fraction of it
#   at(t: float)                               put every node in its state at clip time t seconds. A pure function of t (no tweens, no
#                                              timers): the harness calls at(frame / fps) before each frame it records, so a frame is
#                                              reproducible. For t beyond audio_length the final state holds.
#   route() -> Dictionary                     {"canvas": Vector2i, "render": Vector2i}: the logical canvas the scene is laid out on and the size it is
#                                              rendered at. Default: a 1280 x 720 canvas rendered at 3840 x 2160 (the SubViewport native-size route: size
#                                              3840x2160, size_2d_override 1280x720, stretch on), right for shaders that work in the node's own or the
#                                              world's numbers. A scene whose shaders read WINDOW PIXELS (FRAGCOORD, SCREEN_PIXEL_SIZE, VERTEX in
#                                              fragment()) returns canvas == render == 1920 x 1080: captured at the size shown, at scale 1 (series rule,
#                                              GLOSSARY.md "Series conventions"; C10 only).
# The stage colour (#D9D5CA) is set by the harness, as in lab/runner.gd. Shaders are read from this film's lab-shaders/ folder
# (override the folder with the environment variable LOCAL_WORLD_SHADERS). No Godot Label nodes: words are ShaderLab readouts.

const Scn := preload("res://scenes_lib.gd")


static func make(id: String) -> RefCounted:
	match id:
		"C01": return C01.new()
		"C02": return C02.new()
		"C03": return C03.new()
		"C04": return C04.new()
		"C05": return C05.new()
		"C06": return C06.new()
		"C07": return C07.new()
		"C08": return C08.new()
		"C09": return C09.new()
		"C10": return C10.new()
		"C11a": return C11a.new()
		"C11b": return C11b.new()
	return null


# estimated audio seconds per capture (SCRIPT.md), used when no measured audio exists yet
const EST := {"C01": 12.9, "C02": 12.6, "C03": 12.9, "C04": 10.2, "C05": 11.6, "C06": 11.9, "C07": 12.6, "C08": 11.6, "C09": 11.9, "C10": 11.6, "C11a": 10.5, "C11b": 12.6}


class Base extends RefCounted:
	var T := 10.0
	var parent: Node

	func build(p: Node, audio_length: float) -> void:
		parent = p
		T = audio_length

	func at(_t: float) -> void:
		pass

	func route() -> Dictionary:
		return {"canvas": Vector2i(1280, 720), "render": Vector2i(3840, 2160), "reads_window_pixels": false}

	# smooth 0..1 over fractions a..b of the beat (ease in and out)
	func ramp(t: float, a: float, b: float) -> float:
		var x := clampf((t / T - a) / (b - a), 0.0, 1.0)
		return x * x * (3.0 - 2.0 * x)

	func faint_sky(alpha: float) -> ColorRect:
		return Scn.sky_rect(Rect2(0, 0, 1280, 720), alpha)


# C01 (B01): two blob sprites on a faint sky; the left reads the sky by local position, the right by world position; both slide right
class C01 extends Base:
	var left: Sprite2D
	var right: Sprite2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var sky: Texture2D = Scn.sky_texture(1536)
		p.add_child(faint_sky(0.35))
		var blob: Texture2D = Scn.blob_texture(256, true)
		left = Scn.sprite(blob, Vector2(220, 240), 1.0, Scn.material("01-sky-local.gdshader", {"sky": sky}))
		right = Scn.sprite(blob, Vector2(700, 240), 1.0, Scn.material("02-sky-world.gdshader", {"sky": sky}))
		p.add_child(left)
		p.add_child(right)

	func at(t: float) -> void:
		var s := ramp(t, 0.10, 0.56)
		left.position.x = 220.0 + 300.0 * s
		right.position.x = 700.0 + 300.0 * s


# C02 (B07): a camera pans right by 100 over a star sky; a 128 px sprite in a cream box with a terracotta dot on its top-left corner
class C02 extends Base:
	var cam: Camera2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var back := Scn.sky_rect(Rect2(0, 0, 2000, 1000), 0.5)
		p.add_child(back)
		var sp := Scn.sprite(Scn.blob_texture(128, true), Vector2(600, 400), 1.0)
		p.add_child(sp)
		var box := Node2D.new()
		sp.add_child(box)
		box.draw.connect(func():
			box.draw_rect(Rect2(-64, -64, 128, 128), Color("#EDE8DA"), false, 2.0)
			box.draw_circle(Vector2(-64, -64), 6.0, Color("#D97757")))
		box.queue_redraw()
		cam = Camera2D.new()
		cam.position = Vector2(890, 460)
		p.add_child(cam)
		cam.make_current()

	func at(t: float) -> void:
		cam.position = Vector2(890.0 + 100.0 * ramp(t, 0.12, 0.40), 460.0)


# C03 (B16): world position as colour; a faint copy of the field behind a blob that slides right over it
class C03 extends Base:
	var sprite: Sprite2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var back := ColorRect.new()
		back.size = Vector2(1280, 720)
		back.modulate = Color(1, 1, 1, 0.35)
		back.material = Scn.material("05-world-field.gdshader")
		p.add_child(back)
		sprite = Scn.sprite(Scn.blob_texture(256, true), Vector2(300, 360), 1.0, Scn.material("05-world-field.gdshader"))
		p.add_child(sprite)

	func at(t: float) -> void:
		sprite.position.x = 300.0 + 680.0 * ramp(t, 0.52, 0.80)


# C04 (B20): the whole view reads the sky by world position; at 64 % the repeat hint is switched off
class C04 extends Base:
	var rect: ColorRect
	var m_on: ShaderMaterial
	var m_off: ShaderMaterial

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var sky: Texture2D = Scn.sky_texture(1536)
		m_on = Scn.material("02-sky-world.gdshader", {"sky": sky})
		m_off = Scn.material("06-sky-no-repeat.gdshader", {"sky": sky})
		rect = ColorRect.new()
		rect.size = Vector2(1280, 720)
		rect.material = m_on
		p.add_child(rect)

	func at(t: float) -> void:
		var want := m_on if t / T < 0.64 else m_off
		if rect.material != want:
			rect.material = want


# C05 (B21): one blob slides over the sky and comes to rest over the ringed planet
class C05 extends Base:
	var sprite: Sprite2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var sky: Texture2D = Scn.sky_texture(1536)
		p.add_child(faint_sky(0.35))
		sprite = Scn.sprite(Scn.blob_texture(256, true), Vector2(640, 240), 1.0, Scn.material("02-sky-world.gdshader", {"sky": sky}))
		p.add_child(sprite)

	func at(t: float) -> void:
		sprite.position.x = 640.0 + 240.0 * ramp(t, 0.10, 0.50)


# C06 (B22): a white square over the planet turns 45 degrees, then stretches wide and low; the sky inside does not move
class C06 extends Base:
	var sprite: Sprite2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var sky: Texture2D = Scn.sky_texture(1536)
		p.add_child(faint_sky(0.35))
		sprite = Scn.sprite(Scn.white_texture(128), Vector2(852, 240), 2.0, Scn.material("02-sky-world.gdshader", {"sky": sky}))
		p.add_child(sprite)

	func at(t: float) -> void:
		sprite.rotation = deg_to_rad(45.0) * ramp(t, 0.06, 0.22)
		var q := ramp(t, 0.24, 0.38)
		sprite.scale = Vector2(2.0 + 0.5 * q, 2.0 - 0.4 * q)


# C07 (B23): a checker read by world position times texture pixel size; the art is swapped from 128 px to 64 px at 78 %
class C07 extends Base:
	var sprite: Sprite2D
	var art128: Texture2D
	var art64: Texture2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		art128 = Scn.blob_texture(128, true)
		art64 = Scn.blob_texture(64, true)
		sprite = Scn.sprite(art128, Vector2(640, 360), 2.0, Scn.material("07-pattern-texel-size.gdshader", {"pattern": Scn.checker_texture(256)}))
		p.add_child(sprite)

	func at(t: float) -> void:
		if t / T >= 0.78:
			if sprite.texture != art64:
				sprite.texture = art64
				sprite.scale = Vector2(4, 4)
		elif sprite.texture != art128:
			sprite.texture = art128
			sprite.scale = Vector2(2, 2)


# C08 (B24): a hole of radius 60 fixed at (640,360), marked by a thin grey ring; a blob slides across it
class C08 extends Base:
	var sprite: Sprite2D

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		sprite = Scn.sprite(Scn.blob_texture(256, true), Vector2(440, 360), 1.0, Scn.material("08-world-hole.gdshader"))
		p.add_child(sprite)
		var ring := Node2D.new()
		p.add_child(ring)
		ring.draw.connect(func(): ring.draw_arc(Vector2(640, 360), 60.0, 0.0, TAU, 96, Color("#8F8A7B"), 3.0, true))
		ring.queue_redraw()

	func at(t: float) -> void:
		sprite.position.x = 440.0 + 400.0 * ramp(t, 0.40, 0.92)


# C09 (B25): the sprite walks right over the sky while `amount` climbs from 0 to 1
class C09 extends Base:
	var sprite: Sprite2D
	var mat: ShaderMaterial

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var sky: Texture2D = Scn.sky_texture(1536)
		p.add_child(faint_sky(0.35))
		mat = Scn.material("09-spacing-out.gdshader", {"sky": sky})
		mat.set_shader_parameter("amount", 0.0)    # the start value is set from code first
		sprite = Scn.sprite(Scn.blob_texture(256, true), Vector2(560, 240), 1.0, mat)
		p.add_child(sprite)

	func at(t: float) -> void:
		sprite.position.x = 560.0 + 440.0 * ramp(t, 0.50, 0.95)
		mat.set_shader_parameter("amount", ramp(t, 0.52, 0.78))


# C10 (B33): four 960 x 540 tiles on a 1920 x 1080 canvas, one screen-address method each, switched on in turn; thin grey tile outlines on top.
# Shaders 10, 12 and 13 read window pixels (a canvas-matrix position, VERTEX in fragment(), FRAGCOORD) and multiply them by SCREEN_PIXEL_SIZE, so this
# capture uses the 1920 x 1080 route at scale 1 (route() below), not the 3x SubViewport route.
class C10 extends Base:
	var tiles: Array = []
	var mats: Array = []
	const AT := [0.20, 0.32, 0.42, 0.58]
	const FILES := ["10-screen-via-matrices.gdshader", "12-screen-vertex-in-fragment.gdshader", "13-screen-fragcoord.gdshader", "14-screen-uv.gdshader"]

	func route() -> Dictionary:
		return {"canvas": Vector2i(1920, 1080), "render": Vector2i(1920, 1080), "reads_window_pixels": true}

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var rects := [Rect2(0, 0, 960, 540), Rect2(960, 0, 960, 540), Rect2(0, 540, 960, 540), Rect2(960, 540, 960, 540)]
		for i in 4:
			var cr := ColorRect.new()
			cr.position = rects[i].position
			cr.size = rects[i].size
			cr.color = Color("#BDB8AA")
			p.add_child(cr)
			tiles.append(cr)
			mats.append(Scn.material(FILES[i]))
		var outline := Node2D.new()
		p.add_child(outline)
		outline.draw.connect(func():
			for r in rects:
				outline.draw_rect(Rect2(r.position + Vector2(1.5, 1.5), r.size - Vector2(3, 3)), Color("#A9A495"), false, 3.0))
		outline.queue_redraw()

	func at(t: float) -> void:
		for i in 4:
			var want: Material = mats[i] if t / T >= AT[i] else null
			if tiles[i].material != want:
				tiles[i].material = want


# C11a and C11b (B36, B37): three blob sprites with local / world / screen stripes at x = 256, 640, 1024 (multiples of 64, so the three
# patterns coincide at the start). C11a slides the sprites right by 160; C11b pans the camera right by 160.
class Anchors extends Base:
	var sprites: Array = []
	var cam: Camera2D
	const FILES := ["15-anchor-local.gdshader", "16-anchor-world.gdshader", "17-anchor-screen.gdshader"]

	func build(p: Node, audio_length: float) -> void:
		super.build(p, audio_length)
		var blob: Texture2D = Scn.blob_texture(256, true)
		for i in 3:
			var s := Scn.sprite(blob, Vector2(256 + 384 * i, 360), 1.0, Scn.material(FILES[i]))
			p.add_child(s)
			sprites.append(s)
		cam = Camera2D.new()
		cam.position = Vector2(640, 360)
		p.add_child(cam)
		cam.make_current()


class C11a extends Anchors:
	func at(t: float) -> void:
		var s := ramp(t, 0.24, 0.60)
		for i in 3:
			sprites[i].position.x = 256.0 + 384.0 * i + 160.0 * s


class C11b extends Anchors:
	func at(t: float) -> void:
		cam.position.x = 640.0 + 160.0 * ramp(t, 0.22, 0.60)
