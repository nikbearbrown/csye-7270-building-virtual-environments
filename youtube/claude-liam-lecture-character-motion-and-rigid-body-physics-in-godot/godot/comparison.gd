extends Node2D
const L = preload("res://layers.gd")
var checks: Array = []
var measurements := {}
var view: SubViewport
var stage: Node2D
var text_layer: CanvasLayer
var root_path := ProjectSettings.globalize_path("res://../")
var trajectory: Array = []
func label(text: String, at: Vector2, size := 30) -> Label:
    var l := Label.new()
    l.text = text
    l.position = at
    l.add_theme_color_override("font_color", Color("3d3929"))
    l.add_theme_font_size_override("font_size", size)
    text_layer.add_child(l)
    return l
func check(name: String, passed: bool, actual: Variant) -> void:
    checks.append({"name":name,"passed":passed,"actual":actual})
    print(("PASS " if passed else "FAIL ") + name + " = " + str(actual))
func fresh(title: String) -> void:
    if stage:
        stage.queue_free()
        text_layer.queue_free()
        await get_tree().process_frame
    stage = Node2D.new()
    view.add_child(stage)
    text_layer = CanvasLayer.new()
    view.add_child(text_layer)
    text_layer.transform = Transform2D.IDENTITY.scaled(Vector2(3,3))
    label(title, Vector2(60,40), 42)
    label("Godot evidence lab | scripted setup, real physics",Vector2(60,660),24)
func shape(body: CollisionObject2D, size: Vector2, color: Color) -> void:
    var s := CollisionShape2D.new()
    var r := RectangleShape2D.new()
    r.size = size
    s.shape = r
    body.add_child(s)
    var v := Polygon2D.new()
    v.polygon = PackedVector2Array([-size/2, Vector2(size.x,-size.y)/2, size/2, Vector2(-size.x,size.y)/2])
    v.color = color
    body.add_child(v)
func floor_body(at: Vector2, size: Vector2) -> StaticBody2D:
    var b := StaticBody2D.new()
    b.position=at
    b.collision_layer=L.bit(L.WORLD)
    b.collision_mask=0
    shape(b,size,Color("3d3929"))
    stage.add_child(b)
    return b
func ticks(n: int) -> void:
    for i in n:
        await get_tree().physics_frame
func snap(name: String) -> void:
    if DisplayServer.get_name() != "headless":
        await RenderingServer.frame_post_draw
        var im := view.get_texture().get_image()
        im.save_png(root_path + "captures/" + name + ".png")
func walker(at: Vector2) -> CharacterBody2D:
    var p := CharacterBody2D.new()
    p.position = at
    p.collision_layer = 4
    p.collision_mask = 1
    shape(p, Vector2(32,48), Color("d97757"))
    stage.add_child(p)
    return p
func _ready() -> void:
    view = SubViewport.new()
    view.size = Vector2i(3840,2160)
    view.world_2d = World2D.new()
    view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    add_child(view)
    view.canvas_transform = Transform2D.IDENTITY.scaled(Vector2(3,3))
    var screen := Sprite2D.new()
    screen.texture = view.get_texture()
    screen.centered = false
    screen.scale = Vector2(1.0/3,1.0/3)
    add_child(screen)
    print("ENGINE " + Engine.get_version_info().string)
    await fresh("Same shape. Different responsibility.")
    var wall := floor_body(Vector2(600,260), Vector2(120,130))
    var sensor := Area2D.new()
    sensor.position = Vector2(600,500)
    sensor.collision_layer = 16
    sensor.collision_mask = 4
    shape(sensor, Vector2(120,130), Color(0.85,0.47,0.34,0.25))
    stage.add_child(sensor)
    var upper := walker(Vector2(180,260))
    var lower := walker(Vector2(180,500))
    var events := [0,0]
    sensor.body_entered.connect(func(_p): events[0] += 1)
    sensor.body_exited.connect(func(_p): events[1] += 1)
    label("StaticBody2D: blocks the moving body", Vector2(60,130),32)
    label("Area2D: reports overlap, allows passage", Vector2(60,370),32)
    var status := label("Enter: 0 | Exit: 0",Vector2(900,480),30)
    await ticks(3)
    await snap("comparison-before")
    for i in 110:
        await get_tree().physics_frame
        upper.move_and_collide(Vector2(6,0))
        lower.move_and_collide(Vector2(6,0))
        status.text = "Enter: %d | Exit: %d" % [events[0], events[1]]
        trajectory.append({"tick":i,"solid_x":upper.position.x,"area_x":lower.position.x,"entered":events[0],"exited":events[1]})
        if i == 69:
            await snap("comparison-overlap")
    await ticks(4)
    status.text = "Enter: %d | Exit: %d" % [events[0], events[1]]
    check("solid blocks",upper.position.x < 525,upper.position.x)
    check("area permits passage",lower.position.x > 800,lower.position.x)
    check("one enter and one exit",events == [1,1],events.duplicate())
    check("same rectangle geometry",wall.get_child(0).shape.size == sensor.get_child(0).shape.size,Vector2(120,130))
    await snap("comparison-after")
    var entry_count: int = events[0]
    sensor.monitoring = false
    lower.position = sensor.position
    await ticks(5)
    check("monitoring false suppresses body detection",events[0] == entry_count,events[0]-entry_count)
    sensor.monitoring = true
    await ticks(5)
    check("monitoring true detects body",sensor.get_overlapping_bodies().has(lower),sensor.get_overlapping_bodies().size())
    sensor.collision_mask = 0
    await ticks(5)
    check("mask zero suppresses detection",sensor.get_overlapping_bodies().is_empty(),sensor.get_overlapping_bodies().size())
    var target := Area2D.new()
    target.position = Vector2(950,260)
    target.collision_layer = 8
    target.collision_mask = 0
    target.monitorable = false
    shape(target,Vector2(60,60),Color("8b8f96"))
    stage.add_child(target)
    sensor.position = target.position
    sensor.collision_mask = 8
    await ticks(5)
    check("monitorable false hides target from another area",sensor.get_overlapping_areas().is_empty(),sensor.get_overlapping_areas().size())
    target.monitorable = true
    target.position.x += 300
    await ticks(5)
    target.position = sensor.position
    await ticks(5)
    check("monitorable true exposes target to another area",sensor.get_overlapping_areas().has(target),sensor.get_overlapping_areas().size())
    await fresh("One door scene: solid panel + approach sensor")
    var packed := load("res://door.tscn") as PackedScene
    var door := packed.instantiate()
    var other := packed.instantiate()
    door.position = Vector2(600,380)
    other.position = Vector2(1000,380)
    other.locked = false
    stage.add_child(door)
    stage.add_child(other)
    var p := walker(Vector2(350,380))
    var requests := [0]
    door.approach_requested.connect(func(_actor): requests[0] += 1)
    var door_heading := label("Door A: locked | Door B: instance override",Vector2(60,140),32)
    var door_status := label("Sensor stays active when the panel opens",Vector2(60,570),30)
    await ticks(3)
    for i in 50:
        await get_tree().physics_frame
        p.move_and_collide(Vector2(6,0))
    await ticks(3)
    check("closed door blocks",p.position.x < 565,p.position.x)
    check("approach signal reaches parent",requests[0] == 1,requests[0])
    check("instance export overrides independent",door.locked and not other.locked,[door.locked,other.locked])
    check("door occupancy tracks body",door.occupants.size() == 1,door.occupants.size())
    door.open()
    check("locked door refuses open",not door.is_open,not door.is_open)
    await snap("door-closed")
    door.locked = false
    door.open()
    await ticks(3)
    check("opening disables solid only",door.solid.disabled and door.sensor.monitoring,[door.solid.disabled,door.sensor.monitoring])
    check("other instance remains closed",not other.is_open,not other.is_open)
    check("occupied door refuses closure",not door.close_when_clear(),door.occupants.size())
    door_heading.text = "Door A: unlocked and open | Door B: closed"
    door_status.text = "Door A open | sensor still monitoring | one occupant"
    await snap("door-open")
    for i in 40:
        await get_tree().physics_frame
        p.move_and_collide(Vector2(6,0))
    await ticks(5)
    check("actor crosses open door",p.position.x > 760,p.position.x)
    check("exit clears occupancy",door.occupants.is_empty(),door.occupants.size())
    check("empty door can close",door.close_when_clear(),not door.is_open)
    await ticks(3)
    check("closed shape restored",not door.solid.disabled,not door.solid.disabled)
    var data := {"engine":Engine.get_version_info().string,"checks":checks,"trajectory":trajectory,"limits":"Scripted single actor, axis-aligned geometry. No network or simultaneous-entry race proof."}
    var f := FileAccess.open(root_path + "evidence/comparison-results.json", FileAccess.WRITE)
    f.store_string(JSON.stringify(data,"  "))
    var failed := checks.filter(func(c): return not c.passed).size()
    print("CHECKS %d | FAILED %d" % [checks.size(),failed])
    get_tree().quit(1 if failed else 0)
