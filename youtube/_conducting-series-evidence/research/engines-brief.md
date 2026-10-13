# Engines brief for "Why Godot" (film 2 of 3) — researched 2026-10-09

## Executive summary (what / why / found)

Bear's premise is PARTLY true. Godot is a very good fit for conducting AI because its project files are plain text and its CLI is complete. But "Unity and Unreal MCP are raw and catching up" is out of date, and "Godot has the better MCP story" is not supported.

- Godot has NO official MCP server or AI integration. Every Godot MCP is community. The best-known one (Coding-Solo/godot-mcp, ~6k stars) was last pushed 2026-04-16.
- Unity has an OFFICIAL MCP server, public since 2026-03-03 and in open beta since May 2026. Epic ships an OFFICIAL "Unreal MCP" plugin in UE 5.8 (2026-06-17), labelled Experimental. Both are first-party and both are labelled beta/experimental. "Raw" fits the labels; "behind Godot" does not.
- Unity's community MCP (CoplayDev/unity-mcp) has ~14.8k stars, more than double Godot's top MCP.
- Godot's real advantages are structural: MIT licence, no vendor account, tiny download, text scenes, full headless CLI.
- Godot's own policy on AI-written contributions to the engine is hostile (autonomous agents get auto-banned). That concerns contributing TO Godot, not using AI to make games WITH Godot. The film should not blur the two.
- Text readability: Godot and Unity (default Force Text mode) are both text. Only Unreal is binary.

Safe framing for the film: "Godot is the engine whose files an agent can read and write directly, with no vendor gate. Unity and Unreal now have official MCP, still labelled beta/experimental."

---

## A. GODOT

| Claim | Verdict | Source / date / short quote |
|---|---|---|
| Licence is MIT | VERIFIED | godotengine.org/license (undated; footer credits 2007–2026): "Copyright (c) 2014-present Godot Engine contributors." Page names MIT/Expat. https://godotengine.org/license/ . Docs: "completely free and open source under the permissive MIT license" https://docs.godotengine.org/en/stable/about/introduction.html . GitHub API 2026-10-09: godotengine/godot, MIT, ~118k stars. |
| Owned by the Godot Foundation (non-profit) | PARTLY TRUE, correct it | The Foundation does NOT own the engine. It is a Dutch non-profit (Stichting Godot, formed Aug 2022) that holds the trademarks, contracts and bank account. https://godotengine.org/governance/ (undated): "Godot can't be sold or purchased by any company." Same page: copyright "held collectively by every contributor." https://godot.foundation/ (undated) calls it a "Dutch non-profit organization" and "legally independent." Trademark owner: https://godot.foundation/policies-and-procedures/trademark-policy . Say "stewarded by a non-profit," not "owned by." |
| Current stable | VERIFIED: 4.7.2, released 18 Aug 2026 | https://godotengine.org/download/macos/ (fetched 2026-10-09): lists 4.7.2, 18 August 2026. Release list https://godotengine.org/blog/release/ : 4.7.2 (18 Aug), 4.7.1 (14 Jul), "Godot 4.7 – Lights, Camera, Action!" (18 Jun 2026). Archive https://godotengine.org/download/archive/ : newest dev snapshot is 4.8-dev7 (29 Sep 2026), no 4.8 beta/RC yet, so 4.7.2 is current stable. GitHub release 4.7.2-stable published 2026-08-18T16:12Z. A 3.6.3 maintenance release (22 Aug) also exists; ignore it, 3.x is legacy. |
| Download size | VERIFIED via GitHub API (godotengine/godot release 4.7.2-stable, assets, 2026-10-09) | Editor zips: Windows x64 86.0 MB; Linux x86_64 77.9 MB; macOS universal 170.6 MB. .NET (C#) builds: Windows x64 116.6 MB; Linux x86_64 107.7 MB; macOS universal 200.8 MB. Export templates are separate: 1,281 MB (standard) / 1,203 MB (.NET). So "under ~200 MB for the editor, single executable, no installer" is accurate; "full toolchain including export templates" is over 1 GB. The download page itself shows no sizes. |
| GDScript and C# | VERIFIED | https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html : "GDScript is a high-level, object-oriented, imperative, and gradually typed programming language built for Godot." The intro page shows the same example in GDScript and C#. C# needs the separate .NET build (above). |
| Scenes/resources are plain text | VERIFIED for .tscn/.tres | https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html (undated): TSCN is "mostly human-readable and easy for version control systems to manage." The page is written for text .tres and mentions .tres comments. Docs also note binary formats load faster, so text is a choice, not a limit. .gd scripts are plain text. project.godot: I could NOT confirm in the docs pages fetched that it is a text/INI-style file (only that override.cfg is "in the same format as project.godot"). It is widely known to be an INI-like ConfigFile; confirm by opening one on camera before stating it. |
| What text means for an agent | REASONING (mine, not a source) | An agent can read a scene with an ordinary file read and write it with an ordinary edit. Diffs are line-level, and git history shows what the agent changed. No bridge is required for basic work, and an MCP server is an optional extra. Caveats: scene files carry uid:// and ext_resource IDs the agent must keep consistent; the docs' "UID" handling is why Coding-Solo's MCP has get_uid and update_project_uids tools. Run `--import` after adding assets. |
| Headless/CLI | VERIFIED | https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html (undated). `--headless`: "Useful for servers and with `--script`." (equivalent to `--display-driver headless --audio-driver Dummy`). `--script <script>` runs a script. `--import` opens the editor, waits for resources to import, then quits. `--export-release <preset> <path>`, `--export-debug <preset> <path>` (implies `--import`), `--export-pack`. `--check-only` parses a script for errors and quits (with `--script`), which is a handy agent lint step. `--quit` exits after the first iteration. |
| Official MCP / AI integration | NOT FOUND, so Bear's premise needs care | No Godot Foundation or godotengine.org announcement of an MCP server or AI assistant. The Godot 4.7 release page (https://godotengine.org/releases/4.7/, fetched 2026-10-09, undated; the blog list dates 4.7 on 18 Jun 2026) does not mention AI, MCP, agents or headless. Every Godot MCP is community-made (below). |
| Godot's AI policy | VERIFIED, with timing caveat | Primary: Godot Foundation post "Changes to our Contribution Policies," 30 Jun 2026, https://godotengine.org/article/contribution-policy-2026/ . "We require all code to be human authored." "This already leads to an auto-ban from our GitHub repository." (autonomous agents and vibe coding). Disclosure rule: "you must disclose it in the PR discussion." AI-written human-to-human text is not allowed. Minor help (code completion, regex, find-and-replace) is permitted with disclosure. Per the post, the AI rules were to be added to the contributing policy "Shortly," so the written rules may not be fully in force; the auto-ban of autonomous agents is described as already enforced. Press: https://www.gamedeveloper.com/business/godot-to-ban-almost-all-ai-coding-contributions (1 Jul 2026). Applies to contributions to the ENGINE, not to games made with it. |

### Godot MCP servers and AI tools (all COMMUNITY, none official). GitHub API figures from 2026-10-09.

| Name | Maintainer | Stars | Licence | Last push | Notes |
|---|---|---|---|---|---|
| Coding-Solo/godot-mcp | Coding-Solo (independent) | ~6.0k | MIT | 2026-04-16 | Oldest and best known. Tools per README sample config: launch_editor, run_project, get_debug_output, stop_project, get_godot_version, list_projects, get_project_info, create_scene, add_node, load_sprite, export_mesh_library, save_scene, get_uid, update_project_uids. Description: "MCP server for interfacing with Godot game engine." No GitHub releases listed. Not updated in ~6 months, so ask whether it works with 4.7 before recommending. https://github.com/Coding-Solo/godot-mcp |
| hi-godot/godot-ai | hi-godot org (individual not named) | ~2.9k | MIT | 2026-10-09 | "Production-grade MCP server and AI tools for the Godot engine." 46 tools / 120+ operations. Editor plugin (addons/godot_ai) plus a Python server (uv). Needs Godot 4.7+ for v4. Very active. https://github.com/hi-godot/godot-ai |
| yurineko73/Godot-MCP-Native | yurineko73 | ~836 | MIT | 2026-08-03 | MCP server implemented natively inside the editor plugin; says it is not officially affiliated with Godot or Anthropic (per search snippet). |
| youichi-uda/godot-mcp-pro | youichi-uda | ~620 | NOASSERTION (likely commercial) | 2026-09-24 | "162 MCP tools." |
| tugcantopaloglu/godot-mcp | tugcantopaloglu | ~474 | MIT | 2026-10-09 | 157 tools, GDScript and C#. |
| IvanMurzak/Godot-MCP | IvanMurzak | ~275 | Apache-2.0 | 2026-10-09 | Needs .NET edition; uses a hosted backend or self-hosted server. |
| HaD0Yun/Doyunha-Gopeak | HaD0Yun | ~267 | MIT | 2026-09-12 | "95+ tools," GDScript LSP and DAP. |
| fennaraOfficial/fennara-godot-ai | Fennara | ~303 | MIT | 2026-10-09 | In-editor chat plus MCP. |

Source for all rows: GitHub search API, `q=godot mcp`, 2026-10-09. Star counts are live GitHub figures; the Coding-Solo repo page itself says 6.0k stars, 480 forks. The Asset Library also lists several (e.g. https://godotengine.org/asset-library/asset/5245), which is a user-submission catalogue and carries no endorsement.

---

## B. UNITY

| Claim | Verdict | Source / date / quote |
|---|---|---|
| Has an OFFICIAL MCP server | YES (first-party) | Unity blog "Unity AI Open Beta: How to get started with MCP," 11 May 2026, https://unity.com/blog/unity-ai-mcp-how-to-get-started : "Unity's AI tools are currently in open beta." Features "may change, be limited, or be discontinued without notice." Docs: https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/manual/unity-mcp-overview.html (Unity Editor exposed to agents via a relay binary + local IPC bridge). |
| Status | OPEN BETA / pre-release, not "raw" | Package com.unity.ai.assistant. Changelog https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/changelog/CHANGELOG.html : "Made MCP tools and APIs public" in 2.0.0-pre.1, 2026-03-03. Every version listed there carries a "pre" tag (1.0.0-pre.1 on 2025-04-11 up to 2.0.0-pre.1). Docs header for the newest manual I fetched reads 2.11.0-pre.2 (2.11 manual: https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.11/manual/integration/mcp-overview.html). Product page https://unity.com/features/ai headline: "Start building with Unity's AI tools in beta." I found NO report of general availability as of 2026-10-09. |
| Requirements | VERIFIED | Blog, 11 May 2026: "Unity 6 (6000.0) or later with the AI Assistant package installed"; a Unity Cloud-connected project; an MCP client (Claude Code, Cursor, Windsurf, Claude Desktop, VS Code Copilot). |
| Tools exposed | VERIFIED | Docs: built-in tools "cover scene management, asset operations, script editing, and console access" (paraphrase); custom tools can be registered in C#. Blog adds GameObject inspection and build settings. |
| Muse / Assistant history | Partly | https://unity.com/features/ai (undated): Unity Muse is "a deprecated product offering"; Sentis "remains active" as the runtime inference engine. Assistant changelog starts 2025-04-11 (1.0.0-pre.1). Another page says Muse and Sentis sunset on Unity AI GA; the Muse sunset wording on the activation page conflicts with the features page on Sentis, so quote only the features page. |
| Cost | CONFLICTING between Unity pages | Blog (11 May 2026): the server requires "a Unity subscription" and "An active trial or subscription to Unity's AI tools beta" but consumes no AI credits. Features page: the CLI, MCP server and official plugin are "all free to use with no concurrency limits," and the in-editor assistant (credits) is included for Pro/Enterprise/Industry, with Personal on a free trial that converts to $10/month. Use "free to use, subscription/trial gating has been inconsistent in Unity's own pages" or check Unity's page again on the day of recording. |
| Text-readable projects | VERIFIED, with a default | Scenes: https://docs.unity3d.com/Manual/FormatDescription.html : "Unity's Scene format uses a custom subset of the YAML data serialization language." Setting: https://docs.unity3d.com/Manual/class-EditorManager.html : Asset Serialization "Force Text (default)"; Mixed and Force Binary exist. .meta files: https://docs.unity3d.com/Manual/AssetMetadata.html says each holds "the unique ID assigned to the asset" and import settings and "must stay with the asset"; that page does NOT say .meta is text (it is YAML in practice; not confirmed from docs). Caveat from me: Unity YAML is text but hard for agents to edit (many fileIDs/GUID cross-references), which is why agents lean on the Editor bridge. |
| Headless CLI | VERIFIED | https://docs.unity3d.com/Manual/EditorCommandLineArguments.html : `-batchmode` ("Run Unity in batch mode."), `-quit`, `-executeMethod`, `-nographics`, `-projectPath`, `-buildTarget`. Needs a licensed/activated Editor. |
| Licence / price | VERIFIED, relevant | Proprietary. https://unity.com/products/unity-personal : free Personal for "less than $200K USD of revenue and funds raised in the last 12 months." No runtime fee on that page. Needs a Unity account and the Hub to install. |
| Community MCP | for contrast | CoplayDev/unity-mcp (MIT, ~14.8k stars, pushed 2026-10-08); IvanMurzak/Unity-MCP (Apache-2.0, ~4.4k); CoderGamester/mcp-unity (MIT, ~1.9k). GitHub API 2026-10-09. Unity's community MCP ecosystem is larger than Godot's by star count. |

Verdict on "Unity's MCP is raw": there is an official server, first public in March 2026, in open beta. "Open beta, features may change" is accurate. Calling it "raw" is a fair opinion, not a sourced fact.

---

## C. UNREAL ENGINE

| Claim | Verdict | Source / date / quote |
|---|---|---|
| Official MCP | YES, first-party, EXPERIMENTAL | UE 5.8 release notes, https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes : listed under "MCP Server (Experimental)"; "a new experimental MCP (Model Context Protocol) plugin for the Unreal Editor." UE 5.8 released 17 Jun 2026 at State of Unreal, Chicago (https://wnhub.io/news/engines/item-51157 , secondary; Puget Systems 2026-07-09 also confirms 5.8). |
| Docs and maturity | VERIFIED | https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor (UE 5.8 docs; undated): Marked Experimental. "Many features are incomplete or missing." APIs and data formats "may change at any time." Local HTTP server (default http://127.0.0.1:8000/mcp), no authentication, loopback-only; HTTP/SSE only, no stdio/WebSocket. Needs the "Unreal MCP" and "All Toolsets" plugins. `ModelContextProtocol.GenerateClientConfig` writes configs for ClaudeCode, Cursor, VSCode, Gemini, Codex. Toolsets can be written in C++ or Python. Tool calls run serially on the game thread. Flag `-ModelContextProtocolStartServer` starts it during editor or commandlet startup. |
| Real-world test | Secondary | Puget Systems, 9 Jul 2026, https://www.pugetsystems.com/blog/2026/07/09/unreal-engine-mcp-hands-on-testing-ai-inside-the-editor/ : Epic labels it experimental; the author calls Epic's docs "a bit lacking." |
| Epic's direction | VERIFIED (secondary) | Edge, 19 Jun 2026 https://knowledge.edge-online.com/p/ai-goes-native-in-unreal-engine-the-five-main-takeaways-from-state-of-unreal-2026 : MCP plugin ships in 5.8; Epic says AI will be built into UE6 from the start. Same article claims UE6 will largely replace C++ with Verse and early access "late next year"; treat as press, not Epic text. Epic's own news page returned 403, so I could not read Epic's announcement. |
| Python scripting | VERIFIED, Experimental | https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python : editor-only (not gameplay, not cooked builds), embeds Python 3.11.8; headless via commandlet `-run=pythonscript -script=...`; page labels it Experimental. |
| Project text-readability | NOT text | Assets (.uasset/.umap) are binary. Epic UE 4.26 Perforce docs (old, https://docs.unrealengine.com/4.26/en-US/ProductionPipelines/SourceControl/Perforce ): "These files are binary, so cannot be opened as text or merged in a text-based merge tool." I found no current Epic page that says otherwise. Config files (.ini) and C++ source are text, so an agent can edit code, but Blueprints and levels need the MCP or Python tools. |
| Size | Weakly sourced | No Epic figure found. Forum thread https://forums.unrealengine.com/t/storage-required-to-install-unreal-engine-5-8-1/2740177 (Aug 2026): a user reports a 39 GB source zip for 5.8.1 and about 70 GB used once extracted; a reply advises 150–200 GB free. Italian tutorial says over 100 GB with all platforms (low-quality source). Say "tens of gigabytes, 100+ GB with a full install," not an exact number. Read the figure in the Epic Launcher on camera if you want one. |
| Licence / cost | VERIFIED, secondary | Epic license page returned 403 to my fetch. Search results restate Epic's terms: free until a product passes $1M lifetime gross revenue, then 5% above that; free for educators. Sources: https://www.unrealengine.com/en-US/license , https://www.unrealengine.com/en-US/faq . Confirm the numbers on Epic's page before the film. Source code on GitHub is available under the EULA, not an open-source licence. |
| Community MCP | for contrast | chongdashu/unreal-mcp (~2.1k stars, last push 2025-04-22, stale); ChiR24/Unreal_mcp (MIT, ~911, pushed 2026-10-09); kevinpbuckley/VibeUE (MIT, ~728). GitHub API 2026-10-09. |

Verdict on "Unreal's MCP is raw": Epic's own docs say experimental, incomplete, APIs may change. That is sourced. But it is a first-party plugin that ships with the engine, not a community add-on.

---

## D. BLENDER MCP (one line)

There are TWO things with this name. Official: "Blender Lab" MCP Server (blender.org/lab/mcp-server; needs Blender 5.1+; add-on + MCP server; lets an LLM use Blender's Python API and docs; the page warns it can "execute LLM generated code in Blender without any guards in place"; I could not find a dated announcement on blender.org; a secondary blog dates v1.0.0 to 27 Apr 2026). Source: https://www.blender.org/lab/mcp-server/ . Community: ahujasid/blender-mcp, ~30.3k stars, MIT, "Community plugin to control Blender 3D with any LLM of your choice," "Not affiliated with the official Blender Foundation," https://github.com/ahujasid/blender-mcp . The community one is the famous one. Say which one the film shows.

---

## Comparison table

| | Godot 4.7.2 | Unity 6 (Unity AI) | Unreal Engine 5.8 |
|---|---|---|---|
| Agent-readable project format | Text: .tscn, .tres, .gd; project.godot not confirmed in docs (docs: TSCN "mostly human-readable", https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) | Text by default (YAML scenes; Force Text is the default) but cross-reference-heavy (https://docs.unity3d.com/Manual/FormatDescription.html , https://docs.unity3d.com/Manual/class-EditorManager.html) | Binary .uasset/.umap (Epic UE 4.26 doc, old; no newer page found); C++ and .ini are text |
| Headless CLI | Yes: `--headless`, `--script`, `--import`, `--export-release` (https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) | Yes: `-batchmode -quit -executeMethod` (https://docs.unity3d.com/Manual/EditorCommandLineArguments.html) | Yes: commandlet `-run=pythonscript`, Python is Experimental (https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) |
| MCP status | No official MCP; community only (Coding-Solo ~6k stars, hi-godot/godot-ai ~2.9k; GitHub API 2026-10-09) | Official, open beta since May 2026, public since 2026-03-03 (https://unity.com/blog/unity-ai-mcp-how-to-get-started , changelog) | Official, "Experimental," shipped with 5.8 on 2026-06-17 (https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor) |
| Licence / cost | MIT, free, no account (https://godotengine.org/license/) | Proprietary; Personal free under $200K revenue (https://unity.com/products/unity-personal); AI tools gated by trial/subscription per May blog, free per features page | Proprietary; free until $1M then 5% (secondary: https://www.unrealengine.com/en-US/faq ; Epic license page returned 403) |
| Size | Editor 78–171 MB (200 MB for .NET build); templates +1.2 GB (GitHub release 4.7.2-stable, API 2026-10-09) | Not verified; Hub plus Editor install, not measured | Tens of GB; ~70 GB extracted source per one forum user (https://forums.unrealengine.com/t/storage-required-to-install-unreal-engine-5-8-1/2740177) |

---

## Items that contradict or weaken Bear's premise

1. Godot has no official MCP or AI integration; Unity and Unreal both do. Godot's "MCP advantage" is a larger menu of community servers, not first-party support.
2. Unity's MCP is first-party, public since 2026-03-03, in open beta with a ~7-month history; "raw" is opinion. Unity's community MCP has more stars than any Godot one.
3. Unreal's MCP is first-party, experimental, shipped 2026-06-17. Epic says UE6 will build AI in from the start, which is the opposite of "catching up and abandoned."
4. The Godot Foundation does not own Godot; it stewards trademarks and money. Copyright belongs to contributors.
5. Godot's flagship community MCP (Coding-Solo) has had no push since 2026-04-16.
6. Godot Foundation policy bans autonomous-agent PRs to the engine (30 Jun 2026). Do not let the film imply Godot welcomes AI agents in its own codebase.
7. Unity scenes are text too (Force Text default). "Text vs binary" separates Unreal from the other two, not Godot from Unity.

## Not verified

- project.godot being plain text (docs fetched don't say it; widely known true).
- Unity .meta files being text (docs page silent).
- Unity install size; exact Unreal install size; Epic's own licence page; Epic's own State of Unreal page (403).
- Whether Unity AI went GA after the May beta; I found no sign as of 2026-10-09.
- Godot Foundation's contribution-policy text has since been added to the written guidelines.
- Dates for the Godot governance/foundation pages (undated).
