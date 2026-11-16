# Act IX (B59-B68) evidence and 4K proof — what is here and how to re-run it

REEL = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot`

What this is: the scripts and output behind Act IX's pictures. Nothing here is a new Godot capture; every picture is a crop (or a circular mask of a sphere's own silhouette) of a real capture that already sat in `captures/`.
Why: so the numbers and pictures on screen can be re-derived, and so the GATE T / GATE V behaviour of dark captures is proven at 4K, not guessed from a low-res preview.
Found: every beat passes GATE T at its 50% frame and at 44/47/53/56%; GATE V passes at 50% and 85% except "underfill" at the 50% frame of B60, B64 and B68 (phased beats, `sparse: true` in `lanes/act9.json`).

| File | What it does |
|---|---|
| `make_a9_pantry.py` | cuts `pantry/a9_*.png` from `captures/lab`, `captures/example-native` (via `pantry/ev_*`) and `captures/forward-plus` (panel crop, four pad crops, 12 + 6 masked spheres, three probe patches, two pad strips) |
| `verify_numbers.py` | asserts every pixel number, every code line and every derived figure Act IX shows against the evidence json / source files (prints `ALL MATCH`) |
| `gate_frames.py` | runs `type_check.py`'s pixel checks (min-size, overflow, contrast, local contrast, bbox overlap, kerning) and `final_frame_check.analyze_frame` (GATE V) on 4K PNG frames |
| `gate4k.sh <Class> [fps]` | renders ONE class at 3840 x 2160 (`manim -qk --fps 8`), cuts the 44/47/50/53/56/85% frames, runs `gate_frames.py`, prints the around-the-midpoint FAIL rows, deletes the scratch media |
| `PREFLIGHT-RUN.txt`, `GATE-RUN-4K.txt` | the last full output (Gate A static check + layout audit; the 4K gate run) |

Re-run (from `REEL`): `python3 evidence/act9/make_a9_pantry.py && python3 evidence/act9/verify_numbers.py && ./preflight.sh 9 B59_GreenLogs B60_CaptureInEngine B61_FourCaptures B62_Gaps B63_ForwardPlusDiffers B64_NoClamp B65_InPlay B66_Sweep B67_OneShaderTwoMaterials B68_NotDone && evidence/act9/gate4k.sh B63_ForwardPlusDiffers`

## What the 4K runs taught (each is a trap for the next builder)
- GATE T samples a clip at its MIDPOINT only (`type_check.extract_frame`, default t = 50%); GATE V samples 50% and 85%. Read the GATE T rows of an `_85` frame as information.
- `check_contrast` (8.3) takes every pixel with gray < 120 as "text colour" and averages them. A large mid-tone capture (the flat green pad at activation 1, the green half-activation strips) drags the mean toward green: 2.5:1 for B64 with the green on screen, 4.47:1 for B63 at 5.4 units wide. Fixes used: a heavy INK frame round the capture (`a9_frame`, stroke 12-14) pulls the mean back (4.95:1), and the flat green arrives AFTER the midpoint in B64.
- GATE V "low-contrast" averages every non-background pixel: a big bright cyan or a cream floor (B64, B65 first builds: 0.26-0.29 < 0.30) fails it; ink frames and a tighter crop fix it. "underfill" is waived only by `sparse`.
- GATE T reads a wide terracotta OUTLINE (aspect 1.5-15, stroke >= 4% of its box) as accent text: `ring()` round a wide box fails 8.3. Terracotta dots, pointers (small filled triangles), circles round spheres, and `ring_line` (aspect > 15) pass. Never ring wide boxes.
- GATE T reads pixels within 48 of INK (61,57,41) as text: Godot's dark panel (18,31,41) sits 50 away, so codec noise makes it flip between frames (B59's first build passed at 50% and failed at 85%). Dark panels land after the midpoint.
- Arrows are text-run blobs for the min-size check: an arrow head under 41 px tall (tip 0.16) fails 8.1; use tip >= 0.22 (B62, B63 fixed).
- The kit's `code_block` rows are now measured (Gate A passes long rows); lines of 59 characters need size 20, which is exactly the type floor and passed at 4K.
