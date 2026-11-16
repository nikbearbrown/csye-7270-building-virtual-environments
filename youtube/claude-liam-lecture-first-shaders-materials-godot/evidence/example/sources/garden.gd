extends Node3D
# One gameplay authority. Presentation observes these fields; it never opens gates.
const SPEED := 3.0
const CHARGE_SECONDS := 0.6
const PAD := Vector3(-2, 0, 0)
const START := Vector3(-4, 0, 0)
var player: CharacterBody3D
var gate: StaticBody3D
var gate_mesh: MeshInstance3D
var pad_material: ShaderMaterial
var charge := 0.0
var charging := false
var gate_open := false
var won := false
var action_count := 0
var finish_count := 0
var elapsed := 0.0
var state := "idle"
var presentation_enabled := true
var audio_enabled := true
var animation_enabled := true
var burst: CPUParticles3D
var ambient: CPUParticles3D
var sound: Node
var rig: Node3D
var hud: Label
var status_label: Label
var light: DirectionalLight3D
var mute := false
var gate_motion: AnimationPlayer
var last_state := ""
var last_step := 0.0

func _ready() -> void:
	get_viewport().content_scale_size = Vector2i(1280, 720)
	for pair in [["garden_left", KEY_A, KEY_LEFT], ["garden_right", KEY_D, KEY_RIGHT], ["garden_up", KEY_W, KEY_UP], ["garden_down", KEY_S, KEY_DOWN], ["garden_action", KEY_E], ["garden_reset", KEY_R], ["garden_pause", KEY_P, KEY_ESCAPE], ["garden_mute", KEY_M]]:
		if not InputMap.has_action(pair[0]):
			InputMap.add_action(pair[0])
			for k in pair.slice(1):
				var e := InputEventKey.new()
				e.physical_keycode = k
				InputMap.action_add_event(pair[0], e)
	process_mode = Node.PROCESS_MODE_ALWAYS
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color("172830")
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color("dce6e2")
	env.environment.ambient_light_energy = 0.3
	add_child(env)
	light = DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-60, -25, 0)
	light.light_energy = 0.65
	light.shadow_enabled = true
	add_child(light)
	var camera := Camera3D.new()
	camera.position = Vector3(5.8, 9, 11)
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 10.3
	add_child(camera)
	camera.look_at(Vector3(0, 0, 0))
	camera.current = true
	make_box("Floor", Vector3(12, 0.4, 6), Vector3(0, -0.2, 0), Color("dfd8c7"), true)
	for z in [-3.0, 3.0]:
		make_box("Rail", Vector3(12, 0.3, 0.16), Vector3(0, 0.12, z), Color("8b9d94"), true)
	for x in [-6.0, 6.0]:
		make_box("EndRail", Vector3(0.16, 0.3, 6), Vector3(x, 0.12, 0), Color("8b9d94"), true)
	var start_marker := Marker3D.new()
	start_marker.name = "StartReference"
	start_marker.position = START
	add_child(start_marker)
	var pad_marker := Marker3D.new()
	pad_marker.name = "PadReference"
	pad_marker.position = PAD
	add_child(pad_marker)
	var pad := make_box("SignalPad", Vector3(1.55, 0.10, 1.55), PAD + Vector3(0, 0.06, 0), Color.WHITE, false)
	pad_material = ShaderMaterial.new()
	pad_material.shader = load("res://signal-garden/signal.gdshader")
	pad.material_override = pad_material
	gate = StaticBody3D.new()
	gate.name = "Gate"
	gate.position = Vector3(1, 0, 0)
	add_child(gate)
	var shape := CollisionShape3D.new()
	shape.name = "Collision"
	var box := BoxShape3D.new()
	box.size = Vector3(0.25, 2.1, 6)
	shape.shape = box
	shape.position.y = 1.05
	gate.add_child(shape)
	gate_mesh = MeshInstance3D.new()
	gate_mesh.name = "Panel"
	var mesh := BoxMesh.new()
	mesh.size = Vector3(0.18, 1.6, 5.7)
	gate_mesh.mesh = mesh
	gate_mesh.position.y = 0.8
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = load("res://signal-garden/assets/gate-color.png")
	mat.roughness_texture = load("res://signal-garden/assets/gate-roughness.png")
	mat.roughness = 1.0
	mat.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
	gate_mesh.material_override = mat
	gate.add_child(gate_mesh)
	for z in [-2.9, 2.9]:
		make_box("GatePost", Vector3(0.4, 2.4, 0.4), Vector3(1, 1.2, z), Color("263e46"), false)
	make_box("Finish", Vector3(1.6, 0.08, 4.8), Vector3(4.6, 0.05, 0), Color("61bca5"), false)
	for x in [-3.0, -0.5, 2.5]:
		make_box("Guide", Vector3(0.15, 0.02, 0.75), Vector3(x, 0.02, 0), Color("7a8c82"), false)
	player = CharacterBody3D.new()
	player.name = "Claude"
	player.position = START
	add_child(player)
	var body := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.40
	capsule.height = 0.90
	body.shape = capsule
	body.position.y = 0.45
	player.add_child(body)
	rig = load("res://signal-garden/mascot-rig.gd").new()
	rig.name = "Rig"
	player.add_child(rig)
	gate_motion = AnimationPlayer.new()
	gate_motion.name = "GateAnimation"
	gate_motion.process_mode = Node.PROCESS_MODE_PAUSABLE
	gate.add_child(gate_motion)
	var lib := AnimationLibrary.new()
	var clip := Animation.new()
	clip.length = 0.5
	var t := clip.add_track(Animation.TYPE_VALUE)
	clip.track_set_path(t, NodePath("Panel:position:y"))
	clip.track_insert_key(t, 0.0, 0.8)
	clip.track_insert_key(t, 0.5, 3.0)
	lib.add_animation("open", clip)
	gate_motion.add_animation_library("", lib)
	burst = load("res://signal-garden/effects/burst.tscn").instantiate()
	ambient = load("res://signal-garden/effects/ambient.tscn").instantiate()
	add_child(burst)
	add_child(ambient)
	ambient.position = Vector3(3, 0.15, 0)
	sound = load("res://signal-garden/sound.gd").new()
	sound.enabled = audio_enabled
	add_child(sound)
	var markers = load("res://signal-garden/markers.gd").new()
	markers.name = "DecorativeMarkers"
	for arg in OS.get_cmdline_user_args():
		if arg == "--markers=cached": markers.mode = "cached"
	add_child(markers)
	build_hud()
	if audio_enabled:
		sound.start_ambience()

func make_box(label: String, size: Vector3, pos: Vector3, color: Color, solid: bool) -> MeshInstance3D:
	var visual := MeshInstance3D.new()
	visual.name = label
	var mesh := BoxMesh.new()
	mesh.size = size
	visual.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color.srgb_to_linear()
	mat.roughness = 0.85
	visual.material_override = mat
	if solid:
		var obj := StaticBody3D.new()
		obj.name = label
		obj.position = pos
		add_child(obj)
		obj.add_child(visual)
		var shape := CollisionShape3D.new()
		var box := BoxShape3D.new()
		box.size = size
		shape.shape = box
		obj.add_child(shape)
	else:
		visual.position = pos
		add_child(visual)
	return visual

func build_hud() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)
	var panel := ColorRect.new()
	panel.color = Color("13242a")
	panel.size = Vector2(1280, 116)
	canvas.add_child(panel)
	hud = Label.new()
	hud.position = Vector2(38, 18)
	hud.add_theme_font_size_override("font_size", 28)
	hud.text = "SIGNAL GARDEN  /  WALKER CLAUDE"
	canvas.add_child(hud)
	var instructions := Label.new()
	instructions.position = Vector2(38, 61)
	instructions.add_theme_font_size_override("font_size", 19)
	instructions.text = "WASD / arrows  Move     E  Charge on the pad     R  Reset     P / Esc  Pause     M  Mute"
	canvas.add_child(instructions)
	status_label = Label.new()
	status_label.position = Vector2(38, 650)
	status_label.add_theme_font_size_override("font_size", 23)
	canvas.add_child(status_label)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("garden_pause") and not event.is_echo():
		get_tree().paused = not get_tree().paused
		get_viewport().set_input_as_handled()
	if event.is_action_pressed("garden_mute") and not event.is_echo():
		mute = not mute
		AudioServer.set_bus_mute(AudioServer.get_bus_index("GardenSFX"), mute)
		AudioServer.set_bus_mute(AudioServer.get_bus_index("GardenAmbience"), mute)

func _physics_process(delta: float) -> void:
	if not is_instance_valid(player):
		return
	if get_tree().paused:
		status_label.text = "PAUSED  /  P to resume"
		return
	elapsed += delta
	if Input.is_action_just_pressed("garden_reset"):
		reset_game()
	var axis := Input.get_vector("garden_left", "garden_right", "garden_up", "garden_down")
	var on_pad := Vector2(player.position.x - PAD.x, player.position.z - PAD.z).length() <= 0.8
	if Input.is_action_just_pressed("garden_action") and on_pad and not charging and not gate_open:
		charging = true
		charge = 0.0
		action_count += 1
		sound.play_event("charge", player.position)
	if charging:
		charge = minf(CHARGE_SECONDS, charge + delta)
		if charge >= CHARGE_SECONDS - 0.00001:
			charging = false
			gate_open = true
			gate.get_node("Collision").set_deferred("disabled", true)
			gate_motion.play("open")
			fire_burst(PAD)
			sound.play_event("gate", gate.position)
	player.velocity.x = axis.x * SPEED if not charging and not won else 0.0
	player.velocity.z = axis.y * SPEED if not charging and not won else 0.0
	player.velocity.y = -2.0
	player.move_and_slide()
	if axis.length() > 0.01 and not charging and not won:
		last_step += delta
		if last_step >= 0.34:
			last_step = 0.0
			sound.play_event("step", player.position)
	if player.position.x > 3.8 and gate_open and not won:
		won = true
		finish_count += 1
		fire_burst(player.position)
		sound.play_event("finish", player.position)
	state = "celebrate" if won else ("charge" if charging else ("walk" if Vector2(player.velocity.x, player.velocity.z).length() > 0.1 else "idle"))
	if animation_enabled:
		rig.set_state(state)
	pad_material.set_shader_parameter("activation", charge / CHARGE_SECONDS)
	ambient.emitting = gate_open and not won and presentation_enabled and is_visible_in_tree()
	status_label.text = "SIGNAL SENT  /  R to replay" if won else ("CHARGING  /  %d%%" % int(charge / CHARGE_SECONDS * 100) if charging else ("GATE OPEN  /  Follow the path" if gate_open else ("ON THE PAD  /  Press E" if on_pad else "01  /  Find the terracotta signal pad")))

func fire_burst(at: Vector3) -> void:
	if presentation_enabled:
		burst.position = at + Vector3(0, 0.4, 0)
		burst.restart()
		burst.emitting = true

func reset_game() -> void:
	player.position = START
	player.velocity = Vector3.ZERO
	charge = 0.0
	charging = false
	gate_open = false
	won = false
	gate.get_node("Collision").set_deferred("disabled", false)
	gate_motion.stop()
	gate_mesh.position.y = 0.8
	burst.emitting = false
	ambient.emitting = false
	last_step = 0.0
	sound.stop_all()
	sound.play_event("reset", START)
	sound.start_ambience()

func _exit_tree() -> void:
	get_tree().paused = false
