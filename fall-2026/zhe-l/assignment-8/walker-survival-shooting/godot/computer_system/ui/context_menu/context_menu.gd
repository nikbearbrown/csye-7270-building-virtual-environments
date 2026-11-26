class_name ContextMenu
extends PopupMenu

const KEY_ID := "id"
const KEY_TEXT := "text"
const KEY_DISABLED := "disabled"

func open_at(items: Array[Dictionary], at_position: Vector2) -> void:
	clear()
	for item in items:
		add_item(item[KEY_TEXT], item[KEY_ID])
		set_item_disabled(get_item_count() - 1, item.get(KEY_DISABLED, false))
	reset_size()
	position = Vector2i(at_position)
	popup()
	position = _fit_inside(position, size)


func _fit_inside(wanted: Vector2i, menu_size: Vector2i) -> Vector2i:
	var area := Rect2i(get_parent().get_viewport().get_visible_rect())
	var result := wanted
	result.x = maxi(area.position.x, mini(wanted.x, area.end.x - menu_size.x))
	result.y = maxi(area.position.y, mini(wanted.y, area.end.y - menu_size.y))
	return result
