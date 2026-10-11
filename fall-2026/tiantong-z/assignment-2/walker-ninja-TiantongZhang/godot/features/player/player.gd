extends CharacterBody2D

const Tuning = preload("res://features/player/tuning.gd")
var tuning = Tuning.new()
# D3 swing geometry. The draw code and the hitbox are both derived from these
# three numbers, so the blade the player sees and the blade that kills cannot
# drift apart.
const ATTACK_PIVOT := Vector2(5.0, -18.0)
const ATTACK_ANGLE_START := -2.0943951023932  # -120 degrees: raised up and back
const ATTACK_ANGLE_END := 0.69813170079773    #  +40 degrees: down and forward
var enabled: bool = false
var tick: int = 0
var last_floor_tick: int = -1000
var jump_request_tick: int = -1000
var opportunity_consumed: bool = false
var require_jump_release: bool = true
var facing: float = 1.0
var jumps: int = 0
# D1/D2 (CHANGE-BRIEF 0.1.0 section 3): one extra jump and one dash per
# airborne period. Both budgets are refilled at exactly one place — floor
# contact in _physics_process — so "once per airborne period" cannot be
# refreshed in mid-air by any other event.
var air_jumps_left: int = 0
var dashes_left: int = 0
var dash_ticks_left: int = 0
var dash_dir: float = 1.0
var dashes: int = 0
# D3 (CHANGE-BRIEF revision 0.3.0): the sword swing.
var attack_ticks_left: int = 0
var attack_dir: float = 1.0
var attacks: int = 0
var attack_hitbox: Area2D
var attack_shape: CollisionShape2D
## C3 (CHANGE-BRIEF revision 2.4.0). Set by the session on a fatal contact and
## cleared on respawn. It is keyed off the SESSION state rather than off
## movement, because on death the body is disabled and `is_on_floor()` keeps
## whatever it last returned -- so a pose derived from movement would differ
## depending on HOW the player died.
var death_pose: bool = false
var test_control: bool = false
var test_axis: float = 0.0
var test_jump_pressed: bool = false
var test_jump_held: bool = false
var test_dash_pressed: bool = false
var test_attack_pressed: bool = false

func _ready() -> void:
	name = "Player"
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 1.0
	# Read straight off disk rather than through res:// import, for the same
	# reason session.gd loads its audio that way: a `--headless --script` run
	# does not rescan the filesystem, so `load()` on an unimported asset fails
	# in exactly the situation the assignment asks to verify -- a fresh
	# checkout. An absent directory is not an error: the code-drawn body is
	# still there and `_draw` falls back to it.
	for key in POSE_FILES:
		var path := ProjectSettings.globalize_path(
			"res://assets/poses/%s.png" % POSE_FILES[key])
		if not FileAccess.file_exists(path):
			continue
		var img := Image.load_from_file(path)
		if img:
			pose_tex[key] = ImageTexture.create_from_image(img)
	var shape := RectangleShape2D.new()
	shape.size = Vector2(18, 28)
	var collider := CollisionShape2D.new()
	collider.shape = shape
	collider.position = Vector2(0, -14)
	add_child(collider)
	# The swing hitbox. Layer 6 = PlayerAttack, mask layer 3 = Enemy, so it can
	# never interact with the world, the player, the hazards or the goal. It is
	# a blade-sized rectangle moved onto the blade each active tick rather than
	# a static box covering the whole arc.
	attack_hitbox = Area2D.new()
	attack_hitbox.name = "SwordArc"
	attack_hitbox.collision_layer = 32
	attack_hitbox.collision_mask = 4
	attack_hitbox.monitoring = false
	attack_shape = CollisionShape2D.new()
	var blade := RectangleShape2D.new()
	# 4.0 matches 2 * the drawn blade half-width below, so the hitbox is not
	# fatter than the blade the player sees (CHANGE-BRIEF 0.3.0 P5).
	blade.size = Vector2(tuning.attack_reach, 4.0)
	attack_shape.shape = blade
	attack_hitbox.add_child(attack_shape)
	add_child(attack_hitbox)

func reset_at(spawn: Vector2) -> void:
	position = spawn
	velocity = Vector2.ZERO
	last_floor_tick = -1000
	jump_request_tick = -1000
	opportunity_consumed = false
	require_jump_release = true
	test_jump_pressed = false
	test_dash_pressed = false
	test_attack_pressed = false
	jumps = 0
	air_jumps_left = tuning.air_jumps
	dashes_left = tuning.air_dashes
	dash_ticks_left = 0
	dashes = 0
	attack_ticks_left = 0
	attacks = 0
	_sync_attack_hitbox()
	queue_redraw()

## 0 = not swinging, 1 = windup, 2 = active (hitbox live), 3 = recovery.
## Which pose this tick. Returns a key rather than a texture so the mapping can
## be asserted without a renderer -- the states are exactly the ones in
## CHARACTER-SHEET section 5, in priority order.
##
## `death` comes first because on death the body is disabled and `is_on_floor()`
## keeps whatever it last returned, so anything derived from movement would
## differ by cause of death.
func pose_key() -> String:
	if death_pose:
		return "death"
	var phase := attack_phase()
	if phase == 1:
		return "windup"
	if phase >= 2:
		# P10 (recovery) is one of the three optional poses and was not
		# generated; three ticks of the live frame is the honest substitute.
		return "live"
	if dash_ticks_left > 0:
		return "dash"
	if not is_on_floor():
		return "rise" if velocity.y < 0.0 else "fall"
	if absf(velocity.x) > 8.0:
		return "run"
	return "idle"

func attack_phase() -> int:
	if attack_ticks_left <= 0:
		return 0
	var elapsed: int = tuning.attack_ticks - attack_ticks_left
	if elapsed < tuning.attack_windup_ticks:
		return 1
	if elapsed < tuning.attack_windup_ticks + tuning.attack_active_ticks:
		return 2
	return 3

## The blade's angle this tick. Held at the start angle through the windup,
## swept during the active window, held at the end angle through recovery.
func attack_angle() -> float:
	var elapsed := float(tuning.attack_ticks - attack_ticks_left)
	var windup := float(tuning.attack_windup_ticks)
	var active := float(tuning.attack_active_ticks)
	# Divide by active - 1 so the sweep REACHES its end angle on the last active
	# tick. Dividing by `active` capped t at 0.8, which left the blade above
	# y=301 for the whole live window and put the only ground-reaching angle in
	# recovery, where the hitbox is off. Enemies standing on the floor were
	# therefore unhittable, and no test noticed because every swing assertion
	# was about the hitbox tracking the blade rather than about what the blade
	# could reach.
	var span: float = maxf(1.0, active - 1.0)
	var t: float = 0.0
	if elapsed >= windup + span:
		t = 1.0
	elif elapsed > windup:
		t = (elapsed - windup) / span
	return lerpf(ATTACK_ANGLE_START, ATTACK_ANGLE_END, t)

func attack_tip() -> Vector2:
	return ATTACK_PIVOT + Vector2.from_angle(attack_angle()) * tuning.attack_reach

## The blade as a world-space segment this tick, mirrored the same way the
## drawing and the annotated hitbox are. Session uses this for the kill test
## because Area2D.overlaps_area() reports the PREVIOUS physics step, and the
## only active tick whose blade angle reaches a ground-level enemy is the last
## one - by the time the server could report it, monitoring is already off.
func attack_segment() -> PackedVector2Array:
	var a := ATTACK_PIVOT
	var b := attack_tip()
	if attack_dir < 0.0:
		a.x = -a.x
		b.x = -b.x
	return PackedVector2Array([position + a, position + b])

func _sync_attack_hitbox() -> void:
	if not is_instance_valid(attack_hitbox):
		return
	var live: bool = attack_phase() == 2
	attack_hitbox.monitoring = live
	if not live:
		return
	var a := ATTACK_PIVOT
	var b := attack_tip()
	var mid := (a + b) * 0.5
	var ang := (b - a).angle()
	if attack_dir < 0.0:
		# Mirroring about the body's vertical axis: (x, y) -> (-x, y) sends an
		# angle t to PI - t.
		mid.x = -mid.x
		ang = PI - ang
	attack_shape.position = mid
	attack_shape.rotation = ang

func _physics_process(delta: float) -> void:
	if not enabled:
		return
	tick += 1
	var axis := test_axis if test_control else Input.get_axis("move_left", "move_right")
	var held := test_jump_held if test_control else Input.is_action_pressed("jump")
	var pressed := test_jump_pressed if test_control else Input.is_action_just_pressed("jump")
	var dash_pressed := test_dash_pressed if test_control else Input.is_action_just_pressed("dash")
	var attack_pressed := test_attack_pressed if test_control else Input.is_action_just_pressed("attack")
	test_jump_pressed = false
	test_dash_pressed = false
	test_attack_pressed = false
	if not held:
		require_jump_release = false
	# The single refill point for every airborne budget.
	if is_on_floor() and velocity.y >= 0.0:
		last_floor_tick = tick
		opportunity_consumed = false
		air_jumps_left = tuning.air_jumps
		dashes_left = tuning.air_dashes
	if pressed and not require_jump_release:
		jump_request_tick = tick
	if not is_zero_approx(axis):
		facing = signf(axis)
	# D3 — sword swing. Ground or air, no movement effect, no invulnerability,
	# and no resources granted. A press during a swing is ignored. Facing is
	# locked for the duration so the drawn blade and the hitbox agree.
	# Count down BEFORE accepting a new press, so the press frame itself is
	# windup tick 0 and the phases come out 4 + 5 + 5 exactly. Counting down
	# first also means a press on the frame a swing ends starts the next one
	# with no dead frame in between.
	if attack_ticks_left > 0:
		facing = attack_dir
		attack_ticks_left -= 1
	if attack_pressed and attack_ticks_left <= 0:
		attack_ticks_left = tuning.attack_ticks
		attack_dir = facing
		attacks += 1
	# D2 — air dash. Refused while standing and while a dash is already
	# running. It grants no jump, and it confers no invulnerability: the
	# session's hazard overlap test is untouched, so a dash into the spikes
	# still kills.
	if dash_pressed and not is_on_floor() and dashes_left > 0 and dash_ticks_left <= 0:
		dashes_left -= 1
		dash_ticks_left = tuning.dash_ticks
		dash_dir = facing
		dashes += 1
	if dash_ticks_left > 0:
		# Locked horizontal speed with vertical motion suspended. Facing is
		# pinned to the direction the dash began in, so the sprite cannot face
		# backwards mid-dash. Gravity and the acceleration curve resume on the
		# tick the dash ends; the leftover speed then decays through the
		# starter's own deceleration, which is what gives the dash a tail.
		dash_ticks_left -= 1
		facing = dash_dir
		velocity.x = dash_dir * tuning.dash_speed
		velocity.y = 0.0
	else:
		var rate: float = tuning.acceleration if not is_zero_approx(axis) else tuning.deceleration
		velocity.x = move_toward(velocity.x, axis * tuning.speed, rate * delta)
		velocity.y = minf(velocity.y + tuning.gravity * delta, tuning.terminal_velocity)
	# The ground/coyote jump keeps precedence over the air jump, so a jump
	# inside the coyote window still spends the FIRST jump and leaves the air
	# jump in hand. A jump also cancels a running dash.
	if not opportunity_consumed and tick - last_floor_tick <= tuning.coyote_ticks and tick - jump_request_tick <= tuning.buffer_ticks:
		velocity.y = tuning.jump_velocity
		opportunity_consumed = true
		jump_request_tick = -1000
		dash_ticks_left = 0
		jumps += 1
	elif air_jumps_left > 0 and tick - jump_request_tick <= tuning.buffer_ticks:
		# D1 — the second jump, at the starter's unchanged jump_velocity.
		velocity.y = tuning.jump_velocity
		air_jumps_left -= 1
		jump_request_tick = -1000
		dash_ticks_left = 0
		jumps += 1
	_sync_attack_hitbox()
	move_and_slide()
	position.x = maxf(position.x, 10.0)
	queue_redraw()

## The rim colour. steel_edge, already in the eight-colour palette, so the
## dungeon rim costs no new colour (CHARACTER-SHEET section 3).
const RIM := Color("9aa7bd")

## C2 (CHANGE-BRIEF revision 2.5.0). One generated sprite per state the code can
## already distinguish, in a 32 x 32 cell whose anchor -- the point the engine
## places at `position` -- is at (20, 30) from the cell's top-left. Both numbers
## come from CHARACTER-SHEET section 2 and are what `scripts/import_pose.py`
## places every frame against.
const POSE_CELL := 32.0
const POSE_ANCHOR := Vector2(20.0, 30.0)
const POSE_FILES := {
	"idle": "p1-idle", "run": "p2-run", "rise": "p3-rising", "fall": "p4-falling",
	"dash": "p5-dash", "windup": "p6-windup", "live": "p7-live", "death": "p8-death",
}
var pose_tex: Dictionary = {}

## The rim is DIRECTIONAL: 1 px toward the character's back and 1 px up, and
## nothing on the front or the underside.
##
## Revision 1.4 changed this, and the reason is arithmetic rather than taste. A
## rim grown on all four sides costs a part 2 px of width, so a 3 px arm keeps
## 1 px of armour and a 4 px leg keeps 2. Rendered, the limbs came out as grey
## pipes with a hint of navy down the middle -- the value scheme that is
## supposed to separate near limb from far limb had almost nowhere to happen.
## Growing in one direction only costs 0 px of width and still breaks the
## silhouette against the wall, because the light in a dungeon comes from a
## torch above and behind, not from everywhere.
##
## x is forward, so `x - 1` is toward the back for both facings: `_mrect`
## mirrors it. The rim therefore stays on the same side of the body when the
## character turns around, which is what a light source does and an outline
## does not.
func _mrect_o(x: float, y: float, w: float, h: float) -> void:
	_mrect(x - 1.0, y - 1.0, w + 1.0, h + 1.0, RIM)

## Same idea for a polygon: the shape translated 1 px back and 1 px up. A
## translation rather than an expansion, so a thin wedge keeps its thickness.
func _mpoly_o(points: PackedVector2Array) -> void:
	var out := PackedVector2Array()
	for p in points:
		out.append(p + Vector2(-1.0, -1.0))
	_mpoly(out, RIM)

func _mrect(x: float, y: float, w: float, h: float, c: Color) -> void:
	# One set of coordinates serves both facings: x is measured forward from the
	# body centre, and the rect is mirrored about that centre when facing left.
	var px: float = x if facing > 0.0 else -(x + w)
	draw_rect(Rect2(px, y, w, h), c)

func _mpoly(points: PackedVector2Array, c: Color) -> void:
	if facing > 0.0:
		draw_colored_polygon(points, c)
		return
	var flipped := PackedVector2Array()
	for i in range(points.size() - 1, -1, -1):
		flipped.append(Vector2(-points[i].x, points[i].y))
	draw_colored_polygon(flipped, c)

func _bar(a: Vector2, b: Vector2, half: float) -> PackedVector2Array:
	# A rectangle of thickness 2*half laid along the segment a->b, so the sword
	# is described by its endpoints instead of hand-computed corner arithmetic.
	var n := (b - a).orthogonal().normalized() * half
	return PackedVector2Array([a + n, b + n, b - n, a - n])

## The body, back to front, as data. Both the rim pass and the paint pass walk
## this one array, so they cannot describe different characters.
##
## Entry shapes: [0, colour, rim, x, y, w, h] for a rect,
##               [1, colour, rim, points]     for a polygon.
## x is measured FORWARD from the body centre; `_mrect`/`_mpoly` mirror it when
## facing left. `rim` marks the parts that form the OUTER silhouette; interior
## detail is false and gets no halo.
##
## Revision 1.4 (CONCEPT): limbs, torso and head are separable. At 18 x 28 that
## cannot be done with gaps -- a 1 px rim closes any gap narrow enough to fit
## here -- so it is done with VALUE. Three steps, and every part belongs to
## exactly one:
##
##   shade  #16233d  the far side of the body, plus the recessed abdomen, the
##                   jawline and the neck
##   plate  #1f3a6e  the near side: chest, near arm, near leg
##   steel  #4a5468  the extremities only -- gauntlets and boots
##
## So the near limbs read against the torso, the far limbs read against the
## near limbs, and the hands and feet read against the limbs they end. None of
## it depends on a gap surviving a rim.
##
## Limb widths are 4 px (legs) and 3 px (arms). The first attempt used 2.5-3 px
## and an all-sides rim, which left 1 px of armour inside a 3 px arm; the rim
## is directional now (see `_mrect_o`) so the full width survives and the value
## step has somewhere to happen.
## The generated-sprite path. The sprite carries the body, the scarf, the rim
## and the visor; the BLADE is still drawn in code, before and after it.
##
## That is not a leftover. The swung blade comes from `ATTACK_PIVOT`,
## `attack_angle()` and `tuning.attack_reach` -- the same three numbers the kill
## hitbox is built from -- so a blade baked into a sprite would stop tracking
## the hitbox the moment anyone touched the tuning, and nothing would say so.
## The generated poses were prompted with "empty hand, NO weapon" for this
## reason, and `attack-hitbox-on-the-blade-*` still measures the agreement.
func _draw_sprite(sprite: Texture2D, phase: int) -> void:
	var steel := Color("4a5468")
	var steel_dark := Color("2a3246")
	var steel_edge := Color("9aa7bd")
	var scarf_tip := Color("6a3fbf")

	if death_pose:
		# The blade has skidded on past the body.
		_mpoly(_bar(Vector2(13.0, -1.1), Vector2(23.0, -0.7), 1.3), steel)
		_mpoly(_bar(Vector2(14.0, -1.1), Vector2(23.0, -0.7), 0.5), steel_edge)
	elif phase == 0:
		# Sheathed, behind the sprite, so only the grip and the scabbard tip
		# protrude -- which is what makes it read as carried rather than held.
		#
		# These endpoints are NOT the code-drawn body's. That silhouette was
		# 18 px wide with a flat-topped helm, and the blade was tuned to be
		# occluded by it; the generated sprite has a taller hood and a narrower
		# waist, so the same line left the grip floating in the air above the
		# head. Pulled down and in so it emerges from behind the shoulder.
		var hilt := Vector2(-7.5, -27.0)
		var tip := Vector2(10.0, -5.0)
		var guard := hilt.lerp(tip, 0.22)
		var perp := (tip - hilt).orthogonal().normalized()
		_mpoly(_bar(guard, tip, 1.7), steel)
		_mpoly(_bar(guard.lerp(tip, 0.10), tip, 0.6), steel_edge)
		_mpoly(_bar(hilt, guard, 1.3), steel_dark)
		_mpoly(_bar(hilt.lerp(guard, 0.35), hilt.lerp(guard, 0.65), 1.4), scarf_tip)
		_mpoly(_bar(guard + perp * 2.9, guard - perp * 2.9, 0.9), steel_dark)

	# The cell, placed so its anchor lands on the node's position. Mirrored by
	# scaling x, because `draw_texture_rect` has no flip argument -- and the
	# transform is reset immediately, or the blade below would mirror twice.
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(facing, 1.0))
	draw_texture_rect(sprite, Rect2(-POSE_ANCHOR, Vector2(POSE_CELL, POSE_CELL)), false)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

	if phase != 0 and not death_pose:
		_draw_swing()

func _body_parts(stride: float, grounded: bool, phase: int) -> Array:
	var plate := Color("1f3a6e")
	var shade := Color("16233d")
	var visor := Color("7fe3ff")
	var glint := Color("d8f7ff")
	var scarf := Color("8a5cf0")
	var steel := Color("4a5468")
	# Arms counter the legs. That opposition is what makes two frames read as a
	# walk rather than as a shiver.
	var leg: float = stride * 0.55
	var arm: float = -stride * 0.35
	# Airborne the legs leave the ground pose: tucked while rising, reaching
	# while falling. This is the P3/P4 distinction in CHARACTER-SHEET section 5,
	# and without it the two air states are the same picture.
	# Positive `tuck` LIFTS. y is negative upward, so a lift subtracts from y --
	# the first version added it, which pushed the boot to y +0.8, below the
	# feet line and into the floor, and squeezed the shin to 0.6 px tall. The
	# jump frame read as a glitch rather than as a tuck.
	var tuck: float = 0.0
	if not grounded:
		tuck = 2.6 if velocity.y < 0.0 else -0.8
	var out: Array = []
	if death_pose:
		return _prone_parts()

	# --- far side, in shade --------------------------------------------------
	# Far arm: upper, forearm, gauntlet. Three parts rather than one bar, so the
	# elbow is a value break instead of a guess.
	_pr(out, shade, true, -8.0 + arm, -17.6, 3.0, 5.2)
	_pr(out, shade, true, -7.8 + arm * 1.7, -12.9, 2.8, 4.2)
	_pr(out, steel, true, -8.0 + arm * 1.7, -9.0, 3.0, 2.0)
	# Far leg: thigh, shin, boot.
	_pr(out, shade, true, -4.8 - leg * 0.5, -10.6, 4.0, 5.8)
	# The shin and boot KEEP their heights and move together: a bent knee, with
	# the shin overlapping the thigh, rather than a shin that shrinks to
	# nothing.
	_pr(out, shade, true, -4.6 - leg, -5.0 - tuck, 3.6, 3.2)
	_pr(out, steel, true, -5.0 - leg, -1.8 - tuck, 4.4, 1.8)
	# Far shoulder plate.
	_pp(out, shade, true, PackedVector2Array([
		Vector2(-4.0, -19.6), Vector2(-8.4, -17.2), Vector2(-4.0, -15.0)]))

	# --- torso --------------------------------------------------------------
	# Chest wide, abdomen narrow and darker. The taper is what makes the torso a
	# torso instead of a block with a head on it, and it is interior: no rim.
	_pr(out, plate, true, -4.2, -19.6, 8.4, 5.6)
	_pp(out, plate, true, PackedVector2Array([
		Vector2(4.2, -18.6), Vector2(7.4, -15.0), Vector2(4.2, -12.0)]))
	_pr(out, shade, false, -3.0, -14.0, 6.0, 2.8)
	_pr(out, scarf, false, -3.4, -11.6, 7.0, 1.8)

	# --- near leg, in plate -------------------------------------------------
	_pr(out, plate, true, 0.8 + leg * 0.5, -10.6, 4.0, 5.8)
	# The near leg lifts a third as much, so the air pose is a scissor and not a
	# crouch.
	_pr(out, plate, true, 1.0 + leg, -5.0 - tuck * 0.35, 3.6, 3.2)
	_pr(out, steel, true, 0.6 + leg, -1.8 - tuck * 0.35, 4.4, 1.8)

	# --- neck and head ------------------------------------------------------
	# A 2 px neck, interior. It is the whole reason the head reads as a head:
	# without it the helm is simply the top of the torso.
	_pr(out, shade, false, -2.0, -20.8, 4.0, 2.0)
	_pr(out, plate, true, -4.0, -28.0, 8.4, 7.2)
	_pp(out, shade, true, PackedVector2Array([
		Vector2(-4.0, -28.0), Vector2(-8.8, -25.2), Vector2(-4.0, -23.2)]))
	_pr(out, shade, false, -4.0, -21.4, 8.4, 1.4)
	_pr(out, visor, false, -1.4, -26.0, 5.6, 2.0)
	_pr(out, glint, false, 3.0, -26.0, 1.4, 2.0)

	# --- near shoulder and near arm -----------------------------------------
	_pp(out, plate, true, PackedVector2Array([
		Vector2(4.2, -19.6), Vector2(8.4, -17.2), Vector2(4.2, -15.0)]))
	if phase == 0:
		_pr(out, plate, true, 5.0 + arm, -17.6, 3.0, 5.2)
		_pr(out, plate, true, 5.0 + arm * 1.7, -12.9, 2.8, 4.2)
		_pr(out, steel, true, 5.0 + arm * 1.7, -9.0, 3.0, 2.0)
	else:
		# Mid-swing the near arm is drawn ALONG the blade, from the shoulder to
		# the hand that holds it. ATTACK_PIVOT is where the blade starts, so the
		# hand goes there and the forearm reaches past it: the arm and the blade
		# come from the same two numbers and cannot disagree about which way the
		# character is swinging.
		var dir := Vector2.from_angle(attack_angle())
		_pp(out, plate, true, _bar(Vector2(3.0, -17.6), ATTACK_PIVOT + dir * 4.5, 1.8))
		_pp(out, steel, true, _bar(ATTACK_PIVOT + dir * 3.0, ATTACK_PIVOT + dir * 5.6, 1.6))
	return out

## P8, the death pose. Specified by the storyboard sketch
## (design/storyboard/panel-06-death.jpg): flat on the ground, face down, head
## pointing the way the character was travelling, limbs collapsed.
##
## It is the only pose in the game that is WIDER THAN IT IS TALL -- roughly
## 26 x 9 against the standing figure's 18 x 28 -- which is the whole reason it
## works at this size. No other state can be mistaken for it even at 5 mm,
## without reading a single pixel of detail.
##
## The collider does not change and is not consulted: the body is disabled for
## the 0.55 s this is on screen, so the drawing is free to lie outside the
## 18 x 28 box exactly as the scarf and the sword already do.
func _prone_parts() -> Array:
	var plate := Color("1f3a6e")
	var shade := Color("16233d")
	var visor := Color("7fe3ff")
	var glint := Color("d8f7ff")
	var scarf := Color("8a5cf0")
	var steel := Color("4a5468")
	var out: Array = []
	# Far leg and boot, trailing behind.
	_pr(out, shade, true, -13.0, -6.0, 7.0, 3.0)
	_pr(out, steel, true, -16.0, -6.2, 3.5, 2.6)
	# Near leg and boot, lower: the legs have fallen apart rather than stacked.
	_pr(out, plate, true, -12.5, -3.0, 7.0, 3.0)
	_pr(out, steel, true, -15.5, -3.0, 3.5, 2.6)
	# Torso lying on its front, with the darker abdomen and the sash across it.
	_pr(out, plate, true, -7.0, -7.0, 9.0, 7.0)
	_pr(out, shade, false, -6.0, -4.0, 4.5, 3.0)
	_pr(out, scarf, false, -6.4, -6.2, 1.4, 5.4)
	# Near arm folded back under the chest.
	_pr(out, shade, true, -5.0, -2.2, 5.0, 2.2)
	# Far arm thrown forward along the floor, gauntlet open.
	_pr(out, plate, true, 1.0, -2.4, 7.0, 2.4)
	_pr(out, steel, true, 7.0, -2.6, 3.0, 2.6)
	# Head. The visor is a band along the BOTTOM edge, because the face is in
	# the floor; that single inversion is what says "face down" rather than
	# "asleep on its side".
	_pr(out, plate, true, 2.0, -7.2, 8.0, 5.4)
	_pp(out, shade, true, PackedVector2Array([
		Vector2(2.0, -7.2), Vector2(-1.6, -8.6), Vector2(2.0, -5.2)]))
	_pr(out, visor, false, 4.6, -3.4, 5.0, 1.4)
	_pr(out, glint, false, 8.4, -3.4, 1.2, 1.4)
	return out

func _pr(out: Array, c: Color, rim: bool, x: float, y: float, w: float, h: float) -> void:
	out.append([0, c, rim, x, y, w, h])

func _pp(out: Array, c: Color, rim: bool, pts: PackedVector2Array) -> void:
	out.append([1, c, rim, pts])

func _draw() -> void:
	# Original geometric art drawn with Godot vector calls — nothing imported,
	# traced, or derived from an existing commercial character. Deep-blue
	# armour, a light-blue visor slit that reads the facing direction, a purple
	# scarf that trails travel, and a back-slung blade that is drawn either
	# sheathed or swung, never both (CHANGE-BRIEF 0.3.0 P6).
	#
	# Collider contract: the 18x28 box spans x -9..9, y -28..0. The torso, helm,
	# shoulders and legs stay within its width -- the 1 px rim added in
	# revision 1.3 puts a single pixel outside it at x -10..10, which is
	# decoration and carries no hitbox, exactly like the scarf and the sword.
	# Measured extents are recorded in CHANGE-BRIEF revision 0.2.0.
	var plate := Color("1f3a6e")
	var shade := Color("16233d")
	var visor := Color("7fe3ff")
	var glint := Color("d8f7ff")
	var scarf := Color("8a5cf0")
	var scarf_tip := Color("6a3fbf")
	var steel := Color("4a5468")
	var steel_dark := Color("2a3246")
	var steel_edge := Color("9aa7bd")
	var grounded := is_on_floor()
	var stride: float = sin(float(tick) * 0.7) * 2.0 if grounded and absf(velocity.x) > 8.0 else 0.0
	var flutter: float = sin(float(tick) * 0.45) * 2.0
	var trail: float = 12.0 if grounded else 15.0
	var phase := attack_phase()

	# Revision 1.4 rebuilds the body as a PARTS LIST instead of a hand-ordered
	# sequence of draw calls, for one reason: the rim pass and the body are now
	# generated from the same array, so a part can never be painted without its
	# rim or rimmed without being painted. The old code duplicated eight shapes
	# in two places and nothing stopped them drifting.
	var sprite: Texture2D = pose_tex.get(pose_key())
	if sprite != null:
		_draw_sprite(sprite, phase)
		return

	var parts: Array = _body_parts(stride, grounded, phase)

	# Rim pass (CONCEPT revision 1.3). On the cream backdrop the body read at
	# 10.03:1 and the dark `shade` shapes did the separating. Against a dungeon
	# wall the body is 1.60:1 and `shade` is 1.14:1, so the dark shading now
	# separates the character from nothing. A 1 px light halo is laid down
	# under everything; the body paints over its middle and only the rim
	# survives. The colour is steel_edge, already one of the eight -- 7.31:1
	# against the wall and 4.57:1 against the plate, so it reads against the
	# background AND against the body it outlines.
	# Only parts flagged as silhouette-forming are rimmed. Rimming everything
	# put a light edge around the visor, the belt and the abdomen as well, and
	# on a 3 px limb a 1 px halo on each side leaves 1 px of armour: the figure
	# came out looking like grey pipework. Interior detail is separated by
	# VALUE instead -- see _body_parts.
	for part in parts:
		if not part[2]:
			continue
		if part[0] == 0:
			_mrect_o(part[3], part[4], part[5], part[6])
		else:
			_mpoly_o(part[3])

	if death_pose:
		# The blade has skidded on past the body, and the scarf has settled over
		# the legs. Both are drawn flat: nothing about this pose should still be
		# standing up.
		_mpoly(_bar(Vector2(13.0, -1.1), Vector2(23.0, -0.7), 1.3), steel)
		_mpoly(_bar(Vector2(14.0, -1.1), Vector2(23.0, -0.7), 0.5), steel_edge)
		_mpoly(PackedVector2Array([
			Vector2(-6.0, -6.4), Vector2(-6.0, -3.4),
			Vector2(-17.0, -5.0), Vector2(-16.0, -7.4),
		]), scarf)
		_mpoly(PackedVector2Array([
			Vector2(-17.0, -5.0), Vector2(-16.0, -7.4), Vector2(-21.0, -6.6),
		]), scarf_tip)
	elif phase == 0:
		# Sheathed: drawn first so the body occludes its middle and only the
		# grip and the scabbard tip protrude, which is what makes it read as
		# carried rather than held.
		var hilt := Vector2(-9.0, -32.0)
		var tip := Vector2(11.0, -4.0)
		var guard := hilt.lerp(tip, 0.22)
		var perp := (tip - hilt).orthogonal().normalized()
		_mpoly(_bar(guard, tip, 1.7), steel)
		_mpoly(_bar(guard.lerp(tip, 0.10), tip, 0.6), steel_edge)
		_mpoly(_bar(hilt, guard, 1.3), steel_dark)
		_mpoly(_bar(hilt.lerp(guard, 0.35), hilt.lerp(guard, 0.65), 1.4), scarf_tip)
		_mpoly(_bar(guard + perp * 2.9, guard - perp * 2.9, 0.9), steel_dark)

	# Scarf next: over the blade's middle, under the body. Skipped when prone --
	# that pose draws its own, lying down.
	if not death_pose:
		_mpoly(PackedVector2Array([
			Vector2(-2.0, -22.0), Vector2(-2.0, -16.0),
			Vector2(-trail + 2.0, -18.0 + flutter), Vector2(-trail, -23.0 + flutter),
		]), scarf)
		_mpoly(PackedVector2Array([
			Vector2(-trail + 2.0, -18.0 + flutter), Vector2(-trail, -23.0 + flutter),
			Vector2(-trail - 4.0, -20.0 + flutter * 1.5),
		]), scarf_tip)

	for part in parts:
		if part[0] == 0:
			_mrect(part[3], part[4], part[5], part[6], part[1])
		else:
			_mpoly(part[3], part[1])

	if phase != 0 and not death_pose:
		_draw_swing()

## The swung blade, over the body, from the same pivot/angle/reach the hitbox
## uses. The arc wedge only appears once the swing is LIVE, so the bright sweep
## marks exactly the ticks that can kill. One copy, shared by the sprite path
## and the code-drawn fallback, so the two cannot disagree about the blade.
func _draw_swing() -> void:
	var steel := Color("4a5468")
	var steel_dark := Color("2a3246")
	var steel_edge := Color("9aa7bd")
	var a := ATTACK_PIVOT
	var b := attack_tip()
	if attack_phase() >= 2:
		var wedge := PackedVector2Array()
		wedge.append(a)
		var samples := 7
		for i in range(samples + 1):
			var t: float = lerpf(ATTACK_ANGLE_START, attack_angle(), float(i) / float(samples))
			wedge.append(a + Vector2.from_angle(t) * tuning.attack_reach)
		_mpoly(wedge, Color(0.49, 0.89, 1.0, 0.28))
	_mpoly(_bar(a - Vector2.from_angle(attack_angle()) * 4.0, a, 1.3), steel_dark)
	_mpoly(_bar(a, b, 2.0), steel)
	_mpoly(_bar(a.lerp(b, 0.14), b, 0.7), steel_edge)
