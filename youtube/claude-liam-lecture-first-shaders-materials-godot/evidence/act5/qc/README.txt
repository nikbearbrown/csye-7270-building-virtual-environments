Builder 5 QC helpers (Acts V and VII). All paths are absolute and assume this Mac.
  gate4k.sh ACT CLASS...   after  ./preflight.sh ACT CLASS... : renders each class at 3840x2160 (fps 10, scratch media, deleted afterwards), cuts the frames at 50 / 85 / 95 %
                           into /private/tmp/claude-501/b5work/ and runs the toolkit's own GATE T pixel checks on each (gate_t_frame.py = type_check.py's functions).
  gate_v_frames.py         runs final_frame_check.analyze_frame (Gate V: edge-bleed, underfill, clustered, low contrast) on those frames, honouring lanes/act*.json "sparse".
  terra_blobs.py FRAME     lists the terracotta blobs GATE T would read as accent text (a ring with width/height < 15, or a logo wider than 1.5 x its height, is flagged).
