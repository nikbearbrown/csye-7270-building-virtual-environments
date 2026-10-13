extends SceneTree
func _initialize():
    call_deferred("test_shader")
func test_shader():
    var rect = ColorRect.new()
    rect.size = Vector2(100,100)
    var material = ShaderMaterial.new()
    var shader = Shader.new()
    shader.code = "shader_type canvas_item; void fragment() { float gain = 5; COLOR = vec4(gain); }"
    material.shader = shader
    rect.material = material
    root.add_child(rect)
    for i in range(5): await process_frame
    print("Negative shader submitted; inspect SHADER ERROR, not exit status.")
    quit()
