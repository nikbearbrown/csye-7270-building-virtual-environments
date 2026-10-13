extends Node2D
# Movie Maker route: does TIME advance by 1/30 s per written frame? Does Engine.time_scale scale it? Frames are saved as PNG; TIME is decoded from them afterwards.
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
var frame := 0
func _ready() -> void:
	var rect := ColorRect.new()
	rect.size = Vector2(20, 20)
	rect.position = Vector2(10, 10)
	var sh := Shader.new()
	sh.code = ENCODER
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	add_child(rect)
func _process(delta: float) -> void:
	frame += 1
	if frame == 30: Engine.time_scale = 0.25
	if frame == 50: Engine.time_scale = 1.0
	print("process frame %d delta %.5f time_scale %.2f" % [frame, delta, Engine.time_scale])
