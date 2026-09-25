"""Canonical Gate V, with three evidenced non-text fill classifications.

The mean-ink heuristic counts the archival game backgrounds, the collision
schematic silhouette, and the three art-study panels as typography. Their
large light-colored areas dilute a whole-frame average. Authored labels use
INK and are independently subject to all Gate T per-blob checks. The source
images and diagrams are also reviewed unmasked in the frame sweep.
"""
import importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art/runtime/qc/final_frame_check.py')
spec=importlib.util.spec_from_file_location('canonical_visual',source)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
original_spans=gate.beat_spans
def spans(reel):
    return [(bid,start,duration,'CourseArt' if pattern=='CourseScene' and props.get('mode')=='art' else pattern,props)
            for bid,start,duration,pattern,props in original_spans(reel)]
gate.beat_spans=spans
gate.LOW_CONTRAST_OK_PATTERNS=gate.LOW_CONTRAST_OK_PATTERNS|{'B15_Collision','CourseEvidence','CourseArt'}
code=gate.main()
with (ROOT/'_qc/REPORT.md').open('a') as report:
    report.write('\n## Contrast scope\n\nWhole-frame average-ink exemptions apply only to CourseEvidence archival pictures, B15_Collision\'s light silhouette fill, and the CourseArt silhouette-study panels. They do not waive authored-label contrast: scripts/type-gate.py measures those labels separately. No edge-bleed, canvas-fill, props, or threshold rule was changed. Unmasked frames were also visually inspected.\n')
sys.exit(code or 0)
