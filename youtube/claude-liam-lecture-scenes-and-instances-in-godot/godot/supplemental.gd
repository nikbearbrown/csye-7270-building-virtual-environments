extends SceneTree
var checks: Array = []
func check(n: String, ok: bool, value: Variant) -> void:
    checks.append({"name":n,"passed":ok,"actual":str(value)})
    print(("PASS " if ok else "FAIL ")+n+" = "+str(value))
func _initialize() -> void:
    run.call_deferred()
func run() -> void:
    var shape := RectangleShape2D.new()
    shape.size = Vector2(20,20)
    var left := CollisionShape2D.new()
    var right := CollisionShape2D.new()
    left.shape = shape
    right.shape = shape
    left.shape.size = Vector2(40,20)
    check("shared resize propagates",right.shape.size.x==40,right.shape.size)
    right.shape = right.shape.duplicate()
    right.shape.size = Vector2(10,20)
    check("duplicate isolates resize",left.shape.size.x==40,left.shape.size)
    left.free();right.free()
    var p := CharacterBody2D.new()
    p.set_script(load("res://player.gd"));root.add_child(p)
    p.coyote=0.05
    p.step(1.0/60,0,true,false)
    check("coyote grants airborne jump",p.velocity.y < -300,p.velocity)
    check("jump consumes windows",p.coyote==0 and p.buffer==0,[p.coyote,p.buffer])
    p.velocity=Vector2.ZERO
    p.step(1.0/60,0,true,false)
    check("air press buffers without jumping",p.buffer>0 and p.velocity.y>0,[p.buffer,p.velocity.y])
    p.velocity.y=-100
    p.step(1.0/60,0,false,true)
    check("release cuts upward velocity",p.velocity.y<0 and p.velocity.y>-50,p.velocity.y)
    var enemy:=CharacterBody2D.new()
    enemy.set_script(load("res://enemy.gd"))
    for n in ["Top","Side"]:
        var a:=Area2D.new();a.name=n;enemy.add_child(a)
    root.add_child(enemy)
    var deaths:=[0]
    enemy.defeated.connect(func():deaths[0]+=1)
    p.velocity.y=100
    enemy.on_top(p);enemy.on_top(p)
    check("enemy defeated once",deaths[0]==1,deaths[0])
    check("stomp bounce points upward",p.velocity.y<0,p.velocity.y)
    var platform:=AnimatableBody2D.new()
    platform.set_script(load("res://platform.gd"));root.add_child(platform)
    var start:=platform.position.x
    for i in 30:await physics_frame
    check("platform advances on physics ticks",platform.position.x-start>25,platform.position.x-start)
    var debris:=Node2D.new();debris.set_script(load("res://debris.gd"));root.add_child(debris)
    debris.shatter(Vector2(300,300))
    for i in 3:await physics_frame
    check("deferred debris creates four bodies",debris.get_child_count()==4,debris.get_child_count())
    check("debris impulse is applied",debris.get_child(0).linear_velocity.x<0,debris.get_child(0).linear_velocity)
    var file:=FileAccess.open(ProjectSettings.globalize_path("res://../evidence/supplemental-results.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(checks,"  "));file.close()
    var bad:=checks.filter(func(c):return not c.passed).size()
    print("RESULT "+str(checks.size())+" checks, "+str(bad)+" failed")
    quit(1 if bad else 0)
