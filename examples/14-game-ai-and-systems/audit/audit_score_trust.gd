extends SceneTree
## Chapter-author audit for Lab C (written by hand, not by the agent).
## Question: the paddle RPC rejects a non-authority caller. Does the score RPC?
## pong.gd declares update_score as @rpc("any_peer", "call_local").
## The client calls update_score.rpc(false) three times, about 0.5 s after the
## match starts, before the ball (speed 100 px/s from the centre of a 640 px
## field) can reach either edge. The host reports its right-hand score.
## Loopback only: requires --walker-loopback, which binds the host to 127.0.0.1.

const FORGED := 3


func _initialize() -> void:
	call_deferred("run")


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
		quit(2)
		return
	var is_host := "--test-host" in OS.get_cmdline_user_args()
	root.size = Vector2i(640, 400)
	var scene: Control = load("res://lobby.tscn").instantiate()
	root.add_child(scene)
	var lobby: Control = scene.get_node("LobbyPanel")
	await process_frame
	await process_frame
	lobby.address.text = "127.0.0.1"
	await click(lobby.host_button if is_host else lobby.join_button)
	var deadline := Time.get_ticks_msec() + 10000
	while not root.has_node("Pong") and Time.get_ticks_msec() < deadline:
		await process_frame
	if not root.has_node("Pong"):
		print("NO MATCH")
		quit(1)
		return
	var pong := root.get_node("Pong")
	var before: int = pong.score_right
	if not is_host:
		await create_timer(0.5).timeout
		for i in FORGED:
			pong.update_score.rpc(false)
		print("client sent ", FORGED, " forged update_score(false) calls")
		await create_timer(2.0).timeout
		if is_instance_valid(pong):
			print("client score_right=", pong.score_right)
		lobby.peer.close()
		lobby.multiplayer.multiplayer_peer = null
		quit(0)
		return
	await create_timer(1.2).timeout
	print("host score_right before=", before, " after=", pong.score_right, " label=", pong.get_node("ScoreRight").text, " ball_x=", snappedf(pong.get_node("Ball").position.x, 0.1))
	print("RESULT forged points accepted by host: ", pong.score_right - before, " of ", FORGED)
	quit(0)
