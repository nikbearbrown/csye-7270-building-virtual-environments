extends SceneTree
func _initialize() -> void:
	var sh: Shader = load("res://shaders/modes_blit.gdshader")
	var m := ShaderMaterial.new()
	m.shader = sh
	print("texture_blit MODE=", sh.get_mode(), " uniforms=", sh.get_shader_uniform_list())
	print("Shader.MODE_* =", Shader.MODE_SPATIAL, Shader.MODE_CANVAS_ITEM, Shader.MODE_PARTICLES, Shader.MODE_SKY, Shader.MODE_FOG)
	print("has DrawableTexture2D class=", ClassDB.class_exists("DrawableTexture2D"))
	quit(0)
