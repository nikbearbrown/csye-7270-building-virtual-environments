extends SceneTree
var game: Node3D
var failures := 0
var samples := []
func _initialize() -> void: call_deferred("run")
func key(code: Key, down: bool) -> void:
	var event := InputEventKey.new(); event.physical_keycode=code; event.pressed=down; Input.parse_input_event(event)
func step() -> void:
	await process_frame
	if game:
		samples.append({"physics_frame":Engine.get_physics_frames(),"elapsed":game.elapsed,"charge":game.charge,"uniform":game.pad_material.get_shader_parameter("activation"),"paused":paused,"time_scale":Engine.time_scale})
func check(label: String, ok: bool) -> void:
	print(("PASS " if ok else "FAIL ")+label)
	if not ok: failures+=1
func tap(code: Key) -> void:
	key(code,true)
	for i in range(4): await step()
	key(code,false)
	for i in range(4): await step()
func new_run() -> void:
	game=load("res://course-series/main.tscn").instantiate();game.audio_enabled=false;root.add_child(game)
	for i in range(4):await step()
	key(KEY_D,true)
	var guard:=0
	while game.player.position.x < -2.1 and guard<1000:await step();guard+=1
	key(KEY_D,false)
	for i in range(4):await step()
func run() -> void:
	await new_run()
	for scale in [1.0,0.5]:
		Engine.time_scale=scale
		var start:float=game.elapsed; var count_before:int=game.action_count
		key(KEY_E,true);await step();key(KEY_E,false)
		var retriggered:=false;var guard:=0
		while not game.gate_open and guard<1000:
			await step();guard+=1
			if game.charge > .2 and not retriggered:
				key(KEY_E,true);await step();key(KEY_E,false);retriggered=true
		var duration:float=game.elapsed-start
		var tolerance:float=1.0/60.0 + 0.00001
		check("scaled duration "+str(scale),absf(duration-.6)<=tolerance)
		check("retrigger ignored "+str(scale),game.action_count==count_before+1)
		check("end uniform one "+str(scale),is_equal_approx(game.pad_material.get_shader_parameter("activation"),1.0))
		print("DURATION ",JSON.stringify({"scale":scale,"game_seconds":duration,"tolerance":tolerance,"render_samples":guard}))
		Engine.time_scale=1.0;game.queue_free();await process_frame;await new_run()
	key(KEY_E,true);await step();key(KEY_E,false)
	while game.charge<.15:await step()
	await tap(KEY_P)
	var before:float=game.charge
	for i in range(30):await step()
	check("pause freezes charge",paused and game.charge==before)
	await tap(KEY_P);await tap(KEY_R)
	check("reset clears uniform",not paused and game.charge==0 and game.pad_material.get_shader_parameter("activation")==0)
	for i in range(100):await step()
	check("interruption has no late gate",not game.gate_open)
	var max_error:=0.0
	for sample in samples:
		# Before the first physics update the resource has no explicit override;
		# the shader declares activation = 0.0. Preserve that observation.
		if sample.uniform == null:
			if sample.charge != 0: failures += 1
			continue
		max_error=maxf(max_error,absf(float(sample.uniform)-float(sample.charge)/.6))
	check("every sampled uniform matches game state",max_error<0.00001)
	print("TRACE ",JSON.stringify(samples))
	print("RESULT 10 checks / ",failures," failures; sample count ",samples.size())
	game.queue_free();await process_frame;quit(1 if failures else 0)
