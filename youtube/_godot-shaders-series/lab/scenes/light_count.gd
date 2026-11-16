extends Node
# C05 scene (light-count): CanvasModulate black, a white square Sprite2D with the shader (a light() outputting a constant 0.2 red),
# and PointLight2D nodes (white 128 px texture, texture_scale 12 so the light covers the 1280x720 canvas, energy 1) added one by one:
# add_light() is called by --call-at. Same recipe as evidence/planning-checks/verify4.gd (320x180 there, 3x here).
var spr: Sprite2D
var count := 0
func harness_setup(ctx: Dictionary) -> void:
	var dark := CanvasModulate.new()
	dark.color = Color(0, 0, 0, 1)
	add_child(dark)
	var bg := ColorRect.new()                         # an unlit-looking dark canvas: the modulate turns it black
	bg.size = ctx["logical"]
	bg.color = Color.WHITE
	bg.light_mask = 0                                 # not lit: it stays black under the modulate
	add_child(bg)
	var im := Image.create(100, 100, false, Image.FORMAT_RGBA8)
	im.fill(Color.WHITE)
	spr = Sprite2D.new()
	spr.texture = ImageTexture.create_from_image(im)
	spr.position = ctx["logical"] / 2.0
	spr.scale = Vector2(3, 3)
	spr.material = ctx["materials"]["main"]
	add_child(spr)
func add_light() -> void:
	var l := PointLight2D.new()
	var im := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	im.fill(Color.WHITE)
	l.texture = ImageTexture.create_from_image(im)
	l.texture_scale = 12.0
	l.energy = 1.0
	l.position = spr.position
	add_child(l)
	count += 1
