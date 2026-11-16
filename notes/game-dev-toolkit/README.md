# The game-development toolkit, judged for agentic programming

*CSYE 7270 course note. Research date 2026-11-03.*

## Executive summary

**What this is.** A reference list of the tools a game developer might use, with 130 entries in the tables below: engines, 3D and 2D art, animation and level tools, audio, asset sources, design tools, editors, version control, CI, testing, profiling, project management, storefronts, backend services, coding agents and AI asset generators. For each tool it says whether it is free, whether it is open source, whether it can be extended, and how well a coding agent such as Claude Code or Codex can use it today, with pros and cons from the agent's side. The full entries are in the five files listed at the end.

**Why read it.** Choosing a tool in a course taught with coding agents is a bet on how well an agent can drive it. An agent does best where the project is plain text, one command builds, runs and tests it with no window, and the result can be checked without a person looking. A tool can be excellent for a human and nearly unusable for an agent: GUI only, binary files, no scripting, or terms that forbid automation.

**What it found.**
1. **Plain text and a command line beat everything else.** The best agent routes are text files plus a CLI: Godot (text scenes, headless mode, GUT and GdUnit4 tests), Blender (bpy scripting), Tiled and LDtk (JSON maps), Aseprite (CLI and Lua), Inkscape (SVG), FFmpeg, Git, GitHub Actions. Unreal's assets are binary, so an agent cannot read or diff a level the way it reads a Godot scene.
2. **Official MCP servers are rare; most are community-made and young.** Official routes exist for Unity (beta), Unreal 5.8 (experimental), Blender (Blender Lab, needs Blender 5.1 or later), Figma, Adobe, Cinema 4D (built in, GUI only), GameMaker (inside its CLI), PlayCanvas, Superluminal, Linear, Jira, Trello, Notion and GameAnalytics. Godot has no official MCP server (more than a dozen community ones). No official server was found for FMOD, Wwise, Aseprite or Krita (an absence claim); the community ones are small.
3. **An MCP server is code that runs with your permissions.** Nearly every editor server has a tool that runs arbitrary code in the editor (GDScript, C#, Python, Lua, JavaScript). Treat it as shell access. Use a throwaway copy of the project, narrow permissions, and prefer a command-line script run under a timeout.
4. **Page text an agent reads is untrusted.** One vendor pricing page (Linear) contained instructions addressed to AI agents. A community Fab MCP has an "accept EULA" parameter that would let an agent accept licence terms on a person's behalf. Do not allow either.
5. **Licences and terms catch students.** Houdini Apprentice and Cascadeur Free are non-commercial. Aseprite's source licence lets you build it for yourself but not redistribute builds. Freesound's API is free for non-commercial use only. Meshy Free outputs are CC BY 4.0 and Free has no API. Midjourney, Suno and Udio have no workable agent route. Steam asks developers to disclose AI-generated content that ships to players.
6. **Several things changed in 2026**, so re-check before depending on them: Gemini CLI stopped serving individual accounts on 2026-06-18; Windsurf is now Devin Desktop; Audacity 4 removed the scripting pipe every Audacity MCP server used (2026-09-03); GodotSteam's repository moved to Codeberg; Notion's open-source MCP server is deprecated; Blender 5.0 removed Collada; Godot's contribution policy (2026-06-30) restricts AI-written code in contributions to the engine itself, not in games made with it.

**What it did not do.** Nothing was installed or run. The five area files were written by separate research agents from official pages, repositories and the GitHub API read on 2026-11-03; where a page blocked automated fetching (Epic, Adobe, Autodesk, Audiokinetic and others) the claim is marked REPORTED or UNVERIFIED in the text. About 260 claims across the files are marked UNVERIFIED. I (Claude) checked these headline claims again against separate sources: the Gemini CLI change (Google's own GitHub discussion), the Unreal 5.8 MCP plugin and its experimental label, the Blender Lab server and its 5.1 requirement, and that Unity's own blog says its MCP server needs a subscription or trial (forum posts disagree; Unity's pages conflict). I did not read Godot's final policy text. Prices are left out on purpose; check current terms before paying.

---

## How to judge a tool for agentic work: six questions

1. **Is the project plain text and diffable?** Godot .tscn and .gd files, JSON maps, SVG, Lua and Markdown: yes. Binary assets (.uasset, .blend, .psd, .kra): the agent can run a script that changes them but cannot review the change as text.
2. **Is there a command line or headless mode?** This decides whether an agent can build, run and test without a window (`godot --headless`, `blender -b --python`, `aseprite -b`, `ffmpeg`).
3. **Can a script do everything the GUI does?** Blender's bpy and Aseprite's Lua can. Many tools expose only a slice.
4. **Is there an MCP server, and who made it?** Official, maintained, narrow scope is best. Community, young, arbitrary-code tools need care. No MCP is fine if the CLI is good.
5. **Can the agent check its own work?** A headless test, a log, an exported image to compare. Exit code 0 is a claim, not evidence (Unity's test runner has no defined exit codes, GUT ignores pending tests, Godot ignores unknown flags). Look, feel and sound stay human checks.
6. **Are the cost and terms workable?** Free for commercial use? Open source or source-available? Does the licence or the platform restrict automation or AI-generated output?

## What this means for the course

- **Why Godot.** It is the best engine that also has an editor: MIT licence, no licence server, text scenes, a documented headless CLI, test frameworks, and many MCP servers (none official). Bevy, three.js, Babylon.js, Phaser and LOVE are even easier for an agent (code only, no editor) but have no editor workflow for designers.
- **Unity and Unreal are the comparison.** Unity has strong first-party agent tooling, but it is in beta and needs a running licensed Editor. Unreal is operable but binary, and its MCP plugin is experimental.
- **Suggested default stack (my suggestion from the ratings, not a course decision).** Godot with GUT or GdUnit4; Blender driven by script (the official Blender Lab server is available if you accept its caution); Aseprite or Pixelorama for pixel art; Tiled or LDtk for maps; Material Maker for textures; FFmpeg and jsfxr for sound; Git with GitHub Actions; Claude Code or Codex. Know the rest exist and know their limits.
- **Record provenance.** For every downloaded or generated asset, write down the source, licence and what attribution is required. The "Asset licence ledger" section of the audio and assets file lists what to record.

---

## The toolkit at a glance

The tables use the same columns throughout. "Agent route" says how an agent reaches the tool (CLI, API, MCP, files). "Agent-friendliness" is the researcher's rating: High means an agent can drive and verify it end to end with little help, Low means GUI-only or no workable route. Each tool's pros, cons, sources and UNVERIFIED flags are in its entry in the detail file.

### Game engines and frameworks (detail: [01-engines.md](01-engines.md)): 17 tools

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

### 3D, 2D art, textures, animation and level design (detail: [02-art-3d-animation-levels.md](02-art-3d-animation-levels.md)): 26 tools

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

### Audio, asset sources and design tools (detail: [03-audio-assets-design.md](03-audio-assets-design.md)): 21 tools

| Tool | Cost | Open source | Extendable | Agent route | Agent-friendliness |
|---|---|---|---|---|---|
| FMOD Studio | Free Indie tier (budget < $600k, revenue < $200k); credit line and logo required | No | JavaScript scripting; plug-in SDK (UNVERIFIED) | MCP (community, alpha), scripting API, CLI (flags UNVERIFIED) | Medium |
| Wwise | Free Indie plan reported (budget < $250K); trial capped | No | WAAPI, C++ plug-ins (UNVERIFIED) | CLI (WwiseConsole), API (WAAPI), MCP (community) | Medium |
| Audacity | Free | Yes (GPLv3) | Nyquist; scripting pipe in 3.x only | MCP (community, 3.x), none in 4.x | Low |
| REAPER | Paid, 60-day trial, discounted tier | No | ReaScript (EEL2/Lua/Python), JSFX, C++ | CLI, API, MCP (community) | Medium |
| LMMS | Free | Yes (GPL-2.0) | C++ plug-ins | CLI (render), MCP (tiny) | Medium |
| jsfxr / Bfxr | Free | Yes (Unlicense / MIT) | JS library | CLI, API (Node) | High |
| FFmpeg | Free | Yes (LGPL-2.1+/GPL) | Filters, libav* | CLI | High |
| SoX | Free | Yes (GPL-2.0+/LGPL) | Effects chains, libsox | CLI | Medium |
| Fab | Free and paid; tiered licence | No | Plug-ins for Unreal/Unity | none official (community MCP) | Low |
| Unity Asset Store | Free and paid; EULA | No | n/a | none (Editor-based) | Low |
| Godot Asset Library / Asset Store | Free; open-source licences | Library yes; Store code private | GDScript/C# add-ons; REST API | Git clone (no CLI) | Medium |
| itch.io asset packs | Free to paid; per-pack licence | No | butler (publishing) | API (no file download) | Low |
| Kenney | Free (CC0) | n/a (CC0 assets) | n/a | none (manual download) | Medium |
| OpenGameArt | Free; per-item licence | n/a | n/a | none | Low |
| Sketchfab | Free CC downloads; per-user OAuth | No | Data and Download APIs | API (OAuth), MCP (community) | Medium |
| Poly Haven | Free (CC0) | Assets CC0; API repo AGPL-3.0 | JSON API | API (keyless) | High |
| Freesound | Free; CC0/CC-BY/NC mix; API non-commercial | No | REST API v2 | API (token + OAuth2), MCP (community) | Medium |
| Figma | Free Starter; paid seats; free Education | No | Plugin API, REST API, MCP | MCP (official), API | High |
| Inkscape | Free | Yes (GPL) | Python extensions | CLI, MCP (community) | High |
| Excalidraw | Free | Yes (MIT) | React component | MCP (official) | Medium |
| Miro | Free tier + subscription | No | REST API/SDK (UNVERIFIED) | MCP (official) | Medium |

### Workflow infrastructure: editors, version control, CI, testing, profiling, project management, storefronts, backend (detail: [04-workflow-infrastructure.md](04-workflow-infrastructure.md)): 41 tools

| Tool | Cost | Open source | Extendable | Agent route | Agent-friendliness |
|---|---|---|---|---|---|
| Visual Studio Code | Free | Source MIT, binary Microsoft | Extensions | CLI / MCP (client) / API | High |
| JetBrains Rider | Paid; free non-commercial | No (Godot plugins open) | Plugins | MCP (built in) | Medium |
| Visual Studio (Community) | Free with limits | No | VSIX | MCP (client, Copilot only) | Medium |
| Neovim | Free | Yes (Apache 2.0 / Vim) | Lua, RPC | CLI / API | Medium |
| Zed | Free; paid Pro for hosted AI | Yes (GPL-3 / Apache) | Extensions | ACP / MCP | Medium |
| Godot editor and CLI | Free | Yes (MIT) | Plugins, GDExtension, source | CLI / API / MCP (community) | High |
| Git + Git LFS | Free software; hosting quota | Yes (LFS MIT) | Hooks, filters | CLI / MCP (GitHub) | High |
| Perforce Helix Core | Free to 5 users; paid | No | CLI, API | CLI / MCP (community-supported) | Medium |
| Unity Version Control | Metered cloud storage | No | CLI, plug-ins | CLI | Medium |
| Diversion | Free Indie tier; paid | No (UNVERIFIED) | CLI, REST API | CLI / API / Claude plugin | Medium |
| GitHub Actions | Free public; metered private | No | Actions, runners | CLI / API / MCP | High |
| GameCI | Free (needs Unity licence) | Yes (MIT) | Actions, Docker | CI actions | Medium |
| Jenkins | Free (self-host) | Yes (MIT) | Plugins | CLI / API / MCP (plugin) | Medium |
| Godot export in CI | Free | Yes (MIT) | Shell, presets | CLI | High |
| GUT | Free | Yes (MIT) | GDScript | CLI | High |
| GdUnit4 | Free | Yes (MIT) | GDScript, C#, Action | CLI | High |
| Unity Test Framework | Included with Unity | Package unchecked | NUnit | CLI | High |
| Unreal Automation / Gauntlet | Included with Unreal | Source-available (UNVERIFIED) | C++, C# | CLI | Medium |
| RenderDoc | Free | Yes (MIT) | Python API | API / MCP (community) | Medium |
| PIX | Free (terms unread) | No | Event markers | CLI | Medium |
| Tracy | Free | Yes (BSD-3) | Instrumentation | CLI (capture, export) | Medium |
| Superluminal | Paid (EUR) | No | PerformanceAPI | CLI / MCP (official) | Medium |
| Unity Profiler | Included with Unity | No | Markers, modules | CLI flags | Medium |
| Unreal Insights | Included with Unreal | Source-available (UNVERIFIED) | Trace macros | CLI (reported unreliable) | Low |
| Godot profiler / monitors | Free | Yes (MIT) | Custom monitors | CLI flags / script API | Medium |
| GitHub Issues and Projects | Included with GitHub | No | GraphQL API, Actions | CLI / API / MCP | High |
| Linear | Free tier; paid | No | API, integrations | MCP (official) | High |
| Jira | Free to 10 users (reported); paid | No | REST API, Forge | MCP (official) | Medium |
| Trello | Free tier; paid | No | REST API | MCP (official) | Medium |
| Notion | Free tier; paid | No (MCP server deprecated) | API, MCP | MCP (official) | Medium |
| Obsidian | Free; optional paid add-ons | No (UNVERIFIED) | Plugins | Files / CLI / MCP (community) | High |
| Steam and Steamworks | USD 100 per app plus revenue share | No (GodotSteam MIT) | Steamworks API | CLI (SteamCMD, reported) / MCP (tiny community) | Medium |
| itch.io and butler | Free to list; chosen share | butler MIT | butler, API | CLI | High |
| Epic Games Store | Revenue share (reported); EOS free | No | EOS SDK | CLI (BPT) | Medium |
| Mobile stores | USD 99 per year (Apple); USD 25 once (Google) | fastlane MIT | APIs, fastlane | CLI / API | Medium |
| Consoles (overview) | Contracts, NDAs | No | NDA SDKs | none public | Low |
| Nakama | Free self-host; managed by quote | Yes (Apache-2.0) | Go, Lua, TypeScript | CLI / API / MCP (community) | High |
| Photon | Free dev tier; paid | No | SDKs | none found | Low |
| PlayFab | Free dev tier; paid (reported) | No | REST, SDKs | API / MCP (community) | Medium |
| Steam networking | Part of Steamworks | GameNetworkingSockets BSD-3 | Steamworks API | none | Low |
| GameAnalytics | Free tier; paid | SDK MIT, service no | SDKs, API | MCP (official) | High |

### Coding agents and AI generation tools (detail: [05-agents-and-ai-tools.md](05-agents-and-ai-tools.md)): 25 tools

| Tool | Cost | Open source | Extendable | Agent route | Agent-friendliness |
|---|---|---|---|---|---|
| Claude Code | Subscription or API tokens; no free plan | No (all rights reserved) | CLAUDE.md, skills, hooks, MCP, SDK | CLI (`-p`), MCP client, SDK | High |
| OpenAI Codex | In ChatGPT plans (limited Free) or API key | Yes (Apache-2.0) | AGENTS.md, MCP, GitHub Action | CLI (`codex exec`), MCP client | High |
| Cursor | Free tier; usage-pool subscriptions | No (UNVERIFIED) | Rules, AGENTS.md, MCP, hooks | CLI (`agent -p`), MCP client | Medium |
| GitHub Copilot | Free tier; credit-based paid plans | No (restrictive CLI licence) | Instruction files, MCP, custom agents | IDE agent, CLI, cloud agent, MCP client | Medium |
| Gemini CLI | Free individual access ended 2026-06-18; paid API key | Yes (Apache-2.0) | GEMINI.md, MCP, extensions | CLI (`gemini -p`), MCP client | Medium |
| Windsurf (Devin Desktop) | Free tier; quota plans | No (UNVERIFIED) | MCP, rules, AGENTS.md | IDE agent, MCP client; headless UNVERIFIED | Medium |
| Cline | Free software; bring your own key | Yes (Apache-2.0) | .clinerules, skills, MCP, SDK | CLI (headless), MCP client | High |
| Aider | Free software; bring your own key | Yes (Apache-2.0) | CONVENTIONS.md | CLI (`--message`) | Medium |
| JetBrains Junie | Free option plus credit tiers; BYOK | No (all rights reserved) | Guidelines, skills, MCP | CLI, CI, MCP client | Medium |
| Midjourney | Subscription; no confirmed free tier | No | None found | none (no official API) | Low |
| Adobe Firefly | Free daily generations; paid credits | No | Firefly API | API; hosted Adobe connector (REPORTED) | Medium |
| Stable Diffusion / ComfyUI | Free; revenue cap $1M on Stability models | ComfyUI yes (GPL-3.0); weights vary | Custom nodes, workflows, API | HTTP API, comfy-cli, MCP | High |
| Scenario | 50 free daily credits; paid plans | No (skills MIT) | REST API, SDKs, custom models | API, MCP | High |
| Layer | Usage-based credits; free allowance unstated | No | REST API, SDK, CLI, plugins | API, CLI, MCP (unverified repo) | Medium |
| Meshy | Free 100 credits/month (CC BY 4.0); API paid | No (MCP MIT) | REST API, plugins | API, MCP, skill pack | High |
| Tripo | API credits; free web tier reported non-commercial | No (MCP MIT) | REST API, Blender add-on | API, CLI, MCP (stale) | Medium |
| Hyper3D Rodin | 7-day trial and free credits; credits | No | HTTP API, Blender add-on | API, MCP (via Blender MCP) | Medium |
| Luma AI | Pay-per-use API | No | REST API (image and video) | API only | Medium |
| ElevenLabs | Free 10,000 credits/month, no commercial licence on Free | No (MCP MIT, archived) | API, SDKs, CLI | API, CLI, hosted MCP | High |
| Suno | Free 50 credits/day, no commercial rights | No | None public | none (no public API) | Low |
| Udio | Unknown; downloads reported disabled | No | None found | none | Low |
| Stable Audio | Open weights (Community License); API | Partly | Local weights, Stability API | API | Medium |
| Runway | Free 125 one-time credits, watermark; paid | No | REST API, SDKs | API, MCP/plugin | High |
| Higgsfield | Paid plan for MCP; free credits unstated | No | Hosted MCP, CLI | MCP, CLI | Medium |
| Inworld | Free On-Demand with commercial licence | No | API, CLI, skill | API, CLI | Medium |

---

## Where the details are

| File | Covers |
|---|---|
| [01-engines.md](01-engines.md) | Godot, Unity, Unreal, Bevy, GameMaker, Defold, Cocos Creator, O3DE, Stride, Flax, LOVE, Phaser, PlayCanvas, Babylon.js, three.js, Construct, RPG Maker; MCP server tables for the big three |
| [02-art-3d-animation-levels.md](02-art-3d-animation-levels.md) | Blender (headless recipes, MCP comparison, formats), Maya, 3ds Max, Houdini, ZBrush, Cinema 4D, MagicaVoxel, Aseprite, Krita, GIMP, Photoshop, Inkscape, Pixelorama, LibreSprite, Substance, Material Maker, ArmorPaint, Spine, Mixamo, Cascadeur, Rokoko, FreeMoCap, Tiled, LDtk, TrenchBroom |
| [03-audio-assets-design.md](03-audio-assets-design.md) | FMOD, Wwise, Audacity, REAPER, LMMS, jsfxr, FFmpeg, SoX; asset sources and the licence ledger; Figma, Inkscape, Excalidraw, Miro |
| [04-workflow-infrastructure.md](04-workflow-infrastructure.md) | Editors and IDEs, version control, CI, test frameworks, profiling, project management and design docs, storefronts, networking, backend and analytics |
| [05-agents-and-ai-tools.md](05-agents-and-ai-tools.md) | Nine coding agents, AI image, 3D, audio, music and video tools, about 38 game-tool MCP servers compared, AI-asset platform and copyright rules |

Every entry has the same shape: what it is, cost, open source, extendable, agent integration, pros and cons for agentic work, a verdict, and sources marked VERIFIED, REPORTED or UNVERIFIED.
