# ============================================================
# Class declaration: class name, what it inherits from and what the whole script does
# ============================================================
class_name DesktopIcon  # We name this script DesktopIcon, so the tablet OS can use it as a type
extends VBoxContainer  # The shell of a desktop icon is a VBoxContainer (image on top, name below), so our script inherits from it too
## Desktop icon: one icon on the desktop, with an image on top and a line of name below.
## It only "displays" and "tells others it was double-clicked"; it does not know what to open after a double-click; the tablet OS decides what to open.
## So the same scene can be used for every desktop icon: "This PC", and later folders, files, shortcuts and so on.

# ============================================================
# Signals: tell others "what has already happened"
# ============================================================
signal activated  # The player double-clicked this icon; the tablet OS hears it and decides which software to open

# ============================================================
# Exported variables (@export): things shown in the Inspector that each icon can fill in for itself
# ============================================================
@export var icon_texture: Texture2D  # The image this icon shows; when placing an icon on the desktop, drag an image in from the Inspector
@export var name_key: String  # The name under this icon: fill in a key from the translation lookup table (e.g. UI_THIS_PC), and Godot shows it as text in the current language

# ============================================================
# Node references (@onready): child nodes in the scene that we use
# ============================================================
@onready var _icon: TextureRect = $Icon  # The image on top
@onready var _name_label: Label = $NameLabel  # The line of name below

# ============================================================
# Engine callbacks: functions Godot calls automatically at certain moments (they act as the entry points; GDScript has no main)
# ============================================================
## Godot calls this once after the icon and its children are all ready: we put the image and name filled in the Inspector onto the children, and the player sees them.
func _ready() -> void:
	_icon.texture = icon_texture  # First we hand this icon's own image to the Icon on top to show
	_name_label.text = name_key  # Then we hand the name key to NameLabel; the Label looks up the text for the current language in the translation lookup table by itself


## Godot calls this when the mouse presses a button or moves inside the icon: we only care about a "left double-click", and when we see one we emit activated.
func _gui_input(event: InputEvent) -> void:
	var mouse_button := event as InputEventMouseButton  # First we check whether this is a mouse button event; if not, we get null here
	if mouse_button == null:  # If it is not a mouse button event (for example, just mouse movement)
		return  # we do nothing
	if mouse_button.button_index == MOUSE_BUTTON_LEFT and mouse_button.pressed and mouse_button.double_click:  # If it is the left button, a press, and a double-click
		accept_event()  # we say "we handled this click", so it is not passed on to the desktop behind
		activated.emit()  # Then we tell the tablet OS: the player double-clicked me; when the tablet OS receives it, it opens the matching software
