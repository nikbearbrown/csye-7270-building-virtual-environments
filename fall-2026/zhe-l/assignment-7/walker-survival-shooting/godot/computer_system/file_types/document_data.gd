# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
class_name DocumentData  # We name it DocumentData, meaning "the definition of one kind of document"
extends FileData  # We extend FileData: the ID, name, icon and storage size are already there, so here we only write the columns that only documents have
## The definition of one kind of document (text, photo, etc.) in the tablet system, matching one row of the "Documents" sheet in my item ID spreadsheet (not in this repo).
## A document is not software and cannot run by itself; it is handed to the software named in open_with to be opened.

# ============================================================
# Exported variables (@export): definition data shown in the Inspector and saved into the .tres
# ============================================================
@export var document_type: StringName = &""  # Document type, matching the spreadsheet's "Document type" column; it must be a spelling registered in the "Document types" sheet
@export var open_with: StringName = &""  # Which software opens it, matching the spreadsheet's "Open with" column; it holds the software's id, and later, when a document is double-clicked, we use it to find that software
@export_multiline var content: String = ""  # What is written in the document, matching the spreadsheet's "Content" column; later the software that opens the document shows it
