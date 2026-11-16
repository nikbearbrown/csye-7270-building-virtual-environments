extends Node
# C09 / C10 / C11 scene: a ColorRect named Rect with the dial shader (06-dial). The fire_* methods hold EXACTLY the lines shown on screen,
# run by --call-at, so the capture shows the shown code running.
func harness_setup(ctx: Dictionary) -> void:
	var r := ColorRect.new()
	r.name = "Rect"
	r.size = ctx["logical"]
	r.material = ctx["materials"]["main"]
	add_child(r)
func fire_set() -> void:
	$Rect.material.set_shader_parameter("red", 0.9)
func fire_typo() -> void:
	$Rect.material.set_shader_parameter("rd", 0.9)   # typo
func fire_correct() -> void:
	$Rect.material.set_shader_parameter("red", 0.9)
func fire_start() -> void:
	$Rect.material.set_shader_parameter("red", 0.0)
func fire_tween() -> void:
	var tween := create_tween()
	tween.tween_property($Rect.material, "shader_parameter/red", 1.0, 2.0)
