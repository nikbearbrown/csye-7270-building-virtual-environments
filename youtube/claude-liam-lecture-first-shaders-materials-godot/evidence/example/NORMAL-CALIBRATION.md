# Actual convention calibration

Official Poly Haven Stone Floor GL/DX pair, 1024×1024 as actually loaded.
Author Dimitrios Savva; CC0; primary URL and verified downloads in
`godot/course-series/normal-calibration/ATTRIBUTION.md`.

GL interpreted as GL: 0.484450.
GL interpreted as DX: 1.515550.
DX interpreted as GL: 1.515549.
DX interpreted as DX: 0.484451.

The known-correct convention is lower. The observed values are not ideal zero
and two, so those ideal numbers are not substituted for measurements. Quantization,
slope limits and texture structure affect this finite-difference check. Calibrate
an acceptance threshold against this actual pair and a disclosed invalid fixture;
do not use a universal magic cutoff. Curl agreement is not artistic correctness.

The first test failed at parse time because a dynamically loaded helper did not
provide an inferred type. Explicit float types repaired it; both receipts remain.
