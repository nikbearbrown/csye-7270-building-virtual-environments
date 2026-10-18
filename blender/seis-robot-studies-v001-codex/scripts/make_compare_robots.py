"""Build compare/ side-by-sides: supplied reference LEFT, render RIGHT. Run: python3 -I make_compare_robots.py <model-folder>
Pairs are chosen by the builder of these pages by eye (matching angle as closely as the supplied photographs allow)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root = Path(sys.argv[1]).resolve()
H = 1100
PH = "references/"
PAIRS = {
 "seis-robot-studies-v001-codex": [
  ("compare/waveform-ref_vs_compact-three-quarter", PH+"approved-waveform-reference.png", "renders/compact-three-quarter.png", "SUPPLIED REFERENCE (drawing)", "RENDER: compact, three-quarter"),
  ("compare/waveform-ref_vs_slim-three-quarter", PH+"approved-waveform-reference.png", "renders/slim-three-quarter.png", "SUPPLIED REFERENCE (drawing)", "RENDER: slim, three-quarter"),
  ("compare/boxy-body-ref_vs_compact-bent-pose", PH+"boxy-body-reference.png", "renders/compact-bent-pose.png", "SUPPLIED REFERENCE (boxy body)", "RENDER: compact, bent pose"),
 ],
 "seis-robot-engineer-v002-codex": [
  ("compare/front-photo_vs_engineer-front", PH+"468985428_10114933438301756_8410860778988019980_n.jpg", "renders/engineer-front.png", "SUPPLIED REFERENCE (photograph, front)", "RENDER: engineer, front"),
  ("compare/back-photo_vs_engineer-back", PH+"00468882964_10114933437233896_1188163251417263509_n.jpg", "renders/engineer-back.png", "SUPPLIED REFERENCE (photograph, back)", "RENDER: engineer, back"),
  ("compare/three-quarter-photo_vs_engineer-three-quarter", PH+"471739246_10115426397816936_7431857388095807107_n.jpg", "renders/engineer-three-quarter.png", "SUPPLIED REFERENCE (photograph, slight turn)", "RENDER: engineer, three-quarter"),
 ],
 "seis-robot-reference-body-v003-codex": [
  ("compare/front-photo_vs_body-front", PH+"468985428_10114933438301756_8410860778988019980_n.jpg", "renders/body-front.png", "SUPPLIED REFERENCE (photograph, front)", "RENDER: v003 body, front"),
  ("compare/back-photo_vs_body-back", PH+"00468882964_10114933437233896_1188163251417263509_n.jpg", "renders/body-back.png", "SUPPLIED REFERENCE (photograph, back)", "RENDER: v003 body, back"),
  ("compare/three-quarter-photo_vs_body-three-quarter", PH+"471739246_10115426397816936_7431857388095807107_n.jpg", "renders/body-three-quarter.png", "SUPPLIED REFERENCE (photograph, slight turn)", "RENDER: v003 body, three-quarter"),
 ],
}[root.name]
try: font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
except Exception: font = ImageFont.load_default()
(root/"compare/web").mkdir(parents=True, exist_ok=True)
for out, l, r, ll, rl in PAIRS:
    A = Image.open(root/l).convert("RGB"); B = Image.open(root/r).convert("RGB")
    A = A.resize((round(A.width*H/A.height), H), Image.LANCZOS); B = B.resize((round(B.width*H/B.height), H), Image.LANCZOS)
    bar = 56; gap = 12
    W = A.width + B.width + gap
    im = Image.new("RGB", (W, H+bar), (24, 24, 26)); im.paste(A, (0, bar)); im.paste(B, (A.width+gap, bar))
    d = ImageDraw.Draw(im); d.text((12, 12), ll, fill=(236, 236, 234), font=font); d.text((A.width+gap+12, 12), rl, fill=(236, 236, 234), font=font)
    im.save(root/(out+".jpg"), quality=88, optimize=True)
    s = 1100/im.width if im.width > 1100 else 1
    im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS).save(root/(out.replace("compare/", "compare/web/")+".jpg"), quality=85, optimize=True)
    print(out, im.size)
