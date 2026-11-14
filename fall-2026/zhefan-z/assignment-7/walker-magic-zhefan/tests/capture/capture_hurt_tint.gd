extends "res://tests/capture/capture_common.gd"
## Hurt-tint captures (CHANGE-BRIEF section 2, "Controlled inputs and predicted values", and section 6, whether
## hint_range clamps a value set from code). Open tests/capture/capture_hurt_tint.tscn, F6, wait until the mage
## stands idle at the start, keep the mouse crosshair away from the mage, press F9.
## The HurtTint driver is disabled for the sequence and re-enabled afterwards; tint_color and intensity are put
## back to what the material held before (tint_color unset = the shader default).

const IDLE := preload("res://assets/sprites/mage/mage_idle.png")
## Texture pixels of mage_idle.png (62x69) sampled in every capture.
const TEXELS := {"hair": Vector2i(27, 18), "hat": Vector2i(24, 7)}
const GREY := Color(0.5, 0.5, 0.5, 1.0)
const CROSSHAIR_REACH := 8.0   # ui/crosshair.gd draws within 5 px of the mouse, plus a 3 px edge

@onready var player: Player = $Main/Player
@onready var sprite: Sprite2D = $Main/Player/Sprite2D
@onready var driver: Node = $Main/Player/HurtTint
@onready var crosshair: Node2D = $Main/UI/Crosshair
@onready var mat: ShaderMaterial = sprite.material


func bindings() -> Dictionary:
	return {"F9": "driver off; intensity 0.0, 0.5, 1.0 (tint_color default red), then tint_color grey "
		+ "Color(0.5, 0.5, 0.5, 1.0) at intensity 2.0; samples texels (27, 18) and (24, 7); restores; driver on"}


func on_key(keycode: Key) -> void:
	if keycode == KEY_F9:
		run_sequence()


## Viewport position of the centre of a texture pixel: canvas transform * (offset + pixel centre).
func viewport_position(texel: Vector2i) -> Vector2:
	var size := sprite.texture.get_size()
	var centre := Vector2(texel) + Vector2(0.5, 0.5)
	if sprite.flip_h:
		centre.x = size.x - centre.x
	if sprite.flip_v:
		centre.y = size.y - centre.y
	var local := sprite.offset + centre
	if sprite.centered:
		local -= size / 2.0
	return sprite.get_global_transform_with_canvas() * local


func run_sequence() -> void:
	var points := {}
	for label: String in TEXELS:
		points[label] = viewport_position(TEXELS[label])
	var why: Array[String] = []
	if player.state != Player.State.IDLE or sprite.texture != IDLE:
		why.append("the mage is not idle (state %s, texture %s)" % [player.state, sprite.texture.resource_path])
	if not sprite.is_visible_in_tree():
		why.append("the sprite is not visible (blinking after a hit?)")
	if player.invulnerable > 0.0 or player.is_failing or player.is_cleared:
		why.append("not at rest (invulnerable %.3f, failing %s, cleared %s)" % [player.invulnerable,
			player.is_failing, player.is_cleared])
	for label: String in points:
		var d: Vector2 = (points[label] - crosshair.position).abs()
		if maxf(d.x, d.y) <= CROSSHAIR_REACH:
			why.append("the crosshair is over the %s pixel; move the mouse away" % label)
	if not why.is_empty():
		print(JSON.stringify({"refused": "F9", "why": why}))
		return

	busy = true
	var saved_tint: Variant = mat.get_shader_parameter("tint_color")   # null = not set, shader default
	var saved_intensity: Variant = mat.get_shader_parameter("intensity")
	var image := IDLE.get_image()
	var stored := {}
	for label: String in TEXELS:
		stored[label] = rgb8(image.get_pixelv(TEXELS[label]))
	var setup := {"texels": {}, "flip_h": sprite.flip_h, "sprite_offset": [sprite.offset.x, sprite.offset.y],
		"canvas_transform_origin": [sprite.get_global_transform_with_canvas().origin.x,
			sprite.get_global_transform_with_canvas().origin.y],
		"crosshair": [crosshair.position.x, crosshair.position.y],
		"saved_tint_color": var_to_str(saved_tint), "saved_intensity": var_to_str(saved_intensity)}
	for label: String in TEXELS:
		setup.texels[label] = {"texture_pixel": [TEXELS[label].x, TEXELS[label].y], "stored_rgb8": stored[label],
			"viewport_position": [points[label].x, points[label].y]}
	print(JSON.stringify({"setup": setup}))

	driver.set_process(false)
	var rows: Array[Dictionary] = []
	mat.set_shader_parameter("tint_color", null)   # the shader default, vec4(1.0, 0.0, 0.0, 1.0)
	for t: float in [0.0, 0.5, 1.0]:
		mat.set_shader_parameter("intensity", t)
		var file := "hurt_tint_i%.1f.png" % t
		var img := await capture(file, {"tint_color": "shader default (red)", "intensity": t})
		for label: String in TEXELS:
			rows.append(sample(img, label, file, points[label], {"tint_color": [255, 0, 0], "intensity": t,
				"mix_on_stored_values": mix8(stored[label], [255, 0, 0], t)}))

	mat.set_shader_parameter("tint_color", GREY)
	mat.set_shader_parameter("intensity", 2.0)
	var grey_file := "hurt_tint_grey_i2.0.png"
	var grey_img := await capture(grey_file, {"tint_color": rgb8(GREY), "intensity": 2.0,
		"intensity_read_back": mat.get_shader_parameter("intensity")})
	for label: String in TEXELS:
		rows.append(sample(grey_img, label, grey_file, points[label], {"tint_color": rgb8(GREY), "intensity": 2.0,
			"mix_on_stored_values_if_not_clamped": mix8(stored[label], rgb8(GREY), 2.0),
			"mix_on_stored_values_if_clamped_to_1": mix8(stored[label], rgb8(GREY), 1.0)}))

	mat.set_shader_parameter("tint_color", saved_tint)
	mat.set_shader_parameter("intensity", saved_intensity)
	driver.set_process(true)
	print(JSON.stringify({"restored": {"tint_color": var_to_str(mat.get_shader_parameter("tint_color")),
		"intensity": var_to_str(mat.get_shader_parameter("intensity")), "driver_processing": driver.is_processing()}}))
	write_json("hurt_tint_pixels.json", {"scene": scene_file_path, "setup": setup, "samples": rows})
	busy = false


## stored * (1 - t) + target * t per channel, on the stored 8-bit values (no hdr_2d), clamped to 0..255 as the
## framebuffer would. Kept unrounded so the x.5 cases stay visible.
func mix8(stored: Array, target: Array, t: float) -> Array:
	var out := []
	for i in 3:
		out.append(clampf(stored[i] * (1.0 - t) + target[i] * t, 0.0, 255.0))
	return out
