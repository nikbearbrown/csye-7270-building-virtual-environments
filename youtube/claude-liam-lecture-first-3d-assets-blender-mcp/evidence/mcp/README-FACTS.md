# README-FACTS - what the MCP project's own files say (2.1.1 on 27 Sept 2026, 2.1.9 on 6 Oct 2026)

**What this is.** Facts read from the recorded files in this folder, with file and line numbers, for the film's Act IV (B29-B40) and Act V (B41-B49). Nothing here was run: no `uv`, no `uvx`, no `claude mcp`, no MCP server, and the Blender add-on was neither installed nor enabled. The files are `readme-211.md` (README at 2.1.1), `readme-219.md` (README at 2.1.9, identical to `readme.md`), `server-0927.py` and `addon-0927.py` (the code snapshot taken on 27 Sept, add-on 1.7), `server-main.py` and `addon-main.py` (a later `main` snapshot, add-on 1.8), `pypi.json` (release dates).

**Version dates (pypi.json upload times, UTC):** 2.1.0 25 Sept; **2.1.1 27 Sept 05:04**; 2.1.2 and 2.1.3 30 Sept; 2.1.5, 2.1.6, 2.1.7, 2.1.8 on 5 Oct; **2.1.9 6 Oct 15:07**. There is no 2.1.4 in the list. Python needed: `>=3.10` (pypi.json info.requires_python reads `>=3.10`).

## (a) The tool list in each version (names only)

### 2.1.1 - from the code snapshot dated 27 Sept, `server-0927.py` (every `@mcp.tool()`; the files do not record that it equals the 2.1.1 wheel byte for byte), 36 tools

The 2.1.1 README (`readme-211.md`) does not list tool names; its "Capabilities" list (lines 564-576) names only `export_scene` in passing (line 570). So this list is from the code.

| line in server-0927.py | tool | |
|---|---|---|
| 413 | `get_addon_status` |  |
| 459 | `disable_telemetry` |  |
| 488 | `get_scene_info` |  |
| 528 | `get_object_info` |  |
| 570 | `get_viewport_screenshot` |  |
| 666 | `execute_blender_code` |  |
| 707 | `describe_node_type` |  |
| 741 | `bpy_api_lookup` |  |
| 811 | `get_polyhaven_categories` |  |
| 864 | `search_polyhaven_assets` |  |
| 983 | `get_polyhaven_asset_preview` |  |
| 1024 | `download_polyhaven_asset` |  |
| 1094 | `set_texture` |  |
| 1156 | `get_polyhaven_status` |  |
| 1175 | `get_hyper3d_status` |  |
| 1200 | `get_sketchfab_status` |  |
| 1219 | `search_sketchfab_models` |  |
| 1296 | `get_sketchfab_model_preview` |  |
| 1339 | `download_sketchfab_model` |  |
| 1497 | `get_polypizza_status` |  |
| 1519 | `search_polypizza_models` |  |
| 1615 | `download_polypizza_model` |  |
| 1721 | `generate_hyper3d_model_via_text` |  |
| 1760 | `generate_hyper3d_model_via_images` |  |
| 1822 | `poll_rodin_job_status` |  |
| 1869 | `import_generated_asset` |  |
| 1902 | `get_hunyuan3d_status` |  |
| 1920 | `generate_hunyuan3d_model` |  |
| 1970 | `poll_hunyuan_job_status` |  |
| 2001 | `import_generated_asset_hunyuan` |  |
| 2044 | `get_tripo_status` |  |
| 2060 | `generate_tripo_model` |  |
| 2096 | `poll_tripo_job_status` |  |
| 2114 | `import_generated_asset_tripo` |  |
| 2133 | `export_scene` |  |
| 2172 | `record_trajectory_feedback` |  |

Of these, the three the assignment says were later removed are `get_object_info` (line 528), `get_viewport_screenshot` (line 570) and `export_scene` (line 2133). The AI-generation tools include Tripo (`generate_tripo_model`, line 2060) even though the 2.1.1 README's feature table (line 164) names only Hyper3D Rodin and Hunyuan3D.

### 2.1.9 - from the README, `readme-219.md` lines 632-643 ("nine tools")

`execute_blender_code`, `look`, `get_scene_info`, `generate_3d`, `search_assets`, `import_asset`, `get_addon_status`, `disable_telemetry`, `record_trajectory_feedback` (the README puts `search_assets` and `import_asset` on one row). The README says "The MCP adds what Python can't do on its own, as nine tools" (line 634).

### later `main` snapshot - from the code, `server-main.py`, 14 registrations

| line in server-main.py | tool | |
|---|---|---|
| 450 | `get_addon_status` | one of the README's nine |
| 499 | `disable_telemetry` | one of the README's nine |
| 606 | `get_scene_info` | one of the README's nine |
| 790 | `execute_blender_code` | one of the README's nine |
| 1482 | `record_trajectory_feedback` | one of the README's nine |
| 1561 | `look` | one of the README's nine |
| 1715 | `generate_3d` | one of the README's nine |
| 1818 | `search_assets` | one of the README's nine |
| 1888 | `import_asset` | one of the README's nine |
| 1997 | `search_mentions` | app-only |
| 2091 | `open_viewport` |  |
| 2097 | `viewport_latest` | app-only |
| 2103 | `viewport_capture` | app-only |
| 2121 | `viewport_pick` | app-only |

All nine README tools are there. `get_object_info`, `get_viewport_screenshot` and `export_scene` are not. The five extra registrations are marked `_APP_ONLY` (UI helpers for a viewport panel; `meta` visibility `app`) and are not in the README's nine. Which release this snapshot equals is not recorded in the files (it is add-on 1.8, protocol 13; the 27 Sept snapshot is add-on 1.7, protocol 11).

`get_scene_info` in 2.1.9 (`server-main.py` lines 604-632; the `fields` documentation is at lines 624-632) takes `fields`; its documented names are `location`, `size` (world bounding box), `ground` ("on ground, floating or below by"), `rotation` (degrees), `scale`, `parent`, `children`, `hidden`, `details`, `materials`, `modifiers`, `animation`, `topology`, `weights`. The default is `location, size, children, hidden`.

## (b) The sentences, commands and labels the narration speaks

| what | verbatim | where |
|---|---|---|
| socket has no authentication or encryption (2.1.1) | "the addon's socket server has no authentication or encryption," and, in the same note, "anyone who can reach that port can run Python inside Blender." | readme-211.md lines 346-347 |
| same sentence (2.1.9) | identical wording | readme-219.md lines 390-391 |
| `brew install uv` (2.1.1) | `brew install uv`, under the comment `# macOS` | readme-211.md line 50 (also 192) |
| `brew install uv` (2.1.9) | same, inside the collapsed "Manual setup" block | readme-219.md line 73 (also 234) |
| the pip warning | "Do not proceed before installing uv. Use the official installer - not `pip install uv`." | readme-211.md line 59; readme-219.md line 82 |
| `claude mcp add` line | `claude mcp add blender uvx mcp-for-blender` | readme-211.md lines 82 and 384; readme-219.md lines 105 and 428 |
| the chapter's own variant | `claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender` is NOT in either README (the README gives the env var as `DISABLE_TELEMETRY=true uvx mcp-for-blender` or a JSON `env` block) | readme-211.md lines 744-761; readme-219.md lines 808-825 |
| `install-addon` | `uvx mcp-for-blender install-addon` | readme-211.md lines 103, 510, 534; readme-219.md lines 126, 571 |
| the one-line installer (2.1.9) | `curl -LsSf https://www.mcp-for-blender.com/install.sh | sh` (Windows: `irm ... | iex`); "Already have uv? Run `uvx mcp-for-blender setup` instead." | readme-219.md lines 48, 54, 57 |
| the add-on name under Preferences | "Edit -> Preferences -> Add-ons -> enable **Interface: MCP for Blender**" | readme-211.md line 106; readme-219.md line 129 |
| what the add-on itself calls itself | `bl_info` name "MCP for Blender", category "Interface", location "View3D > Sidebar > MCP for Blender", add-on version (1, 7) | addon-0927.py lines 31-40 |
| sidebar tab | "MCP for Blender" (`bl_category`) | addon-0927.py line 5717 (README: "Find the **MCP for Blender** tab", readme-211.md line 553) |
| panel title | "MCP for Blender" (`bl_label`) | addon-0927.py line 5713 |
| the connect button, as drawn in the panel | **"Connect to MCP server"** with a play icon; once connected the panel says "Connected on port N" and the button becomes **"Disconnect"**; when not connected it says "Not connected" and shows the Port field | addon-0927.py lines 5736-5744 |
| the button as the README names it | "Start MCP Server" (Quickstart) | readme-211.md line 110; readme-219.md lines 133, 586 |
| the button as the README names it, in Usage | "Connect to Claude" | readme-211.md line 555; readme-219.md line 621 |
| the operator's own label (tooltips, F3 search) | "Connect to Claude" / "Stop the connection to Claude" | addon-0927.py lines 5868, 5889 |
| the start-on-open claim (2.1.9) | "The addon starts its server when Blender opens. To check, press `N` in the 3D viewport -> open the **MCP for Blender** tab (click **Start MCP Server** if it isn't running)." | readme-219.md line 133 |
| Safe mode (opt-in) | "By default, the AI can run any Python code in Blender. Set `BLENDER_MCP_SAFE_MODE=1` to check every script before it runs ..." | readme-211.md line 353; readme-219.md line 397; checked in the MCP server process, server-0927.py line 674 |
| telemetry | "Telemetry is **opt-in**" for content, but "a minimal anonymous usage record" is collected by default; `DISABLE_TELEMETRY=true` turns off even that | readme-211.md lines 735-746; readme-219.md lines 799-810 |

## (c) Services and downloads, and their default states

All in `addon-0927.py` `register()` (lines 5925-6092); every one is a per-scene checkbox:

| checkbox in the sidebar | property | default | line |
|---|---|---|---|
| Poly Haven (asset library, downloads) | `blendermcp_use_polyhaven` | **False** | 5945-5949 |
| Sketchfab (asset library, API key) | `blendermcp_use_sketchfab` | **False** | 6047-6051 |
| Poly Pizza (asset library, API key) | `blendermcp_use_polypizza` | **False** | 6066-6070 |
| Hyper3D Rodin (AI generation) | `blendermcp_use_hyper3d` | **False** | 5951-5955 |
| Tencent Hunyuan 3D (AI generation) | `blendermcp_use_hunyuan3d` | **False** | 5974-5978 |
| Tripo (AI generation, labelled "(Premium)") | `blendermcp_use_tripo` | **False** | 6060-6064 |

Other defaults that matter for the safety note:
- **Server auto-start: `blendermcp_auto_start_server` default `True`** (lines 5939-5943), a per-scene setting. At add-on enable and after each file load, a timer starts the server after 0.5 s (lines 113-135). `if bpy.app.background: return None` (line 81) and `start()` itself refuses with "cannot start server in background mode (blender -b)" (lines 1251-1254): **in a no-window run (`-b`) the add-on never starts the server**, so the script route does not open the socket.
- **Host `'localhost'`, port 9876** (`BlenderMCPServer.__init__`, line 1170; Port property default 9876, min 1024, lines 5926-5932). The socket is bound with `self.socket.bind((self.host, self.port))` (line 1267); the host comes from the constructor, which the panel calls with only a port (line 5878), so it is localhost unless the code is changed. The MCP-server side has `--host` / `BLENDER_HOST` and the README warns against pointing them at a remote machine (readme-211.md lines 348-350).
- **Telemetry consent: `telemetry_consent` default `False`** (addon-0927.py lines 5587-5592). README text: lines 735-741.
- **Premium upsell**: with no key, the panel draws "No API keys? Use Premium" and a "Get Premium" button (addon-0927.py lines 5458-5462). The README's "Premium" section (readme-211.md lines 166-168; readme-219.md lines 192-194) describes paid generation without your own API keys. The Hunyuan3D URL setting defaults to `http://localhost:8081` (line 6014), i.e. a local server, not a cloud one.
- **Downloads** happen only when a library box is ticked and Claude calls the matching tool; they run on Blender's main thread (readme-211.md Troubleshooting table, line 713).

## (d) Does anything in these files contradict narration.py Acts IV and V (B29-B49)?

**Contradicted or inaccurate:**

1. **B45, "Nine days later the next version removed all three, and added a tool called look."** The PyPI release list (`pypi.json`) shows the version after 2.1.1 is **2.1.2, three days later (30 Sept)**; 2.1.9 is nine days after 2.1.1 (6 Oct) but is the **seventh** release after it (2.1.2, 2.1.3, 2.1.5, 2.1.6, 2.1.7, 2.1.8, 2.1.9; there is no 2.1.4). The files do not say which release removed `get_object_info`, `get_viewport_screenshot` and `export_scene` or added `look`; they only show the 27 Sept snapshot has the three and no `look`, and the 2.1.9 README and the `main` snapshot have `look` and not the three. A true wording: "Nine days later, version two point one point nine had removed all three and added a tool called look."
2. **B31, "...a one-line installer that sets up every M C P client it finds on your machine, not only Claude Code."** The 2.1.9 README says the installer "finds the MCP clients on your machine (...), and **lets you pick which to set up**" (readme-219.md line 59). So it finds every client but does not necessarily set up every one. The assignment's own sentence ("sets up every MCP client they find") has the same overstatement. A true wording: "finds every M C P client on your machine and offers to set up each one, not only Claude Code." Whether the installer really offers a pick was not run; the `setup` code is in a module that is not in these snapshots (`run_cli`, server-main.py line 24).

**Supported, with a detail the film may want:**

3. **B29** (add-on opens a local socket; a small server launched by Claude Code relays the calls): supported. `BlenderMCPServer(host='localhost', port=9876)` (addon-0927.py 1170, 1265-1271); the server is a stdio MCP server, `mcp.run()` (server-0927.py line 2244) that Claude Code starts from the `claude mcp add ... uvx mcp-for-blender` line.
4. **B30** (steps as recorded on 27 Sept from the README): supported (readme-211.md 37-110; PyPI upload 27 Sept 05:04).
5. **B32** (uv with Homebrew on a Mac; README warns against pip): supported (readme-211.md lines 50, 59). The README's warning says to use "the official installer" while its macOS line is `brew install uv`; those are both in the README.
6. **B33** ("The readme's own line is shorter. This version adds one setting, which turns off the server's anonymous usage record."): supported: README line `claude mcp add blender uvx mcp-for-blender`; `DISABLE_TELEMETRY=true` turns off "a minimal anonymous usage record" (readme-211.md 737, 744). The `-e ... --` form is the chapter's, not the README's, as the assignment says.
7. **B34** (Edit, Preferences, Add-ons, enable "Interface: M C P for Blender"): the README says exactly that (lines 106, 129) and the add-on's `bl_info` has category "Interface" and name "MCP for Blender". In Blender 5.1.2's Add-ons list rows show **names only, with no "Category:" prefix** (see `ev_bl_prefs_addons.png`), so the row a student looks for is most likely just **"MCP for Blender"** (inference from bl_info and the screenshot; the add-on was not installed here). On-screen text could show both.
8. **B35** ("The add-on starts its server when Blender opens"): supported by the code (auto-start default True, addon-0927.py 5939-5943, 113-135); the 2.1.1 README did not say so (it told the reader to click Start). **The button the narration/README tell the student to look for ("Start MCP Server") is drawn in the panel as "Connect to MCP server"** (line 5744), and when the server has auto-started the panel instead shows "Connected on port 9876" and a "Disconnect" button. "Every service and download checkbox stays off": supported, all default False (see (c)).
9. **B36** ("runs Python that Claude writes, inside your Blender, with no guard"; no authentication or encryption): supported by readme-211.md 346-347 / 353 ("By default, the AI can run any Python code in Blender"). Omission: the README documents an **opt-in Safe mode** (`BLENDER_MCP_SAFE_MODE=1`) that screens scripts. It runs in the MCP server process (server-0927.py 674), so it does not guard the socket against a client that talks to the port directly (code reading only; not run).
10. **B37A/B37B** (keep the port on localhost; turn the add-on off in Preferences; the socket opens whenever Blender starts with the add-on enabled): supported (auto-start, lines 113-135; bind to localhost, 1170 and 1267). Extra fact: in a no-window run (`-b`) the add-on does not start the server (lines 81, 1251-1254).
11. **B38-B40** (two hours, script route, six of eight points): course rules from the assignment, not from these files. **B39A/B39B**: see the exit-code demo in `evidence/exitcode/`.
12. **B41-B44** (prompt: plan first; `get_scene_info`, `execute_blender_code`, `look`; forbids the generation tools): every tool name the assignment's prompt uses exists in 2.1.9: `get_scene_info` (server-main.py 606), `execute_blender_code` (790), `look` (1561), `generate_3d` (1715), `search_assets` (1818), `import_asset` (1888). `get_scene_info` has the `location`, `size`, `rotation` and `scale` fields (docstring, `server-main.py` lines 624-626). It also has a `ground` field ("on ground, floating or below by"), which reports the origin/floor problem of B26/B56 without Godot.
13. **B46-B49** (look yourself; hand edit; save the code; save `.blend`, `.blend1` backups): not about these files. The `.blend1` naming is checked in `evidence/assets/ls_blend.log`.
14. **B50-B52** ("The newer add-on has no export tool"): supported, `export_scene` is in the 27 Sept code (server-0927.py 2133) and not in 2.1.9's README list or the `main` snapshot.

**The README itself disagrees with the add-on in two places** worth a sentence if the film shows the panel: the README says "Start MCP Server" (and "Connect to Claude" in Usage), the panel says "Connect to MCP server"; and the README says "Make sure the MCP server is running in your terminal" (readme-211.md line 556; readme-219.md line 622) while elsewhere it says the client launches the server and "Do **not** run the `uvx` command in the terminal" (readme-211.md line 711; readme-219.md line 775).
