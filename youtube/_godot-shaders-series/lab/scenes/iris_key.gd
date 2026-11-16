extends Node
# C17 scene: the script shown on screen (B43) on the scene's root node, a Sprite child named Sprite with the iris shader. The harness pushes one
# physical key event (--key-at), the script's own _unhandled_key_input tweens the radius.
const HANDLER := "extends Node\nfunc _ready():\n\t$Sprite.material.set_shader_parameter(\"radius\", 0.0)\n\nfunc _unhandled_key_input(event):\n\tif event.pressed:\n\t\tvar tween := create_tween()\n\t\ttween.tween_property($Sprite.material, \"shader_parameter/radius\", 0.8, 1.5)\n"
func harness_setup(ctx: Dictionary) -> void:
	var holder := Node.new()
	var scr := GDScript.new()
	scr.source_code = HANDLER
	var err := scr.reload()
	holder.set_script(scr)
	var im := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	var n := 128
	for y in n:
		for x in n:
			var on := ((x / (n / 8)) + (y / (n / 8))) % 2 == 0
			im.set_pixel(x, y, Color("#FAF9F5") if on else Color("#5FA391"))
	var spr := Sprite2D.new()
	spr.name = "Sprite"
	spr.texture = ImageTexture.create_from_image(im)
	spr.position = ctx["logical"] / 2.0
	var sc: float = minf(ctx["logical"].x, ctx["logical"].y) * 0.8 / 128.0
	spr.scale = Vector2(sc, sc)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	spr.material = ctx["materials"]["main"]
	holder.add_child(spr)
	add_child(holder)                       # _ready of the shown script runs here
	print("scene script reload error: ", err)
