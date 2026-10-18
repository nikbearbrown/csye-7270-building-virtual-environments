
import sys, os
W="/PATH/TO/seis-bot-v004-detailed"
sys.path[:0]=[W+"/src", W+"/parts"]
import bpy, seis_lib as L, seis_stage as st, _proxy
L.clear_scene(); L.set_collection("T")
objs=_proxy.build()
for o in objs: L.set_material(o,"teal")
st.workshop()
st.set_clay(False)
st.camera_for(objs,"three_q",focal=85,margin=1.1,aspect=0.8,fstop=2.8)
st.render(sys.argv[-1]+"/workshop.png",800,1000,48)
