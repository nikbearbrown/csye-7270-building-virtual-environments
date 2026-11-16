# Scenes and Instances in Godot — Capture

The reference review below was inherited from the combined lecture. Only beats present in content.json are used here. The new door comparison is documented separately below.

# Reproduce the evidence

Commands may run from /Users/bear/Documents/CoWork/bear-textbooks/books; every project path is explicit.

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/godot --editor --import --quit
/Applications/Godot.app/Contents/MacOS/Godot --headless --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/godot --quit-after 600
/Applications/Godot.app/Contents/MacOS/Godot --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/godot --quit-after 600
/Applications/Godot.app/Contents/MacOS/Godot --headless --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/godot --script res://supplemental.gd
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/capture_docs.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/extract_excerpts.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-collision-physics/verify_evidence.py
```

Capture stdout/stderr into the corresponding evidence logs when rerunning. The rendered main run creates six 3840×2160 viewport PNGs and physics-results.json; headless mode skips PNG capture. Supplemental creates supplemental-results.json. Do not overwrite the final rendered result JSON with headless results and still call it rendered evidence. Preserve earlier failed logs when fixing a problem.

Scripted setups and direct test calls are explicitly identified. No hidden teleport was used to claim normal gameplay; respawn itself is an isolated function test. None of these captures is a normal-input walkthrough or human playtest.


## New comparison reproduction

Run only when source changes justify it:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --path /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-scenes-and-instances-in-godot/godot res://comparison.tscn
```

This writes five captures and evidence/comparison-results.json. Capture stdout separately if rerunning. Headless mode performs checks without PNG capture. Native SubViewport output is 3840 × 2160. Current images were visually checked; this is evidence QA, not film-frame QA.
