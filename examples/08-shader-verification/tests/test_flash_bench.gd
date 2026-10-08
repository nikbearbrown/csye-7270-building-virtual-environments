extends SceneTree

const BENCH := preload("res://tests/flash_bench.tscn")
const SHADER_PATH := "res://features/player/clawd_flash.gdshader"
var failures := 0


func check(id: String, passed: bool, observed) -> void:
	print(JSON.stringify({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed}))
	if not passed:
		failures += 1


func _initialize() -> void:
	run.call_deferred()


func run() -> void:
	var bench := BENCH.instantiate()
	root.add_child(bench)
	await process_frame
	var expected := {"Amount0": 0.0, "Amount05": 0.5, "Amount1": 1.0}
	var material_ids := []
	for node_name in expected:
		var copy: Node2D = bench.get_node(node_name)
		var material := copy.material as ShaderMaterial
		var amount: float = material.get_shader_parameter("flash_amount") if material else -1.0
		check("%s has a ShaderMaterial" % node_name, material != null, str(material))
		if material:
			material_ids.append(material.get_instance_id())
		check("%s flash_amount is fixed at %.1f" % [node_name, expected[node_name]], is_equal_approx(amount, expected[node_name]), amount)
	check("the three copies have distinct ShaderMaterials", material_ids.size() == 3 and material_ids[0] != material_ids[1] and material_ids[0] != material_ids[2] and material_ids[1] != material_ids[2], material_ids)

	var shader: Shader = load(SHADER_PATH)
	var uniforms := shader.get_shader_uniform_list()
	var by_name := {}
	for uniform in uniforms:
		by_name[uniform.name] = uniform
	var amount_uniform: Dictionary = by_name.get("flash_amount", {})
	var color_uniform: Dictionary = by_name.get("flash_color", {})
	check("shader uniform names are intact", by_name.size() == 2 and by_name.has("flash_amount") and by_name.has("flash_color"), by_name.keys())
	check("flash_amount uniform is float", amount_uniform.get("type") == TYPE_FLOAT, amount_uniform)
	check("flash_color uniform is Color", color_uniform.get("type") == TYPE_COLOR, color_uniform)

	bench.queue_free()
	await process_frame
	print("FLASH_BENCH_TEST failures=", failures)
	quit(1 if failures else 0)
