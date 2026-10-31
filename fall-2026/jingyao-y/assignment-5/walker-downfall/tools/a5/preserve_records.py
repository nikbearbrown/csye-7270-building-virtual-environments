"""Preserve the existing assignment documents and the Step 4 working records."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUTSIDE = ROOT.parent / "evidence/change-brief-2026-10-30"
archive = ROOT / "a5/archive/pre-final-documents"
archive.mkdir(parents=True, exist_ok=True)
for name in ("README.md", "TEST-REPORT.md", "FRICTIONAL.md", "SOURCES.md", "SUBMISSION.md", "LANGUAGE-NOTES.md", "CLAUDE.md"):
    destination = archive / name
    if not destination.exists() and (ROOT / name).exists():
        shutil.copy2(ROOT / name, destination)

records = ROOT / "evidence/a5/step4"
records.mkdir(parents=True, exist_ok=True)
for source, target in (("export_standard_material.gd", "export_standard_material.gd.txt"),
                       ("export_standard_material.log", "export.log"),
                       ("validate_standard_generated.log", "render-validation.log"),
                       ("validate_standard_generated.gd", "validate_standard_generated.gd.txt")):
    shutil.copy2(OUTSIDE / source, records / target)

session = Path(r"D:\CodexData\codex-home-parts\sessions\2026\10\30\rollout-2026-10-30T09-26-15-01a18cfd-5724-7cb1-956d-d7cfe5dfe46b.jsonl")
rows = session.read_text(encoding="utf-8").splitlines()
first = json.loads(rows[536])["payload"]["input"]
literal = re.search(r'tools\.apply_patch\(("(?:\\.|[^"\\])*")\)', first).group(1)
patch = json.loads(literal)
document = "\n".join(line[1:] for line in patch.splitlines() if line.startswith("+") and not line.startswith("+++")) + "\n"
(records / "language-notes-draft-1.md").write_text(document, encoding="utf-8")
payload = json.loads(rows[767])["payload"]
for block in payload["output"]:
    text = block.get("text", "")
    if text.startswith('{"chunk_id"'):
        result = json.loads(text)
        document = result["output"]
        assert document.startswith("# LANGUAGE-NOTES")
        (records / "language-notes-draft-2.md").write_text(document, encoding="utf-8")
        break
else:
    raise RuntimeError("The second archived document was not found")
shutil.copy2(archive / "LANGUAGE-NOTES.md", records / "language-notes-english-draft.md")
manifest = {p.name: {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in records.iterdir() if p.is_file() and p.name != "records-manifest.json"}
(records / "records-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("Preserved", len(manifest), "Step 4 records")
