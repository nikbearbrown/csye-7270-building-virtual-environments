"""
scenes.py — Adding Particle Effects to Walker Claude
Manim scenes for 11 body beats (B01–B11).
Render at 3840×2160, 24 fps.
"""
from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────
STAGE    = "#F2F0E9"
INK      = "#3D3929"
TERRA    = "#D97757"
WARM     = "#C4B99A"
ACCENT2  = "#6B8F71"
GREEN_OK = "#4CAF50"
RED_ERR  = "#E53935"
BLUE_GPU = "#5B8DD9"
GREY_CPU = "#8A8A7A"
BOLD     = "BOLD"      # stub-safe: fake manim doesn't export this

config.pixel_height = 2160
config.pixel_width  = 3840
config.frame_rate   = 24
config.background_color = STAGE


def ink(t, scale=1.0, **kw):
    return Text(t, color=INK, font_size=int(52 * scale), **kw)


def label(t, scale=0.7, **kw):
    return Text(t, color=INK, font_size=int(52 * scale), **kw)


def terra(t, scale=0.9, **kw):
    return Text(t, color=TERRA, font_size=int(52 * scale), weight=BOLD, **kw)


# ── B01: Emission / Process / Draw ───────────────────────────────────
class B01_ThreePartModel(Scene):
    def construct(self):
        title = ink("The Three-Part Model", scale=1.1).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        rows = [
            ("Emission",  "amount · lifetime · one_shot · explosiveness",  "When and where particles are born",  INK),
            ("Process",   "spread · velocity · gravity · scale curve",      "How each particle moves and changes", BLUE_GPU),
            ("Draw",      "texture · blend mode · billboard · .tres",       "What each particle looks like",       ACCENT2),
        ]
        y_start = 1.4
        for i, (name, props, desc, col) in enumerate(rows):
            y = y_start - i * 1.5
            box = RoundedRectangle(width=13.0, height=1.1, corner_radius=0.1,
                                   color=col, fill_color=col, fill_opacity=0.10,
                                   stroke_width=2).move_to([0, y, 0])
            self.play(FadeIn(box), run_time=0.3)

            name_text = Text(name, color=col, font_size=48, weight=BOLD).move_to([-5.0, y + 0.18, 0])
            prop_text = label(props, scale=0.60).move_to([1.5, y + 0.18, 0])
            desc_text = label(desc, scale=0.55, slant="ITALIC").set_color(WARM).move_to([0.5, y - 0.22, 0])
            self.play(FadeIn(name_text), FadeIn(prop_text), FadeIn(desc_text), run_time=0.4)

        self.wait(0.5)


# ── B02: DeathBurst Config ───────────────────────────────────────────
class B02_DeathBurstConfig(Scene):
    def construct(self):
        title = ink("DeathBurst — Node Config", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        props_batch1 = [
            ("type",         "GPUParticles2D"),
            ("emitting",     "false"),
            ("one_shot",     "true"),
            ("explosiveness","1.0"),
        ]
        props_batch2 = [
            ("amount",       "32"),
            ("lifetime",     "0.6 s"),
            ("texture",      "GradientTexture2D  16×16 radial"),
            ("particle_flag_disable_z", "true"),
        ]
        y_start = 1.8
        row_h   = 0.72

        dots1 = []
        for i, (k, v) in enumerate(props_batch1):
            y = y_start - i * row_h
            dot = Dot([-5.0, y, 0], radius=0.10, color=TERRA)
            key_t = Text(k, color=INK, font_size=38, weight=BOLD).move_to([-2.8, y, 0])
            val_t = label(v, scale=0.65).set_color(ACCENT2).move_to([2.5, y, 0])
            dots1.append((dot, key_t, val_t))

        for dot, key_t, val_t in dots1:
            self.play(FadeIn(dot), FadeIn(key_t), FadeIn(val_t), run_time=0.3)

        dots2 = []
        y_off = y_start - len(props_batch1) * row_h
        for i, (k, v) in enumerate(props_batch2):
            y = y_off - i * row_h
            dot = Dot([-5.0, y, 0], radius=0.10, color=BLUE_GPU)
            key_t = Text(k, color=INK, font_size=38, weight=BOLD).move_to([-2.0, y, 0])
            val_t = label(v, scale=0.65).set_color(BLUE_GPU).move_to([2.5, y, 0])
            dots2.append((dot, key_t, val_t))

        for dot, key_t, val_t in dots2:
            self.play(FadeIn(dot), FadeIn(key_t), FadeIn(val_t), run_time=0.3)

        self.wait(0.5)


# ── B03: Parent Trap ─────────────────────────────────────────────────
class B03_ParentTrap(Scene):
    def construct(self):
        title = ink("Parent Trap — Player vs Main", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Left column: bad (Player parent)
        bad_box = RoundedRectangle(width=5.8, height=5.0, corner_radius=0.15,
                                   color=RED_ERR, fill_color=RED_ERR, fill_opacity=0.07,
                                   stroke_width=2).move_to([-3.5, -0.3, 0])
        self.play(FadeIn(bad_box), run_time=0.3)

        bad_header = Text("Player parent", color=RED_ERR, font_size=40, weight=BOLD).move_to([-3.5, 1.9, 0])
        self.play(FadeIn(bad_header), run_time=0.3)

        bad_lines = [
            "Player → hide()",
            "└─ DeathBurst",
            "   (hidden too)",
            "",
            "emitting == true",
            "visible == false",
        ]
        for i, line in enumerate(bad_lines):
            t = label(line, scale=0.60).set_color(RED_ERR).move_to([-3.5, 1.2 - i * 0.58, 0])
            self.play(FadeIn(t), run_time=0.2)

        # Right column: good (Main parent)
        good_box = RoundedRectangle(width=5.8, height=5.0, corner_radius=0.15,
                                    color=GREEN_OK, fill_color=GREEN_OK, fill_opacity=0.07,
                                    stroke_width=2).move_to([3.5, -0.3, 0])
        self.play(FadeIn(good_box), run_time=0.3)

        good_header = Text("Main parent", color=GREEN_OK, font_size=40, weight=BOLD).move_to([3.5, 1.9, 0])
        self.play(FadeIn(good_header), run_time=0.3)

        good_lines = [
            "Main",
            "├─ Player → hide()",
            "└─ DeathBurst",
            "   (still visible)",
            "",
            "emitting == true",
            "visible == true ✓",
        ]
        for i, line in enumerate(good_lines):
            t = label(line, scale=0.60).set_color(GREEN_OK).move_to([3.5, 1.2 - i * 0.58, 0])
            self.play(FadeIn(t), run_time=0.2)

        self.wait(0.5)


# ── B04: Nine Checks ─────────────────────────────────────────────────
class B04_NineChecks(Scene):
    def construct(self):
        title = ink("9-Check Test Spec", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        checks_batch1 = [
            "texture is GradientTexture2D",
            "particle_flag_disable_z enabled",
            "not emitting at load",
            "not emitting before hit",
            "emitting after hit",
        ]
        checks_batch2 = [
            "visible_in_tree after hit",
            "global_position == player hit position",
            "finished within lifetime + 0.5 s",
            "restarts on second death",
        ]

        y_start = 1.8
        row_h   = 0.60
        dots1 = []
        for i, check in enumerate(checks_batch1):
            y = y_start - i * row_h
            dot = Dot([-6.0, y, 0], radius=0.12, color=ACCENT2)
            t = label(check, scale=0.70).move_to([0.5, y, 0])
            dots1.append((dot, t))

        for dot, t in dots1:
            self.play(FadeIn(dot), FadeIn(t), run_time=0.3)

        y_off = y_start - len(checks_batch1) * row_h
        dots2 = []
        for i, check in enumerate(checks_batch2):
            y = y_off - i * row_h
            dot = Dot([-6.0, y, 0], radius=0.12, color=BLUE_GPU)
            t = label(check, scale=0.70).move_to([0.5, y, 0])
            dots2.append((dot, t))

        for dot, t in dots2:
            self.play(FadeIn(dot), FadeIn(t), run_time=0.3)

        caveat = label("State checks only — none establish what you see", scale=0.62, slant="ITALIC")
        caveat.set_color(WARM).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caveat), run_time=0.4)
        self.wait(0.5)


# ── B05: Session 1 Mistake ───────────────────────────────────────────
class B05_SessionOneMistake(Scene):
    def construct(self):
        title = ink("Session 1 — Prediction ≠ Output", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        headers = ["Check", "Predicted", "Real"]
        col_xs  = [-4.5, 0.0, 4.5]
        y0      = 1.8

        header_els = []
        for j, h in enumerate(headers):
            t = Text(h, color=TERRA, font_size=40, weight=BOLD).move_to([col_xs[j], y0, 0])
            header_els.append(t)
        self.play(*[FadeIn(h) for h in header_els], run_time=0.4)

        sep = Line([-6.5, y0 - 0.35, 0], [6.5, y0 - 0.35, 0], color=WARM, stroke_width=1.5)
        self.play(Create(sep), run_time=0.3)

        # Column dividers (each play → distinct shape states)
        bottom_y = -3.0
        col_seps = [(-2.4, col_xs[0], col_xs[1]), (2.2, col_xs[1], col_xs[2])]
        for cx, _, _ in col_seps:
            vl = Line([cx, y0 - 0.35, 0], [cx, bottom_y, 0], color=WARM, stroke_width=0.8)
            self.play(Create(vl), run_time=0.2)

        rows = [
            ("emitting after hit",   "FAIL",  "PASS"),
            ("visible_in_tree",      "FAIL",  "PASS"),
            ("global_position",      "FAIL",  "PASS"),
            ("finished signal",      "FAIL",  "FAIL"),
        ]
        row_h = 0.65
        for i, (check, pred, real) in enumerate(rows):
            y = y0 - (i + 1) * row_h - 0.1
            check_t = label(check, scale=0.62).move_to([col_xs[0], y, 0])
            pred_c  = RED_ERR if pred == "FAIL" else GREEN_OK
            real_c  = RED_ERR if real == "FAIL" else GREEN_OK
            pred_t  = Text(pred, color=pred_c, font_size=36).move_to([col_xs[1], y, 0])
            real_t  = Text(real, color=real_c, font_size=36).move_to([col_xs[2], y, 0])
            self.play(FadeIn(check_t), FadeIn(pred_t), FadeIn(real_t), run_time=0.3)

        note = label("2 of 3 predicted failures were wrong", scale=0.65, slant="ITALIC")
        note.set_color(RED_ERR).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


# ── B06: Lambda Bug ──────────────────────────────────────────────────
class B06_LambdaBug(Scene):
    def construct(self):
        title = ink("Lambda Capture Bug", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Outer var box
        outer_box = RoundedRectangle(width=4.5, height=1.0, corner_radius=0.1,
                                     color=INK, fill_color=INK, fill_opacity=0.08,
                                     stroke_width=2).move_to([-3.0, 1.2, 0])
        outer_label = Text("var finished = false", color=INK, font_size=36).move_to([-3.0, 1.2, 0])
        self.play(FadeIn(outer_box), FadeIn(outer_label), run_time=0.4)

        # Lambda box
        lambda_box = RoundedRectangle(width=5.5, height=2.0, corner_radius=0.1,
                                      color=TERRA, fill_color=TERRA, fill_opacity=0.08,
                                      stroke_width=2).move_to([3.0, 0.4, 0])
        lambda_label = Text("lambda copy", color=TERRA, font_size=34, weight=BOLD).move_to([3.0, 1.0, 0])
        lambda_code  = label("finished = true", scale=0.60).set_color(TERRA).move_to([3.0, 0.2, 0])
        lambda_note  = label("(own copy)", scale=0.52, slant="ITALIC").set_color(TERRA).move_to([3.0, -0.3, 0])
        self.play(FadeIn(lambda_box), FadeIn(lambda_label), FadeIn(lambda_code), FadeIn(lambda_note), run_time=0.4)

        # Arrow: outer → lambda (copy)
        copy_arrow = Arrow([-0.8, 1.2, 0], [0.25, 0.8, 0], color=WARM, stroke_width=3)
        self.play(GrowArrow(copy_arrow), run_time=0.3)

        # Signal fires
        signal_dot = Dot([3.0, -1.2, 0], radius=0.15, color=ACCENT2)
        signal_t   = label("signal fires", scale=0.62).set_color(ACCENT2).move_to([3.0, -1.6, 0])
        self.play(FadeIn(signal_dot), FadeIn(signal_t), run_time=0.3)

        # Test reads original — still false
        test_box = RoundedRectangle(width=4.5, height=1.0, corner_radius=0.1,
                                    color=RED_ERR, fill_color=RED_ERR, fill_opacity=0.08,
                                    stroke_width=2).move_to([-3.0, -1.3, 0])
        test_t   = Text("test reads: false  ✗", color=RED_ERR, font_size=36).move_to([-3.0, -1.3, 0])
        self.play(FadeIn(test_box), FadeIn(test_t), run_time=0.4)

        self.wait(0.5)


# ── B07: Two Silent Defects ──────────────────────────────────────────
class B07_SilentDefects(Scene):
    def construct(self):
        title = ink("Two Silent Defects", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Panel 1: null texture
        box1 = RoundedRectangle(width=6.0, height=4.2, corner_radius=0.15,
                                color=RED_ERR, fill_color=RED_ERR, fill_opacity=0.06,
                                stroke_width=2).move_to([-3.3, -0.2, 0])
        self.play(FadeIn(box1), run_time=0.3)

        p1_header = Text("Defect 1: null texture", color=RED_ERR, font_size=38, weight=BOLD).move_to([-3.3, 1.6, 0])
        p1_prob   = label("texture = null\n→ draws 1×1-pixel squares", scale=0.60).set_color(INK).move_to([-3.3, 0.6, 0])
        p1_fix    = label("Fix: GradientTexture2D\n16×16, radial fill", scale=0.60).set_color(GREEN_OK).move_to([-3.3, -0.6, 0])
        p1_note   = label("6/7 checks passed\non 1-pixel particles", scale=0.55, slant="ITALIC").set_color(WARM).move_to([-3.3, -1.6, 0])
        self.play(FadeIn(p1_header), FadeIn(p1_prob), run_time=0.3)
        self.play(FadeIn(p1_fix), FadeIn(p1_note), run_time=0.3)

        # Panel 2: Disable Z
        box2 = RoundedRectangle(width=6.0, height=4.2, corner_radius=0.15,
                                color=TERRA, fill_color=TERRA, fill_opacity=0.06,
                                stroke_width=2).move_to([3.3, -0.2, 0])
        self.play(FadeIn(box2), run_time=0.3)

        p2_header = Text("Defect 2: Disable Z off", color=TERRA, font_size=38, weight=BOLD).move_to([3.3, 1.6, 0])
        p2_prob   = label("particle_flag_disable_z\ndefaults to false in 3D\nmaterial", scale=0.60).set_color(INK).move_to([3.3, 0.5, 0])
        p2_fix    = label("Fix: particle_flag_disable_z\n= true", scale=0.60).set_color(GREEN_OK).move_to([3.3, -0.6, 0])
        p2_note   = label("Found in docs,\nnot in tests", scale=0.55, slant="ITALIC").set_color(WARM).move_to([3.3, -1.6, 0])
        self.play(FadeIn(p2_header), FadeIn(p2_prob), run_time=0.3)
        self.play(FadeIn(p2_fix), FadeIn(p2_note), run_time=0.3)

        self.wait(0.5)


# ── B08: Sleep Output ────────────────────────────────────────────────
class B08_SleepOutput(Scene):
    def construct(self):
        title = ink("Cost Script Without --fixed-fps", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        rows = [
            ("Empty scene baseline",         "6.900 ms"),
            ("GPUParticles2D  amount=50000",  "6.899 ms"),
            ("CPUParticles2D  amount=1000",   "6.898 ms"),
            ("CPUParticles2D  amount=50000",  "6.899 ms"),
        ]

        y_start = 1.5
        row_h   = 0.72
        dots = []
        for i, (case, cost) in enumerate(rows):
            y = y_start - i * row_h
            dot = Dot([-6.0, y, 0], radius=0.12, color=WARM)
            case_t = label(case, scale=0.62).move_to([-1.5, y, 0])
            cost_t = Text(cost, color=TERRA, font_size=38, weight=BOLD).move_to([4.5, y, 0])
            dots.append((dot, case_t, cost_t))

        for dot, case_t, cost_t in dots:
            self.play(FadeIn(dot), FadeIn(case_t), FadeIn(cost_t), run_time=0.3)

        verdict = label("This is a sleep, not particle cost", scale=0.75, slant="ITALIC")
        verdict.set_color(RED_ERR).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(verdict), run_time=0.4)
        self.wait(0.5)


# ── B09: Fixed-FPS Cost Table ────────────────────────────────────────
class B09_FixedFpsTable(Scene):
    def construct(self):
        title = ink("Fixed-FPS 60 — Real CPU Cost", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        headers = ["Emitter", "1 000", "10 000", "50 000"]
        col_xs  = [-4.8, -0.8, 1.8, 4.4]
        y0      = 1.8

        header_els = []
        for j, h in enumerate(headers):
            t = Text(h, color=TERRA, font_size=38, weight=BOLD).move_to([col_xs[j], y0, 0])
            header_els.append(t)
        self.play(*[FadeIn(h) for h in header_els], run_time=0.4)

        sep = Line([-6.5, y0 - 0.35, 0], [6.5, y0 - 0.35, 0], color=WARM, stroke_width=1.5)
        self.play(Create(sep), run_time=0.3)

        # Column dividers (each play → distinct shape states)
        bottom_y = -3.0
        col_seps_xs = [-2.8, 0.5, 3.1]
        for cx in col_seps_xs:
            vl = Line([cx, y0 - 0.35, 0], [cx, bottom_y, 0], color=WARM, stroke_width=0.8)
            self.play(Create(vl), run_time=0.2)

        rows = [
            ("Empty scene",      "0.002 ms",  "",          ""),
            ("GPUParticles2D",   "0.002 ms",  "0.002 ms",  "0.002 ms"),
            ("CPUParticles2D",   "0.035 ms",  "0.33 ms",   "1.61 ms"),
        ]
        row_cols = [INK, BLUE_GPU, GREY_CPU]
        row_h = 0.70
        for i, (row, col) in enumerate(zip(rows, row_cols)):
            y = y0 - (i + 1) * row_h - 0.1
            name_t = Text(row[0], color=col, font_size=36, weight=BOLD).move_to([col_xs[0], y, 0])
            cells  = [label(v, scale=0.65).set_color(col).move_to([col_xs[j+1], y, 0]) for j, v in enumerate(row[1:])]
            self.play(FadeIn(name_t), *[FadeIn(c) for c in cells], run_time=0.3)

        note = label("~0.032 µs per CPUParticles particle per frame", scale=0.62, slant="ITALIC")
        note.set_color(WARM).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


# ── B10: Headless Limits ─────────────────────────────────────────────
class B10_HeadlessLimits(Scene):
    def construct(self):
        title = ink("What 9/9 PASS Did Not Prove", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        items_batch1 = [
            "Whether the burst is visible against the background",
            "Whether the speed reads as a death on screen",
        ]
        items_batch2 = [
            "Whether the gradient looks round at the edges",
            "What any of it costs on a real GPU",
        ]

        y_start = 1.4
        row_h   = 1.0

        crosses1 = []
        for i, item in enumerate(items_batch1):
            y = y_start - i * row_h
            x = Cross(stroke_color=RED_ERR, stroke_width=5).scale(0.22).move_to([-5.5, y, 0])
            t = label(item, scale=0.70).move_to([0.8, y, 0])
            crosses1.append((x, t))

        for x, t in crosses1:
            self.play(FadeIn(x), FadeIn(t), run_time=0.35)

        y_off = y_start - len(items_batch1) * row_h
        crosses2 = []
        for i, item in enumerate(items_batch2):
            y = y_off - i * row_h
            x = Cross(stroke_color=RED_ERR, stroke_width=5).scale(0.22).move_to([-5.5, y, 0])
            t = label(item, scale=0.70).move_to([0.8, y, 0])
            crosses2.append((x, t))

        for x, t in crosses2:
            self.play(FadeIn(x), FadeIn(t), run_time=0.35)

        verdict = label("Only a person at a screen can establish these", scale=0.68, slant="ITALIC")
        verdict.set_color(TERRA).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(verdict), run_time=0.4)
        self.wait(0.5)


# ── B11: Engine Map ──────────────────────────────────────────────────
class B11_EngineMap(Scene):
    def construct(self):
        title = ink("One-Shot Burst — Three Engines", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        headers = ["Concept", "Godot", "Unity Built-in", "Unreal Niagara"]
        col_xs  = [-5.0, -1.2, 1.8, 4.8]
        col_w   = 3.0
        y0      = 1.9

        header_els = []
        for j, h in enumerate(headers):
            t = Text(h, color=TERRA, font_size=36, weight=BOLD).move_to([col_xs[j], y0, 0])
            header_els.append(t)
        self.play(*[FadeIn(h) for h in header_els], run_time=0.4)

        sep = Line([-6.5, y0 - 0.35, 0], [6.5, y0 - 0.35, 0], color=WARM, stroke_width=1.5)
        self.play(Create(sep), run_time=0.3)

        # Column separators for distinct shape states
        for j in range(1, len(headers)):
            cx = col_xs[j] - col_w / 2
            vl = Line([cx, y0 - 0.35, 0], [cx, -3.0, 0], color=WARM, stroke_width=0.8)
            self.play(Create(vl), run_time=0.2)

        rows = [
            ("one_shot",        "one_shot = true",       "Looping off",             "Loop Behavior Once"),
            ("burst amount",    "amount + explosiveness=1","Burst at t=0, Count N",  "Spawn Burst Instantaneous"),
            ("restart",         "restart()",              "Play()",                  "ResetSystem() / Activate"),
            ("finished",        "finished signal",        "OnParticleSystemStopped", "OnSystemFinished"),
            ("scene format",    ".tscn (text, diffable)", "YAML .prefab",            ".uasset (binary)"),
        ]
        row_h = 0.68
        for i, row in enumerate(rows):
            y = y0 - (i + 1) * row_h - 0.1
            for j, cell in enumerate(row):
                fs = 33 if j == 0 else 29
                col = TERRA if j == 0 else (GREEN_OK if j == 1 else INK)
                t = Text(cell, color=col, font_size=fs).move_to([col_xs[j], y, 0])
                self.play(FadeIn(t), run_time=0.2)

        self.wait(0.5)
