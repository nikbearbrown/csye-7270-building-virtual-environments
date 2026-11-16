extends CharacterBody2D
signal head_bumped(collision: KinematicCollision2D)
signal hurt
@export var max_speed := 180.0
@export var ground_accel := 1400.0
@export var ground_decel := 1800.0
@export var air_accel := 900.0
@export var jump_height := 72.0
@export var time_to_apex := 0.38
@export var fall_gravity_multiplier := 1.8
@export var jump_cut_multiplier := 0.45
@export var max_fall_speed := 600.0
@export var coyote_time := 0.08
@export var jump_buffer_time := 0.10
@export var push_strength := 40.0
@export var accept_input := false
@onready var rise_gravity := 2.0 * jump_height / pow(time_to_apex, 2)
@onready var jump_velocity := -rise_gravity * time_to_apex
var coyote := 0.0
var buffer := 0.0
func _physics_process(delta: float) -> void:
    if not accept_input:
        return
    step(delta, Input.get_axis("move_left", "move_right"),
        Input.is_action_just_pressed("jump"), Input.is_action_just_released("jump"))
func step(delta: float, axis: float, pressed: bool, released: bool) -> void:
    # Floor state here belongs to the previous movement call.
    coyote = coyote_time if is_on_floor() else maxf(coyote - delta, 0.0)
    buffer = jump_buffer_time if pressed else maxf(buffer - delta, 0.0)
    var g := rise_gravity * (fall_gravity_multiplier if velocity.y > 0.0 else 1.0)
    velocity.y = minf(velocity.y + g * delta, max_fall_speed)
    var rate := air_accel
    if is_on_floor():
        rate = ground_decel if is_zero_approx(axis) else ground_accel
    velocity.x = move_toward(velocity.x, axis * max_speed, rate * delta)
    if buffer > 0.0 and coyote > 0.0:
        velocity.y = jump_velocity
        buffer = 0.0
        coyote = 0.0
    if released and velocity.y < 0.0:
        velocity.y *= jump_cut_multiplier
    move_and_slide()
    # Floor state now describes this movement call.
    for i in get_slide_collision_count():
        var c := get_slide_collision(i)
        if c.get_normal().y > 0.7:
            head_bumped.emit(c)
        var rb := c.get_collider() as RigidBody2D
        if rb:
            rb.apply_central_impulse(-c.get_normal() * push_strength)
func bounce() -> void:
    velocity.y = jump_velocity * 0.6
func take_hit() -> void:
    hurt.emit()
func respawn(at: Vector2) -> void:
    global_position = at
    velocity = Vector2.ZERO
    reset_physics_interpolation()
func drop_through() -> void:
    set_collision_mask_value(Layers.ONE_WAY, false)
    await get_tree().create_timer(0.2, true, true).timeout
    # Minimal timed policy: production code must check that the body is clear.
    set_collision_mask_value(Layers.ONE_WAY, true)
