# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name SoftwareData  # We name it SoftwareData, meaning "the definition of one kind of software"
extends FileData  # We extend FileData: the ID, name, icon and storage size are already there, so here we only write the columns that only software has
## The definition of one kind of software in the tablet system, matching one row of the "Software" sheet in my item ID spreadsheet (not in this repo).
## Every piece of software can be used on both the tablet and the computer. CPU, GPU and memory will later decide whether this software can be opened (a query point, code rule 3).

# ============================================================
# Exported variables (@export): definition data shown in the Inspector and saved into the .tres
# ============================================================
@export var category: StringName = &""  # Software category, matching the spreadsheet's "Software category" column; it must be a spelling registered in the "Software categories" sheet
@export_multiline var function_description: String = ""  # What this software does, matching the spreadsheet's "Function" column; the Inspector gives it a multi-line text box
@export var cpu: float = 0.0  # How much CPU power it needs to open (unit [TBD]); later, before opening the software, we compare it with the tablet's available power
@export var gpu: float = 0.0  # How much GPU power it needs to open (unit [TBD]); used the same way as cpu
@export var memory: float = 0.0  # How much memory it takes when open (unit [TBD]); later, when several programs are open at once, we add them up and compare with the memory limit
