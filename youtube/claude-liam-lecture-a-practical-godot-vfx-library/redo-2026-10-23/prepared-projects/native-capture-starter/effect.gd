@tool
extends Node3D
## Preview looping is explicitly labeled. Runtime spawns use play() and bounded disposal.
@export var preview_loop := true
@export var preview_interval := 3.5
@export var solo_layer := ""
@export var smoke_enabled := true
@export var auto_free := false
var phase := 999.0
var active := false
var triggered: Array[String] = []
func play():
 phase=0.0;active=true;triggered.clear()
func stop():
 active=false;preview_loop=false
 for child in get_children():
  if child is GPUParticles3D:child.emitting=false
func _process(delta):
 if not is_visible_in_tree():return
 if preview_loop and phase>=preview_interval:play()
 if not active:return
 phase+=delta
 var finish_time:=0.0
 var sub_tail:=0.0
 for child in get_children():
  if child is GPUParticles3D:
   child.visible=(solo_layer=="" or solo_layer==child.name) and (smoke_enabled or child.name!="Smoke") and not child.get_meta("disabled",false)
   if child.get_meta("disabled",false):child.emitting=false;continue
   if child.get_meta("sub_emitter_only",false):
    child.emitting=false;sub_tail=maxf(sub_tail,child.lifetime);continue
   var delay=float(child.get_meta("delay",0.0));var stop_at=float(child.get_meta("emit_until",4.0))
   finish_time=maxf(finish_time,delay+child.lifetime if child.one_shot else stop_at+child.lifetime)
   if phase>=delay and not str(child.name) in triggered:
    if child.emitting:child.restart()
    else:child.emitting=true
    triggered.append(str(child.name))
   if not child.one_shot and phase>=stop_at:child.emitting=false
  elif child is OmniLight3D:child.light_energy=maxf(0.0,1.0-absf(phase-1.5)*4.0)*2.5
 if auto_free and phase>finish_time+sub_tail+.15:queue_free()
