@tool
extends EditorPlugin
## Editor driver for the godot-shaders series (editor-capture pilot).
##
## It runs INSIDE the real Godot editor. When the editor was started with Movie Maker (--write-movie), every step below happens
## in front of the recorder, so the recorded frames are the editor's own window showing exactly the Inspector / shader editor
## state the script asked for. No human clicks.
##
## Input:  res://state_script.json  (override with env DRIVER_STATE_SCRIPT). A JSON list of steps, or {"steps": [...], "boot_frames": N}.
## Output: env DRIVER_LOG (default user://states.json): every step, every mark (NAME -> Engine.get_frames_drawn()), dumps, errors.
##
## Steps (all have "op"; any step may carry "settle": N to wait N frames after it):
##   wait_frames {n}                         open_scene {path}                     select_node {node, via: selection|edit_node}   select_nodes {nodes:[..]}
##   inspect_object {node, target, for_property, inspector_only}                  edit_resource {node, target}
##   set_property {node, target, property, value | value_vec2 | value_color, undo}  assign_new {node, property, class}
##   edit_resource_file {path}               assign_shader_file {node, path}         set_main_screen {name}                scroll_inspector {property, object, align, margin | y | to}
##   unfold_resource {property, object}      press {find:{class,text,name,prop}, within}   open_picker_menu {property, object}
##   dump_popup {name}                       pick_menu_item {text, contains}       close_popups {}      focus_menu_item {text, contains} (the hover highlight)
##   expand_all {}  collapse_all {}          set_editor_setting {name, value}      log {text}
##   mark {name}                             dump_inspector {name}                 dump_tree {name, root, max_depth, only_visible}
##   probe_window {name}                     window_set_size {w, h}                unfold_group {property, object}
##   click_control {find:{class,text,name,prop}, within, index, dx, dy}            click_at {x, y}   (scripted mouse input through the real GUI path)
##   menu_item {button, item}                hide_bottom_panel {}                  dump_scene_tree {name}      dump_object {find:{class,name}, name}
##   dock_split {name, offsets:[..]} | {name, offset}                              select_tab {text}
##   (follow-up ops) menubar_open {menu} | menubar_pick {menu, item|contains} | dump_menubar {name} | dump_texts {within, name, max_depth}
##   select_tree_item {within, path:[..], tree_index} | toggle_check {within, property|text, value} | close_dialog {within} | dump_rows {within, name}
##   editor_setting_info {names:[..]}   set_toggle {within, text, value}   (open_option_button also takes within + index)
## A script object may also carry {"window": [w, h]}: the driver sizes the editor window to w x h BEFORE the flash and waits "window_settle" frames.
## `mark` always ends the frame it ran in: the step after a mark runs on the next frame, so nothing can change the marked picture.
## "target" is node (default) | material | shader | scene_root | chain (+ "chain": ["material", "shader_parameter/noise_tex", ...]);  "node" is a path relative to the edited scene root ("." = root).
## For rows inside a resource view ("object" key of unfold_group / unfold_resource / open_picker_menu / scroll_inspector) the same "target" and "chain" keys name the resource.
## FRAME NUMBERS: the movie file index is NOT Engine.get_frames_drawn() (the editor skips drawing while idle, so that counter falls behind).
## The movie writer writes one file per main-loop iteration, so the file index is Engine.get_process_frames(); every mark logs both.
## The first thing the driver does is flash the whole editor magenta for 2 frames: the helper finds the flash in the PNG sequence and checks
## that it sits at the logged process frame. It happens before any mark, so it is never in a marked frame.

const SCRIPT_PATH_DEFAULT := "res://state_script.json"
const FLASH_COLOR := Color(1.0, 0.0, 1.0, 1.0)

var _steps: Array = []
var _idx := 0
var _wait := 0
var _poll: Dictionary = {}
var _booted := false
var _boot_count := 0
var _boot_frames := 25
var _window: Array = []
var _window_settle := 40
var _window_done := false
var _finished := false
var _quit_in := -1
var _flash: ColorRect = null
var _flash_free_at := -1
var _requeued := false
var _retries := {}   # step index -> how many times it was re-run because something it needs was not on screen yet
var _step_rec := {}  # step index -> its log record
var _log: Dictionary = {}
var _log_path := ""
var _script_path := ""
var _t0_ms := 0

func _enter_tree() -> void:
	_script_path = OS.get_environment("DRIVER_STATE_SCRIPT")
	if _script_path == "":
		_script_path = SCRIPT_PATH_DEFAULT
	if not FileAccess.file_exists(_script_path):
		return # nothing to drive: the plugin stays inert
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(_script_path))
	if parsed is Dictionary:
		_steps = parsed.get("steps", [])
		_boot_frames = int(parsed.get("boot_frames", _boot_frames))
		_window = parsed.get("window", [])
		_window_settle = int(parsed.get("window_settle", _window_settle))
	elif parsed is Array:
		_steps = parsed
	else:
		push_error("DRIVER: state script is not valid JSON: " + _script_path)
		return
	_log_path = OS.get_environment("DRIVER_LOG")
	if _log_path == "":
		_log_path = "user://states.json"
	_log = {
		"driver_version": "1.0",
		"godot": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(),
		"state_script": _script_path,
		"steps": [], "marks": {}, "dumps": [], "errors": [], "notes": [],
	}
	_t0_ms = Time.get_ticks_msec()
	set_process(true)
	print("DRIVER: loaded %d steps from %s; log -> %s" % [_steps.size(), _script_path, _log_path])

func _exit_tree() -> void:
	if _flash and is_instance_valid(_flash):
		_flash.queue_free()

# ---------------------------------------------------------------------------------------------------------------- main loop

func _process(_delta: float) -> void:
	if _steps.is_empty() and not _finished:
		return
	var frame := Engine.get_frames_drawn()
	if _quit_in >= 0:
		_quit_in -= 1
		if _quit_in < 0:
			print("DRIVER: quitting at frame %d" % frame)
			get_tree().quit()
		return
	if _flash and frame >= _flash_free_at:
		_flash.queue_free()
		_flash = null
	if not _booted:
		if EditorInterface.get_resource_filesystem().is_scanning():
			return
		_boot_count += 1
		if _boot_count < _boot_frames:
			return
		if not _window.is_empty() and not _window_done:
			_window_done = true
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
			DisplayServer.window_set_size(Vector2i(int(_window[0]), int(_window[1])))
			_note("boot: window_set_size(%d, %d) -> window_get_size = %s" % [int(_window[0]), int(_window[1]), str(DisplayServer.window_get_size())])
			_wait = _window_settle
			return
		_booted = true
		_log["boot_done_frame"] = frame
		_log["window_size"] = [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y]
		_log["content_scale_factor"] = get_tree().root.content_scale_factor
		_log["editor_scale"] = EditorInterface.get_editor_scale()
		_log["gui_embed_subwindows"] = get_tree().root.get("gui_embed_subwindows")
		_start_flash(frame)
		return
	if _wait > 0:
		_wait -= 1
		return
	if not _poll.is_empty():
		_poll["waited"] = int(_poll["waited"]) + 1
		var ok: bool = _poll["fn"].call()
		if ok:
			_note("poll '%s' satisfied after %d frames" % [_poll["desc"], _poll["waited"]])
			_poll = {}
		elif int(_poll["waited"]) >= int(_poll["max"]):
			_err("poll '%s' TIMED OUT after %d frames" % [_poll["desc"], _poll["waited"]])
			_poll = {}
		else:
			return
	while _idx < _steps.size() and _wait == 0 and _poll.is_empty():
		var step: Dictionary = _steps[_idx]
		_idx += 1
		_run_step(step)
	if _idx >= _steps.size() and _wait == 0 and _poll.is_empty() and not _finished:
		_finish()

func _start_flash(frame: int) -> void:
	_flash = ColorRect.new()
	_flash.color = FLASH_COLOR
	_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_flash.set_anchors_preset(Control.PRESET_FULL_RECT)
	EditorInterface.get_base_control().add_child(_flash)
	_flash_free_at = frame + 2
	_log["flash"] = {"frame": frame, "process_frame": Engine.get_process_frames(), "frames": 2, "color": "#ff00ff"}
	_wait = 4 # let the flash end and the editor repaint before the first step
	print("DRIVER: flash at frame %d" % frame)

func _finish() -> void:
	_finished = true
	_log["finished_frame"] = Engine.get_frames_drawn()
	_log["elapsed_ms"] = Time.get_ticks_msec() - _t0_ms
	_write_log()
	print("DRIVER: finished at frame %d, %d marks, %d errors" % [Engine.get_frames_drawn(), _log["marks"].size(), _log["errors"].size()])
	_quit_in = 6 # a few idle frames so the last mark's frame is certainly written

func _write_log() -> void:
	var f := FileAccess.open(_log_path, FileAccess.WRITE)
	if f == null:
		push_error("DRIVER: cannot write log " + _log_path)
		return
	f.store_string(JSON.stringify(_log, "  "))
	f.close()

func _note(t: String) -> void:
	_log["notes"].append({"frame": Engine.get_frames_drawn(), "text": t})
	print("DRIVER: ", t)

func _not_ready(msg: String, max_tries: int = 40) -> void:
	# An op calls this when what it needs is not there yet (a row, a popup, a dialog): the step runs again two frames later, up to
	# max_tries times, then the error is logged. The editor builds its UI over several frames, so this is the normal case at times.
	var key := _idx - 1
	var n: int = int(_retries.get(key, 0)) + 1
	_retries[key] = n
	if n <= max_tries:
		_idx = key
		_wait = 1
		_requeued = true
	else:
		_err("%s (gave up after %d tries)" % [msg, max_tries])
		_idx = key + 1

func _err(t: String) -> void:
	_log["errors"].append({"frame": Engine.get_frames_drawn(), "step": _idx - 1, "text": t})
	print("DRIVER ERROR: ", t)

# ------------------------------------------------------------------------------------------------------------------- helpers

func _scene_root() -> Node:
	return EditorInterface.get_edited_scene_root()

func _node(path: String) -> Node:
	var root := _scene_root()
	if root == null:
		return null
	if path == "" or path == ".":
		return root
	return root.get_node_or_null(path)

func _resolve(step: Dictionary) -> Object:
	var n := _node(String(step.get("node", ".")))
	if n == null:
		_err("no node '%s' in the edited scene" % String(step.get("node", ".")))
		return null
	match String(step.get("target", "node")):
		"node":
			return n
		"scene_root":
			return _scene_root()
		"material":
			var m = n.get("material")
			if m == null:
				_err("node '%s' has no material" % n.name)
			return m
		"shader":
			var m2 = n.get("material")
			if m2 == null or m2.get("shader") == null:
				_err("node '%s' has no material.shader" % n.name)
				return null
			return m2.get("shader")
		"chain":
			# follow a list of property names from the node: ["material", "shader_parameter/noise_tex", "noise"]
			var cur: Variant = n
			for pn in step.get("chain", []):
				if cur == null or not (cur is Object):
					_err("chain: '%s' reached a non-object" % str(pn))
					return null
				cur = (cur as Object).get(String(pn))
			if cur == null:
				_err("chain %s ended at null" % str(step.get("chain", [])))
				return null
			return cur
	_err("unknown target '%s'" % String(step.get("target", "node")))
	return null

func _desc(o: Object) -> Dictionary:
	if o == null:
		return {"class": null}
	var d := {"class": o.get_class()}
	if o is Node:
		d["name"] = String(o.name)
	if o is Resource:
		d["resource_path"] = o.resource_path
		d["resource_name"] = o.resource_name
	return d

func _rect(c: Control) -> Array:
	var s: float = get_tree().root.content_scale_factor
	return [int(round(c.global_position.x * s)), int(round(c.global_position.y * s)), int(round(c.size.x * s)), int(round(c.size.y * s))]

func _collect(root: Node, pred: Callable, out: Array, max_depth: int = 40, depth: int = 0) -> void:
	if depth > max_depth:
		return
	for c in root.get_children():
		if pred.call(c):
			out.append(c)
		_collect(c, pred, out, max_depth, depth + 1)

func _find_prop(prop: String, obj: Object = null) -> EditorProperty:
	var found: Array = []
	_collect(EditorInterface.get_inspector(), func(n): return n is EditorProperty and String(n.get_edited_property()) == prop and (obj == null or n.get_edited_object() == obj), found)
	for p in found:
		if p.is_visible_in_tree():
			return p
	return found[0] if found.size() > 0 else null

func _refresh_inspector() -> void:
	var props: Array = []
	_collect(EditorInterface.get_inspector(), func(n): return n is EditorProperty, props)
	for p in props:
		p.update_property()

func _value(step: Dictionary) -> Variant:
	if step.has("value_vec2"):
		var a: Array = step["value_vec2"]
		return Vector2(a[0], a[1])
	if step.has("value_color"):
		return Color(String(step["value_color"]))
	return step.get("value")

func _open_windows() -> Array:
	# every visible Window of the editor (dialogs, popups) with its place in the editor window; embedded ones carry the decoration size too
	var wins: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is Window and n.visible, wins, 80)
	var out := []
	for w in wins:
		var e := {"class": w.get_class(), "title": w.title if w.get("title") != null else "", "embedded": w.is_embedded(), "position": [w.position.x, w.position.y], "size": [w.size.x, w.size.y]}
		if w is AcceptDialog:
			e["dialog_text"] = w.dialog_text
		if w.is_embedded():
			e["title_height"] = w.get_theme_constant("title_height")
			var sb: StyleBox = w.get_theme_stylebox("embedded_border")
			if sb != null:
				e["border"] = [sb.get_margin(SIDE_LEFT), sb.get_margin(SIDE_TOP), sb.get_margin(SIDE_RIGHT), sb.get_margin(SIDE_BOTTOM)]
		out.append(e)
	return out

func _state_snapshot() -> Dictionary:
	var insp := EditorInterface.get_inspector()
	var sel := []
	for n in EditorInterface.get_selection().get_selected_nodes():
		sel.append(String(n.name))
	var root := _scene_root()
	return {
		"edited_object": _desc(insp.get_edited_object()),
		"inspector_scroll": insp.scroll_vertical,
		"inspector_rect_px": _rect(insp),
		"inspector_dock_rect_px": _dock_rect(),
		"open_windows": _open_windows(),
		"selected_nodes": sel,
		"scene": root.scene_file_path if root else "",
		"open_scenes": EditorInterface.get_open_scenes(),
	}

# --------------------------------------------------------------------------------------------------------------------- steps

func _run_step(step: Dictionary) -> void:
	var op := String(step.get("op", ""))
	var step_index := _idx - 1
	var rec: Dictionary
	if _step_rec.has(_idx - 1):
		rec = _step_rec[_idx - 1]
	else:
		rec = {"i": _idx - 1, "op": op, "frame": Engine.get_frames_drawn(), "process_frame": Engine.get_process_frames()}
		for k in step.keys():
			if k != "op":
				rec[k] = step[k]
		_log["steps"].append(rec)
		_step_rec[_idx - 1] = rec
	var errs_before: int = _log["errors"].size()
	match op:
		"wait_frames":
			_wait = int(step.get("n", 1))
		"open_scene":
			var path := String(step["path"])
			EditorInterface.open_scene_from_path(path)
			var scene_is_open := func() -> bool:
				var r := _scene_root()
				return r != null and r.scene_file_path == path
			_poll = {"desc": "scene open " + path, "waited": 0, "max": 150, "fn": scene_is_open}
		"select_node":
			var n := _node(String(step.get("node", ".")))
			if n == null:
				_err("select_node: no node '%s'" % String(step.get("node", ".")))
			elif String(step.get("via", "selection")) == "edit_node":
				EditorInterface.edit_node(n)
			else:
				EditorInterface.get_selection().clear()
				EditorInterface.get_selection().add_node(n)
		"select_nodes":
			EditorInterface.get_selection().clear()
			for np in step.get("nodes", []):
				var nn := _node(String(np))
				if nn == null:
					_err("select_nodes: no node '%s'" % String(np))
				else:
					EditorInterface.get_selection().add_node(nn)
		"inspect_object":
			var o := _resolve(step)
			if o != null:
				EditorInterface.inspect_object(o, String(step.get("for_property", "")), bool(step.get("inspector_only", false)))
		"edit_resource":
			var r2 := _resolve(step)
			if r2 is Resource:
				EditorInterface.edit_resource(r2)
			else:
				_err("edit_resource: target is not a Resource")
		"set_property":
			var o2 := _resolve(step)
			if o2 != null:
				var prop := String(step["property"])
				var val = _value(step)
				var old = o2.get(prop)
				if bool(step.get("undo", false)):
					var ur := EditorInterface.get_editor_undo_redo()
					ur.create_action("Driver: set " + prop)
					ur.add_do_property(o2, prop, val)
					ur.add_undo_property(o2, prop, old)
					ur.commit_action()
				else:
					o2.set(prop, val)
				_refresh_inspector()
				_note("set %s.%s: %s -> %s (read back: %s)" % [o2.get_class(), prop, str(old), str(val), str(o2.get(prop))])
		"assign_new":
			var n2 := _node(String(step.get("node", ".")))
			if n2 == null:
				_err("assign_new: no node")
			else:
				var inst = ClassDB.instantiate(String(step["class"]))
				n2.set(String(step["property"]), inst)
				_note("assigned new %s to %s.%s" % [String(step["class"]), n2.name, String(step["property"])])
		"assign_shader_file":
			var m = _resolve({"node": step.get("node", "."), "target": "material"})
			if m != null:
				m.set("shader", load(String(step["path"])))
				_note("assigned shader file %s" % String(step["path"]))
		"edit_resource_file":
			var rf = load(String(step["path"]))
			if rf is Resource:
				EditorInterface.edit_resource(rf)
			else:
				_err("edit_resource_file: cannot load %s" % String(step["path"]))
		"set_main_screen":
			EditorInterface.set_main_screen_editor(String(step["name"]))
		"scroll_inspector":
			_op_scroll_inspector(step)
		"unfold_resource":
			_op_unfold_resource(step)
		"press":
			_op_press(step)
		"open_picker_menu":
			_op_open_picker_menu(step)
		"dump_popup":
			_op_dump_popup(step)
		"pick_menu_item":
			_op_pick_menu_item(step)
		"focus_menu_item":
			_op_focus_menu_item(step)
		"close_popups":
			_op_close_popups()
		"expand_all":
			EditorInterface.get_inspector().expand_all_folding()
		"collapse_all":
			EditorInterface.get_inspector().collapse_all_folding()
		"set_editor_setting":
			EditorInterface.get_editor_settings().set_setting(String(step["name"]), step["value"])
		"log":
			_note(String(step.get("text", "")))
		"mark":
			var nm := String(step["name"])
			var m2 := _state_snapshot()
			m2["frame"] = Engine.get_frames_drawn()
			m2["process_frame"] = Engine.get_process_frames()
			m2["step"] = _idx - 1
			_log["marks"][nm] = m2
			_write_log()
			print("DRIVER: mark %s at frame %d" % [nm, Engine.get_frames_drawn()])
			_wait = maxi(_wait, 1)
		"menu_item":
			_op_menu_item(step)
		"hide_bottom_panel":
			hide_bottom_panel()
		"dump_scene_tree":
			_op_dump_scene_tree(step)
		"dump_object":
			_op_dump_object(step)
		"dump_windows":
			_op_dump_windows(step)
		"set_text":
			_op_set_text(step)
		"menubar_open":
			_op_menubar_open(step)
		"menubar_pick":
			_op_menubar_pick(step)
		"dump_menubar":
			_op_dump_menubar(step)
		"dump_texts":
			_op_dump_texts(step)
		"select_tree_item":
			_op_select_tree_item(step)
		"toggle_check":
			_op_toggle_check(step)
		"set_toggle":
			_op_set_toggle(step)
		"close_dialog":
			_op_close_dialog(step)
		"dump_rows":
			_op_dump_rows(step)
		"editor_setting_info":
			_op_editor_setting_info(step)
		"select_option":
			_op_select_option(step)
		"open_option_button":
			_op_open_option_button(step)
		"press_ok":
			_op_press_ok(step)
		"press_cancel":
			_op_press_cancel(step)
		"dock_split":
			_op_dock_split(step)
		"select_tab":
			_op_select_tab(step)
		"probe_window":
			_op_probe_window(step)
		"window_set_size":
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
			DisplayServer.window_set_size(Vector2i(int(step["w"]), int(step["h"])))
			_note("window_set_size(%d, %d) -> window_get_size = %s" % [int(step["w"]), int(step["h"]), str(DisplayServer.window_get_size())])
		"unfold_group":
			_op_unfold_group(step)
		"click_control":
			_op_click_control(step)
		"click_at":
			_click_at(Vector2(float(step["x"]), float(step["y"])))
		"dump_inspector":
			_op_dump_inspector(step)
		"dump_tree":
			_op_dump_tree(step)
		_:
			_err("unknown op '%s'" % op)
	rec["ok"] = (_log["errors"].size() == errs_before)
	rec["retries"] = int(_retries.get(step_index, 0))
	if _requeued:
		_requeued = false # the step will run again; its settle applies after it really ran
		return
	if step.has("settle"):
		_wait = maxi(_wait, int(step["settle"]))

func _op_scroll_inspector(step: Dictionary) -> void:
	var insp := EditorInterface.get_inspector()
	if step.has("y"):
		insp.scroll_vertical = int(step["y"])
		return
	if String(step.get("to", "")) == "top":
		insp.scroll_vertical = 0
		return
	if String(step.get("to", "")) == "bottom":
		insp.scroll_vertical = 100000
		return
	var obj: Object = _object_of(step)
	var p := _find_prop(String(step["property"]), obj)
	if p == null:
		_not_ready("scroll_inspector: no inspector row for '%s'" % String(step["property"]))
		return
	var scale: float = 1.0
	var row_y: float = p.global_position.y - insp.global_position.y # row top relative to the viewport top, current scroll included
	var margin: float = float(step.get("margin", 8))
	match String(step.get("align", "top")):
		"top":
			insp.scroll_vertical = int(insp.scroll_vertical + row_y - margin)
		"center":
			insp.scroll_vertical = int(insp.scroll_vertical + row_y - insp.size.y * 0.5 + p.size.y * 0.5)
		_:
			insp.ensure_control_visible(p)
	_note("scroll_inspector to '%s' (row y in view was %d): scroll_vertical now %d" % [String(step["property"]), int(row_y), insp.scroll_vertical])

func _op_unfold_resource(step: Dictionary) -> void:
	# The click on a resource's thumbnail: the picker emits resource_selected(resource, true) and the property row toggles its inline sub-inspector.
	var picker := _picker_for(step)
	if picker == null:
		return
	var parts := []
	for c in picker.get_children():
		parts.append("%s:%s%s vis=%s %s" % [c.get_class(), c.name, (" text='" + c.text + "'") if c is Button else "", str(c.is_visible_in_tree()) if c is CanvasItem else "-", str(_rect(c)) if c is Control else ""])
	_note("picker children: %s" % " | ".join(parts))
	var res: Resource = picker.get_edited_resource()
	if res == null:
		_err("unfold_resource: the slot is empty")
		return
	picker.resource_selected.emit(res, true)
	# the Inspector may take many frames to switch to the resource (a NoiseTexture2D took about 30): wait until it has
	var t0 := Engine.get_frames_drawn()
	var navigated := func() -> bool:
		if EditorInterface.get_inspector().get_edited_object() == res:
			_note("unfold_resource: the Inspector shows %s after %d frames" % [res.get_class(), Engine.get_frames_drawn() - t0])
			return true
		return false
	_poll = {"desc": "Inspector edits the resource", "waited": 0, "max": 150, "fn": navigated}

func _picker_for(step: Dictionary) -> EditorResourcePicker:
	var obj: Object = _object_of(step)
	var p := _find_prop(String(step["property"]), obj)
	if p == null:
		_not_ready("no inspector row for '%s'" % String(step["property"]))
		return null
	var pickers: Array = []
	_collect(p, func(n): return n is EditorResourcePicker, pickers, 3)
	if pickers.is_empty():
		_not_ready("no EditorResourcePicker in row '%s'" % String(step["property"]))
		return null
	return pickers[0]

func _picker_quiet(step: Dictionary) -> EditorResourcePicker:
	var obj: Object = _object_of(step)
	var p := _find_prop(String(step["property"]), obj)
	if p == null:
		return null
	var pickers: Array = []
	_collect(p, func(n): return n is EditorResourcePicker, pickers, 3)
	return pickers[0] if pickers.size() > 0 else null

func _op_open_picker_menu(step: Dictionary) -> void:
	# Presses the picker's dropdown arrow (the real handler builds the PopupMenu and pops it up). The Inspector can rebuild its rows under us
	# (previews arrive, the layout settles), which frees the picker and its popup: so the picker is looked up again every frame and the
	# arrow is pressed again every 6 frames until a menu of THIS picker is visible.
	var state := {"presses": 0, "last": -100}
	var attempt := func() -> bool:
		var picker := _picker_quiet(step)
		if picker == null:
			return false
		for m in picker.get_children():
			if m is PopupMenu and m.visible:
				return true
		var f := Engine.get_process_frames()
		if f - int(state["last"]) >= 6 and int(state["presses"]) < 8:
			var buttons: Array = picker.get_children().filter(func(c): return c is Button)
			if buttons.size() >= 2:
				state["presses"] = int(state["presses"]) + 1
				state["last"] = f
				_note("open_picker_menu: press %d on %s (arrow rect %s)" % [int(state["presses"]), String(picker.name), str(_rect(buttons[buttons.size() - 1]))])
				buttons[buttons.size() - 1].pressed.emit()
		return false
	_poll = {"desc": "picker menu visible", "waited": 0, "max": 80, "fn": attempt}

func _all_popups() -> Array:
	var found: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is PopupMenu, found, 60)
	return found

func _op_dump_popup(step: Dictionary) -> void:
	var out := []
	for pm in _all_popups():
		if pm.visible:
			var items := []
			for i in pm.item_count:
				items.append({"i": i, "id": pm.get_item_id(i), "text": pm.get_item_text(i), "separator": pm.is_item_separator(i), "disabled": pm.is_item_disabled(i)})
			out.append({"popup": String(pm.name), "parent": String(pm.get_parent().name), "parent_class": pm.get_parent().get_class(), "embedded": pm.is_embedded(), "position": [pm.position.x, pm.position.y], "size": [pm.size.x, pm.size.y], "items": items})
	_log["dumps"].append({"name": String(step.get("name", "popup")), "frame": Engine.get_frames_drawn(), "visible_popups": out})
	_note("dump_popup '%s': %d visible popup(s)" % [String(step.get("name", "popup")), out.size()])

func _op_pick_menu_item(step: Dictionary) -> void:
	var want := String(step.get("text", ""))
	var contains := String(step.get("contains", ""))
	for pm in _all_popups():
		if not pm.visible:
			continue
		for i in pm.item_count:
			var t: String = pm.get_item_text(i)
			if (want != "" and t == want) or (contains != "" and t.contains(contains)):
				_note("pick_menu_item: emitting id_pressed(%d) for '%s'" % [pm.get_item_id(i), t])
				pm.id_pressed.emit(pm.get_item_id(i))
				if bool(step.get("hide", true)):
					pm.hide()
				return
	_not_ready("pick_menu_item: no visible popup item '%s%s'" % [want, contains])

func _op_close_popups() -> void:
	for pm in _all_popups():
		if pm.visible:
			pm.hide()
	# the popups of OptionButtons and MenuButtons are internal children, which the ordinary child walk does not return
	var owners: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is OptionButton or n is MenuButton, owners, 80)
	for o in owners:
		var pop: PopupMenu = o.get_popup()
		if pop != null and pop.visible:
			pop.hide()

func _op_press(step: Dictionary) -> void:
	var f: Dictionary = step.get("find", {})
	var within := String(step.get("within", "base"))
	var root: Node = EditorInterface.get_base_control()
	if within == "inspector":
		root = EditorInterface.get_inspector()
	var found: Array = []
	var pred := func(n) -> bool:
		if f.has("class") and not n.is_class(String(f["class"])):
			return false
		if f.has("text") and not (n is Button and n.text == String(f["text"])):
			return false
		if f.has("name") and String(n.name) != String(f["name"]):
			return false
		if f.has("tooltip") and not (n is Control and n.tooltip_text.contains(String(f["tooltip"]))):
			return false
		return n is Control and n.is_visible_in_tree()
	_collect(root, pred, found, 80)
	if found.is_empty():
		_err("press: nothing matches %s" % str(f))
		return
	var target = found[int(step.get("index", 0))]
	_note("press: %s '%s' (of %d matches)" % [target.get_class(), String(target.name), found.size()])
	if target is BaseButton:
		target.pressed.emit()
	else:
		_err("press: target is not a button")

func _op_dump_inspector(step: Dictionary) -> void:
	var insp := EditorInterface.get_inspector()
	var rows := []
	var props: Array = []
	_collect(insp, func(n): return n is EditorProperty, props)
	for p in props:
		rows.append({"property": String(p.get_edited_property()), "label": p.get_label(), "class": p.get_class(), "visible": p.is_visible_in_tree(),
				"rect_px": _rect(p), "object": _desc(p.get_edited_object())})
	var sections := []
	var secs: Array = []
	_collect(insp, func(n): return n.get_class() == "EditorInspectorSection", secs)
	for s in secs:
		sections.append({"class": s.get_class(), "name": String(s.name), "visible": s.is_visible_in_tree(), "rect_px": _rect(s)})
	var edited := insp.get_edited_object()
	var groups := []
	if edited != null:
		for pi in edited.get_property_list():
			if int(pi["usage"]) & PROPERTY_USAGE_GROUP or int(pi["usage"]) & PROPERTY_USAGE_CATEGORY or int(pi["usage"]) & PROPERTY_USAGE_SUBGROUP:
				var kind := "category" if int(pi["usage"]) & PROPERTY_USAGE_CATEGORY else ("group" if int(pi["usage"]) & PROPERTY_USAGE_GROUP else "subgroup")
				groups.append({"kind": kind, "name": pi["name"], "hint_string": pi["hint_string"]})
	_log["dumps"].append({"name": String(step.get("name", "inspector")), "frame": Engine.get_frames_drawn(), "edited_object": _desc(edited),
			"inspector_rect_px": _rect(insp),
		"inspector_dock_rect_px": _dock_rect(), "scroll": insp.scroll_vertical, "properties": rows, "sections": sections, "object_groups": groups})
	_note("dump_inspector '%s': %d property rows, %d sections" % [String(step.get("name", "inspector")), rows.size(), sections.size()])

func _op_dump_tree(step: Dictionary) -> void:
	var root: Node = EditorInterface.get_base_control()
	if step.get("root") is Dictionary:
		root = _find_first(EditorInterface.get_base_control(), step["root"], false)
		if root == null:
			_err("dump_tree: nothing matches root %s" % str(step["root"]))
			return
	else:
		match String(step.get("root", "base")):
			"inspector":
				root = EditorInterface.get_inspector()
			"main_screen":
				root = EditorInterface.get_editor_main_screen()
	var lines: Array = []
	_dump_node(root, 0, int(step.get("max_depth", 6)), bool(step.get("only_visible", true)), lines)
	_log["dumps"].append({"name": String(step.get("name", "tree")), "frame": Engine.get_frames_drawn(), "lines": lines})
	_note("dump_tree '%s': %d lines" % [String(step.get("name", "tree")), lines.size()])

func _dump_node(n: Node, depth: int, max_depth: int, only_visible: bool, out: Array) -> void:
	if only_visible and n is CanvasItem and not n.is_visible_in_tree():
		return
	var line := "  ".repeat(depth) + n.get_class() + ":" + String(n.name)
	if n is Control:
		line += " " + str(_rect(n))
	if n is Button:
		line += " text='" + n.text + "'"
	elif n is Label:
		line += " text='" + n.text + "'"
	elif n is EditorProperty:
		line += " prop=" + String(n.get_edited_property()) + " label='" + n.get_label() + "'"
	elif n is PopupMenu:
		line += " items=" + str(n.item_count) + " visible=" + str(n.visible)
	out.append(line)
	if depth < max_depth:
		for c in n.get_children():
			_dump_node(c, depth + 1, max_depth, only_visible, out)

# ----------------------------------------------------------------------------------------------------- window / input helpers

func _op_probe_window(step: Dictionary) -> void:
	var root := get_tree().root
	var info := {
		"root_size": [root.size.x, root.size.y],
		"root_content_scale_size": [root.content_scale_size.x, root.content_scale_size.y],
		"root_content_scale_mode": root.content_scale_mode,
		"root_content_scale_aspect": root.content_scale_aspect,
		"root_content_scale_factor": root.content_scale_factor,
		"root_visible_rect": str(root.get_visible_rect()),
		"root_texture_size": [root.get_texture().get_width(), root.get_texture().get_height()],
		"dispserver_window_size": str(DisplayServer.window_get_size()),
		"dispserver_window_size_with_decorations": str(DisplayServer.window_get_size_with_decorations()),
		"dispserver_window_position": str(DisplayServer.window_get_position()),
		"dispserver_window_mode": DisplayServer.window_get_mode(),
		"screen_size": str(DisplayServer.screen_get_size()),
		"screen_usable_rect": str(DisplayServer.screen_get_usable_rect()),
		"screen_scale": DisplayServer.screen_get_scale(),
		"screen_dpi": DisplayServer.screen_get_dpi(),
		"editor_scale": EditorInterface.get_editor_scale(),
		"base_control_size": str(EditorInterface.get_base_control().size),
		"gui_embed_subwindows": root.get("gui_embed_subwindows"),
		"is_multi_window_enabled": EditorInterface.is_multi_window_enabled(),
		"display_scale_setting": EditorInterface.get_editor_settings().get_setting("interface/editor/appearance/display_scale"),
		"single_window_setting": EditorInterface.get_editor_settings().get_setting("interface/editor/display/single_window_mode"),
		"project_override": [ProjectSettings.get_setting("display/window/size/window_width_override"), ProjectSettings.get_setting("display/window/size/window_height_override")],
	}
	_log["dumps"].append({"name": String(step.get("name", "window")), "frame": Engine.get_frames_drawn(), "window": info})
	_note("probe_window '%s': %s" % [String(step.get("name", "window")), str(info)])

func _click_at(pos: Vector2) -> void:
	var root := get_tree().root
	var mm := InputEventMouseMotion.new()
	mm.position = pos
	mm.global_position = pos
	root.push_input(mm)
	var down := InputEventMouseButton.new()
	down.position = pos
	down.global_position = pos
	down.button_index = MOUSE_BUTTON_LEFT
	down.button_mask = MOUSE_BUTTON_MASK_LEFT
	down.pressed = true
	root.push_input(down)
	var up := InputEventMouseButton.new()
	up.position = pos
	up.global_position = pos
	up.button_index = MOUSE_BUTTON_LEFT
	up.button_mask = 0
	up.pressed = false
	root.push_input(up)
	_note("scripted click at (%d, %d)" % [int(pos.x), int(pos.y)])

func _click_control_center(c: Control) -> void:
	# A scripted left click at the centre of a control. Controls inside an EMBEDDED dialog report positions relative to that dialog, so the
	# dialog's own position in the editor window is added.
	var r := c.get_global_rect()
	var pos := r.position + r.size * 0.5
	var w := c.get_window()
	if w != null and w != get_tree().root and w.is_embedded():
		pos += Vector2(w.position)
	_click_at(pos)

func _section_of(c: Node) -> Control:
	var n: Node = c.get_parent()
	while n != null:
		if n.get_class() == "EditorInspectorSection":
			return n
		n = n.get_parent()
	return null

func _op_unfold_group(step: Dictionary) -> void:
	# Unfold the Inspector group (EditorInspectorSection) that holds the row for `property`. Tries a method first, else a scripted click on the header.
	var obj: Object = _object_of(step)
	var p := _find_prop(String(step["property"]), obj)
	if p == null:
		_not_ready("unfold_group: no inspector row for '%s'" % String(step["property"]))
		return
	var sec := _section_of(p)
	if sec == null:
		_not_ready("unfold_group: row '%s' is not inside a section" % String(step["property"]))
		return
	if p.is_visible_in_tree():
		_note("unfold_group: group of '%s' is already open (row visible)" % String(step["property"]))
		return
	var has_unfold := sec.has_method("unfold")
	_note("unfold_group: section %s has_method(unfold)=%s, rect=%s" % [String(sec.name), str(has_unfold), str(sec.get_global_rect())])
	if has_unfold and not bool(step.get("click", false)):
		sec.call("unfold")
	else:
		var scale: float = EditorInterface.get_editor_scale()
		var r := sec.get_global_rect()
		_click_at(Vector2(r.position.x + 90.0 * scale, r.position.y + 13.0 * scale))

func _op_click_control(step: Dictionary) -> void:
	var f: Dictionary = step.get("find", {})
	var root: Node = EditorInterface.get_base_control()
	if String(step.get("within", "base")) == "inspector":
		root = EditorInterface.get_inspector()
	var found: Array = []
	var pred := func(n) -> bool:
		if f.has("class") and not n.is_class(String(f["class"])):
			return false
		if f.has("text") and not (n is Button and n.text == String(f["text"])):
			return false
		if f.has("name") and String(n.name) != String(f["name"]):
			return false
		return n is Control and n.is_visible_in_tree()
	_collect(root, pred, found, 80)
	if found.is_empty():
		_not_ready("click_control: nothing matches %s" % str(f))
		return
	var c: Control = found[int(step.get("index", 0))]
	var r := c.get_global_rect()
	var scale: float = EditorInterface.get_editor_scale()
	_click_at(Vector2(r.position.x + r.size.x * 0.5 + float(step.get("dx", 0)) * scale, r.position.y + r.size.y * 0.5 + float(step.get("dy", 0)) * scale))

# ----------------------------------------------------------------------------------------------- discovery / layout helpers

func _find_first(root: Node, f: Dictionary, visible_only: bool = false) -> Node:
	var found: Array = []
	var pred := func(n) -> bool:
		if f.has("class") and not n.is_class(String(f["class"])):
			return false
		if f.has("name") and String(n.name) != String(f["name"]):
			return false
		if f.has("text") and not (n is Button and n.text == String(f["text"])):
			return false
		if visible_only and n is CanvasItem and not n.is_visible_in_tree():
			return false
		if visible_only and n is Window and not n.visible:
			return false
		return true
	_collect(root, pred, found, 80)
	return found[0] if found.size() > 0 else null

func _op_menu_item(step: Dictionary) -> void:
	var buttons: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is MenuButton and n.is_visible_in_tree() and n.text == String(step["button"]), buttons, 80)
	if buttons.is_empty():
		_not_ready("menu_item: no visible MenuButton '%s'" % String(step["button"]))
		return
	var pm: PopupMenu = buttons[0].get_popup()
	var want := String(step["item"])
	var texts := []
	for i in pm.item_count:
		texts.append(pm.get_item_text(i))
		if pm.get_item_text(i) == want or pm.get_item_text(i).contains(want):
			_note("menu_item: %s > '%s' (id %d)" % [String(step["button"]), pm.get_item_text(i), pm.get_item_id(i)])
			pm.id_pressed.emit(pm.get_item_id(i))
			return
	_not_ready("menu_item: '%s' not in menu %s" % [want, str(texts)])

func _op_dump_scene_tree(step: Dictionary) -> void:
	var trees: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is Tree and n.is_visible_in_tree(), trees, 80)
	var out := []
	for t in trees:
		var items := []
		var it: TreeItem = t.get_root()
		var stack := []
		if it:
			stack.append(it)
		while not stack.is_empty():
			var cur: TreeItem = stack.pop_back()
			var btns := []
			for col in t.columns:
				for b in cur.get_button_count(col):
					btns.append({"col": col, "i": b, "tooltip": cur.get_button_tooltip_text(col, b)})
			items.append({"text": cur.get_text(0), "tooltip": cur.get_tooltip_text(0), "buttons": btns})
			var ch := cur.get_first_child()
			while ch:
				stack.append(ch)
				ch = ch.get_next()
		out.append({"tree": String(t.name), "rect_px": _rect(t), "items": items})
	_log["dumps"].append({"name": String(step.get("name", "scene_tree")), "frame": Engine.get_frames_drawn(), "trees": out})
	_note("dump_scene_tree: %d visible Tree control(s)" % trees.size())

func _op_dump_object(step: Dictionary) -> void:
	var n := _find_first(EditorInterface.get_base_control(), step.get("find", {}), bool(step.get("visible_only", false)))
	if n == null:
		_err("dump_object: nothing matches %s" % str(step.get("find", {})))
		return
	var props := {}
	for pi in n.get_property_list():
		if int(pi["usage"]) & PROPERTY_USAGE_EDITOR or int(pi["usage"]) & PROPERTY_USAGE_SCRIPT_VARIABLE:
			var v = n.get(pi["name"])
			props[pi["name"]] = str(v)
	var methods := []
	for m in n.get_method_list():
		if not String(m["name"]).begins_with("_"):
			methods.append(m["name"])
	_log["dumps"].append({"name": String(step.get("name", "object")), "frame": Engine.get_frames_drawn(), "object": {"class": n.get_class(), "name": String(n.name), "properties": props, "methods": methods}})
	_note("dump_object: %s '%s' with %d properties, %d methods" % [n.get_class(), String(n.name), props.size(), methods.size()])

func _op_dock_split(step: Dictionary) -> void:
	var n := _find_first(EditorInterface.get_base_control(), {"name": String(step["name"])})
	if n == null:
		_err("dock_split: no node '%s'" % String(step["name"]))
		return
	if step.has("offsets"):
		var arr := PackedInt32Array()
		for v in step["offsets"]:
			arr.append(int(v))
		n.set("split_offsets", arr)
	elif step.has("offset"):
		n.set("split_offset", int(step["offset"]))
	_note("dock_split %s: split_offsets=%s split_offset=%s" % [String(step["name"]), str(n.get("split_offsets")), str(n.get("split_offset"))])

func _op_select_tab(step: Dictionary) -> void:
	var tabs: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is TabContainer and n.is_visible_in_tree(), tabs, 80)
	for tc in tabs:
		for i in tc.get_tab_count():
			if tc.get_tab_title(i) == String(step["text"]):
				tc.current_tab = i
				_note("select_tab '%s' in %s" % [String(step["text"]), String(tc.name)])
				return
	_err("select_tab: no visible tab '%s'" % String(step["text"]))

func _op_dump_windows(step: Dictionary) -> void:
	var wins: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is Window and n.visible, wins, 80)
	var out := []
	for w in wins:
		var we := {"class": w.get_class(), "name": String(w.name), "title": w.title if w.get("title") != null else "", "embedded": w.is_embedded(), "position": str(w.position), "size": str(w.size)}
		if w is AcceptDialog:
			we["dialog_text"] = w.dialog_text
			we["ok_text"] = w.get_ok_button().text
			if w is ConfirmationDialog:
				we["cancel_text"] = w.get_cancel_button().text
		out.append(we)
	_log["dumps"].append({"name": String(step.get("name", "windows")), "frame": Engine.get_frames_drawn(), "windows": out})
	_note("dump_windows '%s': %s" % [String(step.get("name", "windows")), str(out)])

func _op_set_text(step: Dictionary) -> void:
	var f: Dictionary = step.get("within", {})
	var scope: Node = EditorInterface.get_base_control()
	if not f.is_empty():
		scope = _find_first(EditorInterface.get_base_control(), f, false)
		if scope == null:
			_not_ready("set_text: nothing matches within %s" % str(f))
			return
	var found: Array = []
	_collect(scope, func(n): return n is LineEdit and n.is_visible_in_tree(), found, 80)
	var idx := int(step.get("index", 0))
	if found.size() <= idx:
		_not_ready("set_text: %d visible LineEdit(s), wanted index %d" % [found.size(), idx])
		return
	found[idx].text = String(step["text"])
	found[idx].text_changed.emit(String(step["text"]))
	_note("set_text: LineEdit %d of %d -> '%s'" % [idx, found.size(), String(step["text"])])

func _op_focus_menu_item(step: Dictionary) -> void:
	var want := String(step.get("text", ""))
	var contains := String(step.get("contains", ""))
	for pm in _all_popups():
		if not pm.visible:
			continue
		for i in pm.item_count:
			var t: String = pm.get_item_text(i)
			if (want != "" and t == want) or (contains != "" and t.contains(contains)):
				pm.set_focused_item(i)
				_note("focus_menu_item: highlighted '%s' (index %d)" % [t, i])
				return
	_not_ready("focus_menu_item: no visible popup item '%s%s'" % [want, contains])

func _op_select_option(step: Dictionary) -> void:
	var scope: Node = _find_first(EditorInterface.get_base_control(), step.get("within", {}), false)
	if scope == null:
		_not_ready("select_option: nothing matches within %s" % str(step.get("within", {})))
		return
	var found: Array = []
	_collect(scope, func(n): return n is OptionButton and n.is_visible_in_tree(), found, 80)
	var idx := int(step.get("index", 0))
	if found.size() <= idx:
		_not_ready("select_option: %d visible OptionButton(s), wanted index %d" % [found.size(), idx])
		return
	var ob: OptionButton = found[idx]
	var items := []
	for i in ob.item_count:
		items.append(ob.get_item_text(i))
		if ob.get_item_text(i) == String(step["text"]):
			ob.select(i)
			ob.item_selected.emit(i)
			_note("select_option: OptionButton %d -> '%s' (items %s)" % [idx, String(step["text"]), str(items)])
			return
	_err("select_option: '%s' not among %s" % [String(step["text"]), str(items)])

func _op_press_ok(step: Dictionary) -> void:
	var dlg = _find_first(EditorInterface.get_base_control(), step.get("within", {}), false)
	if dlg == null or not (dlg is AcceptDialog):
		_not_ready("press_ok: no AcceptDialog matches %s" % str(step.get("within", {})))
		return
	var btn: Button = dlg.get_ok_button()
	_note("press_ok: '%s' text='%s' disabled=%s" % [String(dlg.name), btn.text, str(btn.disabled)])
	btn.pressed.emit()

func _op_press_cancel(step: Dictionary) -> void:
	var dlg = _find_first(EditorInterface.get_base_control(), step.get("within", {}), true)
	if dlg == null or not (dlg is ConfirmationDialog):
		_not_ready("press_cancel: no ConfirmationDialog matches %s" % str(step.get("within", {})))
		return
	var btn: Button = (dlg as ConfirmationDialog).get_cancel_button()
	_note("press_cancel: '%s' button text='%s' visible=%s" % [String(dlg.name), btn.text, str(dlg.visible)])
	btn.pressed.emit()

func _op_open_option_button(step: Dictionary) -> void:
	# Opens the dropdown of an OptionButton: the first visible one that has an item containing step.contains (or the index-th visible one
	# when contains is empty), optionally inside the node found by step.within. The real show_popup().
	var scope: Node = EditorInterface.get_base_control()
	if step.has("within"):
		scope = _find_first(EditorInterface.get_base_control(), step["within"], false)
		if scope == null:
			_not_ready("open_option_button: nothing matches within %s" % str(step["within"]))
			return
	var obs: Array = []
	_collect(scope, func(n): return n is OptionButton and n.is_visible_in_tree(), obs, 80)
	var want := String(step.get("contains", ""))
	var k := 0
	for ob in obs:
		var items := []
		for i in ob.item_count:
			items.append(ob.get_item_text(i))
		var match_ok := (want != "" and str(items).contains(want)) or (want == "" and k == int(step.get("index", 0)))
		k += 1
		if match_ok:
			_note("open_option_button: OptionButton '%s' rect=%s items=%s selected=%d" % [String(ob.name), str(_rect(ob)), str(items), ob.selected])
			ob.show_popup()
			if step.has("focus"):
				for i in ob.item_count:
					if ob.get_item_text(i) == String(step["focus"]):
						ob.get_popup().set_focused_item(i)
						_note("open_option_button: highlighted '%s'" % String(step["focus"]))
			return
	var all := []
	for ob in obs:
		var its := []
		for i in ob.item_count:
			its.append(ob.get_item_text(i))
		all.append(its)
	_not_ready("open_option_button: no visible OptionButton with an item containing '%s' (visible OptionButtons: %s)" % [want, str(all)])

# ------------------------------------------------------------------------------------------------ follow-up: menus, dialogs, settings

func _menubars() -> Array:
	var mbs: Array = []
	_collect(EditorInterface.get_base_control(), func(n): return n is MenuBar, mbs, 80)
	return mbs

func _op_dump_menubar(step: Dictionary) -> void:
	var out := []
	for mb in _menubars():
		var entry := {"native": mb.is_native_menu(), "visible": mb.is_visible_in_tree(), "rect_px": _rect(mb), "menus": []}
		for i in mb.get_menu_count():
			var pm: PopupMenu = mb.get_menu_popup(i)
			var items := []
			for j in pm.item_count:
				items.append({"text": pm.get_item_text(j), "id": pm.get_item_id(j), "separator": pm.is_item_separator(j), "disabled": pm.is_item_disabled(j)})
			entry["menus"].append({"title": mb.get_menu_title(i), "has_rect_method": mb.has_method("get_menu_rect"), "items": items})
		out.append(entry)
	_log["dumps"].append({"name": String(step.get("name", "menubar")), "frame": Engine.get_frames_drawn(), "menubars": out})
	_note("dump_menubar '%s': %d MenuBar(s)" % [String(step.get("name", "menubar")), out.size()])

func _menubar_index(title: String) -> Array:
	for mb in _menubars():
		for i in mb.get_menu_count():
			if mb.get_menu_title(i) == title:
				return [mb, i]
	return []

func _menu_title_rect(mb: MenuBar, idx: int) -> Rect2:
	# MenuBar has no public rectangle accessor in 4.7.2, so lay the titles out the way its own draw code does: left to right, each as wide as its
	# text plus the normal StyleBox margins, separated by the h_separation theme constant.
	var font: Font = mb.get_theme_font("font")
	var fs: int = mb.get_theme_font_size("font_size")
	var hsep: int = mb.get_theme_constant("h_separation")
	var style: StyleBox = mb.get_theme_stylebox("normal")
	var x := 0.0
	for i in mb.get_menu_count():
		if mb.is_menu_hidden(i):
			continue
		var tw: float = font.get_string_size(mb.get_menu_title(i), HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x + style.get_minimum_size().x
		if i == idx:
			return Rect2(x, 0, tw, mb.size.y)
		x += tw + hsep
	return Rect2()

func _op_menubar_open(step: Dictionary) -> void:
	# Shows the menu the way a user does: a scripted click on its title in the (embedded) menu bar. Needs Editor Settings
	# interface/editor/appearance/use_embedded_menu = true (otherwise macOS draws the menu in the screen's top bar, outside the window).
	var found := _menubar_index(String(step["menu"]))
	if found.is_empty():
		_not_ready("menubar_open: no menu titled '%s'" % String(step["menu"]))
		return
	var mb: MenuBar = found[0]
	var idx: int = found[1]
	if mb.is_native_menu() or mb.size.x <= 1.0:
		_err("menubar_open: the menu bar is native (drawn by macOS, outside the window); turn on use_embedded_menu")
		return
	var r := _menu_title_rect(mb, idx)
	var gp := mb.get_global_position()
	_click_at(Vector2(gp.x + r.position.x + r.size.x * 0.5, gp.y + r.position.y + r.size.y * 0.5))
	_note("menubar_open: clicked '%s' title (title rect %s in the menu bar at %s)" % [String(step["menu"]), str(r), str(gp)])

func _op_menubar_pick(step: Dictionary) -> void:
	var found := _menubar_index(String(step["menu"]))
	if found.is_empty():
		_not_ready("menubar_pick: no menu titled '%s'" % String(step["menu"]))
		return
	var mb: MenuBar = found[0]
	var pm: PopupMenu = mb.get_menu_popup(found[1])
	var want := String(step.get("item", ""))
	var contains := String(step.get("contains", ""))
	var texts := []
	for j in pm.item_count:
		var t := pm.get_item_text(j)
		texts.append(t)
		if (want != "" and t == want) or (contains != "" and t.contains(contains)):
			_note("menubar_pick: %s > '%s' (id %d)" % [String(step["menu"]), t, pm.get_item_id(j)])
			pm.id_pressed.emit(pm.get_item_id(j))
			if bool(step.get("hide", true)):
				pm.hide()
			return
	_err("menubar_pick: '%s%s' not in menu %s: %s" % [want, contains, String(step["menu"]), str(texts)])

func _text_entry(n: Node) -> Dictionary:
	var e := {}
	if n is Label:
		e["text"] = n.text
	elif n is RichTextLabel:
		e["text"] = n.get_parsed_text()
	elif n is OptionButton:
		var items := []
		for i in n.item_count:
			items.append(n.get_item_text(i))
		e["items"] = items
		e["selected"] = n.selected
		e["text"] = n.text
	elif n is Button:
		e["text"] = n.text
		if n.tooltip_text != "":
			e["tooltip"] = n.tooltip_text
		if n is BaseButton and n.toggle_mode:
			e["pressed"] = n.button_pressed
	elif n is LineEdit:
		e["text"] = n.text
		e["placeholder"] = n.placeholder_text
	elif n is TabBar:
		var titles := []
		for i in n.tab_count:
			titles.append(n.get_tab_title(i))
		e["tabs"] = titles
		e["current"] = n.current_tab
	elif n is TabContainer:
		var titles2 := []
		for i in n.get_tab_count():
			titles2.append(n.get_tab_title(i))
		e["tabs"] = titles2
		e["current"] = n.current_tab
	elif n is PopupMenu:
		var items2 := []
		for i in n.item_count:
			items2.append(n.get_item_text(i))
		e["items"] = items2
		e["popup_visible"] = n.visible
	elif n is EditorProperty:
		e["label"] = n.get_label()
		e["property"] = String(n.get_edited_property())
	elif n is Tree:
		var rows := []
		var stack := []
		var root: TreeItem = n.get_root()
		if root:
			stack.append([root, 0])
		while not stack.is_empty():
			var cur = stack.pop_back()
			var it: TreeItem = cur[0]
			var texts := []
			for c in n.columns:
				texts.append(it.get_text(c))
			rows.append({"depth": cur[1], "text": texts, "collapsed": it.collapsed, "selected": it.is_selected(0)})
			var kids := []
			var ch := it.get_first_child()
			while ch:
				kids.append(ch)
				ch = ch.get_next()
			kids.reverse()
			for k in kids:
				stack.append([k, int(cur[1]) + 1])
		e["tree_rows"] = rows
	if n is Control and n.tooltip_text != "" and not e.has("tooltip"):
		e["tooltip"] = n.tooltip_text
	return e

func _walk_texts(n: Node, out: Array, depth: int, max_depth: int) -> void:
	if depth > max_depth:
		return
	if n is CanvasItem and not n.is_visible_in_tree():
		return
	var e := _text_entry(n)
	if not e.is_empty():
		e["class"] = n.get_class()
		e["name"] = String(n.name)
		if n is Control:
			e["rect_px"] = _rect(n)
		out.append(e)
	for c in n.get_children():
		_walk_texts(c, out, depth + 1, max_depth)

func _op_dump_texts(step: Dictionary) -> void:
	# Every visible string under a dialog (or the whole editor): labels, buttons, tabs, option items, line edit text and placeholder,
	# tree rows, tooltips, Inspector row labels. These are the live strings, not conventions.
	var root: Node = EditorInterface.get_base_control()
	if step.has("within"):
		root = _find_first(EditorInterface.get_base_control(), step["within"], false)
		if root == null:
			_not_ready("dump_texts: nothing matches within %s" % str(step["within"]))
			return
	var out: Array = []
	_walk_texts(root, out, 0, int(step.get("max_depth", 40)))
	_log["dumps"].append({"name": String(step.get("name", "texts")), "frame": Engine.get_frames_drawn(), "within": str(step.get("within", "base")), "texts": out})
	_note("dump_texts '%s': %d entries" % [String(step.get("name", "texts")), out.size()])

func _op_dump_rows(step: Dictionary) -> void:
	# The Inspector-style rows (EditorProperty) inside a dialog such as Editor Settings or Project Settings.
	var root := _find_first(EditorInterface.get_base_control(), step.get("within", {}), false)
	if root == null:
		_not_ready("dump_rows: nothing matches within %s" % str(step.get("within", {})))
		return
	var props: Array = []
	_collect(root, func(n): return n is EditorProperty, props, 80)
	var rows := []
	for p in props:
		var o: Object = p.get_edited_object()
		rows.append({"property": String(p.get_edited_property()), "label": p.get_label(), "class": p.get_class(), "visible": p.is_visible_in_tree(), "rect_px": _rect(p), "object": _desc(o)})
	_log["dumps"].append({"name": String(step.get("name", "rows")), "frame": Engine.get_frames_drawn(), "rows": rows})
	_note("dump_rows '%s': %d rows" % [String(step.get("name", "rows")), rows.size()])

func _op_select_tree_item(step: Dictionary) -> void:
	# Expands and selects a Tree item by its path of texts, e.g. ["Rendering", "Renderer"] (a TreeItem.select, what a click does).
	var root := _find_first(EditorInterface.get_base_control(), step.get("within", {}), false)
	if root == null:
		_not_ready("select_tree_item: nothing matches within %s" % str(step.get("within", {})))
		return
	var trees: Array = []
	_collect(root, func(n): return n is Tree and n.is_visible_in_tree(), trees, 80)
	var want: Array = step.get("path", [])
	for t in trees:
		var cur: TreeItem = t.get_root()
		if cur == null:
			continue
		var ok := true
		for seg in want:
			var found: TreeItem = null
			var ch := cur.get_first_child()
			while ch:
				if ch.get_text(0) == String(seg):
					found = ch
					break
				ch = ch.get_next()
			if found == null:
				ok = false
				break
			cur.collapsed = false
			cur = found
		if ok:
			cur.select(0)
			t.scroll_to_item(cur)
			_note("select_tree_item: selected %s in Tree '%s'" % [str(want), String(t.name)])
			return
	_not_ready("select_tree_item: path %s not found in %d visible Tree(s)" % [str(want), trees.size()])

func _op_toggle_check(step: Dictionary) -> void:
	# Sets the CheckBox/CheckButton of a dialog row (found by its property path or its label text) to value; the row's own handler then
	# changes the setting, exactly as a click does.
	var root := _find_first(EditorInterface.get_base_control(), step.get("within", {}), false)
	if root == null:
		_not_ready("toggle_check: nothing matches within %s" % str(step.get("within", {})))
		return
	var rows: Array = []
	_collect(root, func(n): return n is EditorProperty and n.is_visible_in_tree(), rows, 80)
	for p in rows:
		var hit: bool = (step.has("property") and String(p.get_edited_property()) == String(step["property"])) or (step.has("text") and p.get_label() == String(step["text"]))
		if not hit:
			continue
		var cbs: Array = []
		_collect(p, func(n): return n is CheckBox or n is CheckButton, cbs, 6)
		if cbs.is_empty():
			_err("toggle_check: row '%s' has no check box" % p.get_label())
			return
		var cb: BaseButton = cbs[0]
		var want_on := bool(step.get("value", true))
		if cb.button_pressed == want_on:
			_note("toggle_check: row '%s' (%s) is already %s" % [p.get_label(), String(p.get_edited_property()), str(want_on)])
			return
		# EditorPropertyCheck listens to the check box's `pressed` signal (not `toggled`), so setting button_pressed alone changes nothing:
		# the default is the click a student makes, scripted through the real GUI input path at the centre of the box.
		if String(step.get("how", "click")) == "signal":
			_note("toggle_check: row '%s' (%s) check box %s -> %s by the pressed signal" % [p.get_label(), String(p.get_edited_property()), str(cb.button_pressed), str(want_on)])
			cb.button_pressed = want_on
			cb.pressed.emit()
		else:
			_note("toggle_check: row '%s' (%s) check box %s -> %s by a scripted click on the box" % [p.get_label(), String(p.get_edited_property()), str(cb.button_pressed), str(want_on)])
			_click_control_center(cb)
		return
	_not_ready("toggle_check: no visible row for %s" % str(step))

func _op_set_toggle(step: Dictionary) -> void:
	# Sets a toggle button (CheckButton / CheckBox / toggle Button) found by its text, optionally inside the node found by step.within, to
	# step.value. Setting button_pressed emits the button's own `toggled` signal, which is what a click does.
	var scope: Node = EditorInterface.get_base_control()
	if step.has("within"):
		scope = _find_first(EditorInterface.get_base_control(), step["within"], false)
		if scope == null:
			_not_ready("set_toggle: nothing matches within %s" % str(step["within"]))
			return
	var btns: Array = []
	var want := String(step["text"])
	_collect(scope, func(n): return n is BaseButton and n.toggle_mode and n.is_visible_in_tree() and n is Button and n.text == want, btns, 80)
	if btns.is_empty():
		_not_ready("set_toggle: no visible toggle button '%s'" % want)
		return
	var b: BaseButton = btns[int(step.get("index", 0))]
	_note("set_toggle: '%s' (%s) %s -> %s (%s)" % [want, b.get_class(), str(b.button_pressed), str(bool(step.get("value", true))), String(step.get("how", "signal"))])
	if String(step.get("how", "signal")) == "click":
		if b.button_pressed != bool(step.get("value", true)):
			_click_control_center(b)
	else:
		b.button_pressed = bool(step.get("value", true))

func _op_close_dialog(step: Dictionary) -> void:
	var dlg = _find_first(EditorInterface.get_base_control(), step.get("within", {}), false)
	if dlg == null or not (dlg is Window):
		_not_ready("close_dialog: no Window matches %s" % str(step.get("within", {})))
		return
	dlg.hide()
	_note("close_dialog: hid %s" % String(dlg.name))

func _op_editor_setting_info(step: Dictionary) -> void:
	# The value, and the engine's own default ("revert") value, of editor settings, as the running editor reports them.
	var es := EditorInterface.get_editor_settings()
	var info := {}
	for nm in step.get("names", []):
		var key := String(nm)
		info[key] = {"has_setting": es.has_setting(key), "value": str(es.get_setting(key)) if es.has_setting(key) else "<none>", "can_revert": es.property_can_revert(key), "revert_value": str(es.property_get_revert(key))}
	_log["dumps"].append({"name": String(step.get("name", "editor_setting_info")), "frame": Engine.get_frames_drawn(), "settings": info})
	_note("editor_setting_info: %s" % str(info))

func _object_of(step: Dictionary) -> Object:
	# "object": "node" | "material" | "shader" | {"target": "chain", "chain": [...]} : the object whose Inspector row is meant (null = any)
	if not step.has("object"):
		return null
	var o = step["object"]
	if o is Dictionary:
		var d: Dictionary = (o as Dictionary).duplicate()
		d["node"] = d.get("node", step.get("node", "."))
		return _resolve(d)
	return _resolve({"node": step.get("node", "."), "target": o})

func _dock_rect() -> Array:
	# the whole right dock (tabs "Inspector | Signals | Groups" + the Inspector) in window pixels: what a film crops
	var d := _find_first(EditorInterface.get_base_control(), {"name": "DockSlotRightUL"}, false)
	if d == null or not (d is Control):
		return []
	return _rect(d)

# `window_size` of the log is the real editor window in pixels; the movie frame is that window scaled to the movie size (same aspect: no crop).
