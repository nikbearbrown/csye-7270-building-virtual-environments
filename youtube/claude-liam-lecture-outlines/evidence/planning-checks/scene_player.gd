extends Node2D
# scene_player.gd: plays one capture "scene spec" (a small JSON file in scenes/) as a pure function of time.
#   var player = load("res://scene_player.gd").new(); player.setup(spec_dictionary); root.add_child(player); player.at(t)   # t in seconds, any order
# Contract for the capture harness: build the player once, then for frame i call player.at(i / fps), let the frame draw, grab it. Canvas is 1280 x 720.
# Everything animated (uniforms, scale, centre, modulate, visibility, which shader is on, which sheet frame shows) is a keyframe list in the spec:
#   value  ::=  constant | {"keys": [[t, v], ...], "interp": "step" | "linear"}      (default "linear"; use "step" for bools, frames, shader names and the texture filter)
# Scripted input (spec "input": [{"t": 1.0, "key": "SPACE"}]) is pushed once, in the first at(t) whose t has reached the event time; the film labels it "scripted input".
# Spec layout: scenes/*.json and CAPTURE-PLAN.md.
const Lib := preload("res://ol_lib.gd")

var spec: Dictionary = {}
var items: Array = []            # [{"node": CanvasItem, "spec": Dictionary, "mats": {shader name: ShaderMaterial}}]
var holder: Node = null
var fired: Dictionary = {}
var pad_script: Object = null
var input_viewport: Viewport = null   # set when the player lives inside a SubViewport: key events pushed to the root window do not reach nodes inside it

func setup(s: Dictionary) -> void:
	spec = s
	pad_script = load("res://padding_snippet.gd").new()
	var script_path: String = spec.get("script", "")
	if script_path != "":
		holder = Node.new()
		var gd := GDScript.new()
		gd.source_code = FileAccess.get_file_as_string(Lib.film_dir().path_join("evidence/planning-checks/" + script_path))
		gd.reload()
		holder.set_script(gd)
	var first := true
	for sd in spec.get("sprites", []):
		var node: CanvasItem
		if sd.has("frames"):
			var sf := SpriteFrames.new()
			for ft in sd["frames"]:
				sf.add_frame("default", Lib.make_texture(ft, pad_script))
			var an := AnimatedSprite2D.new()
			an.sprite_frames = sf
			node = an
		else:
			var sp := Sprite2D.new()
			sp.texture = Lib.make_texture(sd.get("texture", {}), pad_script)
			if sd.has("hframes"):
				sp.hframes = int(sd["hframes"])
			if sd.has("region"):
				var r: Array = sd["region"]
				sp.region_enabled = true
				sp.region_rect = Rect2(r[0], r[1], r[2], r[3])
			node = sp
		node.name = "Sprite" if (holder != null and first) else str(sd.get("name", "item"))
		node.texture_filter = filter_of(str(value_at(sd.get("filter", "nearest"), 0.0)))
		node.set("centered", false)
		if holder != null and first:
			holder.add_child(node)
		else:
			add_child(node)
		first = false
		items.append({"node": node, "spec": sd, "mats": {}})
	at(0.0)                          # materials and first-frame values are in place before a script's _ready() can look at them
	if holder != null:
		add_child(holder)

func tex_size(node: CanvasItem) -> Vector2:
	if node is Sprite2D:
		var sp := node as Sprite2D
		var w: float = sp.texture.get_width()
		var h: float = sp.texture.get_height()
		if sp.hframes > 1: w /= sp.hframes
		if sp.vframes > 1: h /= sp.vframes
		if sp.region_enabled:
			w = sp.region_rect.size.x; h = sp.region_rect.size.y
		return Vector2(w, h)
	var an := node as AnimatedSprite2D
	var tt: Texture2D = an.sprite_frames.get_frame_texture("default", an.frame)
	return Vector2(tt.get_width(), tt.get_height())

func value_at(v: Variant, t: float) -> Variant:
	if typeof(v) == TYPE_DICTIONARY and v.has("keys"):
		var keys: Array = v["keys"]
		var interp: String = v.get("interp", "linear")
		if t <= keys[0][0]:
			return keys[0][1]
		var prev = keys[0]
		for k in keys:
			if k[0] <= t:
				prev = k
			else:
				if interp == "step":
					return prev[1]
				return _lerp(prev[1], k[1], (t - prev[0]) / maxf(k[0] - prev[0], 0.0001))
		return prev[1]
	return v

func _lerp(a: Variant, b: Variant, f: float) -> Variant:
	if typeof(a) == TYPE_ARRAY:
		var out: Array = []
		for i in range(a.size()):
			out.append(lerpf(a[i], b[i], f))
		return out
	return lerpf(float(a), float(b), f)

func filter_of(name: String) -> CanvasItem.TextureFilter:
	return {"nearest": CanvasItem.TEXTURE_FILTER_NEAREST, "linear": CanvasItem.TEXTURE_FILTER_LINEAR, "default": CanvasItem.TEXTURE_FILTER_PARENT_NODE}.get(name, CanvasItem.TEXTURE_FILTER_NEAREST)

func to_param(pname: String, v: Variant) -> Variant:
	if typeof(v) == TYPE_ARRAY:
		if pname.ends_with("color"):
			return Color(v[0], v[1], v[2], v[3] if v.size() > 3 else 1.0)
		if v.size() == 2: return Vector2(v[0], v[1])
		if v.size() == 3: return Vector3(v[0], v[1], v[2])
		return Vector4(v[0], v[1], v[2], v[3])
	return v

# per-instance uniforms (instance uniform in the shader, CanvasItem.set_instance_shader_parameter): a value for this node only, applied from "instance_from" seconds on
func _instance_values(node: CanvasItem, sd: Dictionary, t: float) -> void:
	if not sd.has("instance_uniforms") or t < float(sd.get("instance_from", 0.0)):
		return
	var iu: Dictionary = sd["instance_uniforms"]
	for k in iu:
		node.set_instance_shader_parameter(k, to_param(k, value_at(iu[k], t)))

func at(t: float) -> void:
	for it in items:
		var node: CanvasItem = it["node"]
		var sd: Dictionary = it["spec"]
		node.visible = bool(value_at(sd.get("visible", true), t))
		node.texture_filter = filter_of(str(value_at(sd.get("filter", "nearest"), t)))      # a keyed filter (step) lets one sprite change filter mid-clip
		var m = value_at(sd.get("modulate", [1, 1, 1, 1]), t)
		node.modulate = Color(m[0], m[1], m[2], m[3] if m.size() > 3 else 1.0)
		if sd.has("frame"):
			node.set("frame", int(value_at(sd["frame"], t)))
		var sc := float(value_at(sd.get("scale", 1.0), t))
		node.scale = Vector2(sc, sc)
		var c = value_at(sd.get("center", [640, 360]), t)
		var sz := tex_size(node) * sc
		node.position = Vector2(roundf(c[0] - sz.x / 2.0), roundf(c[1] - sz.y / 2.0))
		var share: String = sd.get("share_with", "")
		if share != "" and t < float(sd.get("own_from", 1.0e9)):
			for other in items:                       # two nodes using one material resource, as instanced scenes do by default
				if str(other["spec"].get("name", "")) == share:
					node.material = (other["node"] as CanvasItem).material
			_instance_values(node, sd, t)
			continue
		var shader_name = value_at(sd["shader_at"], t) if sd.has("shader_at") else sd.get("shader", null)
		if shader_name == null or shader_name == "":
			node.material = null
		else:
			var mats: Dictionary = it["mats"]
			if not mats.has(shader_name):
				mats[shader_name] = Lib.material(shader_name)
			var mat: ShaderMaterial = mats[shader_name]
			if node.material != mat:
				node.material = mat
			var uni: Dictionary = sd.get("uniforms", {})
			for k in uni:
				var keyed: bool = typeof(uni[k]) == TYPE_DICTIONARY and uni[k].has("keys")
				var seen: String = "_set_" + shader_name + k
				if holder != null and not keyed and mats.get(seen, false):
					continue            # in a scripted scene the script owns a constant uniform after the first frame
				mat.set_shader_parameter(k, to_param(k, value_at(uni[k], t)))
				mats[seen] = true
		_instance_values(node, sd, t)
	for ev in spec.get("input", []):
		var key: String = str(ev["t"]) + str(ev["key"])
		if t >= float(ev["t"]) and not fired.has(key) and is_inside_tree():
			fired[key] = true
			var kc: int = {"SPACE": KEY_SPACE, "ENTER": KEY_ENTER, "A": KEY_A}.get(ev["key"], KEY_SPACE)
			var down := InputEventKey.new(); down.keycode = kc as Key; down.physical_keycode = kc as Key; down.pressed = true
			var target: Viewport = input_viewport if input_viewport != null else get_tree().root
			target.push_input(down)
			var up := InputEventKey.new(); up.keycode = kc as Key; up.physical_keycode = kc as Key; up.pressed = false
			target.push_input(up)
