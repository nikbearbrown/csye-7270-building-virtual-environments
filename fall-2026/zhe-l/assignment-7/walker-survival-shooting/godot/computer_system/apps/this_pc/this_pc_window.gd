# ============================================================
# Class declaration: class name, what it inherits from and what the whole script does
# ============================================================
class_name ThisPCWindow  # We name this script ThisPCWindow, so the tablet OS can use it as a type, find it and call open()
extends PanelContainer  # The shell of the This PC window is a PanelContainer, so our script inherits from it too, so it can be attached to ThisPCWindow
## This PC window: when it is opened, someone hands it "which tablet to show" and "where to get the data", and it lists the drives this tablet can see, one row each, in DriveList.
## It is software that can be lifted out on its own (project rule 7b): it does not go looking for the backend itself, it only uses the data entry point handed in through open();
## in the game that entry point is the backend FileService, and when run alone (the demo scene in the demo folder) it is a fake entry point; the window itself cannot tell the difference.
## It only displays; it does not save or change any drive data (rule 5); what it shows is only a copy.

# ============================================================
# Signals: tell the outside "what has already happened"
# ============================================================
signal close_requested  # The player clicked the × at the top right and wants to close this window; the window does not decide how to close itself, the tablet OS (or demo scene) that opened it receives this and closes it
signal minimize_requested  # The player clicked the — at the top right and wants to put this window away; the window does not decide how to put itself away, the tablet OS receives this, hides it and keeps it on the taskbar

# ============================================================
# Exported variables (@export): things shown in the Inspector that can be swapped directly
# ============================================================
@export var drive_icon: Texture2D  # The icon shown in front of each drive: drag an image in from the Inspector. For now icon.svg is a placeholder; later it becomes a proper drive icon

# ============================================================
# Member variables: state used inside the script (a leading underscore = used only inside this script)
# ============================================================
var _device_uid: int  # Which device (which tablet) this window shows; handed in through open(), and refresh_drives() uses it to ask the data entry point
var _file_source: Node  # The data entry point handed in: in the game it is the backend FileService, when run alone it is a fake entry point. It must have a get_drives(device_uid) function and a drives_changed(device_uid) signal

# ============================================================
# Node references (@onready): child nodes in the scene that we use
# ============================================================
@onready var _drive_list: ItemList = $Layout/DriveList  # The list that shows the drives; refresh_drives() refills the drives here every time, and this is what the player sees
@onready var _minimize_button: Button = $Layout/TitleBar/MinimizeButton  # The — button at the right of the title bar; when the player clicks it, we emit minimize_requested
@onready var _close_button: Button = $Layout/TitleBar/CloseButton  # The × button at the right of the title bar; when the player clicks it, we emit close_requested

# ============================================================
# Engine callbacks: functions Godot calls automatically at certain moments (they act as the entry points; GDScript has no main)
# ============================================================
## Godot calls this once after the window and its children are all ready: we start listening for the — and × buttons being clicked.
func _ready() -> void:
	_minimize_button.pressed.connect(_on_minimize_button_pressed)  # First we tell the — button: as soon as it is clicked, call our _on_minimize_button_pressed()
	_close_button.pressed.connect(_on_close_button_pressed)  # Then we tell the × button: as soon as it is clicked, call our _on_close_button_pressed()

# ============================================================
# Functions: called by others, or called inside this script
# ============================================================
## Called when the player clicks the — button (the button emits pressed): we pass "the player wants to put the window away" on to the outside.
func _on_minimize_button_pressed() -> void:
	minimize_requested.emit()  # We emit minimize_requested; the tablet OS receives it and hides the window, and brings it back later when its taskbar button is clicked


## Called when the player clicks the × button (the button emits pressed): we pass "the player wants to close the window" on to the outside.
func _on_close_button_pressed() -> void:
	close_requested.emit()  # We emit close_requested; the tablet OS or demo scene that opened us receives it and decides whether to hide the window or delete it



## Called when the tablet OS (or the demo scene when run alone) opens This PC: it tells the window which tablet to show and where to get the data, and the window lists the drives at once.
## This is this software's "interface": all that comes in is a device ID and a data entry point, and all that goes out is questions to the data entry point.
func open(device_uid: int, file_source: Node) -> void:
	if _file_source != null and _file_source.drives_changed.is_connected(_on_drives_changed):  # If we were opened before and are still listening to the old data entry point
		_file_source.drives_changed.disconnect(_on_drives_changed)  # we stop listening to it first, so one change does not refresh twice
	_device_uid = device_uid  # First we note which tablet to show
	_file_source = file_source  # Then we note the data entry point; from now on we get the drives from it
	_file_source.drives_changed.connect(_on_drives_changed)  # Then we tell the data entry point: whenever any device's drives change, call our _on_drives_changed()
	refresh_drives()  # Finally we ask for the drives right away and fill the list, so the player sees them as soon as it opens


## Called when the data entry point emits drives_changed: if the change is on the tablet we show, we list the drives again; a change on another player's tablet has nothing to do with us.
func _on_drives_changed(device_uid: int) -> void:
	if device_uid == _device_uid:  # If the tablet that changed is exactly the one this window shows
		refresh_drives()  # we ask for the drives again


## Called from open(), and when our tablet's drives change: we ask the data entry point for the latest drives and refill DriveList.
func refresh_drives() -> void:
	_drive_list.clear()  # First we clear out all the old items in the list, so the same drive does not show up twice
	for drive: Dictionary in _file_source.get_drives(_device_uid):  # Then we ask the data entry point for copies of all the drives this tablet can see, and look at them one by one
		_drive_list.add_item(drive["letter"], drive_icon)  # For each drive we add a row: the text is the drive letter it got this time (C, D, E...), with drive_icon in front; this row is what the player sees in the window
