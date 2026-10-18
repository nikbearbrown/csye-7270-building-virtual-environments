# Run INSIDE Blender (blender --python mcp_startup.py) with BLENDER_USER_SCRIPTS pointing at the scratch
# profile that holds blender_mcp.py. Enables the "MCP for Blender" add-on, which opens its socket
# server on localhost:9876, then logs whether the port came up.
import bpy, os, socket

LOG_PATH = os.environ.get("SEIS_MCP_LOG", "/tmp/seis_mcp_startup.log")
LOG = open(LOG_PATH, "a")


def log(*a):
    LOG.write(" ".join(str(x) for x in a) + "\n")
    LOG.flush()


def port_open():
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect(("localhost", 9876))
        return True
    except Exception:
        return False
    finally:
        s.close()


def step1():
    log("blender", bpy.app.version_string)
    log("before enable: port 9876 open =", port_open())
    try:
        bpy.ops.preferences.addon_enable(module="blender_mcp")
        log("addon_enable ok; enabled =", "blender_mcp" in bpy.context.preferences.addons)
    except Exception as e:
        log("addon_enable ERROR", repr(e))
    return None


def step2():
    log("3 s after enable: port 9876 open =", port_open())
    return None


bpy.app.timers.register(step1, first_interval=3.0)
bpy.app.timers.register(step2, first_interval=9.0)
