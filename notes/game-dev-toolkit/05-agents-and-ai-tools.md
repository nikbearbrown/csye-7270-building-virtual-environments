# D. Coding agents and AI generation tools for games
*Part of the game-development toolkit note: see [README.md](README.md). Research date 2026-11-03.*

## Executive summary

**What this is.** Notes on nine coding agents, sixteen AI generation tools used for game assets, about 38 MCP servers for game tools, and the platform and legal rules for AI-generated assets (Steam, itch.io, Google Play, Epic, copyright).

**Why read it.** The agents are the tools the course teaches with. The AI generators and MCP servers decide what an agent can reach. The legal section decides what can be shipped.

**What it found.**
- Highest agent-friendliness: Claude Code, OpenAI Codex (Apache-2.0) and Cline (Apache-2.0) among agents; ComfyUI and Scenario among generators. Claude Code is not open source (all rights reserved).
- Gemini CLI stopped serving individual accounts on 2026-06-18 (free, AI Pro and AI Ultra; Google's own GitHub discussion confirms it). It still runs with a paid API key. Windsurf is now called Devin Desktop. Aider's last GitHub release was August 2025.
- No workable agent route: Midjourney (no official API), Suno and Udio.
- Meshy Free outputs are licensed CC BY 4.0 (attribution required) and Free has no API. ElevenLabs' official MCP repository is archived and a hosted server replaces it. Tripo's official MCP has had no push since April 2025.
- MCP comparison: official routes exist for Blender (Blender Lab), Unity (beta), Unreal (5.8, experimental), Figma and Adobe. No official server was found for Godot, Aseprite or Krita (an absence claim, UNVERIFIED).
- Steam asks developers to disclose AI-generated content that ships to players; itch.io has an AI disclosure tag. Apple, console and GOG rules were not checked.

**What it did not do.** Nothing was installed or run. About 55 claims are marked UNVERIFIED, many because the Midjourney, Tripo, Adobe, Scenario and Blender Lab pages returned errors. Prices are left out on purpose.

---

Researched 2026-11-03 for CSYE 7270 (Godot 4, Claude Code and Codex). "Read" below means fetched during this task on 2026-11-03. GitHub facts (licence, stars, last push, releases) come from the GitHub API through `gh api`, read-only. Prices are left out on purpose except where a free-tier allowance matters; check current terms before paying. Nothing was installed or run.

Source marks: VERIFIED = official page or repository read in this task. REPORTED = secondary source or a search-result summary. UNVERIFIED = could not check.

Two surprises worth knowing before you read on: (1) Gemini CLI stopped serving free individual accounts on 2026-06-18; (2) Windsurf is now called Devin Desktop.

---

# Part 1. Coding agents

### Claude Code
**What it is:** Anthropic's coding agent; a terminal CLI first, plus VS Code, JetBrains, desktop and web surfaces that share one engine.
**Cost:** Subscription (Pro, Max, Team, Enterprise; no Free plan) or pay-per-token via an Anthropic Console key; Bedrock, Vertex and Foundry also work. No free use. Commercial Terms are linked from the repo README; not read (UNVERIFIED). Plans: https://claude.com/pricing
**Open source:** No. The repo is public but `LICENSE.md` is "All rights reserved" (Anthropic).
**Extendable:** CLAUDE.md (also reads AGENTS.md), skills, hooks, subagents, plugins, MCP, and an Agent SDK in Python and TypeScript.
**Agent integration:** (a) It reads and writes plain text; it is the agent. (b) `claude -p` is headless, with `--output-format json|stream-json`, `--allowedTools`, `--permission-mode` (acceptEdits, auto, dontAsk), a non-zero exit on failure, and GitHub Actions and GitLab CI recipes. (c) Agent SDK. (d) MCP client: `claude mcp add`, scopes local/project/user, stdio and HTTP. Caution: a `-p` run loads a repo's `.mcp.json` and hooks with no trust dialog unless `--bare` is used. (f) It runs tests itself, but "done" is still its claim.
**Pros for agentic work:**
- Narrowest permission controls here (per-command allow/deny rules, modes, `dontAsk` for CI).
- Skills and hooks let a course ship its own rules and checks.
**Cons for agentic work:**
- Closed source; cost grows with long headless loops.
- Repo-supplied config (hooks, `.mcp.json`) runs in `-p` mode before any trust prompt.
**Verdict:** High: best mix of headless mode, narrow permissions and extension points.
**Sources:** VERIFIED https://code.claude.com/docs/en/overview ; https://code.claude.com/docs/en/headless ; https://code.claude.com/docs/en/mcp ; https://code.claude.com/docs/en/permissions ; https://raw.githubusercontent.com/anthropics/claude-code/main/LICENSE.md ; https://claude.com/pricing. Latest release v2.1.317, 2026-11-03 (VERIFIED, `gh api`).

### OpenAI Codex (CLI and cloud)
**What it is:** OpenAI's coding agent: an open-source Rust CLI, an IDE extension, a desktop app, and a cloud agent (Codex Web).
**Cost:** Included in ChatGPT plans (Free, Go, Plus, Pro, Business, Edu, Enterprise) with an allowance shared by local and cloud use; Free is limited (desktop app, one model, subject to rollout). Credits can be bought past the limit. An API key also works, without cloud features. Output terms not read (UNVERIFIED). https://learn.chatgpt.com/docs/pricing
**Open source:** Yes, Apache-2.0 (133k stars, pushed 2026-11-03, release rust-v0.166.0 on 2026-10-29).
**Extendable:** AGENTS.md (global plus per-directory, 32 KiB default cap), MCP, a GitHub Action, `.codex/config.toml`. Skills and subagents are linked from the docs but were not read (UNVERIFIED).
**Agent integration:** (a) plain text. (b) `codex exec`: read-only by default, `--sandbox workspace-write`, `--json` event stream, `--output-schema`, `-o` last message, `resume`. (c) n/a. (d) MCP client via `codex mcp add` or `config.toml`; stdio and streamable HTTP; per-tool approval modes. Caution: `http_headers_helper` runs a local command, and OAuth secrets can sit in `config.toml`. (f) OS sandbox: Seatbelt on macOS, bubblewrap on Linux; `danger-full-access` only in isolated containers.
**Pros for agentic work:**
- Real OS-level sandbox, default read-only in `exec`.
- Open source, so students can read how it works.
**Cons for agentic work:**
- Limits are shared and model-dependent; Free is thin.
- Local MCP servers may not exist in the cloud environment.
**Verdict:** High: open source, sandboxed, scriptable.
**Sources:** VERIFIED https://github.com/openai/codex ; https://learn.chatgpt.com/docs/codex/cli ; https://learn.chatgpt.com/docs/sandboxing ; https://learn.chatgpt.com/docs/non-interactive-mode ; https://learn.chatgpt.com/docs/extend/mcp ; https://learn.chatgpt.com/docs/agent-configuration/agents-md ; https://learn.chatgpt.com/docs/pricing

### Cursor
**What it is:** An AI code editor with an agent, a separate CLI (`agent`), and cloud agents.
**Cost:** Free plan with limited requests; paid tiers (Plus, Premium, Super, Ultra, Teams, Enterprise) draw from a usage pool that refreshes weekly; third-party models are billed at API list price on top. Commercial terms not read (UNVERIFIED). https://cursor.com/pricing
**Open source:** No public source found. The public `getcursor/cursor` repo has no licence (UNVERIFIED whether it holds only issues).
**Extendable:** Rules (`.cursor/rules/*.mdc`, AGENTS.md), MCP (`.cursor/mcp.json`); hooks, an Agent SDK and a cloud-agent API appear in the docs index but were not read.
**Agent integration:** (b) `agent -p` prints and exits; without `--force` it only proposes changes, with `--force` it edits files without asking; `CURSOR_API_KEY` for scripts; `json` and `stream-json` output; GitHub Actions page exists. (d) MCP client over stdio, SSE and streamable HTTP, OAuth for remote. Docs warn servers can execute code on your behalf. (f) A CLI permissions page exists but was not read (allow/deny rules UNVERIFIED).
**Pros for agentic work:**
- Reads AGENTS.md, so a course repo works in Cursor unchanged.
- Strong editor review of diffs.
**Cons for agentic work:**
- Closed source; pricing has changed shape and mixes in other vendors.
- Headless safety is a single `--force` switch in the page read.
**Verdict:** Medium: capable, but GUI-first and closed.
**Sources:** VERIFIED https://cursor.com/pricing ; https://cursor.com/docs/rules ; https://cursor.com/docs/mcp ; https://cursor.com/docs/cli/headless ; https://cursor.com/llms.txt

### GitHub Copilot (agent mode, CLI and cloud agent)
**What it is:** GitHub's assistant: agent mode in VS Code and other IDEs, a Copilot CLI, and a cloud coding agent that opens pull requests.
**Cost:** Free plan (agent mode with limited usage, Copilot CLI); Pro, Pro+, Max add credits, the cloud agent and more models; Business and Enterprise by contact. Usage counts in "GitHub AI Credits". Commercial terms not read (UNVERIFIED). https://github.com/features/copilot/plans
**Open source:** No. The `github/copilot-cli` repo is public but its licence lets you install, run and redistribute only unmodified copies (read).
**Extendable:** `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, AGENTS.md, and a root CLAUDE.md or GEMINI.md; custom agents, skills, hooks; MCP.
**Agent integration:** (b) Cloud agent runs in a cloud sandbox or GitHub Actions (59-minute cap on Actions runs). A `-p` flag for the CLI was not found in its README (UNVERIFIED). (d) MCP: agent mode uses configured servers; the GitHub MCP server ships by default in the CLI; for Business/Enterprise an org policy "MCP servers in Copilot" is off by default. VS Code asks you to trust a server before it starts. (f) VS Code can sandbox terminal commands; the CLI previews each action.
**Pros for agentic work:**
- Reads the other vendors' instruction files (AGENTS.md, CLAUDE.md, GEMINI.md).
- Pro+ can delegate to third-party agents.
**Cons for agentic work:**
- Three surfaces with different limits; the CLI licence is restrictive.
- Credit accounting is hard to predict.
**Verdict:** Medium: wide reach, but the headless story is weaker than Claude Code or Codex.
**Sources:** VERIFIED https://github.com/features/copilot/plans ; https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions ; https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp ; https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent ; https://github.com/github/copilot-cli ; https://code.visualstudio.com/docs/copilot/agents/overview

### Gemini CLI (and its successor, Antigravity CLI)
**What it is:** Google's open-source terminal agent for Gemini models.
**Cost:** Free individual access ended. On 2026-06-18 Gemini CLI stopped serving Google AI Pro/Ultra and free "Code Assist for individuals" accounts; those users were moved to Antigravity CLI (`agy`). Gemini CLI still works with paid Gemini API keys, Vertex AI, and Code Assist Standard/Enterprise licences. Whether Antigravity's free access suits commercial games: not stated (UNVERIFIED).
**Open source:** Yes, Apache-2.0 (109k stars, pushed 2026-11-03, v0.66.0 on 2026-10-27). Whether Antigravity CLI is open source: not stated (UNVERIFIED).
**Extendable:** GEMINI.md context files, MCP servers in `~/.gemini/settings.json`, extensions. Antigravity keeps skills, hooks, subagents and "Antigravity plugins", with no promise of full parity.
**Agent integration:** (b) `gemini -p` with `--output-format json` or `stream-json`. (d) MCP client. (f) A sandboxing guide is linked; its contents were not read (UNVERIFIED). Antigravity CLI is built in Go, runs asynchronous multi-agent work, and shares a harness with the Antigravity 2.0 desktop app. Whether it supports MCP and GEMINI.md was not stated (UNVERIFIED).
**Pros for agentic work:**
- Open source with headless JSON output.
- Google keeps it for paid API-key users.
**Cons for agentic work:**
- Students lose the old free route; instructions written in 2025 are stale.
- The successor's openness and MCP support are unconfirmed.
**Verdict:** Medium: good tool, but a student cannot assume free access.
**Sources:** VERIFIED https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ ; https://raw.githubusercontent.com/google-gemini/gemini-cli/main/README.md ; https://github.com/google-gemini/gemini-cli

### Windsurf (now Devin Desktop)
**What it is:** The former Windsurf AI editor, renamed Devin Desktop; its agent harness is shared with a Devin CLI.
**Cost:** Free plan (light quota, unlimited inline edits and Tab completions), then Pro, Max, Teams, Enterprise; extra usage at API pricing on Pro. Commercial terms not read (UNVERIFIED). The Devin site says "Devin Desktop is the new name for Windsurf"; windsurf.com redirects to devin.ai. https://devin.ai/pricing
**Open source:** No public source found (UNVERIFIED).
**Extendable:** MCP servers, rules and AGENTS.md (the docs page names them but the detail pages were not read), workflows, ACP (Agent Client Protocol). Config folder is still `~/.codeium/windsurf`.
**Agent integration:** (a) The docs say rules and AGENTS.md files customise the agent. (b) A headless or batch mode was not found (UNVERIFIED). (d) MCP client; no per-server detail read. (e) Built-in agent, "Fast Context" search, review tool; lead model can be paired with a cheaper helper. (f) Terminal-permission model not covered on the pages read (UNVERIFIED).
**Pros for agentic work:**
- Free plan exists; reads AGENTS.md.
- Can run local or cloud agent sessions.
**Cons for agentic work:**
- Product and docs mid-rename (windsurf.com now redirects to devin.ai); old guides mislead.
- No confirmed headless mode.
**Verdict:** Medium: usable editor agent, but unproven for scripted runs.
**Sources:** VERIFIED https://devin.ai/desktop ; https://devin.ai/pricing ; https://docs.devin.ai/desktop/getting-started . REPORTED https://livemy.app/blog/windsurf-pricing (rename date 2026-06-02).

### Cline
**What it is:** An open-source coding agent with a VS Code extension, JetBrains plugin, CLI, desktop app, and an SDK.
**Cost:** The software is free; you pay for model use through your own provider key, Cline's usage billing, or a flat "ClinePass" subscription. Local models (Ollama, LM Studio) work. Free for commercial use under the licence; model-provider terms apply.
**Open source:** Yes, Apache-2.0 (71k stars, pushed 2026-11-03, v4.1.26 on 2026-10-26).
**Extendable:** `.clinerules`, skills, MCP (`cline mcp`), SDK plugins that register tools and hooks.
**Agent integration:** (b) CLI installed with `npm i -g cline`; headless mode for CI with piped input and JSON output. (d) MCP client. (e) Plan mode (explore) and Act mode (execute). (f) By default every file edit and terminal command needs your approval; auto-approve is optional.
**Pros for agentic work:**
- Any model, including local; open source and scriptable.
- Per-action approval is the default.
**Cons for agentic work:**
- Quality depends on the model you plug in.
- Auto-approve settings are easy to over-widen (UNVERIFIED how fine-grained they are; the page read does not say).
**Verdict:** High: open, model-agnostic, headless.
**Sources:** VERIFIED https://github.com/cline/cline ; https://docs.cline.bot/getting-started/what-is-cline

### Aider
**What it is:** An open-source terminal pair-programming tool that edits files and commits to git.
**Cost:** Free software; you bring your own model key (or a local model), and pay the provider. No hosted plan found.
**Open source:** Yes, Apache-2.0 (50k stars). Maintenance is slow: latest GitHub release v0.86.0 on 2025-08-09; last push 2026-05-22.
**Extendable:** CONVENTIONS.md loaded with `--read` or `read:` in `.aider.conf.yml`; an unofficial Python API.
**Agent integration:** (a) plain text; every change is a git commit, easy to review and undo. (b) `--message`/`-m` runs one instruction and exits; `--yes`, `--dry-run`, env vars such as `AIDER_YES`. (c) The docs say the Python scripting API is "not officially supported". (d) No MCP client and no AGENTS.md appear in the release history page (checked); a community MCP server wraps Aider so Claude Code can call it (disler/aider-mcp-server, experimental, REPORTED). (f) Tests are run by you or by `--test-cmd` (UNVERIFIED, from memory, not checked).
**Pros for agentic work:**
- Git-first: small commits, easy rollback.
- Works with local models.
**Cons for agentic work:**
- No built-in MCP, sandbox or permission model.
- Slow release cadence; fewer agent features than 2026 peers.
**Verdict:** Medium: simple and scriptable, but not a full agent harness.
**Sources:** VERIFIED https://github.com/Aider-AI/aider ; https://aider.chat/docs/scripting.html ; https://aider.chat/docs/usage/conventions.html ; https://aider.chat/HISTORY.html . REPORTED https://lobehub.com/mcp/disler-aider-mcp-server

### JetBrains Junie
**What it is:** JetBrains's coding agent, as an IDE plugin, a Junie CLI, and a GitHub/GitLab CI integration.
**Cost:** Free "Junie Lite" listed, with AI usage billed separately; paid AI Pro and AI Ultra tiers give monthly AI credits with top-ups; bring-your-own-key works with 10+ models, including local ones. The page is ambiguous on free limits: check current terms. Authentication: JetBrains account, a Junie API key, or your own key.
**Open source:** No. The public `JetBrains/junie` repo says "All rights reserved"; use is under JetBrains AI Service terms (read). 531 stars, release 4003.1 on 2026-11-03.
**Extendable:** Guidelines/AGENTS.md, skills, MCP, GitHub Actions (`/install-github-action`).
**Agent integration:** (b) CLI with environment variables mirroring flags for CI, and `--act-as-interactive` for unattended runs (REPORTED from the official docs via search). (d) MCP servers live in `~/.junie/mcp/mcp.json` and project `.junie/mcp/`; a third-party issue alleges a CVE around a committed `.junie/mcp/mcp.json` stdio server (UNVERIFIED; the general lesson stands: committed MCP config can launch commands). AGENTS.md lookup order starts at `.junie/AGENTS.md` (REPORTED). (f) Permission/brave-mode detail not read (UNVERIFIED).
**Pros for agentic work:**
- Reads AGENTS.md; CLI runs outside the IDE; model-agnostic.
- Good fit if the course used Rider or IntelliJ.
**Cons for agentic work:**
- Closed, credit-based; little game-engine tooling for Godot.
- Docs I could read were thin; several claims rest on search summaries.
**Verdict:** Medium: capable but JetBrains-centric and closed.
**Sources:** VERIFIED https://junie.jetbrains.com/ ; https://github.com/JetBrains/junie ; https://raw.githubusercontent.com/JetBrains/junie/main/README.md . REPORTED https://junie.jetbrains.com/docs/guidelines-and-memory.html ; https://junie.jetbrains.com/docs/environment-variables.html (search summaries)

---

# Part 2. AI generation tools used for game assets

Each entry keeps the same headings. "Agent integration" here means: does an API, CLI or MCP server exist for an agent to call. "Cost" covers the free tier and whether free outputs are usable in a commercial game. Nothing here is legal advice; see Part 4.

### Midjourney
**What it is:** A hosted image (and video) generator used through its website and Discord.
**Cost:** Subscription. A current free tier or trial could not be confirmed (UNVERIFIED); reports say trial outputs are non-commercial (CC BY-NC) (REPORTED). Paid users own their assets, but a company with more than $1,000,000 gross annual revenue must be on the Pro or Mega plan (Midjourney docs, REPORTED via search summary because the docs page returned 403). Midjourney keeps a broad licence to your content, and content is public by default unless Stealth Mode (paid) is used.
**Open source:** No.
**Extendable:** No public plugin system found.
**Agent integration:** (b) No official public API found (REPORTED by vendor blogs, 2026; not confirmed on Midjourney's own pages, UNVERIFIED). Third-party "Midjourney API" wrappers exist; reports say they breach the terms and risk bans (REPORTED). (d) No official MCP server found.
**Pros for agentic work:**
- Strong concept art and moodboards done by a human.
- Clear ownership statement for paid plans.
**Cons for agentic work:**
- An agent cannot call it legitimately; scraping risks the account.
- Revenue-threshold rule and public-by-default outputs need tracking.
**Verdict:** Low: GUI/Discord only; no sanctioned agent route.
**Sources:** REPORTED https://docs.midjourney.com/hc/en-us/articles/27870375276557-Using-Images-Videos-Commercially (via search summary) ; https://www.cometapi.com/is-midjourney-free-what-to-know-now-a-2026-update/ ; https://terms.law/2026/01/15/midjourney-commercial-use-rights-complete-2026-guide/

### Adobe Firefly
**What it is:** Adobe's image, video and audio generation, in a web app and through the Firefly API (Firefly Services).
**Cost:** Free daily generations in the app; paid plans give monthly credits; standard image features are unlimited on paid plans while video, audio and partner models consume credits. Adobe says outputs of its own Firefly models are safe for commercial use (trained on licensed and public-domain content); for partner models the user judges suitability. IP indemnification is described for eligible enterprise customers only. API pricing not on the page read.
**Open source:** No.
**Extendable:** Firefly API: custom models (subject and style), composite, upscale, Image Model 5.
**Agent integration:** (b) REST API with custom-model training; authentication and pricing not described on the page read (UNVERIFIED). (d) A hosted Adobe connector for Claude ("Adobe for Claude", 50+ tools across Photoshop, Firefly, Express and others) launched 2026-04-28 (REPORTED; Adobe help page returned 403). No Firefly-specific MCP on the API page.
**Pros for agentic work:**
- Best-stated commercial-safety position among the image tools.
- Custom style models help keep a game's look consistent.
**Cons for agentic work:**
- API access and price unclear for students; enterprise leaning.
- Content Credentials are attached automatically (a plus for disclosure, a nuisance for pixel pipelines).
**Verdict:** Medium: safest licensing, but the API route is enterprise-shaped.
**Sources:** VERIFIED https://www.adobe.com/products/firefly/plans.html ; https://developer.adobe.com/firefly-services/docs/firefly-api/ . REPORTED https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector

### Stable Diffusion and ComfyUI
**What it is:** Open image models (Stability AI's Stable Diffusion family and many others) run locally, usually through ComfyUI, a node-graph tool with a server and API.
**Cost:** ComfyUI is free software (GPL-3.0) and runs offline on your own GPU. Stability's Community License lets organisations under US$1M annual revenue use covered models (SD 3.5 suite, SDXL Turbo, Stable Fast 3D, Stable Audio 3.0) free for commercial use; at $1M they must buy an Enterprise licence. Other checkpoints carry their own licences (not checked, UNVERIFIED).
**Open source:** ComfyUI yes (GPL-3.0, 145k stars, pushed 2026-11-03). Model weights vary: Stability's are "free under a revenue cap", not OSI open source.
**Extendable:** Custom nodes (Python), workflow JSON, partner API nodes that spend credits.
**Agent integration:** (b) HTTP `POST /prompt`, `GET /history/{id}`, `/queue`, `/interrupt`, and WebSocket `/ws`; `comfy-cli` (`comfy launch --background`, `comfy run --workflow x.json --wait`, `comfy validate`). (d) MCP: Comfy-Org/comfy-mcp (beta, 41 tools, wraps comfy-cli, 323 stars, pushed 2026-11-03; the README says AGPL-3.0-or-later OR Commercial while GitHub shows no SPDX id); artokun/comfyui-mcp (MIT, 888 stars, 2026-11-02); joenorton/comfyui-mcp-server (Apache-2.0, 412 stars, last push 2026-02-17). Caution: ComfyUI has no built-in authentication, partner nodes spend money, and custom nodes run arbitrary code.
**Pros for agentic work:**
- Fully scriptable and free to run; reproducible workflow files in git.
- Several MCP servers, one from Comfy-Org.
**Cons for agentic work:**
- Needs a capable GPU and model downloads; setup is heavy.
- Licence differs per model; the $1M cap and custom-node risk need policing.
**Verdict:** High: open, API-first, many agent routes.
**Sources:** VERIFIED https://stability.ai/license ; https://docs.comfy.org/development/comfyui-server/comms_routes ; https://docs.comfy.org/comfy-cli/getting-started ; https://github.com/comfyanonymous/ComfyUI ; https://raw.githubusercontent.com/Comfy-Org/comfy-mcp/main/README.md ; https://github.com/artokun/comfyui-mcp

### Scenario
**What it is:** A game-oriented generation platform: train a model on your own art, then generate images, video, 3D and audio.
**Cost:** 50 free daily credits with no card; paid monthly plans by credit bundle (Starter, Pro, Max, Enterprise). The only ownership sentence found ("You own what you generate") sits in the Enterprise section; whether it covers free and lower plans was not stated (UNVERIFIED). Terms page returned 404.
**Open source:** Platform no. The agent skills repo `scenario-labs/skills` is MIT (1,960 stars, pushed 2026-11-03); the Blender add-on `scenario-labs/blender-plugin` is GPL-3.0 (939 stars).
**Extendable:** REST API with TypeScript and Python SDKs, saved workflows, custom models, Blender plugin.
**Agent integration:** (b) REST API and SDKs. (d) An official "Scenario MCP" connects Claude, Codex or Cursor to your workspace (per the vendor page; repository and licence of the MCP itself not located, UNVERIFIED). Agent skills drive Blender, Maya and others (vendor repo). (f) Outputs are downloadable files.
**Pros for agentic work:**
- Built for game pipelines; style-consistent training.
- API, SDKs, MCP and skills all exist.
**Cons for agentic work:**
- Credit spend by an agent needs a cap.
- Licence statement for non-Enterprise plans is unclear.
**Verdict:** High: designed for game assets, with an MCP route.
**Sources:** VERIFIED https://www.scenario.com/ ; https://api.github.com/repos/scenario-labs/skills (via `gh api`)

### Layer
**What it is:** An AI asset-generation platform for game studios, with engine plugins.
**Cost:** Usage-based "Creative Units"; a "Start for free" option exists but the free allowance is not stated on the pages read (UNVERIFIED). The pricing page lists a commercial licence for studio subscriptions; who owns the outputs is not stated (UNVERIFIED). Customer data is said not to train foundation models.
**Open source:** No.
**Extendable:** REST API for models and workflows, typed TypeScript SDK, CLI, webhooks, scoped API keys.
**Agent integration:** (b) REST API, CLI and webhooks with async jobs. (d) The vendor page says an MCP server connects Claude and Claude Code; repository, licence and maintenance not found (UNVERIFIED). Unity, Unreal, Blender, Maya and Photoshop plugins are listed. The company page shows © 2026, so it appears active.
**Pros for agentic work:**
- CLI plus MCP plus engine plugins is the right shape for agents.
- Per-use pricing, no seats.
**Cons for agentic work:**
- Thin public detail on licence and free tier; small vendor risk.
- Godot plugin not listed (UNVERIFIED).
**Verdict:** Medium: right tooling, but terms and free tier unverified.
**Sources:** VERIFIED https://www.layer.ai/ ; https://www.layer.ai/pricing

### Meshy
**What it is:** A text-to-3D and image-to-3D generator with texturing, remeshing and animation.
**Cost:** Free plan: 100 credits a month (up to 10 asset generations), 10 downloads a month, and outputs under CC BY 4.0 (commercial use allowed with attribution). API access is not on the Free plan; Pro, Premium, Ultra and Studio include it. On paid plans the assets are private and customer-owned. MCP calls use credits at the REST rate.
**Open source:** Platform no; the MCP server is MIT.
**Extendable:** REST API; plugins for Blender, Unity, Maya; export GLB, FBX, OBJ, STL, USDZ, 3MF.
**Agent integration:** (b) REST API. (d) Official `meshy-dev/meshy-mcp-server` (MIT, 89 stars, pushed 2026-11-03), installed with `npx add-mcp @meshy-ai/meshy-mcp-server --env MESHY_API_KEY=...`; also a skill pack `meshy-dev/meshy-3d-agent`. Caution: the install example puts the API key on the command line, so it lands in shell history; downloads go to a `meshy_output` folder. Godot not listed. (f) Check meshes in Blender or Godot headless; topology and scale are human checks.
**Pros for agentic work:**
- Official MCP and a skill pack; clear plan-by-plan licence.
- Rigging and animation endpoints.
**Cons for agentic work:**
- Free outputs require attribution and no API; API needs a paid plan.
- Game-ready topology still needs a human pass.
**Verdict:** High: official MCP and clear licence rules.
**Sources:** VERIFIED https://www.meshy.ai/pricing ; https://docs.meshy.ai/en ; https://docs.meshy.ai/en/api/ai ; https://github.com/meshy-dev/meshy-mcp-server

### Tripo
**What it is:** A 3D generation service (text, image, multi-view to 3D) with texturing, retopology, auto-rig and animation.
**Cost:** API is usage-based credits (1 credit = $0.01, per the developer page read 2026-11-03). Web free tier: reported to be non-commercial with public models, free credits vary by source (REPORTED, the official pricing page returned 403, so UNVERIFIED). The API page states no output-licence terms (UNVERIFIED).
**Open source:** No; the MCP repo is MIT.
**Extendable:** REST API (`openapi.tripo3d.ai`, bearer key), webhooks, models for quad topology (P2.0), Blender add-on.
**Agent integration:** (b) REST API and a `tripo-cli` npm package that the page says an AI agent can install. (d) Official `tripo-mcp` (MIT, 225 stars, last push 2025-04-14, labelled alpha, works only with the Tripo Blender add-on, REPORTED); the repo now sits under `Tripo-Developer`. Unity/Unreal appear only as partner logos; Godot not mentioned.
**Pros for agentic work:**
- Cheap per-model API pricing; rig and animation endpoints.
- A CLI an agent can drive.
**Cons for agentic work:**
- The MCP server looks stale (no push in 18 months) and Blender-only.
- Free-tier licensing unclear and probably restrictive.
**Verdict:** Medium: API and CLI are good; MCP is stale.
**Sources:** VERIFIED https://developers.tripo3d.ai/ . REPORTED https://costbench.com/software/ai-3d-generation/tripo-ai/free-plan/ ; https://github.com/VAST-AI-Research/tripo-mcp

### Hyper3D Rodin
**What it is:** Deemos's Rodin 3D generator (text or image to 3D) with an API, a Blender add-on and an MCP feature.
**Cost:** A 7-day free trial and "free credits" are advertised; amounts not stated. Commercial use "depending on your plan and license"; the terms are not on the pages read (UNVERIFIED).
**Open source:** No.
**Extendable:** Async HTTP/JSON API with bearer key; credit pricing; Blender add-on (docs at docs.deemos.dev).
**Agent integration:** (b) HTTP API (VERIFIED). (d) The vendor home page says an MCP feature connects agents to Rodin's tools (repository not located, UNVERIFIED). The community Blender MCP server (`ahujasid/mcp-for-blender`, MIT, 33k stars) exposes Rodin as one of its `generate_3d` backends. Security: that server runs arbitrary Python in Blender; see Part 3.
**Pros for agentic work:**
- Documented API; shows up inside the most popular Blender MCP.
- Trial lets a class test without commitment.
**Cons for agentic work:**
- Licence and free-credit detail missing.
- Outputs still need cleanup for games.
**Verdict:** Medium: API is real, terms are unclear.
**Sources:** VERIFIED https://hyper3d.ai/ ; https://docs.hyper3d.ai/ ; https://github.com/ahujasid/blender-mcp

### Luma AI (API)
**What it is:** A video and image generation platform; the API serves Ray video models and a Uni image model.
**Cost:** Pay-per-use API, no commitment (a Scale tier for dedicated capacity); no free API allowance stated. Commercial terms not read (UNVERIFIED).
**Open source:** No.
**Extendable:** REST API; models listed are Ray3.2 (text/image/video to video, reframing) and Uni-1.1 images.
**Agent integration:** (b) API available. (d) No MCP or CLI mentioned on the page. (e) The API page does not mention 3D generation or 3D capture, so a Luma route to game meshes is not supported there (the page lists image and video only).
**Pros for agentic work:**
- Straightforward pay-per-use API; HDR and EXR options for video.
- Useful for trailers and concept animatics.
**Cons for agentic work:**
- No 3D asset route on the API page; not a model source for Godot.
- No MCP.
**Verdict:** Medium: API yes, but not a 3D or in-engine asset tool.
**Sources:** VERIFIED https://lumalabs.ai/api

### ElevenLabs
**What it is:** Speech, sound-effect and music generation (text-to-speech, speech-to-text, sound effects, music, dubbing, voice agents).
**Cost:** Free plan with 10,000 credits a month, three Studio projects; Music and Sound Effects are Free features, but "Commercial License" is listed as an add-on from the Starter plan, so treat Free outputs as non-commercial. Music costs about 900 credits per minute, sound effects about 200 per generation (page, 2026-11-03). API access on Free not stated (UNVERIFIED).
**Open source:** No; the MCP repo is MIT.
**Extendable:** SDKs (`pip install elevenlabs`, `npm install @elevenlabs/elevenlabs-js`), CLI `elevenlabs`, agent onboarding command `npx -y @elevenlabs/cli@latest onboard init`.
**Agent integration:** (b) API, SDKs and CLI. (d) Official `elevenlabs/elevenlabs-mcp` (MIT, 1,546 stars) is archived since 2026-08-20 and deprecated in favour of the hosted server `https://api.elevenlabs.io/v1/mcp` (OAuth), per the repo notice. Credits are spent on every call; the old local server put the API key in client config.
**Pros for agentic work:**
- Complete route: API, SDK, CLI, hosted MCP.
- Sound effects and music in one place.
**Cons for agentic work:**
- Commercial licence needs a paid plan.
- Old tutorials point at the archived local MCP server.
**Verdict:** High: API, CLI and an official hosted MCP.
**Sources:** VERIFIED https://elevenlabs.io/pricing ; https://elevenlabs.io/docs/overview/intro ; https://github.com/elevenlabs/elevenlabs-mcp

### Suno
**What it is:** A text-to-song generator (vocals and instruments).
**Cost:** Free: 50 credits a day, "no commercial rights"; Pro and Premier include commercial rights; the page says the terms contain "limitations on commercial use" (terms not read, UNVERIFIED).
**Open source:** No.
**Extendable:** None public.
**Agent integration:** (b) No public API. A developer-API partner programme was announced on 2026-07-01 for a small curated group (REPORTED, Digital Music News), with no published documentation or launch date. Unofficial wrappers carry terms and reliability risk (REPORTED). (d) No official MCP or CLI found.
**Pros for agentic work:**
- Fast, strong song-length results by hand.
- Clear plan rule: paid for commercial rights.
**Cons for agentic work:**
- No agent route.
- Commercial limits in the terms are unread; vocals are risky to ship.
**Verdict:** Low: no public API, rights need a close read.
**Sources:** VERIFIED https://suno.com/pricing . REPORTED https://www.digitalmusicnews.com/2026/07/03/suno-is-opening-an-api-partner-program/

### Udio
**What it is:** A text-to-music generator, now in transition after a settlement with Universal Music.
**Cost:** Unknown current plans (UNVERIFIED). After the October 2025 settlement the product was reported to become a "walled garden" with downloads switched off ahead of a licensed platform planned for 2026 (REPORTED); whether that platform has launched could not be confirmed.
**Open source:** No.
**Extendable:** None found.
**Agent integration:** No API, CLI or MCP found. Commercial licence for any new output: unknown, so assume it cannot be shipped until terms are read (UNVERIFIED).
**Pros for agentic work:**
- Interesting licensed-training direction.
**Cons for agentic work:**
- Output export reported as blocked; no agent route.
- Rights status unclear.
**Verdict:** Low: no API and, as reported, no downloads.
**Sources:** REPORTED https://djmag.com/news/universal-music-settles-ai-firm-udio-lawsuit-deal-struck-create-new-platform ; https://www.digitalmusicnews.com/2025/10/29/umg-udio-deal-everything-we-know/

### Stable Audio
**What it is:** Stability AI's audio and music models (Stable Audio 3.0 Large, Medium, Small and Small SFX).
**Cost:** Medium and Small/Small SFX are offered with open weights; Large is enterprise grade. Stability's Community License (free for commercial use under $1M annual revenue) lists Stable Audio 3.0 as covered. Stability says the models are trained on licensed data and offers indemnification under its Enterprise licence. A free API allowance is not stated (UNVERIFIED).
**Open source:** Partly: open weights under the Community License, which is revenue-capped, not OSI open source.
**Extendable:** Run weights locally; use the Stability Platform API.
**Agent integration:** (b) Hosted API on the Stability Platform; local weights can be scripted. (d) No CLI or MCP found for Stable Audio specifically (absence not proven, UNVERIFIED). (f) Listening to results is a human check.
**Pros for agentic work:**
- Most clearly licensed audio model here; runs locally.
- Small SFX model fits game sound effects.
**Cons for agentic work:**
- No MCP route found; you build the glue.
- Revenue cap applies once a studio passes $1M.
**Verdict:** Medium: cleanest rights, little agent plumbing.
**Sources:** VERIFIED https://stability.ai/stable-audio ; https://stability.ai/license

### Runway
**What it is:** A video, image and audio generation platform with a developer API; it also exposes third-party models.
**Cost:** Free plan: 125 one-time credits, limited tools, 5 GB storage, watermarked video. Paid tiers remove the watermark. Runway's help centre says you own and may commercially use what you make, including on Free (REPORTED search summary); the Terms also give Runway a broad licence to inputs and outputs, including for training (REPORTED). API and Enterprise use separate terms (REPORTED).
**Open source:** No.
**Extendable:** REST API with Node (`@runwayml/sdk`) and Python (`runwayml`) SDKs.
**Agent integration:** (b) API and SDKs; model catalogue includes Kling, Seedance, Aleph and GPT Image (docs page). (d) The docs have a "Connect the MCP only" guide and a plugin for Codex, Cursor and Claude Code; the MCP repository and licence were not located (UNVERIFIED). Free-tier API allowance not stated (UNVERIFIED).
**Pros for agentic work:**
- Official SDKs and an official MCP/plugin route.
- C2PA credentials on outputs.
**Cons for agentic work:**
- Video focus; limited direct value for engine assets beyond cutscenes and animatics.
- Training licence in the consumer Terms.
**Verdict:** High: SDKs and MCP, clear commercial statement.
**Sources:** VERIFIED https://docs.dev.runwayml.com/ ; https://runway.com/pricing . REPORTED https://help.runwayml.com/hc/en-us/articles/21668707517587-Can-I-use-the-content-I-made-in-Runway-for-commercial-purposes

### Higgsfield
**What it is:** An image and video generation hub exposing 30+ models.
**Cost:** The pricing page mentions free-tier credits and plan-dependent commercial rights, but gives no detail (UNVERIFIED). MCP use needs a paid plan and spends plan credits (REPORTED, third-party guides).
**Open source:** No. Community MCP servers exist (Hikhakk/higgsfield-mcp-unified, jfikrat/higgsfield-mcp) that are not Higgsfield's own (REPORTED); not reviewed.
**Extendable:** Hosted MCP, a CLI package, bundles for After Effects, Blender, Premiere, Photoshop and others (vendor page).
**Agent integration:** (d) Hosted MCP at `https://mcp.higgsfield.ai/mcp`, "no API key required" (vendor page); guides say it signs in with OAuth and the Claude Code command is `claude mcp add higgsfield https://mcp.higgsfield.ai/mcp` (REPORTED; the exact URL differs between guides). An official `@higgsfield/cli` is reported (REPORTED). (b) A public REST API was not found (UNVERIFIED).
**Pros for agentic work:**
- No key handling; works from Claude Code.
- Many video models behind one connector.
**Cons for agentic work:**
- Paid; credit burn from loops.
- Rights vary by plan and are not spelled out.
**Verdict:** Medium: easy agent route, licensing detail missing.
**Sources:** VERIFIED https://higgsfield.ai/mcp ; https://higgsfield.ai/pricing . REPORTED https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it

### Inworld (NPC voice and dialogue)
**What it is:** Today Inworld's pages describe Voice (text-to-speech, speech-to-text, a realtime voice-agent API) and Inference (text, image, video and decision models behind one API key); the older NPC "character engine" is not on the pages read.
**Cost:** On-Demand plan at $0, pay as you go: up to 70 minutes of text-to-speech, 100 custom voices, 2 professional voice clones, 100+ LLMs; the plan page says a commercial licence is included. Paid plans sell credits that roll over for up to three months.
**Open source:** No.
**Extendable:** API on every plan; docs MCP server; `npm install -g @inworld/cli`; a copyable "Inworld skill" for coding assistants.
**Agent integration:** (b) API and CLI. (d) The docs include a docs MCP server (it serves documentation, not generation, per the description; UNVERIFIED in detail). Unity and Unreal SDKs were not mentioned on the pages read (UNVERIFIED whether older ones remain). Similar options such as ElevenLabs agents cover the same role; not compared. (f) Listening and in-game latency are human checks.
**Pros for agentic work:**
- Free, commercially licensed tier for prototyping voices.
- API, CLI and a skill an agent can install.
**Cons for agentic work:**
- Product direction moved to voice and inference; older NPC tooling is unclear.
- Live-generated dialogue triggers Steam's live-generated disclosure and guardrail rules (Part 4).
**Verdict:** Medium: usable voice API, unclear engine support.
**Sources:** VERIFIED https://inworld.ai/pricing ; https://docs.inworld.ai/

---

# Part 3. MCP servers for game tools (comparison)

Facts from `gh api` on 2026-11-03: licence, stars, "last push" (the date of the newest push to any branch, close to last commit). "Official" means published by the tool's vendor. Do not install without reading the code: every server below can change files, and several execute code you did not write. Claude Code's docs say to trust each server first and note that servers fetching external content bring prompt-injection risk.

| Tool | Server | Official? | Repository | Licence | Last push | Stars | What it does | Security caution |
|---|---|---|---|---|---|---|---|---|
| Blender | Blender Lab MCP | Yes (Blender Lab) | https://projects.blender.org/lab/blender_mcp (page returned 403; repo details UNVERIFIED) | Not stated on the Blender page (UNVERIFIED) | UNVERIFIED (add-on v1.0.3; page images dated March 2026) | n/a | Natural-language interface to Blender's Python API; scene analysis, debugging, geometry-nodes docs; Blender 5.1+ | Page says it runs LLM-written code "without any guards"; use a VM |
| Blender | mcp-for-blender (formerly blender-mcp) | No (community) | https://github.com/ahujasid/blender-mcp | MIT | 2026-10-29 | 33,192 | Run Python in Blender, viewport `look`, asset search (Poly Haven, Sketchfab), `generate_3d` (Tripo, Hunyuan3D, Rodin, Meshy) | README: arbitrary code is "potentially dangerous"; add-on socket has no authentication; minimal anonymous telemetry on by default |
| Godot | godot-ai (hi-godot) | No (community) | https://github.com/hi-godot/godot-ai | MIT | 2026-11-03 | 3,375 | Add-on plus Python server (via `uv`); 46 tools, 120+ operations; needs Godot 4.7+; scene test-suite prompt | Signed releases, loopback WebSocket, writes confined to the project; "provided as is"; arbitrary-script execution not stated (UNVERIFIED) |
| Godot | godot-mcp (Coding-Solo) | No | https://github.com/Coding-Solo/godot-mcp | MIT | 2026-04-16 | 6,491 | Launch the editor, run projects, capture debug output | 75 open issues; no push in ~6.5 months |
| Godot | godot-mcp (tugcantopaloglu) | No | https://github.com/tugcantopaloglu/godot-mcp | MIT | 2026-10-09 | 509 | 157 tools, GDScript and C# (repo description) | Large tool surface; review before use |
| Godot | godot-mcp-pro | No (paid) | https://github.com/youichi-uda/godot-mcp-pro | NOASSERTION (paid, one-time fee per description) | 2026-09-24 | 641 | 162 tools for Godot 4 | Closed terms; read licence |
| Godot | Godot-MCP (ee0pdt) | No | https://github.com/ee0pdt/Godot-MCP | MIT | 2025-03-19 | 621 | Create and edit Godot games | Stale (no push in 19 months) |
| Unity | Unity MCP Server in AI Assistant package | Yes (Unity) | https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.17/manual/integration/unity-mcp-get-started.html | Closed (package); UNVERIFIED terms | Pre-release 2.17.0-pre.1 | n/a | Unity 6+ bridge, relay binary in `~/.unity/relay/`; tools like ManageScene, ManageGameObject, ReadConsole; works with Claude Code, Cursor, Windsurf, Claude Desktop | Open beta, needs an active Unity AI trial or subscription; first connection needs approval |
| Unity | unity-mcp (CoplayDev) | No | https://github.com/CoplayDev/unity-mcp | MIT | 2026-10-30 | 15,677 | Python server plus C# editor tools; custom tools | 127 open issues; editor-level access |
| Unity | Unity-MCP (IvanMurzak) | No | https://github.com/IvanMurzak/Unity-MCP | Apache-2.0 | 2026-11-03 | 4,576 | Any C# method can become a tool; CLI; Docker or .NET server; 71 tools (REPORTED) | Downloads a server binary from GitHub Releases at plugin start |
| Unity | mcp-unity (CoderGamester) | No | https://github.com/CoderGamester/mcp-unity | MIT | 2026-10-11 | 2,013 | Connects the Unity editor to IDE agents | Review before use |
| Unreal | Epic MCP plugin (UE 5.8) | Yes (Epic) | https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274 | Engine licence (UNVERIFIED) | UE 5.8 release (June 2026, REPORTED) | n/a | Epic says it "connects LLMs directly to Unreal Engine"; asset creation, testing | Experimental per a developer write-up (REPORTED); a user reports toolset registries must be enabled by hand (unverified user report) |
| Unreal | Unreal_mcp (ChiR24) | No | https://github.com/ChiR24/Unreal_mcp | MIT | 2026-10-30 | 1,004 | TypeScript server plus native C++ Automation Bridge plugin; UE 5.0-5.8 (REPORTED) | Full editor control |
| Unreal | VibeUE | No | https://github.com/kevinpbuckley/VibeUE | MIT | 2026-11-01 | 808 | Toolset on top of Epic's MCP in 5.8+ (REPORTED) | Depends on Epic's experimental plugin |
| Unreal | ue-mcp (db-lyon) | No | https://github.com/db-lyon/ue-mcp | MIT | 2026-11-03 | 468 | Unreal toolkit exposed as MCP tools | 109 open issues |
| Unreal | unreal-engine-mcp (flopperam) | No (vendor-owned) | https://github.com/flopperam/unreal-engine-mcp | None listed | 2026-06-26 | 1,116 | Description says it is now owned by Aura, an AI agent for Unreal | No licence, promotional ownership; check terms |
| Unreal | unreal-mcp (chongdashu) | No | https://github.com/chongdashu/unreal-mcp | None listed | 2025-04-22 | 2,111 | Natural-language Unreal control | No licence, stale |
| Unreal | unreal-mcp (runreal) | No | https://github.com/runreal/unreal-mcp | MIT | 2025-06-06 | 117 | Uses Unreal Python Remote Execution (UE 5.4+) | README: agents get full Editor access; stale |
| Figma | Figma MCP server (remote) | Yes (Figma) | https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server | Hosted service | Live service | n/a | `https://mcp.figma.com/mcp`; reads design context, variables, components; write tools for Design, FigJam, Slides | Writing is "free during the beta" then usage-priced; writes outside drafts need a Full seat; roughly two dozen clients incl. Claude Code, Codex, Gemini CLI |
| Figma | Figma Context MCP (Framelink) | No | https://github.com/GLips/Figma-Context-MCP | MIT | 2026-10-27 | 16,148 | Gives coding agents Figma layout information | Needs a Figma token |
| Figma | figma-console-mcp (southleft) | No | https://github.com/southleft/figma-console-mcp | MIT | 2026-10-29 | 2,665 | Design-system extraction, creation, debugging | Plugin-level write access |
| Figma | cursor-talk-to-figma-mcp (Grab) | No | https://github.com/grab/cursor-talk-to-figma-mcp | MIT | 2026-07-26 | 7,075 | Read and modify designs from agents | 97 open issues |
| Aseprite | aseprite-mcp (diivi) | No | https://github.com/diivi/aseprite-mcp | MIT | 2026-10-21 | 877 | MCP server over the Aseprite API | Review scripts it generates |
| Aseprite | aseprite-ai-artist (with-pebbly) | No | https://github.com/with-pebbly/aseprite-ai-artist | MIT | 2026-10-22 | 560 | Agent draws in an open Aseprite window; MCP plus skills | Live-editor control |
| Aseprite | pixel-mcp (willibrandon) | No | https://github.com/willibrandon/pixel-mcp | MIT | 2025-10-18 | 157 | Go server; shading, spritesheet export | Stale ~12 months |
| Aseprite | aseprite-mcp (letsagents) | No | https://github.com/letsagents/aseprite-mcp | MIT | 2026-08-11 | 0 | 76 tools, drives Aseprite headlessly via generated Lua (REPORTED) | Zero stars; unproven |
| Krita | krita-mcp (nanayax3) | No | https://github.com/nanayax3/krita-mcp | MIT | 2026-02-26 | 51 | AI paints in Krita via MCP | Small; ~8 months old |
| Krita | krita-mcp (SanSaSane) | No | https://github.com/SanSaSane/krita-mcp | CC0-1.0 | 2026-10-23 | 11 | Reads canvas back as PNG | Very new, tiny |
| Krita | krita-codex-mcp (cyyprezz) | No | https://github.com/cyyprezz/krita-codex-mcp | MIT | 2026-10-23 | 11 | Control Krita from Codex | Very new, tiny |
| Photoshop | Adobe for Claude connector | Yes (Adobe) | https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector | Hosted service | Launched 2026-04-28 (REPORTED) | n/a | 50+ tools across Photoshop, Illustrator, Firefly, Express and more, per the blog summary; lists Claude Code (REPORTED) | Needs a Claude account and Adobe sign-in; Teams-plan admins reported blocks (REPORTED); Adobe pages returned 403, so details UNVERIFIED |
| Photoshop | photoshop-mcp (alisaitteke) | No | https://github.com/alisaitteke/photoshop-mcp | MIT | 2026-11-01 | 796 | 118 tools (description); Photoshop must be running | Controls a desktop app with your files |
| Photoshop | adb-mcp (mikechambers) | No | https://github.com/mikechambers/adb-mcp | MIT | 2026-07-08 | 737 | Photoshop and Premiere via a UXP plugin and a proxy server | Local proxy; review |
| Photoshop | photoshop-python-api-mcp-server (loonghao) | No | https://github.com/loonghao/photoshop-python-api-mcp-server | MIT | 2026-10-17 | 346 | Wraps Photoshop's Python API; Windows only (REPORTED) | Windows-only |

Maturity notes. Blender, Unity and Figma have both an official and a popular community route. Godot has no official server I could find (an absence claim, UNVERIFIED). Krita servers are all under 100 stars and none is official. For the course: Blender (bpy script or the official Lab server), Godot (a maintained community server, or no MCP at all with `--headless` scripts), Figma (official remote server) are the best-supported; Krita and Aseprite are experimental.

---

# Part 4. Platform and legal rules for AI-generated assets

This is a summary of rules read on 2026-11-03, not legal advice. Rules change; re-read before shipping.

**Steam (Valve).** The Steamworks Content Survey has an AI section. Disclose AI-created content that ships with the game and reaches players (art, sound, narrative, localisation). The page says it does not cover "efficiency" tools used only in development, so a coding agent that only wrote your scripts is outside it (VERIFIED, Steamworks; a January 2026 clarification narrowed the scope, REPORTED). Two categories: pre-generated (made in development, ships in the game) means you promise no illegal or infringing content and that the game matches its marketing; Valve reviews it like any other content. Live-generated (made while the game runs, for example an NPC that generates dialogue) adds a duty to describe guardrails against illegal content. Valve said in January 2024 that it will show the disclosure on store pages and that players can report content via the overlay (VERIFIED, Video Games Chronicle, 2024-01-10). The Steamworks page does not itself say how disclosures are shown.

**itch.io.** Creators tag a project in an "AI Disclosure" section if it contains materials produced by generative AI. Self-contained algorithms without large external datasets (pathfinding, procedural level generation, dynamic difficulty) need no tag. Tagged projects appear on an "AI Assisted" browse page. Not tagging asset, soundtrack, physical-game, comic and book pages "may result in delisting"; excessive AI-generated content may be removed from browse as spam (VERIFIED, itch.io quality guidelines).

**Epic Games Store.** No announced AI-disclosure requirement, as of October 2026; Tim Sweeney has publicly criticised Steam's labels (REPORTED, news coverage; no Epic policy page read).

**Google Play.** Apps that generate content with generative AI must follow the developer policies, prevent restricted content, and provide in-app reporting or flagging, then use the reports to improve filtering (VERIFIED, Play policy page). The page does not separate pre-generated from live-generated content.

**Not checked:** Apple App Store, Xbox, PlayStation, Nintendo and GOG rules (UNVERIFIED).

**Copyright.** The US Copyright Office's Part 2 report on copyrightability (2025-01-29, date VERIFIED) is summarised by law firms as: protection needs human authorship, prompts alone are not enough, and selection, arrangement and your own modifications can qualify (REPORTED; the copyright.gov page read gives the date and the registration-guidance link but not those conclusions). Practical consequence for a course: pure model output may not be protectable, so keep human-made work around it.

**Tool-licence traps seen above.** Meshy Free outputs are CC BY 4.0 (attribution). Midjourney needs Pro or Mega over $1M revenue. Stability's Community License caps at $1M revenue. ElevenLabs Free and Suno Free carry no commercial rights. Tripo's Free web tier is reported non-commercial. Runway Free video is watermarked. Keep an asset ledger: tool, plan at the time, date, prompt, terms link, and whether the asset ships to players (that last column answers the Steam question).

**Sources:** VERIFIED https://partner.steamgames.com/doc/gettingstarted/contentsurvey ; https://www.videogameschronicle.com/news/steam-pages-will-now-disclose-which-games-use-ai-generated-content/ ; https://itch.io/docs/creators/quality-guidelines ; https://support.google.com/googleplay/android-developer/answer/13985936 ; https://www.copyright.gov/ai/ . REPORTED https://www.notebookcheck.net/Epic-CEO-Tim-Sweeney-lambasts-abhorrent-Steam-AI-Disclosure-Policy-claiming-labels-double-as-political-statement.1433682.0.html ; https://copyrightalliance.org/ai-report-part-2-copyrightability/ ; https://ipwatchdog.com/2025/01/29/part-two-copyright-office-ai-report-says-creative-prompting-doesnt-constitute-authorship/

---

# Summary table

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
