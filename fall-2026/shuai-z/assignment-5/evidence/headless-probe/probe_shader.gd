extends SceneTree
## Compiles one shader the way a material does, then prints what a headless run
## can see of it: any SHADER ERROR (Godot prints it when the shader is set on a
## ShaderMaterial, not when it is loaded), the uniforms the engine reports, and
## the source's declaration lines, which hold the defaults the dummy renderer
## does not report. It reads the shader and writes nothing.
##
## From assignment-5/, with the project's folder and the shader's res:// path:
##   timeout 120 godot --headless --path game --script "$PWD/evidence/headless-probe/probe_shader.gd" -- res://shaders/invulnerable_tint.gdshader

const MODES := ["spatial", "canvas_item", "particles", "sky", "fog"]
const HINTS := {
	PROPERTY_HINT_NONE: "no hint",
	PROPERTY_HINT_RANGE: "range",
	PROPERTY_HINT_RESOURCE_TYPE: "resource",
	PROPERTY_HINT_COLOR_NO_ALPHA: "colour without alpha",
}


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 1:
		printerr("PROBE usage: godot --headless --path <project> --script <this file> -- res://<shader>.gdshader")
		quit(2)
		return
	var shader := load(args[0]) as Shader
	printerr("PROBE %s loaded: %s" % [args[0], shader != null])
	if shader == null:
		quit(1)
		return
	var material := ShaderMaterial.new()
	material.shader = shader
	# This marker must not contain the words the log is searched for.
	printerr("PROBE set on a ShaderMaterial; a compile error would be printed above this line")
	printerr("PROBE mode: %s" % MODES[shader.get_mode()])
	var uniforms := shader.get_shader_uniform_list(true)
	printerr("PROBE uniforms the engine reports: %d" % uniforms.size())
	for u: Dictionary in uniforms:
		if u.type == TYPE_NIL:
			printerr("PROBE   group %s" % u.name)
		else:
			printerr("PROBE   %s: %s, %s '%s'" % [u.name, type_string(u.type), HINTS.get(u.hint, "hint %d" % u.hint), u.hint_string])
	printerr("PROBE declarations in the source:")
	var declaration := RegEx.create_from_string("^(shader_type|render_mode|((global|instance) )?uniform|group_uniforms)\\b")
	var lines := shader.code.split("\n")
	for i in lines.size():
		var line := lines[i].strip_edges()
		if declaration.search(line):
			printerr("PROBE   line %d: %s" % [i + 1, line])
	printerr("PROBE done")
	quit(0)
