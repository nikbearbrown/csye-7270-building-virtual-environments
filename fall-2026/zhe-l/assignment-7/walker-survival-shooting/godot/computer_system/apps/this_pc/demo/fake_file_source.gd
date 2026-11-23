# ============================================================
# Class declaration: what it inherits from and what the whole script does
# ============================================================
extends Node  # The fake data entry point is just a plain node, placed in the demo scene
## Fake data entry point: when the This PC window runs on its own, it stands in for the backend FileService.
## It has the same get_drives(device_uid) and drives_changed(device_uid) as FileService, so the window cannot tell real from fake.
## It is used only in the demo scene; the game uses the real backend.

# ============================================================
# Constants: values defined once that never change
# ============================================================
const FAKE_LETTERS: Array[String] = ["C", "D", "E"]  # The drives the demo pretends are connected: the tablet C, a computer D, and a USB drive E, so several rows show in the window

# ============================================================
# Signals: pretend the data changed and notify the window
# ============================================================
signal drives_changed(device_uid: int)  # The same as FileService's signal; nobody emits it in the demo for now, but the window listens to it all the same

# ============================================================
# Functions: called by the This PC window
# ============================================================
## Called when the This PC window runs refresh_drives(): whichever device is asked about, we hand back the same set of fake drives.
func get_drives(_device_uid: int) -> Array[Dictionary]:
	var result: Array[Dictionary] = []  # First we prepare an empty result list
	for letter in FAKE_LETTERS:  # Then we take out each fake drive letter one by one
		result.append({"letter": letter})  # turn it into a Dictionary with "letter", the same as the backend's copy, and put it in the result; the window only uses letter
	return result  # Finally we hand it to the window, which lists these drives one row each
