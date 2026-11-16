extends SceneTree
func _initialize():
 for name in ["burst","ambient"]:
  var effect=load("res://baseline-effects/"+name+".tscn").instantiate()
  effect.use_fixed_seed=true;effect.seed=7270;effect.color=Color.WHITE
  var ramp=Gradient.new();var tint=Color("e8794e") if name=="burst" else Color("56cce2")
  ramp.set_color(0,Color(tint,.25));ramp.set_color(1,Color(tint,0));ramp.add_point(.2,Color(tint,1));ramp.add_point(.65,Color(tint,.8));effect.color_ramp=ramp
  var curve=Curve.new();curve.add_point(Vector2(0,.25));curve.add_point(Vector2(.2,1));curve.add_point(Vector2(1,.05));effect.scale_amount_curve=curve
  effect.mesh=effect.mesh.duplicate(false);effect.mesh.material=effect.mesh.material.duplicate(false);effect.mesh.material.transparency=BaseMaterial3D.TRANSPARENCY_ALPHA
  effect.mesh.radius=.055 if name=="burst" else .032;effect.mesh.height=effect.mesh.radius*2
  if name=="ambient":effect.preprocess=2
  var packed=PackedScene.new();packed.pack(effect);ResourceSaver.save(packed,"res://effects/"+name+".tscn")
  ResourceSaver.save(ramp,"res://effects/"+name+"-ramp.tres");ResourceSaver.save(curve,"res://effects/"+name+"-scale.tres");effect.free()
 print("Proposed separate tuning resources saved; visual revision approval pending")
 quit()
