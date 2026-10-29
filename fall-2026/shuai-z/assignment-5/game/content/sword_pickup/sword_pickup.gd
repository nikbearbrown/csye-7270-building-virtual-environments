class_name SwordPickup
extends Area2D
## The sword-and-shield pickup (PROP-SWORDSHIELD). Rudy's first touch gives him
## the sword form, with one pickup sound. It then stops monitoring and hides; it
## is never freed, because after a death the level calls reset() and it is back
## where it was. Its art (PROP-SWORDSHIELD) is the sword crossed over the shield
## with a warm glow, drawn from props.json's origin at SCALE times the art's
## game size (about 100 px across), so it is seen from afar, floating and
## bobbing a little; it gets no outline, which would follow the glow. The touch
## area grows with it. The origin is on the ground below it.

const SCALE := 1.5 ## times the art's game size (its texture is at 2 px per game px)
const HEIGHT := 76.0 ## px from the ground to its centre
const BOB := 6.0 ## px up and down
const BOB_PERIOD := 1.6 ## s

var taken := false

var _clock := 0.0

@onready var _art: Sprite2D = $Art


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	_clock += delta
	_art.position.y = -HEIGHT + sin(_clock * TAU / BOB_PERIOD) * BOB


## Back where it was, for Rudy to take again.
func reset() -> void:
	taken = false
	visible = true
	set_deferred("monitoring", true)


func _on_body_entered(body: Node2D) -> void:
	if taken or not body is Rudy:
		return
	var rudy := body as Rudy
	if not rudy.can_be_touched() or rudy.gear != Rudy.Gear.NONE:
		return
	taken = true
	set_deferred("monitoring", false)
	visible = false
	rudy.equip_sword()
	Sfx.play(&"pickup")

