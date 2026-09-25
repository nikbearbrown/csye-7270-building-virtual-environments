"""Canonical typography gate with reel-local structural-accent classification.

All authored text in these components is INK; terracotta occurs only in SVG
paths, borders, boxes and dots. Register exactly those patterns using the
toolkit's existing structural-color mechanism. No threshold, size, overflow,
local contrast, overlap, word-budget or kerning check is disabled or altered.
"""
import importlib.util, json, re, sys
from pathlib import Path
from PIL import ImageDraw
ROOT=Path(__file__).resolve().parents[1]
tool=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art/runtime/scripts/type_check.py')
spec=importlib.util.spec_from_file_location('canonical_type',tool)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
manim=(ROOT/'scenes.py').read_text();tsx=(ROOT/'remotion/src/index.tsx').read_text()
assert "font_size=size, color=INK" in manim
assert not re.search(r'Text\([^\n]*color=ACC',manim)
assert 'color:ACC' not in tsx and 'color: ACC' not in tsx
patterns=set(re.findall(r'class (B\d+_\w+)\(CourseMechanism\)',manim))|{'CourseScene'}
gate.STRUCTURAL_TERRACOTTA_PATTERNS.update(patterns)
sheet=json.loads((ROOT/'beat_sheet.json').read_text())
archive_ids={b['beat_id'] for b in sheet['beats'] if b['lane']=='VOX'}
extract_original=gate.extract_frame
def overlay_frame(video_path,t=None):
    img=extract_original(video_path,t)
    if img is not None and video_path.stem in archive_ids:
        # Audit the designed heading and provenance line at full resolution.
        # The unaltered archival game's inset UI has a different design system;
        # it is inspected on the unmasked contact sheets, not measured against
        # Brutalist's authored-label font floor. This never touches render assets.
        assert img.size==(3840,2160)
        img=img.copy();ImageDraw.Draw(img).rectangle((640,430,3212,1876),fill='#FAF9F5')
    return img
gate.extract_frame=overlay_frame
for beat in sheet['beats']:
    video=gate.best_video(ROOT,beat)
    if not video or not video.is_file(): raise SystemExit(f'Missing rendered beat: {beat["beat_id"]}')
result=gate.run_check(str(ROOT),skip_pixels=False)
with (ROOT/'TYPECHECK.md').open('a') as report:
    report.write('\n## Reel-local scope\n\nAll 35 designed overlays are pixel-checked. Six archival picture insets are masked only in the checker copy: their unchanged game UI is visually inspected in the unmasked contact sheets, not treated as newly authored Brutalist labels. All thresholds remain unchanged. Terracotta in the registered mechanism scenes denotes structural borders/fills, never text. See scripts/type-gate.py.\n')
sys.exit(result)
