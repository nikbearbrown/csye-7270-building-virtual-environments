import sys, glob, os
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc")
import final_frame_check as f
import json
lanes = {}
R="/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/lanes/"
for a in ("act5.json","act7.json"):
    for k,v in json.load(open(R+a)).items(): lanes[k]=v
W="/private/tmp/claude-501/b5work/"
for fr in sorted(glob.glob(W+"B*_f0.[58]*.png")):
    name=os.path.basename(fr)
    if name.endswith("_s.png"): continue
    bid=name.split("_")[0]
    d, cover = f.analyze_frame(fr)
    sparse = lanes[bid].get("sparse", True)
    if sparse: d=[x for x in d if x[1] not in ("underfill","clustered","empty-frame")]
    print(f"{name:42s} cover={cover*100:4.0f}% sparse={sparse!s:5s} ->", d if d else "clean")
