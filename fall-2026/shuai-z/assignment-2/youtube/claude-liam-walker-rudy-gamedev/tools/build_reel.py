#!/usr/bin/env python3
"""Conform every beat to its measured narration, build the gameplay/evidence
media, and mix each beat's sound. Run after generate_audio_kokoro.py and
before remotion_scenes.py:

    python3 tools/build_reel.py [--only B07 B09]

Remotion beats: duration = lead + narration + tail, frame-aligned; cue times
are placed on the narration's own words (character position of the phrase in
the measured line); the props get durationSeconds.

Gameplay beats (shot.capture_plan): each 1.0x segment is copied frame for
frame from the hashed capture; slowed segments are labelled REPLAY and play
no game sound; if narration outlasts the footage, the last frame is held and
labelled. Nothing is sped up, centre-cut or retimed to fit a sentence. The
slice's own mix plays under the narration at game_audio_gain_db (0 dB and
no narration in the labelled B03), time-aligned with the 1.0x frames.

Each beat's audio becomes mix/beat-<ID>.wav (48 kHz stereo), named in
audio_file; compile.py takes it as that beat's sound.
"""
import argparse, json, math, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
FONTS = Path("/Users/eric/csye7270/brutalist.art/runtime/fonts")
FPS, SR, W, H = 30, 48000, 3840, 2160
NARR_LEAD = 0.3      # s of silence before narration in evidence beats
TAIL = 0.5           # s after the last word, before the cut
CHIP_Y = H - 130     # baseline row of chips, inside the 5% title-safe inset
SFX_NAMES = {"jump": "SFX-JUMP", "stomp": "SFX-STOMP", "hurt": "SFX-HURT", "portal": "SFX-PORTAL",
             "slash": "SFX-SLASH", "pickup": "SFX-PICKUP"}


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"command failed: {' '.join(map(str, cmd))}\n{r.stderr[-1500:]}")
    return r.stdout


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0


def write_wav(path, data):
    path.parent.mkdir(exist_ok=True)
    pcm = (np.clip(data, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def frames_for(seconds):
    return math.ceil(seconds * FPS - 1e-6)


def cue_time(text, phrase, lead, narr):
    i = text.lower().find(phrase.lower())
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    return round(lead + narr * i / max(len(text), 1), 2)


def chip(text, size=46, bg=(20, 18, 16, 190), fg=(255, 255, 255, 255)):
    f = ImageFont.truetype(str(FONTS / "Inter/static/Inter_28pt-Medium.ttf"), size)
    box = ImageDraw.Draw(Image.new("RGBA", (4, 4))).textbbox((0, 0), text, font=f)
    w, h = box[2] - box[0] + 48, box[3] - box[1] + 30
    img = Image.new("RGBA", (w, h), bg)
    ImageDraw.Draw(img).text((24, 15 - box[1]), text, font=f, fill=fg)
    return img


def log_rows(capture):
    rows = {}
    for line in (REEL / f"capture/{capture}-inputs.jsonl").read_text().splitlines():
        d = json.loads(line)
        if d.get("kind") == "state":
            rows[d["f"]] = d
    return rows


def build_gameplay(b, narr_path):
    plan = b["shot"]["capture_plan"]
    cap = plan["capture"]
    src = REEL / f"capture/{cap}.mp4"
    narr = decode(narr_path) if narr_path else np.zeros((0, 2), np.float32)
    nsec = len(narr) / SR
    lead = 0.0 if plan.get("no_narration") else NARR_LEAD
    # Timeline of segments in output frames.
    timeline, t = [], 0
    for s in plan["segments"]:
        n = round((s["to"] - s["from"]) / s["speed"])
        timeline.append({**s, "out_from": t, "out_frames": n}); t += n
    action = t
    need = frames_for(lead + nsec + TAIL) if nsec else action
    hold = max(0, need - action)
    total = action + hold
    dur = total / FPS
    # ---- overlays
    work = REEL / "clips_work" / b["beat_id"]; work.mkdir(parents=True, exist_ok=True)
    overlays = []   # (png, x, y, t0, t1)
    first, last = plan["segments"][0]["from"], plan["segments"][0]["to"]
    prov = chip(f"SCRIPTED INPUT · NATIVE 4K ENGINE CAPTURE · {cap} · frames {first}–{last - 1}", 40)
    p = work / "prov.png"; prov.save(p)
    overlays.append((p, W - 200 - prov.width, CHIP_Y - prov.height, 0, dur))
    y = CHIP_Y
    for i, c in enumerate(plan.get("chips", [])):
        im = chip(c, 52, bg=(217, 119, 87, 235) if "NO NARRATION" in c else (20, 18, 16, 190))
        p = work / f"chip{i}.png"; im.save(p)
        y -= im.height + 16 if i else 0
        overlays.append((p, 200, CHIP_Y - im.height - (i * (im.height + 16)), 0, dur))
    rows = log_rows(cap)
    sound_row = CHIP_Y - 2 * 110 - 30
    for s in timeline:
        if s["speed"] != 1.0:
            im = chip(s["label"], 48, bg=(61, 57, 41, 225)); p = work / f"seg{s['out_from']}.png"; im.save(p)
            overlays.append((p, W - 200 - im.width, CHIP_Y - prov.height - 16 - im.height,
                             s["out_from"] / FPS, (s["out_from"] + s["out_frames"]) / FPS))
            continue
        for f in range(s["from"], s["to"]):
            for snd in rows.get(f, {}).get("sounds", []):
                im = chip("SOUND  " + SFX_NAMES.get(snd, snd) + "  ·  Sfx.play(&\"" + snd + "\")", 50, bg=(48, 61, 52, 230))
                p = work / f"snd{f}-{snd}.png"; im.save(p)
                t0 = (s["out_from"] + f - s["from"]) / FPS
                overlays.append((p, 200, sound_row, t0, min(t0 + 1.0, dur)))
    if hold:
        im = chip(f"HELD FINAL FRAME · {hold / FPS:.1f} s · no gameplay", 48, bg=(61, 57, 41, 225)); p = work / "hold.png"; im.save(p)
        overlays.append((p, W - 200 - im.width, CHIP_Y - prov.height - 16 - im.height, action / FPS, dur))
    # ---- video graph
    parts, fc = [], []
    fc.append(f"[0:v]split={len(timeline)}" + "".join(f"[s{i}]" for i in range(len(timeline))))
    for i, s in enumerate(timeline):
        k = 1.0 / s["speed"]
        fc.append(f"[s{i}]trim=start_frame={s['from']}:end_frame={s['to']},setpts=PTS-STARTPTS"
                  + (f",setpts={k:.4f}*PTS,fps={FPS}" if s["speed"] != 1.0 else "")
                  + f",trim=end_frame={s['out_frames']},setpts=PTS-STARTPTS[g{i}]")
        parts.append(f"[g{i}]")
    fc.append("".join(parts) + f"concat=n={len(timeline)}:v=1:a=0,tpad=stop_mode=clone:stop={hold}[base]")
    prev = "base"
    inputs = ["-i", str(src)]
    for j, (png, x, yy, t0, t1) in enumerate(overlays):
        inputs += ["-i", str(png)]
        fc.append(f"[{prev}][{j + 1}:v]overlay={x}:{yy}:enable='between(t,{t0:.4f},{t1:.4f})'[o{j}]")
        prev = f"o{j}"
    out = REEL / f"media/{b['beat_id']}.mp4"; out.parent.mkdir(exist_ok=True)
    sig = json.dumps({"plan": plan, "total": total, "overlays": [(Path(o[0]).name, o[1], o[2], round(o[3], 4), round(o[4], 4)) for o in overlays],
                      "src": src.stat().st_size, "v": 1}, sort_keys=True, ensure_ascii=False)
    sig_path = work / "video-signature.json"
    cached = out.exists() and sig_path.exists() and sig_path.read_text() == sig
    if not cached:
      sh(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", f"[{prev}]",
        "-frames:v", str(total), "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "14",
        "-pix_fmt", "yuv420p", "-an", str(out)])
      sig_path.write_text(sig)
    got = int(sh(["ffprobe", "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries",
                  "stream=nb_read_frames", "-of", "csv=p=0", str(out)]).strip())
    if got != total:
        raise SystemExit(f"{b['beat_id']}: built {got} frames, planned {total}")
    # ---- audio: the slice's own mix under 1.0x frames, narration on top
    game = decode(REEL / f"capture/{cap}.wav")
    gain = 10 ** (plan.get("game_audio_gain_db", -11.0) / 20)
    mix = np.zeros((round(dur * SR), 2), np.float32)
    for s in timeline:
        if s["speed"] != 1.0:
            continue
        a0, a1 = round(s["from"] / FPS * SR), round(s["to"] / FPS * SR)
        o0 = round(s["out_from"] / FPS * SR)
        seg = game[a0:a1] * gain
        mix[o0:o0 + len(seg)] += seg[:len(mix) - o0]
    if nsec:
        o = round(lead * SR); mix[o:o + len(narr)] += narr[:len(mix) - o]
    b["shot"]["capture_plan"].update({"action_frames": action, "held_final_frames": hold, "total_frames": total})
    px, py = W - 200 - prov.width, CHIP_Y - prov.height   # the provenance chip, on every gameplay frame
    b.setdefault("qc", {}).update({
        "contrast_regions": [{"label": "provenance chip", "box": [round((px + 8) / W, 4), round((py + 4) / H, 4),
                                                                  round((px + prov.width - 8) / W, 4), round((py + prov.height - 4) / H, 4)]}],
        "contrast_reason": "Engine capture of painted game art: the whole-frame ink average measures the art, not text. The film's own essential text is its chips; the provenance chip is on every frame and is measured locally. The game's HUD and debug line are the game's own and are reviewed by eye."})
    return dur, mix


def build_still(b, narr_path):
    img = Image.open(REEL / b["shot"]["still_plan"]["image"]).convert("RGB")
    canvas = Image.new("RGB", (W, H), (250, 249, 245))
    img.thumbnail((W, H), Image.LANCZOS)
    canvas.paste(img, ((W - img.width) // 2, (H - img.height) // 2))
    work = REEL / "clips_work" / b["beat_id"]; work.mkdir(parents=True, exist_ok=True)
    frame = work / "frame.png"; canvas.save(frame)
    narr = decode(narr_path)
    total = frames_for(NARR_LEAD + len(narr) / SR + TAIL + 0.4)
    dur = total / FPS
    out = REEL / f"media/{b['beat_id']}.mp4"
    sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(frame), "-frames:v", str(total), "-r", str(FPS),
        "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", str(out)])
    mix = np.zeros((round(dur * SR), 2), np.float32)
    o = round(NARR_LEAD * SR); mix[o:o + len(narr)] += narr[:len(mix) - o]
    return dur, mix


def build_remotion(b, narr_path):
    narr = decode(narr_path)
    nsec = len(narr) / SR
    lead = float(b.get("lead_silence_s", 0.0))
    total = frames_for(lead + nsec + float(b.get("tail_s", TAIL)))
    dur = total / FPS
    mix = np.zeros((round(dur * SR), 2), np.float32)
    o = round(lead * SR); mix[o:o + len(narr)] += narr[:len(mix) - o]
    rem = b["shot"]["remotion"]; props = rem["props"]
    props["durationSeconds"] = round(dur, 4)
    text = b["narration_text"]
    if b["shot"].get("cue_phrases"):
        props["cues"] = [{"at": cue_time(text, c["phrase"], lead, nsec), "line": c["line"], "label": c["label"]}
                         for c in b["shot"]["cue_phrases"]]
    if b["shot"].get("cue_cards"):
        props["cues"] = [{"at": cue_time(text, p, lead, nsec), "card": k} for p, k in b["shot"]["cue_cards"]]
    return dur, mix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    path = REEL / "beat_sheet.json"
    sheet = json.loads(path.read_text())
    for b in sheet["beats"]:
        bid = b["beat_id"]
        if a.only and bid not in a.only:
            continue
        narr = REEL / f"mp3/beat-{bid}.mp3"
        narr = narr if b.get("narration_text") else None
        shot = b["shot"]
        if shot.get("capture_plan"):
            dur, mix = build_gameplay(b, narr)
        elif shot.get("still_plan"):
            dur, mix = build_still(b, narr)
        else:
            dur, mix = build_remotion(b, narr)
        write_wav(REEL / f"mix/beat-{bid}.wav", mix)
        b["audio_file"] = f"mix/beat-{bid}.wav"
        b["actual_duration_s"] = round(dur, 6)
        b.pop("render_duration_s", None)
        print(f"{bid:5} {dur:7.3f}s  {'gameplay' if shot.get('capture_plan') else 'still' if shot.get('still_plan') else shot['remotion']['pattern']}")
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    print("total", round(sum(b["actual_duration_s"] for b in sheet["beats"]), 2), "s")


if __name__ == "__main__":
    main()
