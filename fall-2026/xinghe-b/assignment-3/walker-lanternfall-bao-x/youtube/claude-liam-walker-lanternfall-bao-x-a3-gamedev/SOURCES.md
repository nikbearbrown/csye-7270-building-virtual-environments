# SOURCES — what the film is made of

| Item | Source | Hash / version |
|---|---|---|
| Game source shown | `godot/` at c0dba4c000330c4b770c4244ad85cde2d55d3440 | `gamedev-evidence.json` (17 files hashed) |
| Godot takes | Movie Maker, isolated `git archive c0dba4c godot` copy, 3840 × 2160, 30 fps (CAPTURE.md) | `capture/takes.sha256` |
| Blender window stills | Blender 5.2.2 LTS `bpy.ops.screen.screenshot` through `execute_blender_code` (mcp-for-blender 2.1.9, add-on 1.8) | `images/blender/SHA256SUMS` |
| MCP look renders | the MCP `look` tool during the real builds | `evidence/a3/mcp/*-look.png` (committed) |
| Brief, logs, notes, scripts | CHANGE-BRIEF.md, `evidence/a3/setup/04-mcp-connect.log`, `evidence/a3/mcp/*-session.md`, BLENDER-NOTES.md, `tools/blender/build_supply_stack.py` | repository at the submission commit |
| Recorded test output | `capture/test-run-film-build-raw.txt` (fresh archive of c0dba4c) | — |
| Session excerpt (B04) | this Claude Code session, 2026-10-14 11:59 EDT | verbatim; English gloss labelled |
| Bao's look (B16) | Bao, 2026-10-15 | verbatim; English labelled as Claude's translation |
| Narration | Kokoro-82M v1.0 (kokoro-onnx), voice `am_onyx`, local; loudnorm −16 LUFS (`tools/level_audio.py`) | `mp3/` (not committed) |
| Outro jingle | stock `logos/bear-brown/bear-brown-1.mp3` from the course toolkit (slug seed 4476 mod 6 = 0) | toolkit file |
| Scenes and fonts | the course's Brutalist toolkit (brutalist.art): ClaudeComposerAsk, BrutalistHesitantWriter, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro; EB Garamond, Inter, PT Mono (toolkit fonts); STHeiti Light (macOS) for Chinese | toolkit checkout |
| Composition | `tools/compose.py` (ffmpeg), `tools/build_media.py` | — |

No paid service, model download or upload was used for the film. The rendered MP4 is kept out of git; the course
media link, file name and SHA-256 go in the repository README and SUBMISSION once Bao has uploaded it.
