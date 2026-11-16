# C2. Development workflow infrastructure (CSYE 7270 toolkit note)
*Part of the game-development toolkit note: see [README.md](README.md). Research date 2026-11-03.*

## Executive summary

**What this is.** Notes on 41 tools a game team uses around the engine: editors and IDEs, version control, CI and builds, test frameworks, profilers, project management and design documents, storefronts, and networking, backend and analytics services. Each entry says what it costs, whether it is open source, how it is extended, and how well a coding agent can use it.

**Why read it.** These are the tools that decide whether an agent's work can be built, tested, shipped and reviewed without a person clicking. Most of the agent-friendly wins are here, and so are the traps.

**What it found.**
- The most agent-friendly tools are command-line and text based: Git with Git LFS, GitHub Actions, Godot export in CI, the GUT and GdUnit4 test frameworks, the Unity Test Framework, itch.io's butler, GitHub Issues, Obsidian, Nakama and VS Code.
- Several official agent routes exist: Superluminal (a documented CLI and MCP route), Linear, Jira, Trello and Notion (hosted MCP servers) and GameAnalytics. Diversion publishes an agent quickstart and a Claude Code plugin. Perforce's MCP server sits in its own GitHub organisation but is labelled "Community Supported". Notion's open-source MCP server is deprecated.
- No workable agent route: consoles, Photon (a preview Godot SDK, dashboard-gated) and Steam networking (needs the Steam client). Unreal Insights is rated Low because its headless export is reported broken on Unreal 5.5 to 5.7.
- Several free tiers and repositories changed in 2026: GodotSteam's GitHub repository was archived on 2026-10-20 and moved to Codeberg, and Unity, Atlassian and GitHub changed storage or pricing rules.
- One vendor page (Linear pricing) contained text addressed to AI agents asking them to connect to its MCP server. The researcher ignored it. Treat page text an agent reads as untrusted input.

**What it did not do.** Nothing was installed or run. About 73 claims are marked UNVERIFIED, mostly because several official pages (Epic, Steam, JetBrains, Unreal licence) returned errors.

---

Researched 2026-11-03. Area: editors and IDEs, version control, CI and build automation, test frameworks, profiling and debugging, project management and design documents, distribution and storefronts, networking, backend and analytics.

Conventions used below:
- "Read today" means I read the number on the vendor page on 2026-11-03. Anything else is "check current terms".
- Repository facts (licence, last push, stars) come from the GitHub API record of the repository, fetched 2026-11-03. "Last push" is the last time anything was pushed to any branch, so it is a rough maintenance signal only.
- VERIFIED = read on an official page or repository during this task. REPORTED = seen only in a secondary source or a search-result snippet. Claims I could not check are marked UNVERIFIED in the text.
- Nothing was installed or run. Page text was treated as data. One vendor page (Linear pricing) contained text addressed to AI agents asking them to connect to its MCP server; I did not act on it.

---

## A. Code editors and IDEs

### Visual Studio Code
**What it is:** Microsoft's free, extensible code editor, and the most common editor for Godot's GDScript outside the Godot editor itself.
**Cost:** Free to download. Source repository is MIT; the shipped product is "a distribution of Code - OSS" under a Microsoft product licence (VERIFIED, README). Whether that licence allows commercial game work was not read (UNVERIFIED; terms at https://code.visualstudio.com/license). Copilot, which powers its built-in agent mode, has its own plans: check current terms.
**Open source:** Source yes (MIT, https://github.com/microsoft/vscode, 194k stars, last push 2026-11-03); the Microsoft-branded binary is not.
**Extendable:** Extension marketplace; forks use Open VSX. Official Godot extension "Godot Tools" (MIT, 2.1k stars, last push 2026-09-10).
**Agent integration:** (a) Plain text. (b) A `code` launcher exists (flags UNVERIFIED). (c) Extension API. (d) VS Code is an MCP client (`mcp.json`, stdio or HTTP); Microsoft warns local servers "can run code on your machine". Claude Code's extension runs a built-in `ide` MCP server on 127.0.0.1 with a per-activation token, exposing `getDiagnostics` from the Problems panel. The Codex IDE extension covers VS Code and forks (REPORTED). (e) Copilot agent mode. (f) Godot Tools surfaces GDScript errors via the Godot language server; `godotTools.lsp.headless` starts a windowless Godot (4.2+). Its debugger is GDScript only.
**Pros for agentic work:**
- First-party extensions for both Claude Code and Codex, with native diff review.
- Diagnostics flow back to the agent without a screenshot.
**Cons for agentic work:**
- MCP servers added here run with your permissions.
- It is a GUI; an agent works the same from a terminal.
**Verdict:** High: first-party extensions for both course agents plus diagnostics sharing.
**Sources:** https://github.com/microsoft/vscode (VERIFIED); https://api.github.com/repos/microsoft/vscode (VERIFIED); https://code.visualstudio.com/docs/copilot/customization/mcp-servers (VERIFIED); https://github.com/godotengine/godot-vscode-plugin (VERIFIED); https://code.claude.com/docs/en/ide-integrations (VERIFIED); Codex IDE extension via search results only (REPORTED).

### JetBrains Rider
**What it is:** JetBrains' cross-platform .NET and game IDE, with first-party support for Unity, Unreal and Godot (GDScript and C#).
**Cost:** Subscription for commercial use; free for non-commercial use since 2024-10-24 (REPORTED: JetBrains blog, which returned 403 to me). JetBrains' guidance, as summarised in search results, is that a product you release for commercial benefit needs a commercial licence (REPORTED). Terms: https://www.jetbrains.com/help/rider/Register.html (not read). Exact prices: check current terms.
**Open source:** No. Two bundled Godot plugins, "Godot Support" and "GdScript", are open source (VERIFIED, Rider docs).
**Extendable:** IntelliJ-platform plugins (UNVERIFIED; not read).
**Agent integration:** (a) Plain text project files. (b) IDE-bound; no headless mode found (UNVERIFIED). (c) Built-in MCP server since 2025.2: read/patch files, search, rename refactor, `get_file_problems`, `build_project`, `execute_run_configuration`, `execute_terminal_command`, git status. Settings, Tools, MCP Server enables it and can auto-write config for Claude Code and Codex. Caution: "brave mode" runs shell commands and run configurations without confirmation; keep it off. (d) Above is official. (e) Junie and AI Assistant (JetBrains' own); Codex reachable via AI Assistant (REPORTED). (f) Godot support includes DAP debugging for GDScript and C#, and gdUnit4Net testing; an agent can build and read problems through MCP.
**Pros for agentic work:**
- IDE-grade diagnostics and refactoring exposed as tools.
- Per-tool switches to disable exposed tools.
**Cons for agentic work:**
- The IDE must be running; heavy for a text-first GDScript course.
- Free licence excludes commercial release.
**Verdict:** Medium: best IDE MCP surface here, but a running GUI app and a licence wall.
**Sources:** https://www.jetbrains.com/help/rider/Godot.html (VERIFIED); https://www.jetbrains.com/help/rider/mcp-server.html (VERIFIED); https://blog.jetbrains.com/blog/2024/10/24/webstorm-and-rider-are-now-free-for-non-commercial-use/ (REPORTED, via search snippet).

### Visual Studio (Community, Windows)
**What it is:** Microsoft's full Windows IDE, used mainly for Unity C# and Unreal C++ work.
**Cost:** Community edition is free for individual developers, classroom learning, academic research and open source. Non-enterprise organisations: up to five users. Enterprises (more than 250 PCs or over USD 1 million revenue) only for open source, research and classroom (VERIFIED, read today at https://visualstudio.microsoft.com/vs/community/). Higher editions are paid (prices not read).
**Open source:** No.
**Extendable:** VSIX extensions (UNVERIFIED; not read).
**Agent integration:** (a) Solution files are XML; code is text. (b) Command-line build via MSBuild (UNVERIFIED; not read). (c) Extensions API. (d) MCP client in VS 2022 17.14+ and VS 2026: `.mcp.json` in the solution or user profile; it also reads `.vscode/mcp.json` and `.cursor/mcp.json`; tools start disabled; tool approvals per session, solution or forever; it resets approvals when a server changes its tool list, to stop "rug-pull" swaps; VS 2026 18.7+ adds trust prompts. (e) GitHub Copilot agent mode, the only agent the docs describe. (f) Debugger and test explorer are GUI; Community page lists Unity and C++. The page does not mention macOS or Linux.
**Pros for agentic work:**
- Strong allow-list and trust controls for MCP.
- Reuses MCP config files from other editors.
**Cons for agentic work:**
- The page read lists Windows targets only; the course machine is a Mac.
- Documented agent path is Copilot only; no Claude Code or Codex integration found (UNVERIFIED).
**Verdict:** Medium: good MCP hygiene, but Copilot-centred and Windows-bound.
**Sources:** https://visualstudio.microsoft.com/vs/community/ (VERIFIED); https://learn.microsoft.com/en-us/visualstudio/ide/mcp-servers (VERIFIED).

### Neovim
**What it is:** A modern fork of Vim, a terminal editor scripted in Lua.
**Cost:** Free.
**Open source:** Yes. Recent contributions are Apache 2.0; code copied from Vim keeps Vim's licence (VERIFIED, README; the API reports NOASSERTION because of the mix). 103k stars, last push 2026-11-03, latest release v0.12.6 (2026-10-09).
**Extendable:** Lua plugins, an RPC API, external UIs.
**Agent integration:** (a) Plain text. (b) `nvim --headless` runs with no UI and is "useful for scripting"; `-l script.lua` runs a Lua file and exits with status 1 on error; `--listen` opens an RPC server (all VERIFIED, runtime docs). (c) RPC API can do what the UI does. (d) No official MCP server checked. Community plugin `coder/claudecode.nvim` ("Claude Code Neovim IDE Extension", MIT, 3.1k stars, last push 2026-11-02) is by Coder, not Anthropic. (e) None built in. (f) Connecting to Godot's language server (port 6005 by default; VERIFIED in Godot docs) needs a manual LSP config; the exact lspconfig entry was not read (UNVERIFIED).
**Pros for agentic work:**
- Fully scriptable from a shell, so an agent can drive it, though it rarely needs to.
- Community Claude Code bridge exists.
**Cons for agentic work:**
- Adds little over a terminal agent plus `git diff`.
- Godot LSP setup is manual; the Godot editor must be running.
**Verdict:** Medium: scriptable and text-native, but a human's editor more than an agent's tool.
**Sources:** https://github.com/neovim/neovim (VERIFIED); https://api.github.com/repos/neovim/neovim (VERIFIED); https://api.github.com/repos/neovim/neovim/releases/latest (VERIFIED); https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/starting.txt (VERIFIED); https://api.github.com/repos/coder/claudecode.nvim (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/editor/external_editor.html (VERIFIED).

### Zed
**What it is:** A fast Rust code editor with a built-in agent panel that can host external agents.
**Cost:** Editor free. Personal plan USD 0 "with your API keys or external agents"; Pro USD 10/month adds hosted-model usage billed beyond USD 5 of tokens (read today at https://zed.dev/pricing). Zed does not charge for External Agents; your Claude or Codex account is billed separately (VERIFIED).
**Open source:** Yes: GPL-3.0-or-later with Apache-2.0 parts (VERIFIED, README). 92k stars, last push 2026-11-03.
**Extendable:** Extensions for languages, themes, MCP servers, debuggers and snippets (VERIFIED).
**Agent integration:** (a) Plain text. (b) Editor has a CLI launcher (UNVERIFIED). (c) Extension API. (d) Zed talks to agents over the Agent Client Protocol (ACP); Claude Agent and Codex install from the ACP Registry; Zed's MCP servers can be forwarded to them. (e) Own agent panel. (f) GDScript support is a community extension (GDQuest repository) that bridges to Godot's language server with netcat on 127.0.0.1:6005 (REPORTED, search result of Zed docs); needs `nc`/`ncat` and a running Godot editor. No debugger for GDScript was checked.
**Pros for agentic work:**
- Cleanest external-agent UI of the lightweight editors.
- Free for course use with your own agent subscription.
**Cons for agentic work:**
- Godot support is community-maintained and needs a netcat shim.
**Verdict:** Medium: excellent agent hosting (ACP), thin Godot support.
**Sources:** https://zed.dev/docs/ai/external-agents (VERIFIED); https://zed.dev/pricing (VERIFIED); https://github.com/zed-industries/zed (VERIFIED); https://zed.dev/docs/extensions (VERIFIED); https://zed.dev/docs/languages/gdscript (REPORTED, snippet).

### Godot built-in editor (and its command line)
**What it is:** The editor and engine binary for Godot 4; one executable edits, runs, exports and serves as a language and debug server.
**Cost:** Free, including commercial games (MIT; https://godotengine.org/license, not re-read: UNVERIFIED wording).
**Open source:** Yes, MIT (VERIFIED via API; 119k stars, last push 2026-11-03).
**Extendable:** `@tool` editor plugins in GDScript, GDExtension in C/C++/Rust, engine source (the web-editor page confirms no GDExtension there).
**Agent integration:** (a) `.tscn`, `.tres`, `.gd` are text; Godot says it aims for "mostly readable and mergeable files". (b) Rich CLI: `--headless`, `--script`, `--check-only`, `--import`, `--quit`/`--quit-after`, `--fixed-fps`, `--export-release|debug|pack`, `--doctool`. Caution (VERIFIED): unknown arguments are silently ignored, and passing `project.godot` opens the editor. (c) `--script` runs SceneTree scripts; `@tool` automates the editor. LSP port 6005, DAP 6006. (d) MCP, all community: `Coding-Solo/godot-mcp` (MIT, 6.5k stars, last push 2026-04-16, so possibly stale) launches the editor, runs the project, reads debug output, creates scenes and nodes, via `npx`. `funplayai/funplay-godot-mcp` (MIT, 49 stars, 2026-10-10) adds `execute_code`. `youichi-uda/godot-mcp-pro` is proprietary and paid (README lists USD 15 one-time; tool count inconsistent, 162 vs 187). Any server that runs GDScript is arbitrary code execution. (e) No official AI assistant (REPORTED; vendor blog). (f) Headless runs, `--check-only`, GUT and GdUnit4 give evidence; looks and feel need a human.
**Pros for agentic work:**
- Text scenes plus a real CLI: the best text-first path of any engine here.
- Free, MIT, nothing to licence-check.
**Cons for agentic work:**
- No official MCP server or AI features.
- Silent-ignore of bad flags can fake success.
**Verdict:** High: text-first project format and a genuine headless CLI.
**Sources:** https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/editor/external_editor.html (VERIFIED); https://api.github.com/repos/godotengine/godot (VERIFIED); https://github.com/Coding-Solo/godot-mcp (VERIFIED); https://api.github.com/repos/funplayai/funplay-godot-mcp (VERIFIED); https://github.com/youichi-uda/godot-mcp-pro (VERIFIED); https://www.summerengine.com/blog/does-godot-have-ai (REPORTED).

---

## B. Version control for game projects

### Git with Git LFS
**What it is:** Git is the standard distributed version control; Git LFS replaces large binary files in the repository with small pointer files and stores the content separately.
**Cost:** Free software. Hosting is the cost: GitHub includes 10 GiB LFS storage and 10 GiB monthly bandwidth on Free and Pro, 250 GiB each on Team and Enterprise Cloud (read today). Over quota with no payment method: you can still clone but only get pointer files and cannot push; bandwidth overage disables LFS until next month.
**Open source:** Git: GPL-2.0 (UNVERIFIED today). Git LFS: MIT (VERIFIED, LICENSE.md; 14.6k stars, last push 2026-11-01).
**Extendable:** Hooks, filters, `.gitattributes` rules, custom transfer agents (UNVERIFIED).
**Agent integration:** (a) Text diffs for scripts and Godot scenes; binaries become pointers. (b) Pure CLI. (c) Everything is scriptable. (d) The official GitHub MCP server (`github/github-mcp-server`, MIT, 34k stars, last push 2026-11-03) covers the hosting side. (e) None. (f) `git status`, `git lfs ls-files` show whether assets are really tracked. Godot's docs recommend LFS for textures, audio and models, and say to set it up before the first commit.
**Pros for agentic work:**
- Every agent already knows Git; worktrees give parallel agents isolated copies.
- Godot's text scenes diff and merge.
**Cons for agentic work:**
- A clone over quota yields pointer files; an agent may "see" an asset that is 130 bytes of text.
- No automatic exclusive locks for binaries (`git lfs lock` exists; UNVERIFIED how well it is enforced).
- History bloat if LFS is added late.
**Verdict:** High: the format and tooling agents know best.
**Sources:** https://github.com/git-lfs/git-lfs/blob/main/LICENSE.md (VERIFIED); https://api.github.com/repos/git-lfs/git-lfs (VERIFIED); https://docs.github.com/en/billing/concepts/product-billing/git-lfs (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html (VERIFIED); https://api.github.com/repos/github/github-mcp-server (VERIFIED).

### Perforce Helix Core (P4)
**What it is:** A centralised version control system built for very large binary-heavy repositories; the long-time industry default for studios.
**Cost:** Free for up to 5 users and 20 workspaces (read today at https://www.perforce.com/products/helix-core/free-version-control; that page does not say whether free use is allowed for commercial work, so UNVERIFIED). P4 Cloud for teams under 100 is advertised at USD 39 per user per month (read today). Self-hosted paid pricing: check current terms.
**Open source:** No (the vendor's MCP server is MIT).
**Extendable:** Command-line and APIs, `-Mj` JSON output (REPORTED), triggers and extensions (UNVERIFIED).
**Agent integration:** (a) Binary assets handled natively; text diffs for scripts. (b) `p4` CLI. (c) CLI and API cover the GUI. (d) `perforce/p4mcp-server` sits in Perforce's GitHub organisation (MIT, 123 stars, last push 2026-11-02), but its README says "Community Supported", not officially supported. Install: `uvx p4mcp-server` (PyPI) or Docker. Tools: read `query_*` (changelists, files, shelves, jobs, reviews, streams) and write `modify_*`; `--readonly` limits it, and the README contradicts itself about the default, so check. Tested on P4 Server 2026.1. HTTP transport has no authentication. (e) P4 DAM has AI tagging. (f) `p4 changes` as evidence. Godot's editor has only a Git plugin (VERIFIED).
**Pros for agentic work:**
- Handles huge binary assets and exclusive checkouts.
- A real MCP server with read-only mode.
**Cons for agentic work:**
- Needs a server; workspace model is less familiar to models than Git (UNVERIFIED).
- No Godot editor integration.
**Verdict:** Medium: capable MCP, but heavyweight and off the Godot path.
**Sources:** https://www.perforce.com/products/helix-core (VERIFIED); https://www.perforce.com/products/helix-core/free-version-control (VERIFIED); https://github.com/perforce/p4mcp-server (VERIFIED); https://api.github.com/repos/perforce/p4mcp-server (VERIFIED); `-Mj` via a Perforce workshop script found by search (REPORTED).

### Unity Version Control (UVCS, formerly Plastic SCM)
**What it is:** Unity's centralised/distributed version control, designed for large binaries, with a simplified client (Gluon) for artists; the docs say it works with any engine.
**Cost:** Cloud: unlimited seats; first 25 GB per organisation per month free, then USD 0.14/GB-month; 100 GB egress free then USD 0.10/GB (Unity support article, updated 2026-07-08, effective 2026-03-01; public cloud only, legacy and on-prem may differ). Free use for commercial games: check Unity's terms.
**Open source:** No.
**Extendable:** CLI, plug-ins for other tools; a public API was not found on the overview (UNVERIFIED).
**Agent integration:** (a) Binary-friendly. (b) `cm` CLI: `cm showcommands`, `cm <command> --usage`, a pipe command for scripting, `cm support bundle`. (c) CLI. (d) No MCP server found (UNVERIFIED; search only). (e) None. (f) `cm status`-style checks (command names not read: UNVERIFIED). Docs include migration guides from Git and Perforce.
**Pros for agentic work:**
- Cheap storage meter and no seat charges.
- Engine-agnostic CLI.
**Cons for agentic work:**
- Models know it far less than Git; no agent-oriented docs or MCP found.
- Pricing changed in 2026; legacy accounts differ.
**Verdict:** Medium: scriptable CLI, but unfamiliar to agents and no MCP.
**Sources:** https://docs.unity.com/en-us/unity-version-control (VERIFIED); https://support.unity.com/hc/en-us/articles/34748492914964-Understanding-Unity-DevOps-charges (VERIFIED); https://docs.unity.com/en-us/unity-version-control/cli/landing (VERIFIED); CLI help text via search results (REPORTED).

### Diversion
**What it is:** A cloud-native version control system for large binary projects, positioned as a modern alternative to Perforce.
**Cost:** Indie: free for the first 5 users with eligibility required, up to 20 users, 100 GB, 5 repositories, extra storage USD 10/month per 100 GB; Education free up to 10 users; Pro USD 25 per user per month; Studio USD 35; Enterprise custom (read today at https://www.diversion.dev/pricing). Eligibility rules for Indie and commercial-use terms: not read (UNVERIFIED).
**Open source:** No stated; treat as proprietary SaaS (UNVERIFIED).
**Extendable:** `dv` CLI, REST API (Pro plan or above), Unreal plugin; Unity and Godot not on the docs home page (UNVERIFIED).
**Agent integration:** (a) Built for binaries. (b) Non-interactive `dv` CLI: `dv commit -a -m`, `dv branch -c`, `dv clone <repo> <path> --new-workspace --ref <branch>`; bare `dv` opens an interactive shell, which agents must avoid. (c) REST API, same bearer token. (d) The agent quickstart mentions no MCP server. It offers a Claude Code plugin, `DiversionCompany/diversion-claude` (early access), that links each commit to the conversation that produced it. (e) A built-in agent, SlothBot. (f) `dv status`; no staging area, no push/pull, commits sync to teammates automatically.
**Pros for agentic work:**
- The only VCS here with a vendor-written agent quickstart, headless token auth and a parallel-agent recipe (one workspace per agent).
**Cons for agentic work:**
- Auto-sync: a bad agent commit reaches teammates at once; agents sharing a branch can conflict.
- Each workspace clones the full repository, binaries included.
**Verdict:** Medium: excellent agent docs, but proprietary and Godot support is unconfirmed.
**Sources:** https://docs.diversion.dev/agent-quickstart (VERIFIED); https://www.diversion.dev/pricing (VERIFIED); https://docs.diversion.dev (VERIFIED); https://www.diversion.dev/diversion-claude-code-plugin (REPORTED, search snippet).

---

## C. CI and build automation

### GitHub Actions
**What it is:** GitHub's CI/CD service; workflows are YAML files in `.github/workflows`.
**Cost:** Standard runners in public repositories are free. Private repositories get a monthly dollar allowance: USD 12 on Free, 18 on Pro and Team, 300 on Enterprise Cloud, with 500 MB artifact storage on Free. Per-minute rates read today: Linux 2-core USD 0.006, Windows 2-core 0.010, macOS 0.062. Self-hosted runners do not use the allowance. The page mentions no 2026 changes.
**Open source:** The service is not. Individual actions are separate repositories with their own licences.
**Extendable:** Marketplace and custom actions, reusable workflows, self-hosted runners.
**Agent integration:** (a) Workflow files are text, diffable. (b) `gh` CLI; `gh issue list` takes `--json` and `--jq` (VERIFIED); run commands UNVERIFIED. (c) REST/GraphQL API (UNVERIFIED). (d) `github/github-mcp-server` is official (MIT, last push 2026-11-03). (e) Agents that run inside CI: `anthropics/claude-code-action` (MIT, 9.8k stars, last push 2026-11-03) and `openai/codex-action` (Apache-2.0, 1.3k stars, 2026-10-31). (f) CI results and exit codes are evidence; an agent can read failed logs and fix.
**Pros for agentic work:**
- An agent can both edit the workflow and read its results, closing the loop.
- Godot and GameCI images run on it.
**Cons for agentic work:**
- Security: pin third-party actions to a full commit SHA; never check out untrusted PR code under `pull_request_target`; avoid self-hosted runners on public repos (VERIFIED).
- Untrusted issue or PR text can steer an agent in CI (my inference).
**Verdict:** High: text workflows plus an official MCP server and agent actions.
**Sources:** https://docs.github.com/en/billing/concepts/product-billing/github-actions (VERIFIED); https://docs.github.com/en/actions/about-github-actions/understanding-github-actions (VERIFIED); https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions (VERIFIED); https://api.github.com/repos/anthropics/claude-code-action (VERIFIED); https://api.github.com/repos/openai/codex-action (VERIFIED).

### GameCI (for Unity)
**What it is:** A set of open-source GitHub Actions and Docker images for building and testing Unity projects in CI.
**Cost:** Free. You still need a Unity licence activated in CI: Personal uses the `.ulf` file, Unity email and password stored as secrets; Pro uses a serial; organisations can use a licence server (VERIFIED). Whether CI use fits your Unity licence: check Unity's terms.
**Open source:** Yes, `game-ci/unity-builder` is MIT (1.1k stars, last push 2026-10-24).
**Extendable:** Actions, Docker images, an Orchestrator, a CLI; also GitLab, CircleCI and self-hosting docs.
**Agent integration:** (a) YAML text. (b) Runs through CI, not locally. (c) Actions for builder, test-runner, activate, return-licence. (d) No MCP found (UNVERIFIED). (e) None. (f) Test results as artifacts; build pass/fail.
**Pros for agentic work:**
- Standard recipe an agent can reproduce from the docs.
- Free for public repos' compute.
**Cons for agentic work:**
- Unity only; the docs home does not mention Godot or Unreal.
- Activation needs your Unity account password in a CI secret; a leaked secret is a real loss.
**Verdict:** Medium: well-trodden for Unity, irrelevant to Godot, credential-heavy.
**Sources:** https://game.ci/docs (VERIFIED); https://game.ci/docs/github/activation (VERIFIED); https://api.github.com/repos/game-ci/unity-builder (VERIFIED).

### Jenkins
**What it is:** A self-hosted open-source automation server, common in studios for large build farms.
**Cost:** Free; you pay for the machines.
**Open source:** Yes, MIT (26.7k stars, last push 2026-11-03).
**Extendable:** Thousands of plugins, pipelines as code (Jenkinsfile; UNVERIFIED).
**Agent integration:** (a) Pipelines are text. (b) CLI and REST (UNVERIFIED). (c) Plugin API. (d) Official MCP Server plugin on plugins.jenkins.io, source `jenkinsci/mcp-server-plugin` (MIT, 119 stars, last push 2026-11-02). Tools: `triggerBuild`, `getBuildLog`, `searchBuildLog`, `getTestResults`, `getFlakyFailures`, `createPipeline`, `replayBuild`, `cancelBuild`, `getJobs`. Endpoints: streamable HTTP at `/mcp-server/mcp`, SSE and stateless. Authentication is a user API token. Two past security advisories for missing permission checks; `allowUnauthenticatedMcp` is off and enabling it weakens CSRF protection. (e) None. (f) Build logs and test results are fetched through tools.
**Pros for agentic work:**
- Official plugin; agent can trigger a build and read the log in one session.
- Runs on GPU machines you control (e.g. Explorer-style nodes).
**Cons for agentic work:**
- You run, patch and secure the server.
- An agent that can create pipelines can run code on your build agents.
**Verdict:** Medium: official MCP, but operations burden and a powerful attack surface.
**Sources:** https://plugins.jenkins.io/mcp-server/ (VERIFIED); https://api.github.com/repos/jenkinsci/mcp-server-plugin (VERIFIED); https://api.github.com/repos/jenkinsci/jenkins (VERIFIED).

### Godot export in CI
**What it is:** Building Godot games in automation, using the editor binary's CLI export and community Docker images and actions.
**Cost:** Free (MIT tooling); CI minutes as above.
**Open source:** Yes. `abarichello/godot-ci` (MIT, 1.2k stars, last push 2026-10-20) is a Docker image with GitLab CI and GitHub Actions templates that deploy to Pages or itch.io. `firebelley/godot-export` (MIT, 653 stars, last push 2026-05-28) is a GitHub Action.
**Extendable:** Any shell step; custom export presets.
**Agent integration:** (a) `export_presets.cfg` is text and safe to commit; secrets live in `.godot/export_credentials.cfg`, which should stay out of version control. (b) `godot --headless --export-release "<preset>" <path>`; `--export-debug`, `--export-pack`. You need the editor binary (not a template), matching export templates installed, and the output directory must already exist; relative output paths resolve from the folder holding `project.godot`. (c) n/a. (d) None needed beyond GitHub's. (e) None. (f) Check the artifact exists and has a sane size, then run it headless with `--quit-after`; exit code 0 alone is not proof, because bad arguments are silently ignored.
**Pros for agentic work:**
- Deterministic, scriptable, textual.
- The course's `--headless --fixed-fps 60 timeout` pattern fits directly.
**Cons for agentic work:**
- Missing templates or SDKs block export; Android and iOS need extra toolchains.
- Community images are a supply-chain choice: pin versions.
**Verdict:** High: a plain CLI with text config.
**Sources:** https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html (VERIFIED); https://api.github.com/repos/abarichello/godot-ci (VERIFIED); https://api.github.com/repos/firebelley/godot-export (VERIFIED).

---

## D. Testing frameworks

### GUT (Godot Unit Test)
**What it is:** The long-standing GDScript unit-test framework for Godot, with doubles, stubs and spies.
**Cost:** Free.
**Open source:** Yes, MIT per its README and `addons/gut/LICENSE.md` (VERIFIED; the GitHub API shows no licence field). 2.8k stars, last push 2026-08-18. Version 9.7.1 targets Godot 4.7.x; 9.6.1 targets 4.6.x.
**Extendable:** Write test scripts in GDScript; command-line config file `.gutconfig.json`.
**Agent integration:** (a) Tests are `.gd` text. (b) Command: `godot -d -s --path "$PWD" addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit -gjunit_xml_file=results.xml`; the docs do not show `--headless`, which the course adds. Returns 1 if any test fails. (c) n/a. (d) No MCP found (UNVERIFIED). (e) None. (f) Exit code plus JUnit XML. Pending tests do not change the exit code.
**Pros for agentic work:**
- An agent can write the test and run it in one loop.
- JUnit XML is easy to parse.
**Cons for agentic work:**
- GDScript only (C# not mentioned).
- Match the GUT release to the Godot minor version.
- Check the output says N passing, not just exit 0.
**Verdict:** High: CLI, exit codes and XML make failures machine-readable.
**Sources:** https://github.com/bitwes/Gut (VERIFIED); https://api.github.com/repos/bitwes/Gut (VERIFIED); https://gut.readthedocs.io/en/latest/Command-Line.html (VERIFIED).

### GdUnit4
**What it is:** An embedded test framework for Godot 4 covering GDScript and C#, with a scene runner that simulates input.
**Cost:** Free.
**Open source:** Yes, MIT (`godot-gdunit-labs/gdUnit4`, 1.3k stars, last push 2026-11-03; formerly under a personal account, redirect not confirmed).
**Extendable:** GDScript/C# test suites; GdUnit4Net C# adapter for Visual Studio, VS Code and Rider; GitHub Action `gdunit4-action`.
**Agent integration:** (a) Text tests. (b) `addons/gdUnit4/runtest.sh` (Linux/macOS) or `runtest.cmd` with `GODOT_BIN` set; flags `-a`, `-i`, `-c`, `-conf`, `-rd`. Exit codes: 0 pass, 100 failures, 101 warnings. Reports: `index.htm` and JUnit `results.xml`. (c) Scene runner drives mouse, keyboard and touch input. (d) No MCP found (UNVERIFIED). (e) None. (f) Exit code plus report; orphan-node detection. Version 6.x needs Godot 4.5+. The CLI page does not mention headless; one GitHub discussion reports the Action using a virtual display (REPORTED).
**Pros for agentic work:**
- Distinct exit codes separate failures from warnings.
- Input simulation lets an agent test UI behaviour without a human.
**Cons for agentic work:**
- Headless behaviour is unclear (UNVERIFIED); test on your own CI.
- Fast-moving version requirements.
**Verdict:** High: richest scene and input testing with machine-readable exit codes.
**Sources:** https://godot-gdunit-labs.github.io/gdUnit4/latest/ (VERIFIED); https://godot-gdunit-labs.github.io/gdUnit4/latest/advanced_testing/cmd/ (VERIFIED); https://api.github.com/repos/godot-gdunit-labs/gdUnit4 (VERIFIED); https://github.com/godot-gdunit-labs/gdUnit4Net/discussions/350 (REPORTED).

### Unity Test Framework
**What it is:** Unity's NUnit-based test package for Edit Mode and Play Mode tests.
**Cost:** Included with Unity; Unity's licence terms apply (check current terms).
**Open source:** Package source licence not checked (UNVERIFIED); Unity itself is not open source.
**Extendable:** NUnit attributes, custom test assemblies.
**Agent integration:** (a) C# text tests. (b) `Unity -runTests -batchmode -projectPath <p> -testPlatform EditMode|PlayMode -testResults <file.xml>`; `-testFilter`, `-testCategory`. Output is NUnit XML. Docs state there is no common definition for exit codes of the components under test, so read the XML. (c) Editor API. (d) Unity MCP bridges are community (e.g. `CoplayDev/unity-mcp`, MIT, 15.7k stars, last push 2026-10-30); not examined beyond that. (e) Unity's own assistant: not checked. (f) XML results plus GameCI's test runner in CI.
**Pros for agentic work:**
- Full CLI and a standard result format.
- Works inside GameCI.
**Cons for agentic work:**
- Needs a Unity licence on the machine; slow project load.
- Exit codes unreliable; parse XML.
**Verdict:** High: complete batch mode, but verify through the XML, not the exit code.
**Sources:** https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html (VERIFIED); https://api.github.com/repos/CoplayDev/unity-mcp (VERIFIED).

### Unreal Automation System and Gauntlet
**What it is:** Automation is Unreal's built-in test runner; Gauntlet is a framework that launches whole game sessions (clients plus server, possibly on devices) and validates results.
**Cost:** Part of Unreal Engine; engine licence terms not read (UNVERIFIED; https://www.unrealengine.com/en-US/license returned 403).
**Open source:** Source-available with the engine (UNVERIFIED wording); not open source.
**Extendable:** C++ tests; Gauntlet test configs in C# (UNVERIFIED); optional Gauntlet plugin with a `TestController` class (VERIFIED).
**Agent integration:** (a) Source text. (b) Editor/client args: `-ExecCmds="Automation RunTest <names>;Quit"`, `-ReportExportPath=<dir>` for JSON plus HTML (VERIFIED, Epic docs). Forum posts add `-unattended -NullRHI` for headless (REPORTED). Gauntlet: `RunUAT RunUnreal -project=... -platform=Win64 -configuration=Development -build=local -test=<Class>` (REPORTED, Epic docs snippet); it runs existing staged builds, so build and stage first. (c) n/a. (d) No MCP found (UNVERIFIED). (e) None found. (f) Report files and process exit; forum reports of "no tests matched" regressions between engine versions (REPORTED).
**Pros for agentic work:**
- Complete headless story for large teams; JSON reports.
- Gauntlet can test multi-process sessions.
**Cons for agentic work:**
- Windows-first, long builds, multi-gigabyte projects.
- Version-sensitive; sparse docs for exact flags.
**Verdict:** Medium: powerful but heavy and version-fragile.
**Sources:** https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine (VERIFIED); https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine (VERIFIED); https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine (REPORTED, snippet); https://forums.unrealengine.com/t/run-automated-testing-from-command-line/294995 (REPORTED).

---

## E. Profiling and debugging

### RenderDoc
**What it is:** A stand-alone graphics frame debugger: capture a frame, then inspect draw calls, textures, shaders and pipeline state.
**Cost:** Free.
**Open source:** Yes, MIT (https://github.com/baldurk/renderdoc, 11.3k stars, last push 2026-11-03).
**Extendable:** A Python API ("most features available in the UI" are reachable), UI extensions, and an in-application capture API.
**Agent integration:** (a) Captures are binary `.rdc`. (b) Runs on Vulkan, D3D11, D3D12, OpenGL and OpenGL ES on Windows, Linux, Android and Switch; Metal and macOS are not listed (VERIFIED). A `renderdoccmd` tool exists (UNVERIFIED on the page read). (c) Python API covers replay, pipeline state, texture saving, pixel history; whether it runs without the GUI was not confirmed. (d) MCP: all community. `JiaboLi-GitHub/renderdoc-mcp` (MIT, 375 stars, last push 2026-06-09): 59 tools, opens `.rdc` files, inspects pipeline and shaders, debugs pixels, diffs captures, asserts pixel and state values for CI; Windows prebuilt executable with bundled RenderDoc runtime; includes a Codex installer and a Claude Code config example. Other servers exist (REPORTED). Downloading a prebuilt binary is a supply-chain risk. (e) None. (f) Pixel and state assertions can verify rendering in CI; whether something looks right remains a human check.
**Pros for agentic work:**
- Scriptable analysis of a frame, and an MCP wrapper.
- Free and MIT.
**Cons for agentic work:**
- No macOS/Metal; the course Mac cannot use it.
- You must still produce the capture on a GPU machine.
**Verdict:** Medium: scriptable and MCP-wrapped, but community-only and no Mac.
**Sources:** https://api.github.com/repos/baldurk/renderdoc (VERIFIED); https://renderdoc.org/docs/index.html (VERIFIED); https://renderdoc.org/docs/python_api/index.html (VERIFIED); https://github.com/JiaboLi-GitHub/renderdoc-mcp (VERIFIED); https://api.github.com/repos/JiaboLi-GitHub/renderdoc-mcp (VERIFIED).

### PIX (PIX on Windows)
**What it is:** Microsoft's GPU and CPU performance tool for Direct3D 12 games on Windows (Xbox uses the version in the GDK).
**Cost:** Downloadable free from Microsoft (latest main version listed: 2610.28); licence terms not read, so "free for commercial use" is UNVERIFIED.
**Open source:** No.
**Extendable:** WinPixEventRuntime on NuGet for markers; the tool is closed.
**Agent integration:** (a) Captures binary. (b) `pixtool.exe` installs with PIX: launch an app for GPU capture, take or open captures, list counters, save the event list as CSV (optionally with timing or counters), extract the captured screenshot as PNG, save render targets and depth buffers, and compare screenshots for automated testing (VERIFIED, Microsoft devblog). (c) The CLI is the scripting surface. (d) No MCP found (UNVERIFIED). (e) None. (f) CSV and PNG outputs are agent-readable evidence.
**Pros for agentic work:**
- Real command-line capture and export.
- Free (apparently).
**Cons for agentic work:**
- Windows and Direct3D 12 centred (D3D12-only is UNVERIFIED); Godot's default Vulkan path on Mac/Linux cannot use it.
- Closed; no MCP.
**Verdict:** Medium: usable CLI, but Windows-only and niche for a Godot course.
**Sources:** https://devblogs.microsoft.com/pix/pixtool/ (VERIFIED); https://devblogs.microsoft.com/pix/download/ (VERIFIED).

### Tracy
**What it is:** A real-time, nanosecond-resolution hybrid frame and sampling profiler with remote capture, widely embedded in game engines.
**Cost:** Free.
**Open source:** Yes, 3-clause BSD (VERIFIED; 17k stars, last push 2026-11-02; release v0.14.1 on 2026-08-22).
**Extendable:** Instrument C, C++, Lua, Python and Fortran, third-party bindings for Rust, Zig, C#; GPU zones for OpenGL, Vulkan, D3D11/12, Metal, OpenCL, CUDA and WebGPU.
**Agent integration:** (a) `.tracy` capture files are binary. (b) Releases ship the manual (`tracy.pdf`) and per-platform zips; the headless tools `tracy-capture` and `tracy-csvexport` are described in secondary sources (REPORTED: `tracy-capture -o out.tracy -a addr -p port -s seconds`; CSV export of per-zone statistics). (c) Source macros in the profiled program. (d) No Tracy MCP server found (UNVERIFIED). (e) None. (f) CSV statistics can back a performance budget check. Godot 4.x documents building the engine with `profiler=tracy` (Tracy 0.13.0, release templates, debug symbols); the page frames this as C++ engine profiling and does not say whether GDScript is covered.
**Pros for agentic work:**
- Headless capture and CSV export fit CI.
- Free, small, BSD.
**Cons for agentic work:**
- Godot needs a custom engine build.
- The viewer is a GUI; the agent sees only exported numbers.
**Verdict:** Medium: automatable capture, but custom Godot builds and no MCP.
**Sources:** https://raw.githubusercontent.com/wolfpld/tracy/master/LICENSE (VERIFIED); https://api.github.com/repos/wolfpld/tracy/releases/latest (VERIFIED); https://github.com/wolfpld/tracy (VERIFIED); https://docs.godotengine.org/en/stable/engine_details/development/profiling/tracy.html (VERIFIED); tracy-capture and csvexport flags from IREE documentation (REPORTED).

### Superluminal
**What it is:** A commercial sampling and instrumentation CPU profiler for Windows and consoles with a strong interface.
**Cost:** Paid, one price for all platforms (EUR, read today, page undated, footer 2026): Personal EUR 59 perpetual for non-commercial use; Business EUR 289 per seat per year; Enterprise on quote; 14-day trial with all features. No free tier; academic licences on request.
**Open source:** No.
**Extendable:** PerformanceAPI for instrumentation from the target app.
**Agent integration:** (a) Captures binary. (b) `SuperluminalCmd.exe` ships with the product to make captures locally or remotely (VERIFIED). A third-party article says capture needs no licence while analysing does (REPORTED). (c) PerformanceAPI. (d) The docs' "AI support" section says agents can analyse captures through a CLI or an MCP server, across supported platforms; setup steps point to the SuperluminalCmd docs and I did not read them (VERIFIED existence, UNVERIFIED details). (e) The MCP server is the AI feature. (f) Agent reads capture data without the GUI.
**Pros for agentic work:**
- One of the few profilers with an official agent route (CLI and MCP).
- Engines listed: Unreal, Unity, Godot.
**Cons for agentic work:**
- Paid; Windows, Xbox, PlayStation (docs list no macOS or Linux; homepage mentions Linux in passing: conflict, UNVERIFIED).
- Not open or extendable beyond the API.
**Verdict:** Medium: official CLI and MCP, but paid and Windows/console-centric.
**Sources:** https://superluminal.eu/pricing/ (VERIFIED); https://superluminal.eu/ (VERIFIED); https://superluminal.eu/docs/documentation.html (VERIFIED); a third-party capture guide (REPORTED).

### Unity Profiler
**What it is:** Unity's built-in profiler for CPU, memory, rendering and more, in the Editor or connected to a player.
**Cost:** Included with Unity; terms: check Unity's current terms.
**Open source:** No.
**Extendable:** Custom markers and counters, custom modules, Profile Analyzer package (linked from the docs).
**Agent integration:** (a) Captures `.raw`/`.data`, binary. (b) Flags documented for Unity 6.x: `-profiler-enable` (profile start-up), `-profiler-log-file <path.raw>` (stream to file on start-up, players and Editor), `-profiler-capture-frame-count <n>` (players only), `-profiler-maxusedmemory`. Combine with `-batchmode`. (c) Scripting APIs (e.g. `ProfilerRecorder`) were not read (UNVERIFIED). (d) Community Unity MCP servers exist (see Unity Test Framework); whether they read profiler data was not checked. (e) Unity's own assistant: not checked. (f) A scripted run can emit a `.raw` file; reading it normally needs the Profiler window or Profile Analyzer (UNVERIFIED for headless analysis).
**Pros for agentic work:**
- Command-line capture works in CI.
- No extra install.
**Cons for agentic work:**
- Analysis is mostly GUI.
- Locked to Unity.
**Verdict:** Medium: capture is scriptable, analysis is not.
**Sources:** https://docs.unity3d.com/Manual/profiler-command-line-arguments.html (REPORTED, search snippet); https://docs.unity.com/en-us/engine/current/manual/analysis/profiler (VERIFIED).

### Unreal Insights
**What it is:** Unreal's telemetry capture and analysis suite (timing, memory, networking, loading, cooking, audio).
**Cost:** Included with Unreal Engine; engine terms not read (UNVERIFIED).
**Open source:** Source-available with the engine (UNVERIFIED wording).
**Extendable:** Add trace events with Trace macros and channels; build the tool from source (`RunUBT ... UnrealInsights`).
**Agent integration:** (a) `.utrace` binary, `.ucache` companion. (b) Start tracing with `-trace=` (REPORTED, older docs). Standalone `UnrealInsights` can be run with `-OpenTraceFile=`, `-NoUI`, `-AutoQuit` and `-ExecOnAnalysisCompleteCmd="TimingInsights.ExportThreads ./CSV/Threads.csv"` (REPORTED, Epic knowledge-base thread). The same thread reports the headless export doing nothing on UE 5.5, 5.6 and 5.7, and `ExportCounters` failing to write, so treat headless export as unreliable (REPORTED). (c) CSV exporters. (d) A community skill wrapping UnrealInsights.exe exists (REPORTED; not examined). (e) None. (f) CSV if it works; otherwise GUI.
**Pros for agentic work:**
- Rich data, cross-version trace files.
- CSV export hooks exist.
**Cons for agentic work:**
- Headless export reported broken on recent engines.
- Unreal-only, heavyweight.
**Verdict:** Low: analysis is GUI-bound and the headless path is reported to fail.
**Sources:** https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine (VERIFIED); https://forums.unrealengine.com/t/knowledge-base-unreal-insights-automated-trace-analysis-and-csv-export/1882278 (REPORTED).

### Godot profiler, monitors and command-line profiling flags
**What it is:** The profiler tools inside the Godot editor's Debugger panel plus a few engine flags and a scripting API for performance numbers.
**Cost:** Free (MIT).
**Open source:** Yes (part of Godot).
**Extendable:** `Performance.add_custom_monitor()` registers your own monitor, which then appears in the Monitor tab (VERIFIED).
**Agent integration:** (a) Not applicable (live data). (b) Flags: `--profiling` (profiling in the script debugger), `--gpu-profile`, `--print-fps`, `--max-fps`, `--disable-vsync`, `--log-file`, `--write-movie`, and `--benchmark` / `--benchmark-file <path>` (JSON; editor builds only) (VERIFIED). (c) `Performance.get_monitor()` returns FPS, memory, object count and draw calls to a script; some monitors return 0 in release exports; headless behaviour not stated (UNVERIFIED). `Time.get_ticks_usec()` for manual timing. (d) No profiler MCP found; the community MCP servers can read debug output (see Godot entry). (e) None. (f) A test script can assert on monitor values; the Profiler tab (off by default, must be started) is GUI-only, and the page does not say its data can be exported. It does not support C# scripts.
**Pros for agentic work:**
- `--benchmark-file` JSON and `Performance` numbers are agent-readable.
- No extra tool to install.
**Cons for agentic work:**
- The Profiler and Visual Profiler are GUI-only; frame-time feel is a human check.
- Software-rendered headless runs do not reflect GPU cost.
**Verdict:** Medium: a few scriptable numbers, but the real profiler is a GUI.
**Sources:** https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html (VERIFIED); https://docs.godotengine.org/en/stable/classes/class_performance.html (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html (VERIFIED).

---

## F. Project management and design documents

### GitHub Issues and Projects
**What it is:** GitHub's issue tracker and its table, board and roadmap planning layer.
**Cost:** Included with GitHub accounts; plan-by-plan Projects availability was not stated on the page read (UNVERIFIED); check current terms.
**Open source:** No.
**Extendable:** GraphQL API, GitHub Actions, built-in workflows, custom fields (VERIFIED).
**Agent integration:** (a) Data lives in the service, not the repo. (b) `gh issue create|list|view|edit|close|comment`; `gh issue list` accepts `--json`, `--jq`, assignee, label and state filters. `gh project create|item-add|item-list|field-list|item-edit` needs the token scope `project` (all VERIFIED). (c) API covers everything. (d) Official `github/github-mcp-server` (MIT, 34k stars, last push 2026-11-03). (e) Copilot features (not checked). (f) An agent can open, label and close its own issues and link them to commits.
**Pros for agentic work:**
- Same system as the code, so one login and one permissions model.
- Mature CLI and official MCP.
**Cons for agentic work:**
- Issue and PR text is untrusted input to an agent (prompt-injection route).
- A token with write scope lets an agent change the board; use a fine-scoped token.
**Verdict:** High: CLI with JSON, official MCP, same place as the code.
**Sources:** https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects (VERIFIED); https://cli.github.com/manual/gh_issue_list (VERIFIED); https://cli.github.com/manual/gh_project (VERIFIED); https://api.github.com/repos/github/github-mcp-server (VERIFIED).

### Linear
**What it is:** A fast issue tracker and roadmap tool popular with small software teams.
**Cost:** Free plan USD 0: unlimited members, 2 teams, 250 issues. Basic USD 10 and Business USD 16 per user per month billed yearly; Enterprise custom (read today at https://linear.app/pricing).
**Open source:** No.
**Extendable:** API (GraphQL; UNVERIFIED), webhooks (UNVERIFIED), integrations.
**Agent integration:** (a) Data is in the service. (b) No CLI checked. (c) API. (d) Official hosted MCP server at `https://mcp.linear.app/mcp` (Streamable HTTP; the SSE endpoint is deprecated). Authentication is OAuth 2.1 or a bearer API key; read-only via `/mcp/readonly` or the `read` scope. Tools find, create and update issues, projects, comments and documents. Claude Code: `claude mcp add --transport http linear-server https://mcp.linear.app/mcp`, then `/mcp` to authenticate. Codex: `codex mcp add linear --url https://mcp.linear.app/mcp`. Clients without remote MCP support use the third-party `mcp-remote` package; review it before `npx`. (e) Linear's own intelligence features are on paid tiers. (f) Agent can read and write its own tickets.
**Pros for agentic work:**
- Official, hosted, no server to run; read-only mode available.
- Setup commands for both course agents are documented.
**Cons for agentic work:**
- Free plan caps at 250 issues.
- Write access means an agent can post comments in your workspace; start read-only.
**Verdict:** High: official remote MCP with a read-only switch and setup for Claude Code and Codex.
**Sources:** https://linear.app/docs/mcp (VERIFIED); https://linear.app/pricing (VERIFIED).

### Jira (Atlassian)
**What it is:** Atlassian's configurable issue and project tracker, heavy but ubiquitous in industry.
**Cost:** A Free plan exists; third-party sources agree on "up to 10 users" (REPORTED; the official page snapshot I read was truncated). Standard and Premium are per-user subscriptions; third-party guides disagree on the Standard price (USD 7.16 to 8.15), and one reports an Atlassian price rise from 2026-10-13: check current terms.
**Open source:** No.
**Extendable:** REST API, Forge apps, automation rules (UNVERIFIED; not read).
**Agent integration:** (a) Data is in the service. (b) No CLI checked. (c) REST API (UNVERIFIED). (d) Official Atlassian Rovo MCP server, remote, at `https://mcp.atlassian.com/v2/mcp`: OAuth 2.1, optional API token; covers Jira, Jira Service Management, Confluence, Bitbucket, Projects, Goals; lists Claude Code, Codex, VS Code and others as clients. Actions respect the user's permissions; Atlassian advises least privilege and reviewing high-impact changes. MCP calls consume Rovo credits from an organisation pool. v1 moves to v2 automatically on 2027-03-01. Plan eligibility not stated. (e) Rovo AI. (f) Agent can create and update work items.
**Pros for agentic work:**
- Official MCP covering the whole Atlassian suite.
- Works with both course agents.
**Cons for agentic work:**
- Credit consumption is opaque; heavy process overhead for a class project.
- Permissions model is only as good as the account you log in with.
**Verdict:** Medium: official MCP, but weighty and metered.
**Sources:** https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/ (VERIFIED); Jira plan numbers from third-party guides (REPORTED).

### Trello
**What it is:** Atlassian's card-and-board tool, simple Kanban for small teams.
**Cost:** Free for up to 10 collaborators per Workspace, 10 boards, 250 Workspace command runs per month, 10 MB per file. Standard USD 5, Premium USD 10, Enterprise USD 17.50 per user per month billed annually (all read today at https://trello.com/pricing).
**Open source:** No.
**Extendable:** REST API with OAuth 2.0 bearer tokens and scopes (VERIFIED); Power-Ups (UNVERIFIED).
**Agent integration:** (a) Data is in the service. (b) None checked. (c) REST API. (d) Official Atlassian Trello MCP server: remote endpoint `https://mcp.trello.com/v1`, OAuth 2.0 only (API tokens are not supported for MCP), works on any plan, reads and updates boards, lists, cards, checklists and comments, supports search; it cannot permanently delete (archive only). Repo `atlassian/trello-mcp-server` (Apache-2.0, 74 stars, last push 2026-10-27). The support page names ChatGPT, Claude, Cursor, VS Code and Gemini CLI, and says any MCP app; Claude Code and Codex are not named, so confirm them yourself (UNVERIFIED). Community servers exist that use API keys (REPORTED). (e) Trello AI on paid plans. (f) Agent can move cards.
**Pros for agentic work:**
- Official remote MCP; no deletion is a built-in safety net.
- Free tier is enough for a class.
**Cons for agentic work:**
- Cards do not carry code context; weak for specs.
- Free tier command-run limit.
**Verdict:** Medium: official MCP, but a thin tool for design work.
**Sources:** https://trello.com/pricing (VERIFIED); https://support.atlassian.com/trello/docs/connect-trello-to-ai-assistants-with-trello-mcp/ (VERIFIED); https://api.github.com/repos/atlassian/trello-mcp-server (VERIFIED); https://developer.atlassian.com/cloud/trello/rest/api-group-actions/ (VERIFIED).

### Notion
**What it is:** A hosted workspace for documents, databases and wikis.
**Cost:** Free USD 0 per member (5 MB uploads, 7-day history, limited AI trial); Plus USD 10 and Business USD 20 per member per month (read today at https://www.notion.com/pricing). Free Plus for students and educators, 1-member limit.
**Open source:** The app is not. `makenotion/notion-mcp-server` is MIT (4.7k stars, last push 2026-10-29) but Notion's docs say it is deprecated and "no longer actively maintained".
**Extendable:** Public API, integrations, MCP.
**Agent integration:** (a) Content lives in Notion's database, not in files. (b) None checked. (c) API. (d) Official hosted MCP at `https://mcp.notion.com/mcp` with OAuth. Claude Code: `claude mcp add --transport http notion https://mcp.notion.com/mcp`, then `/mcp`. Codex: add `[mcp_servers.notion]` with the URL, then `codex mcp login notion`. Business and Enterprise owners can issue an MCP token for headless use. Capabilities: search, create and edit pages, comments, databases and views, file upload. Only workspace members can connect, not guests; an admin policy may block it. (e) Notion's own agent and Skills. (f) Agent can read specs and write notes.
**Pros for agentic work:**
- Official hosted MCP for both agents.
- Good for non-programmers on a team.
**Cons for agentic work:**
- Not diffable or in the repo; versioning is Notion's history.
- Open-source server is deprecated; bearer MCP tokens must be guarded.
**Verdict:** Medium: official MCP, but documents sit outside the repo.
**Sources:** https://developers.notion.com/guides/mcp/get-started-with-mcp (VERIFIED); https://developers.notion.com/guides/mcp/mcp-supported-tools (VERIFIED); https://www.notion.com/pricing (VERIFIED); https://api.github.com/repos/makenotion/notion-mcp-server (VERIFIED).

### Obsidian
**What it is:** A note-taking app over a folder of Markdown files ("a vault"), with backlinks and plugins.
**Cost:** The app is "free without limits"; a commercial licence of USD 50 per user per year is encouraged but not required. Optional Sync USD 4 per user per month (billed annually) and Publish USD 8 per site per month (read today at https://obsidian.md/pricing). Full licence text not read (UNVERIFIED).
**Open source:** App is closed source (UNVERIFIED; the pricing page does not say); notes are plain Markdown, so there is no lock-in.
**Extendable:** Community plugins and themes. Plugins have no sandbox; they inherit Obsidian's access, and Restricted Mode is on by default (REPORTED, official help snippet).
**Agent integration:** (a) Plain Markdown: an agent can read and edit the vault with no app. (b) Obsidian CLI (1.12 installer; it connects to the running app and launches it if closed): create, read, append, search, backlinks, properties, tasks, `eval`, `dev:screenshot`, `dev:console`; many listings return JSON, CSV or TSV. (c) The CLI mirrors UI actions. (d) Community MCP only: `MarkusPfundstein/mcp-obsidian` (MIT, 4.5k stars, last push 2026-08-31), `coddingtonbear/obsidian-local-rest-api` (REST plus MCP, MIT, 3.1k, 2026-10-17), `bitbonsai/mcpvault` (MIT, 1.7k, 2026-11-02), `StevenStavrakis/obsidian-mcp` (MIT, 748, 2026-10-08). (e) None. (f) Developer commands let agentic tools test and debug (per the CLI docs).
**Pros for agentic work:**
- Plain files mean agents work with no integration at all.
- Vault can live inside the course repo, with diffs.
**Cons for agentic work:**
- CLI needs the desktop app running; plugins are an unsandboxed risk.
- MCP servers are community, one maintainer each.
**Verdict:** High: plain Markdown plus an agent-aware CLI.
**Sources:** https://obsidian.md/pricing (VERIFIED); https://obsidian.md/help/cli (VERIFIED); https://obsidian.md/help/plugin-security (REPORTED, snippet); https://api.github.com/search/repositories?q=obsidian+mcp+server (VERIFIED).

---

## G. Distribution and storefronts

### Steam and Steamworks
**What it is:** Valve's PC storefront (Steam) and its developer platform (Steamworks) with an SDK, achievements, cloud saves, networking and build delivery.
**Cost:** USD 100 per app, non-refundable but recoupable from payments once the app has USD 1,000 of adjusted gross revenue (read today). Valve takes a share of sales: check current terms (commonly reported as 30%, UNVERIFIED on a Valve page). Onboarding needs the NDA and distribution agreement, a tax interview (up to 30 days), review of 1 to 5 days, a 21-day wait between paying and release, and a public "coming soon" page for two weeks. The SDK is required only to upload builds; its licence terms were not on the page read.
**Open source:** No. `GodotSteam` (MIT) is a community integration: its GitHub repository was archived on 2026-10-20 and moved to Codeberg (`codeberg.org/godotsteam/godotsteam`); release 4.23.2, GDExtension or engine module, last commit 2026-10-28.
**Extendable:** Steamworks API; GodotSteam; build scripts.
**Agent integration:** (a) Build scripts are VDF text. (b) SteamCMD uploads via an app build script (REPORTED, third-party guide; Valve's page returned 403 to me); build accounts hit Steam Guard two-factor friction (REPORTED). (c) Store-page editing is a web form (UNVERIFIED that no API exists). (d) Only tiny community MCP servers, all under 15 stars: `wazzapsenk/steamworks-mcp` (MIT; checks store assets, fills Steamworks "only after approval"), `TMHSDigital/steam-mcp`, `sandraschi/steam-mcp`, `Sarg338/steam-mcp` (read-only). (e) None. (f) Upload logs.
**Pros for agentic work:**
- Scriptable build uploads fit CI.
- GodotSteam is MIT.
**Cons for agentic work:**
- Identity, tax, legal and store-page steps are human.
- Never hand Steam credentials to an agent; use a dedicated build account.
**Verdict:** Medium: build upload is scriptable, but onboarding is human and MCP servers are immature.
**Sources:** https://partner.steamgames.com/doc/gettingstarted/onboarding (VERIFIED); https://partner.steamgames.com/doc/gettingstarted/appfee (VERIFIED); https://partner.steamgames.com/doc/sdk (VERIFIED); https://github.com/GodotSteam/GodotSteam (VERIFIED); https://codeberg.org/godotsteam/godotsteam (VERIFIED); https://api.github.com/search/repositories?q=steam+mcp+server+steamworks&per_page=5 (VERIFIED); SteamCMD upload via https://kb.heathen.group/steam/uploading-to-steam (REPORTED).

### itch.io and butler
**What it is:** An open indie marketplace, and `butler`, its command-line tool for pushing builds.
**Cost:** Free to list. itch.io's share is whatever you choose: default 10%, adjustable from 0% to 100% (read today); payment processor fees apply; minimum payout USD 5; revenue available after 7 days; PayPal or Payoneer. A validated tax interview is required for payouts.
**Open source:** `itchio/butler` is MIT (1k stars, last push 2026-11-01). The site is not.
**Extendable:** butler patches, itch API (UNVERIFIED), the `godot-ci` templates that deploy to itch.io.
**Agent integration:** (a) Not applicable. (b) `butler push <directory> <user>/<game>:<channel>` uploads only the differences; channels such as `windows-beta` set platform tags; `--userversion` sets a version; the docs describe it as built for automated pipelines. API-key login docs: not read (UNVERIFIED; the key is an account secret). (c) CLI. (d) Only small community MCP servers for game-jam and asset search (0 to few stars). (e) None. (f) butler prints the upload result; the itch.io page must still be checked.
**Pros for agentic work:**
- One command from CI to a playable web or desktop build.
- Delta uploads make repeated pushes fast.
**Cons for agentic work:**
- The API key must be a CI secret; HTML5 "playable in browser" tagging is set manually after the first push.
- Store-page copy and screenshots are manual.
**Verdict:** High: a single, well-documented CLI for deployment.
**Sources:** https://docs.itch.zone/butler/master/pushing.html (VERIFIED); https://docs.itch.zone/butler/master/index.html (VERIFIED); https://itch.io/docs/creators/payments (VERIFIED); https://api.github.com/repos/itchio/butler (VERIFIED).

### Epic Games Store
**What it is:** Epic's PC storefront, plus Epic Online Services (EOS) for accounts, lobbies, voice and more.
**Cost:** Epic announced in May 2025 that developers pay 0% on the first USD 1 million per product per year for payments Epic processes, with the standard 88/12 split above that; the FAQ says the threshold resets each 1 January from 2026 (REPORTED; Epic's page returned 403). EOS: free core services, no royalty or hosting fees, anti-cheat extras by enterprise agreement (REPORTED, licensing page snippet). Whether free use covers every commercial case: read https://onlineservices.epicgames.com/licensing yourself.
**Open source:** No.
**Extendable:** EOS C SDK; engine integrations (a Godot integration was not found: UNVERIFIED).
**Agent integration:** (a) Not applicable. (b) BuildPatch Tool (BPT) is a command-line uploader; it needs ClientId, ClientSecret, OrganizationId, ProductId, ArtifactId, SandboxId and build version, and a cache folder outside the build root (REPORTED, forum posts); one forum thread reports BPT 1.9.0 (UE 5.8) needing a `-FeatureLevel` argument that Epic's own script did not pass (REPORTED). (c) The developer portal is web UI. (d) No MCP server found (UNVERIFIED). (e) None. (f) BPT output and the portal's build status.
**Pros for agentic work:**
- BPT can be scripted into CI.
- EOS is free and engine-agnostic.
**Cons for agentic work:**
- Credentials are powerful secrets; setup is thin on official docs.
- Approval and store setup are manual.
**Verdict:** Medium: scriptable uploader, human-gated store.
**Sources:** https://dev.epicgames.com/docs/epic-games-store (VERIFIED); https://store.epicgames.com/distribution/revenue-programs/revenue-share (REPORTED, search snippet); https://onlineservices.epicgames.com/licensing (REPORTED, search snippet); https://forums.unrealengine.com/t/how-to-upload-binaries-using-buildpatchtool/795133 (REPORTED).

### Mobile stores (Apple App Store and Google Play)
**What it is:** The two storefronts for iOS and Android, each with its own account, signing and review process.
**Cost:** Apple Developer Program USD 99 per membership year, waivers for eligible nonprofits, educational institutions and governments (read today). Google Play: USD 25 one-time registration fee, identity verification, and extra testing requirements for personal accounts (details not on the page read: UNVERIFIED). Store revenue shares: check current terms.
**Open source:** Stores no. `fastlane` (MIT, Ruby 3.2+) automates builds, signing, screenshots and uploads to TestFlight, the App Store and Google Play.
**Extendable:** App Store Connect API (builds, TestFlight, metadata, submissions; JWT from an API key; the `.p8` private key downloads once); Google Play Developer API (UNVERIFIED; not read).
**Agent integration:** (a) Godot export presets are text. (b) Godot Android export needs JDK 17, Android SDK, NDK r28b, a Gradle build for AAB and a release keystore; signing can use `GODOT_ANDROID_KEYSTORE_*` environment variables. iOS export needs a Mac with Xcode, produces an Xcode project, and needs a Team ID and bundle id. Neither page describes command-line export, though the generic `--export-release` flag exists. (c) APIs and fastlane. (d) No MCP found (UNVERIFIED). (e) None. (f) Build artifacts; TestFlight status via API.
**Pros for agentic work:**
- Documented APIs and a mature CLI (fastlane).
- Environment-variable signing suits CI.
**Cons for agentic work:**
- Identity checks, signing keys, review and payments are human or secret-bearing.
- An agent holding an API key or keystore can publish or break your account.
**Verdict:** Medium: automatable after setup, but setup and secrets are human-held.
**Sources:** https://developer.apple.com/programs/whats-included/ (VERIFIED); https://support.google.com/googleplay/android-developer/answer/6112435 (VERIFIED); https://developer.apple.com/documentation/appstoreconnectapi (VERIFIED); https://docs.fastlane.tools/ (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html (VERIFIED); https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html (VERIFIED).

### Consoles (overview: Switch, PlayStation, Xbox)
**What it is:** Closed platforms that require developer accounts, signed agreements, and proprietary SDKs.
**Cost:** Not published in what I read; accounts require a registered legal entity and non-disclosure agreements (REPORTED, translated Godot docs). Dev kit and licence costs: check each platform.
**Open source:** No.
**Extendable:** Vendor SDKs under NDA. Godot's docs say the only console officially supported is Steam Deck (via Linux templates); W4 Games is the official middleware vendor for Switch, Xbox Series X|S and PlayStation 5; other porting companies exist (REPORTED, search snippet of the 4.4/4.5 docs; the stable URL returned 404). Microsoft publishes a Godot 4 sample binding the GDK, Xbox services, PlayFab and GameInput for Xbox on PC (`microsoft/XBOX-Godot-Sample`, MIT, 240 stars, last push 2026-10-30).
**Agent integration:** (a) Project files are your own. (b) Build tooling is behind the NDA. (c) None public. (d) None. (e) None. (f) None without kit access. A practical point: NDA-covered SDK documents should not be pasted into a cloud-hosted agent (my reading of typical NDAs; check yours).
**Pros for agentic work:**
- The Xbox-on-PC Godot sample is public and buildable.
- Porting vendors take the NDA work off students.
**Cons for agentic work:**
- Nothing to automate for a course without access.
- Legal entity, NDA and certification gates.
**Verdict:** Low: gated by contracts, with no public agent route.
**Sources:** https://docs.godotengine.org/en/4.5/tutorials/platform/consoles.html (REPORTED, search snippet); https://api.github.com/search/repositories?q=playfab+godot&per_page=5 (VERIFIED, for the Xbox sample).

---

## H. Networking, backend services and analytics

### Nakama (Heroic Labs)
**What it is:** An open-source game backend: accounts, realtime multiplayer, matchmaking, leaderboards, chat, storage and social features.
**Cost:** Self-host free. Heroic Cloud (managed) lists no Nakama price on the page read; plans are sized by CPU and you contact sales (Satori, the analytics product, starts at USD 600/month; support packages USD 2,000 and up; read today).
**Open source:** Yes, Apache-2.0 (13.7k stars, last push 2026-11-03).
**Extendable:** Server runtime in Go, Lua or TypeScript; client libraries include Godot 3 and 4 (`heroiclabs/nakama-godot`, Apache-2.0, 783 stars, last push 2026-11-03), Unity, Unreal and others.
**Agent integration:** (a) Server modules are text code; the Godot client is GDScript. (b) Docker Compose for local runs; REST and gRPC APIs. (c) Console and client APIs. (d) Community MCP: `mlger/nakama-mcp` (Apache-2.0, last push 2026-09-05, 0 stars) wraps the client and console APIs in about 180 operations through a search-and-execute pattern, stdio or HTTP; the console API can change or delete data. A second community server exists (not checked). (e) None. (f) An agent can start the server in Docker and run client scripts against it; integration tests are plausible.
**Pros for agentic work:**
- Runs locally under Docker, so an agent can test without a cloud account.
- Server logic in TypeScript or Go is well-known to models.
**Cons for agentic work:**
- MCP servers are brand new and unstarred.
- Realtime behaviour still needs two clients to judge.
**Verdict:** High: local, text-based, scriptable backend.
**Sources:** https://heroiclabs.com/docs/nakama/ (VERIFIED); https://heroiclabs.com/pricing/ (VERIFIED); https://api.github.com/repos/heroiclabs/nakama (VERIFIED); https://api.github.com/repos/heroiclabs/nakama-godot (VERIFIED); https://api.github.com/repos/mlger/nakama-mcp (VERIFIED).

### Photon (Exit Games)
**What it is:** A family of hosted multiplayer products: Fusion, Quantum, Realtime, Chat, Voice, and the older PUN.
**Cost:** Realtime public cloud: free "development only" tier of 20 concurrent users and 60 GB traffic per month; paid launch plans from a one-time USD 95 (100 CCU, 12 months) to USD 95/month (500 CCU) and above (read today; page is Realtime pricing and does not give Fusion figures or mention Godot). Fusion is "free for development".
**Open source:** No (UNVERIFIED; cloud SDKs under Photon's licence).
**Extendable:** SDKs for Unity, Unreal and, as a preview, Godot.
**Agent integration:** (a) SDK files in `addons/`. (b) Fusion Godot SDK 3.0.0 Preview, build 684 (2026-10-26): "not intended for production use", Godot 4.6+, needs a Fusion 3 AppId from the web dashboard, GDExtension loaded after copying the `fusion/` folder. (c) Dashboard is a GUI. (d) No MCP server found (UNVERIFIED). (e) None. (f) Needs two running clients and a cloud app; an agent cannot easily prove netcode correct headless.
**Pros for agentic work:**
- Official Godot SDK now exists.
- Free development tier.
**Cons for agentic work:**
- Preview API may change.
- Account and AppId creation are manual; no agent route found.
**Verdict:** Low: preview SDK, dashboard-gated, no agent route.
**Sources:** https://doc.photonengine.com/ (VERIFIED); https://www.photonengine.com/pricing (VERIFIED); https://doc.photonengine.com/fusion-godot/v3-shared-authority/getting-started/sdk-download (VERIFIED).

### PlayFab (Microsoft)
**What it is:** Microsoft's hosted live-game backend: identity, economy, leaderboards, multiplayer servers, matchmaking and data.
**Cost:** Free development tier plus paid Standard and Premium plans (REPORTED via search snippets of Microsoft pages: free for 10 development-mode titles and 1,000 lifetime players per title; Standard USD 99/month; Premium USD 1,999/month; sources conflict on the free limit, 1,000 versus 100,000 players): check current terms at https://playfab.com/pricing/ (403 to me).
**Open source:** No. SDKs have their own licences (UNVERIFIED).
**Extendable:** SDKs for C/C++, C#, Java, JavaScript, Python; engine pages for Unity, Unreal and Cocos2d-x (Godot is not listed); REST API, Postman collection and an SDK generator (VERIFIED). Community Godot addon `Structed/godot-playfab` (MIT, 170 stars, last push 2026-06-18).
**Agent integration:** (a) Config in the dashboard; code in your repo. (b) REST API is scriptable. (c) API. (d) Community MCP only: `akiojin/playfab-mcp-server` (MIT, TypeScript, 3 stars, last push 2026-11-02): item search, segments, player profiles, inventory. It needs `PLAYFAB_TITLE_ID` and `PLAYFAB_DEV_SECRET_KEY`; the dev secret key is administrative power, so do not give it to an agent. No official MCP found (UNVERIFIED). (e) None. (f) Test titles in Development Mode.
**Pros for agentic work:**
- REST API and generated SDKs suit code generation.
- Microsoft's Xbox-Godot sample shows PlayFab with Godot 4.
**Cons for agentic work:**
- Not in the engine list for Godot; community addon.
- Dev secret key exposure; pricing numbers inconsistent across pages.
**Verdict:** Medium: complete API, but weak Godot support and a risky MCP.
**Sources:** https://learn.microsoft.com/en-us/gaming/playfab/ (VERIFIED); https://api.github.com/repos/akiojin/playfab-mcp-server (VERIFIED); https://api.github.com/search/repositories?q=playfab+godot&per_page=5 (VERIFIED); pricing via search results (REPORTED).

### Steam networking (Steam Networking Sockets, Messages and Datagram Relay)
**What it is:** Valve's networking APIs inside the Steamworks SDK: connection-based sockets, a UDP-like messages interface and a relay service.
**Cost:** The Steamworks documentation page does not say; usage presumes a Steam app (USD 100 per app, see above). Whether the relay has fees: UNVERIFIED.
**Open source:** The transport library `ValveSoftware/GameNetworkingSockets` is BSD-3-Clause, C++ with a C interface, and works without Steam ("Steam is not needed"); the Steam Datagram Relay network is unavailable outside Steam (VERIFIED, README). The Steamworks SDK is not open.
**Extendable:** Wrapped for Godot by GodotSteam (see Steam entry).
**Agent integration:** (a) C++/C or GodotSteam GDScript. (b) None. (c) API. (d) No MCP found (UNVERIFIED). (e) None. (f) Testing needs the Steam client, two accounts and a real or test app id; GameNetworkingSockets alone can be tested locally. Docs mention P2P with relay, SDR for dedicated servers to hide IPs and resist DoS, and the older `ISteamNetworking` as deprecated.
**Pros for agentic work:**
- The open library can be built and tested without Steam.
- GodotSteam makes it callable from GDScript.
**Cons for agentic work:**
- Full stack needs the Steam client and accounts, so no headless proof.
- GodotSteam's GitHub home just moved to Codeberg.
**Verdict:** Low: needs the Steam client, so an agent cannot verify it headless.
**Sources:** https://partner.steamgames.com/doc/features/multiplayer/networking (VERIFIED); https://github.com/ValveSoftware/GameNetworkingSockets (VERIFIED).

### GameAnalytics
**What it is:** A hosted game-analytics service with SDKs and dashboards.
**Cost:** A free tier exists with no monthly-active-user cap on the pricing page, but the column headings were not labelled in what I read, so which features are free is UNVERIFIED. Paid: AnalyticsIQ Pro USD 49/month, PipelineIQ from USD 499/month, MarketIQ USD 499/month (read today). The hosted MCP is reported to be part of PipelineIQ Pro (REPORTED).
**Open source:** The service is not. SDK `GameAnalytics/GA-SDK-GODOT` is MIT (65 stars, last push 2026-10-21). `GameAnalytics/GA-MCP` is Apache-2.0, but shows 0 stars and a last push of 2026-01-12.
**Extendable:** SDKs, Collection API, raw export and metrics API on higher tiers.
**Agent integration:** (a) SDK in your repo; settings in the dashboard. (b) None. (c) Metrics API. (d) Official MCP: a hosted server (sign in with your GameAnalytics account), a self-hosted open-source server (`pip install git+https://github.com/GameAnalytics/GA-MCP`, Metrics API key from PipelineIQ, run as `python3 -m ga_mcp.server`), and a Documentation MCP that can help an agent add the SDK. Docs list Claude Code and Codex among supported clients. Read-only versus write was not stated (UNVERIFIED). (e) A documentation assistant. (f) Events visible in the dashboard.
**Pros for agentic work:**
- Official MCP servers and an official Godot SDK.
- Docs MCP lowers the cost of integration.
**Cons for agentic work:**
- Metrics access is on paid tiers; the self-hosted repo looks quiet.
- Analytics data about players: mind privacy before sending to a model.
**Verdict:** High: official MCP servers and Godot SDK, with metrics behind a paid tier.
**Sources:** https://docs.gameanalytics.com/ai-tools/ai-tools-overview (VERIFIED); https://www.gameanalytics.com/pricing (VERIFIED); https://api.github.com/repos/GameAnalytics/GA-MCP (VERIFIED); https://api.github.com/search/repositories?q=GameAnalytics+godot+sdk&per_page=5 (VERIFIED).

---

## Summary table

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

## Cross-cutting cautions for students

- An MCP server is code that acts with your permissions. Prefer official servers; use read-only modes first; pin versions; never put admin keys (PlayFab dev secret, Steam, Apple `.p8`, itch.io API key, Unity password) where an agent can read them.
- A tool's exit code is a claim. Unity's test framework says it has no common exit-code definition, GUT ignores pending tests, Godot ignores unknown flags, and Unreal Insights' headless export is reported to exit cleanly while exporting nothing. Read the XML, CSV or artifact.
- Anything about how a frame looks, how a game feels, or whether two networked clients agree is a human check, whatever the tool.
- Text issue, PR, card or page content that an agent reads is untrusted input.
- Several free tiers changed in 2026 (Unity storage meter, Atlassian pricing, GitHub storage rules, GodotSteam's repository move). Re-check prices and terms before depending on them.
