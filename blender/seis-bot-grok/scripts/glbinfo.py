import json, struct, sys
for fn in sys.argv[1:]:
    b = open(fn, 'rb').read()
    l = struct.unpack('<I', b[12:16])[0]; j = json.loads(b[20:20 + l])
    tris = 0
    for m in j['meshes']:
        for p in m['primitives']:
            if 'indices' in p: tris += j['accessors'][p['indices']]['count'] // 3
    print(fn, '%.2f MB' % (len(b) / 1e6), 'nodes', len(j['nodes']), 'meshes', len(j['meshes']), 'tris', tris, 'skins', len(j.get('skins', [])),
          'joints', len(j['skins'][0]['joints']) if j.get('skins') else 0, 'anims', [a['name'] for a in j.get('animations', [])],
          'materials', len(j.get('materials', [])), 'images', len(j.get('images', [])), 'ext', j.get('extensionsUsed'))
