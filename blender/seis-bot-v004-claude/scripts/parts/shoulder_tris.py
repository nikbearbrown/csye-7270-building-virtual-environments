import sys, os
HERE = "/PATH/TO/seis-bot-v004-detailed"
sys.path.insert(0, HERE + "/src"); sys.path.insert(0, HERE + "/parts")
import bpy, time
import seis_lib as L, seis_stage as st
L.clear_scene(); st.studio(size=1.0)
L.set_collection(L.collection("PART_shoulder"))
import shoulder
t=time.time(); res = shoulder.build(); print("BUILDTIME", round(time.time()-t,1))
rows=[]
for ob in res:
    ob.data.calc_loop_triangles(); rows.append((len(ob.data.loop_triangles), ob.name))
rows.sort(reverse=True)
print("TOTAL", sum(r[0] for r in rows), len(rows))
for r in rows[:25]: print("TRI", r)
