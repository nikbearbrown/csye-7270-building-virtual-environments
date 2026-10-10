#!/usr/bin/env python3
"""Compose a 4K beat video from layers: real engine footage, real files (sprites, raw model outputs, recorded test
output) and text, each revealed at a time. Used for the film's evidence beats; nothing here draws game content.

    python3 tools/compose.py spec.json

Spec: {"out": "media/B05.mp4", "duration": 21.3, "fps": 30, "bg": "#FAF9F5", "audio": "video" | null,
       "layers": [ {"kind": "text" | "image" | "rect" | "video", ...}, ... ]}
Coordinates are pixels on the 3840 x 2160 canvas. Every layer may carry "t": [t_in, t_out] and "fade" (seconds).
  text  : text, font (serif | sans | sans-medium | mono), size, color, x, y, w (wrap width), align, spacing
  image : src, x, y, w, h, fit (contain | stretch), resample (nearest | lanczos), pad_color
  rect  : x, y, w, h, fill, outline, width, radius
  video : src, ss (source seconds), x, y, w, h, crop [x, y, w, h] in source pixels (after "pad", if given),
          pad (px of dark margin added around the source first), resample (nearest | lanczos)
          (sources are the cleaned takes from tools/clean_take.py, so frame n of a take is game frame n)
A video layer is drawn above everything listed before it. With "audio": "video" the first video layer's audio
(same span) is kept — used only for the game-sound-only beats.
"""
import json, math, os, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160
FONTS = Path(os.environ.get("ART_FONTS", "/Users/yxlh/brutalist.art/runtime/fonts"))
FONT_FILES = {
    "serif": FONTS / "EB_Garamond/static/EBGaramond-Regular.ttf",
    "serif-medium": FONTS / "EB_Garamond/static/EBGaramond-Medium.ttf",
    "serif-italic": FONTS / "EB_Garamond/static/EBGaramond-Italic.ttf",
    "sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf",
    "sans-medium": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
    "mono": FONTS / "PT_Mono/PTMono-Regular.ttf",
    "cjk": Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),   # Bao's own words, quoted in Chinese
}
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_FILES[name]), size)


def wrap(draw, text: str, f, width: int) -> list:
    lines = []
    for para in text.split("\n"):
        if not width or draw.textlength(para, font=f) <= width:   # fits: keep it as written (tables keep their spaces)
            lines.append(para)
            continue
        words, cur = para.split(" "), ""
        for w in words:
            nxt = w if not cur else cur + " " + w
            if width and draw.textlength(nxt, font=f) > width and cur:
                lines.append(cur)
                cur = w
            else:
                cur = nxt
        lines.append(cur)
    return lines


def render_text(L: dict) -> tuple:
    f = font(L.get("font", "sans"), int(L["size"]))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = wrap(probe, L["text"], f, int(L.get("w", 0)))
    lh = int(L["size"] * L.get("spacing", 1.25))
    width = int(L.get("w") or max(probe.textlength(s, font=f) for s in lines)) + 8
    height = lh * len(lines) + int(L["size"] * 0.35)
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, s in enumerate(lines):
        tw = d.textlength(s, font=f)
        x = {"left": 0, "center": (width - tw) / 2, "right": width - tw}[L.get("align", "left")]
        d.text((x, i * lh), s, font=f, fill=L.get("color", "#3D3929"))
    return im, int(L["x"]), int(L["y"])


def render_image(L: dict, base: Path) -> tuple:
    src = Image.open(base / L["src"]).convert("RGBA")
    w, h = int(L["w"]), int(L["h"])
    resample = Image.NEAREST if L.get("resample") == "nearest" else Image.LANCZOS
    if L.get("fit", "contain") == "stretch":
        im = src.resize((w, h), resample)
        ox = oy = 0
    else:
        s = min(w / src.width, h / src.height)
        if L.get("resample") == "nearest" and s >= 1:
            s = max(1, int(s))          # whole-number pixel scale keeps pixel art square
        im = src.resize((max(1, round(src.width * s)), max(1, round(src.height * s))), resample)
        ox, oy = (w - im.width) // 2, (h - im.height) // 2
    canvas = Image.new("RGBA", (w, h), L.get("pad_color", (0, 0, 0, 0)))
    canvas.alpha_composite(im, (ox, oy))
    return canvas, int(L["x"]), int(L["y"])


def render_rect(L: dict) -> tuple:
    w, h = int(L["w"]), int(L["h"])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(L.get("radius", 0)), fill=L.get("fill"),
                        outline=L.get("outline"), width=int(L.get("width", 0)))
    return im, int(L["x"]), int(L["y"])


def main() -> None:
    spec_path = Path(sys.argv[1]).resolve()
    spec = json.loads(spec_path.read_text())
    base = Path(spec.get("base", spec_path.parent)).resolve()
    out = (base / spec["out"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    dur, fps = float(spec["duration"]), int(spec.get("fps", 30))
    frames = math.ceil(dur * fps - 1e-6)    # the compiler pads, never truncates: same frame count, so no retime
    dur = frames / fps
    with tempfile.TemporaryDirectory(prefix="compose-") as tmp:
        tmp = Path(tmp)
        bg = Image.new("RGBA", (W, H), spec.get("bg", "#FAF9F5"))
        inputs, chains, last = [], [], "[0:v]"
        bg.save(tmp / "bg.png")
        inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", str(tmp / "bg.png")]
        audio_from = None
        for n, L in enumerate(spec["layers"]):
            t_in, t_out = (L.get("t") or [0, dur])
            fade = float(L.get("fade", 0.0))
            idx = len([a for a in inputs if a == "-i"])
            if L["kind"] == "video":
                src = (base / L["src"]).resolve()
                ss = float(L.get("ss", 0))
                span = t_out - t_in
                vf = []
                if L.get("pad"):            # dark margin outside the game frame, so a crop can stay centred near an edge
                    pd = int(L["pad"])
                    vf.append(f"pad=iw+{2 * pd}:ih+{2 * pd}:{pd}:{pd}:color=0x0E1020")
                if L.get("crop"):
                    cx, cy, cw, ch = L["crop"]
                    vf.append(f"crop={cw}:{ch}:{cx}:{cy}")
                flags = "neighbor" if L.get("resample") == "nearest" else "lanczos"
                vf.append(f"scale={int(L['w'])}:{int(L['h'])}:flags={flags}")
                vf.append(f"setpts=PTS-STARTPTS+{t_in}/TB")
                inputs += ["-ss", f"{ss:.4f}", "-t", f"{span + 0.5:.3f}", "-i", str(src)]
                chains.append(f"[{idx}:v]{','.join(vf)}[v{n}]")
                chains.append(f"{last}[v{n}]overlay={int(L['x'])}:{int(L['y'])}:eof_action=pass:"
                              f"enable='between(t,{t_in:.4f},{t_out:.4f})'[o{n}]")
                if spec.get("audio") == "video" and audio_from is None:
                    audio_from = idx
                last = f"[o{n}]"
                continue
            if L["kind"] == "text":
                im, x, y = render_text(L)
            elif L["kind"] == "image":
                im, x, y = render_image(L, base)
            elif L["kind"] == "rect":
                im, x, y = render_rect(L)
            else:
                raise SystemExit("unknown layer kind " + L["kind"])
            p = tmp / f"layer{n}.png"
            im.save(p)
            inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", str(p)]
            f_chain = "format=rgba"
            if fade > 0:
                f_chain += f",fade=t=in:st={t_in:.4f}:d={fade:.3f}:alpha=1"
                if t_out < dur - 0.01:
                    f_chain += f",fade=t=out:st={max(t_in, t_out - fade):.4f}:d={fade:.3f}:alpha=1"
            chains.append(f"[{idx}:v]{f_chain}[l{n}]")
            chains.append(f"{last}[l{n}]overlay={x}:{y}:enable='between(t,{t_in:.4f},{t_out:.4f})'[o{n}]")
            last = f"[o{n}]"
        chains.append(f"{last}format=yuv420p[vout]")
        cmd = [FFMPEG, "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(chains), "-map", "[vout]"]
        if audio_from is not None:
            cmd += ["-map", f"{audio_from}:a", "-c:a", "aac", "-b:a", "256k", "-ar", "48000"]
        cmd += ["-frames:v", str(frames), "-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
        if audio_from is not None:
            cmd[cmd.index("-frames:v"):cmd.index("-frames:v")] = ["-t", f"{dur:.4f}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(r.stderr[-3000:])
    print(out)


if __name__ == "__main__":
    main()
