extends Node
# Instrumentation only. The source game is copied unchanged; fixtures place Rudy
# near each case, then use real Input actions and the existing effect driver.
const OUT := "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-6/evidence/use-it-code"
var main: Node
var rudy: Node
var dust: GPUParticles2D
var bursts: Node
var phase := "setup"
var tick := 0
var measuring := false
var phase_tick := 0
var samples: Array = []
var frame_count := 0
var max_bursts := 0
var peak_frames := 0
var measured_ticks := 0
var emitting_ticks := 0
var born := 0
var snapshots: Array = []
var results: Array = []
var sample_clock := 0.0
var direction := 1
var done := false

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	process_priority = 100
	process_physics_priority = 100
	run.call_deferred()

func bind_main():
	main = get_tree().current_scene
	rudy = main.get_node("Rudy")
	dust = main.get_node("DustTrail/RunDust")
	bursts = main.get_node("Effects/SlashBursts")
	bursts.child_entered_tree.connect(func(_n): born += 1)

func _physics_process(_delta):
	tick += 1
	if not measuring: return
	phase_tick += 1
	if phase == "02_A_heavy":
		if phase_tick % 20 == 1: Input.action_press("slash")
		if phase_tick % 20 == 3: Input.action_release("slash")
	if phase == "04_B_heavy":
		if rudy.position.x >= 2890: direction = -1
		if rudy.position.x <= 2600: direction = 1
		Input.action_release("move_left" if direction == 1 else "move_right")
		Input.action_press("move_right" if direction == 1 else "move_left")
	max_bursts = maxi(max_bursts,bursts.get_child_count())
	measured_ticks += 1
	if bursts.get_child_count() == 2: peak_frames += 1
	if dust.emitting: emitting_ticks += 1

func _process(delta):
	if not measuring: return
	frame_count += 1
	sample_clock += delta
	if sample_clock >= 0.1:
		sample_clock = 0
		samples.append({"fps":Performance.get_monitor(Performance.TIME_FPS),"process_ms":1000*Performance.get_monitor(Performance.TIME_PROCESS),"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),"gpu_ms":RenderingServer.viewport_get_measured_render_time_gpu(get_viewport().get_viewport_rid()),"bursts":bursts.get_child_count(),"dust":dust.emitting})

func wait_s(seconds):
	await get_tree().create_timer(seconds,true,false,true).timeout
func frames(n):
	for i in n: await get_tree().physics_frame
func tap(action):
	var event := InputEventAction.new()
	event.action = action
	event.pressed = true
	Input.parse_input_event(event)
	await get_tree().process_frame
	await frames(2)
	event = InputEventAction.new()
	event.action = action
	event.pressed = false
	Input.parse_input_event(event)
	await get_tree().process_frame
func release_all():
	for action in ["move_right","move_left","jump","slash","pause","restart"]: Input.action_release(action)
func set_phase(name):
	phase = name
	FileAccess.open("/tmp/a6-use-it/phase.txt",FileAccess.WRITE).store_string(name)
	print("PHASE ",name)
func state():
	return {"phase":phase,"tick":tick,"x":rudy.position.x,"y":rudy.position.y,"vx":rudy.velocity.x,"vy":rudy.velocity.y,"gear":rudy.gear,"mode":rudy.mode,"main_state":main.state,"facing":rudy.facing,"floor":rudy.is_on_floor(),"invulnerable":rudy.is_invulnerable(),"look_alpha":rudy.get_node("Look").modulate.a,"dust_alpha":dust.modulate.a,"dust_emitting":dust.emitting,"bursts":bursts.get_child_count(),"born":born,"paused":get_tree().paused,"checkpoint":main.checkpoint_name}
func capture(name):
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	var path := OUT.path_join(name+".png")
	img.save_png(path)
	var s = state()
	s["image"] = name+".png"
	s["width"] = img.get_width()
	s["height"] = img.get_height()
	snapshots.append(s)
	FileAccess.open(OUT.path_join("snapshots.json"),FileAccess.WRITE).store_string(JSON.stringify(snapshots,"\t"))
	print("CAPTURE ",JSON.stringify(s))
func place(x,y=840.0):
	release_all()
	rudy.position = Vector2(x,y)
	rudy.velocity = Vector2.ZERO
	main.get_node("Camera").position.x = x
	main.get_node("Camera").reset_smoothing()
	await frames(3)
func until(condition: Callable, seconds=3.0):
	var end := Time.get_ticks_msec()+int(seconds*1000)
	while not condition.call() and Time.get_ticks_msec()<end: await get_tree().physics_frame
	if not condition.call(): print("CONDITION_TIMEOUT ",phase," ",JSON.stringify(state()))
func f9():
	var e := InputEventKey.new()
	e.keycode = KEY_F9
	e.pressed = true
	Input.parse_input_event(e)
	await get_tree().process_frame
	e = InputEventKey.new()
	e.keycode = KEY_F9
	e.pressed = false
	Input.parse_input_event(e)
	await get_tree().process_frame
func measure(name):
	release_all()
	await wait_s(1.0)
	set_phase(name)
	measuring = true
	phase_tick=0
	await wait_s(1.5)
	samples=[]
	frame_count=0
	measured_ticks=0
	peak_frames=0
	emitting_ticks=0
	max_bursts=0
	var start := Time.get_ticks_usec()
	await wait_s(5.0)
	var elapsed := (Time.get_ticks_usec()-start)/1e6
	measuring=false
	release_all()
	var result={"phase":name,"elapsed_s":elapsed,"frames":frame_count,"counted_fps":frame_count/elapsed,"max_bursts":max_bursts,"ticks":measured_ticks,"two_burst_ticks":peak_frames,"dust_emitting_ticks":emitting_ticks,"samples":samples}
	results.append(result)
	FileAccess.open(OUT.path_join("performance.json"),FileAccess.WRITE).store_string(JSON.stringify(results,"\t"))
	print("MEASUREMENT ",name," fps ",frame_count/elapsed," max_bursts ",max_bursts)
	await capture(name)

func run():
	var scene = load("res://app/main.tscn").instantiate()
	get_tree().root.add_child(scene)
	get_tree().current_scene = scene
	bind_main()
	RenderingServer.viewport_set_measure_render_time(get_viewport().get_viewport_rid(),true)
	print("ENV ",Engine.get_version_info()," renderer=",RenderingServer.get_current_rendering_method()," gpu=",RenderingServer.get_video_adapter_name()," screen_hz=",DisplayServer.screen_get_refresh_rate()," window=",DisplayServer.window_get_size())
	set_phase("title")
	await capture("10_title_first")
	await wait_s(1.0)
	await capture("11_title_settled")
	await tap("restart")
	if main.state != 1:
		printerr("FAILED_TO_START_PLAY")
		get_tree().quit(1)
		return
	await capture("12_play_first")
	await wait_s(1.2)
	await capture("13_play_idle")
	set_phase("pickup")
	await place(2320)
	Input.action_press("move_right")
	await until(func(): return rudy.gear == 1)
	release_all()
	await wait_s(0.8)
	if rudy.gear != 1:
		printerr("FAILED_TO_ACQUIRE_SWORD")
		get_tree().quit(1)
		return
	await place(2750)
	await wait_s(1.0)
	await f9()
	print("VSYNC_OFF_MODE ",DisplayServer.window_get_vsync_mode())
	await measure("01_A_off")
	await measure("02_A_heavy")
	await measure("03_B_off")
	await measure("04_B_heavy")
	await f9()
	print("VSYNC_RESTORED_MODE ",DisplayServer.window_get_vsync_mode())
	set_phase("rapid_slash")
	await place(2750)
	await wait_s(0.8)
	await tap("move_right")
	await tap("slash")
	await wait_s(0.05)
	await capture("20_slash_first")
	await until(func(): return not rudy.is_slashing())
	await tap("slash")
	await wait_s(0.03)
	await capture("21_slash_overlap")
	await wait_s(0.6)
	set_phase("left_slash")
	await tap("move_left")
	await tap("slash")
	await wait_s(0.09)
	await capture("22_left_slash")
	await wait_s(0.6)
	set_phase("goblin")
	var goblin=main.get_node("Level1/Enemies/GoblinB")
	await tap("move_right")
	await place(goblin.position.x-70)
	await tap("slash")
	await wait_s(0.09)
	await capture("23_goblin_slash")
	print("GOBLIN_DEAD ",goblin.dead," SPARKS_ALIVE ",bursts.get_child_count())
	await wait_s(0.7)
	set_phase("dust_run_stop_jump")
	await place(3600)
	Input.action_press("move_right")
	await wait_s(0.5)
	await capture("30_dust_running")
	Input.action_release("move_right")
	await wait_s(0.12)
	await capture("31_dust_stopping")
	await wait_s(0.5)
	await capture("32_dust_stopped")
	Input.action_press("move_left")
	await wait_s(0.3)
	await tap("jump")
	await wait_s(0.3)
	await tap("slash")
	await wait_s(0.04)
	await capture("33_sky_apex")
	await until(func(): return rudy.is_on_floor())
	await wait_s(0.12)
	await capture("34_dust_landing")
	release_all()
	await wait_s(0.8)
	set_phase("pit_jump")
	await place(4190)
	Input.action_press("move_right")
	await wait_s(0.15)
	await tap("jump")
	await until(func(): return rudy.position.x>4370)
	await tap("slash")
	await wait_s(0.06)
	await capture("35_over_pit")
	await until(func(): return rudy.is_on_floor(),2.0)
	release_all()
	await wait_s(0.7)
	set_phase("edges")
	await place(300)
	await tap("move_left")
	await tap("slash")
	await wait_s(0.08)
	await capture("40_left_start")
	await wait_s(0.6)
	await place(70)
	await tap("slash")
	await wait_s(0.05)
	await capture("41_left_clip_early")
	await wait_s(0.12)
	await capture("42_left_clip_late")
	await wait_s(0.5)
	Input.action_press("move_right")
	await wait_s(0.35)
	await capture("43_left_dust")
	release_all()
	await wait_s(0.6)
	await place(7080)
	await tap("move_right")
	await tap("slash")
	await wait_s(0.06)
	await capture("44_right_before_portal_early")
	await wait_s(0.15)
	await capture("45_right_before_portal_late")
	await wait_s(0.6)
	set_phase("pause_dust")
	await place(3650)
	Input.action_press("move_right")
	await wait_s(0.5)
	await tap("pause")
	await wait_s(0.1)
	await capture("50_dust_paused_a")
	await wait_s(0.6)
	await capture("51_dust_paused_b")
	release_all()
	await tap("pause")
	await wait_s(0.15)
	await capture("52_dust_resumed")
	await wait_s(0.6)
	set_phase("pause_sparks")
	await tap("slash")
	await wait_s(0.04)
	await tap("pause")
	await wait_s(0.1)
	await capture("53_sparks_paused_a")
	await wait_s(0.6)
	await capture("54_sparks_paused_b")
	await tap("pause")
	await wait_s(0.1)
	await capture("55_sparks_resumed")
	await wait_s(0.8)
	set_phase("hurt_running")
	await place(985)
	Input.action_press("move_right")
	await until(func(): return rudy.is_invulnerable())
	await until(func(): return rudy.mode == 1 and rudy.is_on_floor())
	for i in 4:
		await wait_s(0.07)
		await capture("60_hurt_run_"+str(i))
	release_all()
	await wait_s(1.5)
	set_phase("respawn")
	await place(3940)
	Input.action_press("move_right")
	await until(func(): return main.checkpoint_name=="waystone")
	await until(func(): return rudy.position.x>4315)
	await capture("64_fall_start")
	await until(func(): return rudy.mode==4)
	await until(func(): return rudy.mode==5)
	await capture("65_respawn_first")
	await until(func(): return rudy.mode==1)
	await wait_s(0.15)
	await capture("66_respawn_running")
	release_all()
	await wait_s(0.8)
	set_phase("complete_restart")
	await place(7100)
	Input.action_press("move_right")
	await until(func(): return main.state==3)
	release_all()
	await wait_s(2.7)
	await capture("70_complete")
	var old_main=main
	await tap("restart")
	await until(func(): return get_tree().current_scene != old_main)
	bind_main()
	await capture("71_restart_first")
	await wait_s(1.0)
	await capture("72_restart_settled")
	set_phase("done")
	print("USE_IT_DONE")
	FileAccess.open(OUT.path_join("done.txt"),FileAccess.WRITE).store_string("complete\n")
	get_tree().quit()
