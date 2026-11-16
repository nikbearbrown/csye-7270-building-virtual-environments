@tool
extends Node2D
## Original teaching simulation. Runs in the editor and in the game.
@export var heading := "Birth, Motion, Death"
@export_range(0.0,100.0) var birth_rate := 20.0
@export_range(0.1,5.0) var lifetime := 2.0
@export var gravity := 180.0
@export var wind := 0.0
@export var launch_speed := 260.0
@export_range(0.0,80.0) var spread := 28.0
@export var radius := 8.0
@export var fade := true
@export var shrink := true
@export var cleanup := true
@export var move_emitter := false
@export var vectors := false
@export var burst_size := 40
var particles: Array[Dictionary] = []
var birth_budget := 0.0
var clock := 0.0
var born := 0
var removed := 0
var rng := RandomNumberGenerator.new()
func _ready() -> void:
	rng.seed = 7270
func emitter() -> Vector2:
	return Vector2(540 + sin(clock*1.5)*140 if move_emitter else 540,510)
func spawn_one() -> void:
	var angle := deg_to_rad(rng.randf_range(-spread,spread))
	particles.append({
		"p": emitter(),
		"v": Vector2(0,-launch_speed).rotated(angle),
		"age": 0.0,
		"life": lifetime
	})
	born += 1
func burst() -> void:
	for i in burst_size:spawn_one()
func reset() -> void:
	particles.clear();birth_budget=0;born=0;removed=0
func _process(delta: float) -> void:
	clock += delta
	birth_budget += birth_rate * delta
	while birth_budget >= 1.0 and particles.size() < 600:
		spawn_one();birth_budget -= 1.0
	for i in range(particles.size()-1,-1,-1):
		var p=particles[i]
		p.age += delta
		p.v += Vector2(wind,gravity) * delta
		p.p += p.v * delta
		if cleanup and p.age >= p.life:
			particles.remove_at(i);removed += 1
	queue_redraw()
func _draw() -> void:
	draw_set_transform(Vector2(-540,-360))
	draw_rect(Rect2(0,0,1080,720),Color("111721"))
	var font=ThemeDB.fallback_font
	draw_string(font,Vector2(34,58),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,34,Color("f4f1e8"))
	draw_string(font,Vector2(34,106),"LIVE %d    BORN %d    REMOVED %d" %[particles.size(),born,removed],HORIZONTAL_ALIGNMENT_LEFT,-1,26,Color("aabacb"))
	draw_line(Vector2(60,610),Vector2(1040,610),Color("384656"),2)
	for p in particles:
		var age01=clampf(p.age/p.life,0,1)
		var c=Color("f4a850");c.a=1-age01 if fade else 1
		var r=radius*(1-age01*.85) if shrink else radius
		draw_circle(p.p,r,c)
		if vectors:
			draw_line(p.p,p.p+p.v*.18,Color("7eddd2"),2)
			draw_line(p.p,p.p+Vector2(wind,gravity)*.18,Color("db83d4"),2)
	draw_circle(emitter(),7,Color("ffffff"))
	draw_string(font,Vector2(34,665),"%.1f births/s   |   %.1f s lifetime   |   wind %.1f   |   gravity %.1f" %[birth_rate,lifetime,wind,gravity],HORIZONTAL_ALIGNMENT_LEFT,-1,26,Color("eeeeee"))
func frame_lesson() -> void:
	for c in EditorInterface.get_base_control().find_children("*","Button",true,false):
		if c.is_visible_in_tree() and c.tooltip_text == "Center View":
			c.emit_signal("pressed")
