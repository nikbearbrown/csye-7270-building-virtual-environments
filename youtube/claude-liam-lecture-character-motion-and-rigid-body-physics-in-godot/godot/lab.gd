extends Node2D
const L = preload("res://layers.gd")
const PLAYER = preload("res://player.gd")
const COIN = preload("res://coin.gd")
const HIT = preload("res://tile_hit.gd")
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
func player(at: Vector2) -> CharacterBody2D:
    var b := CharacterBody2D.new()
    b.set_script(PLAYER)
    b.position=at
    b.collision_layer=L.bit(L.PLAYER)
    b.collision_mask=L.bit(L.WORLD)|L.bit(L.ONE_WAY)
    shape(b,Vector2(32,48),Color("d97757"))
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
    measurements["engine"] = Engine.get_version_info().string
    measurements["display"] = DisplayServer.get_name()
    await fresh("Scenes: one definition, separate instances")
    var template := Node2D.new()
    template.name="Actor"
    var child := Node2D.new()
    child.name="Visual"
    child.position=Vector2(20,0)
    template.add_child(child)
    child.owner=template
    var packed := PackedScene.new()
    check("pack scene",packed.pack(template)==OK,"PackedScene")
    ResourceSaver.save(packed,"res://actor.tscn")
    template.free()
    var a := packed.instantiate() as Node2D
    var b := packed.instantiate() as Node2D
    stage.add_child(a); stage.add_child(b)
    a.position=Vector2(100,100);b.position=Vector2(300,100)
    check("independent instance transforms",a.position!=b.position,[str(a.position),str(b.position)])
    check("child transform inherits",a.get_node("Visual").global_position==Vector2(120,100),str(a.get_node("Visual").global_position))
    check("layer 3 bit",L.bit(3)==4,L.bit(3))
    var probe := CollisionShape2D.new()
    check("one way direction property",probe.get("one_way_collision_direction")==Vector2.DOWN,str(probe.get("one_way_collision_direction")))
    probe.free()
    await fresh("Coin detection: mask scans Player")
    var p := player(Vector2(420,350))
    var coin := Area2D.new()
    coin.set_script(COIN)
    coin.position=Vector2(420,350)
    coin.collision_layer=L.bit(L.PICKUP)
    coin.collision_mask=L.bit(L.PLAYER)
    shape(coin,Vector2(100,100),Color(0.85,0.47,0.34,0.35))
    stage.add_child(coin)
    var awards := [0]
    coin.collected.connect(func(v): awards[0]+=v)
    await ticks(5)
    check("area detects body without reciprocal mask",awards[0]==1,awards[0])
    coin._on_body_entered(p)
    check("coin latch prevents double award",awards[0]==1,awards[0])
    label("Coin: mask Player | Player: mask World + One Way",Vector2(60,140))
    label("Awards: " + str(awards[0]),Vector2(650,330),40)
    await snap("coin")
    var missed := [0]
    var off := Area2D.new()
    off.position=p.position; off.collision_mask=0;off.collision_layer=L.bit(L.PICKUP)
    shape(off,Vector2(70,70),Color("8b8f96"));stage.add_child(off)
    off.body_entered.connect(func(_body):missed[0]+=1)
    await ticks(5)
    check("zero mask prevents detection",missed[0]==0,missed[0])
    await fresh("Character: authored jump, collision-resolved landing")
    floor_body(Vector2(640,560),Vector2(1100,32))
    p=player(Vector2(420,500))
    await ticks(2)
    for i in 10:
        await get_tree().physics_frame
        p.step(1.0/60,0.0,false,false)
    check("character lands on floor",p.is_on_floor(),p.is_on_floor())
    var initial := p.position.y
    var min_y := initial
    for i in 70:
        await get_tree().physics_frame
        p.step(1.0/60,0.0,i==0,false)
        min_y=minf(min_y,p.position.y)
        trajectory.append({"tick":i,"time":float(i+1)/60,"height":initial-p.position.y,"vy":p.velocity.y})
        if i==23:
            label("Scripted jump | target height 72 px",Vector2(60,140))
            await snap("jump")
    measurements["jump_height"] = initial-min_y
    check("jump height within ten percent",absf(initial-min_y-72.0)<=7.2,initial-min_y)
    check("jump returns to floor",p.is_on_floor(),p.is_on_floor())
    p.respawn(Vector2(800,400))
    check("respawn resets velocity",p.velocity==Vector2.ZERO,str(p.velocity))
    await fresh("Rigid body: impulse divided by mass")
    floor_body(Vector2(640,560),Vector2(1100,32))
    var rb:=RigidBody2D.new()
    rb.position=Vector2(380,300)
    rb.mass=2.0
    rb.gravity_scale=0.0
    rb.linear_damp=0.0
    rb.collision_layer=L.bit(L.DEBRIS);rb.collision_mask=L.bit(L.WORLD)
    rb.contact_monitor=true;rb.max_contacts_reported=4
    shape(rb,Vector2(70,70),Color("8b8f96"));stage.add_child(rb)
    await ticks(2)
    rb.apply_central_impulse(Vector2(120,0))
    await ticks(2)
    check("impulse changes velocity",absf(rb.linear_velocity.x-60)<1,rb.linear_velocity.x)
    label("mass = 2 | impulse = 120 | velocity ≈ 60",Vector2(60,140))
    await snap("impulse")
    rb.gravity_scale=1.0
    var contacts := [0]
    rb.body_entered.connect(func(_body):contacts[0]+=1)
    await ticks(75)
    check("rigid contact reporting enabled",contacts[0]>0,contacts[0])
    text_layer.get_child(0).text = "Rigid body: gravity and floor contact"
    text_layer.get_child(2).text = "Contact reporting enabled | floor contact observed"
    await snap("crate")
    await fresh("Tile contact: exact cell from surface point")
    var tiles:=TileMapLayer.new()
    tiles.position=Vector2(200,300)
    var ts:=TileSet.new()
    ts.tile_size=Vector2i(64,64)
    ts.add_physics_layer()
    ts.set_physics_layer_collision_layer(0,L.bit(L.WORLD))
    ts.set_physics_layer_collision_mask(0,0)
    var atlas:=TileSetAtlasSource.new()
    var im:=Image.create(64,64,false,Image.FORMAT_RGBA8)
    im.fill(Color("8b8f96"))
    atlas.texture=ImageTexture.create_from_image(im)
    atlas.texture_region_size=Vector2i(64,64)
    atlas.create_tile(Vector2i.ZERO)
    ts.add_source(atlas,0)
    var td:=atlas.get_tile_data(Vector2i.ZERO,0)
    td.set_collision_polygons_count(0,1)
    var polygon := PackedVector2Array([
        Vector2(-32,-32), Vector2(32,-32),
        Vector2(32,32), Vector2(-32,32)])
    td.set_collision_polygon_points(0,0,polygon)
    tiles.tile_set=ts
    stage.add_child(tiles)
    for x in 6: tiles.set_cell(Vector2i(x,0),0,Vector2i.ZERO)
    tiles.update_internals()
    p=player(Vector2(200+3*64+32,480))
    await ticks(4)
    var hit:KinematicCollision2D=p.move_and_collide(Vector2(0,-180))
    check("tile collision exists",hit!=null,hit!=null)
    if hit:
        var cell:=HIT.cell_at(tiles,hit.get_position(),hit.get_normal())
        var rid_cell:=tiles.get_coords_for_body_rid(hit.get_collider_rid())
        check("contact selects intended cell",cell==Vector2i(3,0),str(cell))
        check("quadrant RID differs from cell",rid_cell!=cell,str(rid_cell))
        measurements["tile"]={"point":str(hit.get_position()),"normal":str(hit.get_normal()),"cell":str(cell),"rid_cell":str(rid_cell)}
        label("Contact cell: "+str(cell)+" | RID quadrant: "+str(rid_cell),Vector2(60,140))
    await snap("tiles")
    await fresh("Swept motion: thin floor, long displacement")
    floor_body(Vector2(640,450),Vector2(900,4))
    p=player(Vector2(400,300))
    await ticks(3)
    var sweep:=p.move_and_collide(Vector2(0,300))
    check("sweep hits thin floor",sweep!=null,sweep!=null)
    label("300 px requested displacement | 4 px floor",Vector2(60,140))
    label("Collision returned: "+str(sweep!=null),Vector2(650,350),36)
    await snap("sweep")
    check("CCD ray enum",RigidBody2D.CCD_MODE_CAST_RAY==1,RigidBody2D.CCD_MODE_CAST_RAY)
    check("CCD shape enum",RigidBody2D.CCD_MODE_CAST_SHAPE==2,RigidBody2D.CCD_MODE_CAST_SHAPE)
    var block:=StaticBody2D.new()
    block.set_script(load("res://block.gd"));stage.add_child(block)
    block.bump();block.bump()
    check("block use latch",block.used,block.used)
    var report:={"measurements":measurements,"checks":checks,"trajectory":trajectory,"limitations":["Scripted isolated experiments, not a human playtest.","No cross-device determinism claim.","Moving platform, coyote/buffer edges, enemy corner contacts and CCD performance require separate tests."]}
    var f:=FileAccess.open(root_path+"evidence/physics-results.json",FileAccess.WRITE)
    f.store_string(JSON.stringify(report,"  "));f.close()
    var failed:=checks.filter(func(c): return not c.passed).size()
    print("RESULT "+str(checks.size())+" checks, "+str(failed)+" failed")
    await ticks(2)
    get_tree().quit(1 if failed else 0)
