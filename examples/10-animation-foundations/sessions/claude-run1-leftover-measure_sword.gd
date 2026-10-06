extends SceneTree
# Temporary measurement script - not the final test.
# Run: godot --headless --path godot --script res://tests/measure_sword.gd --fixed-fps 120

func _initialize() -> void:
	call_deferred("run")

func press_f() -> void:
	var e := InputEventKey.new()
	e.keycode = KEY_F
	e.pressed = true
	Input.parse_input_event(e)
	e = InputEventKey.new()
	e.keycode = KEY_F
	e.pressed = false
	Input.parse_input_event(e)

func snap(sword: Node, sm: Node, f: int) -> void:
	var ap := sword.get_node("AnimationPlayer") as AnimationPlayer
	print("f%03d anim=%-15s pos=%6.4f vis=%s mon=%s rot=%8.3f in=%d rdy=%s combo=%d st=%s" % [
		f, ap.current_animation, ap.current_animation_position,
		sword.visible, sword.monitoring, sword.rotation_degrees,
		sword.attack_input_state, sword.ready_for_next_attack,
		sword.combo_count, sm.current_state.name
	])

func run() -> void:
	root.size = Vector2i(1280, 720)
	var demo: Node = load("res://Demo.tscn").instantiate()
	root.add_child(demo)
	for _i in 10:
		await process_frame

	var sm: Node = demo.get_node("Player/StateMachine")
	var sword: Node = demo.get_node("Player/BodyPivot/WeaponPivot/Offset/Sword")

	# ---------- SCENARIO A: single tap ----------
	print("=== SCENARIO A: single tap ===")
	print("before press: combo=%d mon=%s state=%s" % [
		sword.combo_count, sword.monitoring, sm.current_state.name])
	press_f()
	print("after  press: combo=%d mon=%s state=%s" % [
		sword.combo_count, sword.monitoring, sm.current_state.name])
	var f := 0
	while true:
		await process_frame
		f += 1
		snap(sword, sm, f)
		if sm.current_state.name == "Idle" and f > 5:
			print(">>> Back to Idle at frame %d" % f)
			break
		if f > 150:
			print("TIMEOUT A")
			break

	for _i in 30:
		await process_frame

	# ---------- SCENARIO B: three-swing combo ----------
	print("=== SCENARIO B: three-swing combo ===")
	var last_combo := 0
	var next_f_frame := -1
	press_f()
	print("after first press: combo=%d mon=%s state=%s" % [
		sword.combo_count, sword.monitoring, sm.current_state.name])
	last_combo = sword.combo_count  # should be 1
	print(">>> Swing 1 starts at f=0, scheduling F at f=20")
	next_f_frame = 20
	f = 0
	while true:
		await process_frame
		f += 1
		var cur_combo: int = sword.combo_count
		if cur_combo > last_combo and cur_combo <= 3:
			last_combo = cur_combo
			print(">>> Swing %d starts at f=%d" % [cur_combo, f])
			if cur_combo < 3:
				next_f_frame = f + 20
				print(">>> Scheduling F at f=%d" % next_f_frame)
		if f == next_f_frame:
			print(">>> F pressed at f=%d (in=%d rdy=%s)" % [
				f, sword.attack_input_state, sword.ready_for_next_attack])
			press_f()
		snap(sword, sm, f)
		if sm.current_state.name == "Idle" and f > 10:
			print(">>> Back to Idle at frame %d" % f)
			break
		if f > 300:
			print("TIMEOUT B")
			break

	for _i in 30:
		await process_frame

	# ---------- SCENARIO C: F tap 5 frames in ----------
	print("=== SCENARIO C: early F at frame 5 ===")
	press_f()
	print("after first press: combo=%d mon=%s state=%s" % [
		sword.combo_count, sword.monitoring, sm.current_state.name])
	f = 0
	while true:
		await process_frame
		f += 1
		snap(sword, sm, f)
		if f == 5:
			print(">>> F pressed at f=5 (in=%d rdy=%s)" % [
				sword.attack_input_state, sword.ready_for_next_attack])
			press_f()
		if sm.current_state.name == "Idle" and f > 5:
			print(">>> Back to Idle at frame %d" % f)
			break
		if f > 150:
			print("TIMEOUT C")
			break

	demo.queue_free()
	await process_frame
	print("=== MEASUREMENT DONE ===")
	quit(0)
