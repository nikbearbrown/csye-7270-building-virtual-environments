#!/usr/bin/env python3
"""Check actual rendered samples; never substitute a process exit code for shader diagnostics."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent
log=(R/'evidence/godot-run.log').read_text()
assert 'SHADER ERROR' not in log and 'ERROR:' not in log, 'Shader diagnostics in positive run'
assert "SHADER ERROR: Invalid assignment of 'int' to 'float'." in (R/'evidence/negative-type.log').read_text()
checks=[]
def pixel(name,x,y,expected,tol=2/255):
 im=Image.open(R/'captures'/f'{name}.png').convert('RGBA');c=im.getpixel((x,y))
 actual=[v/255 for v in c]
 assert all(abs(a-e)<=tol for a,e in zip(actual,expected)),(name,actual,expected)
 checks.append({'capture':name,'xy':[x,y],'actual':actual,'expected':expected,'tolerance':tol})
pixel('constant',1700,1000,[1,.5,.5,1])
pixel('uv',1350,1000,[.25,570/1200,0,1])
pixel('uv',2050,1000,[.75,570/1200,0,1])
pixel('scalars',1700,1000,[.5,0,0,1])
pixel('swizzle',1700,1000,[.9,.6,.2,1])
pixel('matrix',1700,1000,[.25,.5,0,1])
pixel('array',1700,1000,[.3,0,0,1])
pixel('varying',1350,1000,[.25,.25,.25,1])
pixel('varying',2050,1000,[.75,.75,.75,1])
pixel('branch',1350,1000,[.2,.2,.2,1])
pixel('branch',2050,1000,[.9,.9,.9,1])
pixel('switch',1700,1000,[.25,.25,.25,1])
pixel('fallthrough',1700,1000,[.1,.1,.1,1])
pixel('loop',1700,1000,[1,1,1,1]);pixel('while',1700,1000,[1,1,1,1])
for name in ['shared','unique','instance']:
 pixel(name,1000,1000,[.85,.25,.12,1])
 pixel(name,2800,1000,[.85,.25,.12,1] if name=='shared' else [.2,.55,.8,1])
for i,e in enumerate([[.2,.55,.8,1],[.525,.4,.46,1],[.85,.25,.12,1]]): pixel('flash',690+i*1230,1000,e)
assert 'CHECK hint_range stores 7.0' in log
assert 'CHECK unique material: true; shared shader: true' in log
shaders=list((R/'godot/shaders').glob('*.gdshader'))
assert len(shaders)==20
assert all((R/'captures'/f'{p.stem}.png').exists() or p.stem=='uniform' for p in shaders)
files=[p for folder in ['godot','captures','sources'] for p in (R/folder).rglob('*') if p.is_file() and '.godot' not in p.parts]
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(R/'evidence/sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'evidence/pixel-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
lines=[f'PASS: {len(shaders)} positive shader files rendered.', 'PASS: no shader errors in positive run.', 'PASS: deliberate type error detected.',f'PASS: {len(checks)} rendered pixel checks.', 'PASS: shared and independent material values.', 'PASS: hint_range stores out-of-range input.', 'Scope: Godot 4.7.2, Compatibility, Apple M4 Pro.', 'Not tested: other GPUs, performance, game feel.']
(R/'evidence/verification.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
