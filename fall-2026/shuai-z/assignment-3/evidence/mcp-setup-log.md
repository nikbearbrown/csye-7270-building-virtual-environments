# MCP for Blender — setup log

Who ran it: Claude Code (Opus 5.5), at my request, in a terminal session on 2026-10-12 from about 22:55 EDT. The commands and outputs below are copied from that session. The steps inside Blender's window (enable the add-on, check the panel) are mine and are recorded at the end once I have done them.

Machine: macOS (Darwin 24.1.0), Blender 5.2.2 LTS, Godot 4.7.2.stable.official.ed1daf0bf, Claude Code 2.1.296, uv 0.10.2.

## 0. Which MCP is which

Before this, I thought I had already connected Blender through a connector in the Claude app. Its manifest (`~/Library/Application Support/Claude/Claude Extensions/ant.dir.gh.blender.blender-mcp/manifest.json`) says it is **Blender Lab's** server, version 1.0.1, repository `https://projects.blender.org/lab/blender_mcp`. That is a different project from the one the assignment names (`ahujasid/mcp-for-blender`), with different tools (`get_objects_summary`, `get_screenshot_of_window_as_image`, `search_api_docs`, … and no `get_scene_info` or `look`). No Blender extension for it was found under `~/Library/Application Support/Blender/5.2/`, so I have no evidence it ever reached my Blender. I did not use it for this assignment.

Checks on the right project before installing:

| Check | Result |
| --- | --- |
| GitHub `ahujasid/mcp-for-blender` | exists, last push 2026-10-06T15:08:04Z |
| PyPI `mcp-for-blender` | latest 2.1.9; homepage `https://github.com/ahujasid/blender-mcp` (the repository's old name) |
| README manual steps (fetched 2026-10-12) | the same three steps the assignment gives: install uv, `claude mcp add blender uvx mcp-for-blender`, `uvx mcp-for-blender install-addon` |

## 1. Install uv — skipped, already installed

The assignment says `brew install uv`. uv was already on the machine from uv's official standalone installer, not from Homebrew:

```
$ which -a uv uvx
/Users/eric/.local/bin/uv
/Users/eric/.local/bin/uvx
$ brew list uv
Error: No such keg: /opt/homebrew/Cellar/uv
$ uv --version
uv 0.10.2 (a788db7e5 2026-02-10)
```

The README lists `curl -LsSf https://astral.sh/uv/install.sh | sh` as the other official installer, and warns only against `pip install uv`. I did not install a second uv through Homebrew. **Differs from the assignment:** uv from the standalone installer, not Homebrew.

## 2. Register the server with Claude Code

The assignment's command, run from `~/csye7270/course-fork`:

```
$ claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender
Invalid environment variable format: blender, environment variables should be added as: -e KEY1=value1 -e KEY2=value2
exit=1
```

**It failed.** In Claude Code 2.1.296, `-e, --env <env...>` takes more than one value, so it read `blender` as a second environment variable. `claude mcp add --help` gives the order `claude mcp add my-server -e API_KEY=xxx -- npx my-mcp-server`: the name first, then `-e`. With the name moved first:

```
$ claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender
Added stdio MCP server blender with command: uvx mcp-for-blender to local config
File modified: /Users/eric/.claude.json [project: /Users/eric/csye7270/course-fork]
exit=0

$ claude mcp get blender
blender:
  Scope: Local config (private to you in this project)
  Status: ✔ Connected
  Type: stdio
  Command: uvx
  Args: mcp-for-blender
  Environment:
    DISABLE_TELEMETRY=true
```

Notes:
- "Connected" here means Claude Code could start the server process. Blender was **not** running, so it does not show a connection to Blender.
- The scope is **local**: only Claude Code sessions started in `~/csye7270/course-fork` see this server. A session in another folder (for example `walker-rudy`) would not.
- **Differs from the assignment:** the argument order of the `claude mcp add` line.

## 3. Version of the server

```
$ uvx --from mcp-for-blender python -c "import importlib.metadata as m;print('mcp-for-blender', m.version('mcp-for-blender'))"
mcp-for-blender 2.1.9
```

(First I tried `uvx mcp-for-blender --version`. There is no such flag; the server simply started, tried Blender and stopped: `Failed to connect to Blender: [Errno 61] Connection refused`. That is expected with Blender closed.)

## 4. Install the add-on

```
$ uvx mcp-for-blender addon-paths
/Users/eric/Library/Application Support/Blender/5.2/scripts/addons (missing)

$ uvx mcp-for-blender install-addon
Installed MCP for Blender addon to /Users/eric/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py. In Blender: Preferences → Add-ons → disable then enable 'Interface: MCP for Blender', or restart Blender, then click Start MCP Server.
exit=0
```

Installed file: `blender_mcp.py`, 270,889 bytes, SHA-256 `eb0facf69781a30e69792532087d8d41c6a14fcd323353250abe7988ee297fa5`. Its `bl_info` version is `(1, 8)`. That is the add-on's own number, separate from the server package's 2.1.9.

## 5. What the installed add-on does by default (read from its code)

| Setting | Default | Where in `blender_mcp.py` |
| --- | --- | --- |
| Socket host | `localhost` | `BlenderMCPServer.__init__(self, host='localhost', port=9876)`, line 1184 |
| Port | 9876 | `blendermcp_port`, line 6216 |
| Auto-start server when Blender loads | **on** | `blendermcp_auto_start_server`, line 6229 |
| Poly Haven, Hyper3D, Hunyuan3D, Sketchfab, Tripo, Poly Pizza | off | lines 6235–6356 |
| Telemetry content consent | off | line 5723 |
| Panel button label | "Connect to MCP server" | line 5880 (its operator is labelled "Connect to Claude", line 6007) |

Auto-start is on, so the socket opens every time Blender starts with the add-on enabled. That is why the add-on should be disabled in Preferences when I am not working on this assignment. The add-on also has "Premium" and API-key panels; I leave them alone.

The README also offers `BLENDER_MCP_SAFE_MODE=1`, which checks each script before it runs. The chapter does not use it, and I have not turned it on.

## 6. Steps in Blender (mine)

- I enabled **Interface: MCP for Blender** in Edit → Preferences → Add-ons.
- In the 3D viewport's sidebar (N), the **MCP for Blender** tab shows "Connected on port 9876" with a Disconnect button, and "Addon 1.8 · up to date": [evidence/mcp-panel-connected.png](mcp-panel-connected.png).
- The checkboxes for Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin and Tencent Hunyuan 3D are all off. The panel shows no Tripo checkbox.
- I turned the Blender Lab connector off by hand in the Claude app, so only this server's tools are offered to Claude.
- A new Claude Code session in `~/csye7270/course-fork`, started at 23:08 EDT, called `get_addon_status` successfully at 23:08:58 EDT. Setup took about 15 minutes, from 22:55 to 23:08.
- On 2026-10-13 at 18:09 EDT, `get_scene_info` failed with `Could not connect to Blender. Make sure the Blender addon is running.` because Blender was closed; after I opened it, the same call worked at 18:10 EDT.

## 7. Check from Claude Code — 2026-10-13

Claude Code called `get_addon_status` (read-only) in this session. Excerpt of the result:

```
"up_to_date": true,
"protocol_version": 13, "expected_protocol_version": 13,
"addon_version": [1, 8],
"blender_version": "5.2.2 LTS",
"libraries": {"polyhaven": "off", "sketchfab": "off", "polypizza": "off"},
"generators": {"tripo": "off (Premium only)", "hunyuan3d": "off", "hyper3d": "off"},
"telemetry_consent": false
```

This shows that the server reached my running Blender, that the add-on and server agree on the protocol, and that every library and generator is off. It does not show that `DISABLE_TELEMETRY=true` stops the anonymous usage record: `telemetry_consent: false` is the separate opt-in for content, and I have no network check of what the server sends.
