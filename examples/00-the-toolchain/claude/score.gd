extends CanvasLayer

var left_score := 0
var right_score := 0

@onready var _left_label := $LeftScore as Label
@onready var _right_label := $RightScore as Label

func _ready() -> void:
	get_parent().get_node("LeftWall").area_entered.connect(_on_left_wall)
	get_parent().get_node("RightWall").area_entered.connect(_on_right_wall)
	_refresh()

func _on_left_wall(area: Area2D) -> void:
	if area.name == "Ball":
		right_score += 1
		_refresh()

func _on_right_wall(area: Area2D) -> void:
	if area.name == "Ball":
		left_score += 1
		_refresh()

func _refresh() -> void:
	_left_label.text = str(left_score)
	_right_label.text = str(right_score)
