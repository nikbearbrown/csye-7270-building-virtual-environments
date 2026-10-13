extends SceneTree
# verify11.gd: what the Inspector is built from. The Inspector draws a group heading for every property-list entry with the GROUP usage
# flag and one row per property, labelled with the property name capitalised. This prints Node2D's property list around "position".
# It does not open the editor, so it confirms the group and the property name, not the look of the panel (editor frame E1 does that).
# Run: godot --headless --path <project dir> --script res://verify11.gd
func _initialize() -> void:
	var n := Node2D.new()
	var rows: Array = []
	var in_transform := false
	for p in n.get_property_list():
		var is_group: bool = (int(p["usage"]) & PROPERTY_USAGE_GROUP) != 0
		var is_editor: bool = (int(p["usage"]) & PROPERTY_USAGE_EDITOR) != 0
		if is_group:
			in_transform = (p["name"] == "Transform")
			rows.append({"group": p["name"]})
		elif in_transform and is_editor:
			rows.append({"property": p["name"], "shown_as": String(p["name"]).capitalize(), "type": type_string(int(p["type"]))})
	print("RESULT " + JSON.stringify({"id": "node2d-inspector-rows", "engine": Engine.get_version_info()["string"], "rows_from_the_Transform_group_on": rows}))
	n.free()
	quit(0)
