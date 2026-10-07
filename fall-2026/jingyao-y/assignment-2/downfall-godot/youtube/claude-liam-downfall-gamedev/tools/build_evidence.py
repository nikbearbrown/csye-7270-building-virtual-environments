"""Write gamedev-evidence.json (schema 1) against a pristine clone of the film's revision.

  python tools/build_evidence.py <snapshot-of-111bf6e>

Every file in the snapshot (minus .git/.godot/*.uid) is either a hashed record tied
to a component the film explains, or an exclusion with a reason. Excerpts are read
from the snapshot and must equal the beat's displayed code; code/result pairs hash
the result media actually shown.
"""
import fnmatch, hashlib, json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
SNAP = Path(sys.argv[1]).resolve()
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
beats = {b["beat_id"]: b for b in sheet["beats"]}

COMPONENTS = [
    ("lappland-states",
     "Lappland's states are cells of two gpt-image atlases; the animator maps facing to five drawn combat rows plus mirrors, "
     "and each action to a first column and frame count. A static cell swap per state.",
     ["B03", "B04"],
     ["godot_assets/lappland_animator_3d.gd", "godot_assets/lappland_8dir_walk_32.png*", "godot_assets/lappland_combat_64.png*",
      "godot_assets/Lappland8DirWalk32.tres", "godot_assets/prepare_combat_atlas.py", "entities/player.gd",
      "godot_assets/拉普兰德战斗素材.md"]),
    ("warehouse-event-sounds",
     "Four warehouse signals emitted on an edge by room_reveal.gd are connected to FieldAudio cues; two cues have "
     "Gemini-generated WAVs cut by cut_audio.py, two are counted but silent until generated.",
     ["B05", "B06"],
     ["world/room_reveal.gd", "game/field_audio.gd", "game/game_manager.gd", "audio/sfx/*", "audio/tools/cut_audio.py",
      "audio/PROMPTS.md"]),
    ("music-loops-and-stings",
     "GameMusic switches base/field loops by game state, freezes the field loop on pause, ducks the base loop, and plays one "
     "sting per run end; loop points come from audio/asset_log.json; Settings mutes the Master bus.",
     ["B08", "B09", "B14"],
     ["game/game_music.gd", "audio/music/*", "audio/asset_log.json", "audio/tools/find_loop.py", "ui/system_screens.gd",
      "ui/event_screens.gd"]),
    ("relic-icon-pipeline",
     "Relic icon trace: brief row → image-model prompt → raw painting → reduce_generated.py (crop, nearest-neighbour, "
     "23-colour quantize, outline) → runtime icon drawn at whole multiples of 72 by AK.relic_icon via RelicIcons.",
     ["B11", "B12"],
     ["art/relics/reduce_generated.py", "art/relics/build_r1.py", "art/relics/R_brief_v1.md", "art/relics/batch_R1_v1/README.md",
      "art/relics/batch_R1_v1/manifest.json", "art/relics/batch_R1_v1/is2_058*", "art/relics/runtime/*", "ui/relic_icons.gd",
      "ui/ak.gd", "art/relics/R1_revision_v2.md"]),
    ("fresh-clone-assets",
     "The repository's ignore rules decide what a fresh clone contains; 111bf6e anchored /music/ after a fresh-clone "
     "capture was silent; run_all.ps1 creates ../evidence so a clone can run the suites.",
     ["B13", "B14", "B16"],
     [".gitignore", "tests/run_all.ps1"]),
    ("audio-tests",
     "test_audio.gd counts every FieldAudio.play call (before the headless early return) through a warehouse walk, and "
     "checks loop points, pause, death/extraction stings and mute; test_relic_icons.gd checks icon coverage and scale.",
     ["B15", "B16"],
     ["tests/test_audio.gd", "tests/test_relic_icons.gd"]),
    ("environments",
     "Generated field surfaces and prop groups per region, tiled by the terrain shader, and the assembled Rhodes base "
     "loaded by BaseMap; the character must stay readable against them.",
     ["B02", "B04", "B06"],
     ["art/field/surface_*_v2.png*", "art/field/scene_groups_v2.png*", "art/field/props_v1.png*", "art/field_art.gd",
      "art/terrain_background.gdshader", "art/rhodes_runtime/*", "world/base_map.gd"]),
    ("assignment-documents",
     "Retrospective concept, storyboard, character sheet, change brief, test report, frictional log, sources/asset log "
     "and submission, with the design images they cite.",
     ["B01", "B02", "B17"],
     ["CONCEPT.md", "STORYBOARD.md", "CHARACTER-SHEET.md", "CHANGE-BRIEF.md", "SOURCES.md", "FRICTIONAL.md", "TEST-REPORT.md",
      "SUBMISSION.md", "README.md", "design/*"]),
]

EXCLUDE = [
    ("art/items/*", "Equipment icon batches E1–E4 (and their briefs/previews): generated art outside this film's traced asset; logged in SOURCES.md."),
    ("art/relics/batch_*", "Other relic batches' contact sheets, previews and manifests; the film traces is2_058 only."),
    ("art/relics/refs/*", "Brief reference tables and screenshots; PRTS images themselves are not in git."),
    ("art/rhodes/*", "Rhodes base art batches, assembly scripts and validators; the assembled runtime is shown via art/rhodes_runtime."),
    ("art/field/*", "Other field art versions, prompts and enemy atlases not explained in this film."),
    ("art/portraits/*", "Portrait brief for a batch not yet delivered."),
    ("art/ui_mockup/*", "HTML GUI prototype, not runtime."),
    ("art/*", "Other art helpers and sources outside the film's components."),
    ("godot_assets/*", "Other Lappland source sheets, VFX and helper scripts not shown in this film."),
    ("tests/*", "Other test, capture and recording scripts; their results are reported in TEST-REPORT.md."),
    ("game/*", "Gameplay systems (combat numbers, loot, base rules, relics, economy) outside an art/audio film."),
    ("entities/*", "Enemies, loot, containers and projectiles: runtime gameplay outside this film's scope."),
    ("inventory/*", "Inventory data model: outside this film's scope."),
    ("ui/*", "Other GUI screens: outside this film's scope."),
    ("world/*", "Map generation, terrain, scene dressing and base views not explained in this film."),
    ("audio/*", "Audio helper files not used at runtime."),
    ("*.md", "Chinese design documents and research notes that the assignment documents summarize."),
    ("*", "Project configuration and remaining files outside the film's components."),
]


def inventory(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                  if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(root).parts) and p.suffix != ".uid")


def match(path, pattern):
    return fnmatch.fnmatchcase(path, pattern)


files, exclusions, comp_files = [], [], {c[0]: [] for c in COMPONENTS}
for path in inventory(SNAP):
    ids = [cid for cid, _, _, pats in COMPONENTS if any(match(path, p) for p in pats)]
    if ids:
        sha = hashlib.sha256((SNAP / path).read_bytes()).hexdigest()
        role = "source" if path.endswith((".gd", ".py", ".ps1", ".gdshader", ".tres")) else \
               "asset" if path.endswith((".png", ".ogg", ".wav", ".json", ".import")) else "document"
        files.append({"path": path, "sha256": sha, "role": role, "component_ids": ids})
        for cid in ids: comp_files[cid].append(path)
    else:
        reason = next(r for pat, r in EXCLUDE if match(path, pat))
        exclusions.append({"path": path, "reason": reason})

components = [{"id": cid, "explanation": expl, "beat_ids": bids, "files": comp_files[cid]} for cid, expl, bids, _ in COMPONENTS]
for c in components:
    assert c["files"], c["id"]

excerpts, pairs = [], []
for bid, b in beats.items():
    props = b.get("shot", {}).get("remotion", {}).get("props", {})
    if b.get("shot", {}).get("remotion", {}).get("pattern") == "GodotDevWorkbench" and props.get("code"):
        path = props["path"].removeprefix("res://")
        start = props["startLine"]
        text = props["code"]
        end = start + len(text.split("\n")) - 1
        excerpts.append({"beat_id": bid, "path": path, "start_line": start, "end_line": end, "text": text})
        order = list(beats)
        result = order[order.index(bid) + 1]
        media = beats[result]["shot"]["evidence_media"]
        pairs.append({"code_beat": bid, "result_beat": result,
                      "observation": beats[result]["shot"]["show"][-1]["event"],
                      "media": {"path": media, "sha256": hashlib.sha256((REEL / media).read_bytes()).hexdigest()}})

data = {"schema_version": 1, "game_revision": "111bf6e", "snapshot": "pristine git clone of 111bf6e",
        "teaching_contract": "code-then-result-v1", "files": files, "components": components,
        "excerpts": excerpts, "exclusions": exclusions, "code_result_pairs": pairs}
(REEL / "gamedev-evidence.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(files), "records,", len(exclusions), "exclusions,", len(excerpts), "excerpts,", len(pairs), "pairs")
