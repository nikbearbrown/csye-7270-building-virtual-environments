from pathlib import Path
import shutil
W=Path(__file__).resolve().parent
w=W/'work-5'
(w/'tests/price-render.gd').write_text('''extends SceneTree
func _initialize():call_deferred("run")
func run():
 root.size=Vector2i(1280,720);root.content_scale_size=Vector2i(1280,720)
 DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
 var game=load("res://main.tscn").instantiate();root.add_child(game);current_scene=game;await process_frame
 game.set_physics_process(false);game.set_process(false);game.audio_enabled=false;game.sound.stop_all()
 game.burst.one_shot=false;game.burst.position=Vector3(-2,.4,0)
 var rid=root.get_viewport_rid();RenderingServer.viewport_set_measure_render_time(rid,true)
 for mode in ["off","burst-loop-upper-bound","ambient","both"]:
  game.burst.visible=mode in ["burst-loop-upper-bound","both"];game.burst.emitting=game.burst.visible
  game.ambient.visible=mode in ["ambient","both"];game.ambient.emitting=game.ambient.visible
  for repeat in range(3):
   for i in range(60):await process_frame
   var cpu:Array[float]=[];var gpu:Array[float]=[];var draws:Array[float]=[]
   for i in range(300):
    await process_frame
    cpu.append(RenderingServer.viewport_get_measured_render_time_cpu(rid)+RenderingServer.get_frame_setup_time_cpu())
    gpu.append(RenderingServer.viewport_get_measured_render_time_gpu(rid))
    draws.append(RenderingServer.viewport_get_render_info(rid,RenderingServer.VIEWPORT_RENDER_INFO_TYPE_VISIBLE,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
   var c:=0.0;var g:=0.0;var d:=0.0
   for n in cpu:c+=n
   for n in gpu:g+=n
   for n in draws:d+=n
   print("RENDER,"+JSON.stringify({"mode":mode,"repeat":repeat,"warmup":60,"frames":300,"render_cpu_ms":c/300,"render_gpu_ms":g/300 if g>0 else null,"gpu_timer_available":g>0,"draw_calls":d/300,"cpu_min_ms":cpu.min(),"cpu_max_ms":cpu.max(),"window_pixels":str(root.get_texture().get_size()),"adapter":RenderingServer.get_video_adapter_name(),"renderer":RenderingServer.get_current_rendering_method(),"instrument":"RenderingServer viewport timers plus frame setup; unavailable GPU stays null; physics disabled to hold same scene"}))
 game.queue_free();await process_frame;await process_frame;quit()
''')
report='''extends Control
@export var show_renderer := false
var previous := ""
var label:Label
func _ready():
 var background=ColorRect.new();background.color=Color("faf9f5");background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT);add_child(background)
 label=Label.new();label.position=Vector2(70,55);label.size=Vector2(1140,620);label.add_theme_color_override("font_color",Color("3d3929"));label.add_theme_font_size_override("font_size",25);add_child(label);refresh()
func refresh():
 var path="res://evidence/render-results.json" if show_renderer else "res://evidence/cpu-results.json"
 var title="Real renderer measurements" if show_renderer else "Headless CPU wall measurements"
 if not FileAccess.file_exists(path):label.text=title+"\\n\\nPENDING — do not use this placeholder as measurement evidence";return
 var data=JSON.parse_string(FileAccess.get_file_as_string(path));var text=title+"\\nSignal Garden · isolated selected version\\n\\n"
 if show_renderer:
  text+="Mode                         CPU ms       GPU ms      Draw calls\\n"
  for row in data.summary:text+="%s  |  %.4f  |  %s  |  %.1f\\n"%[row.mode,row.render_cpu_ms,str(row.render_gpu_ms) if row.render_gpu_ms!=null else "unavailable",row.draw_calls]
  text+="\\n"+data.instrument+"\\n"+data.renderer_context
 else:
  text+="Mode                         Median mean ms       Range ms\\n"
  for row in data.summary:text+="%s  |  %.6f  |  %.6f–%.6f\\n"%[row.mode,row.median_ms,row.min_ms,row.max_ms]
  text+="\\n60 warm-up · 300 timed · 3 repetitions · 3 fresh processes\\nFixed 60 Hz simulation · dummy renderer\\nGPU simulation and drawing are not measured.\\nThese values are not interactive FPS."
 text+="\\n\\nActual JSON results · source hashes and raw logs retained"
 label.text=text
func _process(_delta):
 var p="res://.lecture/input.json"
 if not FileAccess.file_exists(p):return
 var value=FileAccess.get_file_as_string(p)
 if value==previous:return
 previous=value;var req=JSON.parse_string(value)
 if req is Dictionary and req.get("property","")=="show_renderer":show_renderer=req.value;refresh()
'''
(w/'price_report.gd').write_text(report)
(w/'price_report.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://price_report.gd" id="1"]
[node name="ActualMeasurementReport" type="Control"]
layout_mode=3
anchors_preset=15
anchor_right=1.0
anchor_bottom=1.0
script=ExtResource("1")
''')
(w/'evidence').mkdir(exist_ok=True);shutil.copy2(W/'film5-selected-checks/cpu-results.json',w/'evidence/cpu-results.json')
print('Signal Garden measurement and report sources prepared; renderer runs wait for unlocked session')
