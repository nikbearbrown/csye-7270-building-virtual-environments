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
