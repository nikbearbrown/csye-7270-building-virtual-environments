extends SceneTree
## Project Manager driver (godot-shaders series, editor-capture follow-up).
##
## `godot --project-manager --script res://pm_driver.gd` makes Godot build the REAL Project Manager inside this script's main loop
## (verified: the root's only child is a ProjectManager node), so the same trick as the editor driver works: find the real buttons and
## dialogs and drive them while Movie Maker records. Nothing is created: the dialogs are opened, read and cancelled, and an isolated HOME
## means the Project Manager's project list is empty and nobody's real list is touched.
##
## Input:  env DRIVER_STATE_SCRIPT (a JSON list of steps, or {"steps": [...], "window": [w, h], "boot_frames": N}).
## Output: env DRIVER_LOG (states.json: steps, marks with process_frame, dumps, errors).
## Steps:  wait_frames {n} | mark {name} | press {text|name, index} | set_text {within, index, text} | select_option {within, index, text}
##         open_option_button {within, index, contains, focus} | dump_texts {within, name} | dump_windows {name} | log {text} | probe {name}
##         click {text|name, index, within_class} (a scripted mouse click: the way to change a radio button as the dialog's own handler sees it)
##         Any step may carry "settle": N. `mark` ends its frame. Frame numbers: the movie file index is Engine.get_process_frames().

var steps: Array = []
var idx := 0
var wait := 0
var poll_tries := {}
var booted := false
var boot_count := 0
var boot_frames := 25
var window_size: Array = []
var window_settle := 40
var window_done := false
var flash: ColorRect = null
var flash_free_at := -1
var log := {"steps": [], "marks": {}, "dumps": [], "errors": [], "notes": []}
var log_path := ""
var finished := false
var quit_in := -1
var requeued := false

func _initialize() -> void:
	var sp := OS.get_environment("DRIVER_STATE_SCRIPT")
	if sp == "" or not FileAccess.file_exists(sp):
		print("PM_DRIVER: no state script (DRIVER_STATE_SCRIPT=%s)" % sp)
		quit(2)
		return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(sp))
	if parsed is Dictionary:
		steps = parsed.get("steps", [])
		window_size = parsed.get("window", [])
		boot_frames = int(parsed.get("boot_frames", boot_frames))
		window_settle = int(parsed.get("window_settle", window_settle))
	elif parsed is Array:
		steps = parsed
	log_path = OS.get_environment("DRIVER_LOG")
	if log_path == "":
		log_path = "user://pm_states.json"
	# The Project Manager does not read the editor's Single Window Mode setting, so its dialogs are separate OS windows, which Movie Maker
	# does not record. Embedding them inside the window is one property of the root window (the editor does the same from its setting).
	root.gui_embed_subwindows = true
	log["godot"] = Engine.get_version_info()["string"]
	log["renderer"] = RenderingServer.get_current_rendering_method()
	log["state_script"] = sp
	print("PM_DRIVER: %d steps from %s; log -> %s" % [steps.size(), sp, log_path])

func _process(_delta: float) -> bool:
	var pf := Engine.get_process_frames()
	if quit_in >= 0:
		quit_in -= 1
		return quit_in < 0
	if flash and pf >= flash_free_at:
		flash.queue_free()
		flash = null
	if not booted:
		boot_count += 1
		if boot_count < boot_frames:
			return false
		if not window_size.is_empty() and not window_done:
			window_done = true
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
			DisplayServer.window_set_size(Vector2i(int(window_size[0]), int(window_size[1])))
			note("boot: window_set_size(%d, %d) -> window_get_size = %s" % [int(window_size[0]), int(window_size[1]), str(DisplayServer.window_get_size())])
			wait = window_settle
			return false
		booted = true
		log["window_size"] = [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y]
		log["screen_scale"] = DisplayServer.screen_get_scale()
		log["gui_embed_subwindows"] = root.get("gui_embed_subwindows")
		flash = ColorRect.new()
		flash.color = Color(1, 0, 1, 1)
		flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
		flash.set_anchors_preset(Control.PRESET_FULL_RECT)
		root.add_child(flash)
		flash_free_at = pf + 2
		log["flash"] = {"frame": Engine.get_frames_drawn(), "process_frame": pf, "frames": 2}
		wait = 4
		print("PM_DRIVER: flash at process frame %d" % pf)
		return false
	if wait > 0:
		wait -= 1
		return false
	while idx < steps.size() and wait == 0:
		var step: Dictionary = steps[idx]
		idx += 1
		run_step(step)
	if idx >= steps.size() and wait == 0 and not finished:
		finished = true
		log["finished_process_frame"] = pf
		write_log()
		print("PM_DRIVER: finished at process frame %d, %d marks, %d errors" % [pf, log["marks"].size(), log["errors"].size()])
		quit_in = 6
	return false

func note(t: String) -> void:
	log["notes"].append({"process_frame": Engine.get_process_frames(), "text": t})
	print("PM_DRIVER: ", t)

func err(t: String) -> void:
	log["errors"].append({"process_frame": Engine.get_process_frames(), "step": idx - 1, "text": t})
	print("PM_DRIVER ERROR: ", t)

func not_ready(msg: String, max_tries: int = 40) -> void:
	var key := idx - 1
	var n: int = int(poll_tries.get(key, 0)) + 1
	poll_tries[key] = n
	if n <= max_tries:
		idx = key
		wait = 1
		requeued = true
	else:
		err("%s (gave up after %d tries)" % [msg, max_tries])

func write_log() -> void:
	var f := FileAccess.open(log_path, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(log, "  "))
		f.close()

func collect(n: Node, pred: Callable, out: Array, depth: int = 0) -> void:
	if depth > 80:
		return
	for c in n.get_children():
		if pred.call(c):
			out.append(c)
		collect(c, pred, out, depth + 1)

func find_first(f: Dictionary) -> Node:
	var found: Array = []
	var pred := func(n) -> bool:
		if f.has("class") and not n.is_class(String(f["class"])):
			return false
		if f.has("name") and String(n.name) != String(f["name"]):
			return false
		return true
	collect(root, pred, found)
	return found[0] if found.size() > 0 else null

func rect_px(c: Control) -> Array:
	return [int(round(c.global_position.x)), int(round(c.global_position.y)), int(round(c.size.x)), int(round(c.size.y))]

func run_step(step: Dictionary) -> void:
	var op := String(step.get("op", ""))
	var step_index := idx - 1
	log["steps"].append({"i": step_index, "op": op, "process_frame": Engine.get_process_frames()})
	var errs_before: int = log["errors"].size()
	match op:
		"wait_frames":
			wait = int(step.get("n", 1))
		"mark":
			var m := {"process_frame": Engine.get_process_frames(), "frame": Engine.get_frames_drawn(), "step": step_index, "window_size": [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y], "open_windows": open_windows()}
			log["marks"][String(step["name"])] = m
			write_log()
			print("PM_DRIVER: mark %s at process frame %d" % [String(step["name"]), Engine.get_process_frames()])
			wait = maxi(wait, 1)
		"log":
			note(String(step.get("text", "")))
		"press":
			op_press(step)
		"click":
			op_click(step)
		"press_cancel":
			op_press_cancel(step)
		"set_text":
			op_set_text(step)
		"select_option":
			op_select_option(step)
		"open_option_button":
			op_open_option_button(step)
		"dump_texts":
			op_dump_texts(step)
		"dump_windows":
			var wins: Array = []
			collect(root, func(n): return n is Window and n.visible, wins)
			var out := []
			for w in wins:
				out.append({"class": w.get_class(), "name": String(w.name), "title": w.title, "embedded": w.is_embedded(), "size": str(w.size), "position": str(w.position)})
			log["dumps"].append({"name": String(step.get("name", "windows")), "process_frame": Engine.get_process_frames(), "windows": out})
			note("dump_windows: %s" % str(out))
		"probe":
			var info := {"classes": {}}
			for cn in ["ProjectManager", "ProjectDialog", "ProjectList", "ProjectSettingsEditor", "EditorSettingsDialog"]:
				info["classes"][cn] = ClassDB.class_exists(cn)
			log["dumps"].append({"name": String(step.get("name", "probe")), "info": info})
		_:
			err("unknown op '%s'" % op)
	if requeued:
		requeued = false
		return
	if step.has("settle"):
		wait = maxi(wait, int(step["settle"]))

func op_press(step: Dictionary) -> void:
	var found: Array = []
	var pred := func(n) -> bool:
		if not (n is BaseButton and n.is_visible_in_tree()):
			return false
		if step.has("text") and not (n is Button and n.text == String(step["text"])):
			return false
		if step.has("name") and String(n.name) != String(step["name"]):
			return false
		if step.has("within_class") and not _inside(n, String(step["within_class"])):
			return false
		return true
	collect(root, pred, found)
	if found.is_empty():
		not_ready("press: nothing matches %s" % str(step))
		return
	var b: BaseButton = found[int(step.get("index", 0))]
	note("press: '%s' (%s), %d match(es)" % [b.text if b is Button else String(b.name), b.get_class(), found.size()])
	b.pressed.emit()

func op_press_cancel(step: Dictionary) -> void:
	# presses the Cancel button of a ConfirmationDialog (found by class): its own handler closes the dialog and creates nothing
	var dlg := find_first(step.get("within", {}))
	if dlg == null or not (dlg is ConfirmationDialog):
		not_ready("press_cancel: no ConfirmationDialog matches %s" % str(step.get("within", {})))
		return
	var btn: Button = (dlg as ConfirmationDialog).get_cancel_button()
	note("press_cancel: '%s' button text='%s'" % [String(dlg.name), btn.text])
	btn.pressed.emit()

func open_windows() -> Array:
	var wins: Array = []
	collect(root, func(n): return n is Window and n.visible, wins)
	var out := []
	for w in wins:
		var e := {"class": w.get_class(), "title": w.title, "embedded": w.is_embedded(), "position": [w.position.x, w.position.y], "size": [w.size.x, w.size.y]}
		if w.is_embedded():
			e["title_height"] = w.get_theme_constant("title_height")
			var sb: StyleBox = w.get_theme_stylebox("embedded_border")
			if sb != null:
				e["border"] = [sb.get_margin(SIDE_LEFT), sb.get_margin(SIDE_TOP), sb.get_margin(SIDE_RIGHT), sb.get_margin(SIDE_BOTTOM)]
		out.append(e)
	return out

func click_at(pos: Vector2) -> void:
	# a scripted left click through the real GUI input path (Viewport.push_input), as the editor driver does
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
	note("scripted click at (%d, %d)" % [int(pos.x), int(pos.y)])

func op_click(step: Dictionary) -> void:
	# click {text|name, index, within_class}: a scripted mouse click at the centre of a visible button. Controls inside an embedded dialog
	# report positions relative to the dialog, so the dialog's own position is added.
	var found: Array = []
	var pred := func(n) -> bool:
		if not (n is BaseButton and n.is_visible_in_tree()):
			return false
		if step.has("text") and not (n is Button and n.text == String(step["text"])):
			return false
		if step.has("name") and String(n.name) != String(step["name"]):
			return false
		if step.has("within_class") and not _inside(n, String(step["within_class"])):
			return false
		return true
	collect(root, pred, found)
	if found.is_empty():
		not_ready("click: nothing matches %s" % str(step))
		return
	var b: BaseButton = found[int(step.get("index", 0))]
	var r := b.get_global_rect()
	var pos := r.position + r.size * 0.5
	var w := b.get_window()
	if w != null and w != root and w.is_embedded():
		pos += Vector2(w.position)
	note("click: '%s' (%s), %d match(es), pressed before = %s" % [b.text if b is Button else String(b.name), b.get_class(), found.size(), str(b.button_pressed)])
	click_at(pos)

func _inside(n: Node, cls: String) -> bool:
	var p := n.get_parent()
	while p != null:
		if p.is_class(cls):
			return true
		p = p.get_parent()
	return false

func op_set_text(step: Dictionary) -> void:
	var scope := find_first(step.get("within", {}))
	if scope == null:
		not_ready("set_text: nothing matches within %s" % str(step.get("within", {})))
		return
	var found: Array = []
	collect(scope, func(n): return n is LineEdit and n.is_visible_in_tree(), found)
	var i := int(step.get("index", 0))
	if found.size() <= i:
		not_ready("set_text: %d visible LineEdit(s), wanted index %d" % [found.size(), i])
		return
	found[i].text = String(step["text"])
	found[i].text_changed.emit(String(step["text"]))
	note("set_text: LineEdit %d of %d -> '%s'" % [i, found.size(), String(step["text"])])

func op_select_option(step: Dictionary) -> void:
	var scope := find_first(step.get("within", {}))
	if scope == null:
		not_ready("select_option: nothing matches within %s" % str(step.get("within", {})))
		return
	var found: Array = []
	collect(scope, func(n): return n is OptionButton and n.is_visible_in_tree(), found)
	var i := int(step.get("index", 0))
	if found.size() <= i:
		not_ready("select_option: %d visible OptionButton(s), wanted index %d" % [found.size(), i])
		return
	var ob: OptionButton = found[i]
	var items := []
	for k in ob.item_count:
		items.append(ob.get_item_text(k))
		if ob.get_item_text(k) == String(step["text"]):
			ob.select(k)
			ob.item_selected.emit(k)
			note("select_option: OptionButton %d -> '%s' (items %s)" % [i, String(step["text"]), str(items)])
			return
	err("select_option: '%s' not among %s" % [String(step["text"]), str(items)])

func op_open_option_button(step: Dictionary) -> void:
	var scope: Node = root
	if step.has("within"):
		scope = find_first(step["within"])
		if scope == null:
			not_ready("open_option_button: nothing matches within %s" % str(step["within"]))
			return
	var found: Array = []
	collect(scope, func(n): return n is OptionButton and n.is_visible_in_tree(), found)
	var want := String(step.get("contains", ""))
	var k := 0
	for ob in found:
		var items := []
		for i in ob.item_count:
			items.append(ob.get_item_text(i))
		var ok: bool = (want != "" and str(items).contains(want)) or (want == "" and k == int(step.get("index", 0)))
		k += 1
		if ok:
			note("open_option_button: items=%s selected=%d" % [str(items), ob.selected])
			ob.show_popup()
			if step.has("focus"):
				for i in ob.item_count:
					if ob.get_item_text(i) == String(step["focus"]):
						ob.get_popup().set_focused_item(i)
			return
	not_ready("open_option_button: no visible OptionButton matching %s" % str(step))

func text_entry(n: Node) -> Dictionary:
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
	elif n is TabContainer:
		var titles2 := []
		for i in n.get_tab_count():
			titles2.append(n.get_tab_title(i))
		e["tabs"] = titles2
	elif n is PopupMenu:
		var items2 := []
		for i in n.item_count:
			items2.append(n.get_item_text(i))
		e["items"] = items2
	elif n is Tree:
		var rows := []
		var stack := []
		var rt: TreeItem = n.get_root()
		if rt:
			stack.append([rt, 0])
		while not stack.is_empty():
			var cur = stack.pop_back()
			var it: TreeItem = cur[0]
			var texts := []
			for c in n.columns:
				texts.append(it.get_text(c))
			rows.append({"depth": cur[1], "text": texts})
			var kids := []
			var ch := it.get_first_child()
			while ch:
				kids.append(ch)
				ch = ch.get_next()
			kids.reverse()
			for kid in kids:
				stack.append([kid, int(cur[1]) + 1])
		e["tree_rows"] = rows
	if n is Control and n.tooltip_text != "" and not e.has("tooltip"):
		e["tooltip"] = n.tooltip_text
	return e

func walk_texts(n: Node, out: Array, depth: int) -> void:
	if depth > 40:
		return
	if n is CanvasItem and not n.is_visible_in_tree():
		return
	var e := text_entry(n)
	if not e.is_empty():
		e["class"] = n.get_class()
		e["name"] = String(n.name)
		if n is Control:
			e["rect_px"] = rect_px(n)
		out.append(e)
	for c in n.get_children():
		walk_texts(c, out, depth + 1)

func op_dump_texts(step: Dictionary) -> void:
	var scope: Node = root
	if step.has("within"):
		scope = find_first(step["within"])
		if scope == null:
			not_ready("dump_texts: nothing matches within %s" % str(step["within"]))
			return
	var out: Array = []
	walk_texts(scope, out, 0)
	log["dumps"].append({"name": String(step.get("name", "texts")), "process_frame": Engine.get_process_frames(), "within": str(step.get("within", "root")), "texts": out})
	note("dump_texts '%s': %d entries" % [String(step.get("name", "texts")), out.size()])
