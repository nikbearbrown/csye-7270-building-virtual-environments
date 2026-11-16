#!/bin/zsh
# E1 (source_color), E2 (the shader clock in the offline harness), E10 (shader TIME against the script clock, real time). Logs: ../logs/e1-*.txt, e2-*.txt, e10-*.txt
G=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot
S=$G/../_godot-shaders-series; L=$G/evidence/planning-checks/logs; C=$G/evidence/planning-checks/check-shaders
{
for rend in forward_plus gl_compatibility; do for up in 0 1; do
  echo "== $rend  use_plain=$up  (0 = the source_color uniform, 1 = the same numbers without the hint)"
  $S/lab/check_shader.sh $C/e1-source-color.gdshader --kind quad3d --set use_plain=$up --probe 0.5,0.5 --renderer $rend | python3 -c "
import sys,json
for l in sys.stdin:
    if l.startswith('RESULT'):
        j=json.loads(l[7:]); print(j['renderer'], 'pixel bytes', [round(x*255) for x in j['probes'][0]['rgba'][:3]], ' typed 0.10, 0.45, 0.70')"
done; done
} > $L/e1-source-color.txt 2>&1
{
echo "E2: ALBEDO = vec3(TIME * 0.2), offline harness (capture_shader.sh), probes at frames 0, 1, 15, 30, 59; TIME decoded from the sRGB pixel; expected frame f: (f + 1) / 30"
$S/lab/capture_shader.sh --shader $C/e2-time-clock.gdshader --kind quad3d --length 2.0 --size 640x360 --name e2 --dest /private/tmp/claude-501/water-scratch --png 1 --probe-at 0:0.5,0.5 --probe-at 0.0334:0.5,0.5 --probe-at 0.5:0.5,0.5 --probe-at 1.0:0.5,0.5 --probe-at 1.9667:0.5,0.5 | python3 -c "
import sys,json
def lin(p): return p/12.92 if p<=0.04045 else ((p+0.055)/1.055)**2.4
for l in sys.stdin:
    if l.startswith('RESULT'):
        j=json.loads(l[7:])
        for p in j['probes']:
            f=round(p['t']*30)
            print('frame %2d  TIME read %.3f  (expected %.3f)' % (f, lin(p['rgba'][0])/0.2, (f+1)/30))"
} > $L/e2-time-clock.txt 2>&1
LOCK=/private/tmp/claude-501/shaderlab.lock
for i in $(seq 1 3600); do mkdir $LOCK 2>/dev/null && break; sleep 0.5; done
{
echo "E10: real-time runs (window kept on top), Forward+: script clock Time.get_ticks_msec() / 1000 minus the shader's TIME (mod 4 s), 90 frames each"
for i in 1 2 3; do godot --path $G/water-project --script $G/evidence/planning-checks/scripts/e10_clock.gd 2>&1 | grep "RESULT E10"; done
} > $L/e10-clock.txt 2>&1
rmdir $LOCK
