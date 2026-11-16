from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
R=Path(__file__).resolve().parent
main=json.loads((R/'evidence/physics-results.json').read_text());extra=json.loads((R/'evidence/supplemental-results.json').read_text());checks=main['checks']+extra
assert len(checks)==32 and all(x['passed'] for x in checks)
for name in ['rendered-lab.log','supplemental.log']:
 s=(R/'evidence'/name).read_text()
 assert not any(x in s for x in ['SCRIPT ERROR:','ERROR:','FAIL ']),name
for name in ['coin','jump','impulse','crate','tiles','sweep']:
 assert Image.open(R/'captures'/f'{name}.png').size==(3840,2160)
for x in json.loads((R/'evidence/web-captures.json').read_text()):
 assert x['status']==200,(x['name'],x['status'])
 assert 'security verification' not in (R/'sources'/f"docs-{x['name']}.txt").read_text().lower()
assert abs(main['measurements']['jump_height']-72)<7.2
lines=['Recorded local evidence — Godot 4.7.2','PASS 32 physics and logic checks','PASS native engine captures: 3840 x 2160','PASS current logs: no script errors',f"MEASURED jump apex: {main['measurements']['jump_height']:.2f} px",'LIMIT no full-game or cross-device proof']
(R/'evidence/verification.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
