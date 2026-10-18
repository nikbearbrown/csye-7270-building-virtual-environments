"""finalize_standing - run INSIDE the Blender that holds the freshly assembled figure (live MCP session or headless).
Keeps the white-cove QA studio as STAGE_cove (visible) and adds the on-model brick-workshop rig as STAGE_workshop (hidden:
tick it on in the Outliner / View Layer and untick STAGE_cove to switch), adds a camera, sets Cycles + AgX, notes, then saves."""
import sys
W = "/PATH/TO/seis-bot-v004-detailed"
for p in (W + "/src", W + "/parts"):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy
import seis_lib as L, seis_stage as st

OUT = globals().get("FINAL_OUT", W + "/seis_bot_v004_standing.blend")
cove = bpy.data.collections.get("STAGE")
if cove:
    cove.name = "STAGE_cove"
L.set_collection(L.collection("SEIS_BOT"))
st.workshop(size=1.0)
ws = bpy.data.collections.get("STAGE")
if ws:
    ws.name = "STAGE_workshop"
    # keep it out of the way until chosen
    def find(lc, name):
        if lc.name == name:
            return lc
        for c in lc.children:
            r = find(c, name)
            if r:
                return r
    lc = find(bpy.context.view_layer.layer_collection, "STAGE_workshop")
    if lc:
        lc.exclude = True
body = [o for o in bpy.data.objects if o.type == "MESH" and o.parent and o.parent.type == "ARMATURE"]
st.configure(1200, 1500, 128)
st.camera_for(body, "three_q", focal=85.0, margin=1.10, aspect=0.8)
sc = bpy.context.scene
if "seis_bot_pose" in sc:
    del sc["seis_bot_pose"]          # a long-lived session may still carry the seated flag
sc["seis_bot_version"] = "v004"
sc["seis_bot_note"] = ("Interpretive model built from reference images and video frames, not a scan. Rigid FK rig, no IK, no face, "
                       "no collision. Units metres, Z up, front faces -Y. Build scripts: seis-bot-v004-detailed/src and parts.")
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("[finalize] saved", OUT, "meshes", len(body))
