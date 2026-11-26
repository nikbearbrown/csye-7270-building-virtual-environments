class_name ThisPCWindow
extends PanelContainer

const KIND_DRIVE := "drive"
const KIND_FOLDER := "folder"
const KIND_FILE := "file"
const ROOT_NAME_KEY := "UI_THIS_PC"
const PATH_SEPARATOR := " / "

signal close_requested
signal minimize_requested

@export var drive_icon: Texture2D
@export var folder_icon: Texture2D
@export var file_icon: Texture2D

var _device_uid: int
var _file_source: Node
var _current_folder_uid: int
var _path: Array[Dictionary] = []

@onready var _entry_list: ItemList = $Layout/EntryList
@onready var _minimize_button: Button = $Layout/TitleBar/MinimizeButton
@onready var _close_button: Button = $Layout/TitleBar/CloseButton
@onready var _up_button: Button = $Layout/Toolbar/UpButton
@onready var _path_label: Label = $Layout/Toolbar/PathLabel

func _ready() -> void:
	_minimize_button.pressed.connect(_on_minimize_button_pressed)
	_close_button.pressed.connect(_on_close_button_pressed)
	_up_button.pressed.connect(_on_up_button_pressed)
	_entry_list.item_activated.connect(_on_entry_activated)

func _on_minimize_button_pressed() -> void:
	minimize_requested.emit()


func _on_close_button_pressed() -> void:
	close_requested.emit()


func open(device_uid: int, file_source: Node) -> void:
	if _file_source != null and _file_source.drives_changed.is_connected(_on_drives_changed):
		_file_source.drives_changed.disconnect(_on_drives_changed)
	_device_uid = device_uid
	_file_source = file_source
	_current_folder_uid = device_uid
	_path.clear()
	_file_source.drives_changed.connect(_on_drives_changed)
	refresh_entries()


func _on_drives_changed(device_uid: int) -> void:
	if device_uid == _device_uid:
		refresh_entries()


func refresh_entries() -> void:
	_entry_list.clear()
	for entry: Dictionary in _file_source.get_folder_entries(_device_uid, _current_folder_uid):
		var row := _entry_list.add_item(tr(entry["name"]) + entry["extension"], _get_icon_for(entry["kind"]))
		_entry_list.set_item_metadata(row, entry)
	_update_toolbar()


func _on_entry_activated(row: int) -> void:
	var entry: Dictionary = _entry_list.get_item_metadata(row)
	if entry["kind"] != KIND_FOLDER and entry["kind"] != KIND_DRIVE:
		return
	_current_folder_uid = entry["uid"]
	_path.append(entry)
	refresh_entries()


func _on_up_button_pressed() -> void:
	if _path.is_empty():
		return
	_path.pop_back()
	_current_folder_uid = _device_uid if _path.is_empty() else _path.back()["uid"]
	refresh_entries()


func _update_toolbar() -> void:
	_up_button.disabled = _path.is_empty()
	var names: Array[String] = [tr(ROOT_NAME_KEY)]
	for folder: Dictionary in _path:
		names.append(tr(folder["name"]))
	_path_label.text = PATH_SEPARATOR.join(names)


func _get_icon_for(kind: String) -> Texture2D:
	match kind:
		KIND_DRIVE:
			return drive_icon
		KIND_FOLDER:
			return folder_icon
		_:
			return file_icon
