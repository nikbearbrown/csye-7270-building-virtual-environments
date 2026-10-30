"""A5 (agent-written): writes textures/hint_experiment/greys_3x1.png, a 3x1
8-bit RGB PNG with greys 64, 128, 192 (CHANGE-BRIEF.md, Hint experiment).
Only IHDR, IDAT and IEND chunks: no gAMA, sRGB or iCCP, so nothing in the file
asks a reader to reinterpret the stored bytes."""
import struct, sys, zlib

def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

greys = (64, 128, 192)
row = b"\x00" + bytes(v for g in greys for v in (g, g, g))  # filter 0, RGB per texel
png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", 3, 1, 8, 2, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(row, 9))
       + chunk(b"IEND", b""))
open(sys.argv[1], "wb").write(png)
