# Layout preflight

Rendered representative registered scenes at 25/50/95 percent: flat-color bookends, UV code/side/video, car contrast code and uber expressions (36 images). Inspected the representative final-state contact sheet and individual correction/UV frames. The hesitant-writer correction is visible; source excerpts wrap without clipping in the examined frames; title outro has the correct title and handle.

Found: small diagnostic captions inside side-by-side stills become too small. Fixed by omitting the bottom diagnostic strip from still derivatives, preserving the complete source images and full-width demonstration videos. Updated videoAspect to 1280/620 for those stills. Re-ran the canonical remotion_scenes.py --stills --only B02 on the UV film and inspected the corrected frame. Enlarged Your Turn with the component's supported largeText setting.

Found: the title template documentation uses shot type CARD, which the current shared JSON schema rejects. Used GRAPHIC with the unchanged lecture-title-slide-16x9 marker and proof_gate CARD; the bookend checker keys on the marker, not shot type. All sixteen updated beat sheets pass the shared JSON schema and project structure validator.

This is representative authoring preflight, not full film QA. Measured-audio cue alignment, all other frames, title portrait layout, voice checks, complete gate checks and actual master inspection remain required during the build. No audio or full film was rendered.
