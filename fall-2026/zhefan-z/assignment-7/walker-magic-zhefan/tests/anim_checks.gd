extends RefCounted
## Shared read-back helper for the A7 clip tests (tests/test_clip_run.gd, tests/test_clip_lunge.gd). Not a test.
## track_problems() follows the assignment's description of the check (its own code is not in this repository):
## resolve every track of a clip from the AnimationPlayer's root node and branch on the track type.


## Every problem found in `anim`'s tracks, as readable strings; empty when every track resolves.
static func track_problems(ap: AnimationPlayer, anim: Animation) -> Array[String]:
	var out: Array[String] = []
	var root := ap.get_node_or_null(ap.root_node)
	if root == null:
		out.append("root_node %s does not resolve" % ap.root_node)
		return out
	for i in anim.get_track_count():
		var path := anim.track_get_path(i)
		var tag := "%s/%d %s" % [anim.resource_name, i, path]
		var node := root.get_node_or_null(NodePath(path.get_concatenated_names()))
		if node == null:
			out.append("%s: no node" % tag)
			continue
		var keys := anim.track_get_key_count(i)
		if keys == 0:
			out.append("%s: no keys" % tag)
		for k in keys:
			var t := anim.track_get_key_time(i, k)
			if t < -1e-6 or t > anim.length + 1e-6:
				out.append("%s: key %d at %s outside 0..%s" % [tag, k, t, anim.length])
			if k > 0 and t <= anim.track_get_key_time(i, k - 1):
				out.append("%s: key %d not after key %d" % [tag, k, k - 1])
		match anim.track_get_type(i):
			Animation.TYPE_VALUE, Animation.TYPE_BEZIER:
				var prop := path.get_concatenated_subnames()
				if prop.is_empty():
					out.append("%s: no property" % tag)
					continue
				var base := path.get_subname(0)
				if not node.get_property_list().any(func(p: Dictionary) -> bool: return p.name == base):
					out.append("%s: %s has no property %s" % [tag, node.get_class(), base])
					continue
				var current: Variant = node.get_indexed(NodePath(prop))
				for k in keys:
					var v: Variant = anim.track_get_key_value(i, k)
					if anim.track_get_type(i) == Animation.TYPE_BEZIER:
						if typeof(current) != TYPE_FLOAT:
							out.append("%s: bezier track on a %s property" % [tag, type_string(typeof(current))])
						break
					if typeof(v) != typeof(current) and not (current == null and v is Object):
						out.append("%s: key %d is %s, property is %s" % [tag, k, type_string(typeof(v)),
							type_string(typeof(current))])
			Animation.TYPE_METHOD:
				for k in keys:
					var m := anim.method_track_get_name(i, k)
					if not node.has_method(m):
						out.append("%s: %s has no method %s" % [tag, node.get_class(), m])
			Animation.TYPE_AUDIO:
				if not (node is AudioStreamPlayer or node is AudioStreamPlayer2D or node is AudioStreamPlayer3D):
					out.append("%s: audio track on a %s" % [tag, node.get_class()])
			Animation.TYPE_ANIMATION:
				if not node is AnimationPlayer:
					out.append("%s: animation track on a %s" % [tag, node.get_class()])
			Animation.TYPE_POSITION_3D, Animation.TYPE_ROTATION_3D, Animation.TYPE_SCALE_3D:
				if not node is Node3D:
					out.append("%s: 3D transform track on a %s" % [tag, node.get_class()])
			Animation.TYPE_BLEND_SHAPE:
				if not node is MeshInstance3D:
					out.append("%s: blend shape track on a %s" % [tag, node.get_class()])
	return out


## Index of the value track at `path` in `anim`, or -1.
static func track(anim: Animation, path: String) -> int:
	return anim.find_track(NodePath(path), Animation.TYPE_VALUE)


## Every AnimationPlayer under `node` (itself included).
static func players(node: Node) -> Array[AnimationPlayer]:
	var out: Array[AnimationPlayer] = []
	if node is AnimationPlayer:
		out.append(node)
	for c in node.get_children():
		out.append_array(players(c))
	return out


## Properties named in `names` that `cls` (with inheritance) does not have, checked with ClassDB on this binary.
static func missing_properties(cls: String, names: Array) -> Array:
	var have := ClassDB.class_get_property_list(cls).map(func(p: Dictionary) -> String: return p.name)
	return names.filter(func(n: String) -> bool: return not n in have)
