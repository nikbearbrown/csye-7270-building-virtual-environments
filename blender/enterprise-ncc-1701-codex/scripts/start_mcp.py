"""Start the existing MCP for Blender add-on for this isolated build session."""
import bpy, importlib.util, sys
source = '/Users/bear/Downloads/seis-course-publish/youtube/claude-liam-lecture-first-3d-assets-blender-mcp/evidence/mcp/addon-0927.py'
spec = importlib.util.spec_from_file_location('enterprise_blender_mcp', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
module.register()
def start():
    if not hasattr(bpy.types, 'blendermcp_server'):
        bpy.types.blendermcp_server = module.BlenderMCPServer(host='127.0.0.1', port=9876)
        bpy.types.blendermcp_server.start()
    print('ENTERPRISE MCP READY', bpy.app.version_string, flush=True)
    return None
bpy.app.timers.register(start, first_interval=2)
