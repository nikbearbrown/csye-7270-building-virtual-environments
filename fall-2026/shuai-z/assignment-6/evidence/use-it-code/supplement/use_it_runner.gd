extends Node
# Instrumentation only. The source game is copied unchanged; fixtures place Rudy
# near each case, then use real Input actions and the existing effect driver.
const OUT := "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-6/evidence/use-it-code/supplement"
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
	await wait_s(1.0)
	await tap("restart")
	await wait_s(0.6)
	await place(2320)
	Input.action_press("move_right")
	await until(func(): return rudy.gear == 1)
	release_all()
	await wait_s(0.8)
	if rudy.gear != 1:
		printerr("FAILED_TO_ACQUIRE_SWORD")
		get_tree().quit(1)
		return
	set_phase("supplement_pause")
	await place(2750)
	await tap("slash")
	await wait_s(0.14)
	await tap("pause")
	await capture("80_sparks_visible_paused_a")
	await wait_s(0.7)
	await capture("81_sparks_visible_paused_b")
	await tap("pause")
	await wait_s(0.07)
	await capture("82_sparks_resumed")
	await wait_s(0.6)
	set_phase("supplement_sky")
	await tap("jump")
	await wait_s(0.22)
	await tap("slash")
	await wait_s(0.14)
	await capture("83_sky_visible")
	await until(func(): return rudy.is_on_floor())
	await wait_s(0.7)
	set_phase("supplement_goblin")
	var goblin=main.get_node("Level1/Enemies/GoblinB")
	await tap("move_right")
	await place(goblin.position.x-70)
	await tap("slash")
	await until(func(): return not goblin.visible,1.0)
	await capture("84_goblin_hidden_sparks")
	print("GOBLIN_HIDDEN ",not goblin.visible," BURSTS ",bursts.get_child_count())
	await wait_s(0.7)
	set_phase("supplement_right_edge")
	await place(6860)
	Input.action_press("move_right")
	await until(func(): return rudy.position.x>=6960)
	await tap("jump")
	await until(func(): return rudy.position.x>7380)
	await until(func(): return rudy.is_on_floor())
	await until(func(): return rudy.position.x>7620)
	await capture("85_right_edge_dust")
	release_all()
	await wait_s(0.3)
	print("RIGHT_EDGE_MAIN_STATE ",main.state," X ",rudy.position.x)
	await tap("slash")
	await wait_s(0.12)
	await capture("86_right_edge_sparks_early")
	await wait_s(0.12)
	await capture("87_right_edge_sparks_late")
	await wait_s(0.6)
	set_phase("supplement_dark_pit")
	await place(4190)
	Input.action_press("move_right")
	await until(func(): return rudy.position.y>950)
	await tap("slash")
	await wait_s(0.1)
	await capture("88_dark_pit_sparks")
	release_all()
	set_phase("done")
	print("SUPPLEMENT_DONE")
	get_tree().quit()
