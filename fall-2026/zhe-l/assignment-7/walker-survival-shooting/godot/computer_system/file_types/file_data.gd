# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name FileData  # We name it FileData; the desktop, This PC and cut/paste only know this type, so software and documents can both be laid out and moved around as "files"
extends Resource  # We extend Resource, so the definition of one kind of file can be saved as a .tres file and filled in in the Inspector
## The "definition" of one kind of file in the tablet system: every file of the same kind (for example, every Notepad) shares this one piece of data (code rule 2).
## Only the columns that both the Software sheet and the Documents sheet have go here; columns only software has are in SoftwareData, columns only documents have are in DocumentData.
## Which drive and which folder one particular file sits in belongs to the "instance"; it is not written here but kept by the backend.
## The values follow the "Software" and "Documents" sheets of my item ID spreadsheet (not in this repo) (code rule 1a).

# ============================================================
# Exported variables (@export): definition data shown in the Inspector and saved into the .tres
# ============================================================
@export var id: StringName = &""  # The unique ID of this kind of file, matching the spreadsheet's Software ID / Document ID; later every file instance uses it to point back to which kind of file it is
@export var display_name: String = ""  # The name shown on screen, matching the spreadsheet's Software name / Document name; it is what is written under the desktop icon
@export var icon: Texture2D  # The icon image; the spreadsheet has no such column. When it is empty, the later icon scene will show a placeholder colour block
@export var storage_size: float = 0.0  # How much storage it takes, matching the spreadsheet's Storage size (unit [TBD]); later we use it to work out how much space is left on drive C and drive D
