extends SceneTree
func _initialize():call_deferred("run")
func run():
 root.size=Vector2i(1280,720);root.content_scale_size=Vector2i(1280,720)
 DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
 var rid=root.get_viewport_rid();RenderingServer.viewport_set_measure_render_time(rid,true)
 for mode in ["off","burst-loop-upper-bound","ambient","both"]:
  var game=load("res://main.tscn").instantiate();game.audio_enabled=false;root.add_child(game);current_scene=game
  game.set_physics_process(false);game.set_process(false);game.sound.stop_all()
  game.burst.one_shot=false;game.burst.position=Vector3(-2,.4,0);game.burst.preprocess=game.burst.lifetime;game.ambient.preprocess=game.ambient.lifetime
  game.burst.visible=mode in ["burst-loop-upper-bound","both"];game.burst.emitting=game.burst.visible
  game.ambient.visible=mode in ["ambient","both"];game.ambient.emitting=game.ambient.visible
  for repeat in range(3):
   for i in range(60):await process_frame
   var cpu:Array[float]=[];var gpu:Array[float]=[];var draws:Array[float]=[]
   for i in range(300):
    await process_frame
    cpu.append(RenderingServer.viewport_get_measured_render_time_cpu(rid)+RenderingServer.get_frame_setup_time_cpu())
    gpu.append(RenderingServer.viewport_get_measured_render_time_gpu(rid))
    draws.append(RenderingServer.viewport_get_render_info(rid,RenderingServer.VIEWPORT_RENDER_INFO_TYPE_VISIBLE,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
   var c:=0.0;var g:=0.0;var d:=0.0
   for n in cpu:c+=n
   for n in gpu:g+=n
   for n in draws:d+=n
   print("RENDER,"+JSON.stringify({"mode":mode,"repeat":repeat,"warmup":60,"frames":300,"render_cpu_ms":c/300,"render_gpu_ms":g/300 if g>0 else null,"gpu_timer_available":g>0,"draw_calls":d/300,"cpu_min_ms":cpu.min(),"cpu_max_ms":cpu.max(),"window_pixels":str(root.get_texture().get_size()),"adapter":RenderingServer.get_video_adapter_name(),"renderer":RenderingServer.get_current_rendering_method(),"instrument":"RenderingServer viewport timers plus frame setup; unavailable GPU stays null; physics disabled; fixed 60-Hz simulation; loop workloads pre-rolled to steady state"}))
  game.queue_free();await process_frame;await process_frame
 quit()
