extends SceneTree
## CPU reference model for CLAUDE.md rule 4. This models the specification,
## not the current shader implementation.

const FLASH_COLOR := Color("25354a")
const SAMPLES := [0.0, 0.5, 1.0]
var failures := 0


func model(vertex_color: Color, amount: float) -> Color:
	return Color(
		lerpf(vertex_color.r, FLASH_COLOR.r, amount),
		lerpf(vertex_color.g, FLASH_COLOR.g, amount),
		lerpf(vertex_color.b, FLASH_COLOR.b, amount),
		vertex_color.a
	)


func hex_rgb(color: Color) -> String:
	return "#%02x%02x%02x" % [roundi(color.r * 255.0), roundi(color.g * 255.0), roundi(color.b * 255.0)]


func check(id: String, passed: bool, observed) -> void:
	print(JSON.stringify({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed}))
	if not passed:
		failures += 1


func _initialize() -> void:
	var colors := {"body": Color("dd775b"), "eyes": Color("000000")}
	var table := {}
	for name in colors:
		var row := {}
		for amount in SAMPLES:
			row[str(amount)] = hex_rgb(model(colors[name], amount))
		table[name] = row
	print("FLASH_MODEL_COLORS: ", JSON.stringify(table))

	for name in colors:
		var source: Color = colors[name]
		var at_zero := model(source, 0.0)
		var at_one := model(source, 1.0)
		check("%s at 0.0 preserves RGB and alpha" % name, at_zero.is_equal_approx(source), at_zero)
		check("%s at 1.0 is flash RGB with alpha unchanged" % name,
			Vector3(at_one.r, at_one.g, at_one.b).is_equal_approx(Vector3(FLASH_COLOR.r, FLASH_COLOR.g, FLASH_COLOR.b)) and is_equal_approx(at_one.a, source.a), at_one)

	# Transparent input remains transparent even though its hidden RGB is mixed.
	var transparent := model(Color(0.8, 0.2, 0.4, 0.0), 1.0)
	check("transparent alpha stays transparent", is_zero_approx(transparent.a), transparent)
	print("FLASH_MODEL failures=", failures)
	quit(1 if failures else 0)
