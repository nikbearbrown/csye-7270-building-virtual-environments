# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name ScreenTablet  # We name this script ScreenTablet, so the brain can use it as a type, find it and call set_shown()
extends Node3D  # The on-screen tablet needs a position in a small 3D world and must move, so we extend Node3D
## The brain (PlayerController) tells this on-screen tablet whether to come out or go back (design document section 5.8):
## while the tablet is held in one hand, it slides in from outside the right edge of the screen and stops in the lower right; once it has stopped, its screen lights, and later this is the one the player operates with the mouse. When the player leaves one-handed mode, its screen goes dark first, then it slides back off screen.
## It lives in a separate small 3D world (SubViewport, Own World 3D), so the main scene's walls cannot block it, and the main scene's lights neither reach it nor make it cast shadows.
## It is only presentation on the local player's own screen, not game state (rule 5): it knows nothing of the Tab key or TabletHold, and only listens to the brain saying "come out" or "go back".

# ============================================================
# Constants: the two ends of the slide progress
# ============================================================
const TABLET_MOVE_START := 0.0  # This trip has just started: when sliding in, the on-screen tablet is still off screen; when sliding out, it is still in the lower right
const TABLET_MOVE_DONE := 1.0   # This trip has arrived at its target slot; once progress reaches this, the on-screen tablet stays at the target slot

# ============================================================
# Exported variables (@export): feel values shown in the Inspector that can be tuned directly
# ============================================================
@export var moving_time : float = 0.35  # How many seconds one slide takes; _process() uses it to work out how far to go each frame. 0.35 matches the tablet_move_seconds of the tablet in hand, so both arrive together

# ============================================================
# Member variables: state used only inside this script (a leading underscore = internal)
# All three are only "where the on-screen tablet is in the picture"; they are presentation, not game state, and neither saves nor co-op need them (rule 5)
# ============================================================
var _screen_want_show := false  # Our intent: should the on-screen tablet be out. Only set_shown() changes it; _process() reads it to decide which slot to head for
var _slide_start_transform:= Transform3D.IDENTITY  # The start of this trip: the on-screen tablet's position and angle at the moment it set off. set_shown() records it and _process() starts from it; at first it is only a placeholder
var _slide_progress := TABLET_MOVE_DONE  # How far this trip has gone. It starts as "arrived", because when the game starts the on-screen tablet is already off screen and needs no slide

# ============================================================
# Node references (@onready): child nodes used in the scene
# ============================================================
@onready var _tablet : TabletDevice = $TabletDevice  # The on-screen tablet itself: the same prefab as the one in hand; we place it every frame
@onready var _tablet_shown_place : Marker3D = $ShownSlot  # The slot in the lower right: when the intent is "come out", the on-screen tablet heads here and stops here
@onready var _tablet_hidden_place : Marker3D = $HiddenSlot  # The slot off screen: when the intent is "go back", the on-screen tablet heads here and hides here

# ============================================================
# Engine callbacks: functions Godot calls automatically at certain times (they act as entry points; GDScript has no main)
# ============================================================
## Godot calls this once after the on-screen tablet and its children are ready: at the start we put the on-screen tablet straight off screen, with no slide.
func _ready() -> void:
	_tablet.transform = _tablet_hidden_place.transform  # We put the on-screen tablet straight on the off-screen slot; from here on _process() takes care of it


## Godot calls this once per drawn frame (delta is the seconds since the last frame): we move the on-screen tablet a little from the start of this trip toward the slot that matches the intent, finishing in exactly moving_time seconds, whatever the frame rate.
## After it arrives this still runs every frame, but the progress is already "arrived", so the on-screen tablet stays at the target slot until set_shown() starts a new trip.
func _process(delta: float) -> void:
	if moving_time <= 0.0:  # If the slide time is set to 0 (or less),
		_slide_progress = TABLET_MOVE_DONE  # we set the progress straight to "arrived": the on-screen tablet jumps into place, and we also avoid dividing by 0 below
	else:  # Otherwise, we push the progress forward bit by bit over time
		# move_toward takes one small step from the current progress toward "arrived" without overshooting; the step delta / moving_time is the share of the whole trip this frame should cover
		_slide_progress = move_toward(_slide_progress,TABLET_MOVE_DONE,delta/moving_time)
	# Then we use smoothstep to turn the even progress into "slow at both ends, fast in the middle" and hand it to the placement below, so the on-screen tablet starts slowly and stops slowly, like a hand pushing it
	var eased := smoothstep(TABLET_MOVE_START,TABLET_MOVE_DONE,_slide_progress)
	var target_place: Marker3D = _tablet_shown_place if _screen_want_show else _tablet_hidden_place  # If the intent is to come out, the target is the lower right; otherwise the target is off screen
	# Finally we use interpolate_with to take a position and angle between the start and the target by eased: 0 = start, 1 = target, 0.5 = halfway; we give it to the on-screen tablet, and that is where it is in this frame's picture
	_tablet.transform = _slide_start_transform.interpolate_with(target_place.transform,eased)
	_update_screen()  # Once it is placed, we decide whether the on-screen tablet's screen should be lit or dark this frame


# ============================================================
# Functions: called by the brain, or from inside this script
# ============================================================
## The brain calls this to control the on-screen tablet: come out (shown is true) or go back (shown is false).
## It only records the new intent and prepares a new trip; it does not move the on-screen tablet. _process() is what actually moves it.
func set_shown(shown: bool) -> void:
	if shown == _screen_want_show: return  # If the shown passed in is the same as our current intent, we do nothing, so the on-screen tablet does not slide again from the start
	_screen_want_show = shown  # Otherwise, we first change our current intent to the new intent; next frame _process() picks the target slot from it
	_slide_start_transform = _tablet.transform  # Then we record where the on-screen tablet is right now as the start of this trip; if it turns round halfway, it sets off from mid-way and does not jump
	_slide_progress = TABLET_MOVE_START  # Finally we set the progress to the start; after this _process() pushes it bit by bit to TABLET_MOVE_DONE and moves the on-screen tablet


## _process() calls this every frame after placing the on-screen tablet: we decide whether its screen is lit or dark this frame.
## The screen lights only when the intent is "come out" and it has slid into the lower right and stopped; as soon as it starts sliding out, the screen goes dark, just like the tablet in hand when it is put away.
func _update_screen() -> void:
	var arrived := _slide_progress == TABLET_MOVE_DONE  # First we check whether this trip is finished: once the progress is "arrived", the on-screen tablet stays still at the target slot
	var screen_on := _screen_want_show and arrived  # Then it should be lit only if the intent is "come out" and it has arrived; while sliding in, sliding out or staying off screen, it should be dark
	_tablet.set_screen_lit(screen_on)  # Finally we hand lit or dark to the on-screen tablet itself; it sets the screen material's brightness to light_strength_percentage (0.39) or 0, and that is the brightness of the screen drawn this frame
