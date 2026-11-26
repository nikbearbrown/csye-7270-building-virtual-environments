extends Control

const MAX_OPEN_WINDOWS := 15

@export var this_pc_window_scene: PackedScene
@export var active_button_color := Color(0.0, 0.05, 0.15)

var _taskbar_button_of: Dictionary[Control, Button] = {}
var _active_button_style: StyleBoxFlat

@onready var _this_pc_icon: DesktopIcon = $Desktop/ThisPCIcon
@onready var _window_layer: Control = $WindowLayer
@onready var _taskbar: ColorRect = $Taskbar
@onready var _taskbar_buttons: HBoxContainer = $Taskbar/Row/TaskbarButtons
@onready var _show_desktop_button: Button = $Taskbar/Row/ShowDesktopButton
@onready var _window_limit_dialog: AcceptDialog = $WindowLimitDialog

func _ready() -> void:
	_window_layer.offset_bottom = _taskbar.offset_top
	_active_button_style = StyleBoxFlat.new()
	_active_button_style.bg_color = active_button_color
	_this_pc_icon.activated.connect(_on_this_pc_icon_activated)
	_show_desktop_button.pressed.connect(_on_show_desktop_button_pressed)

func _on_this_pc_icon_activated() -> void:
	if not _can_open_window():
		_window_limit_dialog.popup_centered()
		return
	var window: ThisPCWindow = this_pc_window_scene.instantiate()
	_window_layer.add_child(window)
	window.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	window.minimize_requested.connect(_on_window_minimize_requested.bind(window))
	window.open(FileService.get_test_tablet_uid(), FileService)
	var button := _add_taskbar_button(_this_pc_icon.name_key, window)
	window.close_requested.connect(_on_window_close_requested.bind(window, button))
	_update_active_button()


func _can_open_window() -> bool:
	return _window_layer.get_child_count() < MAX_OPEN_WINDOWS


func _add_taskbar_button(name_key: String, window: Control) -> Button:
	var button := Button.new()
	button.text = name_key
	button.pressed.connect(_on_taskbar_button_pressed.bind(window))
	_taskbar_buttons.add_child(button)
	_taskbar_button_of[window] = button
	return button


func _update_active_button() -> void:
	var active_window: Control = null
	for window in _window_layer.get_children():
		if window.visible and not window.is_queued_for_deletion():
			active_window = window
	for window in _taskbar_button_of:
		var button := _taskbar_button_of[window]
		if window == active_window:
			button.add_theme_stylebox_override("normal", _active_button_style)
		else:
			button.remove_theme_stylebox_override("normal")


func _on_taskbar_button_pressed(window: Control) -> void:
	window.show()
	_window_layer.move_child(window, -1)
	_update_active_button()


func _on_window_minimize_requested(window: Control) -> void:
	window.hide()
	_update_active_button()


func _on_show_desktop_button_pressed() -> void:
	for window in _window_layer.get_children():
		window.hide()
	_update_active_button()


func _on_window_close_requested(window: Control, button: Button) -> void:
	_taskbar_button_of.erase(window)
	button.queue_free()
	window.queue_free()
	_update_active_button()
