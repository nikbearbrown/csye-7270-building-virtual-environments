#!/usr/bin/env python3
"""b26_check.py — re-runs, read-only, the two comparisons behind B26 on the real walker-jumpman-clawd repo:
  (1) the record's own check (scripts/clawd-build.cjs lines 7-8): slice player.gd from `func _physics_process(` to the next `\\nfunc `
      and compare that slice, baseline commit 9387542 vs HEAD;
  (2) the whole file: `git diff --numstat` for player.gd (added, removed) and the sha256 of the whole file at each commit.
  python3 evidence/act4/b26_check.py        (output saved in b26_check.log)
"""
import subprocess, hashlib
C = "/Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman-clawd"
BASE, P = "9387542", "godot/features/player/player.gd"
git = lambda *a: subprocess.run(["git", "-C", C, *a], capture_output=True, text=True, check=True).stdout
old, new = git("show", f"{BASE}:{P}"), git("show", f"HEAD:{P}")
def sl(s):
    i = s.index("func _physics_process(")
    return s[i:s.index("\nfunc ", i + 5)]
print("slice from `func _physics_process(` to the next `func`:")
print("  old slice sha256", hashlib.sha256(sl(old).encode()).hexdigest()[:16], f"({sl(old).count(chr(10)) + 1} lines)")
print("  new slice sha256", hashlib.sha256(sl(new).encode()).hexdigest()[:16], f"({sl(new).count(chr(10)) + 1} lines)")
print("  slices byte-identical:", sl(old) == sl(new))
print("whole player.gd:")
print("  old sha256", hashlib.sha256(old.encode()).hexdigest()[:16], f"({old.count(chr(10))} lines)")
print("  new sha256", hashlib.sha256(new.encode()).hexdigest()[:16], f"({new.count(chr(10))} lines)")
print("  whole files byte-identical:", old == new)
a, d, _ = git("diff", "--numstat", BASE, "HEAD", "--", P).split("\t")
print(f"  git diff --numstat: +{a} -{d} = {int(a) + int(d)} changed lines")
print("git diff --stat (HEAD vs baseline), player.gd row:", [l for l in git("diff", "--stat", BASE, "HEAD", "--", "godot").splitlines() if "player.gd" in l][0].strip())
