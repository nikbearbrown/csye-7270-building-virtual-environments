extends RefCounted
## Shared read-back helpers for the A7 clip tests (tests/test_clip_run.gd, tests/test_clip_lunge.gd). Not a test.
## track_problems() is the published assignment function, verbatim (with its root_node null check). key_problems(),
## step_problems() and half_frame() hold my extra checks.


static func track_problems(player: AnimationPlayer) -> Array[String]:
	var problems: Array[String] = []
	var root := player.get_node_or_null(player.root_node)
	if root == null: problems.append("root_node %s resolves to nothing" % player.root_node); return problems
	for clip_name in player.get_animation_list():
		var clip := player.get_animation(clip_name)
		for t in clip.get_track_count():
			var path := clip.track_get_path(t)
			var node := root.get_node_or_null(NodePath(path.get_concatenated_names()))
			if node == null:
				problems.append("%s track %d: no node at %s" % [clip_name, t, path])
				continue
			if path.get_subname_count() == 0:
				continue
			var sub := path.get_subname(0)
			match clip.track_get_type(t):
				Animation.TYPE_POSITION_3D, Animation.TYPE_ROTATION_3D, Animation.TYPE_SCALE_3D:
					var skeleton := node as Skeleton3D
					if skeleton == null or skeleton.find_bone(sub) == -1:
						problems.append("%s track %d: no bone %s on %s" % [clip_name, t, sub, node.name])
				Animation.TYPE_BLEND_SHAPE:
					var mesh := node as MeshInstance3D
					if mesh == null or mesh.find_blend_shape_by_name(sub) == -1:
						problems.append("%s track %d: no blend shape %s on %s" % [clip_name, t, sub, node.name])
				_:
					if not (sub in node):
						problems.append("%s track %d: %s has no property %s" % [clip_name, t, node.name, sub])
	return problems


## Extra checks of mine, kept apart from the assignment's track_problems(): in every clip of `player`, every track has
## keys, key times are increasing and within 0..length, and each value-track key has the type of the property it sets
## (an int 0 keyed on a float rotation is caught here).
static func key_problems(player: AnimationPlayer) -> Array[String]:
	var out: Array[String] = []
	var root := player.get_node(player.root_node)
	for clip_name in player.get_animation_list():
		var anim := player.get_animation(clip_name)
		for i in anim.get_track_count():
			var path := anim.track_get_path(i)
			var tag := "%s/%d %s" % [clip_name, i, path]
			var keys := anim.track_get_key_count(i)
			if keys == 0:
				out.append("%s: no keys" % tag)
			for k in keys:
				var t := anim.track_get_key_time(i, k)
				if t < -1e-6 or t > anim.length + 1e-6:
					out.append("%s: key %d at %s outside 0..%s" % [tag, k, t, anim.length])
				if k > 0 and t <= anim.track_get_key_time(i, k - 1):
					out.append("%s: key %d not after key %d" % [tag, k, k - 1])
			var node := root.get_node_or_null(NodePath(path.get_concatenated_names()))
			var prop := path.get_concatenated_subnames()
			if node == null or prop.is_empty() or anim.track_get_type(i) != Animation.TYPE_VALUE:
				continue
			var current: Variant = node.get_indexed(NodePath(prop))
			for k in keys:
				var v: Variant = anim.track_get_key_value(i, k)
				if typeof(v) != typeof(current) and not (current == null and v is Object):
					out.append("%s: key %d is %s, property is %s" % [tag, k, type_string(typeof(v)),
						type_string(typeof(current))])
	return out


## Clips of `player` whose `step` is not one frame period at `fps` (is_equal_approx(clip.step, 1.0 / fps)).
static func step_problems(player: AnimationPlayer, fps: float) -> Dictionary:
	var out := {}
	for clip_name in player.get_animation_list():
		var clip := player.get_animation(clip_name)
		if not is_equal_approx(clip.step, 1.0 / fps):
			out[str(clip_name)] = clip.step
	return out


## Key-time tolerance: half a frame period at `fps`. Key times are 32-bit floats; never compare them with ==.
static func half_frame(fps: float) -> float:
	return 0.5 / fps


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
