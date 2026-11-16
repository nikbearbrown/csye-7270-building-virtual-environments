extends SceneTree
func _initialize():
 var dot=GradientTexture2D.new();dot.width=96;dot.height=96;dot.fill=GradientTexture2D.FILL_RADIAL;dot.fill_from=Vector2(.5,.5);dot.fill_to=Vector2(1,.5)
 var gradient=Gradient.new();gradient.set_color(0,Color.WHITE);gradient.set_color(1,Color(1,1,1,0));gradient.add_point(.4,Color(1,1,1,.6));dot.gradient=gradient
 ResourceSaver.save(dot,"res://assets/soft-dot.tres")
 var ramp=GradientTexture1D.new();ramp.gradient=Gradient.new();ramp.gradient.set_color(0,Color(1,.9,.5,1));ramp.gradient.set_color(1,Color(.9,.22,.04,0));ramp.gradient.add_point(.3,Color(1,.45,.07,1));ResourceSaver.save(ramp,"res://assets/hot-fade.tres")
 var smoke=GradientTexture1D.new();smoke.gradient=Gradient.new();smoke.gradient.set_color(0,Color(.6,.67,.75,.1));smoke.gradient.set_color(1,Color(.35,.4,.48,0));smoke.gradient.add_point(.2,Color(.7,.74,.8,.55));ResourceSaver.save(smoke,"res://assets/smoke-fade.tres")
 var curve=CurveTexture.new();curve.curve=Curve.new();curve.curve.add_point(Vector2(0,.2));curve.curve.add_point(Vector2(.3,.6));curve.curve.add_point(Vector2(1,1));ResourceSaver.save(curve,"res://assets/grow.tres")
 print("Original procedural particle resources saved");quit()
