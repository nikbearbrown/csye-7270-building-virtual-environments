#!/usr/bin/env python3
"""Original algorithmic textures. No model, network, or borrowed image."""
from pathlib import Path
import struct,zlib
root=Path(__file__).resolve().parents[1]/'godot/signal-garden/assets'
def png(name,role):
    data=bytearray()
    for y in range(64):
        data.append(0)
        for x in range(64):
            stripe=(x//8)%2
            data.extend(((44+stripe*15,78+stripe*18,85+stripe*16) if role=='color' else (int(255*(0.4 if stripe else 0.85)),)*3))
    def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    (root/name).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,64,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(data))+chunk(b'IEND',b''))
png('gate-color.png','color');png('gate-roughness.png','data')
