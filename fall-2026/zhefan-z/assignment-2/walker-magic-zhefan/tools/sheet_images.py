"""Make the two CHARACTER-SHEET check images from the cleaned sprites.

design/character/silhouette.png  idle filled solid black at 64 px on the actual cave background (1x, 640x360),
                                 on the ground tiles, at three screen positions
design/character/collision.png   every pose at 64 px (shown 4x) with the sheet's 14x44 collision rectangle,
                                 feet to chin, centred on the body, identical in every pose

Run after tools/clean_sprites.py, with the ComfyUI venv:
    E:/7270/tools/ComfyUI/.venv/Scripts/python.exe tools/sheet_images.py
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import clean_sprites as cs

REPO = Path(__file__).resolve().parent.parent
SPR = REPO / "assets" / "sprites"
OUT = REPO / "design" / "character"
FRAMES = ["idle", "run_contact", "run_passing", "rise", "fall", "cast", "hurt", "fail", "win"]
RECT_W, RECT_H = 14, 44  # CHARACTER-SHEET.md, "Collision overlay"


def load_log():
    d = json.loads((SPR / "edit-log.json").read_text(encoding="utf-8"))
    return {e["asset"]: e for e in d["assets"] if e["group"] == "mage"}


def collision_rect(log):
    """Feet (anchor row) up 44 px, centred on the body. The body centre is the median column of the
    idle torso's tunic pixels, which the cleanup already put on the anchor column."""
    ax, ay = log["idle"]["anchor_out"]
    x0 = ax - RECT_W // 2
    return x0, ay - RECT_H, x0 + RECT_W, ay  # [x0, y0, x1, y1), canvas pixels


def silhouette(log):
    bg = Image.open(SPR / "env" / "cave_bg.png").convert("RGBA")
    tile = Image.open(SPR / "env" / "cave_ground_tile.png")
    W, H = bg.size
    ground_top = H - tile.height
    for x in range(0, W, tile.width):
        bg.alpha_composite(tile, (x, ground_top))
    idle = Image.open(SPR / "mage" / "mage_idle.png")
    a = np.asarray(idle).copy()
    a[a[..., 3] > 0, :3] = 0  # solid black, alpha kept
    sil = Image.fromarray(a, "RGBA")
    ax, ay = log["idle"]["anchor_out"]
    L = cs.srgb_to_lab(np.asarray(bg.convert("RGB")).reshape(-1, 3))[:, 0].reshape(H, W)
    stats = []
    for sx in (W // 5, W // 2, 4 * W // 5):  # left rock wall, dark centre, right rock wall
        px, py = sx - ax, ground_top + 1 - ay  # feet on the ledge's top row
        region = L[max(0, py):py + idle.height, max(0, px):px + idle.width]
        mask = a[: region.shape[0], : region.shape[1], 3] > 0
        stats.append({"screen_x": sx, "bg_L*_behind_median": round(float(np.median(region[mask])), 1)})
        bg.alpha_composite(sil, (px, py))
    path = OUT / "silhouette.png"
    bg.convert("RGB").save(path, optimize=True)
    return path, stats


def collision(log, rect):
    s, gap, label_h = 4, 8, 18
    ims = [Image.open(SPR / "mage" / f"mage_{n}.png") for n in FRAMES]
    w, h = ims[0].size
    sheet = Image.new("RGB", (len(ims) * (w * s + gap) + gap, h * s + 2 * gap + label_h), cs.SHEET_MID)
    d = ImageDraw.Draw(sheet)
    x0, y0, x1, y1 = rect
    rows = []
    for i, (n, im) in enumerate(zip(FRAMES, ims)):
        ox = gap + i * (w * s + gap)
        sheet.paste(im.resize((w * s, h * s), Image.NEAREST), (ox, gap), im.resize((w * s, h * s), Image.NEAREST))
        d.rectangle([ox + x0 * s, gap + y0 * s, ox + x1 * s - 1, gap + y1 * s - 1], outline=(255, 0, 230), width=2)
        d.text((ox, gap + h * s + 4), n, fill=(20, 20, 30))
        e = log[n]
        ay = e["anchor_out"][1]
        chin = ay + (e["face_bbox_src"][3] + 1 - (e["ground_y_src"] + 1)) / e["scale_src_px_per_px"]
        rows.append({"pose": n, "chin_y": round(chin, 1), "rect_top": y0, "chin_minus_rect_top_px": round(chin - y0, 1)})
    path = OUT / "collision.png"
    sheet.save(path, optimize=True)
    return path, rows


def main():
    log = load_log()
    rect = collision_rect(log)
    sp, sstats = silhouette(log)
    cp, crows = collision(log, rect)
    print(f"{sp.relative_to(REPO)}  sha256 {cs.sha256(sp)}")
    for st in sstats:
        print(f"  silhouette at x={st['screen_x']}: cave L* behind it (median) {st['bg_L*_behind_median']}  vs black L* 0")
    print(f"{cp.relative_to(REPO)}  sha256 {cs.sha256(cp)}")
    print(f"  collision rect (canvas px, [x0,y0,x1,y1)): {list(rect)} = {RECT_W}x{RECT_H}, same in every pose")
    for r in crows:
        print(f"  {r['pose']:12s} chin at y={r['chin_y']:5.1f}  -> {r['chin_minus_rect_top_px']:+5.1f} px below the rect top")


if __name__ == "__main__":
    main()
