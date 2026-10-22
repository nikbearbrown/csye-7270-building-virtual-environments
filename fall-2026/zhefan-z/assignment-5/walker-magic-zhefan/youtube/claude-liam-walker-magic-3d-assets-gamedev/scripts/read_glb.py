"""Read .glb files outside Blender and print what the film's B13 shows (node transform, up axis and
bounds, triangles, materials). Read-only. The same checks Claude Code ran on each export on 2026-10-14.

  python -I scripts/read_glb.py <models folder>
"""
import json
import struct
import sys
from pathlib import Path


def read(path):
    data = path.read_bytes()
    magic, ver, length = struct.unpack_from('<4sII', data, 0)
    clen, _ = struct.unpack_from('<I4s', data, 12)
    j = json.loads(data[20:20 + clen])
    assert magic == b'glTF' and length == len(data)
    print(f'{path.name}: glTF {ver}, {len(data)} bytes, generator "{j["asset"].get("generator")}", '
          f'extensionsUsed {j.get("extensionsUsed")}')
    for n in j['nodes']:
        t = {k: n[k] for k in ('translation', 'rotation', 'scale', 'matrix') if k in n}
        print(f'  node {n["name"]}: transform {t or "none (identity)"}')
    lo, hi, tris = [1e9] * 3, [-1e9] * 3, 0
    for m in j['meshes']:
        for p in m['primitives']:
            acc = j['accessors'][p['attributes']['POSITION']]
            lo = [min(a, b) for a, b in zip(lo, acc['min'])]
            hi = [max(a, b) for a, b in zip(hi, acc['max'])]
            tris += j['accessors'][p['indices']]['count'] // 3
    r = lambda v: [round(c, 4) + 0.0 for c in v]
    print(f'  bounds X {r([lo[0], hi[0]])}  Y (up) {r([lo[1], hi[1]])}  Z {r([lo[2], hi[2]])}  '
          f'size {r([b - a for a, b in zip(lo, hi)])}  triangles {tris}')
    for mat in j['materials']:
        pbr = mat['pbrMetallicRoughness']
        print(f'  material {mat["name"]}: base {[round(c, 4) for c in pbr.get("baseColorFactor", [])]} '
              f'metallic {round(pbr.get("metallicFactor", 1.0), 3)} roughness {round(pbr.get("roughnessFactor", 1.0), 3)}'
              + (f' emissive {[round(c, 4) for c in mat["emissiveFactor"]]}' if 'emissiveFactor' in mat else ''))
    return j


if __name__ == '__main__':
    folder = Path(sys.argv[1])
    for name in ('rock.glb', 'crystal.glb', 'chest.glb'):
        read(folder / name)
    # The chest's front: the gold (lock) reaches further toward +Z than the wood.
    j = json.loads((folder / 'chest.glb').read_bytes()[20:20 + struct.unpack_from('<I', (folder / 'chest.glb').read_bytes(), 12)[0]])
    for p in j['meshes'][0]['primitives']:
        print(f'  chest {j["materials"][p["material"]]["name"]}: max Z {round(j["accessors"][p["attributes"]["POSITION"]]["max"][2], 4)}')
