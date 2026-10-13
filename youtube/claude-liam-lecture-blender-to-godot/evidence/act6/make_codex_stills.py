#!/usr/bin/env python3
"""make_codex_stills.py — renders the Codex-template stills of Act V part 2 (B64-B66) from REAL transcript text.

  python3 evidence/act6/make_codex_stills.py          (run from the REEL folder; needs the TK Remotion project, Node, Pillow)

Everything displayed comes from:
  * examples/03-blender-mcp-to-godot/PROMPTS.md          the Codex prompt, exactly as run  -> evidence/act6/prompt2_codex.txt
  * examples/03-blender-mcp-to-godot/transcripts/run2-codex.jsonl   (item numbers below are line indexes in that file, 0-based)
The library components (CodexComposerAsk, CodexWindow, CodexCodeBeat) are the templates in TK/runtime/remotion; they are fed props only.
Template chrome that is not from the run is kept to what the template needs (sidebar labels, 'codex result' bar); the strings that
ARE ours are listed in REEL/SESSION-act6.md under 'labels'.  Stills are rendered on a 1280 x 720 composition at --scale=4.5 (5760 x 3240) so the Manim beats can
zoom into them and keep the type above the GATE T floor.  Output: pantry/a6_codex_*.png
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image

REEL = Path(__file__).resolve().parents[2]
EX = REEL.parent.parent / "examples" / "03-blender-mcp-to-godot"
RM = REEL.parents[2] / "brutalist.art" / "runtime" / "remotion"
TMP = Path("/private/tmp/claude-501/act6-rm"); TMP.mkdir(parents=True, exist_ok=True)

# ── the prompt, exactly as run ──
md = (EX / "PROMPTS.md").read_text()
blk = md[md.index("## Run 2 — Codex CLI"):]
prompt = re.search(r"```text\n(.*?)\n```", blk, re.S).group(1)
(REEL / "evidence/act6/prompt2_codex.txt").write_text(prompt + "\n")

# ── the transcript lines we display ──
tr = [json.loads(l) for l in (EX / "transcripts/run2-codex.jsonl").read_text().splitlines()]
query = tr[11]["item"]["action"]["query"]                                  # web_search, completed
msg_docs = tr[20]["item"]["text"].split(". ")[0] + "."                      # agent_message item_10, first sentence
msg_hull = tr[29]["item"]["text"][tr[29]["item"]["text"].index("I’ve also changed"):]   # agent_message item_15, last sentence
fc = [(c["kind"], c["path"].split("walker-3d-platformer-asset/")[-1]) for c in tr[24]["item"]["changes"]]   # file_change item_12 (completed)
upd = [f"{k}  {p}" for k, p in fc if k == "update"]
assert "godot/props/checkpoint_post.glb.import" in upd[0] and "tools/blender/build_checkpoint_post.py" in upd[1], upd
tool = tr[44]["item"]
assert tool["server"] == "cua_repl" and tool["tool"] == "js"
tool_title = tool["arguments"]["title"]; tool_code = tool["arguments"]["code"]
refusal = tool["result"]["content"][0]["text"]; assert refusal == "Computer Use was not approved to use Blender"

props = {
    "ask": ("CodexComposerAsk", {"command": prompt, "topic": "CODEX CLI 0.153.4", "segment": "", "workspace": "walker-3d-platformer-asset",
                                 "runningText": "", "output": [], "modelLabel": "gpt-5.6-sol", "modeLabel": "workspace-write"}),
    "found": ("CodexWindow", {"view": "report", "title": "codex exec", "heading": "item.completed",
                              "lines": ["web_search: " + query, msg_docs, upd[0], upd[1], msg_hull],
                              "workspace": "walker-3d-platformer-asset", "statusLine": "item.completed"}),
    "tool_a": ("CodexCodeBeat", {"title": tool_title, "language": "cua_repl · js", "code": tool_code, "command": "", "statusLine": ""}),
    "tool_b": ("CodexCodeBeat", {"title": tool_title, "language": "cua_repl · js", "code": tool_code, "command": "", "statusLine": refusal}),
}
for name, (comp, p) in props.items():
    pj = TMP / f"{name}.json"; pj.write_text(json.dumps(p))
    out = TMP / f"a6_codex_{name}_raw.png"
    r = subprocess.run(["npx", "remotion", "still", "src/index.ts", comp, str(out), "--frame=150", "--scale=4.5", "--width=1280", "--height=720", f"--props={pj}"],
                       cwd=RM, capture_output=True, text=True, timeout=600)
    assert out.exists(), r.stderr[-500:]
    print("rendered", out.name)

S = 4.5   # remotion --scale on a 1280 x 720 composition override -> 5760 x 3240
def crop(img, box): return img.crop(tuple(int(round(v * S)) for v in box))

P = REEL / "pantry"
# the composer window: the app window only (the template insets it 5 % on the page)
im = Image.open(TMP / "a6_codex_ask_raw.png").convert("RGB")
ask = crop(im, (64, 36, 1216, 684))
# the template draws a stray status dot (its empty 'running' line) above the prompt box; paint that one dot out with the page colour
from PIL import ImageDraw
ImageDraw.Draw(ask).rectangle((1576, 273, 1628, 318), fill=(247, 247, 245))
ask.save(P / "a6_codex_ask.png")
# the report window: the top of the window that holds the content (the template leaves the rest empty)
im = Image.open(TMP / "a6_codex_found_raw.png").convert("RGB")
crop(im, (0, 0, 1280, 455)).save(P / "a6_codex_found.png")
# the tool-call card: header + the code line + the status bar + the card's lower edge (the empty middle of the dark card is cut)
for n in ("tool_a", "tool_b"):
    im = Image.open(TMP / f"a6_codex_{n}_raw.png").convert("RGB")
    top = crop(im, (89.6, 79.2, 1190.4, 190)); mid = crop(im, (89.6, 508, 1190.4, 572)); bot = crop(im, (89.6, 618, 1190.4, 640.8))
    out = Image.new("RGB", (top.width, top.height + mid.height + bot.height), (17, 17, 17))
    out.paste(top, (0, 0)); out.paste(mid, (0, top.height)); out.paste(bot, (0, top.height + mid.height))
    out.save(P / f"a6_codex_{n}.png")
for n in ("ask", "found", "tool_a", "tool_b"):
    print(n, Image.open(P / f"a6_codex_{n}.png").size)
