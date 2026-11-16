extends SceneTree
func _initialize():call_deferred("build")
func build():
	DirAccess.make_dir_recursive_absolute("res://assets");DirAccess.make_dir_recursive_absolute("res://effects")
	var gradient=Gradient.new();gradient.set_color(0,Color.WHITE);gradient.set_color(1,Color(1,1,1,0))
	var texture=GradientTexture2D.new();texture.gradient=gradient;texture.width=32;texture.height=32;texture.fill=GradientTexture2D.FILL_RADIAL;texture.fill_from=Vector2(.5,.5);texture.fill_to=Vector2(1,.5)
	ResourceSaver.save(texture,"res://assets/soft-dot.tres")
	var size=Curve.new();size.add_point(Vector2(0,.2));size.add_point(Vector2(.12,1));size.add_point(Vector2(1,.02))
	var curve=CurveTexture.new();curve.curve=size;ResourceSaver.save(curve,"res://assets/size-over-life.tres")
	var fade=Gradient.new();fade.set_color(0,Color("fff3ac"));fade.set_color(1,Color(0.95,.3,.1,0));fade.add_point(.3,Color("ff8e39"))
	var ramp=GradientTexture1D.new();ramp.gradient=fade;ResourceSaver.save(ramp,"res://assets/color-over-life.tres")
	var mat=ParticleProcessMaterial.new();mat.particle_flag_disable_z=true;mat.direction=Vector3(0,-1,0);mat.spread=180;mat.gravity=Vector3(0,140,0);mat.initial_velocity_min=100;mat.initial_velocity_max=220;mat.scale_min=.4;mat.scale_max=.8;mat.scale_curve=curve;mat.color_ramp=ramp
	var burst=GPUParticles2D.new();burst.name="PickupBurst";burst.amount=48;burst.lifetime=.8;burst.one_shot=true;burst.explosiveness=1;burst.emitting=false;burst.texture=texture;burst.process_material=mat;burst.visibility_rect=Rect2(-400,-400,800,800);burst.use_fixed_seed=true;burst.seed=7270;burst.local_coords=false
	var scene=PackedScene.new();scene.pack(burst);ResourceSaver.save(scene,"res://effects/pickup_burst.tscn");burst.free()
	print("ASSETS_WRITTEN: original procedural dot, size curve, alpha ramp, reusable one-shot scene")
	quit()
