extends CanvasLayer
## Everything the player needs to understand the slice with the sound off:
## how many days are left, how close to being seen they are, how cold the house
## is getting, and whether audio is muted.

@onready var _days: Label = $Days
@onready var _recognition: Label = $Recognition
@onready var _frost: ColorRect = $Frost
@onready var _mutes: Label = $Mutes
@onready var _banner: Label = $Banner
@onready var _hint: Label = $Hint
@onready var _opening: Label = $Opening
@onready var _note: Label = $Note
var _note_tween: Tween
var _hint_tween: Tween
var _cue_tween: Tween
@onready var _cue: Label = $Cue


func _ready() -> void:
	_banner.visible = false
	_opening.visible = false
	_note.visible = false
	_cue.visible = false
	_frost.color = Color(0.78, 0.86, 0.92, 0.0)


func set_days(days_left: int, total: int) -> void:
	_days.text = "%d NIGHTS LEFT" % days_left
	# A visible tear: the label jolts when a day is lost, so the cost reads muted.
	var tween := create_tween()
	_days.scale = Vector2(1.12, 1.12)
	tween.tween_property(_days, "scale", Vector2.ONE, 0.35).set_trans(Tween.TRANS_BACK)


func set_recognition(recognition: int, needed: int) -> void:
	var filled := "".rpad(0)
	for i in needed:
		filled += "●  " if i < recognition else "○  "
	_recognition.text = "THINGS OF HIS, FOUND   " + filled


func set_frost(level: float) -> void:
	var tween := create_tween()
	tween.tween_property(_frost, "color:a", clampf(level, 0.0, 1.0) * 0.38, 0.8)


func set_mutes(music_muted: bool, sfx_muted: bool) -> void:
	var parts := []
	if music_muted:
		parts.append("MUSIC MUTED (M)")
	if sfx_muted:
		parts.append("SFX MUTED (N)")
	_mutes.text = "   ".join(parts)


## One beat of the counter per heartbeat, so the sound and the number are
## visibly the same thing: the night running out.
func pulse_days() -> void:
	var tween := create_tween()
	_days.modulate = Color(1.0, 0.72, 0.62, 1.0)
	_days.scale = Vector2(1.06, 1.06)
	tween.set_parallel(true)
	tween.tween_property(_days, "modulate", Color(0.86, 0.88, 0.9, 0.92), 0.45)
	tween.tween_property(_days, "scale", Vector2.ONE, 0.45)


## The opening: three lines over the house as it really is, shown once.
func show_opening(lines: Array, world) -> void:
	_opening.visible = true
	_opening.modulate.a = 0.0
	for i in lines.size():
		if world._skip_opening:
			break
		_opening.text = "\n".join(lines.slice(0, i + 1))
		var t := create_tween()
		t.tween_property(_opening, "modulate:a", 1.0, 0.55)
		await t.finished
		await world._hold(0.85)
	if world._skip_opening:
		return
	var out := create_tween()
	out.tween_property(_opening, "modulate:a", 0.0, 0.9)
	await out.finished
	_opening.visible = false


func hide_opening() -> void:
	_opening.visible = false
	_note.visible = false
	_cue.visible = false


## A line of his, held for a few seconds and then let go. Deliberately low on
## the screen and quiet, so it reads as a thought rather than an instruction.
func show_note(text: String) -> void:
	_note.text = text
	_note.visible = true
	if _note_tween and is_instance_valid(_note_tween):
		_note_tween.kill()
	_note.modulate.a = 0.0
	_note_tween = create_tween()
	_note_tween.tween_property(_note, "modulate:a", 1.0, 0.8)
	_note_tween.tween_interval(3.4)
	_note_tween.tween_property(_note, "modulate:a", 0.0, 1.2)
	_note_tween.tween_callback(func(): _note.visible = false)


## A prompt that appears only when it can be acted on, sits next to the thing
## it refers to, and goes away once the player has used it. A hint line that
## lists every control at all times is read once and then ignored, which is how
## a playtester can finish a level without ever learning its central verb.
func set_hint(text: String) -> void:
	if _hint.text == text:
		return
	_hint.text = text
	if _hint_tween and is_instance_valid(_hint_tween):
		_hint_tween.kill()
	_hint.modulate.a = 0.0
	_hint_tween = create_tween()
	_hint_tween.tween_property(_hint, "modulate:a", 1.0 if text != "" else 0.0, 0.4)


## The key you need, floating beside the thing that needs it.
func show_cue(text: String, at: Vector2) -> void:
	_cue.text = text
	_cue.position = at - Vector2(_cue.size.x * 0.5, 120.0)
	if not _cue.visible:
		_cue.visible = true
		_cue.modulate.a = 0.0
		if _cue_tween and is_instance_valid(_cue_tween):
			_cue_tween.kill()
		_cue_tween = create_tween()
		_cue_tween.tween_property(_cue, "modulate:a", 1.0, 0.35)
	var pulse := 0.78 + 0.22 * sin(Time.get_ticks_msec() / 220.0)
	_cue.modulate = Color(1.0, 0.93, 0.74, _cue.modulate.a * pulse / maxf(0.01, _cue.modulate.a))


func hide_cue() -> void:
	if not _cue.visible:
		return
	if _cue_tween and is_instance_valid(_cue_tween):
		_cue_tween.kill()
	_cue_tween = create_tween()
	_cue_tween.tween_property(_cue, "modulate:a", 0.0, 0.3)
	_cue_tween.tween_callback(func(): _cue.visible = false)


func show_banner(text: String) -> void:
	_banner.text = text
	_banner.visible = true
	_banner.modulate.a = 0.0
	var tween := create_tween()
	tween.tween_property(_banner, "modulate:a", 1.0, 0.9)
