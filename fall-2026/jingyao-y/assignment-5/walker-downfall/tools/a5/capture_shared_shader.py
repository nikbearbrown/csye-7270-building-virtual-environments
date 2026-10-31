"""Change one shader statement, render both materials, and restore exact bytes."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[2]
SHADER = ROOT / "shaders/cargo_panel.gdshader"
OUT = ROOT / "evidence/a5/use-it"
original = SHADER.read_bytes()
before_hash = hashlib.sha256(original).hexdigest()
old = b"ALBEDO = texture(albedo_tex, uv).rgb * tint_color.rgb;"
new = b"ALBEDO = texture(albedo_tex, uv).rgb * tint_color.rgb * 0.5;"
assert original.count(old) == 1
record = {"before_sha256": before_hash, "original_statement": old.decode(), "changed_statement": new.decode()}
try:
    SHADER.write_bytes(original.replace(old, new))
    with (ROOT/"logs/a5_shared_shader_capture.log").open("wb") as log:
        result = subprocess.run([os.environ.get("GODOT",str(ROOT.parent/"Godot_v4.7.2-stable_win64_console.exe")), "--path",str(ROOT),
                                 "--script","res://tools/a5/capture_material_pair.gd", "--resolution","1280x720", "--fixed-fps","60"], stdout=log, stderr=subprocess.STDOUT, timeout=300)
    assert result.returncode == 0
finally:
    SHADER.write_bytes(original)
    record["restored_sha256"] = hashlib.sha256(SHADER.read_bytes()).hexdigest()
    record["restored_byte_exact"] = SHADER.read_bytes() == original
    (OUT/"shared-shader.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
assert record["restored_byte_exact"]
baseline = Image.open(OUT/"materials-baseline.png").convert("RGB")
shared = Image.open(OUT/"materials-shared-shader-change.png").convert("RGB")
single = Image.open(OUT/"materials-a-only.png").convert("RGB")
for name, image in (("shared_shader",shared),("A_only",single)):
    record[name] = {}
    for label, box in (("A",(235,190,590,530)),("B",(690,190,1045,530))):
        diff = ImageChops.difference(baseline.crop(box),image.crop(box))
        record[name][label] = {"mean_abs_rgb8": ImageStat.Stat(diff).mean, "changed":diff.getbbox() is not None}
assert record["shared_shader"]["A"]["changed"] and record["shared_shader"]["B"]["changed"]
assert record["A_only"]["A"]["changed"] and not record["A_only"]["B"]["changed"]
(OUT/"shared-shader.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
print(json.dumps(record,indent=2))
