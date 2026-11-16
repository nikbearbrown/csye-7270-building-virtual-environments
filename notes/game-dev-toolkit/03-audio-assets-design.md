# C1. Audio tools, asset sources and design/UI tools, judged for agentic programming
*Part of the game-development toolkit note: see [README.md](README.md). Research date 2026-11-03.*

Research date: 2026-11-03. Every claim below was checked that day unless it carries the word UNVERIFIED. "VERIFIED" in a Sources line means the page or repository was read during this task; "REPORTED" means a search-result summary or a secondary page. Star counts and "last push" dates come from the GitHub API on 2026-11-03 and are only a rough maturity signal.

## Executive summary

- **Best agent baseline for audio is a command line, not a DAW.** FFmpeg (plus ffprobe) can convert, trim, loudness-measure and JSON-report on audio with no GUI. jsfxr gives a text-parameter sound-effect generator with a Node CLI. REAPER is the only DAW with plain-text projects, a full scripting API and a render-and-exit command line.
- **Audio middleware (FMOD, Wwise) is drivable only through community MCP servers**, all small, all driving a running GUI app over a local socket. There is no official MCP server from either vendor (none found). Free licences exist for small projects, but FMOD requires an in-game credit line and logo.
- **Audacity just lost its scripting door.** Audacity 4.0.0 (2026-09-03) ships without the scripting pipe that every Audacity MCP server uses; they work only on 3.x, and need a running GUI.
- **Asset marketplaces mostly have no agent route at all.** Fab, Unity Asset Store, OpenGameArt and itch.io have no documented download API. The agent-friendly sources are Poly Haven (open JSON API, CC0), Freesound (API with licence filters, but original downloads need OAuth2 and the API is free for non-commercial use only), Sketchfab (Download API with per-user OAuth) and Kenney (CC0 zips, no API).
- **The legal record matters more than the download.** CC0 needs no credit; CC-BY needs credit; CC-BY-SA, CC-BY-NC and store EULAs add traps. Section "Asset licence ledger" lists exactly what an agent must write down for every file.
- **Figma has the strongest official agent story in this whole note**: a hosted, official MCP server with 41 documented tools, 14 of them writing, including `use_figma`, which runs Plugin API code in your file. It is gated by seat, plan and rate limits, and its write-to-canvas feature is in beta. Students get Professional-tier limits through the free Education plan.
- **Sites that block automated fetching** (HTTP 403 in this research): Audiokinetic (Wwise), Fab, the OpenGameArt FAQ via the default fetcher. An agent told to "just read the licence page" may not be able to; plan for a human to paste licence text.

---

## Part 1. Audio tools

### FMOD Studio
**What it is:** Proprietary audio middleware: a desktop authoring tool (FMOD Studio) that builds event and bank files, plus the FMOD Engine runtime that plays them inside the game.
**Cost:** Free commercial use under the Indie licence when the development budget is under $600k and company revenue is under $200k a year; a per-title fee applies above the revenue line, and higher tiers start at $600k (read in the licensing page source on 2026-11-03; check current terms). The project must be registered, and shipped games must show an in-app credit line and the FMOD logo at startup unless a logo waiver is bought. The registration form also has non-commercial and student categories. Terms: https://www.fmod.com/licensing
**Open source:** No (source code is an extra-fee option on Premium licences).
**Extendable:** JavaScript scripting API inside Studio (menu commands, project edits, builds); plug-in SDK for custom DSP (UNVERIFIED); community Godot bindings.
**Agent integration:** (a) Project is a folder of metadata files that teams commit (REPORTED: community repos commit `.fmod/Metadata` XML); source audio and built banks are binary. (b) Release notes mention an `fmodstudiocl` command-line tool added for macOS in 2.03.13 (REPORTED); its flags are UNVERIFIED. (c) `studio.project.build()` takes banks and platforms and returns true or false (2.02 docs, VERIFIED); scripts run inside the open editor. (d) MCP: `EYamanS/fmod-studio-mcp`, community, MIT, 17 stars, last push 2026-10-12, README says alpha, about 148 tools generated from the Scripting API; install `claude mcp add fmod-studio -- uvx fmod-studio-mcp`. It needs Studio open with the Script Server on (TCP 127.0.0.1:3663, off by default). Caution: that server evaluates any JavaScript it receives and the README mentions no authentication. Godot: community `utopia-rise/fmod-gdextension` (MIT, 950 stars, pushed 2026-11-03). (e) None. (f) A build success flag and game logs are checkable; how it sounds is a human check.
**Pros for agentic work:**
- Documented scripting API with build, create, save and lookup.
- A live-editing MCP server exists, MIT-licensed.
**Cons for agentic work:**
- MCP route needs the GUI open, an unauthenticated JavaScript socket, and is alpha.
- Free licence carries credit-line and logo duties an agent must not forget.
- No verified headless build command.
**Verdict:** Medium. Real scripting API plus a community MCP, but a GUI app with an unauthenticated eval socket.
**Sources:** https://www.fmod.com/licensing (VERIFIED, read from the page's JavaScript bundle at https://www.fmod.com/bundle.js because the page is client-rendered); https://d1s9dnlmdewoh1.cloudfront.net/2.02/studio/scripting-api-reference-project.html (VERIFIED); https://github.com/EYamanS/fmod-studio-mcp and its README (VERIFIED); https://pypi.org/pypi/fmod-studio-mcp/json (VERIFIED, v0.1.0 uploaded 2026-07-02); https://api.github.com/repos/utopia-rise/fmod-gdextension (VERIFIED); FMOD revision-history and community `.gitignore` pages (REPORTED, search excerpts).

### Wwise
**What it is:** Audiokinetic's proprietary game-audio middleware: the Wwise Authoring app builds SoundBanks that the Wwise runtime plays in engines.
**Cost:** A free Indie plan exists. REPORTED (search excerpt of the Audiokinetic pricing page; the page itself returned HTTP 403): production budget under $250K and no asset limit; the free trial and unregistered use are non-commercial and capped at 200 media assets. Check current terms: https://www.audiokinetic.com/pricing
**Open source:** No (the community Godot integration is separate and has its own licence, shown as "Other" by GitHub).
**Extendable:** Wwise Authoring API (WAAPI, WAMP protocol), C++ plug-in SDK (UNVERIFIED), command-line WwiseConsole.
**Agent integration:** (a) Project (`.wproj`) and work-unit (`.wwu`) files are meant to be committed (REPORTED from Audiokinetic's version-control guidance); WAV sources and `.bnk`/`.wem` banks are binary. (b) `WwiseConsole generate-soundbank <project>.wproj --platform ...` builds banks without opening the authoring UI (REPORTED from Audiokinetic Q&A threads). (c) WAAPI lets scripts do most of what the editor does while Authoring runs with WAAPI enabled; a Python client `waapi-client` exists (REPORTED). (d) MCP, all community and unofficial: `BilkentAudio/Wwise-MCP` (Apache-2.0, 79 stars, pushed 2026-10-04; README says experimental and production use is not recommended; needs Wwise 2024.1 or later; a prebuilt exe from GitHub Releases, macOS needs a Gatekeeper override); `WilliamWAudio/wwise-mcp-server` (MIT, 2 stars, Rust, 45 tools); `silver-rain-dev/sk-wwise-mcp` (Apache-2.0, 5 stars). Caution: they expose raw WAAPI, so they can edit or delete project content. Godot: `alessandrofama/wwise-godot-integration` (community, 452 stars, pushed 2026-11-02). (e) None. (f) Console build exit code and bank files can be checked; listening is human.
**Pros for agentic work:**
- Strongest scripting surface of the two middlewares (WAAPI plus a real build CLI).
- Several independent MCP servers, so no single point of failure.
**Cons for agentic work:**
- No official MCP; every server is young and small.
- Audiokinetic's site blocks automated fetching, so terms must be pasted by a human.
- Licence thresholds seen only second-hand.
**Verdict:** Medium. WAAPI plus a build CLI is the best audio-middleware route, but every MCP is community and young.
**Sources:** https://api.github.com/repos/BilkentAudio/Wwise-MCP and its README (VERIFIED); https://api.github.com/repos/WilliamWAudio/wwise-mcp-server (VERIFIED); https://api.github.com/search/repositories?q=wwise+mcp (VERIFIED); https://api.github.com/repos/alessandrofama/wwise-godot-integration (VERIFIED); Audiokinetic pricing, version-control and Q&A pages (REPORTED via search; direct fetch 403); https://pypi.org/project/waapi-client (REPORTED).

### Audacity
**What it is:** Free cross-platform audio editor for recording, cutting and processing clips.
**Cost:** Free; GPL licence, so no fee for commercial game work. Licence file: https://github.com/audacity/audacity/blob/master/LICENSE.txt
**Open source:** Yes. GPLv3, with many source files under GPLv2-or-later; documentation under CC-BY 3.0.
**Extendable:** Nyquist plug-ins (a Lisp-based language), and in 3.x the `mod-script-pipe` module for outside control; VST and similar plug-ins (UNVERIFIED).
**Agent integration:** (a) Project format is not plain text (UNVERIFIED: believed to be a SQLite database); exports are ordinary audio files. (b) No headless mode found; the manual implies Audacity must be running. (c) Audacity 3.x: scripts talk to a running instance over named pipes, commands mirror the macro commands; one project at a time, awkward output parsing. **Audacity 4.0.0 (released 2026-09-03) does not include the scripting pipe or the Macro Manager**; the release notes say they are planned for later. 4.0.2 was published 2026-11-02. (d) MCP, community: `xDarkzx/Audacity-MCP` (Apache-2.0, 127 stars, pushed 2026-10-31, release v0.1.23 on 2026-09-05, 144 tools, Audacity 3.x only); `xDarkzx/Audacity4-MCP` (early alpha, needs a custom Audacity 4 fork built from source); `gizmos-quest/gizmos-audacity-mcp` (MIT, 1 star). Caution: the manual says enabling the pipe weakens security, since anyone able to write to the pipe can make Audacity read and write files. (e) None. (f) Export the result and measure it with FFmpeg; listening is human.
**Pros for agentic work:**
- Free and GPL, nothing to license.
- Rich community MCP on 3.x.
**Cons for agentic work:**
- The scripting pipe is gone in Audacity 4; students who install the newest version get no agent route.
- GUI must be running; no headless mode.
- Pipe is a documented security weakness.
**Verdict:** Low. The one scripting interface was removed from the current major version, and the old one needs a running GUI.
**Sources:** https://www.audacityteam.org/changelog/4.0.0/ (VERIFIED); https://manual.audacityteam.org/man/scripting.html (VERIFIED); https://raw.githubusercontent.com/audacity/audacity/master/LICENSE.txt (VERIFIED); https://api.github.com/repos/audacity/audacity/releases/latest (VERIFIED); https://raw.githubusercontent.com/xDarkzx/Audacity-MCP/main/README.md (VERIFIED); https://api.github.com/search/repositories?q=audacity+mcp (VERIFIED); https://manual.audacityteam.org/man/nyquist.html (VERIFIED).

### REAPER
**What it is:** A compact, proprietary digital audio workstation (DAW) with deep scripting.
**Cost:** Paid licence with a free 60-day full-function evaluation. A discounted licence is allowed for personal use, for commercial use under $20,000 of yearly gross revenue, and for educational or non-profit use; everyone else buys the commercial licence (page read 2026-11-03; prices not repeated here, check current terms): https://www.reaper.fm/purchase.php
**Open source:** No.
**Extendable:** ReaScript in EEL2, Lua 5.4 or Python; JSFX effects; C++ extensions that use the same API.
**Agent integration:** (a) `.RPP` project files are text (REPORTED: community tools edit them directly and the CLI notes name blocks inside them); media and renders are binary. (b) Command line: `reaper -renderproject file.rpp` renders and exits; `-nosplash`, `-newinst`, and passing a `.lua` script after the project are documented in the community ReaTeam notes (REPORTED). It still launches the GUI process. (c) ReaScript can call any REAPER action and most of the API (official page). (d) MCP, all community: `bonfire-systems/reaper-mcp` (MIT, 178 stars, pushed 2026-10-25, ~61 tools, via python-reapy, REAPER 7+); `xDarkzx/Reaper-MCP` (Apache-2.0, 112 stars, 181 tools, a Lua script inside REAPER exchanging JSON files with the server); `dschuler36/reaper-mcp-server` (MIT, 135 stars, project inspection). Caution: setup enables REAPER's remote-control API or runs a script that executes agent-requested commands, so use only on a trusted machine and back up projects. (e) None. (f) Render headlessly and run FFmpeg loudness and silence checks; mix quality is human.
**Pros for agentic work:**
- Text projects diff in git; full scripting API.
- Render-and-exit command line suits batch jobs.
**Cons for agentic work:**
- Paid after 60 days (discount for students and small earners).
- Not truly headless; every MCP server is community-made.
**Verdict:** Medium. The most scriptable DAW, but a paid GUI process and unofficial MCP servers.
**Sources:** https://www.reaper.fm/purchase.php (VERIFIED); https://www.reaper.fm/sdk/reascript/reascript.php (VERIFIED); https://raw.githubusercontent.com/ReaTeam/Doc/master/REAPER-CLI.md (REPORTED, community-maintained docs); https://api.github.com/search/repositories?q=reaper+mcp (VERIFIED); https://raw.githubusercontent.com/bonfire-systems/reaper-mcp/main/README.md (VERIFIED); https://raw.githubusercontent.com/xDarkzx/Reaper-MCP/main/README.md (VERIFIED).

### LMMS
**What it is:** Free, open-source music-production program for making tracker-style and synth-based loops and songs.
**Cost:** Free; GPL-2.0, so free for commercial games. https://github.com/LMMS/lmms
**Open source:** Yes (GPL-2.0).
**Extendable:** C++ plug-ins and instruments; no scripting API found in the sources read (UNVERIFIED that none exists).
**Agent integration:** (a) Projects are `.mmp` XML or compressed `.mmpz`; `lmms dump` prints the XML of a compressed file (man page). (b) CLI: `lmms render <project>` with `-f wav|ogg|mp3`, `-o`, `-s` sample rate, `-l` loop; `rendertracks` writes one file per track; `upgrade` migrates old files (man page, VERIFIED). The man page does not say whether it needs a display (UNVERIFIED). (c) No scripting API found. (d) MCP, community and tiny: `ZipseLu/lmms-mcp` (MIT, 2 stars, pushed 2026-08-21), `Jx9x/lmms-mcp-bridge` (GPL-2.0, 0 stars, pushed 2026-10-23). Treat as experiments. (e) None. (f) Render to WAV then measure with FFmpeg; musical quality is human.
**Pros for agentic work:**
- XML projects an agent can generate and edit as text.
- Documented offline render command.
**Cons for agentic work:**
- Stable release on GitHub is still 1.2.2 (July 2020); 1.3 exists only as alpha tags (checked 2026-11-03), so many students will meet old packaging.
- No scripting API and no serious MCP.
**Verdict:** Medium. Text project plus render CLI is workable, but little ecosystem and an old stable release.
**Sources:** https://man.archlinux.org/man/lmms.1.en (VERIFIED); https://api.github.com/repos/LMMS/lmms (VERIFIED); https://api.github.com/repos/LMMS/lmms/releases/latest and /tags (VERIFIED); https://api.github.com/search/repositories?q=lmms+mcp (VERIFIED).

### jsfxr (and the Bfxr/sfxr family)
**What it is:** Browser and Node ports of the sfxr retro sound-effect generator: pick a preset (coin, laser, explosion), tweak parameters, export a WAV.
**Cost:** Free. jsfxr carries an UNLICENSE file (GitHub reports the Unlicense, a public-domain dedication); `increpare/bfxr2` (the Bfxr web port) is MIT. That means free commercial use of the tool; whether any extra claim attaches to generated sounds was not found (UNVERIFIED, but the licences above give none). https://github.com/chr15m/jsfxr
**Open source:** Yes (Unlicense for jsfxr, MIT for bfxr2).
**Extendable:** JavaScript library (`npm i jsfxr`); parameters are a JSON object or a base58 short string.
**Agent integration:** (a) A sound is a small text JSON, so it diffs well; output is WAV. (b) The package ships a Node script `sfxr-to-wav` that takes the encoded string or JSON on stdin and writes a `.wav` (script read, VERIFIED). (c) `sfxr.generate(preset)`, `toBuffer`, `toWave` in Node; `play()` needs a browser. (d) MCP, community and unvetted: `jsfxr-mcp-wrapper` on npm (MIT, v1.0.1, February 2026, one maintainer, no repository link in the registry entry) and `make-sfx-mcp` (npm 2.0.0, updated 2026-10-21, MIT, built on ZzFX, a close relative of sfxr; repository `Tuntii/make-sfx`). Caution: running unreviewed npm packages with file-write access; prefer calling `sfxr-to-wav` directly. (e) None. (f) Check the WAV's length and level with ffprobe and FFmpeg; whether it is a satisfying "pickup" sound is a human ear check.
**Pros for agentic work:**
- Fully scriptable text parameters; deterministic WAV out.
- No account, no network, no licence worries.
**Cons for agentic work:**
- Sounds are limited to the chiptune palette.
- The MCP wrappers are single-maintainer and unaudited.
**Verdict:** High. Text parameters in, WAV out, with a ready-made CLI script.
**Sources:** https://raw.githubusercontent.com/chr15m/jsfxr/master/README.md, https://raw.githubusercontent.com/chr15m/jsfxr/master/sfxr-to-wav, https://api.github.com/repos/chr15m/jsfxr/contents/, https://api.github.com/repos/increpare/bfxr2, https://registry.npmjs.org/jsfxr-mcp-wrapper, https://registry.npmjs.org/make-sfx-mcp (all VERIFIED).

### FFmpeg
**What it is:** The standard command-line toolkit for converting, cutting, mixing and analysing audio and video (with `ffprobe` for inspection).
**Cost:** Free. Licence is LGPL 2.1 or later by default and becomes GPL if you build with certain GPL parts; it is not offered under other terms. Commercial games can use it if they follow the LGPL rules (dynamic linking, ship source, credit). The project warns that H.264 and similar formats may carry patent licensing issues in commercial products. https://ffmpeg.org/legal.html
**Open source:** Yes (LGPL-2.1+, GPL-2.0+ for some parts).
**Extendable:** Filter graphs, libraries (libav*), source access. The project distributes source only; binaries come from third parties (download page).
**Agent integration:** (a) Not a project tool; inputs and outputs are files. (b) The whole interface is the command line; `ffprobe -of json -show_streams -show_format` prints machine-readable JSON (VERIFIED). (c) Filters include `ebur128`, `loudnorm`, `volumedetect`, `astats`, `silencedetect`, `silenceremove` (names present in the filter manual). (d) MCP: none official, none needed. Community example: `kajisho5/ffmpeg-skill` (MIT, 4,453 stars, pushed 2026-10-31) bundles 42 FFmpeg tools with an MCP server for video editing; cautious use, since it is a wrapper around a CLI an agent already drives. (e) None. (f) Strongest of any tool here: an agent can measure loudness, detect silence and read duration, sample rate and channel count, and compare against thresholds. Exit code 0 can still hide a silent or truncated file, so check the measurements, not the exit code.
**Pros for agentic work:**
- Plain CLI with JSON inspection; agents already know it.
- Doubles as the verification tool for every other audio tool in this list.
**Cons for agentic work:**
- Option and filter-graph syntax is easy to get subtly wrong.
- Patent and build-flag licensing needs care before shipping a build that embeds it.
**Verdict:** High. A complete batch interface with JSON inspection and measurable audio checks.
**Sources:** https://ffmpeg.org/legal.html, https://ffmpeg.org/download.html (9.0.2 dated 2026-09-18), https://ffmpeg.org/ffprobe.html, https://ffmpeg.org/ffmpeg-filters.html (filter names in table of contents only), https://api.github.com/repos/kajisho5/ffmpeg-skill (all VERIFIED).

### SoX (Sound eXchange)
**What it is:** A long-standing command-line audio converter and effects processor.
**Cost:** Free; GPL-2.0+ with the library under LGPL-2.1+, so usable in commercial pipelines (tool use, not redistribution). https://sourceforge.net/projects/sox/
**Open source:** Yes (GPL-2.0+/LGPL-2.1+).
**Extendable:** Effects chains on the command line; library `libsox`; source access.
**Agent integration:** (a) Files in, files out. (b) Command line only: `sox in.wav out.ogg trim 0 3 fade ...` style chains (the `stat` and `stats` effects exist, UNVERIFIED here). (c) No scripting layer beyond the shell. (d) MCP: none found. (e) None. (f) Output files can be re-measured, ideally with FFmpeg, since SoX's own measurements are less standard (judgment).
Status: official SoX 14.4.2 is dated 22 February 2015 and development has stalled; the community fork `sox_ng` (Codeberg, 57 stars, updated 2026-10-27, 108 open issues) is what many distributions ship (REPORTED).
**Pros for agentic work:**
- Short, readable effect chains; good for trim, fade, normalise, resample.
- No GUI, no network.
**Cons for agentic work:**
- Upstream has not released since 2015; students may get a distro-patched fork with different command names.
- FFmpeg covers nearly everything it does, so there is little reason to add a second tool.
**Verdict:** Medium. Agent-friendly interface, but a stalled upstream and FFmpeg overlaps it.
**Sources:** https://sourceforge.net/projects/sox/ (VERIFIED); https://en.wikipedia.org/wiki/SoX (REPORTED); https://codeberg.org/api/v1/repos/sox_ng/sox_ng (VERIFIED).

---

## Part 2. Asset sources and marketplaces

### Fab (Epic Games)
**What it is:** Epic's marketplace for 3D models, textures, sound, VFX, Unreal and Unity plug-ins, replacing the old Unreal Engine Marketplace.
**Cost:** Free and paid listings. Buyer licences: Standard (Personal or Professional price tier, split at $100,000 of gross commercial revenue in the past 12 months, per Epic's docs read 2026-11-03) and Creative Commons for free items. Terms: the Fab End User License Agreement on fab.com (not readable by the fetcher, HTTP 403 on the URLs tried); the licence tiers below come from Epic's docs: https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab
**Open source:** No (a service). Individual listings may be CC-BY.
**Extendable:** Fab plug-ins exist for Unreal and Unity; no official Godot or Blender add-on found (REPORTED).
**Agent integration:** (a) Content is binary (meshes, textures, uncooked Unreal packs). Many listings are Unreal-only formats. (b) No documented CLI or public API; downloads go through the website or the Epic Games Launcher (REPORTED). (c) None official. (d) MCP, community: `jonit-dev/fab-mcp` (no licence file, 2 stars, pushed 2026-10-29) downloads free listings and takes a parameter to accept the EULA, so an agent must never set that on a user's behalf; unofficial endpoint wrappers (the `egs-api` Rust crate) rely on undocumented URLs that may break or breach terms (UNVERIFIED). (e) None. (f) File type and hash checks only.
Licence notes: the Standard licence is reported to allow use in any compatible tool, not only Unreal, but this came from a forum reply and a search summary, so confirm on each listing (REPORTED). Epic's policy asks sellers to tag AI-made listings "CreatedWithAI" (REPORTED), and assets may carry a NoAI tag that blocks generative-AI data use and forces the Standard licence rather than CC-BY (docs, VERIFIED).
**Pros for agentic work:**
- Large catalogue with a per-listing licence and AI tags to record.
**Cons for agentic work:**
- No supported automation; terms page blocks automated reading.
- Unreal-oriented formats need conversion for Godot.
**Verdict:** Low. No supported agent route, and licence reading needs a human.
**Sources:** https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab (VERIFIED); Epic forum threads on Standard licence and AI tagging (REPORTED); https://api.github.com/repos/jonit-dev/fab-mcp (VERIFIED); docs.rs egs-api (REPORTED).

### Unity Asset Store
**What it is:** Unity's marketplace for packages, tools, art and audio, sold by Unity and third-party publishers.
**Cost:** Free and paid assets; each is licensed under the Asset Store EULA (some carry separate publisher terms, called Restricted Asset Terms). Terms: https://unity.com/legal/as-terms
**Open source:** No (individual packages may include open-source components that follow their own licences).
**Extendable:** Not applicable (it is a store); publishers upload packages.
**Agent integration:** (a) Content arrives as `.unitypackage` archives, which are binary bundles. (b) No official CLI or public download API found; downloads happen in the Unity Editor's Package Manager and are cached locally (REPORTED). (c) None. (d) MCP: none for the store itself; a Unity MCP pull request adds list, download and import through reflection into Package Manager, so it needs the Editor running (REPORTED). (e) None. (f) Inspect the archive contents and licence file.
Licence points, read from the EULA today: assets may be used outside Unity (Unity's support page says so, subject to Section 2); the licence lets you embed an asset in a product with substantial original content and monetise it, but not resell or redistribute the asset on its own; and Section 2.2.1.1(g) bars using the Asset Store or its assets to train AI or machine-learning models without consent. Extension Assets are licensed per seat.
**Pros for agentic work:**
- Clear, written licence with explicit rules on engines and AI training.
**Cons for agentic work:**
- No supported download automation; needs a Unity ID login and often the Editor.
- Assets built for Unity usually need conversion for Godot.
**Verdict:** Low. Legal terms are clear, but there is no agent route to the files.
**Sources:** https://unity.com/legal/as-terms (VERIFIED); https://support.unity.com/hc/en-us/articles/34387186019988-Can-I-use-assets-from-the-Asset-Store-with-other-engines (VERIFIED); Unity forum and PR threads on automation (REPORTED).

### Godot Asset Library and the new Godot Asset Store
**What it is:** Godot's official add-on catalogue. The old Asset Library lists open-source add-ons, templates and demos as Git commits; the new Godot Asset Store (store.godotengine.org) is replacing it.
**Cost:** Free. The Library accepts free and open-source licences (GPL v2 and v3, MIT, BSD, Boost among them). The Asset Store announcement (official, 2026-05-22) says buying and selling is not yet available. Terms: https://docs.godotengine.org/en/stable/community/asset_library/submitting_to_assetlib.html
**Open source:** The Asset Library is open source (REST API and frontend repository; licence not stated in the README read). The Asset Store's code is private per Godot's docs. Most listed add-ons are open source.
**Extendable:** Add-ons are GDScript/C# plug-ins; the Library has a REST API documented in the repo's `API.md` (not read, UNVERIFIED).
**Agent integration:** (a) Add-ons are plain text in a Git repository. (b) The Library hosts no files: each entry points to a Git repo and commit, and the download link is computed from them (docs), so an agent can clone and pin the commit instead of using the editor. (c) The editor's AssetLib tab is GUI; no CLI. (d) MCP: several Godot MCP servers advertise Asset Library or CC0 asset search (REPORTED search summaries, not opened; the Godot MCP researcher covers them). (e) None. (f) Run the project headless and check for load errors.
Status: the Library repo says it is in maintenance mode and the Foundation's store will deprecate it. Godot's article calls the store live and stable, the docs still label it beta, and full editor integration is promised for Godot 4.7.
**Pros for agentic work:**
- Source is text in Git, so an agent can read, diff and vendor it.
- Library lists the licence per asset.
**Cons for agentic work:**
- Two catalogues during the transition; authors must re-upload, so listings differ.
- No official CLI; licence is not independently verified by the catalogue.
**Verdict:** Medium. Assets are Git commits an agent can pin, but no official command line.
**Sources:** https://docs.godotengine.org/en/stable/community/asset_library/using_assetlib.html, https://docs.godotengine.org/en/stable/community/asset_library/submitting_to_assetlib.html, https://docs.godotengine.org/en/stable/community/asset_store/what_is_asset_store.html, https://godotengine.org/article/introducing-the-godot-asset-store/, https://raw.githubusercontent.com/godotengine/godot-asset-library/master/README.md (all VERIFIED).

### itch.io asset packs
**What it is:** The indie marketplace where creators sell or give away asset packs (art, audio, fonts, tilesets) with terms they set themselves.
**Cost:** Free, pay-what-you-want and paid, per creator. The licence is whatever the creator states on the page or in the pack's licence file; itch.io's terms give buyers a non-exclusive, perpetual licence to access content (ToS Section 4). Terms: https://itch.io/docs/legal/terms
**Open source:** No (a store). Packs vary.
**Extendable:** Creators publish with the `butler` command-line tool (MIT, 1,007 stars, pushed 2026-11-01), mainly for builds (UNVERIFIED for asset packs). Server-side API with an API key.
**Agent integration:** (a) Packs are zips of PNG, WAV, OGG, GLB, text. (b) The documented server-side API lists your uploaded games and owned download keys but documents no file-download call (VERIFIED); downloads happen in the browser or the itch app. (c) None for downloading. (d) MCP, community and tiny: `nadezhdkov/game-asset-finder` (MIT, 0 stars, pushed 2026-11-03, searches itch.io and OpenGameArt), `Adamshrugged/packrat-assets` (MIT, 0 stars). (e) None. (f) Read the licence file inside the zip.
AI: since November 2024 creators must disclose generative-AI use on asset pages, and buyers can filter out "No AI" listings (REPORTED by games press).
**Pros for agentic work:**
- Huge indie catalogue; many packs are free and CC0.
**Cons for agentic work:**
- No uniform licence field; every pack must be read individually.
- No documented download API; purchases need a human login.
**Verdict:** Low. Licence varies per pack and there is no documented download route.
**Sources:** https://itch.io/docs/legal/terms, https://itch.io/docs/api/serverside, https://api.github.com/repos/itchio/butler, https://api.github.com/search/repositories?q=itch.io+mcp (VERIFIED); AI disclosure articles from Engadget and PC Gamer (REPORTED via search).

### Kenney
**What it is:** A prolific indie studio that publishes game-ready 2D, 3D and audio packs as free downloads.
**Cost:** Free. The site states all assets on its asset pages are CC0, usable in commercial projects, credit not required (appreciated as "Kenney"). Some bundles are sold on itch.io, Steam and the Epic store. https://kenney.nl/support
**Open source:** Assets are CC0 (public domain dedication), not "open source" software.
**Extendable:** Not applicable; packs are plain files.
**Agent integration:** (a) PNG, SVG, OGG, GLB and similar; packs ship a licence file. (b) Download through the website; no API found (UNVERIFIED). (c) None. (d) MCP, community and tiny: `dcc-mcp/dcc-asset-kenney` (MIT, 0 stars, pushed 2026-07-29), `hengtuibabai/openassets.studio` (no licence listed, 0 stars). (e) None. (f) Verify the licence file is in the pack.
**Pros for agentic work:**
- CC0 makes the legal bookkeeping minimal.
- Consistent style and file layout across packs, which agents learn quickly.
**Cons for agentic work:**
- No API; downloads are manual or scripted from page links.
- Kenney gives no engine-import help (support page).
**Verdict:** Medium. The easiest licence of any source here, but no official programmatic access.
**Sources:** https://kenney.nl/support (VERIFIED); https://api.github.com/search/repositories?q=kenney+assets+mcp (VERIFIED).

### OpenGameArt
**What it is:** A long-running community archive of user-submitted game art, music and sound, each with its own licence.
**Cost:** Free to download. Commercial use is allowed if you follow each item's licence. The site accepts CC0, CC-BY 3.0/4.0, CC-BY-SA 3.0/4.0, OGA-BY 3.0/4.0 and GPL-family licences. Terms: https://opengameart.org/content/faq
**Open source:** Content is under free licences (CC0, CC-BY, GPL and others); the site's own code was not checked.
**Extendable:** Not applicable.
**Agent integration:** (a) Mixed binary assets plus a "Copyright/Attribution Notice" field. (b) No official API found (UNVERIFIED); the default fetcher got HTTP 403 on the FAQ. (c) None. (d) MCP, community and tiny: `nadezhdkov/game-asset-finder` (MIT, 0 stars). (e) None. (f) Compare the saved licence text with the submission page.
Licence rules from the FAQ: CC-BY needs credit with title, creator and link and an indication of changes, and cannot be used on distribution platforms that apply DRM; CC-BY-SA requires derivatives to carry the same licence; OGA-BY drops the DRM limit. An artist may change a licence later, but your original licence stays irrevocable. A suggested credit line is "[asset name] by [author] licensed [licence]: [URL]".
**Pros for agentic work:**
- Excellent worked examples of attribution wording.
- Many CC0 items.
**Cons for agentic work:**
- Multi-licence items and share-alike traps need human judgment.
- No API; fetch blocking; items can be re-licensed.
**Verdict:** Low. Rich catalogue, but licences vary per item and there is no machine route.
**Sources:** https://opengameart.org/content/faq (VERIFIED; the default fetcher got 403, so the page was read with a command-line `curl`); https://api.github.com/search/repositories?q=opengameart+api+OR+opengameart+mcp (VERIFIED).

### Sketchfab
**What it is:** An online 3D model viewer and library; many free models can be downloaded as glTF.
**Cost:** Free to browse; Download API gives access to a library of "over 1 million free models, available under Creative Commons" licences (docs). Other models carry Standard or Editorial licences (Editorial bars commercial use). Terms: https://sketchfab.com/licenses
**Open source:** No (a service).
**Extendable:** Data API v3 and Download API.
**Agent integration:** (a) glTF zip (scene.gltf, bin, textures) or USDZ. (b) `GET /v3/models/{uid}/download` with a Bearer token returns a link that expires in about five minutes (docs); each end user must log in via OAuth 2.0. (c) The Data API supports searching; the CC0 filter parameter was not confirmed (UNVERIFIED). (d) MCP, community: `gregkop/sketchfab-mcp-server` (44 stars, no licence listed, last push 2025-03-09, stale), `AliRezaBeigy/sketchfab-mcp-server` (2 stars, pushed 2026-06-29); Blender MCP also lists Sketchfab. (e) None. (f) Read the model's licence from the API response and save it.
Ownership: the Epic news post (REPORTED via search; fetch blocked) says KitBash announced on 2026-08-10 that it would take over ArtStation and Sketchfab from Epic. In 2024 Epic had said it planned to stop offering downloadable content on Sketchfab in 2025; sources conflict on what happened, so check current availability.
**Pros for agentic work:**
- glTF output imports into Godot directly.
- Every model carries a licence in API metadata.
**Cons for agentic work:**
- Per-user OAuth means a human signs in.
- Ownership change and earlier plans to end downloads make long-term access uncertain.
**Verdict:** Medium. A real download API with glTF, held back by user sign-in and uncertainty about the platform's future.
**Sources:** https://sketchfab.com/developers/download-api and /downloading-models, https://sketchfab.com/licenses (VERIFIED); KitBash/Epic coverage via search (REPORTED); https://api.github.com/search/repositories?q=sketchfab+mcp (VERIFIED).

### Poly Haven
**What it is:** A library of HDRIs, PBR textures and 3D models, all released CC0.
**Cost:** Free; CC0, commercial use allowed, no attribution for the assets. The API is free "for any purpose, personal or commercial" but a "Powered by Poly Haven" style credit applies if you show content live from the API. https://github.com/Poly-Haven/Public-API
**Open source:** Assets are CC0; the API repository is AGPL-3.0.
**Extendable:** Public JSON API at `api.polyhaven.com` (assets, categories, per-asset file lists); Blender add-on.
**Agent integration:** (a) Standard files (EXR/HDR, PNG/JPG, glTF, Blender). (b) The API answers plain HTTP with JSON, no key; the API terms require a unique user-agent or referer identifying your app (ToS 2.4). I fetched `api.polyhaven.com/assets?t=hdris` and got JSON with name, authors, categories, tags and download counts. (c) The API covers listing and file URLs. (d) MCP: Blender MCP (`ahujasid/blender-mcp`, community, MIT, 33,190 stars, pushed 2026-10-29) can search and import Poly Haven and Sketchfab assets, but also exposes `execute_blender_code` (arbitrary Python); its safe mode is off by default and its socket has no authentication. Small Poly Haven-only skills exist (`dcc-mcp/dcc-asset-polyhaven`, 1 star). (e) None. (f) Check file hashes and dimensions; look at renders.
AI note (REPORTED, search summary of the Poly Haven FAQ): the CC0 licence permits AI training, and the textures are not made with generative AI.
**Pros for agentic work:**
- Cleanest legal position and the only open JSON API in this group.
- Assets arrive in standard formats.
**Cons for agentic work:**
- Scope is environment art (HDRIs, materials, props), not characters or UI.
- Must send an identifying user-agent.
**Verdict:** High. CC0 assets behind an open, keyless JSON API.
**Sources:** https://github.com/Poly-Haven/Public-API, https://raw.githubusercontent.com/Poly-Haven/Public-API/master/ToS.md, https://api.polyhaven.com/assets?t=hdris&limit=1, https://raw.githubusercontent.com/ahujasid/blender-mcp/main/README.md, https://api.github.com/repos/ahujasid/blender-mcp (all VERIFIED); https://docs.polyhaven.com/en/faq (REPORTED).

### Freesound
**What it is:** A community database of sound recordings and samples, searchable with licence filters.
**Cost:** Free to download. Each sound has its own Creative Commons licence: CC0 (no credit), CC-BY (credit required, commercial use fine), CC-BY-NC (credit, no commercial use) and a retiring Sampling+. The API is free for non-commercial use only; commercial API use needs a contact with Freesound. https://freesound.org/help/faq/ and https://freesound.org/docs/api/terms_of_use.html
**Open source:** No (the site's content is CC; the platform's code was not checked).
**Extendable:** REST API v2.
**Agent integration:** (a) Audio files plus metadata. (b) API: a token (key) for read-only search; OAuth2 (browser consent) for `GET /sounds/<id>/download/`, which returns the original file; access tokens last 24 hours (docs). (c) Search accepts `filter=` on `license`, `username`, `name` and a `gen_ai_preference` field (creator opt-outs for generative AI), returning `name,tags,username,license` by default; ask for `url` explicitly. (d) MCP, community: `Losera/soundfetch` (MIT, 4 stars, pushed 2026-10-23, license-aware CLI plus MCP across Freesound, Openverse and Internet Archive), `sandraschi/sfx-mcp` (MIT, 3 stars, pushed 2026-11-03), `johnkimdw/freesound-mcp-server` (MIT, 10 stars, last push 2025-06). (e) None. (f) Record the license string from the response and verify it matches the sound's page.
Attribution (FAQ): credit the sound name, the creator's username, a link and the licence; many sounds can be listed on one credits page. Do not remix CC-BY-NC sounds into anything commercial.
**Pros for agentic work:**
- Licence is a first-class, filterable API field, and creators' AI preferences are filterable too.
**Cons for agentic work:**
- Original downloads need a human OAuth step; the API is non-commercial only.
- Mixed licences make "just grab a sound" risky; NC sounds are traps.
**Verdict:** Medium. The best licence metadata of any source, but downloads require an OAuth sign-in and the API is non-commercial.
**Sources:** https://freesound.org/help/faq/, https://freesound.org/docs/api/authentication.html, https://freesound.org/docs/api/terms_of_use.html, https://freesound.org/docs/api/resources_apiv2.html, https://api.github.com/search/repositories?q=freesound+mcp (all VERIFIED).

---

## Asset licence ledger: what an agent must record for every external file

**Licence meanings (from the OpenGameArt and Freesound FAQs, both VERIFIED):**

| Licence | Credit needed | Commercial game OK | Derivatives | Catch |
|---|---|---|---|---|
| CC0 | No | Yes | Any | Underlying rights (for example real-world brands or designs) are not cleared by CC0 |
| CC-BY 3.0/4.0 | Yes: title, creator, link, licence, note of changes | Yes | Any, with credit | OGA says it cannot be used on platforms with DRM |
| CC-BY-SA 3.0/4.0 | Yes, as CC-BY | Yes | Derivatives must carry the same licence | Share-alike may spread to modified assets |
| OGA-BY | Yes, as CC-BY | Yes | Any | Removes the DRM limit |
| CC-BY-NC | Yes | **No** | Noncommercial only | Cannot be relicensed as CC0 or CC-BY |
| Store EULAs (Unity, Fab Standard, itch.io) | Per listing | Usually, per EULA | No standalone resale | Read each; some forbid AI training |

**Record in an `ASSETS.csv` (one row per source file or pack), generated or updated by the agent at download time:**
1. Asset name and pack name.
2. Creator or username, as shown on the page.
3. Source page URL (the asset page, never a CDN link) and the date retrieved.
4. Licence name and version as printed on the page, and the licence URL. Save a copy of the licence text or page next to the asset. A search snippet or a "free" label is not a licence.
5. The exact credit line to ship (use the creator's own "Copyright/Attribution Notice" if given).
6. Flags: commercial use allowed; credit required; share-alike; non-commercial; DRM caveat.
7. Whether the file was modified and how (CC-BY requires saying so).
8. Where it lives in the repo, and a SHA-256 of the original download.
9. AI flags: Fab "CreatedWithAI" or NoAI tag, itch.io generative-AI disclosure, Freesound `gen_ai_preference`.
10. Terms of the access route itself (for example, Freesound's API is non-commercial).

**Rules for the agent:** never decide the licence from a thumbnail or search summary; re-read the licence at the moment of download; stop and ask when a site blocks reading (Audiokinetic, Fab, OpenGameArt returned 403 to the fetcher); never click through or set an "accept EULA" parameter on the user's behalf (`fab-mcp` has one); keep a generated `CREDITS.md` built from the ledger; prefer CC0 sources (Kenney, Poly Haven, CC0-filtered Freesound) for anything an agent downloads unattended; send a human the NC and SA rows for review.

---

## Part 3. Design and UI tools

### Figma (with the official Figma MCP server)
**What it is:** Browser-based design and prototyping tool; the Figma MCP server lets agents read designs and, in beta, write to the canvas.
**Cost:** Starter plan is free; Professional, Organization and Enterprise are per-seat subscriptions (Full, Dev, Collab and View seats; pricing page read 2026-11-03, check current terms). Free for students and educators: Figma's Education plan gives access to the Professional tier (Enterprise for schools with under-13 students), including the AI toolkit for eligible education users. The Terms of Service let free accounts use the Services for business or personal purposes (Section 1.1), and the customer keeps rights to their content (2.8). https://www.figma.com/tos/ and https://www.figma.com/education/
**Open source:** No. The guide repository `figma/mcp-server-guide` is public (2,146 stars, pushed 2026-11-03) but shows no licence.
**Extendable:** Plugin API (JavaScript, runs only when a user starts it, cannot run in the background), REST API (read files, comments, webhooks, variables), Code Connect, Figma Make, community MCP servers.
**Agent integration:**
(a) Design files live in Figma's cloud; there is no plain-text project format to diff (a `.fig` export is binary, UNVERIFIED). (b) No command line or headless mode; agents go through the remote server. (c) Scripting: the Plugin API (JavaScript, runs only when a user starts it, no background runs) and the REST API, which reads files, images, comments and variables and can post comments and manage webhooks, but its overview page does not describe creating or editing nodes. `use_figma` (below) is how an agent gets Plugin API power.
(d) **Official MCP server**, hosted at `https://mcp.figma.com/mcp`, no desktop app required. The docs list **41 tools**: 18 read-only, 14 writing, plus 9 Figma Weave tools that need a separate paid Weave account. *Read:* `get_design_context` (code plus design data for a layer), `get_screenshot`, `get_metadata`, `get_variable_defs`, `get_figjam`, `get_motion_context`, `search_design_system`, `get_libraries`, `download_assets`, `whoami`, Code Connect lookups, shader and plug-in listings. *Write:* **`use_figma`** (creates, edits, deletes and inspects content in Design, FigJam, Slides and Specs files by running code through the Plugin API: frames, components, variants, variables, auto layout), `generate_figma_design` and `html_to_figma` (live page or HTML into layers), `send_code_to_figma`, `create_new_file`, `upload_assets`, `generate_image` (uses AI credits), `generate_diagram` (FigJam from Mermaid or text), and Code Connect mapping tools. This session's live plug-in also exposes `create_session`, which the docs table I read did not list (the docs lag the server).
*Limits:* each `use_figma` call returns up to 20 KB; it cannot add images by itself (use `upload_assets`); only fonts uploaded to your Figma account work; components with images or videos cannot be imported yet; output is beta quality. Write-to-canvas is remote-server only, free during the beta and later usage-based; writing outside your drafts needs a Full seat, a Dev seat can write in drafts only. *Rate limits* (docs page, read 2026-11-03): Full or Dev seats get 200 calls a day and 10 a minute on Professional and Education, 200 and 15 on Organization, 600 and 20 on Enterprise; View and Collab seats get up to 20 a month. The guide README says 6 a month for those seats, so the two Figma pages disagree; check current terms. Exempt from limits on the docs page: `add_code_connect_map`, `create_new_file`, `generate_figma_design`, `whoami` (the README says all writing tools are exempt, which the limits page does not say).
*Install:* Claude Code: `claude plugin install figma@claude-plugins-official` (adds Figma's skills) or `claude mcp add --transport http figma https://mcp.figma.com/mcp`, then sign in through the browser. Codex: the Codex app plug-in, or `codex mcp add figma --url https://mcp.figma.com/mcp` (no skills). Enterprise admins may block plug-ins. The plug-in's skills (in this session: figma-use, figma-generate-design, figma-generate-library, figma-use-figjam and others) must be loaded before the matching tools; `figma-use` comes before any `use_figma` call.
*Community alternatives:* `GLips/Figma-Context-MCP` (MIT, 16,148 stars, pushed 2026-10-27, read-oriented), `southleft/figma-console-mcp` (MIT, 2,665 stars, pushed 2026-10-29, adds creation and debugging through a plug-in), `sonnylazuardi/cursor-talk-to-figma-mcp` (MIT, 7,075 stars, pushed 2026-07-26, read and modify designs).
(e) Built-in AI: Figma AI features and credits (`generate_image` draws on them); the Figma AI Terms page returned 404, so how they treat customer content is UNVERIFIED. Using the MCP server means agreeing to the Figma Developer Terms; I found no clause there limiting AI training on API data.
(f) Verification and security: an agent can check its work with `get_screenshot` and `get_metadata` and by reading variables back; whether the design is good or on-brand is a human check. `use_figma` runs agent-written code against your real file with your permissions, so Figma's own advice is to test on a duplicate or draft and keep a backup. Course practice: allow the read tools by name and make `use_figma` ask each time.
*For Godot:* there is no official Figma-to-Godot path. A public converter by the course instructor (`github.com/nikbearbrown/figma-to-godot`) reads a Figma file through `use_figma` and writes `.tscn` scenes and Theme `.tres` files (from the instructor's project notes; not re-checked here).
**Pros for agentic work:**
- Official, hosted, documented MCP server with both read and write tools; works in Claude Code and Codex.
- `get_design_context`, variables and Code Connect give an agent structured design data, not just pixels.
- Free for students through Education, with Professional-tier limits.
**Cons for agentic work:**
- Cloud-only, binary-ish files, no diff; write mode is beta and may become paid.
- Seat, plan and rate-limit rules are intricate and inconsistent between Figma pages; the free Starter plan is nearly unusable for agents.
- Design output still needs human taste and cleanup; `use_figma` is arbitrary code in your file.
**Verdict:** High. The only tool here with an official, documented MCP server that can both read and write the design.
**Sources:** https://developers.figma.com/docs/figma-mcp-server/ ; /tools-and-prompts/ ; /rate-limits-access/ ; /write-to-canvas/ ; /remote-server-installation/ ; /code-connect-integration/ (all VERIFIED); https://github.com/figma/mcp-server-guide and https://raw.githubusercontent.com/figma/mcp-server-guide/main/README.md (VERIFIED); https://developers.figma.com/docs/rest-api/ and /plugins/ (VERIFIED); https://www.figma.com/pricing/, /education/, /tos/, /developer-terms/ (VERIFIED); GitHub API pages for the three community servers (VERIFIED); this session's own plug-in tool list and skill list (VERIFIED locally); /Users/bear/.claude/projects/-Users-bear-Documents-CoWork/memory/figma-to-godot-repo.md (REPORTED, instructor's notes).

### Inkscape
**What it is:** Free vector graphics editor whose native format is SVG.
**Cost:** Free; commercial use of your own drawings is fine. https://inkscape.org
**Open source:** Yes. Most source is GPL-2.0-or-later; complete binaries are GPL-3.0-or-later (COPYING file).
**Extendable:** Python extensions (`inkex`, REPORTED via an MCP README), plug-in formats, source access. Official gitlab project: 4,022 stars, active 2026-11-03.
**Agent integration:** (a) SVG is plain XML text that an agent can write, diff and validate. (b) Command line: `inkscape input.svg --export-type=png --export-filename=out.png`; `--export-id` exports named objects; `--actions="..."` chains actions; `--pipe` reads SVG from stdin; `--shell` keeps one instance for many files. Verbs were removed, use actions (wiki, VERIFIED). (c) Actions cover GUI operations. (d) MCP, community: `aravindev/inkscape_mcp` (MIT, 91 stars, pushed 2026-11-02; eight tools; runs headless or drives a live window over D-Bus; install `claude mcp add inkscape_mcp -s user -- uvx inkscape_mcp`); `sandraschi/inkscape-mcp` (MIT, 96 stars, pushed 2026-10-24); `Shriinivas/inkmcp` (AGPL-3.0, 79 stars, pushed 2026-01-14). Caution: they run the Inkscape binary and can run extensions on local files. (e) None. (f) Export to PNG and inspect it; the SVG can be validated as XML. The headless guidance on the wiki is inconsistent about which flags are still needed, so test your version.
**Pros for agentic work:**
- Text-based format plus a rich CLI; agents can generate SVG with no app at all.
- Godot can import SVG (UNVERIFIED here).
**Cons for agentic work:**
- Complex art by prompt still needs human review.
- MCP servers are community-made and young; GUI mode needs D-Bus on Windows.
**Verdict:** High. SVG is text, and the command line exports without a GUI session.
**Sources:** https://wiki.inkscape.org/wiki/Using_the_Command_Line, https://gitlab.com/inkscape/inkscape/-/raw/master/COPYING, https://gitlab.com/api/v4/projects/inkscape%2Finkscape, https://raw.githubusercontent.com/aravindev/inkscape_mcp/main/README.md, https://api.github.com/search/repositories?q=inkscape+mcp (all VERIFIED).

### Excalidraw
**What it is:** Free browser whiteboard for hand-drawn-style diagrams; useful for design-doc sketches.
**Cost:** Free. MIT licence on the main repository. https://github.com/excalidraw/excalidraw
**Open source:** Yes (MIT, 135,110 stars, pushed 2026-11-03). The separate `excalidraw/excalidraw-mcp` repo shows no licence file in its root listing, so reuse terms there are unclear.
**Extendable:** Embeddable React component, libraries, open source.
**Agent integration:** (a) A drawing is JSON of "elements" (per the MCP README), so it is text, though verbose. (b) No CLI found (UNVERIFIED). (c) None official beyond the component. (d) **Official MCP** (published under the `excalidraw` GitHub organisation): `excalidraw/excalidraw-mcp`, 5,634 stars, 64 open issues, last push 2026-03-24 (about seven months old). Remote server `https://mcp.excalidraw.com` or local stdio/HTTP or a `.mcpb` bundle for Claude Desktop; built on MCP Apps so clients that support it render the drawing inside chat. Tools: `read_me` (format cheat sheet) and `create_view` (takes element JSON, streams an SVG render, then returns a screenshot to the model). The README does not mention Claude Code. Caution: the hosted server sees your diagram JSON; the checkpoint store can sit in memory or Redis. (e) None. (f) The screenshot returned by `create_view` lets the agent look at what it drew; export to a file is not described.
**Pros for agentic work:**
- Simple JSON format; official MCP server with visual feedback.
- Free, open source, no account for basic use.
**Cons for agentic work:**
- Hand-drawn style is not precise for architecture diagrams.
- MCP repo lacks a licence file and has not been updated for seven months.
**Verdict:** Medium. Text JSON and an official MCP with a screenshot loop, but file export and licence are unclear.
**Sources:** https://api.github.com/repos/excalidraw/excalidraw, https://api.github.com/repos/excalidraw/excalidraw-mcp, https://api.github.com/repos/excalidraw/excalidraw-mcp/contents/, https://raw.githubusercontent.com/excalidraw/excalidraw-mcp/main/README.md and /CLAUDE.md (all VERIFIED).

### Miro
**What it is:** Cloud whiteboard for workshops and design docs, with an official MCP server for AI tools.
**Cost:** Subscription SaaS with a free tier. The MCP docs page I read first said the server works on all plans including free teams; a second page did not address plans, so confirm (REPORTED). Enterprise admins must switch the server on. Terms: https://miro.com/legal/terms-of-service/ (not read, UNVERIFIED).
**Open source:** No.
**Extendable:** REST API and Web SDK apps (UNVERIFIED here); the MCP server.
**Agent integration:** (a) Boards live in the cloud; no text file to diff. (b) No CLI. (c) REST API (UNVERIFIED). (d) **Official MCP server**, `https://mcp.miro.com`; Claude Code: install the Miro plug-in or `claude mcp add --transport http miro https://mcp.miro.com`, then `/mcp` to sign in; sign-in uses OAuth 2.1 and respects existing board permissions. Codex: through a plug-in; I found no verified `codex mcp add` command. The tools page I read lists 52 tools (28 read, 24 write): create and update board content from SVG, read board areas as SVG, tables, comments, sharing and role changes, prototypes from HTML, images, spaces. Board summarising uses AI credits. The tool list differs between Miro's pages, so expect change. Caution: it can share boards and change roles; board comments and sticky notes are untrusted text from other people, which an agent must treat as data. (e) Miro has built-in AI (UNVERIFIED). (f) `canvas_read_as_svg` lets the agent read back what it made.
**Pros for agentic work:**
- Official MCP with OAuth and a wide tool set, including SVG round trips.
- Fine for workshop boards and non-programmers.
**Cons for agentic work:**
- Cloud-only, proprietary, no git history.
- Sharing and role tools widen what a mistaken or misled agent can change.
**Verdict:** Medium. Official MCP, but the data lives in a vendor cloud and cannot be diffed.
**Sources:** https://developers.miro.com/docs/miro-mcp, https://developers.miro.com/docs/miro-mcp-tools, https://developers.miro.com/docs/mcp-intro (VERIFIED); Miro connection guide via search (REPORTED).

---

## Summary table

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
