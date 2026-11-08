"""List the files git tracks for the A6 upload (user, 2026-11-07: upload only
what the assignment needs, but a reviewer must be able to open and run it).

The set is: every file the game reaches at run time (tools/export_manifest.py,
the same whitelist the Windows export uses) plus each one's .import and .uid
sidecar, all of tests/ and scripts/, project.godot and the A6 write-ups.
Art sources, reference sheets, .blend files and delivery batches stay on disk.

    python scripts/a6_tracked_files.py > ../build/a6_tracked.txt
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "..", "build", "_export_manifest.txt")
JUNK = (".log", ".zip", ".blend", ".blend1", ".mp4", ".mp3", ".wav", ".mov")

subprocess.run([sys.executable, os.path.join(ROOT, "tools", "export_manifest.py"), "--dry-run"], cwd=ROOT, stdout=subprocess.DEVNULL)
out = set()
with open(REPORT, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line)
for f in list(out):
    for side in (".import", ".uid"):
        if os.path.exists(os.path.join(ROOT, f + side)):
            out.add(f + side)
for top in ("tests", "scripts"):
    for d, _, names in os.walk(os.path.join(ROOT, top)):
        for n in names:
            if not n.endswith(JUNK):
                out.add(os.path.relpath(os.path.join(d, n), ROOT).replace("\\", "/"))
# Data the existing suites read that the export does not ship (found by the
# fresh-clone check of tag a6, 2026-11-07): without them test_a3_assets,
# test_audio, test_i18n and test_materials fail on a clean checkout.
TEST_SUPPORT = (
    "art/models/asset_preview.tscn", "art/models/arched_ramp_segment.glb",
    "art/models/cliff_wall_segment.glb", "audio/asset_log.json", "i18n/keys.json",
    "materials/cargo_panel_mild.tres", "materials/cargo_panel_weathered.tres",
    "textures/cargo_panel/rusty_metal_sheet_diff_1k.png",
    "textures/cargo_panel/rusty_metal_sheet_nor_dx_1k.png",
    "textures/cargo_panel/rusty_metal_sheet_nor_dx_1k_inverty.png",
    "textures/cargo_panel/rusty_metal_sheet_nor_gl_1k.png",
    "textures/cargo_panel/rusty_metal_sheet_rough_1k.png",
    "textures/hint_experiment/greys_3x1.png",
)
for f in TEST_SUPPORT:
    for side in ("", ".import", ".uid"):
        if os.path.exists(os.path.join(ROOT, f + side)):
            out.add(f + side)
for f in ("project.godot", "export_presets.cfg", "icon.svg", "default_bus_layout.tres"):
    if os.path.exists(os.path.join(ROOT, f)):
        out.add(f)
print("\n".join(sorted(out)))
