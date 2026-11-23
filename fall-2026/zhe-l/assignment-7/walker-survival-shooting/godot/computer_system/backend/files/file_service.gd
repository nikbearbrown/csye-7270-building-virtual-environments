# ============================================================
# Class declaration: what it extends, what the whole script does
# ============================================================
extends Node  # We extend Node because it is registered as an Autoload (a global singleton): it is in the scene tree from the start of the game, and anyone can call it as FileService
## The backend file service: it keeps "where everything is" for every drive, folder and file on all tablets, computers and external devices (design document 5.2, code rule 6a).
## The UI (the desktop, the This PC window) can only ask it questions (the get_ functions) or send requests (such as connect_drive()); the UI itself never stores or changes this data.
## Everything it hands out is a plain Dictionary, never the internal Entry objects, so the interface will not have to change when the backend later moves to another process or is saved as a JSON save file.
## Every device's drive has its own record, which stays in the backend all the time and is not deleted when it is disconnected (decided by the user on 2026-11-13).
## Each tablet is one "device" with its own drive C, desktop and drive-letter table; in co-op every player's tablet is different, so every question must say which device it is about (code rule 6: there is no global "the player").
## Drive letters are assigned on connection, like in Windows: C is always the tablet itself, D is always kept for the base computer, and external devices start at E and take the next free letter.
## For now it holds fake data (one test tablet and the computer's drive); once there are save files, this will read from the save instead.
## Note: its Autoload name is FileService, so we do not write class_name here, or the two names would clash.

# ============================================================
# Constants: values defined once that never change
# ============================================================
const NO_PARENT := 0  # 0 means "no parent": a drive is at the top level, so its parent is 0; real IDs therefore start at 1
const NO_DEVICE := 0  # 0 also means "no such device": a device's ID is the ID of its own drive C, and real IDs start at 1
const FIRST_UID := 1  # The ID the first entry gets; every new entry after that adds 1
const KIND_DRIVE := "drive"  # This entry is a drive (a tablet's, the computer's, or an external device's)
const KIND_FOLDER := "folder"  # This entry is a folder, which can hold more files and folders
const KIND_FILE := "file"  # This entry is a file (software or a document); its def_id points to a FileData id
const TABLET_DRIVE_LETTER := "C"  # The tablet's drive letter: design document 5.2 says the tablet is drive C; it is also the first letter in the drive-letter table
const COMPUTER_DRIVE_LETTER := "D"  # The base computer's drive letter: design document 5.2 says the computer is drive D, and this letter is always kept for the computer
const FIRST_EXTERNAL_LETTER := "E"  # External devices start from this letter (decided by the user on 2026-11-13)
const LAST_DRIVE_LETTER := "Z"  # Drive letters go up to this letter at most
const NO_FREE_LETTER := ""  # An empty string means "E to Z are all taken"; then the external device cannot connect
const NO_DRIVE_LABEL := ""  # The drive's own name (volume label, such as "Local Disk") is not decided yet [TBD], so it stays empty; the drive letter is not stored here but in each device's drive-letter table
const DESKTOP_FOLDER_NAME := "FOLDER_DESKTOP"  # The desktop folder's name. We store the translation key, not the text: when the UI shows it, tr() turns it into "Desktop" in the player's language (the desktop is a folder on drive C, decided by the user on 2026-11-11)

# ============================================================
# Signals: changes that already happened in the backend, telling the UI to redraw
# ============================================================
signal drives_changed(device_uid: int)  # The drives one device can see have changed (a device was connected or disconnected); the argument says which device. The This PC window showing that device hears it and calls get_drives() again; it is only used to refresh the screen and decides nothing

# ============================================================
# Member variables: state used inside this script (leading underscore = internal to this script)
# ============================================================
var _entries: Dictionary[int, Entry] = {}  # Every entry: ID -> that entry. Drives, folders and files all live in this one table and are linked into a tree by parent_uid
var _next_uid := FIRST_UID  # The ID the next entry should get; only _add_entry() uses it and increases it, so IDs never repeat
var _mount_tables: Dictionary[int, Dictionary] = {}  # Each device's drive-letter table: device ID -> (drive letter -> drive ID), listing only the drives connected to that device now. Only create_tablet(), connect_drive() and disconnect_drive() change it; get_drives() reads it
var _desktop_uids: Dictionary[int, int] = {}  # Each device's desktop: device ID -> its desktop folder ID; create_tablet() records it, get_desktop_uid() hands it out
var _computer_drive_uid := NO_PARENT  # The ID of the base computer's drive; _build_fake_data() records it after building it, and connect_drive() uses it to recognize "this is the computer" and give it D
var _test_tablet_uid := NO_DEVICE  # Temporary: the ID of the test tablet in the fake data. Once players have their own tablets, the tablet system will hand the device ID to the software, and this variable and get_test_tablet_uid() will be deleted

# ============================================================
# Inner classes: small classes used only in this script
# ============================================================
## One entry in the file system (a drive, folder or file). Used only inside the backend; before it is handed out, to_dict() turns it into plain data.
class Entry:
	var uid: int  # This entry's unique ID
	var parent_uid: int  # Which entry it sits in; drives are at the top level, so this is NO_PARENT
	var kind: String  # Which kind it is: KIND_DRIVE, KIND_FOLDER or KIND_FILE
	var name: String  # A drive's volume label (not decided yet, empty for now) or a folder's name; a file's name will later come from FileData's display_name, so it can be empty here
	var def_id: StringName  # Used only by files: which kind of file it is, matching a FileData id; empty for drives and folders

	## Called by _add_entry() when it makes a new entry: we fill in all five things at once.
	func _init(new_uid: int, new_parent_uid: int, new_kind: String, new_name: String, new_def_id: StringName) -> void:
		uid = new_uid  # We record its ID
		parent_uid = new_parent_uid  # record which entry it sits in
		kind = new_kind  # record whether it is a drive, a folder or a file
		name = new_name  # record its name
		def_id = new_def_id  # record which kind of file it is (empty here for drives and folders)

	## Called before the backend hands an entry out: we copy it into a plain Dictionary, so if the outside changes this copy, it cannot change the real data in the backend.
	func to_dict() -> Dictionary:
		return {"uid": uid, "parent_uid": parent_uid, "kind": kind, "name": name, "def_id": def_id}  # We copy the five things in as they are, with keys named like the variables

# ============================================================
# Engine callbacks: functions Godot calls automatically at certain moments (the entry points, since GDScript has no main)
# ============================================================
## Godot calls this once, after putting this Autoload into the scene tree at the start of the game: we build the fake data first, so there is something to answer whoever asks later.
func _ready() -> void:
	_build_fake_data()  # We build one test tablet (drive C and the desktop) and the computer's drive

# ============================================================
# Functions: queries and requests for the UI, and functions used inside this script
# ============================================================
## Later, starting a new save, or a new player joining in co-op, will call this: we build a new tablet for them and hand back its device ID.
## The new tablet has its own drive C (always connected, drive letter C) and a desktop folder on drive C.
func create_tablet() -> int:
	var tablet_uid := _add_entry(NO_PARENT, KIND_DRIVE, NO_DRIVE_LABEL)  # First we build this tablet's own drive; this drive's ID is also this device's ID
	_mount_tables[tablet_uid] = {TABLET_DRIVE_LETTER: tablet_uid}  # Then we give it a new drive-letter table that at first holds only itself, with drive letter C; from then on get_drives() always hands it out
	_desktop_uids[tablet_uid] = _add_entry(tablet_uid, KIND_FOLDER, DESKTOP_FOLDER_NAME)  # Then we build the desktop folder on its drive C and record its ID, which get_desktop_uid() will hand out
	return tablet_uid  # Finally we hand back the device ID; anyone who asks about this tablet later asks with this ID


## The This PC window calls this: we list the drives one device can see now, sorted by drive letter from C to Z.
## Each drive's copy gets one extra item, "letter": the drive letter it was given on this device. If the device does not exist, we hand back an empty list.
func get_drives(device_uid: int) -> Array[Dictionary]:
	var result: Array[Dictionary] = []  # We first prepare an empty result list
	if not _mount_tables.has(device_uid):  # If there is no such device
		return result  # we hand back the empty list
	var table: Dictionary = _mount_tables[device_uid]  # Otherwise, we take out this device's drive-letter table
	for code in range(TABLET_DRIVE_LETTER.unicode_at(0), LAST_DRIVE_LETTER.unicode_at(0) + 1):  # Then we look at the letters from C to Z one by one, so the result comes out sorted by drive letter
		var letter := String.chr(code)  # We turn the letter's code back into the letter, for example 67 into "C"
		if not table.has(letter):  # If no drive holds this letter on this device
			continue  # we look at the next letter
		var drive := _entries[table[letter]].to_dict()  # Otherwise, we find this drive through the drive-letter table and copy it
		drive["letter"] = letter  # Then we write the drive letter it got on this device into the copy; this is what the This PC window shows
		result.append(drive)  # and put it into the result
	return result  # Finally we hand it to the This PC window, which lists these drives one row each


## The desktop and the This PC window call this: we list what sits directly inside one entry (without looking into deeper folders).
## What we hand out is a copy (Dictionary) of each entry, in the order they were built.
func get_entries_in(parent_uid: int) -> Array[Dictionary]:
	var result: Array[Dictionary] = []  # We first prepare an empty result list
	for entry: Entry in _entries.values():  # Then we take out every entry one by one and look at it
		if entry.parent_uid == parent_uid:  # If this entry sits right inside the entry we are looking for
			result.append(entry.to_dict())  # we put its copy into the result
	return result  # Finally we hand the result to whoever asked; Godot's Dictionary remembers insertion order, so the order is the order they were built in


## The desktop UI will call this later: it asks for one device's desktop folder ID, then calls get_entries_in() with it to know what is on the desktop.
func get_desktop_uid(device_uid: int) -> int:
	return _desktop_uids.get(device_uid, NO_PARENT)


## The "connect the tablet to the computer" action will call this later: it asks for the computer drive's ID, then calls connect_drive() with it.
func get_computer_drive_uid() -> int:
	return _computer_drive_uid


## Temporary: there is no "player gets their own tablet" yet, so the This PC window uses this for now to get the ID of the test tablet in the fake data. To be deleted later.
func get_test_tablet_uid() -> int:
	return _test_tablet_uid


## The "connect to the computer" and "plug in an external device" actions will call this later (how and where to connect is not decided yet): we connect this drive to this device and give it a drive letter, so this device can see it.
## The computer always gets D; other devices get the first free letter from E. A drive can be connected to only one device at a time [TBC: in co-op, can the computer be connected to several tablets at once?].
## We hand back true if it really got connected; otherwise we change nothing and hand back false.
func connect_drive(device_uid: int, drive_uid: int) -> bool:
	if not _mount_tables.has(device_uid):  # If there is no such device
		return false  # we change nothing and tell the caller "cannot connect"
	if not _entries.has(drive_uid) or _entries[drive_uid].kind != KIND_DRIVE:  # If this drive ID does not exist, or it is not a drive at all
		return false  # we change nothing and tell the caller "cannot connect"
	if _find_device_of(drive_uid) != NO_DEVICE:  # If this drive is already connected to some device (this one or another player's)
		return false  # we change nothing and tell the caller "cannot connect"
	var table: Dictionary = _mount_tables[device_uid]  # First we take out this device's drive-letter table
	var letter := COMPUTER_DRIVE_LETTER if drive_uid == _computer_drive_uid else _find_free_external_letter(table)  # Then we decide the drive letter: the computer gets D, other devices look for a free one on this device starting from E
	if letter == NO_FREE_LETTER:  # If E to Z are all taken
		return false  # we change nothing and tell the caller "cannot connect"
	table[letter] = drive_uid  # We register it in this device's drive-letter table; from then on get_drives() hands it out
	drives_changed.emit(device_uid)  # Then we tell the UI: the drives this device can see have changed; the This PC window showing this device hears it and lists the drives again
	return true  # Finally we tell the caller: connected


## The "disconnect from the computer" and "unplug an external device" actions will call this later: we take this drive out of this device's drive-letter table, so this device can no longer see it, and its letter is freed for the next device.
## The drive's data stays in its own record and is not deleted. The tablet's own drive C cannot be unplugged. We hand back true if it really got disconnected, otherwise false.
func disconnect_drive(device_uid: int, drive_uid: int) -> bool:
	if not _mount_tables.has(device_uid):  # If there is no such device
		return false  # we change nothing and tell the caller "nothing changed"
	var table: Dictionary = _mount_tables[device_uid]  # First we take out this device's drive-letter table
	var letter: Variant = table.find_key(drive_uid)  # Then we look up which letter this drive holds in the table; if it is not there, we get null
	if letter == null or letter == TABLET_DRIVE_LETTER:  # If it is not connected to this device, or it is the tablet's own drive C
		return false  # we change nothing and tell the caller "nothing changed"
	table.erase(letter)  # Otherwise, we take it out of the drive-letter table; from then on get_drives() no longer hands it out, and the letter is free again
	drives_changed.emit(device_uid)  # Then we tell the UI: the drives this device can see have changed; the This PC window showing this device hears it and lists the drives again
	return true  # Finally we tell the caller: disconnected


## Called by connect_drive() to check "is this drive already connected somewhere else": we look for it in every device's drive-letter table and hand back the device it is connected to; if it is not connected anywhere, we hand back NO_DEVICE.
func _find_device_of(drive_uid: int) -> int:
	for device_uid: int in _mount_tables:  # We take out every device one by one and look at it
		if _mount_tables[device_uid].find_key(drive_uid) != null:  # If this device's drive-letter table has this drive
			return device_uid  # then it is connected to this device, and we hand back this device
	return NO_DEVICE  # We looked at every device and did not find it, so it is not connected anywhere


## Called by connect_drive() when it gives an external device a drive letter: we search this device's drive-letter table from E onward and hand back the first letter not taken; if all are taken, we hand back NO_FREE_LETTER.
func _find_free_external_letter(table: Dictionary) -> String:
	for code in range(FIRST_EXTERNAL_LETTER.unicode_at(0), LAST_DRIVE_LETTER.unicode_at(0) + 1):  # We look at the letters from E to Z one by one
		var letter := String.chr(code)  # We turn the letter's code back into the letter
		if not table.has(letter):  # If no drive holds this letter on this device
			return letter  # it is the one we want, and we hand it back
	return NO_FREE_LETTER  # Every letter up to Z is taken, so we hand back "no free letter"


## Called inside this script to build a new entry: we issue a new ID, build the entry, put it into the main table, then hand back the ID.
## Later, paste and new folder will both go through here, so IDs are issued in only this one place and never repeat (code rule 4).
func _add_entry(parent_uid: int, kind: String, entry_name: String, def_id: StringName = &"") -> int:
	var entry := Entry.new(_next_uid, parent_uid, kind, entry_name, def_id)  # First we build this entry with the next free ID
	_entries[entry.uid] = entry  # Then we put it into the main table, so it can be found by its ID later
	_next_uid += 1  # Then we move "the next ID" up by one, kept for the next entry
	return entry.uid  # Finally we hand back this entry's ID; the caller can use it as the parent of other entries


## Called once by _ready(): we build the fake data for testing. Once there are save files, this will read from the save instead.
func _build_fake_data() -> void:
	_test_tablet_uid = create_tablet()  # First we build one test tablet (drive C and the desktop) and record its ID; for now the This PC window gets it through get_test_tablet_uid()
	_computer_drive_uid = _add_entry(NO_PARENT, KIND_DRIVE, NO_DRIVE_LABEL)  # Then we build the base computer's drive and record its ID; it is always in the computer but not yet connected to any tablet, so at first the tablets cannot see it
