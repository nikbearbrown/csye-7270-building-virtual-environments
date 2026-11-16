#!/usr/bin/env python3
"""Code-authored PBR texture set for the PBR films (no downloaded or generated-by-AI images).

One tile material, five maps, 1024x1024, all from the same height field:
  tiles_albedo.png     base colour (sRGB): cream and terracotta tiles, dark grout
  tiles_roughness.png  data (linear): tiles 0.30 (+ small noise), grout 0.90
  tiles_metallic.png   data (linear): 0 everywhere except four brass tiles at 1
  tiles_normal.png     data (linear, OpenGL Y+): from the height field
  tiles_ao.png         data (linear): 1 on tile faces, darker in the grout
  tiles_arm.png        packed: R = AO, G = roughness, B = metallic (Poly Haven ARM order)
  flat_normal.png      every texel (128, 128, 255)
  painted_sphere.png   a sphere's lighting PAINTED into a colour texture (for the 'old way' demo)
Run: python3 make_textures.py <out dir>
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image

N = 1024
TILES = 4
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7270)

u = (np.arange(N) + 0.5) / N
U, V = np.meshgrid(u, u)
fu, fv = (U * TILES) % 1.0, (V * TILES) % 1.0
iu, iv = (U * TILES).astype(int), (V * TILES).astype(int)
GROUT = 0.06
BEVEL = 0.12
edge = np.minimum.reduce([fu, 1 - fu, fv, 1 - fv])          # distance to the tile edge, in tile units
height = np.clip((edge - GROUT) / BEVEL, 0, 1)
height = height * height * (3 - 2 * height)                  # 0 in the grout, a smooth bevel up to 1 on the face
tile_face = edge > GROUT

# base colour
cream = np.array([0.93, 0.89, 0.80]); terra = np.array([0.85, 0.47, 0.34]); grout = np.array([0.20, 0.18, 0.16])
brass = np.array([0.89, 0.72, 0.38])
checker = ((iu + iv) % 2 == 0)
metal_tiles = {(1, 1), (2, 2), (0, 3), (3, 0)}
is_metal = np.zeros((N, N), bool)
for (a, b) in metal_tiles: is_metal |= (iu == a) & (iv == b)
col = np.where(checker[..., None], cream, terra)
col = np.where(is_metal[..., None], brass, col)
col = np.where(tile_face[..., None], col, grout)
Image.fromarray((col * 255 + 0.5).astype(np.uint8)).save(out / 'tiles_albedo.png')

# roughness (data)
rough = np.where(tile_face, 0.30 + 0.05 * rng.standard_normal((N, N)), 0.90)
rough = np.where(is_metal & tile_face, 0.22, rough)
rough = np.clip(rough, 0, 1)
Image.fromarray((rough * 255 + 0.5).astype(np.uint8), 'L').save(out / 'tiles_roughness.png')

# metallic (data)
metal = np.where(is_metal & tile_face, 1.0, 0.0)
Image.fromarray((metal * 255 + 0.5).astype(np.uint8), 'L').save(out / 'tiles_metallic.png')

# ambient occlusion (data)
ao = 0.25 + 0.75 * np.clip((edge - 0.02) / (GROUT + BEVEL), 0, 1) ** 0.6
Image.fromarray((ao * 255 + 0.5).astype(np.uint8), 'L').save(out / 'tiles_ao.png')

# normal map from the height field (OpenGL convention: green = +Y = up the image)
strength = 28.0
gy, gx = np.gradient(height * strength)
nx, ny, nz = -gx, gy, np.ones_like(gx)        # image rows grow downward, so +Y (up) is -d/drow
ln = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
nrm = np.stack([nx / ln, ny / ln, nz / ln], -1)
Image.fromarray(((nrm * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8)).save(out / 'tiles_normal.png')

# packed ARM
arm = np.stack([ao, rough, metal], -1)
Image.fromarray((arm * 255 + 0.5).astype(np.uint8)).save(out / 'tiles_arm.png')

# flat normal
Image.fromarray(np.tile(np.array([128, 128, 255], np.uint8), (64, 64, 1))).save(out / 'flat_normal.png')

# the 'old way': lighting painted into an equirectangular colour texture for a sphere
W, H = 2048, 1024
lon = ((np.arange(W) + 0.5) / W) * 2 * np.pi - np.pi
lat = np.pi / 2 - ((np.arange(H) + 0.5) / H) * np.pi
LON, LAT = np.meshgrid(lon, lat)
# Godot's SphereMesh UV: u wraps around Y; the painted light comes from upper-left-front in the sphere's own frame
px, py, pz = np.cos(LAT) * np.sin(LON), np.sin(LAT), np.cos(LAT) * np.cos(LON)
L = np.array([-0.5, 0.6, 0.62]); L = L / np.linalg.norm(L)
ndl = np.clip(px * L[0] + py * L[1] + pz * L[2], 0, 1)
Hh = L + np.array([0, 0, 1.0]); Hh = Hh / np.linalg.norm(Hh)
spec = np.clip(px * Hh[0] + py * Hh[1] + pz * Hh[2], 0, 1) ** 60
base = terra
paint = base * (0.12 + 0.88 * ndl[..., None]) + spec[..., None] * 0.9
Image.fromarray((np.clip(paint, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out / 'painted_sphere.png')

facts = {
    'flat_normal_texel': [128, 128, 255],
    'roughness_tile_mean': float(rough[tile_face & ~is_metal].mean()),
    'roughness_grout': 0.90,
    'metal_tiles': sorted(list(metal_tiles)),
    'arm_order': 'R=AO G=roughness B=metallic',
    'normal_blue_min': int(((nrm[..., 2] * 0.5 + 0.5) * 255 + 0.5).min()),
}
(out / 'textures.json').write_text(json.dumps(facts, indent=2) + '\n')
print(json.dumps(facts, indent=2))
