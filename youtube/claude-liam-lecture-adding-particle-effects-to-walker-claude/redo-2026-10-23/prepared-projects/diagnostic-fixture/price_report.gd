extends Control
@export var show_renderer := false
var previous := ""
var label:Label
func _ready():
 var background=ColorRect.new();background.color=Color("faf9f5");background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT);add_child(background)
 label=Label.new();label.position=Vector2(70,35);label.size=Vector2(1140,650);label.add_theme_color_override("font_color",Color("3d3929"));label.add_theme_font_size_override("font_size",23);label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;add_child(label);refresh()
func refresh():
 var path="res://evidence/render-results.json" if show_renderer else "res://evidence/cpu-results.json"
 var title="Real renderer measurements" if show_renderer else "Headless CPU wall measurements"
 if not FileAccess.file_exists(path):label.text=title+"\n\nPENDING — do not use this placeholder as measurement evidence";return
 var data=JSON.parse_string(FileAccess.get_file_as_string(path));var text=title+"\nSignal Garden · isolated selected version\n\n"
 if show_renderer:
  text+="Mode                         CPU ms       GPU ms      Draw calls\n"
  for row in data.summary:text+="%s  |  %.4f  |  %s  |  %.1f\n"%[row.mode,row.render_cpu_ms,str(row.render_gpu_ms) if row.render_gpu_ms!=null else "unavailable",row.draw_calls]
  text+="\n"+data.instrument+"\n"+data.renderer_context
 else:
  text+="Mode                         Median mean ms       Range ms\n"
  for row in data.summary:text+="%s  |  %.6f  |  %.6f–%.6f\n"%[row.mode,row.median_ms,row.min_ms,row.max_ms]
  text+="\n60 warm-up · 300 timed · 3 repetitions · 3 fresh processes\nFixed 60 Hz simulation · dummy renderer\nGPU simulation and drawing are not measured.\nThese values are not interactive FPS."
 text+="\n\nActual JSON results · source hashes and raw logs retained"
 label.text=text
func _process(_delta):
 var p="res://.lecture/input.json"
 if not FileAccess.file_exists(p):return
 var value=FileAccess.get_file_as_string(p)
 if value==previous:return
 previous=value;var req=JSON.parse_string(value)
 if req is Dictionary and req.get("property","")=="show_renderer":show_renderer=req.value;refresh()
