# ============================================================
# About: exports the main character and its tablet clips from my Blender working copy to a .glb for Godot (A7, step 5)
# ============================================================
# Run (headless, nothing is saved back into the .blend):
#   blender -b <path>/xz_anim.blend --python tools/blender/export_main_character.py -- <output.glb>
# What it does:
#   1. Builds a one-frame action "tablet_hold_hip" from frame 0 of "tablet_raise_one_hand" (the put-away hold pose).
#   2. Puts the three clips the game uses on NLA tracks named after them, so the exporter writes exactly these three animations:
#      tablet_hold_hip, tablet_raise_one_hand (frames 0-20), tablet_hold_one_hand (one frame).
#   3. Exports only the rig and the four skinned meshes (not the reference tablet model), deform bones only (the "tablet" bone
#      is a deform bone, so it is kept), with every frame sampled so the IK and constraints are baked into the bone tracks.
import sys
import bpy

# ============================================================
# Constants: names in the .blend and the clips to export
# ============================================================
RIG_NAME = "rig"  # The Auto-Rig Pro armature object
CLIPS = ["tablet_hold_hip", "tablet_raise_one_hand", "tablet_hold_one_hand"]  # The animations the game's state machine plays
RAISE = "tablet_raise_one_hand"  # The committing clip; frame 0 of it is the put-away pose
HIP = "tablet_hold_hip"  # The put-away hold pose we build here
REFERENCE_TABLET = "PROP_Tablet"  # The game tablet imported only as a reference for posing; never exported


## Reads every channel of an action at one frame (Blender 5 slotted actions: the curves live in the first layer's channel bag).
def channel_values(action, frame):
    bag = action.layers[0].strips[0].channelbags[0]
    return [(fc.data_path, fc.array_index, fc.evaluate(frame)) for fc in bag.fcurves]


## Builds the one-frame put-away pose as its own action, from frame 0 of the raise.
def build_hip_action(rig):
    old = bpy.data.actions.get(HIP)
    if old:
        bpy.data.actions.remove(old)  # If an older copy exists we start clean
    values = channel_values(bpy.data.actions[RAISE], 0)  # First we read frame 0 of the raise: hand down, tablet on the hip
    action = bpy.data.actions.new(HIP)
    rig.animation_data.action = action  # The rig records keys into the new action
    for path, index, value in values:
        owner_path, prop = path.rsplit(".", 1)
        owner = rig.path_resolve(owner_path)
        current = getattr(owner, prop)
        if hasattr(current, "__len__"):
            current[index] = value  # Array properties (location, rotation): we set the one component
            rig.keyframe_insert(path, index=index, frame=0)
        else:
            setattr(owner, prop, value)  # Single values (a constraint's influence): we set it directly
            rig.keyframe_insert(path, frame=0)
    rig.animation_data.action = None
    return action


## Puts each clip on its own NLA track, named after the clip; the exporter turns each track into one animation of that name.
def build_nla(rig):
    ad = rig.animation_data
    for track in list(ad.nla_tracks):
        ad.nla_tracks.remove(track)  # We remove any old tracks so only our three clips are written
    ad.action = None
    for name in CLIPS:
        action = bpy.data.actions[name]
        track = ad.nla_tracks.new()
        track.name = name
        strip = track.strips.new(name, int(action.frame_range[0]), action)
        if hasattr(strip, "action_slot") and strip.action_slot is None and len(action.slots) > 0:
            strip.action_slot = action.slots[0]  # Blender 5: the strip needs the action's slot that animates the rig


## Selects only what goes into the .glb: the rig and the meshes it deforms.
def select_export_objects(rig):
    for obj in bpy.context.view_layer.objects:
        obj.select_set(False)
    rig.select_set(True)
    for child in rig.children:
        if child.type == "MESH" and child.name != REFERENCE_TABLET:
            child.select_set(True)
    bpy.context.view_layer.objects.active = rig


## Entry point: reads the output path after "--", builds the clips, exports.
def main():
    out = sys.argv[sys.argv.index("--") + 1]
    scene = bpy.context.scene
    scene.render.fps = 30  # The brief is written at 30 fps; the .glb stores seconds, so this sets 1 frame = 1/30 s
    rig = bpy.data.objects[RIG_NAME]
    build_hip_action(rig)
    build_nla(rig)
    select_export_objects(rig)
    bpy.ops.export_scene.gltf(
        filepath=out,
        export_format="GLB",
        use_selection=True,
        use_active_scene=True,  # Only the main scene: the .blend also has a second scene (avatar_render) sharing the rig, which would export every node and clip twice
        export_animation_mode="NLA_TRACKS",
        export_def_bones=True,
        export_force_sampling=True,
        export_frame_step=1,
        export_optimize_animation_size=False,  # Keep a key on every frame 0-20 (the optimiser would merge the frames where the tablet stands still), so the keys match the phase table frame by frame
        export_image_format="JPEG",
    )
    print("EXPORTED", out)


main()
