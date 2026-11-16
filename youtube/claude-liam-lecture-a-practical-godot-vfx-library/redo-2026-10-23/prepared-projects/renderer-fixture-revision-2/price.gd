extends SceneTree
func _initialize():call_deferred("run")
func run():
 root.size=Vector2i(1280,720);DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
 var rid=root.get_viewport_rid();RenderingServer.viewport_set_measure_render_time(rid,true)
 for mode in ["off","explosion","campfire","both"]:
  var stage=load("res://arena.tscn").instantiate();root.add_child(stage);current_scene=stage;stage.set_process(false)
  for name in ["Explosion","Campfire","Rain","Magic"]:
   var effect=stage.get_node(name);effect.stop();stage.remove_child(effect);effect.queue_free()
  for name in (["Explosion","Campfire"] if mode=="both" else ([mode.capitalize()] if mode!="off" else [])):
   var effect=load("res://effects/"+name.to_snake_case()+".tscn").instantiate();stage.add_child(effect);effect.preview_loop=true;effect.play()
  for repeat in range(3):
   for i in range(60):await process_frame
   var cpu:=0.0;var gpu:=0.0;var draws:=0.0
   for i in range(300):
    await process_frame
    cpu+=RenderingServer.viewport_get_measured_render_time_cpu(rid)+RenderingServer.get_frame_setup_time_cpu()
    gpu+=RenderingServer.viewport_get_measured_render_time_gpu(rid)
    draws+=RenderingServer.viewport_get_render_info(rid,RenderingServer.VIEWPORT_RENDER_INFO_TYPE_VISIBLE,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME)
   print("RENDER,"+JSON.stringify({"mode":mode,"repeat":repeat,"warmup":60,"frames":300,"render_cpu_ms":cpu/300,"render_gpu_ms":gpu/300 if gpu>0 else null,"gpu_timer_available":gpu>0,"draw_calls":draws/300,"adapter":RenderingServer.get_video_adapter_name(),"renderer":RenderingServer.get_current_rendering_method(),"window_pixels":str(root.get_texture().get_size()),"instrument":"Viewport timers plus frame setup; fixed 60 Hz simulation; normal labeled preview replay intervals; not interactive FPS"}))
  stage.queue_free();await process_frame;await process_frame
 quit()
