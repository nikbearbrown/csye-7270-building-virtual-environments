extends Node

const NO_PARENT := 0
const ROOT_KEY := 0
const KIND_DRIVE := "drive"
const KIND_FOLDER := "folder"
const KIND_FILE := "file"
const TEST_TREE := {
	ROOT_KEY: [
		[101, KIND_FOLDER, "Desktop"],
		[102, KIND_FOLDER, "Test Folder"],
		[201, KIND_DRIVE, "Base Computer"],
		[301, KIND_DRIVE, "Test USB Drive"],
	],
	102: [
		[103, KIND_FOLDER, "Second Level"],
		[104, KIND_FILE, "Test File"],
	],
	103: [
		[105, KIND_FOLDER, "Third Level"],
	],
	201: [
		[202, KIND_FOLDER, "Test Data"],
	],
}

signal drives_changed(device_uid: int)

func get_folder_entries(device_uid: int, folder_uid: int) -> Array[Dictionary]:
	var key := ROOT_KEY if folder_uid == device_uid else folder_uid
	var result: Array[Dictionary] = []
	for item: Array in TEST_TREE.get(key, []):
		var parent_uid: int = NO_PARENT if item[1] == KIND_DRIVE else folder_uid
		result.append({"uid": item[0], "parent_uid": parent_uid, "kind": item[1], "name": item[2], "def_id": &"", "extension": ""})
	return result
