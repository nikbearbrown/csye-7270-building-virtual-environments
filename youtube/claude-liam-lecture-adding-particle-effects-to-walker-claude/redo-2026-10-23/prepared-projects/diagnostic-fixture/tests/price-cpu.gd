extends SceneTree
func _initialize():call_deferred("run")
func run():
 for mode in ["empty","burst-loop-upper-bound","ambient","both"]:
  var fixture=Node3D.new();root.add_child(fixture)
  if mode in ["burst-loop-upper-bound","both"]:
   var burst=load("res://effects/burst.tscn").instantiate();burst.one_shot=false;fixture.add_child(burst);burst.emitting=true
  if mode in ["ambient","both"]:
   var ambient=load("res://effects/ambient.tscn").instantiate();fixture.add_child(ambient);ambient.emitting=true
  for repeat in range(3):
   for i in range(60):await process_frame
   var samples:Array[float]=[];var previous=Time.get_ticks_usec()
   for i in range(300):
    await process_frame
    var now=Time.get_ticks_usec();samples.append((now-previous)/1000.0);previous=now
   samples.sort();var total:=0.0
   for item in samples:total+=item
   print("PRICE,"+JSON.stringify({"mode":mode,"repeat":repeat,"warmup":60,"frames":300,"mean_ms":total/300.0,"min_ms":samples[0],"configured_rendering_method":RenderingServer.get_current_rendering_method(),"video_adapter":RenderingServer.get_video_adapter_name(),"display_driver":DisplayServer.get_name(),"instrument":"Headless uses a dummy renderer: GPU simulation and drawing are not measured","p95_ms":samples[284],"max_ms":samples[-1],"gpu_measured":false,"scope":"Headless CPU wall time per fixed 60-Hz simulated frame, not interactive FPS","memory_bytes":Performance.get_monitor(Performance.MEMORY_STATIC)}))
  fixture.queue_free();await process_frame
 quit()
