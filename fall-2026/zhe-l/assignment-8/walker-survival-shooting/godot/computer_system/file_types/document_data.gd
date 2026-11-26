class_name DocumentData
extends FileData

@export var document_type: DocumentTypeData
@export var open_with: StringName = &""
@export_multiline var content: String = ""
@export var read_only: bool = false
