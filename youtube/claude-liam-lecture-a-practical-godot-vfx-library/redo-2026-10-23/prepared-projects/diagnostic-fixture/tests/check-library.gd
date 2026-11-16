extends SceneTree
var checks:Array[Dictionary]=[]
func check(id,ok,details=""):
 checks.append({"id":id,"pass":ok,"details":details});print(JSON.stringify(checks.back()))
func _initialize():call_deferred("run")
func run():
 var stage=load("res://arena.tscn").instantiate();root.add_child(stage);current_scene=stage
 for group in ["Explosion","Campfire","Rain","Magic"]:
  var scene=load("res://effects/"+group.to_snake_case()+".tscn").instantiate();scene.preview_loop=false;scene.auto_free=true;root.add_child(scene);scene.play()
  check(group+"-children-packed",scene.get_child_count()>=3,scene.get_child_count())
  scene.queue_free()
 await process_frame
 var rain=load("res://effects/rain.tscn").instantiate();rain.preview_loop=false;stage.add_child(rain)
 var drop=rain.get_node("Drops");var splash=rain.get_node("Splash")
 check("sub-emitter-target",drop.get_node(drop.sub_emitter)==splash)
 check("child-not-independently-emitting",not splash.emitting and splash.get_meta("sub_emitter_only",false))
 check("bounded-splash-capacity",splash.amount==64 and is_equal_approx(splash.lifetime,.35))
 drop.process_material.sub_emitter_mode=0;rain.play();await create_timer(2).timeout
 var off=splash.capture_aabb()
 drop.process_material.sub_emitter_mode=3;rain.play();await create_timer(2).timeout
 var on=splash.capture_aabb()
 print("RAIN_BOUNDS ",JSON.stringify({"off":str(off),"on":str(on),"sub_emitter_mode":drop.process_material.sub_emitter_mode,"renderer":RenderingServer.get_current_rendering_method()}))
 check("contact-creates-spatial-splashes",on.size.x>off.size.x+1 and on.size.z>off.size.z+1 and on.position.y>-.5,{"off":str(off),"on":str(on)})
 rain.queue_free();await process_frame
 var total:=0
 for i in range(3):
  var effect=load("res://effects/explosion.tscn").instantiate();effect.preview_loop=false;effect.auto_free=true;stage.add_child(effect);effect.play();total+=1
 await create_timer(3).timeout
 var active=0
 for c in stage.get_children():
  if c.get_script()==load("res://effect.gd") and c.auto_free:active+=1
 check("three-layered-instances-dispose",total==3 and active==0,active)
 var failures=checks.filter(func(c):return not c.pass).size()
 print("RESULT ",checks.size()," checks / ",failures," failures; visual review still pending")
 stage.queue_free();await process_frame;await create_timer(.5).timeout;quit(1 if failures else 0)
