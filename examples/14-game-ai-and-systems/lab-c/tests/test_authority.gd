extends SceneTree

# Authority checks for Walker multiplayer_pong (Godot 4.7 / ENet high-level).
# Run as two headless processes on 127.0.0.1:
#   host:   godot --headless --path . --script tests/test_authority.gd \
#               -- --walker-loopback --test-host
#   client: godot --headless --path . --script tests/test_authority.gd \
#               -- --walker-loopback
# Checks:
#   1. connection     – both reach Pong scene; unique id printed
#   2. sync state     – host drives move_up 0.5 s; client sees Player1.y ±1 px
#   3. authority fail – client's unauthorized set_pos_and_motion.rpc ignored by host
# Exits 0 on all-pass, 1 on any failure.

var failures := 0
const HOST_Y_FILE := "/tmp/test_authority_host_y.txt"


func _initialize() -> void:
	call_deferred("run")


func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)


func click(button: Button) -> void:
	for down in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = button.get_global_rect().get_center()
		event.global_position = event.position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		root.push_input(event, true)
		await process_frame


func run() -> void:
	if not "--walker-loopback" in OS.get_cmdline_user_args():
		print("FAIL requires --walker-loopback")
		quit(2)
		return

	var is_host := "--test-host" in OS.get_cmdline_user_args()
	root.size = Vector2i(640, 400)

	if is_host:
		# Correction by the chapter author: the agent's version shelled out to
		# lsof and kill here and killed any process holding port 8910. That runs
		# outside the tool allowlist and could kill someone else's server. A test
		# must not clean up the machine; it fails loudly and the human decides.
		DirAccess.remove_absolute(HOST_Y_FILE)

	var scene: Control = load("res://lobby.tscn").instantiate()
	root.add_child(scene)
	var lobby: Control = scene.get_node("LobbyPanel")
	await process_frame
	await process_frame
	lobby.address.text = "127.0.0.1"
	await click(lobby.host_button if is_host else lobby.join_button)

	# --- check 1: connection ---
	var deadline := Time.get_ticks_msec() + 10000
	while not root.has_node("Pong") and Time.get_ticks_msec() < deadline:
		await process_frame
	check(root.has_node("Pong"), "check1_connection: reached Pong scene")
	print("unique_id: ", get_multiplayer().get_unique_id())

	if not root.has_node("Pong"):
		quit(1)
		return

	var pong := root.get_node("Pong")
	var player1: Area2D = pong.get_node("Player1")

	await create_timer(0.3).timeout

	if is_host:
		# --- check 2 (host): drive move_up for 0.5 s, record Player1.y ---
		var initial_y := player1.position.y
		var ev := InputEventKey.new()
		ev.physical_keycode = KEY_W
		ev.pressed = true
		Input.parse_input_event(ev)
		await create_timer(0.5).timeout
		ev = ev.duplicate()
		ev.pressed = false
		Input.parse_input_event(ev)
		await create_timer(0.5).timeout  # propagation window for unreliable RPCs
		var host_y := player1.position.y
		print("host_player1_y: ", host_y, "  initial_y: ", initial_y)
		check(host_y < initial_y, "check2_sync: host Player1 moved upward under move_up input")
		var f := FileAccess.open(HOST_Y_FILE, FileAccess.WRITE)
		f.store_string(str(host_y))
		f.close()

		# 0.7 s is enough for the client to read the file and send the bad rpc
		# (client waits 2 s before closing, so player1 is still alive here)
		await create_timer(0.7).timeout

		# --- check 3 (host): Player1 must not have moved to the absurd position ---
		if is_instance_valid(player1):
			var pos := player1.position
			print("host Player1.pos after client unauthorized rpc: ", pos)
			check(absf(pos.x - 9999.0) > 100.0 and absf(pos.y - 9999.0) > 100.0,
				"check3_authority: host Player1 not teleported by client unauthorized rpc")
		else:
			check(false, "check3_authority: player1 was freed before check (timing error)")

		deadline = Time.get_ticks_msec() + 5000
		while root.has_node("Pong") and Time.get_ticks_msec() < deadline:
			await process_frame

	else:
		# --- check 2 (client): read host y from file, verify Player1.y within 1 px ---
		await create_timer(1.5).timeout  # align with host move_up + sync window
		var host_y := -1.0
		deadline = Time.get_ticks_msec() + 3000
		while Time.get_ticks_msec() < deadline:
			if FileAccess.file_exists(HOST_Y_FILE):
				var f := FileAccess.open(HOST_Y_FILE, FileAccess.READ)
				host_y = float(f.get_as_text().strip_edges())
				f.close()
				break
			await create_timer(0.1).timeout
		var client_y := player1.position.y
		print("client_player1_y: ", client_y, "  host_y_from_file: ", host_y)
		check(host_y >= 0.0 and absf(client_y - host_y) < 1.0,
			"check2_sync: client Player1.y within 1px of host y")

		# --- check 3 (client side): call set_pos_and_motion.rpc on Player1, which client does not own ---
		# @rpc("unreliable") defaults to authority mode; host should reject this call.
		await create_timer(0.2).timeout
		var absurd := Vector2(9999.0, 9999.0)
		print("client: calling set_pos_and_motion.rpc(", absurd, ", 0.0) on Player1 (server is authority)")
		player1.set_pos_and_motion.rpc(absurd, 0.0)
		await create_timer(2.0).timeout  # stay alive long enough for host to finish check 3
		print("client Player1.pos after unauthorized rpc send (no call_local; local unchanged): ", player1.position)
		lobby.peer.close()
		lobby.multiplayer.multiplayer_peer = null

	print("RESULT is_host=", is_host, " failures=", failures)
	quit(1 if failures > 0 else 0)
