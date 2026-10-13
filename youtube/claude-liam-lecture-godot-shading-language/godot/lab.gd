extends Node
var viewport: SubViewport
var stage: Control
var report: Array = []
var out_dir: String
var capture_mode := false
func _ready():
    out_dir = ProjectSettings.globalize_path("res://../captures")
    capture_mode = "--capture" in OS.get_cmdline_user_args()
    viewport = SubViewport.new()
    viewport.size = Vector2i(3840,2160)
    viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    add_child(viewport)
    var display = TextureRect.new()
    display.texture = viewport.get_texture()
    display.size = Vector2(960,540)
    add_child(display)
    await run_examples()
    if capture_mode: get_tree().quit()
func reset(title: String):
    if is_instance_valid(stage):
        stage.queue_free()
    stage = Control.new()
    viewport.add_child(stage)
    label(title, Vector2(180,120), 86)
    label("Godot engine output · scripted teaching lab · Compatibility", Vector2(180,1940), 52)
func label(text: String, pos: Vector2, size: int):
    var l = Label.new()
    l.text = text
    l.position = pos
    l.add_theme_font_size_override("font_size",size)
    l.add_theme_color_override("font_color",Color("3d3929"))
    stage.add_child(l)
    return l
func material(name: String) -> ShaderMaterial:
    var m = ShaderMaterial.new()
    m.shader = load("res://shaders/" + name + ".gdshader")
    return m
func patch(m: ShaderMaterial, pos:=Vector2(1000,430), sz:=Vector2(1400,1200)) -> ColorRect:
    var r = ColorRect.new()
    r.position = pos
    r.size = sz
    r.color = Color(0.2,0.55,0.8,1)
    r.material = m
    stage.add_child(r)
    return r
func save(name: String):
    for i in range(5): await RenderingServer.frame_post_draw
    var im = viewport.get_texture().get_image()
    if capture_mode: im.save_png(out_dir.path_join(name + ".png"))
    var samples = []
    for p in [Vector2i(1350,1000),Vector2i(2050,1000)]:
        var c = im.get_pixelv(p)
        samples.append([snappedf(c.r,0.001),snappedf(c.g,0.001),snappedf(c.b,0.001),snappedf(c.a,0.001)])
    report.append({"capture":name,"samples":samples})
    print("CAPTURE ",name," ",JSON.stringify(samples))
func run_examples():
    for name in ["constant","uv","scalars","swizzle","matrix","array","varying","branch","switch","fallthrough","loop","while","vertex","wave"]:
        reset(name + ".gdshader")
        patch(material(name))
        await save(name)
    reset("Shared ShaderMaterial · both change")
    var shared = material("uniform")
    patch(shared,Vector2(400,500),Vector2(1300,1200))
    patch(shared,Vector2(2140,500),Vector2(1300,1200))
    shared.set_shader_parameter("tint",Color(0.85,0.25,0.12,1))
    await save("shared")
    reset("Unique materials · one changes")
    var unique = shared.duplicate()
    unique.set_shader_parameter("tint",Color(0.2,0.55,0.8,1))
    patch(shared,Vector2(400,500),Vector2(1300,1200))
    patch(unique,Vector2(2140,500),Vector2(1300,1200))
    await save("unique")
    reset("Instance uniforms · one shared material")
    var inst = material("instance")
    var left = patch(inst,Vector2(400,500),Vector2(1300,1200))
    var right = patch(inst,Vector2(2140,500),Vector2(1300,1200))
    left.set_instance_shader_parameter("tint",Color(0.85,0.25,0.12,1))
    right.set_instance_shader_parameter("tint",Color(0.2,0.55,0.8,1))
    await save("instance")
    reset("sampler2D · image_tex sampled at UV")
    var im = Image.create(8,8,false,Image.FORMAT_RGBA8)
    for y in range(8):
        for x in range(8): im.set_pixel(x,y,Color(0.2,0.55,0.8) if (x+y)%2==0 else Color(1,0.8,0.2))
    var sampler = material("sampler")
    sampler.set_shader_parameter("image_tex",ImageTexture.create_from_image(im))
    patch(sampler)
    await save("sampler")
    reset("Predict the tint · amount = 0 / 0.5 / 1")
    for i in range(3):
        var m = material("flash")
        m.set_shader_parameter("amount",i*0.5)
        patch(m,Vector2(200+i*1230,550),Vector2(980,1050))
        label(str(i*0.5),Vector2(550+i*1230,1740),70)
    await save("flash")
    # Proof of material sharing, independent resource, hint vs runtime value.
    shared.set_shader_parameter("amount",7.0)
    print("CHECK hint_range stores ",shared.get_shader_parameter("amount"))
    print("CHECK unique material: ",shared != unique,"; shared shader: ",shared.shader == unique.shader)
    await spatial_capture("spatial")
    await spatial_capture("alpha")
    if capture_mode:
        var f = FileAccess.open(out_dir.path_join("pixels.json"),FileAccess.WRITE)
        f.store_string(JSON.stringify(report,"  "))
func spatial_capture(name: String):
    reset(name + ".gdshader · real 3D render")
    var view3 = SubViewport.new()
    view3.size = Vector2i(3000,1500)
    view3.own_world_3d = true
    view3.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    stage.add_child(view3)
    var cam = Camera3D.new()
    view3.add_child(cam)
    cam.position = Vector3(3,2,4)
    cam.look_at(Vector3.ZERO)
    var mesh = MeshInstance3D.new()
    mesh.mesh = BoxMesh.new()
    mesh.scale = Vector3(3,3,3)
    mesh.material_override = material(name)
    view3.add_child(mesh)
    var light = DirectionalLight3D.new()
    light.rotation_degrees = Vector3(-35,-30,0)
    view3.add_child(light)
    var env = WorldEnvironment.new()
    env.environment = Environment.new()
    env.environment.background_mode = Environment.BG_COLOR
    env.environment.background_color = Color(0.12,0.15,0.2)
    env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    env.environment.ambient_light_color = Color.WHITE
    env.environment.ambient_light_energy = 0.4
    view3.add_child(env)
    var image = TextureRect.new()
    image.texture = view3.get_texture()
    image.position = Vector2(420,360)
    image.size = Vector2(3000,1500)
    stage.add_child(image)
    await save(name)
