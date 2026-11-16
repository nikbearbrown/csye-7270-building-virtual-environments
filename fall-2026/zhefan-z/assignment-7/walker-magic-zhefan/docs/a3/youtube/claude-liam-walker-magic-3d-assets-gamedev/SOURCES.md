# SOURCES — walker-magic Assignment 3 gamedev film

## Source revision
Commit `8d8895c` (`8d8895cf80a68d85e18e9142b6a687c68618c51d`) on branch `zhefan-z/assignment-3`; `walker-magic-zhefan` tree `79ea0965c11386d2b3fac1a8eb39bd20f29f4149`. Game files identical to `1bacec8`. Excerpts and hashes come from a `git archive` snapshot of that tree (`gamedev-evidence.json`).

## Engine capture
`capture/run-01.avi` — Godot Movie Maker, 3840×2160 MJPEG @ 60 fps, 720 frames, sha256 `d3ec6d17142c06ce8ea931f3dafc31ed1d6fa3d572a156984b575b8c9351a696`, scripted camera on a capture copy of `8d8895c` (CAPTURE.md). Not in Git.

## Recorded output
- `evidence/test_a3_assets-8d8895c.log` — `tests/test_a3_assets.gd`, headless, on the reference copy of `8d8895c` (B18).
- `evidence/glb-read-8d8895c.log` — `scripts/read_glb.py` on the reference copy's `assets/models/` (B13).

## The author's screenshots (labelled "My screenshot")
In `fall-2026/zhefan-z/assignment-3/evidence/`: `blender-learn-uv-sphere-960-tris.png`, `blender-learn-icosphere-subdiv1-20-tris.png`, `blender-learn-cone-6-verts-10-tris.png` (B03), `claude-code-rock-plan-approval.png` (B04), `hand-edit-crystal-short-b-rotz20.png` (B07), `prop-room-f6-before-fixes.png`, `prop-room-editor-above-before-fixes.png`, `prop-room-editor-below-before-fixes.png` (B14). None is a reconstruction.

## Claude Code's Blender MCP look renders (labelled "Blender MCP look render — captured by Claude Code")
Saved by the MCP `look` tool on 2026-10-14 in the Claude Code session's tool results; copied unchanged into `evidence/look/` (hashes in `evidence/media-provenance.json`):

| File | Original | Time | sha256 (first 16) |
|---|---|---|---|
| `rock-first-build.png` | `mcp-blender-blob-1792017743552-i6lcdy.png` | 18:42 | `aebdb478705e8a1e` |
| `rock-revision-1.png` | `mcp-blender-blob-1792018303030-f9n62h.png` | 18:51 | `9eaa306dadc13697` |
| `crystal.png` | `mcp-blender-blob-1792020244403-4apygw.png` | 19:24 | `98e0eb12ccfb80e5` |
| `chest-gold-metallic-1.0.png` | `mcp-blender-blob-1792021347883-kxuazh.png` | 19:42 | `4daf14af65c93bcd` |

Each is 1031×686 (six views); the film shows them enlarged and says so. The chest render predates the gold change (metallic 1.0, shown as such).

## Documents the narration draws on
`fall-2026/zhefan-z/assignment-3/CHANGE-BRIEF.md`, `TEST-REPORT.md` and `FRICTIONAL.md` at `8d8895c`; `tools/blender/build_*.py` (numbers printed by the recorded calls); FACTCHECK.md maps each sentence.

## Tools
Brutalist (`E:\7270\brutalist.art`, commit `29ba0e8`, with one uncommitted local change: `runtime/remotion/package-lock.json`): `godot-gamedev` + `walker`, Remotion compositions `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`. Kokoro-82M `am_onyx` (local). Pillow cards in the Claude palette (EB Garamond, Inter, PT Mono from the toolkit). FFmpeg 9.0.2. Godot 4.7.2. Blender 5.2.2 LTS with MCP for Blender 2.1.9 (add-on 1.8). No paid service, no generated media, no captions. Nothing published.
