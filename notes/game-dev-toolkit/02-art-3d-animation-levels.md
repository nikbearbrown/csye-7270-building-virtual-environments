# B. Content-creation tools: 3D, 2D art, textures, animation, level design
*Part of the game-development toolkit note: see [README.md](README.md). Research date 2026-11-03.*

Researched 2026-11-03 for CSYE 7270 (Building Virtual Environments; Godot 4; Claude Code and Codex). Area B of the game-development toolkit note.

## Executive summary

- **26 tools covered.** The best agent routes in this area are plain text or documented files plus a command line: Blender (CLI plus bpy plus an official MCP server), Aseprite (CLI plus Lua plus a public file spec), Tiled and LDtk (text or JSON maps), Inkscape (SVG plus CLI actions), Material Maker (JSON graph plus CLI export), Spine (JSON export plus CLI).
- **Official versus community.** Blender has an official MCP server from Blender Lab (GPL-3, Blender 5.1+, 26 tools) and a far more popular community one (33k stars, MIT, not affiliated). Cinema 4D ships its own MCP server inside the app (off by default, token-protected, GUI-only). Adobe offers an official "Adobe for creativity" connector for Claude, and community MCP servers for Photoshop. Everything else listed here is community MCP (small, often under 100 stars) or has no MCP.
- **Every DCC MCP server can run arbitrary code.** Blender, Maya, Houdini, GIMP, Cinema 4D and Photoshop servers expose a Python or script escape hatch. Treat them as full shell access to the machine and the open document; use a VM or a throwaway account, and keep command-line scripts (which run under `timeout` and a narrow permission rule) as the default route.
- **Licences students will trip over.** Houdini Apprentice and Cascadeur Free are non-commercial; Aseprite's source licence lets you compile it for yourself but not redistribute; Spine, Maya, 3ds Max, Photoshop, Substance, ZBrush and Cinema 4D are paid; Rokoko Vision's free tier is 30 seconds a month. Blender, Krita, GIMP, Inkscape, Tiled, LDtk, Pixelorama, Material Maker and TrenchBroom are free open source.
- **Platform traps.** 3ds Max is Windows-only (REPORTED); Cascadeur on Mac needs Apple Silicon; Substance Designer on Linux is limited (REPORTED).
- **Course default:** Blender (script-driven), Aseprite or Pixelorama, Tiled and/or LDtk, Material Maker, Inkscape/Krita/GIMP as needed. The rest are "know they exist, know their limits".

## How to read this file

- VERIFIED = I read it on an official page, vendor page, repository or the GitHub API (api.github.com) during this task, on 2026-11-03. Star counts, licence fields and "last push" dates come from api.github.com on that day. A repository README I did not open is not claimed to say anything.
- REPORTED = from a search-result snippet or a third-party page.
- UNVERIFIED = I could not confirm it; it is marked in the text.
- Prices are quoted only where I read them on the vendor page on 2026-11-03; otherwise "check current terms".
- "Last push" is the latest push to the default repository on GitHub (not necessarily a release).
- Agent-friendliness scale: High (agent can create, change and check results without a GUI), Medium (real script or MCP route but needs a running GUI, a licence, or is immature), Low (GUI only or no workable route).

---

## 1. 3D modeling, sculpting and DCC suites

### Blender
**What it is:** A free 3D suite for modeling, sculpting, rigging, animation, rendering and Geometry Nodes, with a complete Python API (bpy) that can also run as a plain Python module.
**Cost:** Free, no tiers. The licence page says what you create with Blender is your sole property, so commercial games and renders are fine (VERIFIED, https://www.blender.org/about/license/). Add-on scripts you publish must be GPL-compatible.
**Open source:** Yes. GPL (mostly v2 or later); Cycles is Apache 2.0; binaries are distributed under GPL v3 (VERIFIED, same page). `bpy` on PyPI is GPL-3.0.
**Extendable:** Python add-ons and extensions, Geometry Nodes, the bpy API, `bpy` as an importable module (PyPI version 5.2.3, Python 3.13 only), and full source.
**Agent integration:**
(a) `.blend` is a binary container (UNVERIFIED: not re-checked on a page today), so do not diff it. Keep the build as a script (`build.py`) and treat the `.blend` as an artifact. Interchange formats are in the deep-dive table below.
(b) Headless CLI: `-b`, `-P script.py`, `--python-expr`, `--python-exit-code N` (non-zero exit on a Python exception), `--factory-startup`, `--addons`, and `--` to pass your own arguments; Python auto-execution is off unless you pass `--enable-autoexec` (all VERIFIED, https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html). Render flags (`-o`, `-f`, `-a`, `-E`) were not confirmed on a page today (UNVERIFIED).
(c) bpy can do what the GUI does for data and operators. As a module it behaves like background mode, edits one `.blend` per process, ignores Ctrl-C during a render and writes no crash log (VERIFIED, https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html).
(d) MCP: official Blender Lab server, community "MCP for Blender", and others; full comparison in the deep dive.
(e) No generator is built into Blender (UNVERIFIED). The official MCP server bundles the Python API and manual for the model to search.
(f) Yes: `--python-exit-code`, scripted asserts (mesh counts, bounding boxes), headless render to PNG, and the official server's screenshot and `render_*_to_path` tools. Whether a render "looks right" stays a human check.
**Pros for agentic work:**
- The most scriptable DCC in this note: full CLI, pip-installable module, free, no licence server.
- An official MCP server exists, plus one with 33k stars, so clients like Claude Code and Codex are both covered.
- Output is plain files (glTF, OBJ, USD) that Godot can import and Git can store.
**Cons for agentic work:**
- `.blend` is not diffable; agents drift if they edit by hand-written GUI state instead of a script.
- Both big MCP servers run arbitrary Python with no sandbox; the official one says so itself.
- The API changes between major versions (Collada was removed in 5.0), so pin the Blender version in the course repo.
**Verdict:** High. A complete headless CLI plus a bpy module means an agent can build, export and check without a GUI.
**Sources:** VERIFIED https://www.blender.org/about/license/ ; VERIFIED https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html ; VERIFIED https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html ; VERIFIED https://pypi.org/pypi/bpy/json ; VERIFIED https://www.blender.org/download/releases/5-0/ ; VERIFIED https://www.blender.org/lab/mcp-server/ ; VERIFIED https://projects.blender.org/lab/blender_mcp/raw/branch/main/readme_tools.rst ; VERIFIED https://api.github.com/repos/ahujasid/blender-mcp

#### Blender deep dive A: headless recipes

```
# export one asset, fail loudly, bounded time (flags VERIFIED above; macOS binary path UNVERIFIED:
# /Applications/Blender.app/Contents/MacOS/Blender)
timeout 300 blender -b --factory-startup --python-exit-code 1 \
  assets/crate.blend -P tools/export_glb.py -- build/crate.glb

# bpy as a module in your own Python 3.13 environment
pip install bpy        # PyPI 5.2.3, GPL-3.0 (VERIFIED)
```

- Arguments run left to right, so load the file before `-P` (practitioner knowledge, UNVERIFIED).
- Inside the script, prefer `bpy.data` for creating and editing objects, and `bpy.ops` only where there is no data-level route, because operators depend on UI context (practitioner knowledge, UNVERIFIED).
- The glTF export operator is `bpy.ops.export_scene.gltf` (from memory; check the 5.2 API docs, UNVERIFIED).
- Course lessons apply directly: exit code 0 can hide errors, so also check that the output file exists and is non-empty, run a glTF validator on it, and render one frame for a human to look at.
- Whether EEVEE renders correctly in background mode on a GPU-less Linux box (CI) is UNVERIFIED; Cycles on CPU is the safe fallback.

#### Blender deep dive B: MCP servers and agent skill packs

| Server | Official? | Licence | Maturity (GitHub, read 2026-11-03) | Tools | Needs running GUI? | Key caution |
|---|---|---|---|---|---|---|
| Blender Lab `blender_mcp` (projects.blender.org/lab/blender_mcp) | Yes, Blender Lab | GPL-3 (VERIFIED LICENSE file) | Releases v1.0.0 2026-04-27, v1.0.2 2026-09-08, v1.0.3 2026-09-11; last commit 2026-09-29 (VERIFIED, Gitea API) | 26: code execution, blend-file summaries, object inspection, API and manual search, screenshots, workspace navigation, thumbnail and viewport renders | Interactive tools yes; the `_for_cli` variants open a saved `.blend` in a background Blender process (VERIFIED readme) | Requires Blender 5.1+; manual install of add-on, client and server (`.mcpb` bundle or source); runs LLM-generated code "without any guards", VM recommended (VERIFIED) |
| `ahujasid/mcp-for-blender` (formerly `blender-mcp`) | No ("Not affiliated with the Blender Foundation") | MIT | 33,190 stars; last push 2026-10-29; 62 open issues (VERIFIED API) | 9: `execute_blender_code`, `look`, `get_scene_info`, `generate_3d`, `search_assets`, `import_asset`, `get_addon_status`, `disable_telemetry`, `record_trajectory_feedback` | Yes (Blender add-on runs a socket server) | Socket server has no authentication; `BLENDER_MCP_SAFE_MODE=1` exists but is off by default; one-line installers pipe remote scripts into a shell; default telemetry is a minimal anonymous usage record, opt-out `DISABLE_TELEMETRY=true`; README says data may be used to train AI models; Blender 3.0+ (all VERIFIED) |
| `dhakalnirajan/blender-open-mcp` | No | MIT | 122 stars; last push 2026-10-27 (VERIFIED API) | Not read | Yes (add-on) | Aimed at local open-weight models via Ollama (REPORTED); README unread |
| Agent skill packs: `arjun988/blender-skills` (94 skills, 1,710 stars), `EL4CTEO/blender-skills` (688 stars), `scenario-labs/blender-plugin` (939 stars, GPL-3.0, add-on with local MCP server) | No | MIT / MIT / GPL-3.0 | pushed 2026-07-10 / 2026-10-30 / 2026-11-03 (VERIFIED API, descriptions only) | n/a | n/a | READMEs unread (UNVERIFIED quality); skills are prompts, not sandboxes |

- Port clash: a competitor's blog reports that the official add-on and the community add-on both default to port 9876 and conflict if both are installed (REPORTED, https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026 ; the author sells a competing server). The community README also advises running one MCP server instance at a time (VERIFIED).
- Anthropic and Blender: Blender's own page (dated 2026-04-28) lists Anthropic as a Corporate Patron of the Development Fund, with the money meant for core development including the Python API, and carries a notice that the membership model changed to "a singular donation" (VERIFIED, https://www.blender.org/?p=96355). A trade article says Anthropic released a Claude connector for Blender 5.1 the same week but does not say it is the Blender Lab server (VERIFIED, https://digitalproduction.com/2026/04/30/anthropic-funds-blender-ships-claude-connector/). Whether the two are the same code is UNVERIFIED.
- Recommendation for Claude Code and Codex: allow only the `_for_cli` summary tools and your own `blender -b ... -P` command by default; make `execute_blender_code` an ask-every-time permission.

#### Blender deep dive C: formats an agent can read or write

| Format | In Blender | Agent notes |
|---|---|---|
| `.blend` | Native | Binary (UNVERIFIED); inspect with the official `get_blendfile_summary_*` tools or a bpy script |
| glTF 2.0 (`.glb`, `.gltf`) | Import and export; ships with Blender (exact manual page not loaded today, UNVERIFIED) | Usual interchange format for Godot 4 (general knowledge, not checked against Godot docs, UNVERIFIED); `.gltf` is JSON text |
| FBX | Import and export; the C++ importer is the default in 5.0 (VERIFIED); legacy importer also listed | Binary |
| OBJ, PLY, STL | Listed under Importing and Exporting Files (VERIFIED) | OBJ and STL are text-capable; direction per format not stated on the listing |
| USD | Listed (VERIFIED); 5.0 notes mention NURBS curve I/O improvements | Text (`.usda`) option is UNVERIFIED |
| Alembic | Listed (VERIFIED) | Baked animation caches |
| BVH | Listed under Motion Capture (VERIFIED) | Text; the usual format for retargeting mocap |
| SVG | Import as curves or as Grease Pencil; Grease Pencil also exports SVG and PDF (VERIFIED) | |
| Collada (`.dae`) | **Removed in Blender 5.0** (VERIFIED) | Old scripts that export `.dae` will break |

GUI-only in Blender: interactive sculpting and weight painting, viewport feel, and any judgement of "does it look right".

---

### Maya
**What it is:** Autodesk's industry-standard DCC for modeling, rigging, character animation and effects.
**Cost:** Subscription. An Indie tier for small earners is reported with a US$100,000 gross-revenue cap, one licence per user, and a cap that varies by country (REPORTED, search summary of Autodesk's Indie pages; the Autodesk page itself returned HTTP 403, so check current terms). Free education access is UNVERIFIED.
**Open source:** No.
**Extendable:** Python (`maya.cmds`, OpenMaya API), MEL, C++ plug-ins; `mayapy` is a standalone interpreter (REPORTED, older Autodesk help pages).
**Agent integration:**
(a) `.ma` is Maya ASCII (text, editable) and `.mb` is binary; Autodesk prefers ASCII when using file references (REPORTED, https://www.loc.gov/preservation/digital/formats/fdd/fdd000604.shtml). GUI-only: sculpt tools, graph editor curve tweaking, viewport playblast review.
(b) `mayapy` after `maya.standalone.initialize()` equals batch mode with UI commands disabled; Autodesk says to match the Python version Maya ships (REPORTED, Autodesk 2016-2017 help, so check your version).
(c) Python covers essentially everything the GUI does.
(d) MCP, all community: `dcc-mcp/dcc-mcp-maya` (MIT, 66 stars, last push 2026-11-01, 79+ typed tools, runs inside Maya as a plug-in or headless with `mayapy -m dcc_mcp_maya`, Maya 2020+, `pip install dcc-mcp-maya`; env vars disable `execute_python`, `execute_mel` or all code-bearing tools, and the README says this "is not a sandbox"); `GimbalGoats/GG_MayaMCP` (MIT, 34 stars, push 2026-08-14, 71 typed tools over `commandPort`, raw execution off unless enabled, localhost only, Maya 2024+); `PatrickPalmer/MayaMCP` (MIT, 120 stars, last push 2025-05-12, so stale; tested on Maya 2023 and 2025, REPORTED); `chadrik/maya-mcp-server` (MIT, 42 stars, push 2026-07-15). No Autodesk MCP server found (absence UNVERIFIED).
(e) Autodesk Assistant in Maya 2027 answers workflow questions from Autodesk docs; the page does not say it runs commands (VERIFIED).
(f) Headless export plus scripted scene queries; viewport review is human.
**Pros for agentic work:**
- A real headless route (`mayapy`) and a typed-tool MCP server that supports it.
- ASCII `.ma` scenes can be diffed and reviewed.
- Mature Python API with decades of examples for models to draw on.
**Cons for agentic work:**
- Paid licence; batch use also needs a licence on the machine (UNVERIFIED how Autodesk meters it).
- Community MCP servers are small; the most-starred standalone one has not been updated since May 2025.
- Heavy installs, and no free path to a CI runner.
**Verdict:** Medium. A real headless route exists, but it is paid and the MCP ecosystem is community-only.
**Sources:** REPORTED https://www.autodesk.com/campaigns/me-indie/maya-indie (403 on fetch; terms via search snippets) ; VERIFIED https://help.autodesk.com/cloudhelp/2027/ENU/Maya-WhatsNew/files/GUID-B126B0C2-A72E-498F-B46B-56DEEFA72478.htm ; VERIFIED https://github.com/dcc-mcp/dcc-mcp-maya ; VERIFIED https://github.com/GimbalGoats/GG_MayaMCP ; VERIFIED https://api.github.com/repos/PatrickPalmer/MayaMCP ; VERIFIED https://api.github.com/search/repositories?q=maya+mcp ; REPORTED https://help.autodesk.com/cloudhelp/2017/ENU/Maya/files/GUID-83799297-C629-48A8-BCE4-061D3F275215.htm

### 3ds Max
**What it is:** Autodesk's Windows 3D modeling, animation and rendering application, strong in architectural visualization and game asset work.
**Cost:** Subscription, with an Indie tier under a US$100,000 revenue cap that varies by country (REPORTED; autodesk.com pages not readable here). Check current terms.
**Open source:** No.
**Extendable:** MAXScript, Python with `pymxs`, C++ SDK (SDK UNVERIFIED), plug-ins.
**Agent integration:**
(a) `.max` scene files are proprietary binary (UNVERIFIED). Windows only (REPORTED, Maxon's requirements page lists 3ds Max as Windows with no macOS entry).
(b) 3ds Max Batch: runs MAXScript or Python without loading the UI; needs a script file, can take a scene file (VERIFIED, Autodesk 2026 help). Dialogs behave differently under batch (REPORTED, Autodesk forum thread).
(c) `pymxs` reaches nearly the whole scene model.
(d) MCP, community only: `dcc-mcp/dcc-mcp-3dsmax` (MIT, 9 stars, last push 2026-10-29; adapter that lets agents inspect and edit scenes with verified undo; local endpoint `127.0.0.1:9765/mcp` and an env var to turn off the `execute_python` tool, REPORTED from PyPI).
(e) None known.
(f) Batch run plus script assertions; render for a human.
**Pros for agentic work:**
- Batch mode is a first-class, supported route.
- MAXScript and Python both available.
**Cons for agentic work:**
- Windows only, so it does not fit a Mac-based course or Linux CI.
- The only MCP adapter has 9 stars.
- Paid licence; no free tier.
**Verdict:** Medium. Batch scripting is real, but Windows-only and paid.
**Sources:** VERIFIED https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Batch/files/GUID-0968FF0A-5ADD-454D-B8F6-1983E76A4AF9.htm ; VERIFIED https://api.github.com/repos/loonghao/dcc-mcp-3dsmax ; REPORTED https://pypi.org/project/dcc-mcp-3dsmax/ ; REPORTED https://support.maxon.net/hc/en-us/articles/16797414314012 ; REPORTED https://forums.autodesk.com/t5/3ds-max-programming-forum/python-script-runs-different-under-3dsmaxbatch-or-3dsmax-exe/m-p/9584054

### Houdini
**What it is:** SideFX's node-based procedural 3D tool for effects, simulation, terrain and procedural level or asset generation.
**Cost:** Houdini Apprentice is free for personal non-commercial projects, with watermarked renders. Indie is a commercial licence for people earning under US$100K per year (studios limited to 3 licences). Core and FX are full commercial licences. No prices appeared on the buy page today; Education licences exist (all VERIFIED, https://www.sidefx.com/get/buy/). Check current terms.
**Open source:** No.
**Extendable:** Digital assets (HDAs), VEX, Python `hou` module, C++ HDK (HDK UNVERIFIED).
**Agent integration:**
(a) `.hip` scene format: UNVERIFIED (not checked). Node networks can be saved as digital assets.
(b) `hython` is a Python shell with `hou` imported; it loads `.hip` files from the command line. Importing `hou` checks out a Houdini Batch licence and falls back to FX; `hou.releaseLicense()` gives it back (VERIFIED, https://www.sidefx.com/docs/houdini/hom/commandline). Whether Apprentice can drive `hython` is UNVERIFIED.
(c) `hou` covers nodes, parameters, cooking and rendering.
(d) MCP, community only: `healkeiser/fxhoudinimcp` (MIT, 394 stars, last push 2026-11-01, 215 tools, Houdini 20.5+, `pip install fxhoudinimcp`, loopback HTTP plug-in, can start headless or GUI sessions; README warns the connection is effectively a shell, no authentication); `capoomgit/houdini-mcp` (MIT, 309 stars, push 2026-06-11, localhost:9876, no security section); `oculairmedia/houdini-mcp` (no licence, 85 stars, push 2026-09-28, uses `hrpyc`). No SideFX MCP found (absence UNVERIFIED).
(e) None.
(f) Cook headless, export, and check counts and bounding boxes in script.
**Pros for agentic work:**
- Procedural graphs are naturally scriptable and re-runnable; one graph, many outputs.
- Largest MCP tool surface in this note (215 tools).
**Cons for agentic work:**
- Houdini Engine plug-ins cover Unreal and Unity but not Godot, and are not allowed with Indie or Education (VERIFIED on the buy page).
- Free Apprentice cannot be used for commercial work.
- Steep learning curve for students and prompts.
**Verdict:** Medium. Strong script and headless story, but licence tiers restrict free and Godot use.
**Sources:** VERIFIED https://www.sidefx.com/get/buy/ ; VERIFIED https://www.sidefx.com/docs/houdini/hom/commandline ; VERIFIED https://github.com/healkeiser/fxhoudinimcp ; VERIFIED https://github.com/capoomgit/houdini-mcp ; VERIFIED https://api.github.com/repos/oculairmedia/houdini-mcp ; REPORTED https://www.sidefx.com/docs/houdini/news/21/engine.html

### ZBrush
**What it is:** Maxon's digital sculpting application for high-resolution organic models, with an iPad version.
**Cost:** Subscription; Maxon's page offers a 14-day trial through the Maxon app and shows no prices today (VERIFIED, https://www.maxon.net/en/zbrush). Sources disagree on whether a perpetual licence is still sold; check current terms.
**Open source:** No.
**Extendable:** ZScript (native), a Python wrapper over ZScript commands, the GoZ bridge to other apps (VERIFIED, Maxon pages), and a separate Python SDK (REPORTED).
**Agent integration:**
(a) Project files (`.zpr`, `.ztl`) are binary (UNVERIFIED). Maxon says ZBrush handles "standard 3D geometry formats" without listing them (VERIFIED); OBJ export is REPORTED.
(b) Command line: `ZBrush -batch -script <script.py> <output_dir> <file.zpr>`; return code 0 for success, 1 for errors such as no visible SubTools (VERIFIED, https://help.maxon.net/zbr/en-us/Content/html/reference-guide/zscript/zscript-python.html).
(c) Python is a wrapper that sends ZScript-style commands; Maxon says Python cannot manipulate ZBrush's internal data directly "in this version" (VERIFIED). There is no built-in Python editor.
(d) MCP, community and early: `dcc-mcp/dcc-mcp-zbrush` (MIT, 10 stars, last push 2026-11-03, described as pre-alpha: inspect meshes and subtools, manage brushes, export OBJ); `newsbubbles/zbrush-mcp` (no licence, 19 stars, last push 2025-12-31).
(e) None known.
(f) The batch script returns a code and writes files; sculpt quality is a human check.
**Pros for agentic work:**
- Batch export of SubTools is a documented, scriptable job.
- Python avoids learning ZScript syntax.
**Cons for agentic work:**
- Cannot read or edit sculpt data from Python; sculpting itself is GUI-only.
- Both MCP servers are tiny or pre-alpha.
- Paid; the free trial is time-limited.
**Verdict:** Low. Only batch export is scriptable, not the sculpting.
**Sources:** VERIFIED https://www.maxon.net/en/zbrush ; VERIFIED https://help.maxon.net/zbr/en-us/Content/html/reference-guide/zscript/zscript-python.html ; VERIFIED https://api.github.com/search/repositories?q=zbrush+mcp ; REPORTED https://www.cgchannel.com/2025/09/maxon-releases-zbrush-2026-0-and-zbrush-for-ipad-2026-0/

### Cinema 4D
**What it is:** Maxon's motion-graphics and 3D application, now sold inside the Maxon One bundle with Redshift and ZBrush.
**Cost:** Subscription (Maxon One), 14-day trial; no prices on the page today; Educational Licensing is linked but not detailed (VERIFIED, https://www.maxon.net/en/cinema-4d). Check current terms.
**Open source:** No.
**Extendable:** Python scripting and plug-ins, C++ SDK (SDK UNVERIFIED), Scene Nodes.
**Agent integration:**
(a) Project files proprietary (UNVERIFIED). The FAQ lists OBJ, FBX, Alembic, USD and glTF as supported model formats (VERIFIED). Windows and macOS only (VERIFIED).
(b) `c4dpy` is a headless Cinema 4D that can load and save files, build scenes and start renders; it needs a licence login (REPORTED, https://developers.maxon.net/docs/py/2025_2_0/manuals/manual_py_c4dpy.html).
(c) Python covers much of the GUI.
(d) MCP: **official built-in server** (off by default; start it from Preferences or the Commander). A token is required from every client. Two Python gates, "Allow exec_python Command" and "Allow Python-Bearing Operations", are both ON for new installations. Remote access is off by default and not encrypted. Every call goes to an audit log. It does nothing in Commandline, Team Render, c4dpy, Cineware or Lite (VERIFIED, https://help.maxon.net/c4d/2027/en-us/Content/html/MCP_Server_FAQ.html.md). Maxon tells users to disable third-party Cinema 4D MCP servers in the same client. Community alternatives: `ttiimmaacc/cinema4d-mcp` (MIT, 134 stars, last push 2026-03-07), `kumoproductions/mcp-cinema4d` (MIT, 28 stars, push 2026-10-23), `sdimaging/cinema4d-mcp` (MIT, 19 stars, 93 tools).
(e) The MCP server is the AI route; the client and model are yours.
(f) The assistant cannot see the screen unless rendering or viewport access is enabled (VERIFIED).
**Pros for agentic work:**
- The only DCC here with a vendor-supported MCP server and an audit log.
- Security defaults (token, remote off) are better than most.
**Cons for agentic work:**
- The official server needs the full UI, so no headless MCP.
- Both Python gates are on by default.
- Paid; hundreds of small objects can stall the server (VERIFIED).
**Verdict:** Medium. An official MCP server exists, but only inside the running GUI.
**Sources:** VERIFIED https://www.maxon.net/en/cinema-4d ; VERIFIED https://help.maxon.net/c4d/2027/en-us/Content/html/MCP_Server_FAQ.html.md ; REPORTED https://developers.maxon.net/docs/py/2025_2_0/manuals/manual_py_c4dpy.html ; VERIFIED https://api.github.com/search/repositories?q=cinema4d+mcp

### MagicaVoxel
**What it is:** A free voxel editor with a GPU path-traced renderer, popular for stylised voxel assets.
**Cost:** Free. Commercial use of what you make is reported as allowed (REPORTED, https://sourceforge.net/app/magicavoxel/ and download sites); I could not read the author's own terms (UNVERIFIED), so confirm before a commercial release.
**Open source:** No (the editor is closed freeware, UNVERIFIED; the `.vox` format is openly documented).
**Extendable:** No plug-in API found. The editor has shaders and an in-app command console (REPORTED by a community MCP README), but I found no documented scripting or CLI.
**Agent integration:**
(a) `.vox` is a documented binary RIFF-style format: header "VOX " plus version, chunks `MAIN`, `SIZE`, `XYZI` (voxel x, y, z, colour index), `RGBA` (256-entry palette), optional `PACK` (VERIFIED, https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt, doc dated 2016, version 150). Newer scene-graph chunks (version 200) are not in that document (UNVERIFIED); a community server handles 150 and 200. OBJ, PLY and VOX import/export is REPORTED. GUI-only: painting, lighting and final render.
(b) No command line (REPORTED: the `voxel-mcp` README says there is no documented CLI or RPC interface; VERIFIED that it says so).
(c) None.
(d) MCP, community: `KaanDRoid/voxel-mcp` (ISC, 5 stars, last push 2026-10-27, 107 tools; strict `.vox` reader and writer that does not need the GUI; writes only inside a workspace folder; optional Windows-only live UI automation, off by default, calibrated for 0.99.7.2); `Mahinika/magicavoxel-mcp` (MIT, 30 stars, last push 2026-01-16, README unread).
(e) None.
(f) Parse the written `.vox` back and check dimensions and palette; the render is human.
**Pros for agentic work:**
- A small, documented file format an agent can write directly.
- Workspace-confined MCP with sandboxed shader runner.
**Cons for agentic work:**
- No CLI or scripting, so no headless rendering of its path tracer.
- MCP servers are very new (single-digit stars for the strict one).
- Closed source, unclear terms.
**Verdict:** Medium. The `.vox` format is documented, so file-level generation works without the GUI.
**Sources:** VERIFIED https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt ; VERIFIED https://github.com/KaanDRoid/voxel-mcp ; VERIFIED https://api.github.com/search/repositories?q=magicavoxel+mcp ; REPORTED https://sourceforge.net/app/magicavoxel/ ; VERIFIED https://ephtracy.github.io/ (page had navigation only, no terms)

---

## 2. 2D art, pixel art and vector

### Aseprite
**What it is:** A pixel-art and sprite-animation editor with frames, tags, slices and sprite-sheet export.
**Cost:** Paid: US$19.99 minimum on itch.io (read 2026-11-03), which includes a Steam key and updates up to v1.9; a trial version is linked from aseprite.org (VERIFIED). The EULA lets you install and use it, make backups, and compile and modify the source for your own personal purpose, but not redistribute copies. It does not address commercial use of the art you make; "content belongs to its owners" (VERIFIED summary of the EULA; read the EULA yourself).
**Open source:** Source-available, not open source. GitHub shows no SPDX licence; source and official binaries are under the Aseprite EULA, with some bundled modules (laf, clip, undo) MIT (VERIFIED).
**Extendable:** Lua scripting (VERIFIED, repository README), extensions, source access under the EULA, and CLI.
**Agent integration:**
(a) `.aseprite` is a binary format with a public spec: header, per-frame chunks for palettes, layers, cels (zlib-compressed), tags, slices, tilesets (VERIFIED, https://raw.githubusercontent.com/aseprite/aseprite/main/docs/ase-file-specs.md). Agent-readable outputs: PNG, GIF, sprite sheet plus JSON metadata.
(b) `--batch`, `--script file.lua`, `--script-param name=value`, `--save-as` (with `{layer}` and `{frame}` placeholders), `--sheet`, `--data` (JSON to a file or stdout), `--list-layers`, `--list-tags`, `--list-slices` (all VERIFIED, https://www.aseprite.org/docs/cli/).
(c) Lua can do most things the GUI does (scope not fully checked).
(d) MCP, community: `letsagents/aseprite-mcp` (MIT, 0 stars, last push 2026-08-11, 76 tools, runs headless through Lua, `npm`, Node 20+); `willibrandon/pixel-mcp` (Go, MIT, 157 stars, last push 2025-10-18 so possibly stale, needs Aseprite 1.3.0+; REPORTED details); two more small Python or Node servers (REPORTED). All run Lua in Aseprite, so treat as arbitrary code.
(e) None.
(f) Export PNG and JSON headless, then compare frame counts, tag names and image hashes.
**Pros for agentic work:**
- The best CLI of any 2D art tool here, and a public file spec.
- Sprite-sheet JSON is exactly what Godot import pipelines consume.
- Actively maintained (last push 2026-11-03, 40.6k stars).
**Cons for agentic work:**
- Paid; compiling it yourself is for personal use only, so a shared class build is not allowed.
- MCP servers are small and unaudited.
- Headless runs still need the binary installed on every machine.
**Verdict:** High. CLI batch mode, Lua scripting and a public file spec.
**Sources:** VERIFIED https://www.aseprite.org/docs/cli/ ; VERIFIED https://raw.githubusercontent.com/aseprite/aseprite/main/EULA.txt ; VERIFIED https://dacap.itch.io/aseprite ; VERIFIED https://api.github.com/repos/aseprite/aseprite ; VERIFIED https://raw.githubusercontent.com/aseprite/aseprite/main/docs/ase-file-specs.md ; VERIFIED https://api.github.com/repos/letsagents/aseprite-mcp ; VERIFIED https://api.github.com/repos/willibrandon/aseprite-mcp ; REPORTED https://en.wikipedia.org/wiki/Aseprite

### Krita
**What it is:** A free painting application for concept art, illustration and animation.
**Cost:** Free. GPL-3.0 (VERIFIED, GitHub mirror of KDE/krita); commercial use of your own art is not restricted by the GPL (general principle, UNVERIFIED for Krita specifically).
**Open source:** Yes, GPL-3.0.
**Extendable:** Python plugins in `pykrita`, the Scripter console, brush engines, source access (VERIFIED, https://docs.krita.org/en/user_manual/python_scripting/introduction_to_python_scripting.html).
**Agent integration:**
(a) `.kra` is a zip-like archive (rename to `.zip` to look inside) and holds a flattened `mergedimage.png` other programs can read (VERIFIED). Export to PNG, JPEG and others.
(b) `krita file.kra --export --export-filename out.png` converts without opening the UI; `--export-sequence` exports an animation; `--template` opens a template (VERIFIED, https://docs.krita.org/en/reference_manual/linux_command_line.html). The docs do not describe a headless mode, so on a server run it under a virtual display (UNVERIFIED).
(c) The Python API runs inside a running Krita; the manual's examples all use GUI elements (VERIFIED).
(d) MCP, community: `edithatogo/krita-cli` (MIT, 9 stars, last push 2026-08-10, `pip install krita-cli` v1.0.1 released 2026-04-19, 40+ tools, plug-in serves local HTTP on port 5678, path sanitisation, rate limits, resource caps; Python 3.12+; Krita versions supported not stated); `dcc-mcp-krita` (loopback bridge that does not expose arbitrary Python, REPORTED); `krita-codex-mcp` (Windows-first, for Codex, MIT, REPORTED).
(e) None known.
(f) Export and diff images; painting quality is human.
**Pros for agentic work:**
- Free and open source, with a first-class export CLI for conversion jobs.
- One MCP server documents its security limits.
**Cons for agentic work:**
- Painting is GUI-driven; the Python API needs a running instance.
- `.kra` is not diffable.
- MCP servers are small (single-digit stars).
**Verdict:** Medium. Export CLI is solid, but drawing needs a running GUI.
**Sources:** VERIFIED https://api.github.com/repos/KDE/krita ; VERIFIED https://docs.krita.org/en/reference_manual/linux_command_line.html ; VERIFIED https://docs.krita.org/en/user_manual/python_scripting/introduction_to_python_scripting.html ; VERIFIED https://docs.krita.org/en/general_concepts/file_formats/file_kra.html ; VERIFIED https://pypi.org/project/krita-cli/ ; VERIFIED https://api.github.com/repos/edithatogo/krita-cli ; REPORTED https://pypi.org/project/dcc-mcp-krita/0.2.0/

### GIMP
**What it is:** A free image editor for photo retouching, composition and texture work.
**Cost:** Free, community-developed, released under the GPL (VERIFIED, https://www.gimp.org/about/).
**Open source:** Yes, GPL. (GitHub's API reports no SPDX value for the mirror, so I rely on the about page.)
**Extendable:** Script-Fu (Scheme), Python plug-ins through GObject Introspection in GIMP 3 (REPORTED), C plug-ins, source.
**Agent integration:**
(a) Native `.xcf` is binary (UNVERIFIED); PNG, JPEG, WebP and others are agent-readable.
(b) `-i` / `--no-interface` runs without UI; `-b` / `--batch <command>` runs commands non-interactively (repeatable; `-` reads stdin); `--batch-interpreter` picks the language, default Script-Fu; `--quit` exits afterwards; `-d` skips brushes and patterns for faster startup (VERIFIED, https://www.gimp.org/man/gimp.html). Older Python-Fu batch recipes for GIMP 2 do not work in 3 (REPORTED).
(c) Procedural database calls cover most GUI actions.
(d) MCP, community: `gimp-mcp/gimp-mcp` (GPL-3.0, 285 stars, last push 2026-11-01, 79 tools, needs GIMP 3.2+ and Python 3.11+, install by copying a plug-in and starting it from Tools > MCP, listens on localhost:9877; includes a live PNG snapshot tool; the `call_api` tool runs arbitrary Python-Fu, no sandbox, sandboxing is only on the roadmap; headless operation not documented).
(e) None built in.
(f) Batch export, then compare images; MCP snapshot tool lets the model see its own result.
**Pros for agentic work:**
- Real batch CLI with a configurable interpreter.
- The MCP server includes a visual-feedback tool, which helps self-checking.
**Cons for agentic work:**
- MCP needs a running GUI and a plug-in reinstall after each minor GIMP upgrade.
- Scripting changed sharply between GIMP 2 and 3, so much online example code is wrong.
- `call_api` is an unsandboxed code path.
**Verdict:** Medium. A batch CLI exists, but the best MCP route needs the GUI.
**Sources:** VERIFIED https://www.gimp.org/about/ ; VERIFIED https://www.gimp.org/man/gimp.html ; VERIFIED https://github.com/gimp-mcp/gimp-mcp ; VERIFIED https://api.github.com/repos/maorcc/gimp-mcp ; REPORTED https://lobehub.com/mcp/gimp-mcp-gimp-mcp-server

### Photoshop
**What it is:** Adobe's industry-standard raster editor, sold only as a Creative Cloud subscription.
**Cost:** Subscription only. Read on Adobe's plans page on 2026-11-03: Photoshop alone for individuals US$22.99 per month on the annual plan billed monthly, or US$263.88 per year billed annually; a 7-day free trial; Teams US$37.99 per month per licence (VERIFIED, https://www.adobe.com/products/photoshop/plans.html). Check current terms.
**Open source:** No.
**Extendable:** UXP plug-ins and scripts (the successor to ExtendScript), ExtendScript (legacy); a cloud Photoshop API billed per operation as part of Firefly Services (REPORTED; plan requirements UNVERIFIED).
**Agent integration:**
(a) `.psd` is a proprietary layered binary (UNVERIFIED); agents work with exports (PNG, JPEG).
(b) No true local headless mode that I could confirm; the cloud Photoshop API is the server-side route (REPORTED, https://developer.adobe.com/photoshop).
(c) UXP needs the latest Photoshop plus the UXP Developer Tool (VERIFIED, https://developer.adobe.com/photoshop/uxp/2022/guides/).
(d) MCP: **official** "Adobe for creativity" connector for Claude, announced 2026-04-28, covering Photoshop, Illustrator, Firefly, Express, Premiere, Lightroom, InDesign and Stock with 50+ tools; an Adobe account unlocks more tools and limits; the post does not say whether it is MCP or give pricing (VERIFIED, https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector). An `@adobe/mcp` npm package is claimed by one blog and is UNVERIFIED. Community: `alisaitteke/photoshop-mcp` (MIT, 796 stars, last push 2026-11-03, 118 or 128 tools depending on README section, unofficial, Photoshop running, Windows or macOS, `npx` install, default anonymous analytics, optional external prompt routing); `loonghao/photoshop-python-api-mcp-server` (MIT, 346 stars, push 2026-10-17); `mikechambers/adb-mcp` (MIT, 737 stars, push 2026-07-08; "proof of concept", "not endorsed" by Adobe, Photoshop 26.0+, Node proxy plus UXP plug-in; for After Effects and Illustrator an ExtendScript path lets the model run arbitrary scripts).
(e) Firefly generative tools (credit-based, REPORTED).
(f) Export and compare; the MCP tools have undo grouping.
**Pros for agentic work:**
- Official connector plus several large community servers.
- Rich batch and generative features for texture and concept work.
**Cons for agentic work:**
- Subscription; the free trial is 7 days.
- Needs the running desktop app and an Adobe account; no confirmed local headless mode.
- Community servers are unofficial and some collect analytics by default.
**Verdict:** Medium. Several routes exist, all tied to a paid, running app or Adobe's cloud.
**Sources:** VERIFIED https://www.adobe.com/products/photoshop/plans.html ; VERIFIED https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector ; VERIFIED https://developer.adobe.com/photoshop/uxp/2022/guides/ ; VERIFIED https://github.com/mikechambers/adb-mcp ; VERIFIED https://github.com/alisaitteke/photoshop-mcp ; VERIFIED https://api.github.com/search/repositories?q=photoshop+mcp ; REPORTED https://developer.adobe.com/photoshop

### Inkscape
**What it is:** A free vector-graphics editor whose native format is SVG.
**Cost:** Free. Licence is GPL (UNVERIFIED: inkscape.org returned HTTP 403, though it is the long-standing licence).
**Open source:** Yes (GPL, UNVERIFIED for version).
**Extendable:** Extensions (Python), the command-line "actions" system, source.
**Agent integration:**
(a) SVG is XML text and diffs well (general knowledge, UNVERIFIED on a page today). Exports PNG, PDF, EPS, PS.
(b) `--actions="a:arg;b"` runs actions, `--export-filename` and `--export-type` set output, `--batch-process` closes the GUI after the actions, `--shell` processes actions line by line, `--query-all` prints object IDs and boxes, `--action-list` lists IDs (VERIFIED for version 1.4.4, https://man.archlinux.org/man/inkscape.1).
(c) Actions cover many GUI operations.
(d) MCP, community (READMEs unread; capabilities from GitHub descriptions): `sandraschi/inkscape-mcp` (MIT, 96 stars, push 2026-10-24, headless SVG automation, 60+ operations); `aravindev/inkscape_mcp` (MIT, 91 stars, push 2026-11-02, interactive alongside the GUI or headless from the CLI); `Shriinivas/inkmcp` (AGPL-3.0, 79 stars, push 2026-01-14); `grumpydevorg/inkscape-mcps` (MIT, 57 stars, push 2025-10-22, security boundaries). The PyPI listing for the last one mentions limits on workspace, file size and timeout (REPORTED).
(e) None.
(f) Re-export to PNG and diff; validate SVG.
**Pros for agentic work:**
- Plain-text native format plus a documented headless action language.
- Four MCP servers to choose from, including headless-capable ones.
**Cons for agentic work:**
- Complex editing through actions strings is awkward for a model.
- MCP maintenance is uneven (one last pushed in 2025).
- Visual quality still a human check.
**Verdict:** High. SVG is plain text and the CLI can do the export and transform steps headless.
**Sources:** VERIFIED https://man.archlinux.org/man/inkscape.1 ; VERIFIED https://api.github.com/search/repositories?q=inkscape+mcp ; REPORTED https://lobehub.com/ru/mcp/yourusername-inkscape-mcp ; REPORTED https://pypi.org/project/iflow-mcp-grumpydevorg-inkscape-mcp/

### Pixelorama
**What it is:** A free pixel-art editor and animation tool built with the Godot engine.
**Cost:** Free. MIT licence (VERIFIED, GitHub API); commercial use of your art is fine under MIT for the program (the art itself is yours).
**Open source:** Yes, MIT. 10,947 stars; last push 2026-11-03.
**Extendable:** Community extensions (language not stated on the page I read); source is GDScript; the README says the project needs Godot 4.7.1 (VERIFIED, https://github.com/Orama-Interactive/Pixelorama).
**Agent integration:**
(a) Native `.pxo` format details UNVERIFIED. Exports PNG, animated PNG, sprite sheets, GIF and video (VERIFIED).
(b) The README says the CLI can automate bulk exports; it does not say it runs headless (VERIFIED, https://github.com/Orama-Interactive/Pixelorama). Option names UNVERIFIED (the docs host did not resolve).
(c) No scripting API documented on that page.
(d) MCP, community: `abidoo22/Pixelorama-MCP` (MIT, 40 stars, last push 2026-10-10; layers, pixel art generation, assets); `CyberIce2077/pixelorama-mcp` (MIT, 0 stars, push 2026-10-27; draws live on canvas with undo); `seiya058904/Pixelorama-Skills` (MIT, 1 star, agent skills). READMEs unread.
(e) None.
(f) Export and diff PNG; animation timing is a human check.
**Pros for agentic work:**
- Same engine as the course, so students can read and patch the source in GDScript.
- Several MCP and skill packs already exist.
**Cons for agentic work:**
- Headless support is not documented.
- MCP projects are tiny and new; no maturity signal.
- Aseprite's CLI and file spec are far more complete.
**Verdict:** Medium. A free, Godot-based editor with early MCP servers, but weaker headless support than Aseprite.
**Sources:** VERIFIED https://api.github.com/repos/Orama-Interactive/Pixelorama ; VERIFIED https://github.com/Orama-Interactive/Pixelorama ; VERIFIED https://api.github.com/search/repositories?q=pixelorama+mcp

### LibreSprite
**What it is:** A free pixel-art and animated-sprite editor forked from the last GPLv2 commit of Aseprite.
**Cost:** Free.
**Open source:** Yes, GPL-2.0 (VERIFIED, GitHub API and README).
**Extendable:** The repo lists a `SCRIPTING.md` file, so scripting exists, but its language and scope are UNVERIFIED. Source access.
**Agent integration:**
(a) File-format compatibility with `.aseprite` is not stated (UNVERIFIED); the editor reads "several file types".
(b) Batch CLI is not described on the page I read (UNVERIFIED), although it descends from Aseprite which has one.
(c) Scripting present (UNVERIFIED depth).
(d) MCP, community: `Snehil-Shah/LibreSprite-MCP` (GPL-2.0, 40 stars, last push 2026-10-22); `vchopDev/libresprite-mcp` (licence "Other", 0 stars, claims headless driving); `Lowkey333/puretty-sprites` (6 stars, "Other"). READMEs unread.
(e) None.
(f) Export PNG and compare.
**Pros for agentic work:**
- Free and GPL, so classes can install and share builds.
- Same workflow as Aseprite at no cost.
**Cons for agentic work:**
- Little verified detail on CLI and scripting.
- Newer Aseprite features (for example newer `.aseprite` chunks) may not be supported (UNVERIFIED).
- MCP servers are small.
**Verdict:** Medium. A free Aseprite alternative, but its agent surface is largely unconfirmed.
**Sources:** VERIFIED https://api.github.com/repos/LibreSprite/LibreSprite ; VERIFIED https://github.com/LibreSprite/LibreSprite ; VERIFIED https://api.github.com/search/repositories?q=libresprite+mcp

---

## 3. Textures and materials

### Substance 3D Painter
**What it is:** Adobe's 3D texture painting application for PBR materials, with baking and layered smart materials.
**Cost:** Subscription; sold through the Substance 3D Collection. In February 2025 Adobe announced individual pricing of US$59.99 per month or US$599.88 per year prepaid (REPORTED from Adobe's blog and a reseller; not read today). Check current terms.
**Open source:** No.
**Extendable:** Python and JavaScript plug-ins, QML interfaces (REPORTED, Adobe's Painter Python API docs on GitHub Pages).
**Agent integration:**
(a) `.spp` projects are binary (UNVERIFIED). Exports are image texture sets.
(b) No batch CLI that I could confirm. Painter must be launched with `--enable-remote-scripting`, then a helper `RemotePainter` posts JSON containing JavaScript or Python to a local HTTP server (default port 60041) (REPORTED, https://helpx.adobe.com/substance-3d-painter/scripting-and-development/scripts-and-plugins/remote-control-with-scripting.html). A release note lists "remote scripting is broken" as a known issue in 7.4.3; current status UNVERIFIED.
(c) The Python API covers texture sets, layers and export.
(d) MCP, community: `elliezu/SubstancePainterMCP` (MIT, 51 stars, push 2026-07-28, includes an `execute_python` tool, Painter 2021.1+); `cavi-ai/substance-mcp` (MIT, 2 stars, push 2026-11-03, Painter plus Designer plus Sampler, workspace-restricted file tools, SHA-256 receipts); `parodyband/painter-mcp` (MIT, 2 stars); `StrangeApeGames/patina` (3 stars, no licence listed, a separate headless "texturing engine for agents" rather than Painter); a paid "MCP Pro for Painter" with 179 tools on itch.io (REPORTED).
(e) None known beyond Adobe-wide features.
(f) Export textures and check size and channel counts; look is human.
**Pros for agentic work:**
- Remote scripting gives MCP servers a real API.
- Several MCP servers, some with safety receipts.
**Cons for agentic work:**
- Needs the GUI running with a flag; no headless mode confirmed.
- Subscription only.
- MCP servers are small.
**Verdict:** Medium. A documented remote API, but GUI-bound and paid.
**Sources:** REPORTED https://helpx.adobe.com/substance-3d-painter/scripting-and-development/scripts-and-plugins/remote-control-with-scripting.html ; REPORTED https://adobedocs.github.io/painter-python-api/ ; REPORTED https://blog.adobe.com/en/publish/2025/02/20/substance-3d-innovations-pricing-updates ; VERIFIED https://api.github.com/search/repositories?q=substance+painter+mcp ; REPORTED https://pypi.org/project/cavi-substance-mcp/

### Substance 3D Designer
**What it is:** Adobe's node-graph tool for authoring procedural materials, exported as Substance archives (`.sbsar`).
**Cost:** Subscription via the Substance 3D Collection (same pricing as Painter; see above). Check current terms.
**Open source:** No.
**Extendable:** Python API (`pysbs`) and command-line tools from the Substance Automation Toolkit (SAT); plug-ins.
**Agent integration:**
(a) `.sbs` graphs are XML-based (UNVERIFIED); `.sbsar` is the cooked archive. Render outputs are PNG maps.
(b) SAT command-line tools: `sbscooker` turns `.sbs` into `.sbsar`; `sbsrender` renders maps from `.sbsar` with parameters; there are also `sbsbaker`, `sbsmutator` and `sbsupdater` (REPORTED, Adobe SAT pages). An Adobe staff reply says Designer's install includes SBSBaker, SBSCooker, SBSRender and SBSUpdater, and that standalone Linux packages are only for Enterprise customers with Steam as the individual Linux route (REPORTED, Adobe community, 2024).
(c) `pysbs` edits `.sbs` graphs without the GUI; whether it ships with a Designer-only licence is UNVERIFIED.
(d) MCP: `cavi-ai/substance-mcp` covers Designer and Sampler servers (MIT, 2 stars, push 2026-11-03; metadata only).
(e) None known.
(f) Render maps headless and compare against a baseline.
**Pros for agentic work:**
- A mature cook-and-render CLI is rare in this category.
- A `.sbsar` is a parameterised material, so one file gives many variants.
**Cons for agentic work:**
- Authoring graphs still needs the GUI or `pysbs`.
- Linux support is limited for individuals.
- Godot has no native `.sbsar` loader (UNVERIFIED); you export PNG maps.
**Verdict:** Medium. Strong render CLI, but paid and graph authoring is not agent-friendly.
**Sources:** REPORTED https://helpx.adobe.com/substance-3d-sat/command-line-tools/sbscooker.html ; REPORTED https://adobedocs.github.io/substance-automation-toolkit/ ; REPORTED https://community.adobe.com/questions-50/how-to-install-substance-3d-designer-or-substance-3d-automation-toolkit-on-linux-626429 ; VERIFIED https://api.github.com/search/repositories?q=substance+painter+mcp

### Material Maker
**What it is:** A free procedural-texture and 3D-painting tool built on the Godot engine.
**Cost:** Free; downloads on itch.io, Steam and package managers (VERIFIED, README).
**Open source:** Yes, MIT (VERIFIED, API and README). 6,206 stars; last push 2026-10-25.
**Extendable:** Node-based graphs, custom nodes, source (Godot project).
**Agent integration:**
(a) `.ptex` project files are JSON text (REPORTED, https://fileinfo.com/extension/ptex ; no formal schema found). Do not confuse with Disney's Ptex format.
(b) `material_maker --export-material --target <engine> -o <output_path> <files.ptex>` exports to Blender, Godot, Unity or Unreal; wildcards accepted (VERIFIED, https://rodzill4.github.io/material-maker/doc/command_line.html). The page does not say whether this needs a display (UNVERIFIED).
(c) No scripting API, but you can generate the JSON graph.
(d) MCP, community: `graysonchalmers/Tool-MaterialMaker-MCP` (MIT, 10 stars, push 2026-10-31); `SS-360/materialpilot` (licence "Other", 9 stars, push 2026-10-16, Material Maker 1.7 and Godot 4.7); `dcc-mcp/dcc-mcp-material-maker` (MIT, 1 star, validates `.ptex` graphs and exports through the native CLI); `Tigertycoon/material-maker-mcp` (MIT, 1 star). READMEs unread.
(e) None.
(f) CLI export, then check image sizes; a human judges the look.
**Pros for agentic work:**
- Text graph files plus a CLI export to Godot, which suits Git and review.
- Free, MIT, and the same engine as the course.
**Cons for agentic work:**
- No formal `.ptex` schema, so agents guess node names and parameters.
- MCP projects are tiny.
- Headless operation is not documented.
**Verdict:** Medium. A text graph and a CLI export, but no schema and only early MCP servers.
**Sources:** VERIFIED https://api.github.com/repos/RodZill4/material-maker ; VERIFIED https://github.com/RodZill4/material-maker ; VERIFIED https://rodzill4.github.io/material-maker/doc/command_line.html ; REPORTED https://fileinfo.com/extension/ptex ; VERIFIED https://api.github.com/search/repositories?q=%22material+maker%22+mcp

### ArmorPaint
**What it is:** A 3D texture-painting tool in the Substance Painter mould, by the Armory3D author.
**Cost:** Source is free to build; "distributed binaries are paid to help with the project funding" (VERIFIED, https://github.com/armory3d/armorpaint). Check current price.
**Open source:** Yes, zlib/libpng licence (VERIFIED via the GitHub licence API; GitHub reports it as "Other"). 5.5k stars.
**Extendable:** Source access; a plug-in system exists in the app (UNVERIFIED).
**Agent integration:**
(a) Project format UNVERIFIED.
(b) Builds run through a make script; I found no documented command-line export (UNVERIFIED).
(c) A community server describes a "scripting engine" and CLI for batch exports (see below); the official docs for it were not read.
(d) MCP, community and early: `baktubak/armorpaint-mcp` (licence "Other", 3 stars, push 2026-09-09, 58 tools via a bridge plug-in in the app's embedded C dialect, no fork needed); `graysonchalmers/Tool-ArmorPaintMCP` (MIT, 1 star, push 2026-10-25, batch re-exports through the CLI and scripting engine); `gprethesh/armorpaint-mcp` (MIT, 1 star). READMEs unread.
(e) None.
(f) Export textures and check them; look is human.
**Pros for agentic work:**
- Free to build and permissive licence, so it can be extended or scripted from source.
- Cheap alternative to a Substance subscription.
**Cons for agentic work:**
- No verified CLI or scripting docs.
- All three MCP servers have 1 to 3 stars.
- Students must either build from source or buy the binary.
**Verdict:** Low. No documented agent route; only tiny, unvetted community bridges.
**Sources:** VERIFIED https://github.com/armory3d/armorpaint ; VERIFIED https://api.github.com/repos/armory3d/armorpaint/license ; VERIFIED https://api.github.com/search/repositories?q=armorpaint+mcp

---

## 4. Animation and motion capture

### Spine
**What it is:** Esoteric Software's 2D skeletal-animation editor, with runtimes for many engines including Godot.
**Cost:** Paid, by edition (the page does not say whether Essential and Professional are perpetual or subscription, only that updates carry no extra charge; Enterprise and Education are one-year licences). Prices read on the vendor page 2026-11-03: Essential US$69 (shown discounted from US$99), Professional US$379 (from US$449), Enterprise US$2,499 plus US$379 per user and required for businesses with US$500,000 or more annual revenue, Education US$850 for 10 computers. Education licences cannot be used for commercial products. A free trial exists (VERIFIED, https://esotericsoftware.com/spine-purchase). Essential lacks meshes and other advanced features. Runtime use needs an editor licence for new products (VERIFIED, same page).
**Open source:** No (editor); runtimes are under the separate Spine Runtimes License (not read).
**Extendable:** JSON import/export, CLI, runtimes in many languages, source for runtimes.
**Agent integration:**
(a) Export JSON is human-readable plain text with pretty-print on (bones, slots, constraints, skins, events, animations); a binary export is smaller and not readable (VERIFIED, https://esotericsoftware.com/spine-json-format). The `.spine` project file is a proprietary format (UNVERIFIED).
(b) `-i` input, `-o` output, `-e` export settings (or `json`/`binary` with `+pack`), `-p` to pack atlases, `-r` to import; "most CLI parameters can be used headless", but image or video export needs a windowing system and OpenGL (VERIFIED, https://esotericsoftware.com/spine-command-line-interface). Which edition's licence the CLI requires is not stated there (UNVERIFIED).
(c) No scripting API for the editor found.
(d) MCP, community: `UmutFarukDilli/spine-mcp` (MIT, 1 star, push 2026-10-25; create, edit, validate and animate Spine skeletons; metadata only).
(e) None.
(f) Export JSON and validate bones, slots and animation names in script; motion quality is human.
**Pros for agentic work:**
- Plain JSON export an agent can read and edit.
- CLI covers export, import and atlas packing for build scripts.
- The `spine-godot` runtime ships as a Godot 4 GDExtension (VERIFIED, https://esotericsoftware.com/spine-godot).
**Cons for agentic work:**
- Paid, with a revenue threshold that forces Enterprise for larger studios.
- The only MCP server has one star.
- Authoring animation is a GUI task.
**Verdict:** Medium. JSON plus a headless CLI, but paid and authoring is manual.
**Sources:** VERIFIED https://esotericsoftware.com/spine-purchase ; VERIFIED https://esotericsoftware.com/spine-command-line-interface ; VERIFIED https://esotericsoftware.com/spine-json-format ; VERIFIED https://esotericsoftware.com/spine-godot ; VERIFIED https://api.github.com/search/repositories?q=spine+skeleton+animation+mcp+esoteric

### Mixamo
**What it is:** Adobe's free web service that auto-rigs an uploaded humanoid and applies a library of motion-captured animations.
**Cost:** Free with an Adobe account (REPORTED; the Mixamo page itself would not load for me, and Adobe's FAQ returned HTTP 403). Adobe community answers say characters and animations can be used royalty-free in commercial games but you may not redistribute the raw files as a product (REPORTED, https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775 ; check Adobe's current terms).
**Open source:** No.
**Extendable:** No documented plug-in or API (UNVERIFIED that none exists).
**Agent integration:**
(a) Inputs and outputs are FBX, and DAE for some downloads (UNVERIFIED).
(b) None; it is a browser service.
(c) No public API found (UNVERIFIED).
(d) MCP: none found. A community pipeline `squall01337/mixamo-llm-mocap` (425 stars, licence "Other", push 2026-09-26) converts video to Mixamo-rig animations with a pose estimator, retargeting and Blender via MCP (metadata only); it does not drive the website.
(e) Auto-rigging and animation are service features.
(f) Check the downloaded FBX in Blender or Godot (frame count, bone names).
**Pros for agentic work:**
- Free, large animation library, and a standard humanoid skeleton.
- Downloaded FBX/animations can be post-processed by scripts.
**Cons for agentic work:**
- A human must log in and click; no documented API, and scraping the site would be against the spirit of the terms (check them).
- The terms forbid selling raw character or animation files as a package.
- Reliance on a service that can change.
**Verdict:** Low. Browser-only; an agent can post-process the downloads but cannot drive the service.
**Sources:** REPORTED https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775 ; REPORTED https://app.cinevva.com/guides/free-character-animations-rigging ; VERIFIED https://api.github.com/search/repositories?q=blender+mcp (listing of `mixamo-llm-mocap`)

### Cascadeur
**What it is:** Nekki's physics-assisted 3D keyframe animation tool for characters.
**Cost:** Plans read on the vendor page 2026-11-03: Free US$0 (full animation toolset, but export only `.casc`, 300 frames and 120 joints per scene, and non-commercial use only); Indie US$19 per month or US$8 per month billed annually (US$96 per year), adds `.fbx` and `.dae` export, for revenue under US$100k; Pro US$49 per month or US$33 per month billed annually (US$396 per year), unlimited commercial use and retargeting, with a 14-day trial (VERIFIED, https://cascadeur.com/plans).
**Open source:** No.
**Extendable:** Python 3.8 `csc` API, custom commands as `.py` files in a commands folder, node editor (VERIFIED, https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur).
**Agent integration:**
(a) `.casc` is a proprietary project (UNVERIFIED format). `.fbx`/`.dae` export needs a paid plan.
(b) The help page does not say scripts run from a command line, and does not say which plan includes Python (VERIFIED absence).
(c) The `csc` API reads and edits scenes, selection and animation tracks, imports FBX, and changes are undoable (VERIFIED).
(d) MCP, community, all small: `gprethesh/cascadeur-mcp` (MIT, 8 stars, push 2026-09-15; animation, rig inspection, keyframes, physics, visual review for Codex, Claude, Cursor); `MnxD2A6/cascadeur-mcp` (MIT, 2 stars, experimental); `muhwagwa0112/cascadeur-complete` (MIT, 2 stars, for 2026.1.2); `BrianFinch-1/cascadeur-codex-bridge` (MIT, 2 stars); `ysk424/cascadeur-mcp` (no licence). READMEs unread; they control a running instance.
(e) Built-in AI-assisted posing, physics and inbetweening tools (the plans page lists physics tools and inbetweening, VERIFIED).
(f) Inspect scene data via the API; motion quality is a human check.
**Pros for agentic work:**
- Python API exists and an agent can read rigs and keyframes.
- Five MCP bridges already target Claude and Codex.
**Cons for agentic work:**
- No documented headless or command-line mode.
- Free plan is non-commercial and cannot export FBX.
- MCP bridges are experimental; Mac needs Apple Silicon (VERIFIED).
**Verdict:** Low. In-app Python only, and no headless mode.
**Sources:** VERIFIED https://cascadeur.com/plans ; VERIFIED https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur ; VERIFIED https://api.github.com/search/repositories?q=cascadeur+mcp

### Rokoko Vision (AI markerless motion capture from video)
**What it is:** A cloud service from Rokoko that turns uploaded video into 3D animation; Rokoko's main business is mocap suits and gloves.
**Cost:** Read on Rokoko's page 2026-11-03: Starter US$0 with 30 seconds of Vision processing per month and FBX export only; Basic US$10 per month billed annually or US$12 monthly, 600 seconds per month, BVH export, custom character import and retargeting. Vision 3.0 takes uploaded video only (no webcam), and the dual-camera feature is being retired (VERIFIED, https://www.rokoko.com/products/vision).
**Open source:** No.
**Extendable:** No Vision API on the page; an SDK exists at sdk.rokoko.com in the robotics section (VERIFIED). Rokoko Studio and plug-ins are for the suit products; free-Studio claims are REPORTED.
**Agent integration:**
(a) Outputs FBX (all plans) and BVH (Basic and above) from Rokoko Studio; these open in Blender, Unreal, Unity, Cinema 4D, Maya and Houdini (VERIFIED). BVH is text and Blender can import it (VERIFIED for Blender).
(b) None.
(c) None.
(d) MCP: none found.
(e) The product is the AI.
(f) Import the FBX/BVH into Blender in a script and check frame count and bone names.
**Pros for agentic work:**
- Cheap way to get humanoid motion data into a text-friendly format (BVH) that scripts can process.
- Real-time streaming is not needed for offline batch.
**Cons for agentic work:**
- Upload and download is a web workflow with no API.
- Free tier is 30 seconds a month.
- AI mocap needs cleanup, which is a human task.
**Verdict:** Low. Web-only service with no API; the files it produces are agent-friendly.
**Sources:** VERIFIED https://www.rokoko.com/products/vision ; REPORTED https://www.toolmage.com/en/tool/rokoko/

### FreeMoCap (open-source markerless mocap option)
**What it is:** A free research-grade motion capture system, intended to be low cost and hardware agnostic.
**Cost:** Free.
**Open source:** Yes, AGPL-3.0 (VERIFIED, API and README); the maintainers say they will talk about other licences. AGPL has network-use obligations, so check before embedding it in a service. 10,661 stars; last push 2026-11-03.
**Extendable:** Source; Python package; a Python server runs on localhost:8005 behind an Electron/React GUI (VERIFIED, README).
**Agent integration:**
(a) Output formats are not listed on the README page I read; Blender, CSV and BVH output are UNVERIFIED.
(b) `pip install freemocap[cuda]` or `[cpu]`, launch with `freemocap`; Python 3.9 to 3.11 (3.11 recommended); source builds use `uv` (VERIFIED, https://github.com/freemocap/freemocap).
(c) No Python API documented on that page.
(d) MCP: none found. A manuals-for-agents repo `korpus91/tool-manuals` lists FreeMoCap manual text (metadata only).
(e) The tool is computer-vision based.
(f) Check output file contents in script.
**Pros for agentic work:**
- Free, pip-installable, and runs locally.
- Not tied to a vendor service.
**Cons for agentic work:**
- No documented headless mode or API.
- Camera calibration and capture are physical, human steps.
- AGPL.
**Verdict:** Low. Hardware setup and a GUI dominate; the post-capture files can be scripted.
**Sources:** VERIFIED https://github.com/freemocap/freemocap ; VERIFIED https://api.github.com/repos/freemocap/freemocap

---

## 5. Level and map editors

### Tiled
**What it is:** A free, flexible 2D tile-map and level editor with orthogonal, isometric and hex maps.
**Cost:** Free; asks for donations (VERIFIED, https://www.mapeditor.org/). Commercial games are fine under the open-source licence (general principle; confirm in the project's licence files).
**Open source:** Yes. The editor and plug-ins are GPL; `libtiled` and viewer tools are BSD 2-clause (VERIFIED, COPYING; GitHub API shows NOASSERTION). 13,026 stars; last push 2026-11-02.
**Extendable:** JavaScript scripting extensions, custom map and tileset formats, Python export plug-ins, C++ plug-ins (VERIFIED, https://doc.mapeditor.org/en/stable/manual/scripting/ and /export/).
**Agent integration:**
(a) Plain text: TMX (XML-based, inferred from its parsers) and JSON map format (`.tmj`); both documented on doc.mapeditor.org (VERIFIED partly). Exports JSON, Lua, CSV, Defold, GameMaker, Godot 4 `.tscn`, tBIN, tIDE and images (VERIFIED). A Godot importer for `.tmj` exists (VERIFIED).
(b) `--export-map` and `--export-tileset`; on Linux it still needs an X server, so use `xvfb-run tiled --export-map ...`. Scripts run headless with `tiled -e file.js` (no UI created; scripts can load, modify and save maps) (VERIFIED).
(c) The JavaScript API can load, edit and save maps and tilesets.
(d) MCP, community: `PengLx/TiledMCP` (no licence field, 3 stars, push 2026-07-28, 52 core tools plus up to 3 optional, TMJ/TSJ plus TMX/TSX/TX writers, preview-approve-apply writes, path sandbox, checkpoints, verified against Tiled 1.12.2, Node 20.19+ and pnpm, draft 0.0.x); `pujan1/tiled-mcp` (MIT, 0 stars, `.tmj` only, no TMX writing).
(e) None.
(f) Re-export through the CLI and diff; validate with the MCP server's checks; look and level feel are human.
**Pros for agentic work:**
- Text maps, a headless export CLI and headless scripting: an agent can both write and check maps.
- Direct Godot 4 `.tscn` export.
**Cons for agentic work:**
- Needs a virtual display on Linux for CLI export.
- Both MCP servers are very small (3 and 0 stars) and the best one has no declared licence.
- AutoMapping is not supported by the MCP server.
**Verdict:** High. Text map formats plus headless export and scripting.
**Sources:** VERIFIED https://www.mapeditor.org/ ; VERIFIED https://doc.mapeditor.org/en/stable/manual/export/ ; VERIFIED https://doc.mapeditor.org/en/stable/manual/scripting/ ; VERIFIED https://github.com/mapeditor/tiled/blob/master/COPYING ; VERIFIED https://doc.mapeditor.org/en/stable/reference/support-for-tmx-maps/ ; VERIFIED https://github.com/PengLx/TiledMCP ; VERIFIED https://api.github.com/search/repositories?q=tiled+mcp+tmx&sort=stars&per_page=5

### LDtk
**What it is:** A modern 2D level editor (Level Designer Toolkit) with entities, IntGrid layers, auto-layers and a documented JSON project format.
**Cost:** Free (MIT-licensed open source; the price statement itself is UNVERIFIED).
**Open source:** Yes, MIT (VERIFIED). 4,374 stars; last push 2026-10-23.
**Extendable:** A documented JSON format and JSON schema, a Haxe API (`ldtk-haxe-api`), and source (VERIFIED).
**Agent integration:**
(a) `.ldtk` is JSON: a `__header`, `defs` (layers, entities, tilesets, enums) and `levels`; optional separate level files; the format changes between versions, so pin one (VERIFIED, https://ldtk.io/docs/game-dev/json-overview/). "Super simple export" writes a PNG per layer and a composite per level, plus optional JSON (REPORTED). Godot 4 importers exist, e.g. `heygleeson/godot-ldtk-importer` (MIT, 265 stars, push 2026-10-12) (VERIFIED metadata).
(b) No command line or headless export found (UNVERIFIED; a search found none).
(c) No scripting API in the editor; edit the JSON directly.
(d) MCP, community: `gazure/ldtk-mcp` (Rust, MIT, 7 stars, last push 2026-10-30, 39 commits, `cargo install --git`, stdio): reads and writes `.ldtk` files directly following `JSON_SCHEMA.json` v1.5.3; tools to inspect and edit levels, IntGrid, entities, tiles and definitions, render a level to PNG, validate, preview a semantic diff, undo and save; it does not evaluate AutoLayer rules yet (VERIFIED, https://github.com/gazure/ldtk-mcp).
(e) None.
(f) Validate against the schema, diff, render the level to PNG with the MCP server, and reload in LDtk; feel is human.
**Pros for agentic work:**
- Plain JSON with a published schema: the best match in this note for "agent edits the file, git diff reviews it".
- The MCP server works on the file, not on a running GUI.
**Cons for agentic work:**
- No CLI or headless export.
- Format version drift; AutoLayer tiles appear only when LDtk reopens the project (VERIFIED, README).
- The only MCP server has 7 stars.
**Verdict:** High. A JSON file with a schema is the easiest thing for an agent to edit and check.
**Sources:** VERIFIED https://api.github.com/repos/deepnight/ldtk ; VERIFIED https://github.com/deepnight/ldtk ; VERIFIED https://ldtk.io/docs/game-dev/json-overview/ ; VERIFIED https://github.com/gazure/ldtk-mcp ; VERIFIED https://api.github.com/search/repositories?q=ldtk+godot+importer ; REPORTED https://ldtk.io/docs/game-dev/

### TrenchBroom
**What it is:** A free cross-platform brush-based 3D level editor for Quake-family engines and similar games.
**Cost:** Free.
**Open source:** Yes, GPL-3.0 (VERIFIED, API). 2,898 stars; last push 2026-11-03.
**Extendable:** Entity definition files (FGD, ENT, DEF), game configuration, and source. It has no scripting API (VERIFIED, from the MCP README).
**Agent integration:**
(a) `.map` Quake files are plain text; the manual names the standard Quake format and Valve 220 (VERIFIED, https://trenchbroom.github.io/manual/latest/, first 100,000 characters only). Compile with ericw-tools to a `.bsp`. For Godot 4, `func-godot/func_godot_plugin` (MIT, 885 stars, last push 2026-11-02) is a "Quake .map support for Godot 4" plug-in (VERIFIED metadata).
(b) No command-line editing; the editor is GUI-only (CLI options for conversion are UNVERIFIED).
(c) No scripting API.
(d) MCP, community: `KyodanCFG/trenchbroom-mcp` (no licence listed, 2 stars, last push 2026-08-31, Node 20+): edits `.map` files on disk and does not talk to a running TrenchBroom; reload in the editor after each edit unless you use a patched build; tools for entities, axis-aligned box brushes, SVG top/front/side previews, FGD lookups, `compile_map` through ericw-tools (it treats a leak as failure even when the compiler exits 0), and `launch_map`. Limits: boxes only, no wedges or rotation, launch only tested with a stand-in engine, and the author suggests a 30B-class coding model as a rough minimum (all VERIFIED, README).
(e) None.
(f) `compile_map` reports errors, warnings and leaks; a human walks the level.
**Pros for agentic work:**
- Text `.map` files plus a compile step that gives a checkable pass or fail.
- Free, GPL, and Godot support through func_godot.
**Cons for agentic work:**
- Editing brushes beyond boxes is not agent-practical; the editor itself is GUI-only.
- The MCP server is a 2-star project with no declared licence.
- Quake-style workflow is niche for a Godot course.
**Verdict:** Medium. A text map format with a compile check, but the MCP route is limited to box brushes.
**Sources:** VERIFIED https://api.github.com/repos/TrenchBroom/TrenchBroom ; VERIFIED https://trenchbroom.github.io/manual/latest/ ; VERIFIED https://github.com/KyodanCFG/trenchbroom-mcp ; VERIFIED https://api.github.com/repos/func-godot/func_godot_plugin

---

## Summary table

| Tool | Cost | Open source | Extendable | Agent route | Agent-friendliness |
|---|---|---|---|---|---|
| Blender | Free | Yes (GPL) | Python bpy, add-ons, source | CLI, API, MCP (official and community) | High |
| Maya | Subscription (Indie tier reported) | No | Python, MEL, C++ | CLI (mayapy), API, MCP (community) | Medium |
| 3ds Max | Subscription (Indie tier reported), Windows only | No | MAXScript, pymxs | CLI (Batch), API, MCP (community, 9 stars) | Medium |
| Houdini | Apprentice free non-commercial; Indie, Core, FX paid | No | HDAs, VEX, Python `hou` | CLI (hython), API, MCP (community) | Medium |
| ZBrush | Subscription (trial 14 days) | No | ZScript, Python wrapper | CLI (batch export), MCP (pre-alpha) | Low |
| Cinema 4D | Subscription (Maxon One) | No | Python, C++ | CLI (c4dpy), MCP (official built-in, GUI only; community) | Medium |
| MagicaVoxel | Free (terms reported) | No | None found | File format (.vox), MCP (community) | Medium |
| Aseprite | Paid, US$19.99 on itch.io | Source-available (EULA) | Lua, CLI | CLI, API (Lua), MCP (community) | High |
| Krita | Free | Yes (GPL-3.0) | Python plug-ins | CLI (export), API (in-app), MCP (community) | Medium |
| GIMP | Free | Yes (GPL) | Script-Fu, Python | CLI (batch), MCP (community) | Medium |
| Photoshop | Subscription | No | UXP, ExtendScript, cloud API | MCP (official connector and community), API | Medium |
| Inkscape | Free | Yes (GPL, version UNVERIFIED) | Extensions, actions | CLI, MCP (community) | High |
| Pixelorama | Free | Yes (MIT) | Extensions, GDScript source | CLI (export), MCP (community) | Medium |
| LibreSprite | Free | Yes (GPL-2.0) | Scripting (UNVERIFIED depth) | MCP (community) | Medium |
| Substance 3D Painter | Subscription (Collection) | No | Python, JS plug-ins | API (remote scripting), MCP (community) | Medium |
| Substance 3D Designer | Subscription (Collection) | No | pysbs, SAT CLI | CLI (sbsrender, sbscooker), MCP (community) | Medium |
| Material Maker | Free | Yes (MIT) | Node graphs, source | CLI (export), MCP (community) | Medium |
| ArmorPaint | Free source, paid binaries | Yes (zlib) | Source | MCP (community, tiny) | Low |
| Spine | Paid by edition (US$69 / US$379 / Enterprise, read 2026-11-03) | No | JSON, CLI, runtimes | CLI, file (JSON), MCP (1 star) | Medium |
| Mixamo | Free (Adobe account) | No | None | None | Low |
| Cascadeur | Free non-commercial; Indie and Pro paid | No | Python `csc` | API (in-app), MCP (community) | Low |
| Rokoko Vision | Free 30 s per month; Basic US$10 to 12 per month | No | None | None (web service) | Low |
| FreeMoCap | Free | Yes (AGPL-3.0) | Source, Python | None documented | Low |
| Tiled | Free | Yes (GPL, BSD libs) | JS scripting, Python export | CLI, API (JS), MCP (community) | High |
| LDtk | Free | Yes (MIT) | JSON, Haxe API | File (JSON), MCP (community) | High |
| TrenchBroom | Free | Yes (GPL-3.0) | Entity defs, source | File (.map), MCP (community) | Medium |

## Ledger of UNVERIFIED claims (for the editor)

Blender `.blend` binary; Blender glTF page not loaded; Blender render flags `-o -f -a -E`; EEVEE in background on GPU-less Linux; `bpy.ops.export_scene.gltf` name; argument order and `bpy.data` versus `bpy.ops` advice; macOS binary path; Blender's USD `.usda`; Godot-glTF usage; Whether Anthropic's Claude connector for Blender is the Blender Lab server; Maya education access, licence metering and absence of an Autodesk MCP; 3ds Max `.max` format and SDK; Houdini `.hip` format, HDK, Apprentice with `hython`, absence of a SideFX MCP; ZBrush project formats; Cinema 4D project format and SDK; MagicaVoxel terms, open-source status, version-200 chunks; GPL output principle for Krita and Tiled; Krita headless on a server; Inkscape licence version and SVG-as-text; Photoshop `.psd` binary, cloud API plan requirements and `@adobe/mcp`; Pixelorama `.pxo` and CLI option names; LibreSprite scripting depth, CLI and format compatibility; Substance Painter `.spp` format and current remote-scripting status; Substance Designer `.sbs` XML, `pysbs` licence and Godot `.sbsar`; Material Maker headless operation; ArmorPaint plug-in system, CLI and project format; Spine `.spine` format and CLI licence edition; Mixamo formats, absence of API; Cascadeur `.casc` format; FreeMoCap output formats; LDtk price statement and absence of CLI; TrenchBroom CLI options.
