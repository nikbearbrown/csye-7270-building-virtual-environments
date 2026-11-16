extends SceneTree
func _initialize():
 var image=Image.create(256,64,false,Image.FORMAT_RGBA8)
 for frame in range(4):
  for y in range(64):
   for x in range(64):
    var p=(Vector2(x,y)-Vector2(31.5,31.5))/31.5
    var radius=.35+frame*.18
    var alpha=clampf(1.0-p.length()/radius,0,1)*(1.0-frame*.17)
    image.set_pixel(frame*64+x,y,Color(1,1,1,alpha))
 image.save_png("res://assets/smoke-flipbook.png")
 var ring=GradientTexture2D.new();ring.width=128;ring.height=128;ring.fill=GradientTexture2D.FILL_RADIAL;ring.fill_from=Vector2(.5,.5);ring.fill_to=Vector2(1,.5)
 var gradient=Gradient.new();gradient.set_color(0,Color(1,1,1,0));gradient.set_color(1,Color(1,1,1,0));gradient.add_point(.65,Color(1,1,1,0));gradient.add_point(.8,Color.WHITE);gradient.add_point(.9,Color(1,1,1,0));ring.gradient=gradient;ResourceSaver.save(ring,"res://assets/ring.tres")
 var fade=GradientTexture1D.new();fade.gradient=Gradient.new();fade.gradient.set_color(0,Color(1,.9,.5,1));fade.gradient.set_color(1,Color(.6,.15,.02,0));ResourceSaver.save(fade,"res://assets/flash-fade.tres")
 var blue=GradientTexture1D.new();blue.gradient=Gradient.new();blue.gradient.set_color(0,Color(.2,.6,1,1));blue.gradient.set_color(1,Color(.7,.2,1,0));ResourceSaver.save(blue,"res://assets/magic-fade.tres")
 print("Original flipbook, ring and ramps saved");quit()
