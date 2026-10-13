#!/usr/bin/env python3
"""Act IV pantry assets (all reproducible, nothing invented):
  pantry/a4_shell_install_addon.png  B34: the toolkit's CCPlainShell (a plain terminal skin) showing the assignment's step-3 command,
                                     WITHOUT output, titled "documented, not run" (rendered by Remotion, then cropped to the window's top)
  pantry/a4_edit_menu_prefs.png      B34: crop of the REAL Blender 5.1.2 Edit menu capture (ev_bl_edit_menu.png): "Lock Object Modes" and
                                     the highlighted "Preferences..." row (box 13,960..731,1196 px, see evidence/gui/NOTES.md E11)
  pantry/a4_prefs_addons_tab.png     B34: crop of the REAL Preferences capture (ev_bl_prefs_addons.png): the left column's
                                     "Get Extensions" / "Add-ons" (selected) / "Themes" (box 0,690..640,1050 px; Add-ons button 36,843,605,938)
Run from the reel folder:  python3 evidence/act4/make_assets.py
"""
import json, subprocess, pathlib
from PIL import Image

REEL = pathlib.Path(__file__).resolve().parents[2]
PAN = REEL / "pantry"
RM = pathlib.Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion")
TMP = pathlib.Path("/private/tmp/claude-501/a4scratch"); TMP.mkdir(parents=True, exist_ok=True)

# 1. B34 shell: CCPlainShell, two lines, no output. Rendered at scale 2 (one still frame) so the crop stays sharp when enlarged.
props = {"title": "documented, not run", "lines": ["# step 3: install the add-on", "$ uvx mcp-for-blender install-addon"],
         "startCue": 4, "lineGap": 10, "durationSeconds": 3}
pf = TMP / "a4_shell_props.json"; pf.write_text(json.dumps(props))
full = TMP / "a4_shell_full.png"
subprocess.run(["npx", "remotion", "still", "src/index.ts", "CCPlainShell", str(full), "--frame=60", f"--props={pf}", "--scale=2"],
               cwd=RM, check=True, capture_output=True)
im = Image.open(full)                          # 3840 x 2160: window at x 280..3560, title bar from y 136
im.crop((280, 136, 3560, 580)).save(PAN / "a4_shell_install_addon.png")

# 2. B34: the real Edit menu, bottom rows (Lock Object Modes, Preferences...)
Image.open(PAN / "ev_bl_edit_menu.png").crop((13, 960, 731, 1196)).save(PAN / "a4_edit_menu_prefs.png")

# 3. B34: the real Preferences window's left column around the Add-ons tab
Image.open(PAN / "ev_bl_prefs_addons.png").crop((0, 690, 640, 1050)).save(PAN / "a4_prefs_addons_tab.png")

for n in ("a4_shell_install_addon.png", "a4_edit_menu_prefs.png", "a4_prefs_addons_tab.png"):
    print(n, Image.open(PAN / n).size)
