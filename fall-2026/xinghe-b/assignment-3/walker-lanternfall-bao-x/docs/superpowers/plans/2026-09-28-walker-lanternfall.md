# walker-lanternfall-bao-x Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship Assignment 2: a playable Godot 4.7.2 survivors-like asset slice ("Lanternfall") whose art, 6 SFX and a seamless music loop were generated with local open models *after* a committed design package, plus logs, tests, a 4K film and a matching Canvas submission.

**Architecture:** Plain GDScript, code-built scene. A `GameState` state machine is the single source of truth; a `session.gd` node owns a deterministic fixed-tick simulation (`tick()`), so headless tests can drive it synchronously. `AudioBus` only *subscribes* to session signals and throttles playback through a pure `SfxGate`; nothing reads audio back. A Python pipeline under `gen/` runs local models, writes one JSON sidecar per generation, and renders `ASSET-LOG.md` from those sidecars.

**Tech Stack:** Godot 4.7.2.stable.official.ed1daf0bf (GL Compatibility, GDScript), Python 3.12 via `uv` (two venvs), mflux + FLUX.1-schnell, diffusers + Stable Audio Open 1.0, transformers + MusicGen (medium, melody), Pillow, numpy, soundfile, librosa, git + gh.

**Spec:** `docs/superpowers/specs/2026-09-28-walker-lanternfall-design.md`

## Global Constraints

- Project/folder/repo name: `walker-lanternfall-bao-x`; lives at `/Users/yxlh/Documents/csye 7270/walker-lanternfall-bao-x`.
- Started from: a blank Godot 4 project; protagonist concept continues A1 `walker-jumpman-bao-x` (itself from nikbearbrown/walker-jumpman). State this in README and SUBMISSION.
- Engine: `/Applications/Godot.app/Contents/MacOS/Godot` = 4.7.2.stable.official.ed1daf0bf. Referred to below as `$GODOT`.
- Viewport 640×360, window 1280×720, stretch `canvas_items`, nearest texture filtering.
- No `class_name` anywhere — every cross-file reference is `const X = preload("res://…")` so a fresh clone runs headless tests without an editor import of the class cache.
- **No generation before tag `design-v1`.** After it, the four design docs are append-only: changes go under a dated `## Revisions` heading at the bottom.
- Game audio is WAV (SFX) and OGG Vorbis (music). Never commit MP3/MP4/AVI, files > 25 MB, `.godot/`, model weights, venvs, or tokens.
- Prompts must not name living artists, copyrighted characters, brands, existing music/recordings, or real voices.
- Sounds only reflect events. Game logic must be identical with streams missing or buses muted.
- Every SFX fires once per event; held/repeated input never causes repeated SFX.
- Character palette (exact): `#F2B84B` lamp gold, `#FFF1C9` glow cream, `#2E3A59` coat navy, `#8A5A3C` satchel brown, `#14121C` outline ink.
- Environment palette (exact): `#0E1020` night, `#1F2540` deep fog, `#3B4A6B` mid fog, `#6E7FA3` light fog, `#C7D0E0` mist, `#F2B84B` lantern gold, `#B5523B` stall red, `#14121C` ink.
- Player collision: circle r = 10 px centred on the torso; sprite frame 32×32 drawn at `Rect2(-16, -20, 32, 32)` so frame pixel (16, 20) is the collision centre.
- Human-only decisions (Bao): design approval, every accept/reject of a generation, both playtests, `FRICTIONAL.md` content, video upload, Canvas submission, any public push.
- Commit author: repo-local `baoxinghe <734283951@qq.com>`; every commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Deliverable docs are written in English.

## Review Focus

1. **Several level-ups from one pickup burst, or a level-up earned while paused** → cards open one level at a time, in order, only while PLAYING; exactly one SFX-04 per level. Pinned in Task 10 (`levelup-queue`, `levelup-while-paused`).
2. **R pressed during pause, level-up or the lose fade-out** → the new run's music starts from 0 at full volume with the low-pass off; the old fade tween must not silence it. Pinned in Task 11 (`restart-during-fade`, `restart-from-pause`).
3. **Death on the same tick the timer hits 3:00** → exactly one terminal state (LOST wins, because damage resolves before the timer) and exactly one stinger. Pinned in Task 10 (`death-and-timer-same-tick`) and Task 11 (`one-stinger`).
4. **A fresh clone with missing/unimported art or audio** → placeholders draw, silence plays, nothing crashes, state identical. Pinned in Task 10 (`missing-art-no-crash`) and Task 11 (`independence`).
5. **Diagonal input and small stick drift** → diagonal speed equals cardinal speed; facing does not flip for |x| ≤ 0.1. Pinned in Task 10 (`diagonal-normalized`, `facing-deadzone`).

## Schedule

| Date | Tasks |
|---|---|
| Mon 9/28 | 1–6 (design package, human gate, tag `design-v1`); start 13 install in background |
| Tue 9/29 | 7–12 (greybox game + tests) |
| Wed 9/30 | 13–16 (pipeline, art) |
| Thu 10/1 | 17–19 (SFX, music, integration) |
| Fri 10/2 | 20–21 (playtests, revision loop, reports) |
| Sat 10/3 | 22 (film) |
| Sun 10/4 | 23 (fresh-clone verify, submit) — buffer |

## File Structure

```
walker-lanternfall-bao-x/
├── README.md  CONCEPT.md  STORYBOARD.md  CHARACTER-SHEET.md  CHANGE-BRIEF.md
├── ASSET-LOG.md (rendered)  SOURCES.md  TEST-REPORT.md  FRICTIONAL.md  SUBMISSION.md
├── walker-lanternfall.command          # macOS double-click launcher
├── design/
│   ├── storyboard/make_panels.py       # writes panel-01..09.svg
│   ├── storyboard/panel-*.svg
│   └── character/make_blockout.py      # pre-generation blockout, silhouettes, collision overlay
├── gen/
│   ├── requirements-art.txt  requirements-audio.txt
│   ├── common.py            # paths, run ids, sidecars, thumbnails
│   ├── art_generate.py      # FLUX.1-schnell via mflux
│   ├── art_process.py       # crop → fit → palette-lock → sheet
│   ├── tile_process.py      # seamless ground tile
│   ├── sfx_generate.py      # Stable Audio Open
│   ├── sfx_process.py       # trim/fade/normalise → WAV
│   ├── music_generate.py    # MusicGen (medium / melody)
│   ├── music_loop.py        # beat-aligned crossfade loop → OGG
│   ├── decide.py            # records Bao's accept/modify/reject into a sidecar
│   ├── render_log.py        # sidecars → ASSET-LOG.md
│   ├── contact_sheet.py
│   ├── checks/palette_check.py  checks/loop_check.py
│   ├── prompts/*.json       # one prompt spec per asset
│   ├── log/<ASSET-ID>/<run>.json   thumbs/<ASSET-ID>/<run>.png
│   ├── accepted/<ASSET-ID>/…       rejected/<ASSET-ID>/…   (raw/ is git-ignored)
├── scripts/audit_repo.py    # check 6 + design-before-generation order proof
├── evidence/                # JSON receipts, screenshots
├── film/                    # beat sheet, script, prompts (no MP4)
└── godot/
    ├── project.godot
    ├── game/main.tscn  game/session.gd  game/game_state.gd
    ├── features/tuning.gd  features/art.gd
    ├── features/player/player.gd
    ├── features/enemies/enemy.gd  features/enemies/spawner.gd
    ├── features/pickups/gem.gd
    ├── features/weapons/beam_shot.gd  features/weapons/weapon_fx.gd
    ├── features/progression/progression.gd
    ├── features/world/ground.gd
    ├── audio/sfx_gate.gd  audio/audio_bus.gd
    ├── ui/hud.gd
    ├── assets/art/{manifest.json,palettes.json,*.png}  assets/sfx/*.wav  assets/music/*.ogg
    └── tests/harness.gd  test_logic.gd  test_gameplay.gd  test_audio.gd
```

---

# Phase A — Design package (no generation allowed)

### Task 1: Repository scaffold, blank Godot project, hygiene audit

**Files:**
- Modify: `.gitignore`
- Create: `godot/project.godot`, `godot/game/main.tscn`, `godot/game/session.gd` (stub), `walker-lanternfall.command`, `scripts/audit_repo.py`, `README.md` (stub)

**Interfaces:**
- Produces: `python3 scripts/audit_repo.py [--stage design|final]` → exit 0/1, writes `evidence/repo-audit.json`.

- [ ] **Step 1: Replace `.gitignore`**

```gitignore
.godot/
.DS_Store
*.mp3
*.mp4
*.avi
*.mov
.env
*.safetensors
*.ckpt
*.bin
gen/.venv-*/
gen/raw/
gen/cache/
film/**/media/
film/**/exports/
film/**/renders/
```

- [ ] **Step 2: Write `godot/project.godot`**

```ini
; Engine configuration file.
config_version=5

[application]

config/name="walker-lanternfall-bao-x"
run/main_scene="res://game/main.tscn"
config/features=PackedStringArray("4.7", "GL Compatibility")

[display]

window/size/viewport_width=640
window/size/viewport_height=360
window/size/window_width_override=1280
window/size/window_height_override=720
window/stretch/mode="canvas_items"

[rendering]

renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/canvas_textures/default_texture_filter=0
environment/defaults/default_clear_color=Color(0.055, 0.063, 0.125, 1)
```

- [ ] **Step 3: Write `godot/game/main.tscn` and a stub `godot/game/session.gd`**

```
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://game/session.gd" id="1"]

[node name="Main" type="Node2D"]
script = ExtResource("1")
```

```gdscript
extends Node2D
# Replaced in Task 10.
```

- [ ] **Step 4: Write the launcher `walker-lanternfall.command` and `chmod +x` it**

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec /Applications/Godot.app/Contents/MacOS/Godot --path godot
```

- [ ] **Step 5: Write `scripts/audit_repo.py`**

```python
#!/usr/bin/env python3
"""audit_repo.py — check 6: repository hygiene, asset-ID coverage and design-before-generation order.

    python3 scripts/audit_repo.py --stage design   # before assets exist
    python3 scripts/audit_repo.py --stage final    # every CHANGE-BRIEF asset ID must have files

Exit 0 when clean, 1 otherwise. Writes evidence/repo-audit.json.
"""
import argparse, datetime as dt, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_EXT = {".mp3", ".mp4", ".avi", ".mov", ".safetensors", ".ckpt"}
MAX_BYTES = 25 * 1024 * 1024
SECRET = re.compile(r"(hf_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,})")
ASSET_ID = re.compile(r"\b(?:ART-[A-Z]+-\d{2}|SFX-\d{2}[ab]?|MUS-\d{2})\b")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["design", "final"], default="final")
    stage = ap.parse_args().stage
    problems: list[str] = []
    files = [f for f in git("ls-files", "-z").split("\0") if f]
    for f in files:
        p = ROOT / f
        if Path(f).suffix.lower() in FORBIDDEN_EXT:
            problems.append(f"forbidden file type: {f}")
        if f.startswith(".godot/") or "/.godot/" in f:
            problems.append(f"godot cache committed: {f}")
        if p.exists() and p.stat().st_size > MAX_BYTES:
            problems.append(f"file over 25 MB: {f}")
        if p.exists() and p.suffix.lower() in {".md", ".json", ".py", ".gd", ".txt", ".cfg", ".godot", ".tscn"}:
            if SECRET.search(p.read_text(errors="ignore")):
                problems.append(f"possible credential in {f}")

    order: dict = {}
    tag_time = git("log", "-1", "--format=%cI", "design-v1").strip()
    if stage == "final":
        if not tag_time:
            problems.append("tag design-v1 missing")
        else:
            order["design_v1_committed"] = tag_time
            t0 = dt.datetime.fromisoformat(tag_time)
            for side in sorted((ROOT / "gen" / "log").glob("*/*.json")):
                created = dt.datetime.fromisoformat(json.loads(side.read_text())["created_utc"])
                if created <= t0:
                    problems.append(f"generation predates design-v1: {side.relative_to(ROOT)}")
            first_gen = git("log", "--diff-filter=A", "--format=%H", "--reverse", "--", "gen/log").split()
            if first_gen and subprocess.run(["git", "merge-base", "--is-ancestor", "design-v1", first_gen[0]], cwd=ROOT).returncode != 0:
                problems.append("first gen/log commit is not a descendant of design-v1")
            order["first_generation_commit"] = first_gen[0] if first_gen else None

        brief = (ROOT / "CHANGE-BRIEF.md").read_text() if (ROOT / "CHANGE-BRIEF.md").exists() else ""
        ids = sorted(set(ASSET_ID.findall(brief)))
        manifest_path = ROOT / "godot/assets/manifest.json"
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        for asset_id in ids:
            paths = manifest.get(asset_id)
            if not paths:
                problems.append(f"{asset_id} listed in CHANGE-BRIEF but not in godot/assets/manifest.json")
                continue
            for rel in paths:
                if not (ROOT / rel).exists():
                    problems.append(f"{asset_id}: missing file {rel}")
        order["asset_ids_checked"] = ids

    out = {"stage": stage, "files_checked": len(files), "problems": problems, **order}
    (ROOT / "evidence").mkdir(exist_ok=True)
    (ROOT / "evidence" / "repo-audit.json").write_text(json.dumps(out, indent=2) + "\n")
    for p in problems:
        print("PROBLEM", p)
    print(f"repo-audit ({stage}): {len(problems)} problem(s), {len(files)} files")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 6: Verify the project opens headless and the audit passes**

Run: `cd godot && $GODOT --headless --path . --import --quit; cd .. && python3 scripts/audit_repo.py --stage design`
Expected: Godot exits 0 with no script errors; audit prints `repo-audit (design): 0 problem(s)`.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "Scaffold blank Godot 4.7 project, launcher and repo audit

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: `CONCEPT.md`

**Files:** Create `CONCEPT.md`

- [ ] **Step 1: Write `CONCEPT.md` (one page, English) with exactly these sections**

1. `# Lanternfall — Concept` + header line: `walker-lanternfall-bao-x · Bao Xing · v1 written 2026-09-28, before any generation`.
2. **In two sentences:** "A lamp-headed courier is trapped in a fog-bound midnight market, and the light on his shoulders is his only weapon. Keep moving, grow the light, and survive three minutes until the fog lifts."
3. **Core loop:** the 7-step loop from spec §3, as a numbered list.
4. **Design pillars** (4): *Light is power*; *Feet, not fingers* (movement is the only verb; decisions live in upgrades); *Readable in silence* (every event has a visual); *Three-minute runs* (instant retry, no punishment).
5. **Systems in this slice:** Beam (rate | pierce), Moth Orbit (count | radius), 3 passives, Sunflare Lighthouse evolution when both weapons hit level 3; moth and fog-wraith enemies; 30 s density steps.
6. **Art direction:** 3/4 top-down, flat-vector shapes reduced to 32-px pixel sprites; warm lamp palette (character) against cool fog palette (environment); value contrast rule: player and pickups always the brightest objects, enemies mid-value, ground darkest. Both palettes listed with hex.
7. **Audio direction:** soft, warm, glassy/bell-like SFX for good events; dull, low, muffled for harm; no harsh high transients because kills are frequent.
8. **Music:** when it plays (run start), changes (Sunflare layer fades in; pause = low-pass + −10 dB; level-up = −6 dB), and stops (lose: 0.5 s fade + stinger; win: 1 s fade + stinger; menu silent).
9. **Semester goal (out of slice scope):** more weapons/recipes, bosses, meta progression, saving, multiple maps.
10. **Starting point:** blank Godot 4.7.2 project; character from A1 `walker-jumpman-bao-x`.
11. **Tools:** `/gdd` was / was not used (state truthfully); final design decisions are Bao's.

- [ ] **Step 2: Commit**

```bash
git add CONCEPT.md && git commit -m "Add CONCEPT v1 (pre-generation)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: `STORYBOARD.md` + nine 16:9 SVG panels

**Files:** Create `design/storyboard/make_panels.py`, `design/storyboard/panel-01.svg … panel-09.svg`, `STORYBOARD.md`

**Interfaces:** Produces panel IDs `P1`…`P9` referenced by CHANGE-BRIEF and ASSET-LOG.

Panel plan (shot size / angle / movement):

| ID | Beat | Shot | Angle | Movement |
|---|---|---|---|---|
| P1 | First thing seen: title over fogged market | Wide | High angle (3/4 overhead) | Slow push-in |
| P2 | Run starts, courier centred, music begins | Medium | Top-down (bird's-eye) | — |
| P3 | Core action: move, beam fires, moth dies, gem flies in | Medium | Top-down | Player motion arrows + gem path |
| P4 | Level-up: 3 cards, cheering portrait | Close-up | Eye level (UI portrait) | — |
| P5 | Hurt: wraith contact, red flash, knockback | Close-up | Dutch/tilted top-down | Knockback arrow |
| P6 | Evolution: Sunflare burst clears ring | Wide | High angle | Zoom-out + ring expansion |
| P7 | Failure: lamp out, defeat pose, result panel | Close-up | Top-down | — |
| P8 | Retry: R → instant return to P2 framing | Medium | Top-down | Hard cut |
| P9 | End of run: 3:00, fog lifts, victory portrait | Wide | Low angle (portrait on end panel) | Fog pull-back |

- [ ] **Step 1: Write `design/storyboard/make_panels.py`**

```python
#!/usr/bin/env python3
"""Writes greybox 16:9 storyboard panels (1920x1080 SVG). Pre-generation: shapes only, no generated art."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
W, H = 1920, 1080
INK, FOG, MIST, GOLD, CREAM, RED = "#14121C", "#3B4A6B", "#C7D0E0", "#F2B84B", "#FFF1C9", "#B5523B"

def courier(x, y, s=1.0, pose="idle"):
    arm = {"cheer": f'<line x1="{x+8*s}" y1="{y-10*s}" x2="{x+26*s}" y2="{y-40*s}" stroke="{INK}" stroke-width="{5*s}"/>',
           "cast": f'<line x1="{x+10*s}" y1="{y-6*s}" x2="{x+40*s}" y2="{y-6*s}" stroke="{INK}" stroke-width="{5*s}"/>'}.get(pose, "")
    tilt = ' transform="rotate(80 %d %d)"' % (x, y) if pose == "down" else ""
    return (f'<g{tilt}><rect x="{x-14*s}" y="{y-10*s}" width="{28*s}" height="{36*s}" fill="{FOG}" stroke="{INK}" stroke-width="{3*s}"/>'
            f'<rect x="{x-26*s}" y="{y}" width="{12*s}" height="{16*s}" fill="#8A5A3C" stroke="{INK}" stroke-width="{2*s}"/>'
            f'<circle cx="{x}" cy="{y-30*s}" r="{20*s}" fill="{GOLD if pose != "down" else FOG}" stroke="{INK}" stroke-width="{3*s}"/>{arm}</g>')

def moth(x, y, s=1.0):
    return f'<ellipse cx="{x}" cy="{y}" rx="{16*s}" ry="{9*s}" fill="{MIST}" stroke="{INK}" stroke-width="2"/>'

def wraith(x, y, s=1.0):
    return f'<path d="M{x-30*s},{y+30*s} Q{x},{y-60*s} {x+30*s},{y+30*s} Z" fill="{FOG}" stroke="{INK}" stroke-width="3" opacity="0.9"/>'

def arrow(x1, y1, x2, y2, color=INK):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="8" marker-end="url(#ah)" stroke-dasharray="24 12"/>')

def card(x, y, title):
    return (f'<rect x="{x}" y="{y}" width="380" height="520" rx="18" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>'
            f'<text x="{x+190}" y="{y+80}" font-size="40" text-anchor="middle" fill="{INK}">{title}</text>')

def frame(n, title, shot, angle, move, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><marker id="ah" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{INK}"/></marker></defs>
<rect width="{W}" height="{H}" fill="#1F2540"/>
{body}
<rect x="0" y="0" width="{W}" height="90" fill="{INK}" opacity="0.85"/>
<text x="30" y="60" font-size="44" fill="{CREAM}" font-family="Helvetica">P{n} · {title}</text>
<text x="{W-30}" y="60" font-size="34" fill="{GOLD}" font-family="Helvetica" text-anchor="end">{shot} · {angle} · {move}</text>
<rect x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="{CREAM}" stroke-width="8"/>
</svg>'''

def fog(n=14):
    return "".join(f'<circle cx="{(i*337)%W}" cy="{150+(i*211)%(H-200)}" r="{120+(i*53)%140}" fill="{MIST}" opacity="0.08"/>' for i in range(n))

stalls = "".join(f'<rect x="{x}" y="{y}" width="160" height="110" fill="{RED}" stroke="{INK}" stroke-width="4"/><circle cx="{x+80}" cy="{y-20}" r="18" fill="{GOLD}"/>' for x, y in [(160, 300), (1500, 260), (300, 820), (1380, 780), (900, 200)])

PANELS = [
    ("First look: LANTERNFALL", "Wide", "High angle", "Push-in",
     fog(20) + stalls + courier(960, 620, 1.6) + f'<text x="960" y="420" font-size="120" text-anchor="middle" fill="{GOLD}" font-family="Helvetica">LANTERNFALL</text><text x="960" y="960" font-size="44" text-anchor="middle" fill="{CREAM}">Enter / A to start</text>'
     + '<rect x="300" y="170" width="1320" height="860" fill="none" stroke="#FFF1C9" stroke-width="4" stroke-dasharray="20 14"/>' + arrow(300, 170, 380, 230, CREAM)),
    ("Run begins", "Medium", "Top-down", "Static",
     fog() + courier(960, 560, 2.2) + f'<text x="960" y="160" font-size="56" text-anchor="middle" fill="{CREAM}">0:00</text>' + moth(300, 300) + moth(1650, 850)),
    ("Core action: move, fire, collect", "Medium", "Top-down", "Player motion",
     fog() + courier(760, 560, 2.0, "cast") + arrow(560, 700, 700, 600) + f'<rect x="860" y="540" width="360" height="16" fill="{CREAM}"/>'
     + moth(1300, 548, 1.5) + f'<polygon points="1420,520 1440,548 1420,576 1400,548" fill="{GOLD}"/>' + arrow(1420, 600, 860, 640, GOLD)),
    ("Level up: choose one", "Close-up", "Eye level", "Static",
     f'<rect width="{W}" height="{H}" fill="{INK}" opacity="0.6"/>' + card(260, 300, "Beam: Quick Wick") + card(770, 300, "Moth: Second Wing") + card(1280, 300, "Magnet Satchel")
     + courier(200, 980, 3.0, "cheer")),
    ("Hurt: wraith contact", "Close-up", "Dutch top-down", "Knockback",
     f'<g transform="rotate(-8 960 540)">' + fog() + wraith(1120, 560, 4) + courier(820, 600, 3.2) + arrow(760, 620, 480, 700, RED)
     + f'</g><rect width="{W}" height="{H}" fill="{RED}" opacity="0.18"/>'),
    ("Evolution: Sunflare Lighthouse", "Wide", "High angle", "Zoom-out + ring",
     fog() + "".join(moth(960 + 520 * __import__('math').cos(a / 3), 560 + 360 * __import__('math').sin(a / 3)) for a in range(19))
     + f'<circle cx="960" cy="560" r="330" fill="none" stroke="{GOLD}" stroke-width="18"/>' + courier(960, 600, 1.4, "cheer")
     + f'<text x="960" y="200" font-size="70" text-anchor="middle" fill="{GOLD}">SUNFLARE LIGHTHOUSE</text>' + arrow(700, 300, 560, 220, CREAM)),
    ("Failure: the lamp goes out", "Close-up", "Top-down", "Static",
     fog() + courier(960, 520, 3.4, "down") + f'<rect x="560" y="760" width="800" height="220" fill="{INK}" opacity="0.85"/><text x="960" y="850" font-size="56" text-anchor="middle" fill="{CREAM}">The lamp went out — 2:14</text><text x="960" y="930" font-size="40" text-anchor="middle" fill="{GOLD}">R / Y to retry</text>'),
    ("Retry: straight back in", "Medium", "Top-down", "Hard cut",
     fog() + courier(960, 560, 2.2) + f'<text x="960" y="160" font-size="56" text-anchor="middle" fill="{CREAM}">0:00</text><text x="120" y="1000" font-size="44" fill="{GOLD}">CUT from P7 &lt; 0.2 s</text>'),
    ("End of run: the fog lifts", "Wide", "Low angle", "Fog pull-back",
     f'<rect width="{W}" height="{H}" fill="#6E7FA3"/>' + courier(960, 900, 5.0, "cheer") + f'<text x="960" y="260" font-size="90" text-anchor="middle" fill="{CREAM}">3:00 — The fog lifts</text>' + arrow(1500, 500, 1800, 300, CREAM)),
]

for i, (title, shot, angle, move, body) in enumerate(PANELS, start=1):
    (OUT / f"panel-{i:02d}.svg").write_text(frame(i, title, shot, angle, move, body))
print(f"wrote {len(PANELS)} panels to {OUT}")
```

- [ ] **Step 2: Run it and eyeball two panels**

Run: `python3 design/storyboard/make_panels.py && open design/storyboard/panel-03.svg design/storyboard/panel-06.svg`
Expected: `wrote 9 panels`; panels show header strip with shot/angle/movement and readable shapes.

- [ ] **Step 3: Write `STORYBOARD.md`**

Header (version, date, "pre-generation greybox; hand-drawn replacements may be added under Revisions"), the panel-plan table above, then one section per panel:

```markdown
## P3 · Core action: move, fire, collect
![P3](design/storyboard/panel-03.svg)
- **Shot / angle / movement:** Medium · Top-down · player motion arrows and gem path
- **Player does:** holds a direction (WASD / arrows / left stick)
- **Screen shows:** courier in cast pose, beam leaving along movement direction, moth breaking, gem flying to the satchel
- **Sound:** SFX-01 on the kill (throttled), SFX-02 when the gem lands; MUS-01 underneath
- **Assets:** ART-PC-01 (cast, walk_contact, walk_passing), ART-EN-01, ART-FX-01, ART-PK-01, ART-ENV-01
- **Why:** proves the only verb (movement) produces every reward; the gem path shows the loop without text
```

Coverage summary table at the end: shot sizes used (Wide P1/P6/P9, Medium P2/P3/P8, Close-up P4/P5/P7), angles (high, top-down, eye level, dutch, low), movement panels (P1, P3, P5, P6, P9), required beats mapped (first seen P1, core action P3, success P4/P6, failure P7, retry P8, end P9).

- [ ] **Step 4: Commit**

```bash
git add design/storyboard STORYBOARD.md && git commit -m "Add nine-panel greybox storyboard (pre-generation)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: `CHARACTER-SHEET.md` + pre-generation blockout images

**Files:** Create `design/character/make_blockout.py`, outputs `design/character/blockout-poses-x8.png`, `silhouette-32.png`, `collision-overlay-x8.png`, `palette.png`; `CHARACTER-SHEET.md`

**Interfaces:** Produces the canonical pose order used by `player.gd` and `art_process.py`:
`["turn_front","turn_side","turn_back","idle","walk_contact","walk_passing","cast","hurt","levelup","sunflare","defeat","victory"]`

- [ ] **Step 1: Write `design/character/make_blockout.py`**

```python
#!/usr/bin/env python3
"""Pre-generation character blockout at true game size (32x32), plus silhouette and collision overlays."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
GOLD, CREAM, NAVY, BROWN, INK = "#F2B84B", "#FFF1C9", "#2E3A59", "#8A5A3C", "#14121C"
POSES = ["turn_front", "turn_side", "turn_back", "idle", "walk_contact", "walk_passing",
         "cast", "hurt", "levelup", "sunflare", "defeat", "victory"]
# per pose: head offset (dx,dy), torso lean px, left/right leg foot x offsets, arm end (dx,dy) or None, satchel visible, glow
SPEC = {
    "turn_front":   dict(head=(0, 0), lean=0, legs=(-3, 3), arm=None, bag=False, glow=False),
    "turn_side":    dict(head=(1, 0), lean=0, legs=(-1, 1), arm=None, bag=True, glow=False),
    "turn_back":    dict(head=(0, 0), lean=0, legs=(-3, 3), arm=None, bag=True, glow=False, back=True),
    "idle":         dict(head=(1, 0), lean=0, legs=(-2, 2), arm=None, bag=True, glow=True),
    "walk_contact": dict(head=(1, 1), lean=1, legs=(-5, 5), arm=(-5, 2), bag=True, glow=True),
    "walk_passing": dict(head=(1, -1), lean=0, legs=(0, 1), arm=None, bag=True, glow=True),
    "cast":         dict(head=(2, 0), lean=2, legs=(-3, 4), arm=(9, -2), bag=True, glow=True),
    "hurt":         dict(head=(-3, 2), lean=-3, legs=(-4, 1), arm=(-7, -4), bag=True, glow=False),
    "levelup":      dict(head=(0, -2), lean=0, legs=(-3, 3), arm=(4, -12), bag=True, glow=True),
    "sunflare":     dict(head=(0, -1), lean=0, legs=(-4, 4), arm=(8, -10), bag=True, glow=True, big=True),
    "defeat":       dict(head=(-9, 12), lean=-9, legs=(4, 7), arm=None, bag=True, glow=False, down=True),
    "victory":      dict(head=(0, -2), lean=0, legs=(-4, 4), arm=(6, -12), bag=True, glow=True),
}

def pose(name: str, silhouette: bool = False) -> Image.Image:
    s = SPEC[name]
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (lambda col: INK) if silhouette else (lambda col: col)
    hx, hy = 16 + s["head"][0], 8 + s["head"][1]
    if s.get("down"):
        d.rectangle([6, 22, 24, 27], fill=c(NAVY), outline=INK)
        d.ellipse([1, 19, 11, 29], fill=c(NAVY if not silhouette else INK), outline=INK)
        return im
    if s["glow"] and not silhouette:
        r = 13 if s.get("big") else 10
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 241, 201, 90))
    for fx in s["legs"]:
        d.line([16 + fx // 2, 26, 16 + fx, 31], fill=INK, width=2)
    tx = 16 + s["lean"]
    d.rectangle([tx - 5, 14, tx + 5, 26], fill=c(NAVY), outline=INK)
    if s["bag"]:
        d.rectangle([tx - 9, 18, tx - 5, 23], fill=c(BROWN), outline=INK)
    if s["arm"]:
        d.line([tx + 3, 17, tx + 3 + s["arm"][0], 17 + s["arm"][1]], fill=INK, width=2)
    d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=c(NAVY if s.get("back") else GOLD), outline=INK)
    if not s.get("back") and not silhouette:
        d.rectangle([hx - 2 + (1 if name != "turn_front" else 0), hy - 2, hx + 2, hy + 2], fill=CREAM)
    return im

def label(im: Image.Image, text: str) -> Image.Image:
    out = Image.new("RGBA", (im.width, im.height + 28), "#C7D0E0")
    out.paste(im, (0, 0))
    ImageDraw.Draw(out).text((6, im.height + 6), text, fill=INK, font=ImageFont.load_default())
    return out

def x8(im): return im.resize((im.width * 8, im.height * 8), Image.NEAREST)

tiles = [label(x8(pose(p)), f"{i+1:02d} {p}") for i, p in enumerate(POSES)]
sheet = Image.new("RGBA", (256 * 6, tiles[0].height * 2), "#C7D0E0")
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % 6) * 256, (i // 6) * t.height))
sheet.save(OUT / "blockout-poses-x8.png")

sil = Image.new("RGBA", (32 * 12 + 11 * 4, 32), "#C7D0E0")
for i, p in enumerate(POSES):
    sil.paste(pose(p, silhouette=True), (i * 36, 0), pose(p, silhouette=True))
Image.Image.resize(sil, (sil.width * 3, sil.height * 3), Image.NEAREST).save(OUT / "silhouette-32.png")
sil.save(OUT / "silhouette-32-actual-size.png")

ov = x8(pose("idle"))
d = ImageDraw.Draw(ov)
d.rectangle([0, 0, 255, 255], outline="#00FF99", width=2)
d.ellipse([(16 - 10) * 8, (20 - 10) * 8, (16 + 10) * 8, (20 + 10) * 8], outline="#FF3366", width=4)
d.line([16 * 8, 0, 16 * 8, 255], fill="#FF3366", width=1)
d.line([0, 20 * 8, 255, 20 * 8], fill="#FF3366", width=1)
ov.save(OUT / "collision-overlay-x8.png")

pal = Image.new("RGB", (5 * 120, 120))
for i, col in enumerate([GOLD, CREAM, NAVY, BROWN, INK]):
    ImageDraw.Draw(pal).rectangle([i * 120, 0, i * 120 + 119, 119], fill=col)
pal.save(OUT / "palette.png")
print("wrote blockout, silhouettes, collision overlay, palette")
```

- [ ] **Step 2: Run it and look at the silhouettes at actual size**

Run: `python3 design/character/make_blockout.py && open design/character/silhouette-32.png design/character/blockout-poses-x8.png`
Expected: 12 distinct black silhouettes; every pose distinguishable without colour. If two poses read the same, change their `SPEC` entry and rerun before committing.

- [ ] **Step 3: Write `CHARACTER-SHEET.md`** with these sections, each embedding the relevant image:

1. Identity: the Lamp-Head Courier; what is carried over from A1 (lamp housing, narrow torso, satchel counterweight, light wedge).
2. **Silhouette test at game size** (`silhouette-32-actual-size.png` and ×3): rule — every pose must be identifiable in black at 32 px; which pairs are the riskiest (walk_contact vs walk_passing; levelup vs victory) and how they differ (leg spread; arm height + glow size).
3. **Facing:** art is authored facing **right**; left is `flip_h` (a mirror, not a new pose); facing follows horizontal input with a 0.1 dead-zone, vertical-only input keeps the last facing. turn_front/turn_back exist for the sheet and title only.
4. **Pose table (12):** pose → game state → trigger → duration: turn_front/side/back → reference; idle → still in PLAYING; walk_contact/walk_passing → moving, alternate every 8 ticks; cast → 8 ticks after each beam shot / 12 after a Sunflare pulse; hurt → first 12 ticks of i-frames; levelup → LEVELUP state; sunflare → 60 ticks after evolving; defeat → LOST; victory → WON.
5. **Collision overlay** (`collision-overlay-x8.png`): circle r = 10 at frame pixel (16, 20); the glow and lamp top are outside the hurtbox on purpose (pillar "light is power": the light never makes you easier to hit).
6. **Palette** (`palette.png`): the 5 hex values with roles.
7. **Consistency rules (every frame):** 32×32, transparent background, binary alpha; only the 5 palette colours; feet on row 31 (except defeat); lamp diameter 11–13 px; torso centre within ±1 px of (16, 20) except hurt/defeat; satchel always on the trailing (left, for right-facing) side; 1-px ink outline on every outer edge; lamp lens faces the travel direction.
8. `## Revisions` (empty heading, filled after generation with sheet-vs-game comparisons).

- [ ] **Step 4: Commit**

```bash
git add design/character CHARACTER-SHEET.md && git commit -m "Add character sheet with 32-px blockout, silhouettes and collision overlay (pre-generation)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: `CHANGE-BRIEF.md`

**Files:** Create `CHANGE-BRIEF.md`

- [ ] **Step 1: Write `CHANGE-BRIEF.md`** with these sections:

1. Record-discipline note (as in A1): predictions frozen at `design-v1`; corrections only under `## Revisions`.
2. **Asset list** — one row per ID (IDs must appear exactly like this; `audit_repo.py` parses them):

| Asset ID | What | Game file | Size | Panels |
|---|---|---|---|---|
| ART-PC-01 | Courier 12-pose sheet | `godot/assets/art/pc_sheet.png` | 384×32 | P1–P9 |
| ART-EN-01 | Moth, 2 frames | `godot/assets/art/enemy_moth.png` | 48×24 | P2, P3, P6 |
| ART-EN-02 | Fog wraith, 2 frames | `godot/assets/art/enemy_wraith.png` | 80×40 | P5 |
| ART-ENV-01 | Cobblestone ground tile (seamless) | `godot/assets/art/env_ground_tile.png` | 64×64 | P2, P3, P8 |
| ART-ENV-02 | Lantern market stall prop | `godot/assets/art/env_stall.png` | 64×48 | P1, P2 |
| ART-FX-01 | Beam bolt | `godot/assets/art/fx_beam.png` | 16×8 | P3 |
| ART-FX-02 | Orbiting lamp-moth | `godot/assets/art/fx_orbit_moth.png` | 12×12 | P4, P6 |
| ART-FX-03 | Sunflare burst | `godot/assets/art/fx_sunflare.png` | 128×128 | P6 |
| ART-PK-01 | Lamp-oil gem | `godot/assets/art/pickup_gem.png` | 12×12 | P3 |
| SFX-01 | Enemy killed | `godot/assets/sfx/sfx_01_kill.wav` | ≤ 0.35 s | P3 |
| SFX-02 | Gem collected | `godot/assets/sfx/sfx_02_pickup.wav` | ≤ 0.3 s | P3 |
| SFX-03 | Player hurt | `godot/assets/sfx/sfx_03_hurt.wav` | ≤ 0.5 s | P5 |
| SFX-04 | Level up | `godot/assets/sfx/sfx_04_levelup.wav` | ≤ 1.2 s | P4 |
| SFX-05 | Sunflare evolution | `godot/assets/sfx/sfx_05_evolve.wav` | ≤ 2.5 s | P6 |
| SFX-06a | Lose stinger | `godot/assets/sfx/sfx_06a_lose.wav` | ≤ 3 s | P7 |
| SFX-06b | Win stinger | `godot/assets/sfx/sfx_06b_win.wav` | ≤ 4 s | P9 |
| MUS-01 | Night-market loop | `godot/assets/music/mus_01_night_market.ogg` | 30–40 s loop | P2–P8 |
| MUS-02 | Sunflare layer (same length/BPM) | `godot/assets/music/mus_02_sunflare_layer.ogg` | = MUS-01 | P6 |

3. **Event → sound table** (event source signal, SFX, gate rule): `enemy_killed` → SFX-01 (cooldown 60 ms, ≤ 3 voices, pitch ±5 %); `gem_collected` → SFX-02 (80 ms merge window, 1 voice); `player_hurt` → SFX-03 (only when damage is applied = once per i-frame window; gate cooldown 800 ms as a second guard); `leveled_up` → SFX-04 (per level); `evolved` → SFX-05 (once per run); state → LOST → SFX-06a; state → WON → SFX-06b.
4. **How repeats are prevented:** sounds subscribe to *state-change* signals only, never to input; `is_action_pressed` ignores echo; the gate uses the simulation clock (ticks → ms) so a paused game cannot accumulate queued sounds; voice accounting is logical (fixed 300 ms per voice), independent of the audio device.
5. **Music behaviour table:** menu silent; run start → MUS-01 + MUS-02 start together at sample 0, MUS-02 at −80 dB; pause → Music bus low-pass 900 Hz + −10 dB, keeps playing; level-up → −6 dB; resume → 0 dB, filter off; evolve → MUS-02 to 0 dB over 2 s; lose → both fade to −80 dB over 0.5 s, stop, SFX-06a; win → 1.0 s fade, SFX-06b; restart → kill fades, start from 0.
6. **Mute:** M master, 9 music, 0 SFX; HUD shows state; logic unaffected.
7. **Predicted problems and how each will be verified** (≥ 3; keep all five):
   1. Kill SFX machine-guns in dense waves → `test_audio.gd` burst check (20 kills same tick → 1 play) + long-run spacing check + listening at 2:30.
   2. Generated poses drift after downscale (lamp size, facing, satchel side) → `palette_check.py`, silhouette strip at 32 px, sheet-vs-game screenshots.
   3. MusicGen output does not loop cleanly or drifts in tempo → `loop_check.py` (wrap jump ≤ p99 sample delta; head/tail RMS ≥ 25 % of mean) + 5 manual loop listens.
   4. Cool fog palette makes enemies unreadable against the ground when muted → luminance contrast check between enemy and ground mean (≥ 0.25 relative), muted playtest.
   5. MUS-02 drifts against MUS-01 → equal frame count check + listen at 0:10/0:25 after evolve; fallback: drop MUS-02 and brighten via a filter change (record as a Revision).
8. `## Revisions`

- [ ] **Step 2: Commit**

```bash
git add CHANGE-BRIEF.md && git commit -m "Add CHANGE-BRIEF v1: asset list, event-sound map, music behaviour, predictions

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 6: HUMAN GATE — design review, tag `design-v1`, GitHub

- [ ] **Step 1: Ask Bao to read CONCEPT, STORYBOARD, CHARACTER-SHEET, CHANGE-BRIEF.** Apply requested edits (still pre-tag, so direct edits are fine), commit each.
- [ ] **Step 2: Ask Bao whether to add hand-drawn storyboard photos now** (optional; place in `design/storyboard/hand/` and link under each panel).
- [ ] **Step 3: Tag**

```bash
git tag -a design-v1 -m "Design package frozen before first generation"
git log -1 --format='%H %cI' design-v1
```

- [ ] **Step 4: Ask Bao for permission and visibility (public/private) before creating the remote.** On yes:

```bash
gh repo create yanxlh/walker-lanternfall-bao-x --<public|private> --source . --push
git push origin design-v1
```

Expected: remote shows the tag; its timestamp is the "design before generation" proof.

---

# Phase B — Greybox game (placeholders only, no generation)

All tests run with:

```bash
cd godot && $GODOT --headless --path . --import --quit && $GODOT --headless --path . --script res://tests/<suite>.gd
```

### Task 7: Tuning, GameState, test harness

**Files:**
- Create: `godot/features/tuning.gd`, `godot/game/game_state.gd`, `godot/tests/harness.gd`, `godot/tests/test_logic.gd`

**Interfaces:**
- Produces: `GameState` constants `MENU, PLAYING, LEVELUP, PAUSED, WON, LOST`, `NAMES`, `current`, `go(to) -> bool`, `restart() -> bool`, `is_terminal() -> bool`, signal `changed(from: int, to: int)`.
- Produces: harness `check(id, passed, observed)`, `suite`, `run()`; writes `evidence/<suite>.json`.

- [ ] **Step 1: Write `godot/features/tuning.gd`**

```gdscript
extends RefCounted
## Every gameplay number lives here.

const TICK_HZ := 60
const RUN_SECONDS := 180
const ARENA := Rect2(-960, -540, 1920, 1080)

const PLAYER_SPEED := 90.0
const SPEED_PER_LEVEL := 15.0
const PLAYER_RADIUS := 10.0
const PLAYER_MAX_HP := 10
const HP_PER_LEVEL := 4
const HEAL_AMOUNT := 3
const IFRAME_TICKS := 48
const HURT_POSE_TICKS := 12
const KNOCKBACK := 160.0
const KNOCKBACK_DECAY := 900.0
const FACING_DEADZONE := 0.1

const PICKUP_RADIUS := 28.0
const PICKUP_RADIUS_PER_LEVEL := 20.0
const COLLECT_RADIUS := 8.0
const GEM_PULL_SPEED := 260.0
const XP_TO_LEVEL := [3, 5, 7, 9, 12, 15, 18, 22, 26, 30, 35, 40]

const BEAM_SPEED := 320.0
const BEAM_LIFE_TICKS := 60
const BEAM_RADIUS := 4.0
const BEAM_DAMAGE := 2
const BEAM_BASE_COOLDOWN := 40
const BEAM_RATE_FACTOR := 0.75
const CAST_POSE_TICKS := 8

const MOTH_SPIN := 3.2
const MOTH_BASE_RADIUS := 36.0
const MOTH_RADIUS_STEP := 14.0
const MOTH_HIT_RADIUS := 5.0
const MOTH_DAMAGE := 1
const MOTH_HIT_COOLDOWN := 20

const SUNFLARE_PERIOD := 120
const SUNFLARE_FIRST_DELAY := 30
const SUNFLARE_RADIUS := 240.0
const SUNFLARE_DAMAGE := 6
const SUNFLARE_RING_TICKS := 24
const EVOLVE_POSE_TICKS := 60
const BANNER_TICKS := 120

const SPAWN_DISTANCE := 400.0
const MAX_ENEMIES := 220
const ENEMIES := {
	"moth": {"hp": 2, "speed": 55.0, "radius": 6.0, "damage": 1, "xp": 1, "frame": 24},
	"wraith": {"hp": 8, "speed": 32.0, "radius": 14.0, "damage": 2, "xp": 3, "frame": 40},
}
const SPAWN_TABLE := [
	{"until_s": 30, "interval_ticks": 60, "batch": 1, "wraith_chance": 0.0},
	{"until_s": 60, "interval_ticks": 45, "batch": 2, "wraith_chance": 0.1},
	{"until_s": 90, "interval_ticks": 36, "batch": 2, "wraith_chance": 0.2},
	{"until_s": 120, "interval_ticks": 30, "batch": 3, "wraith_chance": 0.25},
	{"until_s": 150, "interval_ticks": 24, "batch": 3, "wraith_chance": 0.3},
	{"until_s": 9999, "interval_ticks": 20, "batch": 4, "wraith_chance": 0.35},
]
```

- [ ] **Step 2: Write `godot/tests/harness.gd`**

```gdscript
extends SceneTree
## Shared headless test harness. Subclasses set `suite` and override run().

var suite := "unnamed"
var results: Array[Dictionary] = []
var failures := 0

func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	await run()
	var out_dir := ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var path := "%s/%s.json" % [out_dir, suite]
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify({
		"suite": suite,
		"engine": Engine.get_version_info().string,
		"utc": Time.get_datetime_string_from_system(true),
		"checks": results.size(),
		"failures": failures,
		"results": results,
	}, "  "))
	f.close()
	print("%s: %d checks, %d failures -> %s" % [suite, results.size(), failures, path])
	quit(1 if failures else 0)

func run() -> void:
	pass

func check(id: String, passed: bool, observed: Dictionary = {}) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(("PASS " if passed else "FAIL ") + id + " " + JSON.stringify(observed))
```

- [ ] **Step 3: Write the failing GameState tests in `godot/tests/test_logic.gd`**

```gdscript
extends "res://tests/harness.gd"
const GS = preload("res://game/game_state.gd")

func run() -> void:
	suite = "logic"
	_state_tests()

func _state_tests() -> void:
	var s = GS.new()
	var changes: Array = []
	s.changed.connect(func(f, t): changes.append([f, t]))
	check("state-menu-rejects-won", not s.go(GS.WON) and s.current == GS.MENU)
	check("state-menu-to-playing", s.go(GS.PLAYING) and s.current == GS.PLAYING)
	check("state-levelup-roundtrip", s.go(GS.LEVELUP) and s.go(GS.PLAYING))
	check("state-pause-roundtrip", s.go(GS.PAUSED) and not s.go(GS.LEVELUP) and s.go(GS.PLAYING))
	s.go(GS.LOST)
	check("state-terminal-is-sticky", not s.go(GS.PLAYING) and not s.go(GS.WON) and s.is_terminal())
	check("state-restart-from-terminal", s.restart() and s.current == GS.PLAYING)
	check("state-signal-log", changes.size() == 7 and changes[-1] == [GS.LOST, GS.PLAYING], {"changes": changes})
	var m = GS.new()
	check("state-restart-not-from-menu", not m.restart())
```

- [ ] **Step 4: Run to verify it fails**

Run: `$GODOT --headless --path . --script res://tests/test_logic.gd`
Expected: parse error — `res://game/game_state.gd` not found.

- [ ] **Step 5: Write `godot/game/game_state.gd`**

```gdscript
extends RefCounted
## Single source of truth for run state.

signal changed(from: int, to: int)

enum { MENU, PLAYING, LEVELUP, PAUSED, WON, LOST }
const NAMES := ["menu", "playing", "levelup", "paused", "won", "lost"]
const ALLOWED := {
	MENU: [PLAYING],
	PLAYING: [LEVELUP, PAUSED, WON, LOST],
	LEVELUP: [PLAYING],
	PAUSED: [PLAYING],
	WON: [],
	LOST: [],
}

var current: int = MENU

func go(to: int) -> bool:
	if not (to in ALLOWED[current]):
		return false
	var from := current
	current = to
	changed.emit(from, to)
	return true

## Any non-menu state may restart into a fresh PLAYING run.
func restart() -> bool:
	if current == MENU:
		return false
	var from := current
	current = PLAYING
	changed.emit(from, PLAYING)
	return true

func is_terminal() -> bool:
	return current == WON or current == LOST
```

- [ ] **Step 6: Run to verify it passes**

Run: `$GODOT --headless --path . --script res://tests/test_logic.gd`
Expected: `logic: 8 checks, 0 failures`.

- [ ] **Step 7: Commit**

```bash
git add godot/features/tuning.gd godot/game/game_state.gd godot/tests evidence/logic.json
git commit -m "Add tuning, GameState machine and headless harness

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 8: Progression — XP, branching cards, Sunflare evolution

**Files:**
- Create: `godot/features/progression/progression.gd`
- Modify: `godot/tests/test_logic.gd`

**Interfaces:**
- Consumes: `Tuning.XP_TO_LEVEL`, `BEAM_*`, `MOTH_*`.
- Produces: fields `xp, level, pending_levelups, beam_level, beam_pierce, beam_cooldown_ticks, moth_level, moth_count, moth_radius, passive: Dictionary{"speed","magnet","hp"}, evolved_sunflare`; `xp_needed() -> int`, `add_xp(amount: int) -> int`, `evolution_ready() -> bool`, `eligible_cards() -> Array[String]`, `offer_cards(rng) -> Array[String]` (always 3), `apply(card: String) -> void`; signal `leveled_up(level: int)`; const `CARD_TEXT: Dictionary[id -> [title, description]]`.

- [ ] **Step 1: Add failing progression tests** — in `test_logic.gd` add `const Prog = preload("res://features/progression/progression.gd")`, call `_progression_tests()` from `run()`, and append:

```gdscript
func _progression_tests() -> void:
	var p = Prog.new()
	var levels: Array = []
	p.leveled_up.connect(func(l): levels.append(l))
	var gained: int = p.add_xp(3 + 5 + 7)
	check("prog-multi-level", gained == 3 and p.level == 4 and p.pending_levelups == 3 and levels == [2, 3, 4], {"gained": gained, "levels": levels})
	var rng := RandomNumberGenerator.new()
	rng.seed = 42
	var offer: Array[String] = p.offer_cards(rng)
	var unique := {}
	for c in offer: unique[c] = true
	check("prog-offer-three-unique", offer.size() == 3 and unique.size() == 3 and not ("sunflare" in offer), {"offer": offer})
	var early: Array[String] = p.eligible_cards()
	check("prog-branches-offered", "beam_rate" in early and "beam_pierce" in early and "moth_new" in early and not ("moth_count" in early), {"eligible": early})
	p.apply("beam_rate")
	check("prog-beam-rate", p.beam_level == 2 and p.beam_cooldown_ticks == 30, {"cooldown": p.beam_cooldown_ticks})
	p.apply("beam_pierce")
	p.apply("moth_new")
	p.apply("moth_count")
	check("prog-not-ready-at-moth-2", not p.evolution_ready() and not ("sunflare" in p.offer_cards(rng)))
	p.apply("moth_radius")
	check("prog-maxed-weapons", p.beam_level == 3 and p.moth_level == 3 and p.moth_count == 3 and p.beam_pierce == 2)
	var evo: Array[String] = p.offer_cards(rng)
	check("prog-sunflare-offered-first", p.evolution_ready() and evo[0] == "sunflare" and evo.size() == 3, {"offer": evo})
	p.apply("sunflare")
	var after: Array[String] = p.eligible_cards()
	check("prog-after-evolve-no-weapon-cards", p.evolved_sunflare and not p.evolution_ready() and not ("beam_rate" in after) and not ("moth_count" in after), {"eligible": after})
	for k in ["pass_speed", "pass_speed", "pass_magnet", "pass_magnet", "pass_hp", "pass_hp"]:
		p.apply(k)
	check("prog-exhausted-pool-pads-heal", p.offer_cards(rng) == ["heal", "heal", "heal"])
	var a = Prog.new(); var b = Prog.new()
	var r1 := RandomNumberGenerator.new(); r1.seed = 7
	var r2 := RandomNumberGenerator.new(); r2.seed = 7
	check("prog-deterministic", a.offer_cards(r1) == b.offer_cards(r2))
```

- [ ] **Step 2: Run to verify it fails**

Run: `$GODOT --headless --path . --script res://tests/test_logic.gd`
Expected: parse error — progression.gd not found.

- [ ] **Step 3: Write `godot/features/progression/progression.gd`**

```gdscript
extends RefCounted
## XP, level-up card offers, weapon/passive levels and the Sunflare evolution.

const Tuning = preload("res://features/tuning.gd")

signal leveled_up(level: int)

const WEAPON_MAX := 3
const PASSIVE_MAX := 2
const CARD_TEXT := {
	"beam_rate": ["Beam: Quick Wick", "Beam fires 25% faster"],
	"beam_pierce": ["Beam: Long Wick", "Beam passes through one more enemy"],
	"moth_new": ["Lamp-Moths", "Two moths circle you and burn what they touch"],
	"moth_count": ["Moths: Another Wing", "One more orbiting moth"],
	"moth_radius": ["Moths: Wider Flight", "Moths circle further out"],
	"pass_speed": ["Light Boots", "Move 15 px/s faster"],
	"pass_magnet": ["Magnet Satchel", "Collect oil from further away"],
	"pass_hp": ["Thick Glass", "+4 max HP, healed now"],
	"heal": ["Trim the Wick", "Restore 3 HP"],
	"sunflare": ["SUNFLARE LIGHTHOUSE", "Beam and moths fuse into a pulsing burst of light"],
}

var xp := 0
var level := 1
var pending_levelups := 0
var beam_level := 1
var beam_pierce := 1
var beam_cooldown_ticks: int = Tuning.BEAM_BASE_COOLDOWN
var moth_level := 0
var moth_count := 0
var moth_radius: float = Tuning.MOTH_BASE_RADIUS
var passive := {"speed": 0, "magnet": 0, "hp": 0}
var evolved_sunflare := false

func xp_needed() -> int:
	var table: Array = Tuning.XP_TO_LEVEL
	return int(table[mini(level - 1, table.size() - 1)])

## Returns how many levels were gained. Each one emits leveled_up and is queued.
func add_xp(amount: int) -> int:
	xp += amount
	var gained := 0
	while xp >= xp_needed():
		xp -= xp_needed()
		level += 1
		gained += 1
		leveled_up.emit(level)
	pending_levelups += gained
	return gained

func evolution_ready() -> bool:
	return beam_level >= WEAPON_MAX and moth_level >= WEAPON_MAX and not evolved_sunflare

func eligible_cards() -> Array[String]:
	var out: Array[String] = []
	if not evolved_sunflare:
		if beam_level < WEAPON_MAX:
			out.append_array(["beam_rate", "beam_pierce"])
		if moth_level == 0:
			out.append("moth_new")
		elif moth_level < WEAPON_MAX:
			out.append_array(["moth_count", "moth_radius"])
	for k in ["speed", "magnet", "hp"]:
		if int(passive[k]) < PASSIVE_MAX:
			out.append("pass_" + k)
	return out

func offer_cards(rng: RandomNumberGenerator) -> Array[String]:
	var pool := eligible_cards()
	for i in range(pool.size() - 1, 0, -1):
		var j := rng.randi_range(0, i)
		var t := pool[i]
		pool[i] = pool[j]
		pool[j] = t
	var out: Array[String] = []
	if evolution_ready():
		out.append("sunflare")
	for c in pool:
		if out.size() >= 3:
			break
		out.append(c)
	while out.size() < 3:
		out.append("heal")
	return out

func apply(card: String) -> void:
	match card:
		"beam_rate":
			beam_level += 1
			beam_cooldown_ticks = maxi(8, roundi(beam_cooldown_ticks * Tuning.BEAM_RATE_FACTOR))
		"beam_pierce":
			beam_level += 1
			beam_pierce += 1
		"moth_new":
			moth_level = 1
			moth_count = 2
		"moth_count":
			moth_level += 1
			moth_count += 1
		"moth_radius":
			moth_level += 1
			moth_radius += Tuning.MOTH_RADIUS_STEP
		"pass_speed", "pass_magnet", "pass_hp":
			var k := card.trim_prefix("pass_")
			passive[k] = int(passive[k]) + 1
		"sunflare":
			evolved_sunflare = true
		"heal":
			pass
```

- [ ] **Step 4: Run to verify it passes**

Run: `$GODOT --headless --path . --script res://tests/test_logic.gd`
Expected: `logic: 18 checks, 0 failures`. (`roundi(40*0.75)` = 30.)

- [ ] **Step 5: Commit**

```bash
git add godot/features/progression godot/tests/test_logic.gd evidence/logic.json
git commit -m "Add progression: branching upgrade cards and Sunflare evolution

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 9: SfxGate — cooldown, voice cap, once-per-run

**Files:**
- Create: `godot/audio/sfx_gate.gd`
- Modify: `godot/tests/test_logic.gd`

**Interfaces:**
- Produces: `SfxGate.new(rules: Dictionary)`, rule keys `cooldown_ms: int`, `max_voices: int`, `once: bool`; `request(id: String, now_ms: int, active_voices: int) -> bool`; `reset() -> void`.

- [ ] **Step 1: Add failing gate tests** — `const Gate = preload("res://audio/sfx_gate.gd")`, call `_gate_tests()` from `run()`:

```gdscript
func _gate_tests() -> void:
	var g = Gate.new({"kill": {"cooldown_ms": 60, "max_voices": 3}, "evolve": {"once": true, "max_voices": 1}, "hurt": {"cooldown_ms": 800, "max_voices": 1}})
	check("gate-first-plays", g.request("kill", 0, 0))
	check("gate-cooldown-blocks", not g.request("kill", 30, 1))
	check("gate-cooldown-releases", g.request("kill", 60, 1))
	check("gate-voice-cap", not g.request("kill", 200, 3) and g.request("kill", 200, 2))
	check("gate-hurt-boundary-inclusive", g.request("hurt", 0, 0) and not g.request("hurt", 799, 0) and g.request("hurt", 800, 0))
	check("gate-once", g.request("evolve", 0, 0) and not g.request("evolve", 99999, 0))
	g.reset()
	check("gate-reset", g.request("evolve", 0, 0) and g.request("kill", 0, 0))
	check("gate-unknown-id-single-voice", g.request("mystery", 0, 0) and not g.request("mystery", 1, 1))
```

- [ ] **Step 2: Run to verify it fails**

Expected: parse error — sfx_gate.gd not found.

- [ ] **Step 3: Write `godot/audio/sfx_gate.gd`**

```gdscript
extends RefCounted
## Pure throttle for sound events: per-id cooldown, voice cap and once-per-run.
## Uses the simulation clock supplied by the caller, never wall time.

var rules: Dictionary
var _last_ms := {}
var _fired := {}

func _init(r: Dictionary) -> void:
	rules = r

func request(id: String, now_ms: int, active_voices: int) -> bool:
	var r: Dictionary = rules.get(id, {})
	var once: bool = r.get("once", false)
	if once and _fired.get(id, false):
		return false
	if _last_ms.has(id) and now_ms - int(_last_ms[id]) < int(r.get("cooldown_ms", 0)):
		return false
	if active_voices >= int(r.get("max_voices", 1)):
		return false
	_last_ms[id] = now_ms
	if once:
		_fired[id] = true
	return true

func reset() -> void:
	_last_ms.clear()
	_fired.clear()
```

- [ ] **Step 4: Run to verify it passes** — Expected: `logic: 26 checks, 0 failures`.

- [ ] **Step 5: Commit**

```bash
git add godot/audio/sfx_gate.gd godot/tests/test_logic.gd evidence/logic.json
git commit -m "Add SfxGate: cooldown, voice cap and once-per-run rules

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 10: Session simulation — player, enemies, weapons, gems, world (placeholders)

**Files:**
- Create: `godot/features/art.gd`, `godot/features/player/player.gd`, `godot/features/enemies/enemy.gd`, `godot/features/enemies/spawner.gd`, `godot/features/pickups/gem.gd`, `godot/features/weapons/beam_shot.gd`, `godot/features/weapons/weapon_fx.gd`, `godot/features/world/ground.gd`, `godot/tests/test_gameplay.gd`
- Replace: `godot/game/session.gd`
- Temporarily stub: `godot/audio/audio_bus.gd` and `godot/ui/hud.gd` (real ones in Tasks 11–12)

**Interfaces:**
- Consumes: GameState, Progression, Tuning.
- Produces (session): signals `run_started`, `enemy_killed(pos: Vector2)`, `gem_collected(value: int)`, `player_hurt(hp: int)`, `leveled_up(level: int)`, `evolved`; fields `state, prog, player, enemies: Array, gems: Array, shots: Array, offered: Array[String], tick_count: int, kills: int, banner_ticks: int, sunflare_ring: int, audio, hud, test_mode, test_axis: Vector2, test_no_spawn`; methods `start_run(seed_value := -1)`, `tick()`, `step_ticks(n)`, `choose_card(index) -> bool`, `toggle_pause()`, `spawn_enemy(kind, pos) -> Node2D`, `drop_gem(pos, value) -> Node2D`, `damage(e, amount)`, `orbit_positions() -> Array[Vector2]`.
- Produces (player): const `POSES` (canonical order), fields `hp, max_hp, speed, facing, iframes, input_axis, pose, override_pose, cast_ticks, empowered, show_collision, sheet`; `reset()`, `step()`, `take_hit(from: Vector2, dmg: int) -> bool`; signals `damaged(hp)`, `died`.
- Produces (art): `Art.texture(path) -> Texture2D or null`, static `Art.disabled`, path consts `PC_SHEET, MOTH, WRAITH, GROUND, STALL, BEAM, ORBIT_MOTH, SUNFLARE, GEM`.

- [ ] **Step 1: Write stubs so session compiles**

`godot/audio/audio_bus.gd`:
```gdscript
extends Node
func setup(_s) -> void:
	pass
func toggle_bus(_name: String) -> void:
	pass
```
`godot/ui/hud.gd`:
```gdscript
extends CanvasLayer
var card_cursor := 0
func setup(_s) -> void:
	pass
func move_card(_d: int) -> void:
	pass
```

- [ ] **Step 2: Write the failing gameplay tests `godot/tests/test_gameplay.gd`**

```gdscript
extends "res://tests/harness.gd"
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")
var game

func fresh(seed_value: int = 1, no_spawn: bool = true) -> void:
	if is_instance_valid(game):
		game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = no_spawn
	root.add_child(game)
	game.start_run(seed_value)

func run() -> void:
	suite = "gameplay"
	await fresh()
	check("run-starts-playing", game.state.current == GS.PLAYING and game.tick_count == 0 and game.player.hp == Tuning.PLAYER_MAX_HP)
	game.test_axis = Vector2.RIGHT
	game.step_ticks(60)
	check("move-speed", absf(game.player.position.x - 90.0) < 0.5, {"x": game.player.position.x})
	check("walk-pose", game.player.pose in ["walk_contact", "walk_passing", "cast"], {"pose": game.player.pose})
	await fresh()
	game.test_axis = Vector2(1, 1)
	game.step_ticks(60)
	check("diagonal-normalized", absf(game.player.position.length() - 90.0) < 0.5, {"dist": game.player.position.length()})
	game.test_axis = Vector2(-1, 0)
	game.step_ticks(1)
	check("facing-left", game.player.facing == -1)
	game.test_axis = Vector2(0.08, 1)
	game.step_ticks(5)
	check("facing-deadzone", game.player.facing == -1)
	game.test_axis = Vector2.ZERO
	game.step_ticks(20)
	check("idle-pose", game.player.pose in ["idle", "cast"], {"pose": game.player.pose})
	game.test_axis = Vector2.LEFT
	game.step_ticks(1200)
	check("arena-clamp", game.player.position.x >= Tuning.ARENA.position.x, {"x": game.player.position.x})

	await fresh()
	game.spawn_enemy("moth", Vector2(80, 0))
	var kills := [0]
	game.enemy_killed.connect(func(_p): kills[0] += 1)
	game.step_ticks(2)
	check("cast-pose-on-fire", game.player.pose == "cast", {"pose": game.player.pose})
	game.step_ticks(38)
	check("beam-kills-moth", kills[0] == 1 and game.gems.size() == 1 and game.enemies.is_empty(), {"kills": kills[0], "gems": game.gems.size()})
	var picked := [0]
	game.gem_collected.connect(func(_v): picked[0] += 1)
	game.test_axis = Vector2.RIGHT
	game.step_ticks(60)
	check("gem-flies-and-collects", picked[0] == 1 and game.prog.xp == 1 and game.gems.is_empty(), {"xp": game.prog.xp})

	await fresh()
	game.prog.add_xp(3)
	game.tick()
	check("levelup-opens", game.state.current == GS.LEVELUP and game.offered.size() == 3 and game.player.pose == "levelup", {"offered": game.offered})
	var frozen: int = game.tick_count
	game.step_ticks(30)
	check("levelup-freezes-sim", game.tick_count == frozen)
	check("choose-card", game.choose_card(0) and game.state.current == GS.PLAYING and game.prog.pending_levelups == 0)
	check("choose-card-rejected-when-playing", not game.choose_card(0))

	await fresh()
	game.prog.add_xp(3 + 5 + 7)
	var opens := 0
	for i in 10:
		game.tick()
		if game.state.current == GS.LEVELUP:
			opens += 1
			game.choose_card(0)
	check("levelup-queue", opens == 3 and game.prog.pending_levelups == 0, {"opens": opens})

	await fresh()
	game.toggle_pause()
	game.prog.add_xp(3)
	game.step_ticks(10)
	check("levelup-while-paused", game.state.current == GS.PAUSED)
	game.toggle_pause()
	game.tick()
	check("levelup-after-unpause", game.state.current == GS.LEVELUP)

	await fresh()
	var hurts: Array = []
	game.player_hurt.connect(func(_hp): hurts.append(game.tick_count))
	var w = game.spawn_enemy("wraith", Vector2.ZERO)
	w.hp = 9999
	for i in 150:
		w.position = game.player.position
		game.tick()
	var spaced := true
	for i in range(1, hurts.size()):
		spaced = spaced and hurts[i] - hurts[i - 1] >= Tuning.IFRAME_TICKS
	check("hurt-iframes", hurts.size() == 4 and spaced, {"hurt_ticks": hurts})
	check("hurt-knockback-and-hp", game.player.hp == Tuning.PLAYER_MAX_HP - 8)

	await fresh()
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.tick()
	check("death-lost", game.state.current == GS.LOST and game.player.pose == "defeat")
	var t_end: int = game.tick_count
	game.step_ticks(10)
	check("lost-freezes-sim", game.tick_count == t_end)

	await fresh()
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	check("won-at-3min", game.state.current == GS.WON and game.player.pose == "victory")

	await fresh()
	var terminal := [0]
	game.state.changed.connect(func(_f, t):
		if t == GS.WON or t == GS.LOST:
			terminal[0] += 1)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.player.hp = 1
	var w3 = game.spawn_enemy("wraith", game.player.position)
	w3.hp = 9999
	game.tick()
	check("death-and-timer-same-tick", terminal[0] == 1 and game.state.current == GS.LOST)

	await fresh()
	var evo := [0]
	game.evolved.connect(func(): evo[0] += 1)
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	check("sunflare-offered", game.offered[0] == "sunflare", {"offered": game.offered})
	game.choose_card(0)
	var ring = game.spawn_enemy("moth", Vector2(200, 0))
	game.step_ticks(Tuning.SUNFLARE_FIRST_DELAY + 1)
	check("sunflare-evolves-once", evo[0] == 1 and game.orbit_positions().is_empty() and game.shots.is_empty() and game.player.empowered)
	check("sunflare-burst-kills", game.enemies.is_empty() and game.banner_ticks > 0)

	await fresh(5, false)
	game.player.hp = 1
	game.step_ticks(20000)
	var lost_first: bool = game.state.is_terminal()
	game.start_run(5)
	check("restart-resets", lost_first and game.state.current == GS.PLAYING and game.tick_count == 0 and game.enemies.is_empty() and game.gems.is_empty() and game.player.hp == Tuning.PLAYER_MAX_HP and game.prog.level == 1)

	Art.disabled = true
	await fresh(9, false)
	game.test_axis = Vector2(1, 0.3)
	for i in 600:
		if game.state.current == GS.LEVELUP:
			game.choose_card(0)
		game.tick()
	check("missing-art-no-crash", game.tick_count > 0 and game.player.sheet == null)
	Art.disabled = false

	await fresh(3, false)
	var chosen: Array = []
	for t in Tuning.RUN_SECONDS * Tuning.TICK_HZ + 10:
		if game.state.is_terminal():
			break
		if game.state.current == GS.LEVELUP:
			chosen.append(game.offered[0])
			game.choose_card(0)
		var a := float(t) / 90.0
		game.test_axis = Vector2(cos(a), sin(a))
		game.tick()
	check("long-run-smoke", game.state.is_terminal(), {"state": GS.NAMES[game.state.current], "seconds": game.tick_count / 60, "kills": game.kills, "level": game.prog.level, "cards": chosen})
```

- [ ] **Step 3: Run to verify it fails**

Run: `$GODOT --headless --path . --script res://tests/test_gameplay.gd`
Expected: errors — `start_run` not found / missing preload files.

- [ ] **Step 4: Write `godot/features/art.gd`**

```gdscript
extends RefCounted
## Loads generated art if it exists; returns null so every drawer can fall back to a placeholder.

const PC_SHEET := "res://assets/art/pc_sheet.png"
const MOTH := "res://assets/art/enemy_moth.png"
const WRAITH := "res://assets/art/enemy_wraith.png"
const GROUND := "res://assets/art/env_ground_tile.png"
const STALL := "res://assets/art/env_stall.png"
const BEAM := "res://assets/art/fx_beam.png"
const ORBIT_MOTH := "res://assets/art/fx_orbit_moth.png"
const SUNFLARE := "res://assets/art/fx_sunflare.png"
const GEM := "res://assets/art/pickup_gem.png"

static var disabled := false

static func texture(path: String) -> Texture2D:
	if disabled or not ResourceLoader.exists(path):
		return null
	return load(path)
```

- [ ] **Step 5: Write `godot/features/player/player.gd`**

```gdscript
extends Node2D
## The Lamp-Head Courier. Movement, facing, i-frames and pose selection; the session calls step() once per tick.

const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

signal damaged(hp: int)
signal died

const POSES := ["turn_front", "turn_side", "turn_back", "idle", "walk_contact", "walk_passing",
	"cast", "hurt", "levelup", "sunflare", "defeat", "victory"]
const FRAME := 32
const WALK_FRAME_TICKS := 8

var sheet: Texture2D
var hp: int = Tuning.PLAYER_MAX_HP
var max_hp: int = Tuning.PLAYER_MAX_HP
var speed: float = Tuning.PLAYER_SPEED
var facing := 1
var iframes := 0
var knock := Vector2.ZERO
var input_axis := Vector2.ZERO
var pose := "idle"
var override_pose := ""
var walk_ticks := 0
var cast_ticks := 0
var empowered := false
var show_collision := false

func _ready() -> void:
	z_index = 2
	sheet = Art.texture(Art.PC_SHEET)

func reset() -> void:
	hp = Tuning.PLAYER_MAX_HP
	max_hp = Tuning.PLAYER_MAX_HP
	speed = Tuning.PLAYER_SPEED
	facing = 1
	iframes = 0
	knock = Vector2.ZERO
	input_axis = Vector2.ZERO
	override_pose = ""
	walk_ticks = 0
	cast_ticks = 0
	empowered = false
	position = Vector2.ZERO
	sheet = Art.texture(Art.PC_SHEET)
	pose = "idle"
	queue_redraw()

func step() -> void:
	var axis := input_axis.limit_length(1.0)
	position += (axis * speed + knock) / Tuning.TICK_HZ
	knock = knock.move_toward(Vector2.ZERO, Tuning.KNOCKBACK_DECAY / Tuning.TICK_HZ)
	var margin := Vector2(16, 16)
	position = position.clamp(Tuning.ARENA.position + margin, Tuning.ARENA.end - margin)
	if axis.x > Tuning.FACING_DEADZONE:
		facing = 1
	elif axis.x < -Tuning.FACING_DEADZONE:
		facing = -1
	if iframes > 0:
		iframes -= 1
	if cast_ticks > 0:
		cast_ticks -= 1
	walk_ticks = walk_ticks + 1 if axis.length() > 0.1 else 0
	pose = choose_pose()
	var flashing := iframes > 0 and (iframes / 4) % 2 == 0
	modulate = Color(1, 0.45, 0.45) if flashing else (Color(1.25, 1.12, 0.85) if empowered else Color.WHITE)
	queue_redraw()

func choose_pose() -> String:
	if override_pose != "":
		return override_pose
	if iframes > Tuning.IFRAME_TICKS - Tuning.HURT_POSE_TICKS:
		return "hurt"
	if cast_ticks > 0:
		return "cast"
	if walk_ticks > 0:
		return "walk_contact" if (walk_ticks / WALK_FRAME_TICKS) % 2 == 0 else "walk_passing"
	return "idle"

func set_override(p: String) -> void:
	override_pose = p
	pose = choose_pose()
	queue_redraw()

func take_hit(from: Vector2, dmg: int) -> bool:
	if iframes > 0 or hp <= 0:
		return false
	hp = maxi(0, hp - dmg)
	iframes = Tuning.IFRAME_TICKS
	var away := position - from
	knock = (away.normalized() if away.length() > 0.01 else Vector2(-facing, 0)) * Tuning.KNOCKBACK
	damaged.emit(hp)
	if hp == 0:
		died.emit()
	return true

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(facing, 1))
	if sheet:
		var i := POSES.find(pose)
		draw_texture_rect_region(sheet, Rect2(-16, -20, FRAME, FRAME), Rect2(i * FRAME, 0, FRAME, FRAME))
	else:
		_draw_placeholder()
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	if show_collision:
		draw_arc(Vector2.ZERO, Tuning.PLAYER_RADIUS, 0, TAU, 24, Color(0, 1, 0.6), 1.0)

func _draw_placeholder() -> void:
	var ink := Color("#14121C")
	var tilt := {"hurt": -0.35, "defeat": 1.4}.get(pose, 0.0) as float
	draw_set_transform(Vector2.ZERO, tilt, Vector2(facing, 1))
	draw_rect(Rect2(-5, -6, 10, 12), Color("#2E3A59"))
	draw_rect(Rect2(-9, -2, 4, 5), Color("#8A5A3C"))
	draw_circle(Vector2(0, -12), 6, Color("#F2B84B"))
	draw_arc(Vector2(0, -12), 6, 0, TAU, 16, ink, 1.0)
	var stride := 2.0 if pose == "walk_contact" else (-2.0 if pose == "walk_passing" else 0.0)
	draw_line(Vector2(-2, 6), Vector2(-2 - stride, 11), ink, 2.0)
	draw_line(Vector2(2, 6), Vector2(2 + stride, 11), ink, 2.0)
	if pose in ["cast", "sunflare", "levelup", "victory"]:
		draw_line(Vector2(3, -3), Vector2(9, -9), ink, 2.0)
```

- [ ] **Step 6: Write enemy, spawner, gem, beam shot, weapon fx, ground**

`godot/features/enemies/enemy.gd`:
```gdscript
extends Node2D
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var kind := "moth"
var hp := 1
var speed := 0.0
var radius := 6.0
var damage := 1
var xp := 1
var flash := 0
var dead := false
var anim := 0
var frame := 24
var tex: Texture2D
var flip := false

func setup(k: String, at: Vector2) -> void:
	kind = k
	position = at
	var d: Dictionary = Tuning.ENEMIES[k]
	hp = d["hp"]; speed = d["speed"]; radius = d["radius"]; damage = d["damage"]; xp = d["xp"]; frame = d["frame"]
	tex = Art.texture(Art.MOTH if k == "moth" else Art.WRAITH)

func step(target: Vector2) -> void:
	var to := target - position
	if to.length() > 0.5:
		position += to.normalized() * speed / Tuning.TICK_HZ
	flip = to.x < 0
	anim += 1
	if flash > 0:
		flash -= 1
	modulate = Color(2.5, 2.5, 2.5) if flash > 0 else Color.WHITE
	queue_redraw()

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(-1 if flip else 1, 1))
	if tex:
		var f := (anim / 10) % 2
		draw_texture_rect_region(tex, Rect2(-frame / 2.0, -frame / 2.0, frame, frame), Rect2(f * frame, 0, frame, frame))
	else:
		draw_circle(Vector2.ZERO, radius, Color("#C7D0E0") if kind == "moth" else Color("#3B4A6B"))
		draw_arc(Vector2.ZERO, radius, 0, TAU, 16, Color("#14121C"), 1.0)
```

`godot/features/enemies/spawner.gd`:
```gdscript
extends RefCounted
const Tuning = preload("res://features/tuning.gd")

## Returns [{kind, angle}] to spawn this tick, driven only by the seeded rng.
func step(tick: int, rng: RandomNumberGenerator) -> Array:
	var sec := tick / Tuning.TICK_HZ
	var phase: Dictionary = Tuning.SPAWN_TABLE[-1]
	for p in Tuning.SPAWN_TABLE:
		if sec < int(p["until_s"]):
			phase = p
			break
	if tick % int(phase["interval_ticks"]) != 0:
		return []
	var out := []
	for i in int(phase["batch"]):
		var kind := "wraith" if rng.randf() < float(phase["wraith_chance"]) else "moth"
		out.append({"kind": kind, "angle": rng.randf() * TAU})
	return out
```

`godot/features/pickups/gem.gd`:
```gdscript
extends Node2D
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var value := 1
var pulled := false
var tex: Texture2D

func setup(at: Vector2, v: int) -> void:
	position = at
	value = v
	tex = Art.texture(Art.GEM)

## True when collected this tick. Once inside the magnet it keeps flying to the courier.
func step(target: Vector2, magnet: float) -> bool:
	var d := position.distance_to(target)
	if d <= Tuning.COLLECT_RADIUS:
		return true
	if pulled or d <= magnet:
		pulled = true
		position = position.move_toward(target, Tuning.GEM_PULL_SPEED / Tuning.TICK_HZ)
	return false

func _draw() -> void:
	if tex:
		draw_texture(tex, -tex.get_size() / 2)
	else:
		draw_colored_polygon(PackedVector2Array([Vector2(0, -5), Vector2(4, 0), Vector2(0, 5), Vector2(-4, 0)]), Color("#F2B84B"))
```

`godot/features/weapons/beam_shot.gd`:
```gdscript
extends Node2D
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var dir := Vector2.RIGHT
var pierce := 1
var life: int = Tuning.BEAM_LIFE_TICKS
var hit_ids := {}
var dead := false
var tex: Texture2D

func setup(at: Vector2, d: Vector2, p: int) -> void:
	position = at
	dir = d
	pierce = p
	rotation = d.angle()
	tex = Art.texture(Art.BEAM)

func step() -> void:
	position += dir * Tuning.BEAM_SPEED / Tuning.TICK_HZ
	life -= 1

func _draw() -> void:
	if tex:
		draw_texture(tex, -tex.get_size() / 2)
	else:
		draw_rect(Rect2(-8, -2, 16, 4), Color("#FFF1C9"))
```

`godot/features/weapons/weapon_fx.gd`:
```gdscript
extends Node2D
## Draws orbiting moths and the Sunflare ring from session data.
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var session
var moth_tex: Texture2D
var flare_tex: Texture2D

func _ready() -> void:
	z_index = 3
	reload()

func reload() -> void:
	moth_tex = Art.texture(Art.ORBIT_MOTH)
	flare_tex = Art.texture(Art.SUNFLARE)

func _process(_d: float) -> void:
	queue_redraw()

func _draw() -> void:
	if session == null or session.prog == null:
		return
	for p in session.orbit_positions():
		if moth_tex:
			draw_texture(moth_tex, p - moth_tex.get_size() / 2)
		else:
			draw_circle(p, 4, Color("#FFF1C9"))
	if session.sunflare_ring > 0:
		var t := 1.0 - float(session.sunflare_ring) / Tuning.SUNFLARE_RING_TICKS
		var r := Tuning.SUNFLARE_RADIUS * t
		var c: Vector2 = session.player.position
		if flare_tex:
			draw_texture_rect(flare_tex, Rect2(c - Vector2(r, r), Vector2(r, r) * 2), false, Color(1, 1, 1, 1.0 - t))
		else:
			draw_arc(c, r, 0, TAU, 64, Color(0.95, 0.72, 0.29, 1.0 - t), 4.0)
```

`godot/features/world/ground.gd`:
```gdscript
extends Node2D
## Tiled ground and decorative stalls. Uses its own fixed seed so it never touches the game rng.
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var tile: Texture2D
var stall: Texture2D
var props: Array[Vector2] = []

func _ready() -> void:
	z_index = -10
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	tile = Art.texture(Art.GROUND)
	stall = Art.texture(Art.STALL)
	var r := RandomNumberGenerator.new()
	r.seed = 1234
	var a := Tuning.ARENA
	while props.size() < 18:
		var p := Vector2(r.randf_range(a.position.x + 48, a.end.x - 48), r.randf_range(a.position.y + 48, a.end.y - 48))
		if p.length() > 120:
			props.append(p)
	queue_redraw()

func _draw() -> void:
	var a := Tuning.ARENA
	if tile:
		draw_texture_rect(tile, a, true)
	else:
		draw_rect(a, Color("#1F2540"))
		for x in range(int(a.position.x), int(a.end.x), 64):
			draw_line(Vector2(x, a.position.y), Vector2(x, a.end.y), Color("#3B4A6B", 0.35))
		for y in range(int(a.position.y), int(a.end.y), 64):
			draw_line(Vector2(a.position.x, y), Vector2(a.end.x, y), Color("#3B4A6B", 0.35))
	for p in props:
		if stall:
			draw_texture(stall, p - stall.get_size() / 2)
		else:
			draw_rect(Rect2(p - Vector2(24, 16), Vector2(48, 32)), Color("#B5523B"))
			draw_circle(p - Vector2(0, 24), 6, Color("#F2B84B"))
	draw_rect(a, Color(0.95, 0.72, 0.29, 0.6), false, 2.0)
```

- [ ] **Step 7: Write `godot/game/session.gd`**

```gdscript
extends Node2D
## Owns one run. Fixed-tick and deterministic for a given seed: tick() is the whole simulation step.

const Tuning = preload("res://features/tuning.gd")
const GameState = preload("res://game/game_state.gd")
const Progression = preload("res://features/progression/progression.gd")
const PlayerScript = preload("res://features/player/player.gd")
const EnemyScript = preload("res://features/enemies/enemy.gd")
const GemScript = preload("res://features/pickups/gem.gd")
const BeamShot = preload("res://features/weapons/beam_shot.gd")
const WeaponFx = preload("res://features/weapons/weapon_fx.gd")
const Spawner = preload("res://features/enemies/spawner.gd")
const Ground = preload("res://features/world/ground.gd")
const AudioBusScript = preload("res://audio/audio_bus.gd")
const Hud = preload("res://ui/hud.gd")

signal run_started
signal enemy_killed(pos: Vector2)
signal gem_collected(value: int)
signal player_hurt(hp: int)
signal leveled_up(level: int)
signal evolved

var test_mode := false
var test_axis := Vector2.ZERO
var test_no_spawn := false

var state = GameState.new()
var prog
var rng := RandomNumberGenerator.new()
var spawner = Spawner.new()
var player
var actors: Node2D
var fx
var camera: Camera2D
var audio
var hud

var enemies: Array = []
var gems: Array = []
var shots: Array = []
var offered: Array[String] = []
var tick_count := 0
var kills := 0
var beam_timer := 0
var orbit_angle := 0.0
var orbit_hit := {}
var sunflare_timer := 0
var sunflare_ring := 0
var pose_override_ticks := 0
var banner_ticks := 0
var last_dir := Vector2.RIGHT

func _ready() -> void:
	_ensure_inputs()
	add_child(Ground.new())
	actors = Node2D.new()
	add_child(actors)
	player = PlayerScript.new()
	add_child(player)
	fx = WeaponFx.new()
	fx.session = self
	add_child(fx)
	camera = Camera2D.new()
	camera.limit_left = int(Tuning.ARENA.position.x)
	camera.limit_top = int(Tuning.ARENA.position.y)
	camera.limit_right = int(Tuning.ARENA.end.x)
	camera.limit_bottom = int(Tuning.ARENA.end.y)
	player.add_child(camera)
	player.damaged.connect(func(hp): player_hurt.emit(hp))
	player.died.connect(_on_player_died)
	audio = AudioBusScript.new()
	add_child(audio)
	audio.setup(self)
	hud = Hud.new()
	add_child(hud)
	hud.setup(self)

func start_run(seed_value: int = -1) -> void:
	if seed_value < 0:
		rng.randomize()
	else:
		rng.seed = seed_value
	for n in actors.get_children():
		n.free()
	enemies.clear(); gems.clear(); shots.clear(); offered.clear(); orbit_hit.clear()
	prog = Progression.new()
	prog.leveled_up.connect(func(l): leveled_up.emit(l))
	player.reset()
	tick_count = 0; kills = 0; beam_timer = 0; orbit_angle = 0.0
	sunflare_timer = 0; sunflare_ring = 0; pose_override_ticks = 0; banner_ticks = 0
	last_dir = Vector2.RIGHT
	if state.current == GameState.MENU:
		state.go(GameState.PLAYING)
	else:
		state.restart()
	run_started.emit()

func _physics_process(_d: float) -> void:
	if test_mode or state.current != GameState.PLAYING:
		return
	player.input_axis = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	tick()

func step_ticks(n: int) -> void:
	for i in n:
		tick()

func tick() -> void:
	if state.current != GameState.PLAYING:
		return
	tick_count += 1
	if test_mode:
		player.input_axis = test_axis
	if player.input_axis.length() > 0.1:
		last_dir = player.input_axis.normalized()
	player.step()
	_step_weapons()
	_step_enemies()
	if state.current != GameState.PLAYING:
		return
	_step_gems()
	if not test_no_spawn:
		for s in spawner.step(tick_count, rng):
			var at: Vector2 = player.position + Vector2.from_angle(s["angle"]) * Tuning.SPAWN_DISTANCE
			spawn_enemy(s["kind"], at.clamp(Tuning.ARENA.position, Tuning.ARENA.end))
	if banner_ticks > 0:
		banner_ticks -= 1
	if pose_override_ticks > 0:
		pose_override_ticks -= 1
		if pose_override_ticks == 0:
			player.set_override("")
	if tick_count >= Tuning.RUN_SECONDS * Tuning.TICK_HZ:
		player.set_override("victory")
		state.go(GameState.WON)
		return
	if prog.pending_levelups > 0:
		offered = prog.offer_cards(rng)
		player.set_override("levelup")
		state.go(GameState.LEVELUP)

func spawn_enemy(kind: String, at: Vector2) -> Node2D:
	if enemies.size() >= Tuning.MAX_ENEMIES:
		return null
	var e = EnemyScript.new()
	e.setup(kind, at)
	actors.add_child(e)
	enemies.append(e)
	return e

func drop_gem(at: Vector2, value: int) -> Node2D:
	var g = GemScript.new()
	g.setup(at, value)
	actors.add_child(g)
	gems.append(g)
	return g

func damage(e, amount: int) -> void:
	if e.dead:
		return
	e.hp -= amount
	e.flash = 3
	if e.hp <= 0:
		e.dead = true
		kills += 1
		enemies.erase(e)
		orbit_hit.erase(e.get_instance_id())
		enemy_killed.emit(e.position)
		drop_gem(e.position, e.xp)
		e.queue_free()

func orbit_positions() -> Array[Vector2]:
	var out: Array[Vector2] = []
	if prog == null or prog.evolved_sunflare or prog.moth_count == 0:
		return out
	for i in prog.moth_count:
		out.append(player.position + Vector2.from_angle(orbit_angle + TAU * i / prog.moth_count) * prog.moth_radius)
	return out

func _step_weapons() -> void:
	if prog.evolved_sunflare:
		sunflare_timer -= 1
		if sunflare_timer <= 0:
			sunflare_timer = Tuning.SUNFLARE_PERIOD
			sunflare_ring = Tuning.SUNFLARE_RING_TICKS
			player.cast_ticks = 12
			for e in enemies.duplicate():
				if e.position.distance_to(player.position) <= Tuning.SUNFLARE_RADIUS:
					damage(e, Tuning.SUNFLARE_DAMAGE)
		if sunflare_ring > 0:
			sunflare_ring -= 1
		return
	beam_timer -= 1
	if beam_timer <= 0:
		beam_timer = prog.beam_cooldown_ticks
		var s = BeamShot.new()
		s.setup(player.position, last_dir, prog.beam_pierce)
		actors.add_child(s)
		shots.append(s)
		player.cast_ticks = Tuning.CAST_POSE_TICKS
	for s in shots.duplicate():
		s.step()
		for e in enemies.duplicate():
			if e.dead or s.hit_ids.has(e.get_instance_id()):
				continue
			if s.position.distance_to(e.position) < e.radius + Tuning.BEAM_RADIUS:
				s.hit_ids[e.get_instance_id()] = true
				damage(e, Tuning.BEAM_DAMAGE)
				s.pierce -= 1
				if s.pierce <= 0:
					s.dead = true
					break
		if s.dead or s.life <= 0:
			shots.erase(s)
			s.queue_free()
	if prog.moth_count > 0:
		orbit_angle += Tuning.MOTH_SPIN / Tuning.TICK_HZ
		var moths := orbit_positions()
		for e in enemies.duplicate():
			var id: int = e.get_instance_id()
			if tick_count - int(orbit_hit.get(id, -9999)) < Tuning.MOTH_HIT_COOLDOWN:
				continue
			for p in moths:
				if p.distance_to(e.position) < e.radius + Tuning.MOTH_HIT_RADIUS:
					orbit_hit[id] = tick_count
					damage(e, Tuning.MOTH_DAMAGE)
					break

func _step_enemies() -> void:
	for e in enemies.duplicate():
		if state.current != GameState.PLAYING:
			return
		if e.dead:
			continue
		e.step(player.position)
		if e.position.distance_to(player.position) < e.radius + Tuning.PLAYER_RADIUS:
			player.take_hit(e.position, e.damage)

func _step_gems() -> void:
	var magnet: float = Tuning.PICKUP_RADIUS + int(prog.passive["magnet"]) * Tuning.PICKUP_RADIUS_PER_LEVEL
	for g in gems.duplicate():
		if g.step(player.position, magnet):
			gems.erase(g)
			g.queue_free()
			prog.add_xp(g.value)
			gem_collected.emit(g.value)

func choose_card(index: int) -> bool:
	if state.current != GameState.LEVELUP or index < 0 or index >= offered.size():
		return false
	var card: String = offered[index]
	prog.apply(card)
	prog.pending_levelups -= 1
	player.set_override("")
	match card:
		"heal":
			player.hp = mini(player.max_hp, player.hp + Tuning.HEAL_AMOUNT)
		"pass_speed":
			player.speed = Tuning.PLAYER_SPEED + int(prog.passive["speed"]) * Tuning.SPEED_PER_LEVEL
		"pass_hp":
			player.max_hp += Tuning.HP_PER_LEVEL
			player.hp += Tuning.HP_PER_LEVEL
		"sunflare":
			_evolve()
	offered = []
	state.go(GameState.PLAYING)
	return true

func _evolve() -> void:
	for s in shots:
		s.queue_free()
	shots.clear()
	sunflare_timer = Tuning.SUNFLARE_FIRST_DELAY
	player.empowered = true
	player.set_override("sunflare")
	pose_override_ticks = Tuning.EVOLVE_POSE_TICKS
	banner_ticks = Tuning.BANNER_TICKS
	evolved.emit()

func toggle_pause() -> void:
	if state.current == GameState.PLAYING:
		state.go(GameState.PAUSED)
	elif state.current == GameState.PAUSED:
		state.go(GameState.PLAYING)

func _on_player_died() -> void:
	player.set_override("defeat")
	state.go(GameState.LOST)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("start") and state.current == GameState.MENU:
		start_run()
	elif event.is_action_pressed("restart") and state.current != GameState.MENU:
		start_run()
	elif event.is_action_pressed("pause"):
		toggle_pause()
	elif event.is_action_pressed("mute_all"):
		audio.toggle_bus("Master")
	elif event.is_action_pressed("mute_music"):
		audio.toggle_bus("Music")
	elif event.is_action_pressed("mute_sfx"):
		audio.toggle_bus("SFX")
	elif event.is_action_pressed("debug_collision"):
		player.show_collision = not player.show_collision
		player.queue_redraw()
	elif state.current == GameState.LEVELUP:
		for i in 3:
			if event.is_action_pressed("card_%d" % (i + 1)):
				choose_card(i)
				return
		if event.is_action_pressed("ui_left"):
			hud.move_card(-1)
		elif event.is_action_pressed("ui_right"):
			hud.move_card(1)
		elif event.is_action_pressed("ui_accept"):
			choose_card(hud.card_cursor)

func _ensure_inputs() -> void:
	if InputMap.has_action("move_left"):
		return
	var keys := {
		"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT],
		"move_up": [KEY_W, KEY_UP], "move_down": [KEY_S, KEY_DOWN],
		"start": [KEY_ENTER, KEY_SPACE], "restart": [KEY_R], "pause": [KEY_ESCAPE, KEY_P],
		"mute_all": [KEY_M], "mute_music": [KEY_9], "mute_sfx": [KEY_0],
		"card_1": [KEY_1], "card_2": [KEY_2], "card_3": [KEY_3], "debug_collision": [KEY_F3],
	}
	for action in keys:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action, 0.2)
		for k in keys[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)
	var axes := {"move_left": [JOY_AXIS_LEFT_X, -1.0], "move_right": [JOY_AXIS_LEFT_X, 1.0], "move_up": [JOY_AXIS_LEFT_Y, -1.0], "move_down": [JOY_AXIS_LEFT_Y, 1.0]}
	for action in axes:
		var m := InputEventJoypadMotion.new()
		m.axis = axes[action][0]
		m.axis_value = axes[action][1]
		InputMap.action_add_event(action, m)
	var buttons := {"start": JOY_BUTTON_A, "pause": JOY_BUTTON_START, "restart": JOY_BUTTON_Y}
	for action in buttons:
		var b := InputEventJoypadButton.new()
		b.button_index = buttons[action]
		InputMap.action_add_event(action, b)
```

- [ ] **Step 8: Run to verify it passes**

Run: `$GODOT --headless --path . --script res://tests/test_gameplay.gd`
Expected: `gameplay: 30 checks, 0 failures`. Note the `long-run-smoke` observation (state/seconds/kills/level) — it is the first balance datapoint; if the run dies before 0:45 or never levels past 4, adjust `SPAWN_TABLE`/`XP_TO_LEVEL` in tuning.gd, rerun, and record the before/after numbers for TEST-REPORT.
If `hurt-iframes` reports 3 hurts instead of 4, the knockback is ending contact: keep the test's `w.position = game.player.position` pin (it is there to isolate i-frames from knockback) and check `IFRAME_TICKS` arithmetic: hits at ticks 1, 49, 97, 145 → 4 in 150 ticks.

- [ ] **Step 9: Run the game once by hand to see the greybox**

Run: `$GODOT --path godot` — press Enter; the menu HUD is still a stub so the run starts immediately visible only as shapes. Close.

- [ ] **Step 10: Commit**

```bash
git add godot evidence/gameplay.json
git commit -m "Add deterministic survivors simulation with placeholder drawing

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 11: AudioBus — throttled SFX, music behaviour, mute, independence

**Files:**
- Replace: `godot/audio/audio_bus.gd`
- Create: `godot/tests/test_audio.gd`

**Interfaces:**
- Consumes: session signals and `session.state.changed`, `session.tick_count`, SfxGate.
- Produces: `setup(session)`, `sfx(id) -> bool`, `toggle_bus(name)`, `is_bus_muted(name) -> bool`, `play_log: Array[Dictionary{id, ms, tick}]`, `disable_streams: bool`, `music_state: String` ∈ {"stopped","playing","paused","ducked","fading"}, `base`, `layer` (AudioStreamPlayer), const `SFX_PATHS`, `RULES`.

- [ ] **Step 1: Write the failing audio tests `godot/tests/test_audio.gd`**

```gdscript
extends "res://tests/harness.gd"
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
var game

func fresh(seed_value: int, no_spawn: bool, silent: bool) -> void:
	if is_instance_valid(game):
		game.free()
	for bus in ["Master", "Music", "SFX"]:
		var i := AudioServer.get_bus_index(bus)
		if i >= 0:
			AudioServer.set_bus_mute(i, false)
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = no_spawn
	root.add_child(game)
	game.audio.disable_streams = silent
	if silent:
		AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"), true)
	game.start_run(seed_value)

func autoplay(ticks: int) -> Dictionary:
	var counts := {"kill": 0, "pickup": 0, "hurt": 0, "levelup": 0, "evolve": 0}
	game.enemy_killed.connect(func(_p): counts["kill"] += 1)
	game.gem_collected.connect(func(_v): counts["pickup"] += 1)
	game.player_hurt.connect(func(_h): counts["hurt"] += 1)
	game.leveled_up.connect(func(_l): counts["levelup"] += 1)
	game.evolved.connect(func(): counts["evolve"] += 1)
	for t in ticks:
		if game.state.is_terminal():
			break
		if game.state.current == GS.LEVELUP:
			var pick: int = game.offered.find("sunflare")
			game.choose_card(maxi(pick, 0))
		var a := float(t) / 90.0
		game.test_axis = Vector2(cos(a), sin(a))
		game.tick()
	return counts

func summary() -> Dictionary:
	return {"state": GS.NAMES[game.state.current], "tick": game.tick_count, "kills": game.kills,
		"level": game.prog.level, "hp": game.player.hp, "x": snappedf(game.player.position.x, 0.01),
		"y": snappedf(game.player.position.y, 0.01), "enemies": game.enemies.size(), "evolved": game.prog.evolved_sunflare}

func plays(id: String) -> Array:
	return game.audio.play_log.filter(func(e): return e["id"] == id)

func min_gap_ms(id: String) -> int:
	var p := plays(id)
	var gap := 1 << 30
	for i in range(1, p.size()):
		gap = mini(gap, int(p[i]["ms"]) - int(p[i - 1]["ms"]))
	return gap

func run() -> void:
	suite = "audio"
	var ticks := Tuning.RUN_SECONDS * Tuning.TICK_HZ + 10
	fresh(11, false, false)
	var counts := autoplay(ticks)
	var loud := summary()
	check("once-levelup", plays("levelup").size() == counts["levelup"], {"plays": plays("levelup").size(), "events": counts["levelup"]})
	check("once-hurt", plays("hurt").size() == counts["hurt"], {"plays": plays("hurt").size(), "events": counts["hurt"]})
	check("once-evolve", plays("evolve").size() == counts["evolve"] and counts["evolve"] <= 1)
	check("kill-throttled", plays("kill").size() <= counts["kill"] and min_gap_ms("kill") >= 60, {"plays": plays("kill").size(), "kills": counts["kill"], "min_gap": min_gap_ms("kill")})
	check("pickup-merged", plays("pickup").size() <= counts["pickup"] and min_gap_ms("pickup") >= 80, {"plays": plays("pickup").size(), "events": counts["pickup"]})
	var stingers := plays("lose").size() + plays("win").size()
	check("one-stinger", stingers == (1 if game.state.is_terminal() else 0), {"state": loud["state"], "stingers": stingers})
	fresh(11, false, true)
	autoplay(ticks)
	var silent := summary()
	check("independence", loud == silent, {"with_sound": loud, "silent": silent})

	fresh(1, true, false)
	for i in 20:
		game.spawn_enemy("moth", Vector2(30 + i, 0))
	for e in game.enemies.duplicate():
		game.damage(e, 99)
	check("burst-20-kills-one-sfx", plays("kill").size() == 1, {"plays": plays("kill").size()})

	fresh(1, true, false)
	game.test_axis = Vector2.RIGHT
	game.audio.play_log.clear()
	game.step_ticks(100)
	check("hold-input-no-sfx", game.audio.play_log.is_empty())
	for i in 20:
		game.toggle_pause()
		game.tick()
	check("rapid-pause-no-sfx", game.audio.play_log.is_empty() and game.state.current == GS.PLAYING)

	var music := AudioServer.get_bus_index("Music")
	game.toggle_pause()
	check("pause-lowpass-and-duck", AudioServer.is_bus_effect_enabled(music, 0) and is_equal_approx(AudioServer.get_bus_volume_db(music), -10.0) and game.audio.music_state == "paused")
	game.toggle_pause()
	check("resume-restores", not AudioServer.is_bus_effect_enabled(music, 0) and is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0) and game.audio.music_state == "playing")
	game.prog.add_xp(3)
	game.tick()
	check("levelup-duck", is_equal_approx(AudioServer.get_bus_volume_db(music), -6.0))
	game.choose_card(0)
	check("levelup-unduck", is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0))

	var before := [game.state.current, game.tick_count]
	for bus in ["Master", "Music", "SFX"]:
		game.audio.toggle_bus(bus)
	check("mute-flags", game.audio.is_bus_muted("Master") and game.audio.is_bus_muted("Music") and game.audio.is_bus_muted("SFX"))
	check("mute-no-state-change", before == [game.state.current, game.tick_count])
	for bus in ["Master", "Music", "SFX"]:
		game.audio.toggle_bus(bus)

	game.player.hp = 1
	var w = game.spawn_enemy("wraith", game.player.position)
	w.hp = 9999
	game.tick()
	check("lost-fades", game.state.current == GS.LOST and game.audio.music_state == "fading" and plays("lose").size() == 1)
	await create_timer(0.8).timeout
	check("lost-stops", game.audio.music_state == "stopped")

	game.start_run(2)
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.tick()
	game.start_run(3)
	await create_timer(0.8).timeout
	check("restart-during-fade", game.audio.music_state == "playing" and is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0) and (game.audio.base.stream == null or game.audio.base.volume_db > -1.0))

	game.toggle_pause()
	game.start_run(4)
	check("restart-from-pause", not AudioServer.is_bus_effect_enabled(music, 0) and is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0) and game.audio.music_state == "playing")
	check("music-loop-flag", game.audio.base.stream == null or game.audio.base.stream.loop)
```

- [ ] **Step 2: Run to verify it fails**

Run: `$GODOT --headless --path . --script res://tests/test_audio.gd`
Expected: errors — `disable_streams` / `play_log` not found on the stub.

- [ ] **Step 3: Write `godot/audio/audio_bus.gd`**

```gdscript
extends Node
## Listens to session signals and plays sound. Never writes game state.

const SfxGate = preload("res://audio/sfx_gate.gd")
const GameState = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const SFX_PATHS := {
	"kill": "res://assets/sfx/sfx_01_kill.wav",
	"pickup": "res://assets/sfx/sfx_02_pickup.wav",
	"hurt": "res://assets/sfx/sfx_03_hurt.wav",
	"levelup": "res://assets/sfx/sfx_04_levelup.wav",
	"evolve": "res://assets/sfx/sfx_05_evolve.wav",
	"lose": "res://assets/sfx/sfx_06a_lose.wav",
	"win": "res://assets/sfx/sfx_06b_win.wav",
}
const MUSIC_BASE := "res://assets/music/mus_01_night_market.ogg"
const MUSIC_LAYER := "res://assets/music/mus_02_sunflare_layer.ogg"
const RULES := {
	"kill": {"cooldown_ms": 60, "max_voices": 3},
	"pickup": {"cooldown_ms": 80, "max_voices": 1},
	"hurt": {"cooldown_ms": 800, "max_voices": 1},
	"levelup": {"cooldown_ms": 0, "max_voices": 8},
	"evolve": {"once": true, "max_voices": 1},
	"lose": {"max_voices": 1},
	"win": {"max_voices": 1},
}
const VOICE_MS := 300
const PAUSE_DB := -10.0
const LEVELUP_DB := -6.0
const SILENT_DB := -80.0
const LOWPASS_HZ := 900.0

var gate = SfxGate.new(RULES)
var play_log: Array[Dictionary] = []
var disable_streams := false
var music_state := "stopped"
var session
var streams := {}
var pools := {}
var voice_end_ms := {}
var base: AudioStreamPlayer
var layer: AudioStreamPlayer
var _fade: Tween
var _layer_fade: Tween

func setup(s) -> void:
	session = s
	process_mode = Node.PROCESS_MODE_ALWAYS
	_ensure_buses()
	for id in SFX_PATHS:
		if ResourceLoader.exists(SFX_PATHS[id]):
			streams[id] = load(SFX_PATHS[id])
		var pool: Array = []
		for i in int(RULES[id].get("max_voices", 1)):
			var p := AudioStreamPlayer.new()
			p.bus = "SFX"
			add_child(p)
			pool.append(p)
		pools[id] = pool
	base = _music_player(MUSIC_BASE)
	layer = _music_player(MUSIC_LAYER)
	s.enemy_killed.connect(func(_p): sfx("kill"))
	s.gem_collected.connect(func(_v): sfx("pickup"))
	s.player_hurt.connect(func(_h): sfx("hurt"))
	s.leveled_up.connect(func(_l): sfx("levelup"))
	s.evolved.connect(_on_evolved)
	s.run_started.connect(_on_run_started)
	s.state.changed.connect(_on_state_changed)

func _music_player(path: String) -> AudioStreamPlayer:
	var p := AudioStreamPlayer.new()
	p.bus = "Music"
	if ResourceLoader.exists(path):
		var st = load(path)
		if st is AudioStreamOggVorbis:
			st.loop = true
		p.stream = st
	add_child(p)
	return p

func now_ms() -> int:
	return int(session.tick_count * 1000.0 / Tuning.TICK_HZ)

func sfx(id: String) -> bool:
	var now := now_ms()
	var ends: Array = voice_end_ms.get(id, []).filter(func(t): return t > now)
	voice_end_ms[id] = ends
	if not gate.request(id, now, ends.size()):
		return false
	ends.append(now + VOICE_MS)
	play_log.append({"id": id, "ms": now, "tick": session.tick_count})
	var stream: AudioStream = null if disable_streams else streams.get(id)
	if stream:
		var pool: Array = pools[id]
		var player: AudioStreamPlayer = pool[0]
		for p in pool:
			if not p.playing:
				player = p
				break
		player.stream = stream
		player.pitch_scale = randf_range(0.95, 1.05) if id == "kill" else 1.0
		player.play()
	return true

func _on_run_started() -> void:
	_kill_tweens()
	gate.reset()
	voice_end_ms.clear()
	_set_lowpass(false)
	_set_music_db(0.0)
	base.stop()
	layer.stop()
	base.volume_db = 0.0
	layer.volume_db = SILENT_DB
	if not disable_streams:
		if base.stream:
			base.play(0.0)
		if layer.stream:
			layer.play(0.0)
	music_state = "playing"

func _on_state_changed(from: int, to: int) -> void:
	match to:
		GameState.PAUSED:
			_set_lowpass(true)
			_set_music_db(PAUSE_DB)
			music_state = "paused"
		GameState.LEVELUP:
			_set_music_db(LEVELUP_DB)
			music_state = "ducked"
		GameState.PLAYING:
			if from == GameState.PAUSED or from == GameState.LEVELUP:
				_set_lowpass(false)
				_set_music_db(0.0)
				music_state = "playing"
		GameState.LOST:
			_fade_out(0.5)
			sfx("lose")
		GameState.WON:
			_fade_out(1.0)
			sfx("win")

func _on_evolved() -> void:
	sfx("evolve")
	if _layer_fade:
		_layer_fade.kill()
	_layer_fade = create_tween()
	_layer_fade.tween_property(layer, "volume_db", 0.0, 2.0)

func _fade_out(seconds: float) -> void:
	_kill_tweens()
	music_state = "fading"
	_fade = create_tween().set_parallel(true)
	_fade.tween_property(base, "volume_db", SILENT_DB, seconds)
	_fade.tween_property(layer, "volume_db", SILENT_DB, seconds)
	_fade.chain().tween_callback(_stop_music)

func _stop_music() -> void:
	base.stop()
	layer.stop()
	music_state = "stopped"

func _kill_tweens() -> void:
	if _fade:
		_fade.kill()
		_fade = null
	if _layer_fade:
		_layer_fade.kill()
		_layer_fade = null

func _ensure_buses() -> void:
	for bus_name in ["Music", "SFX"]:
		if AudioServer.get_bus_index(bus_name) == -1:
			AudioServer.add_bus()
			var i := AudioServer.bus_count - 1
			AudioServer.set_bus_name(i, bus_name)
			AudioServer.set_bus_send(i, "Master")
	var mi := AudioServer.get_bus_index("Music")
	if AudioServer.get_bus_effect_count(mi) == 0:
		var lp := AudioEffectLowPassFilter.new()
		lp.cutoff_hz = LOWPASS_HZ
		AudioServer.add_bus_effect(mi, lp)
	AudioServer.set_bus_effect_enabled(mi, 0, false)

func _set_lowpass(on: bool) -> void:
	AudioServer.set_bus_effect_enabled(AudioServer.get_bus_index("Music"), 0, on)

func _set_music_db(db: float) -> void:
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), db)

func toggle_bus(bus_name: String) -> void:
	var i := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_mute(i, not AudioServer.is_bus_mute(i))

func is_bus_muted(bus_name: String) -> bool:
	return AudioServer.is_bus_mute(AudioServer.get_bus_index(bus_name))
```

- [ ] **Step 4: Run all three suites**

Run: `for s in logic gameplay audio; do $GODOT --headless --path . --script res://tests/test_$s.gd || break; done`
Expected: `logic: 26 … 0 failures`, `gameplay: 27 … 0 failures`, `audio: 21 checks, 0 failures`. (No asset files exist yet, so streams are null in both runs; `independence` becomes a stronger check again in Task 19 once real streams load.)

- [ ] **Step 5: Commit**

```bash
git add godot/audio godot/tests/test_audio.gd evidence/audio.json
git commit -m "Add AudioBus: gated SFX, music duck/filter/fade, mute; prove audio never drives state

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 12: HUD — menu, bars, cards, pause, end panel, mute indicators, silent feedback

**Files:** Replace `godot/ui/hud.gd`; Modify `godot/tests/test_gameplay.gd`

**Interfaces:** Consumes session fields listed in Task 10; produces `setup(session)`, `move_card(delta)`, `card_cursor`, `lines() -> PackedStringArray` (the text currently shown — lets tests assert readability without pixels).

- [ ] **Step 1: Add failing HUD readability checks** at the end of `test_gameplay.gd::run()`:

```gdscript
	await fresh()
	check("hud-shows-timer-hp-level", _has(game.hud.lines(), "0:00") and _has(game.hud.lines(), "HP 10/10") and _has(game.hud.lines(), "Lv 1"), {"lines": game.hud.lines()})
	game.prog.add_xp(3)
	game.tick()
	check("hud-shows-cards", _has(game.hud.lines(), "[1]") and _has(game.hud.lines(), "[3]"), {"lines": game.hud.lines()})
	game.choose_card(0)
	game.toggle_pause()
	check("hud-shows-paused", _has(game.hud.lines(), "PAUSED"))
	game.toggle_pause()
	game.player.hp = 1
	var wx = game.spawn_enemy("wraith", game.player.position)
	wx.hp = 9999
	game.tick()
	check("hud-shows-lost-and-retry", _has(game.hud.lines(), "The lamp went out") and _has(game.hud.lines(), "R / Y to retry"))
	game.audio.toggle_bus("Music")
	check("hud-shows-mute-state", _has(game.hud.lines(), "MUSIC off"))
	game.audio.toggle_bus("Music")
```

and the helper:

```gdscript
func _has(lines: PackedStringArray, needle: String) -> bool:
	for l in lines:
		if needle in l:
			return true
	return false
```

- [ ] **Step 2: Run to verify it fails** — Expected: `lines` not found on the HUD stub.

- [ ] **Step 3: Write `godot/ui/hud.gd`**

```gdscript
extends CanvasLayer
## All on-screen text and bars. Every event that has a sound also has a visual here or on the sprite.

const GameState = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const Progression = preload("res://features/progression/progression.gd")
const PlayerScript = preload("res://features/player/player.gd")
const Art = preload("res://features/art.gd")

const W := 640.0
const H := 360.0
const INK := Color("#14121C")
const CREAM := Color("#FFF1C9")
const GOLD := Color("#F2B84B")
const RED := Color("#B5523B")
const MIST := Color("#C7D0E0")

var session
var view: Control
var card_cursor := 0
var portrait: Texture2D
var _lines := PackedStringArray()

func setup(s) -> void:
	session = s
	layer = 10
	view = Control.new()
	view.size = Vector2(W, H)
	view.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(view)
	view.draw.connect(_draw_view)
	portrait = Art.texture(Art.PC_SHEET)
	s.state.changed.connect(_on_state_changed)

func _on_state_changed(_from: int, to: int) -> void:
	if to == GameState.LEVELUP:
		card_cursor = 0

func _process(_d: float) -> void:
	view.queue_redraw()

func move_card(delta: int) -> void:
	card_cursor = wrapi(card_cursor + delta, 0, maxi(1, session.offered.size()))

## Text currently on screen; rebuilt from state so tests can read it without drawing.
func lines() -> PackedStringArray:
	_lines = PackedStringArray()
	var st: int = session.state.current
	_lines.append("MUSIC %s  SFX %s  [M/9/0]" % ["off" if _muted("Music") or _muted("Master") else "on", "off" if _muted("SFX") or _muted("Master") else "on"])
	if st == GameState.MENU:
		_lines.append_array(["LANTERNFALL", "Survive the fog for 3:00", "Move: WASD / arrows / left stick", "Enter / A to start"])
		return _lines
	var secs: int = session.tick_count / Tuning.TICK_HZ
	_lines.append("%d:%02d" % [secs / 60, secs % 60])
	_lines.append("HP %d/%d" % [session.player.hp, session.player.max_hp])
	_lines.append("Lv %d" % session.prog.level)
	_lines.append("Kills %d" % session.kills)
	if session.prog.evolved_sunflare:
		_lines.append("Sunflare Lighthouse")
	else:
		_lines.append("Beam %d/3  Moths %d/3" % [session.prog.beam_level, session.prog.moth_level])
	if session.banner_ticks > 0:
		_lines.append("SUNFLARE LIGHTHOUSE")
	match st:
		GameState.LEVELUP:
			for i in session.offered.size():
				var t: Array = Progression.CARD_TEXT[session.offered[i]]
				_lines.append("[%d] %s — %s" % [i + 1, t[0], t[1]])
		GameState.PAUSED:
			_lines.append("PAUSED — Esc/P resume · R restart")
		GameState.LOST:
			_lines.append("The lamp went out — %d:%02d" % [secs / 60, secs % 60])
			_lines.append("R / Y to retry")
		GameState.WON:
			_lines.append("3:00 — The fog lifts")
			_lines.append("R / Y to play again")
	return _lines

func _muted(bus: String) -> bool:
	var i := AudioServer.get_bus_index(bus)
	return i >= 0 and AudioServer.is_bus_mute(i)

func _text(pos: Vector2, s: String, size := 12, color := CREAM, align := HORIZONTAL_ALIGNMENT_LEFT, width := -1.0) -> void:
	view.draw_string(ThemeDB.fallback_font, pos, s, align, width, size, color)

func _pose(p: String, rect: Rect2) -> void:
	if portrait:
		var i := PlayerScript.POSES.find(p)
		view.draw_texture_rect_region(portrait, rect, Rect2(i * 32, 0, 32, 32))

func _draw_view() -> void:
	var l := lines()
	var st: int = session.state.current
	_text(Vector2(0, 14), l[0], 9, MIST, HORIZONTAL_ALIGNMENT_RIGHT, W - 6)
	if st == GameState.MENU:
		view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.55))
		_pose("turn_front", Rect2(W / 2 - 48, 70, 96, 96))
		_text(Vector2(0, 200), l[1], 32, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
		_text(Vector2(0, 228), l[2], 12, CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
		_text(Vector2(0, 250), l[3], 10, MIST, HORIZONTAL_ALIGNMENT_CENTER, W)
		_text(Vector2(0, 300), l[4], 14, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
		return
	var p = session.player
	if p.iframes > Tuning.IFRAME_TICKS - 10:
		view.draw_rect(Rect2(0, 0, W, H), Color(RED, 0.22))
	view.draw_rect(Rect2(8, 8, 120, 10), Color(INK, 0.8))
	view.draw_rect(Rect2(8, 8, 120.0 * p.hp / p.max_hp, 10), RED)
	_text(Vector2(10, 30), l[2], 10)
	_text(Vector2(0, 20), l[1], 16, CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
	_text(Vector2(10, 44), l[3] + "   " + l[4], 10, MIST)
	_text(Vector2(10, 58), l[5], 10, GOLD)
	var prog = session.prog
	view.draw_rect(Rect2(0, H - 6, W, 6), Color(INK, 0.8))
	view.draw_rect(Rect2(0, H - 6, W * float(prog.xp) / prog.xp_needed(), 6), GOLD)
	if session.banner_ticks > 0:
		view.draw_rect(Rect2(0, 120, W, 40), Color(INK, 0.7))
		_text(Vector2(0, 148), "SUNFLARE LIGHTHOUSE", 22, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
	match st:
		GameState.LEVELUP:
			view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.6))
			_text(Vector2(0, 70), "LEVEL UP — choose one", 18, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
			for i in session.offered.size():
				var r := Rect2(40 + i * 195, 90, 175, 190)
				var t: Array = Progression.CARD_TEXT[session.offered[i]]
				view.draw_rect(r, CREAM if i != card_cursor else GOLD)
				view.draw_rect(r, INK, false, 2.0)
				_text(r.position + Vector2(8, 22), "[%d]" % (i + 1), 12, INK)
				_text(r.position + Vector2(8, 60), t[0], 13, INK)
				_text(r.position + Vector2(8, 90), t[1], 10, INK, HORIZONTAL_ALIGNMENT_LEFT, r.size.x - 16)
			_pose("levelup", Rect2(8, H - 104, 96, 96))
		GameState.PAUSED:
			view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.6))
			_text(Vector2(0, 180), "PAUSED", 28, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
			_text(Vector2(0, 210), "Esc/P resume · R restart · M/9/0 audio", 11, CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
		GameState.LOST, GameState.WON:
			var won := st == GameState.WON
			view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.65))
			_pose("victory" if won else "defeat", Rect2(W / 2 - 64, 60, 128, 128))
			_text(Vector2(0, 220), l[-2], 22, GOLD if won else CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
			_text(Vector2(0, 246), "Kills %d · Level %d" % [session.kills, prog.level], 12, MIST, HORIZONTAL_ALIGNMENT_CENTER, W)
			_text(Vector2(0, 280), l[-1], 14, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
```

- [ ] **Step 4: Run all suites** — Expected: gameplay now `35 checks, 0 failures`; logic and audio unchanged.

- [ ] **Step 5: Play by hand for 60 s** (`./walker-lanternfall.command`): Enter starts, WASD moves, a level-up shows 3 cards, 1/2/3 picks, Esc pauses, M/9/0 flip the indicator, F3 shows the collision circle. Fix anything broken before committing.

- [ ] **Step 6: Commit**

```bash
git add godot/ui godot/tests/test_gameplay.gd evidence/gameplay.json
git commit -m "Add HUD: menu, bars, level-up cards, pause, end panels, mute state

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

# Phase C — Generation (only after `design-v1` exists)

**Gate check before any step in this phase:** `git rev-parse design-v1` must succeed. If it fails, stop.

### Task 13: Generation environments (+ HUMAN license step)

**Files:** Create `gen/requirements-art.txt`, `gen/requirements-audio.txt`

- [ ] **Step 1: Install uv and Python 3.12 (does not touch the system/anaconda Python 3.14)**

```bash
brew install uv
uv python install 3.12
```

- [ ] **Step 2: Write requirement files**

`gen/requirements-art.txt`:
```
mflux
pillow
numpy
```
`gen/requirements-audio.txt`:
```
torch
torchaudio
diffusers>=0.30
transformers>=4.44
accelerate
torchsde
einops
soundfile
librosa
numpy
matplotlib
huggingface_hub
```

- [ ] **Step 3: Create venvs**

```bash
uv venv --python 3.12 gen/.venv-art && uv pip install --python gen/.venv-art -r gen/requirements-art.txt
uv venv --python 3.12 gen/.venv-audio && uv pip install --python gen/.venv-audio -r gen/requirements-audio.txt
gen/.venv-art/bin/mflux-generate --help | head -40
gen/.venv-audio/bin/python -c "import torch, diffusers, transformers; print(torch.__version__, torch.backends.mps.is_available(), diffusers.__version__, transformers.__version__)"
```
Expected: help text lists `--model --prompt --seed --steps --width --height --quantize --output` (if a flag name differs in the installed mflux version, update `art_generate.py` in Task 15 to match and note it in SOURCES.md); torch prints `True` for MPS.

- [ ] **Step 4: HUMAN — Stable Audio Open licence.** Ask Bao to (a) open https://huggingface.co/stabilityai/stable-audio-open-1.0, read and accept the Stability AI Community License in person, and (b) run `gen/.venv-audio/bin/huggingface-cli login` in Bao's own terminal. Claude never handles the token.

- [ ] **Step 5: Pre-download weights** (after Step 4)

```bash
gen/.venv-audio/bin/python -c "from huggingface_hub import snapshot_download as d; [print(d(r)) for r in ['stabilityai/stable-audio-open-1.0','facebook/musicgen-medium','facebook/musicgen-melody']]"
```
FLUX.1-schnell downloads on the first mflux run.

- [ ] **Step 6: Commit**

```bash
git add gen/requirements-*.txt && git commit -m "Pin local generation environments

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 14: Logging pipeline — sidecars, decisions, contact sheets, ASSET-LOG

**Files:** Create `gen/common.py`, `gen/decide.py`, `gen/render_log.py`, `gen/contact_sheet.py`

**Interfaces:**
- Produces: `common.new_run_id(asset_id, seed) -> str` (`<ASSET-ID>-<YYYYMMDDTHHMMSSZ>-s<seed>`), `common.write_sidecar(meta: dict) -> Path` (to `gen/log/<ASSET-ID>/<run_id>.json`, adds `created_utc`), `common.thumbnail_image(src, asset_id, run_id) -> Path` (256 px into `gen/thumbs/`), `common.thumbnail_audio(src, asset_id, run_id) -> Path` (waveform+spectrogram PNG), `common.ROOT`.
- Sidecar schema: `asset_id, run_id, created_utc, model, model_version, runtime, license, prompt, negative_prompt, settings{…}, raw_outputs[], thumbnail, storyboard_panels[], decision: null | {verdict: accept|modify|reject, reason, edits, final_paths[], decided_by, decided_utc}`.

- [ ] **Step 1: Write `gen/common.py`**

```python
"""Shared helpers for the generation pipeline: run ids, JSON sidecars and thumbnails."""
import datetime as dt
import json
import platform
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = f"local — {platform.machine()} macOS {platform.mac_ver()[0]} (Apple M4 Pro, 16 GB)"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def new_run_id(asset_id: str, seed: int) -> str:
    return f"{asset_id}-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-s{seed}"


def write_sidecar(meta: dict) -> Path:
    meta = {"created_utc": utc_now(), "runtime": RUNTIME, "decision": None, **meta}
    path = ROOT / "gen" / "log" / meta["asset_id"] / f"{meta['run_id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta, indent=2) + "\n")
    return path


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


def thumbnail_image(src: Path, asset_id: str, run_id: str) -> Path:
    from PIL import Image
    out = ROOT / "gen" / "thumbs" / asset_id / f"{run_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    im.thumbnail((256, 256))
    im.save(out, optimize=True)
    return out


def thumbnail_audio(src: Path, asset_id: str, run_id: str) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import soundfile as sf
    y, sr = sf.read(src, always_2d=True)
    m = y.mean(axis=1)
    out = ROOT / "gen" / "thumbs" / asset_id / f"{run_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, (a, b) = plt.subplots(2, 1, figsize=(3.2, 1.8), dpi=80)
    a.plot(np.arange(len(m)) / sr, m, linewidth=0.4)
    a.set_axis_off()
    b.specgram(m, Fs=sr, NFFT=512, noverlap=256)
    b.set_axis_off()
    fig.tight_layout(pad=0.1)
    fig.savefig(out)
    plt.close(fig)
    return out
```

- [ ] **Step 2: Write `gen/decide.py`**

```python
#!/usr/bin/env python3
"""Record Bao's decision on one generation run.

    python gen/decide.py ART-PC-01 <run_id> accept "reason" --edits "..." --final godot/assets/art/pc_sheet.png
"""
import argparse, json, shutil
from pathlib import Path
from common import ROOT, utc_now

ap = argparse.ArgumentParser()
ap.add_argument("asset_id")
ap.add_argument("run_id")
ap.add_argument("verdict", choices=["accept", "modify", "reject"])
ap.add_argument("reason")
ap.add_argument("--edits", default="")
ap.add_argument("--final", nargs="*", default=[])
ap.add_argument("--by", default="Bao Xing")
a = ap.parse_args()

side = ROOT / "gen" / "log" / a.asset_id / f"{a.run_id}.json"
meta = json.loads(side.read_text())
meta["decision"] = {"verdict": a.verdict, "reason": a.reason, "edits": a.edits, "final_paths": a.final,
                    "decided_by": a.by, "decided_utc": utc_now()}
if a.verdict in ("accept", "modify"):
    for raw in meta.get("raw_outputs", []):
        src = ROOT / raw
        if src.exists():
            dst = ROOT / "gen" / "accepted" / a.asset_id / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            meta.setdefault("accepted_copies", []).append(str(dst.relative_to(ROOT)))
side.write_text(json.dumps(meta, indent=2) + "\n")
print(f"{a.asset_id} {a.run_id}: {a.verdict}")
```

- [ ] **Step 3: Write `gen/contact_sheet.py`**

```python
#!/usr/bin/env python3
"""Contact sheet of every thumbnail for an asset, stamped ACCEPT/MODIFY/REJECT/PENDING.

    python gen/contact_sheet.py ART-PC-01      -> gen/rejected/ART-PC-01-contact.png
"""
import json, sys
from PIL import Image, ImageDraw
from common import ROOT

asset = sys.argv[1]
sides = sorted((ROOT / "gen" / "log" / asset).glob("*.json"))
tiles = []
for s in sides:
    m = json.loads(s.read_text())
    th = ROOT / m["thumbnail"]
    im = Image.open(th).convert("RGB").resize((256, 256)) if th.exists() else Image.new("RGB", (256, 256), "gray")
    verdict = (m.get("decision") or {}).get("verdict", "pending").upper()
    d = ImageDraw.Draw(im)
    color = {"ACCEPT": "#2E8B57", "MODIFY": "#F2B84B", "REJECT": "#B5523B"}.get(verdict, "#6E7FA3")
    d.rectangle([0, 226, 255, 255], fill=color)
    d.text((6, 232), f"{verdict}  seed {m['settings'].get('seed')}", fill="white")
    tiles.append(im)
cols = min(4, max(1, len(tiles)))
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 260, max(1, rows) * 260), "#14121C")
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 260 + 2, (i // cols) * 260 + 2))
out = ROOT / "gen" / "rejected" / f"{asset}-contact.png"
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out, optimize=True)
print(out)
```

- [ ] **Step 4: Write `gen/render_log.py`**

```python
#!/usr/bin/env python3
"""Render ASSET-LOG.md from gen/log/**.json. The sidecars are the source of truth; never hand-edit ASSET-LOG.md."""
import json
from collections import defaultdict
from common import ROOT

runs = defaultdict(list)
for p in sorted((ROOT / "gen" / "log").glob("*/*.json")):
    m = json.loads(p.read_text())
    runs[m["asset_id"]].append(m)

out = ["# ASSET-LOG", "",
       "Rendered by `gen/render_log.py` from the JSON sidecars in `gen/log/`. Every run is listed, including rejects.",
       "Tag `design-v1` precedes every timestamp below (checked by `scripts/audit_repo.py --stage final`).", ""]
for asset in sorted(runs):
    out += [f"## {asset}", ""]
    contact = ROOT / "gen" / "rejected" / f"{asset}-contact.png"
    if contact.exists():
        out += [f"![{asset} contact sheet](gen/rejected/{asset}-contact.png)", ""]
    for m in sorted(runs[asset], key=lambda r: r["created_utc"]):
        d = m.get("decision") or {}
        out += [f"### {m['run_id']}", "",
                "| Field | Value |", "|---|---|",
                f"| Created (UTC) | {m['created_utc']} |",
                f"| Model / version | {m['model']} / {m['model_version']} |",
                f"| Runtime | {m['runtime']} |",
                f"| Licence / terms | {m['license']} |",
                f"| Settings | `{json.dumps(m['settings'])}` |",
                f"| Storyboard panels | {', '.join(m.get('storyboard_panels', []))} |",
                f"| Decision | **{d.get('verdict', 'PENDING')}** by {d.get('decided_by', '—')} at {d.get('decided_utc', '—')} |",
                f"| Reason | {d.get('reason', '—')} |",
                f"| Manual edits | {d.get('edits') or '—'} |",
                f"| Project files | {', '.join(d.get('final_paths', [])) or '—'} |",
                f"| Thumbnail | ![]({m['thumbnail']}) |", "",
                "**Prompt**", "", "```", m["prompt"], "```", "",
                "**Negative prompt**", "", "```", m.get("negative_prompt") or "(none)", "```", ""]
(ROOT / "ASSET-LOG.md").write_text("\n".join(out) + "\n")
print(f"ASSET-LOG.md: {sum(len(v) for v in runs.values())} runs across {len(runs)} assets")
```

- [ ] **Step 5: Smoke test with a fake sidecar, then delete it**

```bash
cd gen && ../gen/.venv-audio/bin/python -c "
from common import *; from PIL import Image
p = ROOT/'gen/raw/TEST-00/x.png'; p.parent.mkdir(parents=True, exist_ok=True); Image.new('RGB',(512,512),'navy').save(p)
t = thumbnail_image(p,'TEST-00','TEST-00-run'); write_sidecar({'asset_id':'TEST-00','run_id':'TEST-00-run','model':'none','model_version':'0','license':'n/a','prompt':'p','negative_prompt':'','settings':{'seed':1},'raw_outputs':[rel(p)],'thumbnail':rel(t),'storyboard_panels':['P1']})"
../gen/.venv-audio/bin/python render_log.py && ../gen/.venv-audio/bin/python contact_sheet.py TEST-00 && grep -c TEST-00 ../ASSET-LOG.md
cd .. && rm -rf gen/log/TEST-00 gen/thumbs/TEST-00 gen/raw/TEST-00 gen/rejected/TEST-00-contact.png ASSET-LOG.md
```
Expected: grep count ≥ 2; files removed afterwards (the test sidecar must never be committed — it would predate nothing but pollutes the log).

- [ ] **Step 6: Commit**

```bash
git add gen/common.py gen/decide.py gen/render_log.py gen/contact_sheet.py
git commit -m "Add generation logging: sidecars, decisions, contact sheets, ASSET-LOG renderer

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 15: ART-PC-01 — generate, choose, palette-lock, palette check

**Files:** Create `gen/prompts/ART-PC-01.json`, `gen/art_generate.py`, `gen/art_process.py`, `gen/checks/palette_check.py`, `godot/assets/art/palettes.json`, `godot/assets/art/manifest.json`, `gen/mappings/ART-PC-01.json`; output `godot/assets/art/pc_sheet.png`, `design/character/pc_sheet_x8.png`

- [ ] **Step 1: Write palettes and manifest**

`godot/assets/art/palettes.json`:
```json
{
  "character": ["#F2B84B", "#FFF1C9", "#2E3A59", "#8A5A3C", "#14121C"],
  "environment": ["#0E1020", "#1F2540", "#3B4A6B", "#6E7FA3", "#C7D0E0", "#F2B84B", "#B5523B", "#14121C"]
}
```
`godot/assets/art/manifest.json` (sprite geometry for the palette check):
```json
{
  "pc_sheet.png": {"id": "ART-PC-01", "palette": "character", "frame": [32, 32], "frames": 12},
  "enemy_moth.png": {"id": "ART-EN-01", "palette": "environment", "frame": [24, 24], "frames": 2},
  "enemy_wraith.png": {"id": "ART-EN-02", "palette": "environment", "frame": [40, 40], "frames": 2},
  "env_ground_tile.png": {"id": "ART-ENV-01", "palette": "environment", "frame": [64, 64], "frames": 1},
  "env_stall.png": {"id": "ART-ENV-02", "palette": "environment", "frame": [64, 48], "frames": 1},
  "fx_beam.png": {"id": "ART-FX-01", "palette": "character", "frame": [16, 8], "frames": 1},
  "fx_orbit_moth.png": {"id": "ART-FX-02", "palette": "character", "frame": [12, 12], "frames": 1},
  "fx_sunflare.png": {"id": "ART-FX-03", "palette": "character", "frame": [128, 128], "frames": 1},
  "pickup_gem.png": {"id": "ART-PK-01", "palette": "character", "frame": [12, 12], "frames": 1}
}
```

- [ ] **Step 2: Write `gen/checks/palette_check.py`**

```python
#!/usr/bin/env python3
"""Check 4: shipped sprites use only their declared palette, binary alpha and exact frame geometry.

    python gen/checks/palette_check.py [--allow-missing]
"""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "godot" / "assets" / "art"


def rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main() -> int:
    allow_missing = "--allow-missing" in sys.argv
    manifest = json.loads((ART / "manifest.json").read_text())
    palettes = {k: {rgb(c) for c in v} for k, v in json.loads((ART / "palettes.json").read_text()).items()}
    results, ok_all = [], True
    for name, spec in manifest.items():
        path = ART / name
        r = {"file": name, "id": spec["id"]}
        if not path.exists():
            r["status"] = "MISSING"
            ok_all = ok_all and allow_missing
            results.append(r)
            continue
        im = Image.open(path).convert("RGBA")
        fw, fh = spec["frame"]
        want = (fw * spec["frames"], fh)
        pal = palettes[spec["palette"]]
        bad_alpha = sum(1 for p in im.getdata() if p[3] not in (0, 255))
        bad_color = sum(1 for p in im.getdata() if p[3] == 255 and p[:3] not in pal)
        opaque = sum(1 for p in im.getdata() if p[3] == 255)
        ok = im.size == want and bad_alpha == 0 and bad_color == 0 and opaque > 0
        ok_all = ok_all and ok
        r.update(status="PASS" if ok else "FAIL", size=list(im.size), want=list(want), bad_alpha=bad_alpha, bad_color=bad_color, opaque=opaque)
        results.append(r)
    (ROOT / "evidence").mkdir(exist_ok=True)
    (ROOT / "evidence" / "palette-check.json").write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        print(r["status"], r["id"], r["file"], {k: v for k, v in r.items() if k not in ("status", "id", "file")})
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
```

Run: `gen/.venv-art/bin/python gen/checks/palette_check.py --allow-missing` → all `MISSING`, exit 0. Without the flag → exit 1. (This is the failing test for this task.)

- [ ] **Step 3: Write `gen/prompts/ART-PC-01.json`**

```json
{
  "asset_id": "ART-PC-01",
  "storyboard_panels": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"],
  "width": 1536,
  "height": 1024,
  "steps": 4,
  "quantize": 4,
  "grid": "3x4",
  "prompt": "character model sheet of one small original courier character repeated in twelve poses, arranged in a neat grid of 3 rows and 4 columns on a plain flat white background, every pose the same character and the same size, full body, side view facing right unless noted. The character: an oversized round brass oil-lamp for a head with a glowing warm yellow glass lens, a narrow dark navy long coat, thin dark legs, a small brown leather satchel on the left hip. Style: simple flat vector shapes, thick uniform dark outline, no gradients, no texture, limited palette of warm yellow, cream, navy, brown and near-black, clean readable silhouette, video game sprite reference. Poses in reading order: front view standing; side view standing; back view standing; relaxed idle; walking with legs apart at contact; walking with legs together passing; arm thrust forward casting a beam of light; flinching backwards hurt; both arms raised cheering; radiant power pose with a large glow halo; collapsed lying on the ground with the lamp dimmed; triumphant victory pose. No text, no letters, no numbers, no labels, no watermark, no background scenery.",
  "negative_prompt": "N/A — FLUX.1-schnell is guidance-distilled and mflux does not accept a negative prompt for it; exclusions (text, labels, scenery, gradients) are written into the positive prompt."
}
```

- [ ] **Step 4: Write `gen/art_generate.py`**

```python
#!/usr/bin/env python3
"""Generate image candidates with FLUX.1-schnell (mflux, local) and log one sidecar per seed.

    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-PC-01.json --seeds 11 23 37 41 59 73
"""
import argparse, json, subprocess, time
from importlib.metadata import version
from pathlib import Path
from common import ROOT, new_run_id, rel, thumbnail_image, write_sidecar

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
ap.add_argument("--prompt-override", help="replace the prompt for a targeted re-generation (logged verbatim)")
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())
prompt = a.prompt_override or spec["prompt"]

for seed in a.seeds:
    run_id = new_run_id(spec["asset_id"], seed)
    out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["mflux-generate", "--model", "schnell", "--prompt", prompt, "--seed", str(seed),
           "--steps", str(spec.get("steps", 4)), "--width", str(spec["width"]), "--height", str(spec["height"]),
           "--quantize", str(spec.get("quantize", 4)), "--output", str(out)]
    t0 = time.time()
    subprocess.run(cmd, check=True, cwd=ROOT / "gen")
    thumb = thumbnail_image(out, spec["asset_id"], run_id)
    side = write_sidecar({
        "asset_id": spec["asset_id"], "run_id": run_id,
        "model": "black-forest-labs/FLUX.1-schnell", "model_version": f"mflux {version('mflux')}, {spec.get('quantize', 4)}-bit",
        "license": "Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction",
        "prompt": prompt, "negative_prompt": spec.get("negative_prompt", ""),
        "settings": {"seed": seed, "width": spec["width"], "height": spec["height"], "steps": spec.get("steps", 4),
                     "quantize": spec.get("quantize", 4), "seconds": round(time.time() - t0, 1)},
        "raw_outputs": [rel(out)], "thumbnail": rel(thumb), "storyboard_panels": spec["storyboard_panels"],
    })
    print(side)
```

- [ ] **Step 5: Generate six candidates**

Run: `cd gen && .venv-art/bin/python art_generate.py prompts/ART-PC-01.json --seeds 11 23 37 41 59 73 && .venv-art/bin/python contact_sheet.py ART-PC-01 && open ../gen/rejected/ART-PC-01-contact.png`
Expected: six sidecars, a contact sheet of six PENDING tiles.

- [ ] **Step 6: HUMAN — Bao picks.** Show the contact sheet and the full-size raws. For each run, Bao says accept / modify / reject and why; record each with `decide.py` (e.g. `gen/.venv-art/bin/python gen/decide.py ART-PC-01 <run> reject "lamp becomes a human face in 5 of 12 poses"`). If no single run has 10+ usable consistent poses, generate targeted single-pose runs with `--prompt-override` (same character description + one pose) and mix sources in the mapping below. Re-render the contact sheet.

- [ ] **Step 7: Write `gen/art_process.py`**

```python
#!/usr/bin/env python3
"""Cut frames out of accepted raws, fit them to game size, lock them to a palette and assemble a strip.

    python gen/art_process.py gen/mappings/ART-PC-01.json

Mapping file:
{
  "out": "godot/assets/art/pc_sheet.png", "preview": "design/character/pc_sheet_x8.png",
  "palette": "character", "frame": [32, 32], "fill": 0.95, "anchor": "bottom", "bg_threshold": 235, "outline": true,
  "frames": [{"name": "turn_front", "src": "gen/accepted/ART-PC-01/<run>.png", "grid": [3, 4], "cell": [0, 0]}, ...]
}
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cut(src: Image.Image, grid, cell, inset=0.02) -> Image.Image:
    rows, cols = grid
    r, c = cell
    cw, ch = src.width / cols, src.height / rows
    box = (int(c * cw + cw * inset), int(r * ch + ch * inset), int((c + 1) * cw - cw * inset), int((r + 1) * ch - ch * inset))
    return src.crop(box)


def key_background(im: Image.Image, threshold: int) -> Image.Image:
    a = np.array(im.convert("RGBA"))
    bg = (a[..., 0] > threshold) & (a[..., 1] > threshold) & (a[..., 2] > threshold)
    a[bg, 3] = 0
    return Image.fromarray(a)


def fit(im: Image.Image, fw: int, fh: int, fill: float, anchor: str) -> Image.Image:
    bbox = im.getbbox()
    if bbox is None:
        raise SystemExit("empty cell after background keying — wrong cell or threshold")
    im = im.crop(bbox)
    s = min(fw * fill / im.width, fh * fill / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    canvas = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    x = (fw - im.width) // 2
    y = fh - im.height if anchor == "bottom" else (fh - im.height) // 2
    canvas.alpha_composite(im, (x, y))
    return canvas


def lock_palette(im: Image.Image, palette, outline_rgb=None) -> Image.Image:
    a = np.array(im).astype(np.int32)
    pal = np.array(palette)
    opaque = a[..., 3] >= 128
    d = ((a[..., None, :3] - pal[None, None, :, :]) ** 2).sum(-1)
    nearest = pal[d.argmin(-1)]
    out = np.zeros_like(a)
    out[opaque, :3] = nearest[opaque]
    out[opaque, 3] = 255
    if outline_rgb is not None:
        o = opaque
        edge = np.zeros_like(o)
        edge[1:, :] |= o[:-1, :]; edge[:-1, :] |= o[1:, :]; edge[:, 1:] |= o[:, :-1]; edge[:, :-1] |= o[:, 1:]
        ring = edge & ~o
        out[ring, :3] = outline_rgb
        out[ring, 3] = 255
    return Image.fromarray(out.astype(np.uint8))


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    palettes = json.loads((ROOT / "godot/assets/art/palettes.json").read_text())
    palette = [rgb(c) for c in palettes[spec["palette"]]]
    fw, fh = spec["frame"]
    frames = []
    for f in spec["frames"]:
        src = Image.open(ROOT / f["src"]).convert("RGBA")
        cell = cut(src, f.get("grid", [1, 1]), f.get("cell", [0, 0])) if "grid" in f else src
        cell = key_background(cell, spec.get("bg_threshold", 235))
        cell = fit(cell, fw, fh, spec.get("fill", 0.95), spec.get("anchor", "bottom"))
        if f.get("mirror"):
            cell = cell.transpose(Image.FLIP_LEFT_RIGHT)
        frames.append(lock_palette(cell, palette, rgb("#14121C") if spec.get("outline") else None))
    strip = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip.paste(fr, (i * fw, 0))
    out = ROOT / spec["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out)
    if spec.get("preview"):
        prev = ROOT / spec["preview"]
        prev.parent.mkdir(parents=True, exist_ok=True)
        strip.resize((strip.width * 8, strip.height * 8), Image.NEAREST).save(prev)
    print(f"{out.relative_to(ROOT)}: {len(frames)} frames")


if __name__ == "__main__":
    main()
```

(`mirror` exists only to correct a source cell that faces left so every stored frame faces right; it never creates a new pose — log any use as a manual edit.)

- [ ] **Step 8: Write `gen/mappings/ART-PC-01.json`** — 12 entries in the canonical pose order, pointing at the accepted raw(s) and the chosen cells Bao confirmed. Run:

```bash
gen/.venv-art/bin/python gen/art_process.py gen/mappings/ART-PC-01.json && open design/character/pc_sheet_x8.png
gen/.venv-art/bin/python gen/checks/palette_check.py --allow-missing
```
Expected: `pc_sheet.png: 12 frames`; `PASS ART-PC-01`.

- [ ] **Step 9: HUMAN — consistency review against CHARACTER-SHEET rules** (lamp size, satchel side, feet row, torso centre). Hand-fix pixels in an editor if needed; record every hand edit in `decide.py --edits`. Rerun the palette check after edits.

- [ ] **Step 10: Import, view in game, commit**

```bash
cd godot && $GODOT --headless --path . --import --quit && cd ..
gen/.venv-art/bin/python gen/render_log.py
git add gen/prompts gen/art_generate.py gen/art_process.py gen/checks gen/mappings gen/log gen/thumbs gen/accepted gen/rejected godot/assets/art design/character/pc_sheet_x8.png ASSET-LOG.md evidence/palette-check.json
git commit -m "Generate ART-PC-01 courier sheet (FLUX.1-schnell), palette-locked to 12 frames

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 16: Enemies, environment, FX, pickup art

**Files:** Create `gen/prompts/{ART-EN-01,ART-EN-02,ART-ENV-01,ART-ENV-02,ART-FX-01,ART-FX-02,ART-FX-03,ART-PK-01}.json`, `gen/tile_process.py`, `gen/mappings/<id>.json`; outputs in `godot/assets/art/`

- [ ] **Step 1: Write the eight prompt specs.** Each uses the same JSON shape as ART-PC-01. Prompts (all end with "plain flat white background, simple flat vector shapes, thick uniform dark outline, no gradients, no text, no letters, no watermark"):
  - ART-EN-01 (1024×512, grid 1×2, panels P2 P3 P6): "two animation frames side by side of one small pale grey-blue night moth seen from above, wings up in the left frame and wings down in the right frame, soft misty colours"
  - ART-EN-02 (1024×512, grid 1×2, P5): "two animation frames side by side of one hooded ghostly fog wraith made of dark blue mist with two faint pale eye-dots, drifting pose, frame two slightly stretched"
  - ART-ENV-01 (1024×1024, P2 P3 P8): "top-down seamless tileable texture of old rounded cobblestones at night, cool dark blue and grey stones, thin dark gaps, even lighting, no objects" — *no* outline clause for this one.
  - ART-ENV-02 (1024×768, P1 P2): "a small wooden night-market stall seen from a high three-quarter angle, red cloth awning, one glowing paper lantern hanging at the front, crates underneath"
  - ART-FX-01 (1024×512, P3): "a short horizontal bolt of warm cream and golden light pointing right, soft rounded tip"
  - ART-FX-02 (512×512, P4 P6): "a tiny round glowing lamp-moth made of warm golden light seen from above, wings spread"
  - ART-FX-03 (1024×1024, P6): "a radial burst of golden sunlight rays forming a ring, bright cream centre, symmetrical, seen from above"
  - ART-PK-01 (512×512, P3): "a single small faceted golden oil drop gem with a cream highlight, seen from above"

- [ ] **Step 2: Write `gen/tile_process.py`**

```python
#!/usr/bin/env python3
"""Make ART-ENV-01 seamless, downscale to 64x64, lock to the environment palette, and measure the seam.

    python gen/tile_process.py gen/accepted/ART-ENV-01/<run>.png
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from art_process import lock_palette, rgb

ROOT = Path(__file__).resolve().parents[1]
src = Image.open(sys.argv[1]).convert("RGB")
side = min(src.size)
src = src.crop(((src.width - side) // 2, (src.height - side) // 2, (src.width + side) // 2, (src.height + side) // 2))
a = np.asarray(src).astype(np.float32)
rolled = np.roll(np.roll(a, side // 2, 0), side // 2, 1)
yy, xx = np.mgrid[0:side, 0:side] / (side - 1)
w = (np.sin(np.pi * yy) * np.sin(np.pi * xx))[..., None]
tile = (a * w + rolled * (1 - w)).clip(0, 255).astype(np.uint8)
small = Image.fromarray(tile).resize((64, 64), Image.LANCZOS).convert("RGBA")
palette = [rgb(c) for c in json.loads((ROOT / "godot/assets/art/palettes.json").read_text())["environment"]]
locked = lock_palette(small, palette)
out = ROOT / "godot/assets/art/env_ground_tile.png"
locked.save(out)
t = np.asarray(locked).astype(np.int32)[..., :3]
seam = float(np.abs(t[:, 0] - t[:, -1]).mean() + np.abs(t[0] - t[-1]).mean()) / 2
interior = float(np.abs(np.diff(t, axis=1)).mean() + np.abs(np.diff(t, axis=0)).mean()) / 2
report = {"seam_mean_abs": round(seam, 2), "interior_mean_abs": round(interior, 2), "pass": seam <= interior * 1.25}
(ROOT / "evidence" / "tile-seam.json").write_text(json.dumps(report, indent=2) + "\n")
Image.fromarray(np.tile(np.asarray(locked), (3, 3, 1))).resize((576, 576), Image.NEAREST).save(ROOT / "evidence" / "tile-3x3-preview.png")
print(report)
```

- [ ] **Step 3: Generate 3–4 seeds per asset, contact sheets, HUMAN picks** (same loop as Task 15 Steps 5–6), for each of the eight assets.
- [ ] **Step 4: Process.** ENV-01 via `tile_process.py` (expect `"pass": true`; if false, reject or regenerate and log). All others via `art_process.py` with mappings: EN-01 frame `[24,24]` 2 frames `anchor: center`, EN-02 `[40,40]` 2 frames, ENV-02 `[64,48]`, FX-01 `[16,8]`, FX-02 `[12,12]`, FX-03 `[128,128]` (`outline: false`), PK-01 `[12,12]`; palettes per `manifest.json`.
- [ ] **Step 5: Readability check (prediction 4).** In `gen/checks/palette_check.py` add `import numpy as np`, this helper above `main()`:

```python
def luminance(path: Path) -> float:
    a = np.asarray(Image.open(path).convert("RGBA")).astype(float) / 255
    opaque = a[..., 3] > 0.5
    lin = np.where(a[..., :3] <= 0.04045, a[..., :3] / 12.92, ((a[..., :3] + 0.055) / 1.055) ** 2.4)
    return float((lin[opaque] @ np.array([0.2126, 0.7152, 0.0722])).mean())
```

and, right before the evidence file is written in `main()`:

```python
    ground = ART / "env_ground_tile.png"
    if ground.exists():
        g = luminance(ground)
        for name, need in (("enemy_moth.png", 0.25), ("enemy_wraith.png", None)):
            if (ART / name).exists():
                diff = abs(luminance(ART / name) - g)
                ok = need is None or diff >= need
                ok_all = ok_all and ok
                results.append({"file": name, "id": "contrast-vs-ground", "status": "PASS" if ok else "FAIL",
                                "luminance_diff": round(diff, 3), "required": need})
```

The wraith is recorded but not gated: it may be low-contrast *only* if Bao accepts it after the muted playtest (log that decision). Run: `gen/.venv-art/bin/python gen/checks/palette_check.py` → all `PASS`, exit 0.
- [ ] **Step 6: Import, eyeball in game, render log, commit**

```bash
cd godot && $GODOT --headless --path . --import --quit && $GODOT --path . ; cd ..
gen/.venv-art/bin/python gen/render_log.py
git add gen godot/assets/art ASSET-LOG.md evidence
git commit -m "Generate enemy, environment, FX and pickup art; seamless tile and contrast checks

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 17: SFX-01…06b — Stable Audio Open

**Files:** Create `gen/prompts/SFX-*.json` (7), `gen/sfx_generate.py`, `gen/sfx_process.py`; outputs `godot/assets/sfx/*.wav`

- [ ] **Step 1: Write the seven prompt specs** (`asset_id, storyboard_panels, duration_s, steps: 100, cfg: 7.0, prompt, negative_prompt, out`). Shared negative: `"music, melody, voice, speech, singing, crowd, reverb tail, noise hiss, distortion, clipping, low quality"`.
  - SFX-01 kill (0.5 s, P3, out `sfx_01_kill.wav`): "a single soft glassy pop of a small moth bursting into sparks, short, warm, dry, video game sound effect"
  - SFX-02 pickup (0.4 s, P3): "a single tiny bright bell-like chime of picking up a drop of oil, short, soft attack, video game sound effect"
  - SFX-03 hurt (0.6 s, P5): "a single dull muffled thud with a low glass rattle, being hit, short, no voice, video game sound effect"
  - SFX-04 levelup (1.5 s, P4): "a short rising warm three-note chime arpeggio made of glass bells, uplifting, video game level up sound"
  - SFX-05 evolve (3.0 s, P6): "a swelling whoosh of warm light building into a bright shimmering burst, magical, video game power up"
  - SFX-06a lose (3.0 s, P7): "a lamp flame guttering out, soft descending glassy tones fading to silence, sad, gentle"
  - SFX-06b win (4.0 s, P9): "a gentle warm triumphant flourish of glass bells and soft chimes, fog clearing, calm resolution"

- [ ] **Step 2: Write `gen/sfx_generate.py`**

```python
#!/usr/bin/env python3
"""Generate SFX candidates with Stable Audio Open 1.0 (local) and log a sidecar per seed.

    gen/.venv-audio/bin/python gen/sfx_generate.py gen/prompts/SFX-01.json --seeds 1 2 3 4
"""
import argparse, json, time
from pathlib import Path
import soundfile as sf
import torch
import diffusers
from diffusers import StableAudioPipeline
from huggingface_hub import snapshot_download
from common import ROOT, new_run_id, rel, thumbnail_audio, write_sidecar

REPO = "stabilityai/stable-audio-open-1.0"
ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())
revision = Path(snapshot_download(REPO, local_files_only=True)).name
device = "mps" if torch.backends.mps.is_available() else "cpu"
pipe = StableAudioPipeline.from_pretrained(REPO, torch_dtype=torch.float32).to(device)
sr = pipe.vae.sampling_rate

for seed in a.seeds:
    run_id = new_run_id(spec["asset_id"], seed)
    out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    g = torch.Generator("cpu").manual_seed(seed)
    audio = pipe(spec["prompt"], negative_prompt=spec["negative_prompt"], num_inference_steps=spec.get("steps", 100),
                 guidance_scale=spec.get("cfg", 7.0), audio_end_in_s=spec["duration_s"], generator=g).audios[0]
    sf.write(out, audio.T.float().cpu().numpy(), sr)
    thumb = thumbnail_audio(out, spec["asset_id"], run_id)
    print(write_sidecar({
        "asset_id": spec["asset_id"], "run_id": run_id,
        "model": REPO, "model_version": f"snapshot {revision}, diffusers {diffusers.__version__}",
        "license": "Stability AI Community License (free for non-commercial and < $1M revenue use; outputs owned by the user)",
        "prompt": spec["prompt"], "negative_prompt": spec["negative_prompt"],
        "settings": {"seed": seed, "duration_s": spec["duration_s"], "steps": spec.get("steps", 100), "cfg": spec.get("cfg", 7.0),
                     "sample_rate": sr, "device": device, "seconds": round(time.time() - t0, 1)},
        "raw_outputs": [rel(out)], "thumbnail": rel(thumb), "storyboard_panels": spec["storyboard_panels"],
    }))
```

- [ ] **Step 3: Write `gen/sfx_process.py`**

```python
#!/usr/bin/env python3
"""Trim, fade, mono, peak-normalise an accepted SFX to 44.1 kHz 16-bit WAV.

    python gen/sfx_process.py gen/accepted/SFX-01/<run>.wav godot/assets/sfx/sfx_01_kill.wav --max-s 0.35
"""
import argparse, json
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--max-s", type=float, required=True)
ap.add_argument("--top-db", type=float, default=40)
ap.add_argument("--peak-db", type=float, default=-1.0)
a = ap.parse_args()
y, sr = librosa.load(a.src, sr=44100, mono=True)
y, _ = librosa.effects.trim(y, top_db=a.top_db)
y = y[: int(a.max_s * sr)]
fi, fo = int(0.004 * sr), min(int(0.03 * sr), len(y) // 3)
y[:fi] *= np.linspace(0, 1, fi)
y[-fo:] *= np.linspace(1, 0, fo)
y *= 10 ** (a.peak_db / 20) / max(1e-9, np.abs(y).max())
Path(a.dst).parent.mkdir(parents=True, exist_ok=True)
sf.write(a.dst, y, sr, subtype="PCM_16")
print(json.dumps({"dst": a.dst, "seconds": round(len(y) / sr, 3), "peak_db": a.peak_db}))
```

- [ ] **Step 4: Generate 4 seeds per SFX, HUMAN listens and picks** (`afplay gen/raw/SFX-01/<run>.wav`), record decisions. Rejected raws: keep as thumbnails; copy rejected WAVs ≤ 1 MB into `gen/rejected/<id>/` so they can be heard later.
- [ ] **Step 5: Process accepted runs** with `--max-s` equal to the CHANGE-BRIEF limits (0.35, 0.3, 0.5, 1.2, 2.5, 3.0, 4.0). Add each final path to `godot/assets/manifest.json` (Task 19 builds it fully).
- [ ] **Step 6: Import and run the audio suite with real streams**

```bash
cd godot && $GODOT --headless --path . --import --quit && $GODOT --headless --path . --script res://tests/test_audio.gd; cd ..
```
Expected: `audio: 21 checks, 0 failures` — now `independence` compares real streams vs silent.

- [ ] **Step 7: Render log, commit**

```bash
gen/.venv-audio/bin/python gen/render_log.py
git add gen godot/assets/sfx ASSET-LOG.md evidence
git commit -m "Generate six SFX events with Stable Audio Open; trimmed WAVs wired to AudioBus

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 18: MUS-01 loop and MUS-02 layer — MusicGen, loop processing, seam check

**Files:** Create `gen/prompts/MUS-01.json`, `gen/prompts/MUS-02.json`, `gen/music_generate.py`, `gen/music_loop.py`, `gen/checks/loop_check.py`; outputs `godot/assets/music/*.ogg`

- [ ] **Step 1: Write the failing loop check `gen/checks/loop_check.py`**

```python
#!/usr/bin/env python3
"""Check 5: music loops have no click and no silent gap at the wrap point; layers share length.

    python gen/checks/loop_check.py godot/assets/music/mus_01_night_market.ogg [godot/assets/music/mus_02_sunflare_layer.ogg]
"""
import json, sys
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]


def analyse(path: str) -> dict:
    y, sr = sf.read(path, always_2d=True)
    m = y.mean(axis=1)
    d = np.abs(np.diff(m))
    p99 = float(np.percentile(d, 99))
    jump = float(abs(m[0] - m[-1]))
    win = int(0.05 * sr)
    rms = lambda s: float(np.sqrt(np.mean(s ** 2)) + 1e-12)
    overall, head, tail = rms(m), rms(m[:win]), rms(m[-win:])
    ok = jump <= p99 and head >= 0.25 * overall and tail >= 0.25 * overall
    return {"file": path, "frames": int(len(m)), "sr": int(sr), "seconds": round(len(m) / sr, 3), "wrap_jump": round(jump, 5),
            "p99_step": round(p99, 5), "head_rms_ratio": round(head / overall, 3), "tail_rms_ratio": round(tail / overall, 3),
            "status": "PASS" if ok else "FAIL"}


results = [analyse(p) for p in sys.argv[1:]]
if len(results) == 2:
    same = results[0]["frames"] == results[1]["frames"]
    results.append({"check": "layer-length-match", "status": "PASS" if same else "FAIL",
                    "frames": [results[0]["frames"], results[1]["frames"]]})
(ROOT / "evidence").mkdir(exist_ok=True)
(ROOT / "evidence" / "loop-check.json").write_text(json.dumps(results, indent=2) + "\n")
for r in results:
    print(r)
sys.exit(0 if all(r["status"] == "PASS" for r in results) else 1)
```

Run it on a deliberately bad file to see it fail:
```bash
gen/.venv-audio/bin/python -c "import numpy as np, soundfile as sf; t=np.arange(44100*2)/44100; sf.write('/tmp/bad.ogg', np.r_[np.sin(2*np.pi*220*t)*0.5, np.zeros(22050)], 44100, format='OGG', subtype='VORBIS')"
gen/.venv-audio/bin/python gen/checks/loop_check.py /tmp/bad.ogg
```
Expected: `FAIL` (tail RMS ratio ≈ 0), exit 1.

- [ ] **Step 2: Write prompt specs**

`gen/prompts/MUS-01.json`:
```json
{
  "asset_id": "MUS-01",
  "storyboard_panels": ["P2", "P3", "P4", "P5", "P7", "P8"],
  "model": "facebook/musicgen-medium",
  "duration_s": 30,
  "guidance_scale": 3.0,
  "prompt": "instrumental loop for a cozy but tense night market video game, 96 bpm, steady soft hand percussion, plucked kalimba and warm glassy mallets, low upright bass, mysterious minor key, even dynamics from start to end, no intro, no ending, no vocals",
  "negative_prompt": "N/A — MusicGen has no negative prompt; exclusions (vocals, intro, ending) are in the positive prompt."
}
```
`gen/prompts/MUS-02.json`: same shape, `"model": "facebook/musicgen-melody"`, `"condition_on": "godot/assets/music/mus_01_night_market.ogg"`, panels `["P6"]`, prompt: "bright energetic layer to play on top of a night market loop, 96 bpm, shimmering bells, driving shaker and tambourine, rising synth pad, same key, even dynamics, no intro, no ending, no vocals".

- [ ] **Step 3: Write `gen/music_generate.py`**

```python
#!/usr/bin/env python3
"""Generate music candidates with MusicGen (local, transformers) and log a sidecar per seed.

    gen/.venv-audio/bin/python gen/music_generate.py gen/prompts/MUS-01.json --seeds 5 8 13 21
"""
import argparse, json, time
from pathlib import Path
import librosa
import soundfile as sf
import torch
import transformers
from huggingface_hub import snapshot_download
from transformers import AutoProcessor, MusicgenForConditionalGeneration, MusicgenMelodyForConditionalGeneration
from common import ROOT, new_run_id, rel, thumbnail_audio, write_sidecar

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())
repo = spec["model"]
melody = "melody" in repo
revision = Path(snapshot_download(repo, local_files_only=True)).name
proc = AutoProcessor.from_pretrained(repo)
model = (MusicgenMelodyForConditionalGeneration if melody else MusicgenForConditionalGeneration).from_pretrained(repo)
sr = model.config.audio_encoder.sampling_rate
tokens = int(spec["duration_s"] * model.config.audio_encoder.frame_rate)

for seed in a.seeds:
    run_id = new_run_id(spec["asset_id"], seed)
    out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(seed)
    kwargs = {"text": [spec["prompt"]], "padding": True, "return_tensors": "pt"}
    if melody:
        cond, _ = librosa.load(ROOT / spec["condition_on"], sr=proc.feature_extractor.sampling_rate, mono=True)
        kwargs.update(audio=cond, sampling_rate=proc.feature_extractor.sampling_rate)
    inputs = proc(**kwargs)
    t0 = time.time()
    audio = model.generate(**inputs, do_sample=True, guidance_scale=spec.get("guidance_scale", 3.0), max_new_tokens=tokens)
    sf.write(out, audio[0, 0].cpu().numpy(), sr)
    thumb = thumbnail_audio(out, spec["asset_id"], run_id)
    print(write_sidecar({
        "asset_id": spec["asset_id"], "run_id": run_id,
        "model": repo, "model_version": f"snapshot {revision}, transformers {transformers.__version__}",
        "license": "MusicGen weights CC-BY-NC-4.0 (non-commercial coursework use); AudioCraft code MIT",
        "prompt": spec["prompt"], "negative_prompt": spec["negative_prompt"],
        "settings": {"seed": seed, "duration_s": spec["duration_s"], "max_new_tokens": tokens, "guidance_scale": spec.get("guidance_scale", 3.0),
                     "sample_rate": sr, "condition_on": spec.get("condition_on"), "seconds": round(time.time() - t0, 1)},
        "raw_outputs": [rel(out)], "thumbnail": rel(thumb), "storyboard_panels": spec["storyboard_panels"],
    }))
```

- [ ] **Step 4: Write `gen/music_loop.py`**

```python
#!/usr/bin/env python3
"""Cut a bar-aligned segment and crossfade its tail into its head so the file loops seamlessly; write OGG Vorbis.

    python gen/music_loop.py SRC.wav DST.ogg --bars 8 [--skip-s 1.0] [--xfade-s 0.25]
    python gen/music_loop.py SRC.wav DST.ogg --match-frames REF.ogg   # stretch a layer to the base loop length

At the wrap the player goes out[L-1] -> out[0]. out[0] = seg[L] (the natural continuation of seg[L-1]) fading into seg[0],
so both sides of the seam are continuous.
"""
import argparse, json
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--bars", type=int, default=8)
ap.add_argument("--beats-per-bar", type=int, default=4)
ap.add_argument("--skip-s", type=float, default=1.0)
ap.add_argument("--xfade-s", type=float, default=0.25)
ap.add_argument("--match-frames")
a = ap.parse_args()
SR = 44100
y, _ = librosa.load(a.src, sr=SR, mono=True)
xf = int(a.xfade_s * SR)

if a.match_frames:
    L = sf.info(a.match_frames).frames
    rate = len(y) / (L + xf)
    y = librosa.effects.time_stretch(y, rate=rate)
    y = np.pad(y, (0, max(0, L + xf - len(y))))[: L + xf]
    start, bpm = 0, None
else:
    tempo, beats = librosa.beat.beat_track(y=y, sr=SR, units="samples")
    bpm = float(np.atleast_1d(tempo)[0])
    beats = beats[beats >= int(a.skip_s * SR)]
    n = a.bars * a.beats_per_bar
    if len(beats) <= n:
        raise SystemExit(f"only {len(beats)} beats after skip; use fewer bars")
    start, end = int(beats[0]), int(beats[n])
    L = end - start
    if start + L + xf > len(y):
        raise SystemExit("not enough audio after the loop end for the crossfade; use fewer bars")
seg = y[start: start + L + xf].copy()
out = seg[:L].copy()
t = np.linspace(0, np.pi / 2, xf)
out[:xf] = seg[:xf] * np.sin(t) + seg[L:L + xf] * np.cos(t)
out *= 10 ** (-3 / 20) / max(1e-9, np.abs(out).max())
Path(a.dst).parent.mkdir(parents=True, exist_ok=True)
sf.write(a.dst, out, SR, format="OGG", subtype="VORBIS")
print(json.dumps({"dst": a.dst, "bpm": bpm, "start_sample": start, "loop_frames": int(L), "seconds": round(L / SR, 3), "xfade_s": a.xfade_s}))
```

- [ ] **Step 5: Generate MUS-01 (4 seeds), HUMAN picks the steadiest**, then:

```bash
gen/.venv-audio/bin/python gen/music_loop.py gen/accepted/MUS-01/<run>.wav godot/assets/music/mus_01_night_market.ogg --bars 12
gen/.venv-audio/bin/python gen/checks/loop_check.py godot/assets/music/mus_01_night_market.ogg
```
Expected: `PASS`. If `FAIL`: try `--bars 8`, `--skip-s 2`, or `--xfade-s 0.5`; log each attempt as a modify edit (this is a ready-made "observe → change loop point → re-verify" loop for TEST-REPORT).

- [ ] **Step 6: HUMAN loop listen.** Bao plays the loop 5× in a looping player (`gen/.venv-audio/bin/python -c "import soundfile as sf, numpy as np; y,sr=sf.read('godot/assets/music/mus_01_night_market.ogg'); sf.write('/tmp/x5.wav', np.tile(y,(5,1)) if y.ndim>1 else np.tile(y,5), sr)" && afplay /tmp/x5.wav`) and says whether a click/gap/tempo jump is audible. Record the answer.

- [ ] **Step 7: Generate MUS-02 (melody-conditioned on the processed MUS-01), HUMAN picks**, then:

```bash
gen/.venv-audio/bin/python gen/music_loop.py gen/accepted/MUS-02/<run>.wav godot/assets/music/mus_02_sunflare_layer.ogg --match-frames godot/assets/music/mus_01_night_market.ogg
gen/.venv-audio/bin/python gen/checks/loop_check.py godot/assets/music/mus_01_night_market.ogg godot/assets/music/mus_02_sunflare_layer.ogg
```
Expected: three `PASS` lines including `layer-length-match`. If the layer drifts audibly against the base (prediction 5), apply the fallback: delete MUS-02, add a CHANGE-BRIEF Revision, and in `audio_bus.gd::_on_evolved` raise the Music low-pass-free volume +2 dB instead; rerun `test_audio.gd`.

- [ ] **Step 8: Import, test, log, commit**

```bash
cd godot && $GODOT --headless --path . --import --quit && $GODOT --headless --path . --script res://tests/test_audio.gd; cd ..
gen/.venv-audio/bin/python gen/render_log.py
git add gen godot/assets/music ASSET-LOG.md evidence
git commit -m "Generate MUS-01 night-market loop and MUS-02 layer with MusicGen; seamless loop check

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
Expected test output includes `PASS music-loop-flag` with a non-null stream.

### Task 19: Integration — asset manifest, full audit, sheet-vs-game evidence

**Files:** Create `godot/assets/manifest.json`, `godot/tests/capture.gd`; Modify `CHARACTER-SHEET.md`, `STORYBOARD.md` (Revisions only)

- [ ] **Step 1: Write `godot/assets/manifest.json`** (every CHANGE-BRIEF ID → repo-relative files; drop MUS-02 only if the Task 18 fallback was taken and recorded as a Revision):

```json
{
  "ART-PC-01": ["godot/assets/art/pc_sheet.png"],
  "ART-EN-01": ["godot/assets/art/enemy_moth.png"],
  "ART-EN-02": ["godot/assets/art/enemy_wraith.png"],
  "ART-ENV-01": ["godot/assets/art/env_ground_tile.png"],
  "ART-ENV-02": ["godot/assets/art/env_stall.png"],
  "ART-FX-01": ["godot/assets/art/fx_beam.png"],
  "ART-FX-02": ["godot/assets/art/fx_orbit_moth.png"],
  "ART-FX-03": ["godot/assets/art/fx_sunflare.png"],
  "ART-PK-01": ["godot/assets/art/pickup_gem.png"],
  "SFX-01": ["godot/assets/sfx/sfx_01_kill.wav"],
  "SFX-02": ["godot/assets/sfx/sfx_02_pickup.wav"],
  "SFX-03": ["godot/assets/sfx/sfx_03_hurt.wav"],
  "SFX-04": ["godot/assets/sfx/sfx_04_levelup.wav"],
  "SFX-05": ["godot/assets/sfx/sfx_05_evolve.wav"],
  "SFX-06a": ["godot/assets/sfx/sfx_06a_lose.wav"],
  "SFX-06b": ["godot/assets/sfx/sfx_06b_win.wav"],
  "MUS-01": ["godot/assets/music/mus_01_night_market.ogg"],
  "MUS-02": ["godot/assets/music/mus_02_sunflare_layer.ogg"]
}
```

- [ ] **Step 2: Run the final audit (expected to fail until everything is present)**

Run: `python3 scripts/audit_repo.py --stage final`
Expected: `0 problem(s)`; the JSON lists `design_v1_committed` and `first_generation_commit`. Fix any missing ID/file it reports.

- [ ] **Step 3: Write `godot/tests/capture.gd`** — a windowed (not headless) script that starts a seeded run, forces each of the 12 poses via `player.set_override(pose)`, and saves `evidence/screens/pose-<name>.png` from `root.get_texture().get_image()` after two process frames; then captures P2, P3 (after 40 ticks with a moth spawned in front), P4 (level-up), P5 (hurt), P6 (evolved + ring), P7 (lost), P9 (won) as `evidence/screens/sb-P<n>.png`.

```gdscript
extends SceneTree
const Session = preload("res://game/session.gd")
const Tuning = preload("res://features/tuning.gd")
var game

func _initialize() -> void:
	call_deferred("_main")

func shot(name: String) -> void:
	await process_frame
	await process_frame
	var dir := ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(dir)
	root.get_texture().get_image().save_png("%s/%s.png" % [dir, name])
	print("saved ", name)

func _main() -> void:
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	game.start_run(21)
	for p in game.player.POSES:
		game.player.set_override(p)
		await shot("pose-" + p)
	game.player.set_override("")
	await shot("sb-P2")
	game.spawn_enemy("moth", Vector2(90, 0))
	game.test_axis = Vector2.RIGHT
	game.step_ticks(20)
	await shot("sb-P3")
	game.prog.add_xp(3)
	game.tick()
	await shot("sb-P4")
	game.choose_card(0)
	var w = game.spawn_enemy("wraith", game.player.position + Vector2(8, 0))
	w.hp = 9999
	game.tick()
	await shot("sb-P5")
	w.queue_free(); game.enemies.erase(w)
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(game.prog.xp_needed())
	game.tick()
	game.choose_card(game.offered.find("sunflare"))
	for i in 12:
		game.spawn_enemy("moth", Vector2.from_angle(i * TAU / 12) * 150)
	game.step_ticks(Tuning.SUNFLARE_FIRST_DELAY + 8)
	await shot("sb-P6")
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.step_ticks(60)
	await shot("sb-P7")
	game.start_run(22)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	await shot("sb-P9")
	quit()
```

Run: `cd godot && $GODOT --path . --script res://tests/capture.gd; cd ..`
Expected: 12 `pose-*.png` + 7 `sb-P*.png` in `evidence/screens/`.

- [ ] **Step 4: Append Revisions** — `CHARACTER-SHEET.md`: side-by-side table (blockout pose ×8 | generated frame ×8 | in-game screenshot) for all 12 poses, plus the generated silhouette strip, and a list of rules that held / broke. `STORYBOARD.md`: table (panel | in-game capture | what differs and why). Dated, under `## Revisions`, originals untouched.

- [ ] **Step 5: Run every check once more**

```bash
cd godot && for s in logic gameplay audio; do $GODOT --headless --path . --script res://tests/test_$s.gd || exit 1; done; cd ..
gen/.venv-art/bin/python gen/checks/palette_check.py && gen/.venv-audio/bin/python gen/checks/loop_check.py godot/assets/music/*.ogg && python3 scripts/audit_repo.py --stage final
```
Expected: all exit 0.

- [ ] **Step 6: Commit**

```bash
git add godot evidence CHARACTER-SHEET.md STORYBOARD.md
git commit -m "Integrate all generated assets; manifest, final audit and sheet/storyboard-vs-game captures

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

# Phase D — Human verification, reports, film, submission

### Task 20: HUMAN playtests + revision loop → `TEST-REPORT.md`

**Files:** Create `TEST-REPORT.md`, `evidence/playtest/` notes/screens

- [ ] **Step 1: Fresh-copy run.** `git clone <remote> /tmp/lf-fresh && cd /tmp/lf-fresh/godot && $GODOT --headless --path . --import --quit && $GODOT --path .` — record whether it runs with all assets.
- [ ] **Step 2: Give Bao a playtest sheet** (in `evidence/playtest/sheet.md`) with checkboxes for: movement & facing; each pose seen; each of the 6 SFX heard exactly once per event; rapid tapping and long-holding produce no repeats; music loop point (listen at ~0:36/1:12); pause → muffled & quieter; level-up duck; lose fade + stinger; win fade + stinger; restart during fade; M/9/0.
- [ ] **Step 3: HUMAN — Playtest A, sound on, full run.** Bao plays and fills the sheet in person; Claude records nothing on Bao's behalf.
- [ ] **Step 4: HUMAN — Playtest B, press M at the menu, full run muted.** Bao notes anything that could not be understood without sound.
- [ ] **Step 5: Revision loop (≥ 1).** Take one concrete observation (e.g. wraith hard to see when muted, kill SFX harsh, loop click). Make the change (asset regen / prompt edit / loop point / palette), log it via `decide.py` or a CHANGE-BRIEF Revision, rerun the relevant check, and have Bao re-verify by playing. Capture before/after evidence.
- [ ] **Step 6: Write `TEST-REPORT.md`** with sections: environment; fresh-copy result; automated checks table (suite, checks, failures, evidence file) for logic/gameplay/audio/palette/loop/tile/repo-audit; playtest A; playtest B; character sheet vs game (link Task 19 table); storyboard vs game; SFX once-per-event table (from `evidence/audio.json` + Bao's ears); rapid/hold input; music seam; pause/end behaviour; muted comprehension; the revision loop(s) as *observation → change → re-verification*; predictions from CHANGE-BRIEF scored right/wrong; open questions.
- [ ] **Step 7: Commit**

```bash
git add TEST-REPORT.md evidence && git commit -m "Add TEST-REPORT with both playtests and the revision loop

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 21: `FRICTIONAL.md`, `SOURCES.md`, `README.md`

- [ ] **Step 1: `FRICTIONAL.md` — HUMAN content.** Claude writes only the section headings (what I intended; where it fought back; decisions I changed and why; what Claude did vs what I did; what I'd do differently) and a dated timeline pulled from `git log`. Bao writes the prose in his own words.
- [ ] **Step 2: `SOURCES.md`** — starter attribution (blank project; character from A1 ← nikbearbrown/walker-jumpman); each model with repo id, snapshot revision, licence, and which asset IDs it made; tools (Godot 4.7.2, mflux, diffusers, transformers, librosa, soundfile, Pillow, uv); Godot fallback font; statement that no living artist, brand, copyrighted character, existing recording or voice was used; link to ASSET-LOG.
- [ ] **Step 3: `README.md`** — project name; started from + attribution; Godot version; run (`./walker-lanternfall.command` or `godot --path godot`); tests (the Task 19 Step 5 block); controls incl. M/9/0/F3 and gamepad; what the slice proves; known limitations; film filename, link, SHA-256 (filled in Task 22); read-order list of all docs.
- [ ] **Step 4: Commit**

```bash
git add FRICTIONAL.md SOURCES.md README.md && git commit -m "Add FRICTIONAL, SOURCES and README

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 22: Film — `godot-gamedev` + walker modifier

- [ ] **Step 1: Record the demonstrated source revision:** `git rev-parse HEAD` → `FILM_SHA`.
- [ ] **Step 2: Invoke the `godot-gamedev` skill with the walker modifier** (not `godot-waikthrough`). Hand it this coverage contract; the skill owns its own phases and gates:
  1. concept + pillars; 2. one asset traced end-to-end: ART-PC-01 blockout → prompt → raw → contact sheet decision → palette lock → in game; 3. ≥ 2 character states; 4. all SFX firing on real events; 5. ≥ 1 segment of game audio only, no narration; 6. one code→result: `SfxGate` rule `kill cooldown_ms 60` → 20 kills produce one pop (show `test_audio` burst check + in-game); 7. testing, open questions, next steps; 8. who did what (Bao / Claude / models); 9. model per asset; 10. `FILM_SHA` on screen. Walker opening/summary, Verdict → Your Turn → regular outro; 4K landscape.
- [ ] **Step 3: Commit the beat sheet, script and prompts under `film/`** (no MP4). Compute `shasum -a 256 <film>.mp4`.
- [ ] **Step 4: HUMAN — Bao uploads the film to the course media space** and gives Claude the link. Fill README/SUBMISSION with filename, link, SHA-256, `FILM_SHA`.
- [ ] **Step 5: Commit**

```bash
git add film README.md && git commit -m "Add film beat sheet, script, prompts and film receipt

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 23: Fresh-clone verification and submission

- [ ] **Step 1: Push (with Bao's go-ahead), then verify from a fresh clone**

```bash
git push origin HEAD --tags
rm -rf /tmp/lf-final && git clone <remote> /tmp/lf-final && cd /tmp/lf-final
cd godot && $GODOT --headless --path . --import --quit && for s in logic gameplay audio; do $GODOT --headless --path . --script res://tests/test_$s.gd || exit 1; done; cd ..
python3 scripts/audit_repo.py --stage final
```
Expected: all pass; audio suite shows non-null streams.

- [ ] **Step 2: Confirm the film revision:** `git diff $FILM_SHA HEAD -- godot/` is empty (or explain the difference in SUBMISSION).
- [ ] **Step 3: Write `SUBMISSION.md`** with the exact template from the assignment (Student: Bao Xing; Project: walker-lanternfall-bao-x; one-sentence concept; repo URL; Started from; Submitted commit SHA — goes in the Canvas note because a commit cannot contain its own hash, as in A1; Source revision shown in the film = `FILM_SHA`; Godot 4.7.2 / macOS 26 Apple M4 Pro; models; film URL/filename; SHA-256; summary; limitations). Commit and push.
- [ ] **Step 4: Build the source ZIP** from the final commit: `git archive --format=zip -o ../walker-lanternfall-bao-x.zip HEAD` and `unzip -l` it to confirm assets are inside and no MP4/MP3.
- [ ] **Step 5: HUMAN — Bao submits the ZIP + SUBMISSION.md on Canvas** with the final commit SHA in the note.
