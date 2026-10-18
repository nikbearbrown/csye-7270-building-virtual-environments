"""Talk to the Blender MCP add-on's socket server (localhost:9876).

The add-on speaks one JSON object per request: {"type": <command>, "params": {...}}.
This is the same wire protocol the `mcp-for-blender` stdio server forwards Claude's tool calls over;
it is used here because that stdio server is not registered in this Claude session.

    python3 mcp_client.py info                  # get_scene_info
    python3 mcp_client.py run /abs/path/x.py    # execute_code: exec() the file inside the open Blender
    python3 mcp_client.py code "print(1+1)"     # execute_code with an inline string
"""
import json
import socket
import sys


def call(cmd_type, timeout=900, **params):
    s = socket.create_connection(("localhost", 9876), timeout=timeout)
    s.sendall(json.dumps({"type": cmd_type, "params": params}).encode())
    buf = b""
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        buf += chunk
        try:
            return json.loads(buf.decode())
        except ValueError:
            continue
    s.close()
    return {"status": "error", "message": "connection closed before a full reply: " + buf[:200].decode("utf8", "replace")}


def run_code(code, timeout=900):
    return call("execute_code", timeout=timeout, code=code)


def run_file(path, timeout=900):
    # exec the file in Blender's main namespace so module-level state persists between calls
    code = "__file__ = %r\nexec(compile(open(%r).read(), %r, 'exec'), globals())\n" % (path, path, path)
    return run_code(code, timeout)


def show(r):
    if not isinstance(r, dict):
        print(r)
        return
    print("status:", r.get("status"))
    res = r.get("result", {})
    out = res.get("result") if isinstance(res, dict) else res
    if out not in (None, ""):
        print(out)
    if r.get("message"):
        print("message:", r["message"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        show(call("get_scene_info"))
    elif cmd == "run":
        show(run_file(sys.argv[2]))
    elif cmd == "code":
        show(run_code(sys.argv[2]))
    else:
        print(__doc__)
