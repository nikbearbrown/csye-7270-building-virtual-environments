extends SceneTree
## Checks CLAUDE.md's headless facts on this machine: which display server and
## renderer a run gets, when a shader error is reported (on load, on reading
## its uniforms, or once a material uses it), what a broken shader's uniform
## list holds, and whether the frame can be read back. Markers go to stderr,
## as Godot's errors do, so the two stay in order in the log.
##
## From assignment-5/:
##   timeout 120 godot --headless --path evidence/headless-probe --script res://probe_headless.gd
## and once more with --rendering-driver metal added, to see what that changes.

func _init() -> void:
	printerr("PROBE display server '%s', video adapter '%s'" % [DisplayServer.get_name(), RenderingServer.get_video_adapter_name()])
	var broken := load("res://shaders/broken.gdshader") as Shader
	printerr("PROBE 1 broken shader loaded: %s" % (broken != null))
	var mat := ShaderMaterial.new()
	mat.shader = broken
	printerr("PROBE 2 broken shader set on a ShaderMaterial")
	var box := MeshInstance3D.new()
	box.mesh = BoxMesh.new()
	box.material_override = mat
	root.add_child(box)
	printerr("PROBE 3 that material is on a mesh in the tree")
	printerr("PROBE 4 broken shader's uniform list: %s" % [broken.get_shader_uniform_list()])
	var good := load("res://shaders/good.gdshader") as Shader
	printerr("PROBE 5 good shader's uniform list: %s" % [good.get_shader_uniform_list()])
	printerr("PROBE 5b the renderer's default for 'amount': %s" % [RenderingServer.shader_get_parameter_default(good.get_rid(), &"amount")])
	var texture := root.get_texture()
	var image := texture.get_image() if texture else null
	printerr("PROBE 6 frame read back: %s" % ("an image of %s" % image.get_size() if image else "nothing"))
	printerr("PROBE done; quitting with code 0")
	quit(0)
