class_name MomeWindow
extends PanelContainer

const CLIPBOARD_TEXT := "text"
const MENU_CUT := 0
const MENU_COPY := 1
const MENU_PASTE := 2

signal close_requested
signal minimize_requested

var _device_uid: int
var _file_source: Node
var _file_uid: int
var _read_only: bool = false

@onready var _read_only_label: Label = $Layout/TitleBar/ReadOnlyLabel
@onready var _title_label: Label = $Layout/TitleBar/TitleLabel
@onready var _minimize_button: Button = $Layout/TitleBar/MinimizeButton
@onready var _close_button: Button = $Layout/TitleBar/CloseButton
@onready var _text_edit: TextEdit = $Layout/TextEdit
@onready var _context_menu: ContextMenu = $ContextMenu

func _ready() -> void:
	_minimize_button.pressed.connect(_on_minimize_button_pressed)
	_close_button.pressed.connect(_on_close_button_pressed)
	_text_edit.gui_input.connect(_on_text_edit_gui_input)
	_context_menu.id_pressed.connect(_on_context_menu_id_pressed)

func _on_minimize_button_pressed() -> void:
	minimize_requested.emit()


func _on_close_button_pressed() -> void:
	close_requested.emit()


func open(device_uid: int, file_source: Node, file_uid: int) -> void:
	_device_uid = device_uid
	_file_source = file_source
	_file_uid = file_uid
	_show_document(_file_source.get_document(_device_uid, _file_uid))


func _show_document(document: Dictionary) -> void:
	_read_only = document["read_only"]
	_title_label.text = tr(document["name"]) + document["extension"]
	_read_only_label.visible = _read_only
	_text_edit.text = tr(document["content"]) if _read_only else document["content"]
	_text_edit.editable = not _read_only


func _on_text_edit_gui_input(event: InputEvent) -> void:
	var mouse := event as InputEventMouseButton
	if mouse != null and mouse.pressed and mouse.button_index == MOUSE_BUTTON_RIGHT:
		_open_text_menu.call_deferred(mouse.global_position)


func _open_text_menu(at_position: Vector2) -> void:
	var has_selection := _text_edit.has_selection()
	var items: Array[Dictionary] = []
	if not _read_only:
		items.append({"id": MENU_CUT, "text": "UI_MOME_CUT", "disabled": not has_selection})
	items.append({"id": MENU_COPY, "text": "UI_MOME_COPY", "disabled": not has_selection})
	if not _read_only:
		var clipboard_has_text: bool = _file_source.get_clipboard(_device_uid)["kind"] == CLIPBOARD_TEXT
		items.append({"id": MENU_PASTE, "text": "UI_MOME_PASTE", "disabled": not clipboard_has_text})
	_context_menu.open_at(items, at_position)


func _on_context_menu_id_pressed(item_id: int) -> void:
	match item_id:
		MENU_COPY:
			_copy_selection()
		MENU_CUT:
			_copy_selection()
			_text_edit.delete_selection()
		MENU_PASTE:
			_paste_clipboard()


func _copy_selection() -> void:
	_file_source.set_clipboard_text(_device_uid, _text_edit.get_selected_text())


func _paste_clipboard() -> void:
	var clipboard: Dictionary = _file_source.get_clipboard(_device_uid)
	if clipboard["kind"] == CLIPBOARD_TEXT:
		_text_edit.insert_text_at_caret(clipboard["text"])
