import sys, importlib.util, numpy as np
from PIL import Image
TC="/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts/type_check.py"
spec=importlib.util.spec_from_file_location("type_check",TC); tc=importlib.util.module_from_spec(spec); sys.modules["type_check"]=tc; spec.loader.exec_module(tc)
for p in sys.argv[1:]:
    img=Image.open(p).convert("RGB")
    if img.size[0] < 3000: img=img.resize((3840,2160), Image.LANCZOS)
    pol,bg=tc.detect_polarity(np.array(img))
    C=p.split('/')[-1].split('.')[0]; bid=C.split('_')[0]
    res=[("min-size",*tc.check_min_size(img,bid,C,polarity=pol)),("overflow",*tc.check_overflow(img,bid,polarity=pol,pattern=C)),
         ("contrast",*tc.check_contrast(img,bid,C,polarity=pol,bg_rgb=bg)),("contrast-local",*tc.check_contrast_per_blob(img,polarity=pol)),
         ("bbox-overlap",*tc.check_bbox_overlap(img,polarity=pol))]
    print("==",p,pol)
    for n,s,m in res: print("  ",s,n,m[:200])
