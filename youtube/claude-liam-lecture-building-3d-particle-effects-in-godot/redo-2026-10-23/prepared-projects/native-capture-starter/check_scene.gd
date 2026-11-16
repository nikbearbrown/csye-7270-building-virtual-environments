extends SceneTree
var checks=[]
func check(label:String,passed:bool,details=""):
 checks.append(passed);print(JSON.stringify({"check":label,"pass":passed,"details":details}))
func _initialize():call_deferred("run")
func run():
 var stage=load("res://arena.tscn").instantiate();root.add_child(stage);current_scene=stage
 await process_frame
 var source=stage.get_node_or_null("Particles");var smoke=stage.get_node_or_null("Smoke")
 check("mesh-draw-present",source!=null and source.draw_pass_1 is SphereMesh)
 check("smoke-draw-present",smoke!=null and smoke.draw_pass_1 is QuadMesh)
 if source==null or smoke==null:quit(1);return
 check("independent-behavior",source.process_material!=smoke.process_material)
 check("particle-billboard",smoke.draw_pass_1.material.billboard_mode==BaseMaterial3D.BILLBOARD_PARTICLES)
 check("vertex-color-connected",source.draw_pass_1.material.vertex_color_use_as_albedo)
 check("alpha-enabled",source.draw_pass_1.material.transparency==BaseMaterial3D.TRANSPARENCY_ALPHA)
 source.visibility_aabb=AABB(Vector3(-20,-30,-20),Vector3(40,60,40))
 source.process_material.collision_mode=ParticleProcessMaterial.COLLISION_DISABLED
 source.restart();await create_timer(3).timeout
 var without=source.capture_aabb()
 source.process_material.collision_mode=ParticleProcessMaterial.COLLISION_RIGID
 source.restart();await create_timer(3).timeout
 var with_collision=source.capture_aabb()
 print("COLLISION_BOUNDS ",JSON.stringify({"off":str(without),"on":str(with_collision),"renderer":RenderingServer.get_current_rendering_method()}))
 if without.size.length()>0 and with_collision.size.length()>0:
  check("collision-reduces-floor-penetration",with_collision.position.y>without.position.y+1,{"off_y":without.position.y,"on_y":with_collision.position.y})
 else:print("INSTRUMENT_LIMIT capture_aabb did not return usable current particle bounds; native motion inspection required")
 print("RESULT ",checks.size()," checks / ",checks.count(false)," failures")
 quit(0 if checks.count(false)==0 else 1)
