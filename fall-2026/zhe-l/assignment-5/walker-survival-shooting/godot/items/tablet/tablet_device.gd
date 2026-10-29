# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name TabletDevice  # Global class name: a tablet device (every character carries its own)
extends Node3D  # Extends Node3D: has a position and rotation and can be attached to a character
## Tablet device: the root script of tablet_device.tscn.
## Every character instances its own tablet, so every tablet has its own Screen node (there is no single global tablet).
## Presentation only: it neither stores nor changes the tablet state (the state is Humanoid's _tablet_hold, rule 5).

# ============================================================
# Node references (@onready): child nodes used in the scene
# ============================================================
# @onready: assigned after the node enters the scene tree and its children are ready
@onready var _screen: MeshInstance3D = $Screen  # Screen: a thin quad (QuadMesh) 1 mm in front of the model's screen; its material is swapped separately later


# ============================================================
# Feature functions: public functions for outside callers
# ============================================================
## Returns this tablet's screen node. In A5, changing the screen's material or parameters starts from here.
## Note: the material on Screen is a resource inside the prefab, so by default every tablet shares the same one;
## to give each tablet's screen its own value, A5 needs another approach (written into CHANGE-BRIEF), not edits to this shared material.
func get_screen() -> MeshInstance3D:
	return _screen
