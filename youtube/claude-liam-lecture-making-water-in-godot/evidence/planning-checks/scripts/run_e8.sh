#!/bin/zsh
# E8: the depth gap, top-down test (gap_scene.gd: camera 6 m above a plate at y = 0; a floor under the left half). Writes ../logs/e8-depth-gap.txt
G=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot
S=$G/../_godot-shaders-series; L=$G/evidence/planning-checks/logs
{
echo "E8: gap = scene depth + VERTEX.z along the view axis; floor height varies; probes: over the floor (0.30, 0.5), over nothing (0.70, 0.5). red = gap / 2 (m). Forward+ outputs are sRGB-coded (decoded); Compatibility writes the number directly."
for fy in -0.2 -0.5 -0.9; do for rend in forward_plus gl_compatibility; do for ub in 1 0; do
  [ "$ub" = 0 ] && [ "$rend" = forward_plus ] && continue
  W_ID=gap W_SHADER=../evidence/planning-checks/check-shaders/e8-depth-gap.gdshader G_FLOOR0=$fy G_FLOOR1=$fy CLIP_L=0.1 $S/lab/capture_shader.sh --scene $G/capture-scenes/gap_scene.gd --length 0.1 --size 1280x720 --warmup 8 --renderer $rend --set-at 0:water.use_branch=$ub --name e8 --dest /private/tmp/claude-501/water-scratch --png 1 --probe-at 0:0.3,0.5 --probe-at 0:0.7,0.5 | python3 -c "
import sys,json
def lin(p): return p/12.92 if p<=0.04045 else ((p+0.055)/1.055)**2.4
rend='$rend'
for l in sys.stdin:
    if l.startswith('RESULT'):
        j=json.loads(l[7:])
        g=[round((lin(p['rgba'][0]) if rend=='forward_plus' else p['rgba'][0])*2,3) for p in j['probes']]
        print('floor y=$fy  %-17s renderer branch in the shader: %s  gap over the floor %.3f m, over nothing %.3f m (clamped at 2)' % (rend, '$ub'=='1' and 'yes' or 'NO', g[0], g[1]))"
done; done; done
} > $L/e8-depth-gap.txt 2>&1
cat $L/e8-depth-gap.txt
