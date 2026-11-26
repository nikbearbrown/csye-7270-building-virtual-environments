extends Node

const NO_PARENT := 0
const NO_DEVICE := 0
const FIRST_UID := 1
const KIND_DRIVE := "drive"
const KIND_FOLDER := "folder"
const KIND_FILE := "file"
const DEFINITION_FOLDERS: Array[String] = [
	"res://computer_system/file_types/data/software/",
	"res://items/documents/",
]
const DEFINITION_EXTENSION := ".tres"
const NO_DRIVE_LABEL := ""
const COMPUTER_DRIVE_LABEL := "DRIVE_BASE_COMPUTER"
const HOME_FOLDER_NAME := "home"
const SOFTWARE_FOLDER_NAME := "FOLDER_SOFTWARE"
const DESKTOP_FOLDER_NAME := "FOLDER_DESKTOP"
const CLIPBOARD_EMPTY := "empty"
const CLIPBOARD_TEXT := "text"

signal drives_changed(device_uid: int)

var _entries: Dictionary[int, Entry] = {}
var _next_uid := FIRST_UID
var _mounted_drives: Dictionary[int, Array] = {}
var _desktop_uids: Dictionary[int, int] = {}
var _software_uids: Dictionary[int, int] = {}
var _computer_drive_uid := NO_PARENT
var _definitions: Dictionary[StringName, FileData] = {}
var _clipboards: Dictionary[int, Dictionary] = {}
var _test_tablet_uid := NO_DEVICE

class Entry:
	var uid: int
	var parent_uid: int
	var kind: String
	var name: String
	var def_id: StringName

	func _init(new_uid: int, new_parent_uid: int, new_kind: String, new_name: String, new_def_id: StringName) -> void:
		uid = new_uid
		parent_uid = new_parent_uid
		kind = new_kind
		name = new_name
		def_id = new_def_id

	func to_dict() -> Dictionary:
		return {"uid": uid, "parent_uid": parent_uid, "kind": kind, "name": name, "def_id": def_id}

func _ready() -> void:
	_build_preset_data()

func create_tablet() -> int:
	var tablet_uid := _add_entry(NO_PARENT, KIND_DRIVE, NO_DRIVE_LABEL)
	_mounted_drives[tablet_uid] = []
	var home_uid := _add_entry(tablet_uid, KIND_FOLDER, HOME_FOLDER_NAME)
	_desktop_uids[tablet_uid] = _add_entry(home_uid, KIND_FOLDER, DESKTOP_FOLDER_NAME)
	_software_uids[tablet_uid] = _add_entry(home_uid, KIND_FOLDER, SOFTWARE_FOLDER_NAME)
	return tablet_uid


func get_folder_entries(device_uid: int, folder_uid: int) -> Array[Dictionary]:
	if not _can_device_see(device_uid, folder_uid):
		return []
	if _entries[folder_uid].kind == KIND_FILE:
		return []
	var result := get_entries_in(folder_uid)
	if folder_uid == device_uid:
		for drive_uid: int in _mounted_drives[device_uid]:
			result.append(_describe(_entries[drive_uid]))
	return result


func get_entries_in(parent_uid: int) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for entry: Entry in _entries.values():
		if entry.parent_uid == parent_uid:
			result.append(_describe(entry))
	return result


func get_desktop_uid(device_uid: int) -> int:
	return _desktop_uids.get(device_uid, NO_PARENT)


func get_software_uid(device_uid: int) -> int:
	return _software_uids.get(device_uid, NO_PARENT)


func get_computer_drive_uid() -> int:
	return _computer_drive_uid


func get_test_tablet_uid() -> int:
	return _test_tablet_uid


func connect_drive(device_uid: int, drive_uid: int) -> bool:
	if not _mounted_drives.has(device_uid):
		return false
	if not _entries.has(drive_uid) or _entries[drive_uid].kind != KIND_DRIVE:
		return false
	if _mounted_drives.has(drive_uid):
		return false
	if _find_device_of(drive_uid) != NO_DEVICE:
		return false
	_mounted_drives[device_uid].append(drive_uid)
	drives_changed.emit(device_uid)
	return true


func disconnect_drive(device_uid: int, drive_uid: int) -> bool:
	if not _mounted_drives.has(device_uid):
		return false
	if not _mounted_drives[device_uid].has(drive_uid):
		return false
	_mounted_drives[device_uid].erase(drive_uid)
	drives_changed.emit(device_uid)
	return true


func set_clipboard_text(device_uid: int, text: String) -> bool:
	if not _mounted_drives.has(device_uid):
		return false
	_clipboards[device_uid] = {"kind": CLIPBOARD_TEXT, "text": text}
	return true


func get_clipboard(device_uid: int) -> Dictionary:
	if not _clipboards.has(device_uid):
		return {"kind": CLIPBOARD_EMPTY}
	return _clipboards[device_uid].duplicate()


func get_document(device_uid: int, file_uid: int) -> Dictionary:
	if not _can_device_see(device_uid, file_uid):
		return {}
	var entry := _entries[file_uid]
	var definition := _get_definition(entry.def_id) as DocumentData
	if entry.kind != KIND_FILE or definition == null:
		return {}
	return {
		"name": entry.name,
		"extension": _extension_of(definition),
		"content": definition.content,
		"read_only": definition.read_only,
	}


func _describe(entry: Entry) -> Dictionary:
	var result := entry.to_dict()
	result["extension"] = _extension_of(_get_definition(entry.def_id))
	return result


func _extension_of(definition: FileData) -> String:
	var document := definition as DocumentData
	if document == null or document.document_type == null:
		return ""
	return document.document_type.extension


func _get_definition(def_id: StringName) -> FileData:
	if def_id == &"":
		return null
	if _definitions.has(def_id):
		return _definitions[def_id]
	for folder in DEFINITION_FOLDERS:
		var path := folder + String(def_id).to_lower() + DEFINITION_EXTENSION
		if ResourceLoader.exists(path):
			_definitions[def_id] = load(path) as FileData
			return _definitions[def_id]
	push_warning("FileService: definition %s not found (was the conversion script run?)" % def_id)
	return null


func _can_device_see(device_uid: int, uid: int) -> bool:
	if not _mounted_drives.has(device_uid) or not _entries.has(uid):
		return false
	var top_uid := uid
	while _entries[top_uid].parent_uid != NO_PARENT:
		top_uid = _entries[top_uid].parent_uid
	return top_uid == device_uid or _mounted_drives[device_uid].has(top_uid)


func _find_device_of(drive_uid: int) -> int:
	for device_uid: int in _mounted_drives:
		if _mounted_drives[device_uid].has(drive_uid):
			return device_uid
	return NO_DEVICE


func _add_entry(parent_uid: int, kind: String, entry_name: String, def_id: StringName = &"") -> int:
	var entry := Entry.new(_next_uid, parent_uid, kind, entry_name, def_id)
	_entries[entry.uid] = entry
	_next_uid += 1
	return entry.uid


func _build_preset_data() -> void:
	_test_tablet_uid = create_tablet()
	_computer_drive_uid = _add_entry(NO_PARENT, KIND_DRIVE, COMPUTER_DRIVE_LABEL)
