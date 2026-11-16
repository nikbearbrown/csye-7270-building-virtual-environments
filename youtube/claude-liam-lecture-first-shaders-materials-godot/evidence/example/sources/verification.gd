extends Node
# An AI-assisted development instrument: observes, never controls gameplay.
var game: Node3D
var panel: Label
var enabled := false
var samples := 0
var mismatches := 0
var last_expected := 0.0
var last_actual := 0.0
var total_us := 0
var declared_uniform := false
var contract_code := ""
func _ready() -> void:
	game = get_parent()
	process_mode = Node.PROCESS_MODE_ALWAYS
	panel = Label.new()
	panel.position = Vector2(740, 145)
	panel.add_theme_font_size_override("font_size", 20)
	panel.add_theme_color_override("font_color", Color("f2f0e9"))
	var backing := StyleBoxFlat.new()
	backing.bg_color = Color(0.07, 0.12, 0.16, 0.96)
	backing.content_margin_left = 12
	backing.content_margin_right = 12
	backing.content_margin_top = 10
	backing.content_margin_bottom = 10
	panel.add_theme_stylebox_override("normal", backing)
	game.hud.get_parent().add_child(panel)
	panel.visible = false
	refresh_contract()
func refresh_contract() -> void:
	contract_code = game.pad_material.shader.code
	declared_uniform = false
	for uniform in game.pad_material.shader.get_shader_uniform_list():
		if uniform.name == "activation": declared_uniform = true
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_V:
		enabled = not enabled
		panel.visible = enabled
func _physics_process(_delta: float) -> void:
	var started := Time.get_ticks_usec()
	if contract_code != game.pad_material.shader.code: refresh_contract()
	last_expected = game.charge / game.CHARGE_SECONDS
	last_actual = float(game.pad_material.get_shader_parameter("activation"))
	samples += 1
	if not declared_uniform or absf(last_expected - last_actual) > 0.05: mismatches += 1
	total_us += Time.get_ticks_usec() - started
	if enabled:
		panel.text = "VERIFICATION / V hides\nState: %s\nDeclared activation: %s\nUniform expected: %.3f\nUniform observed: %.3f\nState probe checks linkage.\nRender and play still need checking." % [game.state, str(declared_uniform), last_expected, last_actual]
