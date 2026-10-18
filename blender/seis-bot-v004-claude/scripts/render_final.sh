#!/bin/bash
# render_final.sh : the big final renders, two chains (standing, seated), each strictly sequential (memory: ~7 GB per Blender).
W=/PATH/TO/seis-bot-v004-detailed
S=/PATH/TO/scratch/final
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT=$W/renders/final; mkdir -p $OUT
( cd $S
  $B -b --factory-startup standing.blend --python $W/src/render_gallery.py -- --out $OUT --set full --only front,three_q --w 2000 --h 2500 --samples 96 --prefix standing_workshop_ --stage workshop --fstop 4 > $W/logs/final_A1.log 2>&1
  $B -b --factory-startup standing.blend --python $W/src/render_gallery.py -- --out $OUT --set full --only left,back,right,top --w 1600 --h 2000 --samples 64 --prefix standing_studio_ > $W/logs/final_A2.log 2>&1
  $B -b --factory-startup standing.blend --python $W/src/render_gallery.py -- --out $OUT --set close --cw 1500 --ch 2000 --samples 96 --prefix standing_closeup_ --stage workshop --fstop 4 > $W/logs/final_A3.log 2>&1
  echo A_DONE > $W/logs/final_A.done ) &
( cd $S
  $B -b --factory-startup seated.blend --python $W/src/render_gallery.py -- --out $OUT --set full --only three_q,front,left --w 1800 --h 2250 --samples 80 --prefix seated_workshop_ --stage workshop --fstop 4 > $W/logs/final_B1.log 2>&1
  echo B_DONE > $W/logs/final_B.done ) &
wait
