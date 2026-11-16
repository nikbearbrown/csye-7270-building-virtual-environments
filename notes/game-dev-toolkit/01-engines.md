# Area A: game engines and frameworks, judged for agentic programming
*Part of the game-development toolkit note: see [README.md](README.md). Research date 2026-11-03.*

Researched 2026-11-03 for CSYE 7270 (Building Virtual Environments). Covers 17 tools: Godot, Unity, Unreal Engine, Bevy, GameMaker, Defold, Cocos Creator, O3DE, Stride, Flax Engine, LOVE (Love2D), Phaser, PlayCanvas, Babylon.js, three.js, Construct, RPG Maker.

## Executive summary (read this first)

**Which engines are easiest for an agent to operate end to end, and why.** An agent works best where the whole project is text, one command builds and runs it, and the run can be checked without a person. By that test:

1. **Code-first libraries and engines with no required editor: Bevy, three.js, Babylon.js, Phaser, LOVE.** Everything is source code, the build and run is a terminal command, and there is no GUI session to keep alive. Their weak spots are different: Bevy's API changes every few months (an agent's memory goes stale), LOVE and the web libraries have no built-in test story, and "does it look right" is always a human check.
2. **Godot is the best engine that also has an editor.** Scenes (.tscn) and resources are plain text, `--headless`, `--script`, `--check-only`, `--fixed-fps` and `--quit-after` run without a window, GUT and gdUnit4 give test output, it is free under MIT with no licence server, and more than a dozen MCP servers exist (all community-made, none official). This is why the course uses it.
3. **Engines with strong first-party agent tooling but an editor in the loop: Unity, PlayCanvas, GameMaker, Babylon.js Editor.** Unity has an official MCP server, CLI and plugins for Claude Code and Codex, but it is in beta, needs a licensed running Editor, and its test runner has no defined exit codes. PlayCanvas has an official Editor MCP server that can capture the viewport and inject input. GameMaker has an official Apache-2.0 CLI with a built-in MCP mode (new in 2026).
4. **Unreal is operable but the hardest of the three majors to review.** Assets are binary, so an agent cannot read or diff a level the way it reads a .tscn. Epic's own MCP plugin shipped in UE 5.8 (June 2026) but is labelled experimental. Python scripting, commandlets and automation tests are real and documented.
5. **Weak routes (rated Low): Construct, RPG Maker, O3DE, Stride, Flax.** They are GUI-centred, and the only MCP servers are tiny community projects (0 to 23 stars) or none could be found.

**Things worth telling students.**
- No engine in this list has an *official* MCP server except Unity (beta), Unreal (experimental), GameMaker (inside `gm-cli`), PlayCanvas, Phaser Editor v5 (in development) and the Babylon.js Editor (in the repository, release status unclear). Every Godot, Bevy, Defold, Cocos, O3DE, Flax, LOVE, Construct, RPG Maker and three.js server is community-made.
- Almost every editor MCP server has a tool that runs arbitrary code in the editor or game (GDScript, C#, JavaScript, Python, Lua) and most have no authentication beyond "listens on localhost". Narrow permissions and a separate working copy matter.
- Godot's 2026 contribution policy bans autonomous agents and substantial AI-written code in contributions *to the engine itself*. It says nothing about games made with Godot (read on the primary source, see the Godot entry).
- Unity says "Unity AI" is being retired as a brand name; the pieces are now called "Unity's AI tools". Unity's own pages disagree on whether the MCP server needs a paid subscription (details in the Unity entry).

**Method and limits.** Pages were read with a fetch tool that summarises the page, so wording is paraphrased and some details the summary did not show are marked UNVERIFIED. GitHub figures (stars, licence, last push) come from the GitHub API or repository page on 2026-11-03. "Last push" is the most recent push to any branch, not necessarily a release. Many repositories have an empty Releases tab, so "last release" is often unknown. Epic's own site (license, EULA, FAQ) returned HTTP 403 to the fetch tool, so Unreal licence terms are REPORTED from search results rather than read. Nothing was installed or run.

**Rating key.** High: an agent can create, change, run and check a project from a terminal with no person in a GUI. Medium: most steps are scriptable but a running editor, licence or GUI session is needed, or checking is weak. Low: GUI-centred, or the only agent route is a tiny or unverified community project.

---

## The three major engines

### Godot
**What it is:** A free 2D/3D game engine with a built-in editor; current stable is 4.7.2 (released 2026-08-18; 4.7 itself came out in June 2026), with 3.6.3 also still maintained.

**Cost:** Free. No fees, royalties or seat limits; commercial games are allowed. The only condition is that if you ship Godot with your game you include its copyright and licence notice (a link in your credits is accepted). Terms: https://godotengine.org/license/

**Open source:** Yes, MIT (GitHub shows about 119,500 stars, last push 2026-11-03).

**Extendable:** GDScript (typed, Python-like), C# in the separate .NET editor build, GDExtension (native C/C++/Rust-style plugins; the 4.7 release page shows a project-level GDExtensions list), editor plugins in GDScript, full engine source, and a new in-editor Asset Store (beta in 4.7, replaces the old Asset Library).

**Agent integration:**
- (a) **Files.** Scenes (.tscn) and resources (.tres) are text, and Godot's own documentation describes the format as mostly human-readable and friendly to version control. 4.x files carry `format=3`. Comments are discarded when the editor re-saves a file. Binary .scn/.res exist but are optional. Hand-edits are feasible but the editor rewrites the file on save, so keep agent edits small and re-open in the editor to check. `project.godot` is text (not re-read today, UNVERIFIED).
- (b) **Command line.** Documented flags: `--headless` (shorthand for a headless display driver plus dummy audio), `--script <file.gd>` (must extend SceneTree or MainLoop), `--check-only` (parse and quit, with `--script`), `--quit`, `--quit-after N`, `--fixed-fps N`, `--import` (import resources then quit), `--export-release/--export-debug/--export-pack <preset> <path>`, `--path`, `--log-file`, `--write-movie <file>`, `--doctool` (dump the API reference as XML). **Unknown arguments are silently ignored, so a typo fails without a warning.** Whether a failing script sets a non-zero exit code in every case was not checked (UNVERIFIED), so read the log as well as the exit code. Under `--headless` there is no real rendering, so screenshots and movies need a windowed run or a GPU session (UNVERIFIED for 4.7).
- (c) **Scripting API.** EditorPlugin and EditorScript code can do what the GUI does. The GDScript language server listens on port 6005 by default but needs a running editor on the project.
- (d) **MCP servers.** There is **no official Godot MCP server** (none found on godotengine.org or in the godotengine GitHub organisation; UNVERIFIED as a negative). All below are community projects. Repository facts read 2026-11-03.

| Server (repo) | Licence | Stars | Last push | What it does | Install / notes |
|---|---|---|---|---|---|
| hi-godot/godot-ai | MIT | 3,376 | 2026-11-03 | 46 tools, 120+ operations: scenes, nodes, scripts, signals, UI, materials, animation. Created 2026-04-12 | Needs Godot 4.7+ and `uv`; add-on from Asset Store or release; chain is MCP client, stdio, local Python server, authenticated WebSocket to editor (loopback). Claims anonymous telemetry (21,000+ monthly installs). Org name resembles the Godot Foundation; no sign of affiliation (UNVERIFIED). Writes confined to project; `project.godot` off limits |
| Coding-Solo/godot-mcp | MIT | 6,491 | 2026-04-16 | Launch editor, run project, capture debug output, create scene, add node, save scene, UID tools | `npx @coding-solo/godot-mcp`; Node 18+; most starred but **last push 6.5 months ago, 75 open issues**; sample config auto-approves every tool, change that |
| tugcantopaloglu/godot-mcp | MIT | 509 | 2026-10-09 | 157 tools; headless .tscn edit, script validate, export through Godot CLI; runtime `game_*` tools via an autoload | Godot 4.4+; `GODOT_MCP_ALLOWED_DIRS` restricts paths; runtime eval runs with Godot's permissions |
| tomyud1/godot-mcp | MIT | 449 | 2026-10-17 | MCP server plus editor plugin | npm `godot-mcp-server` (version 0.5.0 per a registry listing, REPORTED) |
| satelliteoflove/godot-mcp | MIT | 183 | 2026-10-02 | 21 tools / 86 actions; input injection, live game-state JSON, frozen-clock stepping, game screenshot, GDScript exec | Godot 4.5+, Node 20+; `--read-only` flag; binds 127.0.0.1; one client at a time. Best for self-checking playtests |
| HaD0Yun/Doyunha-Gopeak | MIT | 269 | 2026-09-12 | 95+ tools incl. LSP (6005) and DAP debugger (6006), screenshots, input | `npx -y gopeak`; many tool groups marked "audit-required" |
| IvanMurzak/Godot-MCP | Apache-2.0 (RQL dependency is PolyForm Shield) | 321 | 2026-11-03 | 24 tools, C# addon, scene tree query language, screenshots | **.NET/mono editor only**; **by default routes through the hosted ai-game.dev relay** (sign-in), self-host mode exists; token stored in plain text locally |
| fennaraOfficial/fennara-godot-ai | MIT | 315 | 2026-11-03 | MCP plus an in-editor chat dock (bring your own API key or local Ollama) | Godot 4.5+; telemetry on by default (anonymous daily install event); CLI installer pipes a remote script into a shell |
| youichi-uda/godot-mcp-pro | Proprietary, **paid, $15 one-time** (vendor page 2026-11-03) | 641 | 2026-09-24 | 162 or 187 tools (README disagrees), screenshots, input record/replay, `execute_editor_script` runs arbitrary GDScript | Public repo holds only the free addon; the MCP server is in the paid package |
| GDAI MCP (gdaimcp.com) | Paid, **$19 one-time** (vendor page 2026-11-03); source licence not stated | n/a | n/a | Scenes, scripts, debugger output, auto screenshots, simulated input | Godot 4.2+; closed-source status UNVERIFIED |
| yurineko73/Godot-MCP-Native | MIT | 869 | 2026-08-03 | "native HTTP, no dependencies" (search listing only; README not opened, REPORTED) | |
| ee0pdt/Godot-MCP | MIT | 621 | 2025-03-19 | Early server | **Stale** (over 19 months) |
| Glade-tool/glade-mcp | MIT | 214 | 2026-11-01 | One bridge for Unity or Godot, 275+ tools (listing, REPORTED) | |

  Common cautions: nearly all can run arbitrary GDScript or Lua-style code in the editor or running game; most bind to localhost with no authentication; the "last release" is unknown for most because Releases tabs are empty. Pin versions and read the source before using `npx` on a project that matters.
- (e) **Built-in AI.** None. The Godot 4.7 release page does not mention AI, LLMs, MCP or agents. Community in-editor chat exists (Fennara above). **Policy note:** the Godot Foundation's 2026 contribution policy bans autonomous AI agents and "vibe coding" in contributions to the engine, disallows substantial AI-generated code, requires disclosure and human review, and says it applies to engine contributions, not to games built with Godot. It was still being drafted when published.
- (f) **Self-verification.** Strong. Headless runs with `--quit-after`, `--log-file`, `--write-movie` (frames to a file), plus two test frameworks: **GUT** (MIT per its README, 2,775 stars, version 9.7.1 targets Godot 4.7.x, command-line runner, JUnit XML export, last push 2026-08-18, 82 open issues) and **gdUnit4** (MIT, 1,287 stars, GDScript and C#, command-line tool for CI, JUnit XML, current master targets Godot 4.7/4.7.1/4.8-dev, last push 2026-11-03). Runtime-aware MCP servers add input injection and state snapshots. Anything visual, audible or about feel is still a human check.

**Pros for agentic work:**
- Plain-text scenes, resources and scripts that diff cleanly in git.
- A real headless CLI plus two maintained test frameworks with JUnit output.
- Free, MIT, no account or licence server, so Codex and Claude Code can run it in a clean container.
- The largest MCP ecosystem of any engine here, several with game-state inspection and input injection.

**Cons for agentic work:**
- No official MCP or AI feature; quality and safety of the many community servers vary and several are stale.
- Silent-ignore of unknown CLI flags and editor re-saves that rewrite files can hide agent mistakes.
- Headless mode cannot judge visuals; MCP servers pinned to Godot 4.5/4.7+ may not match the version a course uses.

**Verdict:** High. Text scenes plus a documented headless CLI and tests let an agent build and check a project with no GUI.

**Sources:** https://godotengine.org/license/ (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html (VERIFIED); https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/editor/external_editor.html (VERIFIED); https://godotengine.org/releases/4.7/ (VERIFIED); https://godotengine.org/article/contribution-policy-2026/ (VERIFIED); https://api.github.com/repos/godotengine/godot and /releases (VERIFIED); https://api.github.com/search/repositories?q=godot+mcp&sort=stars (VERIFIED, source of stars/licence/push dates); https://github.com/hi-godot/godot-ai , https://github.com/Coding-Solo/godot-mcp , https://github.com/tugcantopaloglu/godot-mcp , https://github.com/satelliteoflove/godot-mcp , https://github.com/HaD0Yun/Gopeak-godot-mcp , https://github.com/IvanMurzak/Godot-MCP , https://github.com/fennaraOfficial/fennara-godot-ai , https://github.com/youichi-uda/godot-mcp-pro , https://gdaimcp.com (all VERIFIED); https://github.com/bitwes/Gut , https://github.com/MikeSchulze/gdUnit4 (VERIFIED); https://www.gamingonlinux.com/2026/06/godot-engine-4-7-is-out-bringing-a-new-asset-store-hdr-support-steam-frame-support/ (REPORTED); https://www.gamingonlinux.com/2026/07/godot-engine-to-get-stricter-on-ai-contributed-code/ (REPORTED, matches the primary source).

---

### Unity
**What it is:** A proprietary C# game engine and editor (the Unity 6 family; Unity 6.7 was in beta in the docs found) with the largest asset store and mobile footprint.

**Cost:** Subscription tiers by company size, not by game. Unity Personal is free for revenue and funding under $200,000 over the prior 12 months, listed for "gaming and entertainment applications only". Unity Pro is required above $200K and listed at $210 per month (2026-11-03); Enterprise is required above $25M. Free use for commercial games is therefore allowed under the threshold. Unity's AI tools are priced separately (see (e)). Terms: https://unity.com/products/compare-plans and https://unity.com/legal/terms-of-service/software (Editor Software Terms, updated 2026-06-30). The terms page summary also says third parties may not run the Editor in the cloud or on a remote server except as an Authorized User (section 2.8); read this before putting Unity in a shared cloud agent sandbox (the exact wording was not checked, UNVERIFIED).

**Open source:** No (proprietary; the plans page lists read-only source code access only for Enterprise). Many packages and the agent plugin are public but under the Unity Companion License, not an open-source licence.

**Extendable:** C# scripting, editor scripts (menu items, asset postprocessors), packages through Package Manager, native plugins, and custom MCP tools registered in C#.

**Agent integration:**
- (a) **Files.** Unity supports a text YAML format for scenes, prefabs and assets, and the docs say text is easier to merge and tools can generate and parse it. JetBrains documents Force Text as the default asset serialization for new projects (REPORTED); a few assets can still be binary (for example ScriptableObjects marked for binary). Every asset has a `.meta` file holding its GUID, so an agent must not move or delete files outside the Editor without the .meta. References are by GUID and fileID, which makes hand-editing scenes fragile.
- (b) **Command line.** Documented: `-batchmode` (no dialogs; exits with code 1 on exception or failed operation; one Editor instance per project), `-nographics`, `-quit` (can hide some errors, and can exit before `-runTests` finishes), `-executeMethod Class.Method` (static method in an Editor folder; throw or call `EditorApplication.Exit` with a non-zero code to fail the run), `-projectPath`, `-logFile` (use `-` for the console), `-buildTarget`. Test runs: `-runTests`, `-testPlatform EditMode|PlayMode|<BuildTarget>`, `-testResults <path>` (NUnit XML), `-testFilter`, `-testCategory`, `-assemblyNames`, `-runSynchronously`. **The Test Framework docs say there is no common definition of exit codes, so parse the results XML and the log, not the exit code.** A newer **Unity CLI** (https://docs.unity.com/en-us/unity-cli/unity-cli-reference) installs Editors, builds, tests, manages licences and version control, and with the separate Unity Pipeline package can control a running Editor (Unity 6+). `unity --help` is the authoritative command list; its release status is not stated on the reference page (a Unity blog snippet calls it experimental, REPORTED).
- (c) **Scripting API.** The C# Editor API (AssetDatabase, SerializedObject, EditorApplication, BuildPipeline) can do essentially everything the GUI does, and `-executeMethod` runs it from a terminal.
- (d) **MCP servers.** The **official** one is Unity's MCP server, part of the AI Assistant package (`com.unity.ai.assistant`), Unity 6 (6000.0) or later, **open beta** (announced 2026-05-11). It runs as a bridge inside the Editor; clients launch a relay binary installed at `~/.unity/relay/` with `--mcp`; the first connection from a client appears as a Pending Connection that a person must approve in Project Settings > AI > Unity MCP. Tools: read and edit the scene hierarchy, GameObjects and component values, create and edit C# scripts, read the console, inspect build settings, and register custom C# tools. Clients named: Claude Code, Cursor, Windsurf, VS Code Copilot, Claude Desktop. **Cost conflict:** the May post says an active trial or subscription to the AI tools is required; the unity.com/products/ai page read today says the CLI, MCP server and official plugin are free with no concurrency limits. Treat access terms as unsettled and check before relying on it. Unity also publishes an **official agent plugin** (https://github.com/Unity-Technologies/unity-agent-plugin; Unity Companion License; 604 stars; last push 2026-11-03; Unity 6+): 29 skills for Claude Code (REPORTED) and 31 for Codex (forum post 2026-09-16) covering UI, 2D, rendering, audio, physics, multiplayer, monetisation. Install: `/plugin marketplace add Unity-Technologies/unity-agent-plugin` then `/plugin install unity@unity-agent-plugin` in Claude Code; `codex plugin marketplace add Unity-Technologies/unity-agent-plugin` then `codex plugin add unity@unity-agent-plugin`. The Codex plugin is skills plus CLI, **not** an MCP server. Its README says to keep the project in version control because Editor changes may not be undoable.

| Community server | Licence | Stars | Last push | Notes |
|---|---|---|---|---|
| CoplayDev/unity-mcp | MIT | 15,677 | 2026-10-30 | 50 tools (scenes, scripts, assets, tests, profiling, builds); v10.3.0 on 2026-10-04; Unity 2021.3 to 6.x; Python 3.10+ via `uv`; 127 open issues; README says it is sponsored and maintained by Aura (which sells a paid Unity product) and not affiliated with Unity Technologies |
| IvanMurzak/Unity-MCP | Apache-2.0 | 4,576 | 2026-11-03 | 70+ tools plus optional packages; `script-execute` compiles and runs C# via Roslyn; reflection tools can call private methods; authorization default is `none`; sign-in/cloud option stores a credential locally |
| CoderGamester/mcp-unity | MIT | 2,013 | 2026-10-11 | Unity 6+, Node 18+, version 1.5.0; per-project auth token in `Library/McpUnity/bridge-token`; `add_package` and batch mode off by default; remote links are unencrypted `ws://`; can run EditMode tests |
| hatayama/unity-cli-loop | MIT | 589 | 2026-11-03 | Editor-to-Play-Mode driving from a CLI (listing only, REPORTED) |
| youngwoocho02/unity-cli | MIT | 316 | 2026-08-28 | Single-binary CLI control, deliberately no MCP (listing only, REPORTED) |
| AnkleBreaker-Studio/unity-mcp-server | Other (non-standard) | 534 | 2026-10-23 | 268 tools; licence not OSI-standard, read it first |
| jackwrichards/UnityMCP | Other | 526 | 2025-03-18 | **Stale** |

- (e) **Built-in AI.** Unity's AI tools (beta; Unity is retiring the "Unity AI" brand): an in-Editor **Assistant** with **Ask** (read-only), **Plan** (shows steps for approval) and **Agent** modes, where Agent has three permission levels (read-only, write scripts only, full autonomy) and a permission prompt before changes; **Generators** for UI, 3D objects, materials, cubemaps and sprites; an **AI Gateway** that lets a third-party agent you already subscribe to connect without using Unity credits. Assistant use is credit-based. On the plans page every plan lists a monthly credit allowance (1,000 Personal, 2,000 Pro, 3,000 Enterprise), and unity.com/products/ai says Personal users get a free trial that converts to a $10 per month subscription (read 2026-11-03; check current terms). By default your data is not used to train models; opt-in sharing is in the dashboard; generated assets carry AI-generated metadata; you are responsible for store disclosures.
- (f) **Self-verification.** Strong on paper: Unity Test Framework (NUnit, Edit Mode and Play Mode, command-line runner, XML results), `-batchmode -nographics` for GPU-less machines (no GI baking), console read through MCP. Weak points: the Editor must open the project (no concurrent instance), licence activation is needed on a fresh machine, and exit codes for tests are undefined.

**Pros for agentic work:**
- First-party MCP, CLI and Claude Code/Codex plugins, with a connection-approval step and agent permission levels.
- Documented batch-mode and test CLI with machine-readable (NUnit XML) results.
- Text YAML assets and a huge public body of C# and Unity examples that models know well.
- Large, active community MCP choices (CoplayDev is the most-starred of any engine's servers).

**Cons for agentic work:**
- Needs a licensed, running Editor; one instance per project; Personal licence tied to revenue threshold; cloud-run Editor clause to check.
- Official AI tools are in beta, with conflicting statements on cost; brand and terms are changing.
- GUID/.meta coupling and YAML object ids make direct file edits risky; compile and domain-reload cycles are slow.
- Test exit codes are undefined and `-quit` can end the run before tests finish.

**Verdict:** Medium. Excellent first-party tooling, but everything depends on a licensed running Editor and beta features.

**Sources:** https://unity.com/products/compare-plans (VERIFIED); https://unity.com/legal/terms-of-service/software (VERIFIED, via summary); https://unity.com/products/ai (VERIFIED); https://unity.com/blog/unity-ai-mcp-how-to-get-started (VERIFIED); https://unity.com/blog/unity-ai-assistant-ask-plan-agent-mode-explained (VERIFIED); https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/manual/unity-mcp-get-started.html (VERIFIED); https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor (VERIFIED); http://docs.unity3d.com/6000.2/Documentation/Manual/test-framework/reference-command-line.html (VERIFIED); https://docs.unity.com/en-us/engine/current/manual/working-with-scenes/text-scene-format (VERIFIED); https://docs.unity.com/en-us/unity-cli/unity-cli-reference (VERIFIED); https://github.com/Unity-Technologies/unity-agent-plugin (VERIFIED); https://discussions.unity.com/t/the-official-unity-plugin-for-codex/1736730 (VERIFIED); https://claude.com/plugins/unity (VERIFIED); https://github.com/CoplayDev/unity-mcp , https://github.com/IvanMurzak/Unity-MCP , https://github.com/CoderGamester/mcp-unity (VERIFIED); https://api.github.com/search/repositories?q=unity+mcp&sort=stars (VERIFIED, source of the table figures); https://www.jetbrains.com/help/rider/Asset-serialization-mode.html (REPORTED, via search); https://unity.com/blog/cicd-made-easier-with-unity-cli (REPORTED, via search snippet); https://www.pocketgamer.biz/unity-launches-official-claude-code-plugin-with-29-built-in-engine-skills/ (REPORTED).

---

### Unreal Engine
**What it is:** Epic Games' C++ and Blueprint engine for high-end 3D; current release is UE 5.8 (June 2026), which Epic describes as likely the last UE5 release, with UE6 early access targeted for late 2027 (REPORTED).

**Cost:** Free to download and use. REPORTED from Epic's licence pages via search (Epic's site returned HTTP 403 to the fetch tool, so not read directly): no royalty on the first $1 million of lifetime gross revenue per product, then 5% above that; sales through the Epic Games Store are royalty-free. Commercial games are allowed. Check current terms: https://www.unrealengine.com/en-US/license and the EULA at https://www.unrealengine.com/en-US/eula/unreal. Reported 2026-10-27 to -29: Epic is updating the EULA to remove a restriction on training AI models on engine and MetaHuman outputs (REPORTED; the restriction was about training, not about using a coding agent).

**Open source:** Source-available, not open source. Source is on GitHub to licensees under the Unreal EULA (UE 5.8 forum announcement lists GitHub as a download route; account gating UNVERIFIED).

**Extendable:** C++ modules and plugins, Blueprints, editor Python, Editor Utility Widgets, the Toolset Registry (Python or C++ functions exposed as tools), and the Fab marketplace. Verse exists only in Fortnite's editor (UEFN).

**Agent integration:**
- (a) **Files.** Binary. Levels (.umap) and assets including Blueprints and materials (.uasset) are binary packages; an agent cannot read or diff them as text. Epic's own 2014 blog describes a text *export* for diffing and a Blueprint-only graphical diff, and an old Epic reply said there were no plans to move .uasset to text (REPORTED, old). I found no current official text-asset format (UNVERIFIED as a negative). Text you can diff: C++ and Python source, `.ini` config, `.uproject` (JSON, not re-read today, UNVERIFIED). Practical consequence: use Perforce/Git LFS with locking, and let the agent act through the editor API instead of editing files.
- (b) **Command line.** `UnrealEditor-Cmd` plus: `-ExecutePythonScript` (launches the full editor, opens the default level, runs the script, exits); the **commandlet** `-run=pythonscript -script=...` (faster, can run headless, takes a file or inline code, does not auto-load levels so call `load_level` first); `-ExecCmds="Automation RunTest <name or Group:name>;Quit"` with `-ReportExportPath=<dir>` to write JSON results with HTML (the official page uses `RunTest`; it does not cover exit codes, `-unattended` or Gauntlet). Community reports use `-unattended -NullRHI -NoSound -NoSplash -log` for CI, and a forum user found some tests fail or crash under `-NullRHI` because they need rendering (suggesting `-RenderOffscreen`) (REPORTED).
- (c) **Scripting API.** Python 3.11.8 embedded by the Python Editor Script Plugin, with the `unreal` module exposing nearly everything Blueprints can reach (including plugin additions), transactions (`ScopedEditorTransaction`), and `EditorAssetLibrary` for safe moves. **Python runs only in the Editor**: not in Play-In-Editor, standalone or cooked builds.
- (d) **MCP servers.** The **official** one is Epic's **Unreal MCP** plugin, new in UE 5.8 and labelled **experimental**: Epic's docs say many features are incomplete or missing and APIs and data formats may change. Enable Unreal MCP plus All Toolsets (Toolset Registry comes with it), restart, then turn on Auto Start Server (Editor Preferences > Model Context Protocol) or run `ModelContextProtocol.StartServer`. `ModelContextProtocol.GenerateClientConfig <Client|All>` writes `.mcp.json` for Claude Code, Cursor, VS Code, Gemini and Codex. Endpoint `http://127.0.0.1:8000/mcp`, HTTP and SSE only. **Security: loopback only, rejects non-loopback Origin, no authentication, not safe to expose.** Tools come from toolsets (shipped examples: SceneTools, ActorTools, MaterialInstanceTools, ObjectTools; the 5.8 notes also list an animation toolset and SequencerTools), authored in Python or C++. Tool calls run serially on the game thread; tool search is on by default so a client sees three meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`); new `UFUNCTION`s need an editor restart. Press coverage says agents can spawn actors, set lighting, create material instances, inspect Slate widgets and run automation tests (REPORTED).

| Community server | Licence | Stars | Last push | Notes |
|---|---|---|---|---|
| ChiR24/Unreal_mcp (now EngineWire) | MIT | 1,004 | 2026-10-30 | C++ editor plugin serves MCP itself; one `unreal` tool with search/describe/execute/configure over 450+ capabilities; UE 5.0 to 5.8; v0.6.0 on Fab, GitHub and npm; per-project capability token; deletes need per-call consent; `system_control` runs console commands and Python |
| db-lyon/ue-mcp | MIT | 468 | 2026-11-03 | 30 category tools, 2,114+ actions (about 830 pulled from Epic's registry on 5.8+); `npx ue-mcp init` builds a bridge plugin; UE 5.4 to 5.8; needs a C++ toolchain; write guards and flow rollback; some reads work with the editor closed |
| kevinpbuckley/VibeUE | MIT | 808 | 2026-11-01 | Extends Epic's own MCP (needs UE 5.8+); Python execution and discovery tools plus about 36 skill packs; loopback, no authentication; no in-editor chat |
| tumourlove/monolith | MIT | 362 | 2026-10-18 | MCP plugin for UE 5.7/5.8 (listing only, REPORTED) |
| Natfii/UnrealClaude | README says MIT; GitHub licence field is empty (UNVERIFIED) | 985 | 2026-06-26 | Puts the Claude Code CLI in an editor chat panel and also runs an MCP server on port 3000; UE 5.7 only; build from source; script execution asks permission by default but the plugin launches `claude` with `--skip-permissions`, so review before use |
| chongdashu/unreal-mcp | README says MIT; licence field empty | 2,111 | **2025-04-22** | UE 5.5+, Python FastMCP server plus C++ TCP plugin; README says experimental, not for production; **stale** |
| runreal/unreal-mcp | MIT | 117 | 2025-06-06 | Uses Unreal's Python Remote Execution; no engine plugin; UE 5.4+; `0.0.0.0` bind suggestion exposes the editor to the LAN |
| flopperam/unreal-engine-mcp | none | 1,116 | 2026-06-26 | Repo description says it is now owned by Aura and is promotional; commercial product behind it |

  Also seen but not checked (REPORTED): Aura (paid assistant), Rekall UE (paid, on Fab), a docs-only "Unreal Engine Assistant MCP" that forwards questions to Epic's assistant.
- (e) **Built-in AI.** (1) The UE 5.8 Unreal MCP plugin above, which is a connection layer: the intelligence is the external model. Epic announced at Unreal Fest (2026-06-17) that MCP is meant to become integral to UE6 with a bring-your-own-model approach (REPORTED, Engadget). (2) The **Epic Developer Assistant**: a chatbot on the Epic Developer Community site that answers Unreal documentation questions and generates C++ for UE 5.6 (VERIFIED on an Epic forum post, which also says UE 5.7 would bring it into the editor); a UE 5.7 in-editor assistant panel for questions, C++ snippets and step-by-step guidance is described by trade press as new and experimental, with a reliability and privacy position Epic had not detailed (REPORTED). The assistant's cost was not stated. Neither feature edits your project by itself.
- (f) **Self-verification.** Possible but heavier than Godot or Unity: automation tests with a JSON report, MCP tools that run automation tests (REPORTED), community viewport-screenshot tools, editor log reading. Full verification needs the editor (or a build) and, for rendering tests, a GPU; C++ changes need a compile, and Live Coding does not pick up new `UFUNCTION`s.

**Pros for agentic work:**
- Epic ships its own MCP plugin with a documented toolset system, so tools are first-party and extensible in Python.
- A rich, documented Python API and commandlets cover batch work (imports, LODs, level layout) without a window.
- The automation framework writes machine-readable (JSON) reports.
- Python tool authoring means a team can wrap its own pipeline functions as agent tools.

**Cons for agentic work:**
- Binary assets: no text diff or review of Blueprints and levels; undo is through source control.
- The MCP plugin is experimental, serial, unauthenticated and 5.8-only; most community servers target 5.4 to 5.7 and some are stale.
- Heavy: large installs, slow C++ builds, GPU-dependent tests, Python not available at gameplay runtime.
- Epic's site blocks automated fetching, so terms and docs are harder to check in a pipeline.

**Verdict:** Medium. Real first-party MCP and Python, but binary assets and an experimental plugin make agent work harder to review.

**Sources:** https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor (VERIFIED); https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python (VERIFIED); https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine (VERIFIED); https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes (VERIFIED, first 200,000 characters only); https://forums.unrealengine.com/t/the-epic-developer-assistant-ai-powered-developer-assistant-for-unreal-engine-5-6/2659525 (VERIFIED); https://www.vp-land.com/stories/unreal-engine-5-8-embeds-an-mcp-server-so-ai-agents-can-drive-the-editor (REPORTED); https://www.engadget.com/2196807/epic-games-details-how-its-embracing-gen-ai-in-unreal-engine/ (REPORTED); https://digitalproduction.com/2025/11/12/unreal-engine-5-7-foliage-pcg-and-in-editor-ai/ (REPORTED); https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274 (REPORTED, search snippet); https://www.gamedeveloper.com/programming/epic-is-updating-the-eula-to-allow-ai-training-on-outputs-from-unreal-engine-and-metahuman (REPORTED); https://www.unrealengine.com/en-US/license (REPORTED, 403 to the fetch tool); https://www.unrealengine.com/blog/diffing-unreal-assets and https://forums.unrealengine.com/t/saving-assets-as-text/3927 (REPORTED, via search); https://github.com/ChiR24/Unreal_mcp , https://github.com/db-lyon/ue-mcp , https://github.com/Natfii/UnrealClaude , https://github.com/kevinpbuckley/VibeUE , https://github.com/chongdashu/unreal-mcp , https://github.com/runreal/unreal-mcp (VERIFIED); https://api.github.com/search/repositories?q=unreal+engine+mcp&sort=stars (VERIFIED, source of stars and push dates).

---

## The other engines and frameworks

### Bevy
**What it is:** A free Rust game engine built on an entity-component-system; code-first, no editor yet; latest release 0.20.1 (crates.io, 2026-10-28).

**Cost:** Free; no fees or revenue share; commercial games allowed. https://bevy.org/

**Open source:** Yes, MIT or Apache-2.0 (about 49,500 stars, last push 2026-11-02).

**Extendable:** Plugins (Rust crates), custom Bevy Remote Protocol (BRP) methods, full source.

**Agent integration:** (a) Rust source. The BSN scene system arrived in 0.19 and is refined in 0.20, but a text `.bsn` asset format is still listed as future work. (b) `cargo build`, `run`, `test`; windowless running depends on how the app is built (UNVERIFIED). (c) BRP (`bevy_remote`) is JSON-RPC 2.0 over HTTP: query, spawn, mutate and watch entities and resources in a running app; default port and authentication were not stated, so assume none (UNVERIFIED). (d) **bevy_brp_mcp** in natepiano/bevy_brp (community; MIT or Apache-2.0; 80 stars; last push 2026-10-30; crate 0.23.0 published 2026-10-09 matches Bevy 0.20; the older bevy_brp_mcp repository is archived): launch with logging, read logs, query and mutate components, trigger events; with the optional `bevy_brp_extras` plugin, screenshots and key, mouse and gamepad input. Install `cargo install bevy_brp_mcp`. Others are tiny (bevy_fairy 29 stars, bevy_manual_mcp 17). (e) No built-in AI. (f) `cargo test`, compiler errors, logs, BRP screenshots.

**Pros for agentic work:**
- All text, one toolchain; compiler errors are precise feedback.
- BRP and the MCP give live inspection and screenshots with no editor.

**Cons for agentic work:**
- API breaks every 3 to 4 months (0.17 to 0.20 within a year), so model memory and old tutorials mislead; give the agent the exact version's docs.
- No editor; slow compiles; small MCP ecosystem.

**Verdict:** High. Everything is source plus `cargo`, with a protocol for live inspection; pin the docs to the version.

**Sources:** https://bevy.org/ (VERIFIED); https://bevy.org/news/bevy-0-20/ (VERIFIED); https://crates.io/api/v1/crates/bevy (VERIFIED); https://docs.rs/bevy_remote/latest/bevy_remote/ (VERIFIED); https://docs.rs/bevy_brp_mcp (VERIFIED); https://github.com/natepiano/bevy_brp (VERIFIED); https://api.github.com/repos/bevyengine/bevy and /search/repositories?q=bevy+mcp (VERIFIED).

### GameMaker
**What it is:** A proprietary 2D engine and IDE using the GML language, now owned by Opera (REPORTED), with a new first-party command-line tool.

**Cost:** Free for non-commercial use; a commercial release needs a paid licence. Professional is a one-time purchase listed at $99.99 USD (FAQ, 2026-11-03); console export needs the Enterprise subscription (no price shown). No watermark on any tier. https://gamemaker.io/en/get

**Open source:** The engine and IDE: no. `gm-cli` is Apache-2.0 (YoYoGames/gm-cli, 50 stars, 272 commits). Enterprise includes source access.

**Extendable:** GML, native extensions, and project resources through `gm-cli resourcetool`.

**Agent integration:** (a) A .yyp project file with .yy resource files (JSON, from general knowledge, UNVERIFIED today) and .gml scripts. Reported agent guidance says to edit resources through ResourceTool and .gml directly (REPORTED). (b) `gm-cli`: `init` (can write AGENTS.md, MCP and Claude config), `run`, `compile`, `package` (fetches the runtime itself; Node.js required), `resourcetool` (`eval`, `repl`, `mcp`), `manual` (semantic manual search), `gxgames` publishing. Professional lists "Igor/CI builds". (c) ResourceTool edits resources without the IDE. (d) **Official MCP:** `gm-cli resourcetool mcp`, for resource editing; compile and run with `--errors-only` is the reported debug route (REPORTED). Community: Ampersand-Game-Studios/gms-mcp (MIT, 8 stars, Python 3.11+, `safe`/`standard`/`full` profiles, optional TCP bridge for ping, state, console, screenshot and log tail that needs your game instrumented); yearningss/gamemaker-mcp (REPORTED 225 tools, not opened). (e) No built-in AI found (UNVERIFIED as a negative). (f) Compile and run errors from `gm-cli`; no official screenshot or input tools.

**Pros for agentic work:**
- Official Apache-2.0 CLI with an MCP mode built for agents (announced 2026-04-30, REPORTED).
- Text GML and JSON resources; `init` writes agent config.

**Cons for agentic work:**
- New tool, few users; commercial release and CI builds need paid tiers.
- No first-party way to see or drive the running game; GML is niche in training data.

**Verdict:** Medium. A first-party CLI and MCP exist, but checking the running game is thin.

**Sources:** https://gamemaker.io/en/get (VERIFIED); https://github.com/YoYoGames/gm-cli (VERIFIED); https://github.com/Ampersand-Game-Studios/gms-mcp (VERIFIED); https://www.summerengine.com/gamemaker-mcp (REPORTED; a competing engine vendor's page, used only to find repositories).

### Defold
**What it is:** A free 2D/3D engine from the Defold Foundation, with an editor, Lua scripting and bundling to desktop, mobile and HTML5.

**Cost:** Free. The licence page says no subscription, royalties or fees; commercial games allowed. https://defold.com/license/

**Open source:** Open under the Defold License 1.0 (Apache 2.0-based, but you may not commercialise the engine or editor itself as a game-engine product). GitHub: 6,445 stars, last push 2026-11-03, licence field NOASSERTION. OSI approval is UNVERIFIED.

**Extendable:** Lua; editor scripts (Lua 5.2 inside the editor: menu commands, build hooks, HTTP routes); native C++ extensions built on a build server that can be self-hosted.

**Agent integration:** (a) Project files are text; the exact syntax is UNVERIFIED today. (b) `bob.jar`: `resolve`, `build` (`--archive`), `bundle --platform`, `distclean`; needs OpenJDK 25; targets macOS, Windows, Linux, iOS, Android, HTML5. Native-extension builds use build.defold.com unless you self-host, so code leaves the machine. Editor-script hooks are not run by Bob. (c) Editor scripts run only inside the editor. (d) MCP, all community: zrnge/defold-mcp, listed on Defold's asset portal (MIT, Node 20+; inspect, edit, validate, build, run; repository not opened); rochana-sadila/defold-mcp (MIT, 1 star, 7 commits, no releases: 10 tools including `defold_build`, `defold_run_headless`, `defold_run_tests`; you supply bob.jar and `dmengine_headless`; stdio only, project-root scoped; hot reload experimental); a "Defold AI" live-editor server described only in a blog post (UNVERIFIED). (e) No built-in AI. (f) Headless engine run plus a PASS:/FAIL: line convention in the small server.

**Pros for agentic work:**
- A real CLI build and a headless engine binary; free, no licence server.
- Small text projects, simple Lua API.

**Cons for agentic work:**
- Only hobby-scale MCP servers; the editor is needed for scene layout.
- Native extensions need a remote or self-hosted build server.

**Verdict:** Medium. Bob plus a headless engine make it scriptable, but the MCP side is hobby-grade.

**Sources:** https://defold.com/license/ (VERIFIED); https://defold.com/manuals/bob/ (VERIFIED); https://defold.com/manuals/editor-scripts/ (VERIFIED); https://defold.com/assets/defold-mcp (VERIFIED); https://github.com/rochana-sadila/defold-mcp (VERIFIED); https://api.github.com/repos/defold/defold (VERIFIED); https://hashnode.com/posts/defold-ai-the-mcp-that-connects-claude-code-straight-into-your-live-defold-editor/6a162094da253d50d4f30823 (REPORTED).

### Cocos Creator
**What it is:** A 2D/3D engine with a desktop editor and TypeScript scripting, strong in mobile and mini-games (repository shows v3.8.9).

**Cost:** Free. The editor EULA grants a royalty-free, revocable licence to build applications and games; you keep rights to your games; an account is required. The text I read never says "commercial", so confirm before a paid release. https://github.com/cocos/cocos-engine/blob/develop/licenses/EDITOR_license_and_terms_en.txt

**Open source:** Split. The runtime is MIT (about 9,900 stars, last push 2026-10-28); the editor is proprietary (no copying, forking or redistribution). A report that Cocos 4 goes fully MIT is unconfirmed (UNVERIFIED).

**Extendable:** TypeScript components; editor extension packages in a project's `extensions` folder; runtime source.

**Agent integration:** (a) Scenes and prefabs are serialized files (JSON, UNVERIFIED today); docs warn that two people editing one prefab give conflicts git cannot merge. (b) `CocosCreator --project <dir> --build "platform=web-desktop;debug=true"`; exit codes 32 (bad parameters), 34 (unexpected error), 36 (success). **No headless mode: the docs say it still needs a GUI environment.** (c) Editor extensions run JavaScript against editor APIs. (d) Community MCP: FunplayAI/funplay-cocos-mcp (MIT, 378 stars; Creator 3.8+; 39 tools by default, 106 in the full profile; screenshots, runtime control, input simulation; `execute_javascript` runs arbitrary JavaScript in the editor and its checks are not a sandbox; localhost by default); DaxianLee/cocos-mcp-server (about 1.5k stars, 50 tools, localhost:3000/mcp, **licence forbids commercial use and resale of the plugin and derivatives**). (e) No built-in AI found. (f) Build exit codes; screenshots and input through Funplay.

**Pros for agentic work:**
- Documented build CLI with exit codes; MIT runtime.
- A capable MCP with screenshots and input simulation.

**Cons for agentic work:**
- Needs a GUI session even for builds; the editor is closed.
- The licence trap on one MCP server; asset formats undocumented for hand-editing.

**Verdict:** Medium. A usable MCP and build CLI, but nothing runs without a GUI environment.

**Sources:** https://github.com/cocos/cocos-engine (VERIFIED); https://github.com/cocos/cocos-engine/blob/develop/licenses/EDITOR_license_and_terms_en.txt (VERIFIED); https://docs.cocos.com/creator/3.8/manual/en/editor/publish/publish-in-command-line.html (VERIFIED); https://docs.cocos.com/creator/3.8/manual/en/asset/prefab.html (VERIFIED); https://github.com/FunplayAI/funplay-cocos-mcp (VERIFIED); https://github.com/DaxianLee/cocos-mcp-server (VERIFIED); https://techintelpro.com/news/ai/generative-ai/cocos-4-game-engine-fully-open-sourced-under-mit-license (REPORTED, unconfirmed).

### O3DE (Open 3D Engine)
**What it is:** A free, open-source multi-platform C++ 3D engine for games, cinematic worlds and simulation, built with CMake.

**Cost:** Free; no royalties; the repository carries both Apache-2.0 and MIT licence files. https://github.com/o3de/o3de

**Open source:** Yes, Apache-2.0 (MIT file also present); about 9,800 stars, last push 2026-11-03, about 3,500 open issues.

**Extendable:** Gems (C++ modules), Python editor bindings (`azlmbr`), Lua and visual scripting (the last two UNVERIFIED today), full source.

**Agent integration:** (a) Levels and prefabs as JSON text (UNVERIFIED). (b) CMake builds; the Editor can run a Python script at launch (exact flag not confirmed, UNVERIFIED). (c) EditorPythonBindings expose editor functions; a level must be loaded first. (d) Community only: nickschuetz/o3de-mcp (Apache-2.0 or MIT; 16 stars, 65 commits, no releases; `pip install o3de-mcp` or `uvx o3de-mcp`): 96 tools in 7 categories; 17 project and build tools work without the editor; 41 editor tools need `o3de-ai-companion-gem` and EditorPythonBindings and include **arbitrary Python execution in the editor**; plaintext on 127.0.0.1 by default; ships a headless-verification and rendering skill, tested on Linux with Xvfb, not yet on Windows. (e) No built-in AI found. (f) That headless skill (Linux).

**Pros for agentic work:**
- Free, permissive and fully source-available, so an agent can read the engine.
- Python editor API and a headless Linux recipe.

**Cons for agentic work:**
- Large C++ build and steep setup; little training data.
- One 16-star MCP server is the whole agent story.

**Verdict:** Low. Capable in principle, but heavy to build and only a tiny community MCP.

**Sources:** https://github.com/o3de/o3de (VERIFIED); https://api.github.com/repos/o3de/o3de (VERIFIED); https://github.com/nickschuetz/o3de-mcp (VERIFIED); https://docs.o3de.org/docs/user-guide/editor/editor-automation/ (REPORTED, via search snippet).

### Stride
**What it is:** A free, open-source C# game engine (formerly Xenko) with a Game Studio editor; latest listed release 4.4.

**Cost:** Free, MIT; commercial games allowed. https://www.stride3d.net/

**Open source:** Yes, MIT (about 7,900 stars, last push 2026-11-03).

**Extendable:** C# scripts and assets, NuGet packages, full source, and the Stride Community Toolkit for code-only games (REPORTED).

**Agent integration:** (a) Scenes and prefabs are separate assets (`.sdscene`, `.sdprefab`) that appear to be YAML written by Stride's asset serializer (REPORTED from a community gist; schema undocumented). (b) Release builds use the IDE or command line, not Game Studio (4.3 docs, REPORTED); a Stride CLI exists, and a third-party `ferafiks.Stride.Cli` manages assets and packages (REPORTED). Game Studio is Windows-first; docs include a Linux-under-Wine guide. (c) C# is the API; no editor automation API found. (d) **No Stride-specific MCP server found** in searches (UNVERIFIED as a negative). (e) No built-in AI. (f) `dotnet build` and `dotnet test` for code only.

**Pros for agentic work:**
- MIT C# with standard `dotnet` tooling and clear compile errors.
- A code-only toolkit lets an agent skip Game Studio.

**Cons for agentic work:**
- No MCP; no documented headless editor; scene work is GUI work.
- Small community, less training data.

**Verdict:** Low. No agent route to the editor, though the code-only route works.

**Sources:** https://www.stride3d.net/ (VERIFIED); https://doc.stride3d.net/latest/en/manual/index.html (VERIFIED); https://api.github.com/repos/stride3d/stride (VERIFIED); https://doc.stride3d.net/4.3/en/manual/files-and-folders/building-the-game/building.html (REPORTED, via search); https://gist.github.com/Eideren/0aa59644eb7c5b029d04b7fa5a285e62 (REPORTED).

### Flax Engine
**What it is:** A 3D game engine with a C++ core, C# scripting and an editor, aimed at desktop, console and mobile.

**Cost:** Free for non-commercial and educational use and for games with no revenue. Commercial products pay 4% of gross revenue after the first $250,000 per game per calendar quarter, with notice before release and quarterly reports (FAQ, 2026-11-03); custom licences exist. https://flaxengine.com/faq/

**Open source:** Source-available, not open source. C++ and C# source and the editor are on GitHub under the Flax EULA; you may not publish modifications, only share them with other licensees on the same version (GitHub licence NOASSERTION; about 7,100 stars, last push 2026-11-02).

**Extendable:** C# and C++ scripts and plugins; visual scripting (UNVERIFIED); engine source.

**Agent integration:** (a) `.flaxproj` project; scene and asset formats not checked (UNVERIFIED). (b) No command-line or headless editor mode confirmed (UNVERIFIED). (c) C# editor plugins. (d) Community only: meet-brad-ch/FlaxMCP-Live (MIT, 0 stars, 96 commits, a fork of eXoz00rd/FlaxMCP): 57 tools in ten toolsets (project, content, scene, build, logs, editor, events, jobs, game); needs .NET 10 and Flax 1.13.7012 or newer; built from source; live, screenshot and build tools need a GUI editor (build tools need it closed); `editor_execute_csharp` and `editor_invoke_method` run arbitrary C# with full user permissions and are off by default; `FLAX_READ_ONLY=true` limits it to inspection. (e) No built-in AI. (f) Logs and play control through that server only.

**Pros for agentic work:**
- Readable C#/C++ source; the MCP has a read-only mode and disables code execution by default.

**Cons for agentic work:**
- One zero-star MCP, source-build install, no confirmed headless mode.
- Royalty terms, no public modifications, small community.

**Verdict:** Low. Only a single unproven community MCP and no confirmed CLI.

**Sources:** https://flaxengine.com/faq/ (VERIFIED); https://github.com/meet-brad-ch/FlaxMCP-Live (VERIFIED); https://api.github.com/repos/FlaxEngine/FlaxEngine (VERIFIED).

### LOVE (Love2D)
**What it is:** A small free 2D framework where games are written in Lua; no editor, no scene files. Stable is 11.5; 12.0 has been "in development" on the wiki (whether it has shipped is UNVERIFIED).

**Cost:** Free, including commercial games. https://love2d.org/

**Open source:** Yes, zlib/libpng licence (about 8,900 stars).

**Extendable:** Lua and LuaJIT libraries, C modules via FFI, full source.

**Agent integration:** (a) Plain `.lua` files, `conf.lua`, ordinary image and audio assets. (b) `love <project-dir>` runs a project; a headless or test mode is not documented on the pages read (UNVERIFIED), so CI would use a virtual display. (c) The framework is the API; there is no editor to automate. (d) Community only: InfiniteLoopRD/lovepilot (MIT, 0 stars, 6 commits, fork of shayarnett/love2d-mcp; Node 18+, LOVE 11+): `get_screenshot`, `send_input`, `get_objects`, `watch_game_state`, `run_lua`, `reload_code` over an unauthenticated TCP bridge on port 12345; your game must include `mcp_bridge.lua` and call `captureIfPending()` in `love.draw`. A docs-lookup server (vanrez-nez/love2d-mcp) also exists (REPORTED). (e) No built-in AI. (f) Screenshot and input via LovePilot; Lua test libraries such as busted are standard but unchecked (UNVERIFIED).

**Pros for agentic work:**
- Tiny API and pure text; an agent can write and reason about a whole game in a few files.
- Free, zlib, no account or licence server.

**Cons for agentic work:**
- No built-in tests, headless mode or editor; checking is "run it and look".
- The only MCP is a new zero-star fork; `run_lua` plus an open TCP port is a risk.

**Verdict:** Medium. Pure text and a one-command run, but no test or headless story.

**Sources:** https://love2d.org/ (VERIFIED); https://github.com/love2d/love (VERIFIED); https://github.com/InfiniteLoopRD/lovepilot (VERIFIED); https://www.love2d.org/wiki/12.0 (REPORTED, 403 to the fetch tool; seen in search); https://glama.ai/mcp/servers/InfiniteLoopRD/lovepilot (REPORTED).

### Phaser
**What it is:** A mature open-source HTML5 2D game framework in JavaScript/TypeScript (v4.2.1 on the repository), with an optional desktop Phaser Editor v5.

**Cost:** The framework is free, MIT, commercial games allowed. Phaser Editor v5 pricing was not on the pages I read (UNVERIFIED). A separate AI game-making product, Phaser AE, uses credits (packs from $10 for 3,500 credits; Pro $20 per month for 8,000 credits; pricing page, 2026-11-03). https://phaser.io/pricing

**Open source:** Framework yes (MIT; about 40,600 stars). Editor v5 and Phaser AE licensing UNVERIFIED (the pricing page links a PolyForm Shield engine licence without saying which product it covers).

**Extendable:** JS/TS plugins, custom game objects and shaders, Spine and Tiled support, source.

**Agent integration:** (a) Plain JS/TS source plus JSON maps and assets. (b) npm and Vite; running needs a browser, and headless Chromium with a test runner is the usual check (not verified here). (c) The library is the API. (d) **Official MCP:** Phaser Editor v5 ships an MCP server (repo phaserjs/editor-mcp-server, 36 stars, distributed as an npm package): 39 tools in four groups (IDE 5, Assets 13, Scene 13 including a scene screenshot, editable Tilemap 8); needs the desktop editor running and Node; the docs say it is still in development; the editor's AI menu auto-configures Claude Desktop, Cursor and VS Code. (e) Editor v5 has a built-in AI Chat for Gemini, Claude, Cursor, OpenAI-compatible and OpenRouter models. The framework repository carries an agent `skills/` folder and a v3 to v4 migration skill. A `npx @phaser-ae/cli` route for your own agent is mentioned in the docs (UNVERIFIED, not opened). (f) Editor scene screenshots; browser tests.

**Pros for agentic work:**
- A web stack models know well; the repo ships agent skills.
- Official editor MCP and AI chat from the maintainers.

**Cons for agentic work:**
- The MCP covers Editor scenes, not game code, and needs the desktop editor open.
- Editor and AE licensing unclear; v3 to v4 differences confuse models.

**Verdict:** High. A code-first web framework with official agent skills and an editor MCP.

**Sources:** https://github.com/phaserjs/phaser (VERIFIED); https://phaser.io/oss/docs/phaser-editor/ai/mcp-server.md (VERIFIED); https://phaser.io/news/2026/04/phaser-editor-v5-release (VERIFIED); https://phaser.io/pricing (VERIFIED); https://github.com/phaserjs/editor-mcp-server (VERIFIED).

### PlayCanvas
**What it is:** An open-source WebGL/WebGPU engine plus a collaborative browser-based visual editor and hosting.

**Cost:** Editor plans (2026-11-03): Free $0 (1 GB, unlimited public projects, free hosting), Personal $15 per month (private projects, 10 GB), Organization $50 per seat per month. The page does not address commercial use on the free plan; check the terms. https://playcanvas.com/pricing

**Open source:** Engine yes (MIT; about 17,200 stars); the Editor has a public repository. The hosted editor is a service.

**Extendable:** JavaScript/TypeScript scripts, engine API, VS Code extension for text assets, editor MCP.

**Agent integration:** (a) Scripts are text; scenes live in PlayCanvas's cloud project (the docs point to the VS Code Extension for text edits with local diffs). (b) The engine builds with npm; no CLI for the hosted editor found. (c) Engine API in JS. (d) **Official MCP:** `@playcanvas/editor-mcp-server` (repo playcanvas/editor-mcp-server, MIT, 150 stars): about 130 tools in 15 categories (project, entities, components, scripts, assets, scenes, settings, templates, animation, builds, version control) plus verification tools: capture the Editor viewport, start and stop Launch, read runtime logs, query entity state, inject keyboard, mouse and touch input. Needs Node 22.18+, Editor 2.35+ for project tools, port 52000, Chrome's local-network permission; one Editor and one agent at a time. Install: `claude mcp add playcanvas -- npx -y @playcanvas/editor-mcp-server`. It acts through your logged-in session and can delete entities, assets, builds and branches (docs advise a checkpoint first). The engine repository includes `AGENTS.md` and `context7.json`. (e) No built-in chat found. (f) Viewport capture, logs, input injection.

**Pros for agentic work:**
- Official MCP with real verification tools (screenshot, logs, input).
- MIT engine and a free tier; no local install.

**Cons for agentic work:**
- The scene lives in a cloud editor session, so review and git-style diffs are weaker.
- One editor and one agent at a time; destructive operations; free-plan projects are public.

**Verdict:** High. An official MCP that can edit and then check its own work in the viewport.

**Sources:** https://developer.playcanvas.com/user-manual/editor/mcp-server/ (VERIFIED); https://github.com/playcanvas/editor-mcp-server (VERIFIED); https://github.com/playcanvas/engine (VERIFIED); https://playcanvas.com/pricing (VERIFIED).

### Babylon.js
**What it is:** A TypeScript 3D rendering and game library for the web, with a desktop Babylon.js Editor.

**Cost:** Free, Apache-2.0, commercial use allowed. https://github.com/BabylonJS/Babylon.js

**Open source:** Yes, Apache-2.0 (about 26,300 stars); the Editor is also Apache-2.0 (about 1,100 stars).

**Extendable:** TypeScript/JavaScript, node materials, plugins, source.

**Agent integration:** (a) Source code; the Editor stores scenes and TypeScript behaviour scripts. (b) npm and bundlers; a browser to run. (c) The library API. (d) The Editor repository has an `mcp/` folder with a tools contract: an HTTP server inside the editor on `127.0.0.1:3712` with an optional token that rejects requests carrying an `Origin` header; tools cover scenes, nodes, meshes, lights, cameras, materials, assets, TypeScript scripts, JavaScript "agent automation" scripts, screenshots, running and stopping the game, simulated input, console logs and batches; saving needs a person's confirmation. Whether it is released and maintained was not shown (UNVERIFIED). Also a community "MCP for Babylon" (pandaGaume/mcp-for-babylon, Apache, posted 2026-03-11): browser UMD bundles plus a Node WebSocket tunnel. (e) The Editor has an assistant panel (REPORTED, from the contract file). (f) Screenshots, play-testing and console logs via the Editor MCP.

**Pros for agentic work:**
- Strong TypeScript types; a written tool contract with loopback binding and a save-confirm step.
- Play-test and screenshot tools are in the same contract.

**Cons for agentic work:**
- Editor MCP release and support status unclear; web-only runtime.
- The community MCP is one author's project.

**Verdict:** High. A typed web library whose editor ships an MCP contract with verification tools (release status unconfirmed).

**Sources:** https://github.com/BabylonJS/Babylon.js (VERIFIED); https://github.com/BabylonJS/Editor (VERIFIED); https://github.com/BabylonJS/Editor/tree/master/mcp (VERIFIED); https://raw.githubusercontent.com/BabylonJS/Editor/master/mcp/mcp-tools-contract.md (VERIFIED); https://forum.babylonjs.com/t/mcp-for-babylon-let-ai-agents-control-your-scene/62756 (VERIFIED).

### three.js
**What it is:** The most used JavaScript 3D rendering library; a renderer and scene graph, not a full game engine (no built-in editor or game framework, general knowledge).

**Cost:** Free, MIT, commercial use allowed. https://github.com/mrdoob/three.js

**Open source:** Yes, MIT (about 117,500 stars).

**Extendable:** Add-ons, loaders, shaders (including WebGPU and node-based), a large ecosystem (React Three Fiber and others).

**Agent integration:** (a) Plain JS/TS plus glTF assets. (b) npm and Vite; a browser to view. (c) The library is the API. (d) Community only: DmitriyGolub/threejs-devtools-mcp (MIT, 128 stars, 41 commits; `claude mcp add threejs-devtools-mcp -- npx threejs-devtools-mcp`): 69 tools for objects, materials, shaders, textures, animation and performance, plus Playwright and Puppeteer helpers and frame capture; it injects a bridge into your dev-server page; live edits are not saved to your code, it reports before/after diffs; development use only. Docs-only servers also exist (REPORTED). (e) The repository includes an `llms.txt` for models. (f) Frame capture and browser automation.

**Pros for agentic work:**
- The library models know best; `llms.txt` ships in the repository.
- Browser dev tools and Playwright are a mature way to screenshot and test.

**Cons for agentic work:**
- Not a game engine; the agent designs the game architecture.
- The MCP needs an injected bridge and an open browser tab; no official MCP.

**Verdict:** High. Code-only, widely known and easy to screenshot; remember it is a renderer, not an engine.

**Sources:** https://github.com/mrdoob/three.js (VERIFIED); https://github.com/DmitriyGolub/threejs-devtools-mcp (VERIFIED); https://github.com/deya-0x/ThreeJSMCP (REPORTED, via search).

### Construct
**What it is:** A proprietary, browser-based no-code/low-code 2D game maker (Construct 3, from Scirra) using event sheets and optional JavaScript.

**Cost:** Subscription editor with a limited Free Edition (50 events, 2 layers, HTML5 publishing, no monetisation); paid plans are royalty-free. Startup and Business plans apply to registered businesses (Startup limits as the page reads 2026-11-03: $50,000 revenue, $100,000 assets or more than 3 employees; check the page). https://www.construct.net/en/make-games/buy-construct

**Open source:** No.

**Extendable:** JavaScript scripting and an addon SDK (the page's JS limits conflict between footnote and table, UNVERIFIED), user-made addons.

**Agent integration:** (a) Folder projects are text: `project.c3proj` (JSON) indexes the project and event sheets are JSON; a `.c3p` is a ZIP; the `uistate` folder can be ignored in source control (REPORTED from Scirra's tutorial via search). (b) No command line or headless mode found (UNVERIFIED); it runs in the browser, so an outside agent only reaches files on disk and a preview tab. (c) No external automation API found. (d) **No official MCP.** Community: liauw-media/construct3-mcp (MIT, 23 stars, 84 commits, README describes v1.10.0, clone and `npm ci`): 83 tools to read, analyse and edit folder projects with backups and read-back checks; runtime tools inject a bridge and drive the game over the Chrome DevTools Protocol. The README says the bridge injection has not yet been checked in the real editor, and you must close and reopen the project in Construct before saving there or it may overwrite the agent's edits. (e) No AI found in the editor. (f) Project validation and runtime driving through that server only.

**Pros for agentic work:**
- JSON folder projects can be diffed; the community server guards object ids and formatting that agents otherwise break.

**Cons for agentic work:**
- Closed, subscription, browser-bound editor with no CLI; one 23-star server with admitted gaps.
- Editor and agent can overwrite each other's changes.

**Verdict:** Low. File edits work, but there is no official route and the editor can clobber outside edits.

**Sources:** https://www.construct.net/en/make-games/buy-construct (VERIFIED); https://github.com/liauw-media/construct3-mcp (VERIFIED); https://www.construct.net/en/tutorials/constructs-project-format-3275 (REPORTED, 403 to the fetch tool; seen in search); https://www.summerengine.com/construct-3-mcp (REPORTED; a competing vendor's page).

### RPG Maker
**What it is:** A proprietary desktop tool for making classic JRPGs (MZ and MV) with a JavaScript plugin system, sold by Gotcha Gotcha Games.

**Cost:** Paid one-time purchase (price not read; check the store) with a free trial. The official FAQ says a purchase includes the right to make commercial games with no further fees or royalties (REPORTED via search). Japanese terms are said to cover personal use, including commercial, but not corporate business use (REPORTED); confirm if a studio is a company. https://www.rpgmakerweb.com/products/rpg-maker-mz

**Open source:** No.

**Extendable:** JavaScript plugins registered in a Plugin Manager; community plugins, each with its own licence.

**Agent integration:** (a) Project data is JSON in the project's `data` folder and plugins are `.js` files (UNVERIFIED today). (b) No command line or headless mode found (UNVERIFIED). (c) No editor automation; plugins run inside the game. (d) Community only: devmagary/MCP-Maker (TypeScript, 2 stars, 3 commits, no licence shown, no releases): create and edit database entries (items, weapons, armors, enemies, states, actors, classes, skills), create and list maps, install plugins into `js/plugins` and `plugins.js`, scan resources; atomic writes and a `System.json` version bump make the editor reload. (e) No built-in AI. (f) None; a person must open and playtest in the editor.

**Pros for agentic work:**
- Structured JSON data and plain-JavaScript plugins let an agent generate content and plugins.

**Cons for agentic work:**
- GUI-bound, paid, closed; no CLI; the only MCP is a 2-star hobby project with no stated licence.
- No automated way to run and check the game.

**Verdict:** Low. GUI only, with an agent route that is a three-commit community project.

**Sources:** https://www.rpgmakerweb.com/products/rpg-maker-mz (VERIFIED); https://github.com/devmagary/MCP-Maker (VERIFIED); https://rpgmakerweb.com/faq (REPORTED, via search); https://lobehub.com/nl/mcp/devmagary-mcp-maker (REPORTED).

---

## Cross-cutting cautions for students

1. **An MCP server is code that controls your editor.** Most expose a tool that runs arbitrary code in the editor or game (`execute_editor_script`, `script-execute`, `execute_javascript`, `execute_python`, `run_lua`, `editor_execute_csharp`). Prefer read-only or safe profiles where offered (satelliteoflove/godot-mcp `--read-only`, FlaxMCP `FLAX_READ_ONLY`, gms-mcp `safe`), keep the editor in a throwaway copy of the project, and never auto-approve every tool.
2. **Telemetry and relays differ.** hi-godot/godot-ai reports anonymous usage counts; Fennara has telemetry on by default; IvanMurzak's Godot and Unity servers route through a hosted relay unless you choose a custom server; Unity's own MCP needs a Unity Cloud-connected project (May 2026 post).
3. **Commercial sponsors sit behind some "community" servers.** CoplayDev/unity-mcp says it is sponsored and maintained by Aura, which sells a paid Unity product; flopperam/unreal-engine-mcp says it is now owned by Aura.
4. **Exit code 0 is not evidence.** Unity documents that test exit codes have no common definition and that `-quit` can end before tests finish; Godot silently ignores unknown arguments; Cocos returns 36 for a successful build and different codes for failures. Parse reports (NUnit XML, JUnit XML, Unreal's JSON report) and read the log.
5. **Stars are not maintenance.** Coding-Solo/godot-mcp (6.5k stars) was last pushed 2026-04-16; chongdashu/unreal-mcp (2.1k) 2025-04-22; ee0pdt/Godot-MCP 2025-03-19; jackwrichards/UnityMCP 2025-03-18.
6. **Licence traps.** DaxianLee/cocos-mcp-server forbids commercial use; Flax and Unreal are source-available, not open source; Unity Personal is capped by revenue; Godot's AI policy applies to contributions to the engine, not to games.

---

## Summary table

| Tool | Cost | Open source | Extendable | Agent route | Agent-friendliness |
|---|---|---|---|---|---|
| Godot | Free, MIT, commercial OK | Yes (MIT) | GDScript, C#, GDExtension, editor plugins | CLI (headless) + community MCP (no official) | High |
| Unity | Free under $200K revenue/funding; Pro/Enterprise above; AI tools credit-based | No | C#, packages, custom MCP tools | CLI + official MCP (beta) + official plugin | Medium |
| Unreal Engine | Free; 5% royalty above $1M per product (REPORTED) | Source-available | C++, Blueprints, Python, Toolset Registry | CLI/Python commandlet + official MCP (experimental, UE 5.8) | Medium |
| Bevy | Free, MIT/Apache-2.0 | Yes | Rust crates, plugins, BRP methods | CLI (cargo) + BRP + community MCP | High |
| GameMaker | Free non-commercial; Pro one-time for commercial | No (gm-cli is Apache-2.0) | GML, extensions, ResourceTool | CLI (gm-cli) + official MCP mode | Medium |
| Defold | Free, no royalties | Defold License (Apache-based) | Lua, editor scripts, native extensions | CLI (bob.jar) + community MCP | Medium |
| Cocos Creator | Free (editor EULA, royalty-free) | Runtime MIT, editor closed | TypeScript, editor extensions | CLI build (needs GUI) + community MCP | Medium |
| O3DE | Free, Apache-2.0/MIT | Yes | C++ gems, Python, Lua | Python + community MCP | Low |
| Stride | Free, MIT | Yes | C#, NuGet | dotnet CLI only; no MCP found | Low |
| Flax Engine | Free non-commercial; 4% above $250K/quarter per game | Source-available | C#, C++ | Community MCP (1) | Low |
| LOVE (Love2D) | Free, zlib | Yes | Lua, FFI | CLI run + community MCP (1) | Medium |
| Phaser | Free (MIT); Editor v5 pricing unverified | Framework yes | JS/TS, plugins | npm + official Editor MCP | High |
| PlayCanvas | Engine MIT; editor Free/$15/$50 tiers | Engine yes | JS/TS, VS Code ext | Official Editor MCP | High |
| Babylon.js | Free, Apache-2.0 | Yes | TS/JS, plugins | npm + Editor MCP (in repo) + community MCP | High |
| three.js | Free, MIT | Yes | Add-ons, ecosystem | npm + community MCP | High |
| Construct | Free tier (limited); subscription | No | JS, addons | Files + community MCP | Low |
| RPG Maker | Paid one-time, free trial | No | JS plugins | Files + community MCP (1) | Low |
