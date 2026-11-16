extends SceneTree
var failures := 0
func check(ok:bool, label:String) -> void:
	print("PASS " if ok else "FAIL ",label)
	if not ok:failures+=1
func _initialize() -> void:
	var lab=load("res://lesson.tscn").instantiate()
	root.add_child(lab);lab.set_process(false)
	lab.birth_rate=20;lab.lifetime=2;lab.cleanup=true;lab.reset()
	for i in 600:lab._process(1.0/60.0)
	check(lab.particles.size()>=38 and lab.particles.size()<=41,"Steady live population approximately rate times lifetime")
	lab.cleanup=false
	var before=lab.particles.size()
	for i in 180:lab._process(1.0/60.0)
	check(lab.particles.size()>before+55,"Seeded cleanup fault retains expired records")
	lab.cleanup=true;lab._process(1.0/60.0)
	check(lab.particles.size()<=41,"Restored cleanup removes expired entries")
	lab.birth_rate=0;lab.reset();lab.burst_size=40;lab.burst()
	check(lab.particles.size()==40,"Burst starts with forty records")
	for i in 121:lab._process(1.0/60.0)
	check(lab.particles.is_empty(),"Whole burst expires after its lifetime")
	lab.lifetime=2;lab.wind=120;lab.gravity=180;lab.spawn_one()
	var v=lab.particles[0].v
	lab._process(0.1)
	check(lab.particles[0].v.is_equal_approx(v+Vector2(12,18)),"Acceleration uses seconds")
	print("LIFECYCLE_CHECKS failures=",failures)
	quit(0 if failures==0 else 1)
