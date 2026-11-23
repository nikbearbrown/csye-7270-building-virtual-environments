# ============================================================
# Class declaration: what it inherits from and what the whole script does
# ============================================================
extends Control  # The tablet OS root node TabletOS is a Control that fills the screen
## Tablet OS: shows the desktop icons and the opened software together.
## Software does not go looking for the backend itself (project rule 7b); when the tablet OS opens it, the tablet OS tells it "which tablet to show and where to get the data".
## A desktop icon does not know what it will open either; it only calls out "I was double-clicked", and the tablet OS decides which software to open.

# ============================================================
# Constants: values defined once that never change
# ============================================================
const MAX_OPEN_WINDOWS := 15  # The most windows the tablet can have open at once (GDD 5.2 "multiple instances"); once it is full, opening another does nothing

# ============================================================
# Exported variables (@export): things shown in the Inspector that can be swapped directly
# ============================================================
@export var this_pc_window_scene: PackedScene  # The scene file of the This PC window (this_pc_window.tscn); each time This PC is opened, we build a new window from it
@export var active_button_color := Color(0.0, 0.05, 0.15)  # The taskbar button of the window in use is painted this colour (darker than the taskbar blue); if it is hard to see, change it in the Inspector, for example to red

# ============================================================
# Member variables: state the script remembers itself
# ============================================================
var _taskbar_button_of: Dictionary[Control, Button] = {}  # Which taskbar button belongs to each open window; we record it when a window opens, cross it out when the window closes, and use it to find a window's button when painting colours
var _active_button_style: StyleBoxFlat  # The background of the "in use" button; made once in _ready() from active_button_color, then lent to the button of whichever window is on top

# ============================================================
# Node references (@onready): child nodes in the scene that we use
# ============================================================
@onready var _this_pc_icon: DesktopIcon = $Desktop/ThisPCIcon  # The "This PC" icon on the desktop; when the player double-clicks it, a new This PC window opens
@onready var _window_layer: Control = $WindowLayer  # Window layer: every open window is placed here; it sits between the desktop and the taskbar, so windows cover the desktop but not the taskbar
@onready var _taskbar: ColorRect = $Taskbar  # The taskbar at the bottom of the screen; the bottom edge of the window layer must line up with its top edge
@onready var _taskbar_buttons: HBoxContainer = $Taskbar/Row/TaskbarButtons  # The row of window buttons in the taskbar; each time a window opens, we put a button here, and it lines them up left to right on its own, filling the space to the left of "Show desktop"
@onready var _show_desktop_button: Button = $Taskbar/Row/ShowDesktopButton  # The "Show desktop" button at the far right of the taskbar; when the player clicks it, we minimise every window
@onready var _window_limit_dialog: AcceptDialog = $WindowLimitDialog  # The "too many windows" dialog; normally hidden, we pop it up when 15 are open and the player tries to open another

# ============================================================
# Engine callbacks: functions Godot calls automatically at certain moments (they act as the entry points; GDScript has no main)
# ============================================================
## Godot calls this once after the tablet OS and its children are all ready: we line up the bottom of the window layer with the taskbar, make the "in use" button background, then start listening for the "This PC" icon being double-clicked and the "Show desktop" button being clicked.
func _ready() -> void:
	_window_layer.offset_bottom = _taskbar.offset_top  # First we pull the bottom edge of the window layer up to the top edge of the taskbar; the taskbar height is filled in only once, on the taskbar, and this follows it
	_active_button_style = StyleBoxFlat.new()  # Then we make a new button background, just for the button "in use"
	_active_button_style.bg_color = active_button_color  # We paint it the colour filled in the Inspector; later _update_active_button() lends it to the button of the top window
	_this_pc_icon.activated.connect(_on_this_pc_icon_activated)  # Then we tell the icon: as soon as it is double-clicked, call our _on_this_pc_icon_activated()
	_show_desktop_button.pressed.connect(_on_show_desktop_button_pressed)  # Finally we tell the "Show desktop" button: as soon as it is clicked, call our _on_show_desktop_button_pressed()

# ============================================================
# Functions: called by others, or called inside this script
# ============================================================
## Called when the player double-clicks the "This PC" icon on the desktop (the icon emits activated): we build a new This PC window, put it in the window layer, make it fill the layer, then open it.
## This PC is the file manager and may have several instances (GDD 5.2), so each double-click builds a new one.
func _on_this_pc_icon_activated() -> void:
	if not _can_open_window():  # First we ask whether another window may still be opened; if it is already full
		_window_limit_dialog.popup_centered()  # we pop up "Too many windows, please close some first" in the middle of the screen; when the player clicks "OK" it closes itself
		return  # and then we build nothing and stop here
	var window: ThisPCWindow = this_pc_window_scene.instantiate()  # If we can still open one, we build a new window from the window scene file; it is not in the scene tree yet, so the player cannot see it
	_window_layer.add_child(window)  # Then we put it in the window layer; at that moment Godot calls its _ready(), and only then can it find its own DriveList and × button
	window.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)  # Then we make it fill the whole window layer (the whole area above the taskbar); every window is fixed at this size (GDD 5.2)
	window.minimize_requested.connect(_on_window_minimize_requested.bind(window))  # We put our _on_window_minimize_requested on this window's "I want to minimise" list, along with the window itself, so when we are called we know which one to hide
	# Temporary: there is no "player gets their own tablet" yet, so for now we use the test tablet in the backend fake data; later the player will hand their own tablet's ID to the tablet OS
	window.open(FileService.get_test_tablet_uid(), FileService)  # Then we tell the new window which tablet to show and that its data entry point is the backend FileService; the window lists the drives at once
	var button := _add_taskbar_button(_this_pc_icon.name_key, window)  # Then we put a button for this window on the taskbar, with the same name as written under the desktop icon; we keep the button we get back, since we need it when the window closes
	window.close_requested.connect(_on_window_close_requested.bind(window, button))  # Then we put _on_window_close_requested on this window's "I want to close" list, along with the window and its taskbar button, so when it closes we know which two to delete
	_update_active_button()  # Finally we check again which window is on top: the new window was just placed last, so its button turns dark and the previous one goes back to normal


## Before opening any new window, we call this first to ask: may we open another one?
## The number of children in the window layer is the number of open windows (minimised ones count too; they are only hidden). Later, other software and opened files will also ask it first.
func _can_open_window() -> bool:
	return _window_layer.get_child_count() < MAX_OPEN_WINDOWS  # If fewer than 15 windows are open, we answer "yes"; at 15 we answer "no"


## Each time we open a window, we call this: we put a new button in the taskbar's button row, with the software's name on it.
## The button remembers which window it belongs to, and when the player clicks it we show that window. The finished button is handed back to the caller, to be deleted together with the window when it closes.
func _add_taskbar_button(name_key: String, window: Control) -> Button:
	var button := Button.new()  # First we build a new button; it is not in the scene tree yet, so the player cannot see it
	button.text = name_key  # We write the translation key of the software's name on the button; when shown, the button looks it up in ui_text.csv by itself and turns it into "This PC"
	button.pressed.connect(_on_taskbar_button_pressed.bind(window))  # We put our _on_taskbar_button_pressed on this button's "I was clicked" list, along with its window, so when we are called we know which one to show
	_taskbar_buttons.add_child(button)  # Then we put it in the taskbar's button row; the row places it to the right of the existing buttons
	_taskbar_button_of[window] = button  # Then we record "this window's button is this one"; we need it to find the button from the window when painting colours
	return button  # Finally we hand the button back; _on_this_pc_icon_activated() binds it together with the window to "I want to close"


## Whenever the window order or which windows are shown/hidden changes, we call this: we find the window now on top, paint its taskbar button dark, and put the other buttons back to normal.
## Called from five places: opening a window, clicking a taskbar button, minimising, show desktop, and closing a window.
func _update_active_button() -> void:
	var active_window: Control = null  # First we assume no window is in use (for example, all are minimised)
	for window in _window_layer.get_children():  # We look at the windows one by one, from the bottom up
		if window.visible and not window.is_queued_for_deletion():  # If this window is visible and is not about to be deleted
			active_window = window  # we take it as the top one for now; later ones are drawn higher, so the one left after we finish is the real top window
	for window in _taskbar_button_of:  # Then we take out each open window and its button, one by one
		var button := _taskbar_button_of[window]  # We find this window's taskbar button
		if window == active_window:  # If it is the window in use
			button.add_theme_stylebox_override("normal", _active_button_style)  # we swap the button's normal background for the dark one
		else:  # Otherwise
			button.remove_theme_stylebox_override("normal")  # we take off the swapped-in background, and the button goes back to Godot's default look


## Called when the player clicks one of the taskbar buttons (the button emits pressed): we show the window that belongs to this button and bring it in front of all the others.
func _on_taskbar_button_pressed(window: Control) -> void:
	window.show()  # First we show the window; if it was minimised (hidden) before, it is visible again now
	_window_layer.move_child(window, -1)  # Then we move it to the last place in the window layer; later children are drawn on top, so it covers the other windows
	_update_active_button()  # Finally we repaint the colours: its button turns dark and the previous top one goes back to normal


## Called when the player clicks a window's — button (that window emits minimize_requested): we hide that window.
## The window is only out of sight, not deleted, and everything in it is still there; later, when its taskbar button is clicked, we show it again.
func _on_window_minimize_requested(window: Control) -> void:
	window.hide()  # We hide the window that sent the request, and the desktop (or another window) behind it shows through
	_update_active_button()  # Then we repaint the colours: the next window that shows through becomes the one in use; if only the desktop is left behind, no button turns dark


## Called when the player clicks the "Show desktop" button at the far right of the taskbar (the button emits pressed): we minimise every window to reveal the desktop (GDD 5.2).
## The windows are only hidden, and their taskbar buttons are all still there; whichever button is clicked, that window comes back.
func _on_show_desktop_button_pressed() -> void:
	for window in _window_layer.get_children():  # We take the windows out of the window layer one by one
		window.hide()  # and hide each one, the same as the player clicking its own —
	_update_active_button()  # Finally we repaint the colours: now no window is in use, so every button goes back to normal


## Called when the player clicks a window's × button (that window emits close_requested): we delete that window together with its taskbar button.
## Unlike minimising, once closed the window is gone; to see it again, a new one has to be opened from the desktop icon.
func _on_window_close_requested(window: Control, button: Button) -> void:
	_taskbar_button_of.erase(window)  # First we cross this window out of the "which button belongs to which window" record, so colour painting no longer cares about it
	button.queue_free()  # Then we delete this button on the taskbar; the button row moves the buttons on its right to the left by itself to fill the gap
	window.queue_free()  # Then we delete the window itself; the window (or desktop) behind it shows through
	_update_active_button()  # Finally we repaint the colours: the window that shows through becomes the one in use
