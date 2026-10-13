# Act I evidence (B01-B05) — what was captured, cut, or run

**What this is.** Every picture in Act I is a real capture, a crop of one, or text copied from a real run on this Mac (2026-10-09). Nothing is mocked. The only drawn content is ideas (a card pair, two bars, an indent guide) and the one Python block, labelled "illustrative".

**Files (all absolute below; REEL = /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-csye-7270-why-godot).**
- REEL/pantry/a1_pong_001..105.jpg: Walker Pong, the real recorded clip (scripted input), cut to frames by REEL/evidence/act1/prep_pantry.py.
- REEL/pantry/a1_license_crop.png, REEL/pantry/a1_download_btn.jpg: crops of the real godotengine.org captures (prep_pantry.py).
- REEL/pantry/a1_editor.png: a REAL Godot 4.7.2 editor window, recorded with Godot's Movie Maker on a scratch copy of the Claude Walker project (REEL/evidence/act1/capture_editor.sh). The scratch copy's window-size override was raised to 1920x1080; the original project is untouched. The scene shown is empty in the 3D view (these projects draw in code); it is the editor's real UI.
- REEL/evidence/act1/gates_act1.py + gates_act1.log: GATE T / Gate V at real 4K for B01-B05 (render under the shared lock).
- REEL/evidence/act1/frames_act1.sh: low-res frames at 25/50/85/95%. REEL/evidence/act1/cropgate.py: a quick synthetic GATE T filter for a capture crop.

**Findings that shaped the build.**
- GATE T at 4K flags dark/blue-grey regions of the godotengine.org hero and download artwork (white nav and subtitle text over dark pixel art; the "text" detector sees mid-dark blobs). The download page is therefore cropped to its buttons; the home hero and the dark editor window land after the 50% sample in B01.
- `du -sh` prints binary units (337M = 337 MiB = 353.4 MB), GitHub's asset is 170,622,178 bytes = 170.6 MB: B04 draws the bars in bytes and labels each with its own source's unit.
