# Does a Blender-only shader node cross into glTF? Does a light cross by default? (Blender 5.1.2 bundled exporter)
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python probe_nodes_lights.py
import bpy, os, json, struct
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "out", "probe"); os.makedirs(out, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.ops.mesh.primitive_cube_add(size=1.0)
cube = bpy.context.active_object
mat = bpy.data.materials.new("ProcMetal"); mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Metallic"].default_value = 0.8
noise = nt.nodes.new("ShaderNodeTexNoise")            # a Blender-only procedural shader node
nt.links.new(noise.outputs["Color"], bsdf.inputs["Base Color"])
cube.data.materials.append(mat)
bpy.ops.object.light_add(type='POINT', location=(2, 2, 3))
def jglb(path):
    d = open(path, "rb").read()
    n = struct.unpack("<I", d[12:16])[0]
    return json.loads(d[20:20 + n])
for lights in (False, True):
    p = os.path.join(out, f"probe_lights_{'on' if lights else 'off'}.glb")
    bpy.ops.export_scene.gltf(filepath=p, export_format='GLB', export_yup=True, export_materials='EXPORT', export_lights=lights)
    j = jglb(p)
    m = j["materials"][0]
    print(f"export_lights={lights}: materials[0]={json.dumps(m)}")
    print(f"export_lights={lights}: extensionsUsed={j.get('extensionsUsed')}  textures={j.get('textures')}  images={j.get('images')}  nodes={[n['name'] for n in j['nodes']]}")
print("PROBE_DONE")
