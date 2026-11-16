"""
scenes.py — A Practical Godot VFX Library
Manim scenes for 11 body beats (B01–B11).
Render at 3840×2160, 24 fps.
"""
from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────
STAGE   = "#F2F0E9"
INK     = "#3D3929"
TERRA   = "#D97757"
WARM    = "#C4B99A"
ACCENT2 = "#6B8F71"
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


def terra(t, scale=1.0, **kw):
    return Text(t, color=TERRA, font_size=int(52 * scale), **kw)


# ── B01: 2D Catalog ──────────────────────────────────────────────────
class B01_TwoDCatalog(Scene):
    def construct(self):
        title = ink("2d/particles — Godot Demo Catalog", scale=1.1).to_edge(UP, buff=0.5)
        sub = label("17 GPUParticles2D nodes · Mobile renderer · commit a3b5c113", scale=0.75)
        sub.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)

        effects = [
            "fountain", "fire", "trail", "sparks", "smoke",
            "galaxy", "flame thrower", "laser", "rain", "snow",
            "magic circle", "shockwave", "confetti", "comet", "debris",
            "aura", "meteor",
        ]
        cols = 3
        rows = 6
        dots = []
        labels = []
        x_start, y_start = -4.5, 1.8
        col_w, row_h = 3.2, 0.52
        for i, name in enumerate(effects):
            col = i % cols
            row = i // cols
            x = x_start + col * col_w
            y = y_start - row * row_h
            d = Dot([x, y, 0], radius=0.13, color=BLUE_GPU)
            t = label(name, scale=0.65).next_to(d, RIGHT, buff=0.18)
            dots.append(d)
            labels.append(t)

        # Reveal in two batches
        batch1 = dots[:9] + labels[:9]
        batch2 = dots[9:] + labels[9:]
        self.play(*[FadeIn(o) for o in batch1], run_time=0.6)
        self.play(*[FadeIn(o) for o in batch2], run_time=0.6)

        note = label("Every node is a readable .tscn — port directly", scale=0.7, slant="ITALIC")
        note.set_color(TERRA).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


# ── B02: 3D Catalog ──────────────────────────────────────────────────
class B02_ThreeDCatalog(Scene):
    def construct(self):
        title = ink("3d/particles — Forward Plus Features", scale=1.1).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        features = [
            ("trail_enabled",     "GPU nodes only — particle trails",      BLUE_GPU),
            ("SDF collision",     "particles bounce off geometry",          ACCENT2),
            ("attractors",        "velocity fields across all particles",   TERRA),
            ("sub_emitter",       "spawn second system at particle events", BLUE_GPU),
        ]
        y0 = 1.6
        boxes = []
        for i, (name, desc, col) in enumerate(features):
            y = y0 - i * 1.1
            box = RoundedRectangle(width=9.0, height=0.85, corner_radius=0.1,
                                   color=col, fill_color=col, fill_opacity=0.12,
                                   stroke_width=2.5).move_to([0, y, 0])
            n_text = Text(name, color=col, font_size=46, weight=BOLD).move_to([-3.5, y, 0])
            d_text = label(desc, scale=0.72).move_to([2.5, y, 0])
            boxes.append((box, n_text, d_text))

        for box, n_text, d_text in boxes:
            self.play(FadeIn(box), FadeIn(n_text), FadeIn(d_text), run_time=0.4)

        note = label("Compatibility: trails and SDF collision unsupported", scale=0.72, slant="ITALIC")
        note.set_color(RED_ERR).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


# ── B03: Three-Part Frame ────────────────────────────────────────────
class B03_ThreePartFrame(Scene):
    def construct(self):
        title = ink("The Three-Part Frame — What Ports Where", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        cols_data = [
            ("Emission",   INK,    "amount · lifetime\nexplosiveness · one_shot\nlocal_coords · fixed_fps",
             "Ports CPU ↔ GPU"),
            ("Process",    BLUE_GPU, "velocity · gravity\nspread · turbulence\n(sub_emitter: GPU only\nshaders: GPU only)",
             "CPU→GPU: gains features\nGPU→CPU: loses sub/trails/shaders"),
            ("Draw",       ACCENT2, "texture · blend mode\nbillboard · proximity_fade\n.tres file",
             "Ports anywhere — independent"),
        ]
        col_w = 4.2
        x_positions = [-4.2, 0, 4.2]
        rect_top = 1.8

        for i, (name, col, body, note) in enumerate(cols_data):
            x = x_positions[i]
            header_box = Rectangle(width=col_w - 0.2, height=0.7, color=col,
                                   fill_color=col, fill_opacity=0.2,
                                   stroke_width=2).move_to([x, rect_top, 0])
            header_text = Text(name, color=col, font_size=50, weight=BOLD).move_to([x, rect_top, 0])
            body_text = label(body, scale=0.68).move_to([x, rect_top - 1.5, 0])
            note_text = label(note, scale=0.60, slant="ITALIC").set_color(col).move_to([x, rect_top - 3.0, 0])

            self.play(FadeIn(header_box), FadeIn(header_text), run_time=0.3)
            self.play(FadeIn(body_text), run_time=0.3)
            self.play(FadeIn(note_text), run_time=0.3)

        self.wait(0.5)


# ── B04: CPU→GPU Conversion ──────────────────────────────────────────
class B04_CPUToGPU(Scene):
    def construct(self):
        title = ink("CPU → GPU: What the Conversion Preserves", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Left: CPU node properties
        cpu_box = RoundedRectangle(width=5.2, height=5.0, corner_radius=0.15,
                                    color=GREY_CPU, fill_color=GREY_CPU, fill_opacity=0.1,
                                    stroke_width=2).move_to([-3.2, -0.3, 0])
        cpu_label_t = Text("CPUParticles2D", color=GREY_CPU, font_size=40, weight=BOLD)
        cpu_label_t.move_to(cpu_box.get_top() + DOWN * 0.45)

        preserved = ["amount", "lifetime", "explosiveness", "one_shot", "local_coords", "fixed_fps",
                     "spread", "velocity range", "gravity", "lifetime_randomness"]
        self.play(FadeIn(cpu_box), FadeIn(cpu_label_t), run_time=0.4)
        preserved_items = []
        for i, prop in enumerate(preserved):
            d = Dot([-5.2, 1.4 - i * 0.44, 0], radius=0.10, color=GREY_CPU)
            t = label(prop, scale=0.65).next_to(d, RIGHT, buff=0.15)
            preserved_items.append((d, t))
        self.play(*[FadeIn(d) for d, t in preserved_items[:5]],
                  *[FadeIn(t) for d, t in preserved_items[:5]], run_time=0.4)
        self.play(*[FadeIn(d) for d, t in preserved_items[5:]],
                  *[FadeIn(t) for d, t in preserved_items[5:]], run_time=0.4)

        # Arrow
        arrow = Arrow([-0.4, -0.3, 0], [0.8, -0.3, 0], color=TERRA, buff=0, stroke_width=6)
        self.play(GrowArrow(arrow), run_time=0.4)

        # Right: GPU node
        gpu_box = RoundedRectangle(width=5.2, height=5.0, corner_radius=0.15,
                                    color=BLUE_GPU, fill_color=BLUE_GPU, fill_opacity=0.1,
                                    stroke_width=2).move_to([3.2, -0.3, 0])
        gpu_label_t = Text("GPUParticles2D", color=BLUE_GPU, font_size=40, weight=BOLD)
        gpu_label_t.move_to(gpu_box.get_top() + DOWN * 0.45)
        self.play(FadeIn(gpu_box), FadeIn(gpu_label_t), run_time=0.4)

        gained = [("+ sub_emitter", BLUE_GPU), ("+ trail_enabled", BLUE_GPU),
                  ("+ particle shaders", BLUE_GPU), ("+ process material", BLUE_GPU),
                  ("  (turbulence, attractors,", BLUE_GPU), ("   SDF collision)", BLUE_GPU)]
        for i, (g, col) in enumerate(gained):
            t = label(g, scale=0.65).set_color(col).move_to([3.2, 1.3 - i * 0.44, 0])
            self.play(FadeIn(t), run_time=0.25)

        self.wait(0.5)


# ── B05: GPU→CPU Losses ──────────────────────────────────────────────
class B05_GPUToCPU(Scene):
    def construct(self):
        title = ink("GPU → CPU: What's Lost", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        lost_items = [
            "sub_emitter",
            "trail_enabled",
            "particle shaders",
            "process material turbulence",
            "attractors",
            "SDF collision",
        ]
        y0 = 1.6
        crosses = []
        texts = []
        for i, item in enumerate(lost_items):
            y = y0 - i * 0.65
            cross = Cross(color=RED_ERR, stroke_width=5).scale(0.22).move_to([-4.0, y, 0])
            t = label(item, scale=0.85).next_to(cross, RIGHT, buff=0.3)
            crosses.append(cross)
            texts.append(t)

        self.play(*[FadeIn(t) for t in texts[:3]], run_time=0.5)
        self.play(*[FadeIn(c) for c in crosses[:3]], run_time=0.4)
        self.play(*[FadeIn(t) for t in texts[3:]], run_time=0.5)
        self.play(*[FadeIn(c) for c in crosses[3:]], run_time=0.4)

        note = label("GPU → CPU is not the same effect on wider hardware.\nIt is a simpler effect.", scale=0.78)
        note.set_color(TERRA).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


# ── B06: Compatibility Map ───────────────────────────────────────────
class B06_CompatibilityMap(Scene):
    def construct(self):
        title = ink("Renderer × Feature Support", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        renderers = ["Compatibility", "Mobile", "Forward+"]
        features  = ["particle trails", "SDF collision", "emit_particle()", "sub_emitter"]
        check = "✓"
        cross = "✗"
        table_data = [
            [cross, cross, cross, check],  # Compatibility
            [check, check, check, check],  # Mobile
            [check, check, check, check],  # Forward+
        ]
        colors = {check: GREEN_OK, cross: RED_ERR}

        col_w = 3.0
        row_h = 0.65
        x0 = -4.5
        y0 = 1.5

        # Header row — renderer names
        ren_texts = []
        for j, r in enumerate(renderers):
            t = label(r, scale=0.72, weight=BOLD).move_to([x0 + (j + 1) * col_w, y0, 0])
            ren_texts.append(t)
        self.play(*[FadeIn(t) for t in ren_texts], run_time=0.4)

        # Feature rows
        for i, feat in enumerate(features):
            y = y0 - (i + 1) * row_h
            feat_t = label(feat, scale=0.70).move_to([x0 + 0.5 * col_w, y, 0])
            row_marks = []
            for j, mark in enumerate(table_data):
                cell = label(mark[i], scale=0.85).set_color(colors[mark[i]])
                cell.move_to([x0 + (j + 1) * col_w, y, 0])
                row_marks.append(cell)
            self.play(FadeIn(feat_t), *[FadeIn(m) for m in row_marks], run_time=0.4)

        self.wait(0.5)


# ── B07: Unity Comparison ───────────────────────────────────────────
class B07_UnityComparison(Scene):
    def construct(self):
        title = ink("Unity vs Godot: Particle Systems", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        rows = [
            ("CPU / GPU",     "Built-in (CPU)",    "VFX Graph (GPU)",   "GPU nodes / CPU nodes"),
            ("File format",   "YAML (.prefab)",    "Binary (.vfx)",     "Text (.tscn)"),
            ("Agent can read","yes — text diff",   "no — binary",       "yes — text diff"),
            ("one_shot equiv","Looping off",        "Loop Behavior Once","one_shot = true"),
            ("finished equiv","OnParticleSystemStopped","OnSystemFinished(?)","finished signal"),
            ("sub-emitter",   "Sub Emitters module","Events (GPU exp.)", "sub_emitter (GPU only)"),
        ]
        headers = ["Feature", "Unity Built-in", "Unity VFX Graph", "Godot"]
        col_w = 3.5
        row_h = 0.58
        x0 = -5.5
        y0 = 1.8

        # Headers
        header_els = []
        for j, h in enumerate(headers):
            t = Text(h, color=TERRA, font_size=38, weight=BOLD)
            t.move_to([x0 + j * col_w, y0, 0])
            header_els.append(t)
        self.play(*[FadeIn(h) for h in header_els], run_time=0.4)

        # Separator
        line = Line([-7, y0 - 0.35, 0], [7, y0 - 0.35, 0], color=WARM, stroke_width=1.5)
        self.play(Create(line), run_time=0.3)

        # Column dividers (each in its own play → distinct shape states)
        bottom_y = y0 - (len(rows) + 1) * row_h - 0.2
        for j in range(1, len(headers)):
            cx = x0 + j * col_w - col_w / 2
            vl = Line([cx, y0 - 0.35, 0], [cx, bottom_y, 0], color=WARM, stroke_width=0.8)
            self.play(Create(vl), run_time=0.2)

        # Data rows
        for i, row in enumerate(rows):
            y = y0 - (i + 1) * row_h - 0.1
            row_els = []
            for j, cell in enumerate(row):
                fs = 34 if j == 0 else 30
                t = Text(cell, color=INK, font_size=fs)
                t.move_to([x0 + j * col_w, y, 0])
                row_els.append(t)
            self.play(*[FadeIn(el) for el in row_els], run_time=0.3)

        self.wait(0.5)


# ── B08: Unreal Niagara ──────────────────────────────────────────────
class B08_UnrealNiagara(Scene):
    def construct(self):
        title = ink("Unreal Niagara vs Godot", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        rows = [
            ("CPU / GPU",    "Sim Target per emitter",   "CPU nodes / GPU nodes"),
            ("File format",  "Binary (.uasset)",          "Text (.tscn + .tres)"),
            ("Agent reads",  "spawn C++ / Python script", "reads .tscn directly"),
            ("one_shot",     "Loop Behavior Once",        "one_shot = true"),
            ("finished",     "OnSystemFinished",          "finished signal"),
            ("sub-emitter",  "Events (CPU only)",         "sub_emitter (GPU only)"),
            ("fixed bounds", "required for GPU sim",      "visibility_aabb"),
        ]
        headers = ["Feature", "Unreal Niagara", "Godot"]
        col_w = 4.5
        row_h = 0.60
        x0 = -4.5
        y0 = 1.9

        header_els = []
        for j, h in enumerate(headers):
            t = Text(h, color=TERRA, font_size=40, weight=BOLD)
            t.move_to([x0 + j * col_w, y0, 0])
            header_els.append(t)
        self.play(*[FadeIn(h) for h in header_els], run_time=0.4)

        line = Line([-7, y0 - 0.35, 0], [7, y0 - 0.35, 0], color=WARM, stroke_width=1.5)
        self.play(Create(line), run_time=0.3)

        # Column dividers (each in its own play → distinct shape states)
        bottom_y = y0 - (len(rows) + 1) * row_h - 0.2
        for j in range(1, len(headers)):
            cx = x0 + j * col_w - col_w / 2
            vl = Line([cx, y0 - 0.35, 0], [cx, bottom_y, 0], color=WARM, stroke_width=0.8)
            self.play(Create(vl), run_time=0.2)

        for i, row in enumerate(rows):
            y = y0 - (i + 1) * row_h - 0.1
            row_els = []
            for j, cell in enumerate(row):
                fs = 36 if j == 0 else 32
                t = Text(cell, color=INK, font_size=fs)
                t.move_to([x0 + j * col_w, y, 0])
                row_els.append(t)
            self.play(*[FadeIn(el) for el in row_els], run_time=0.3)

        self.wait(0.5)


# ── B09: .tscn Advantage ─────────────────────────────────────────────
class B09_TscnAdvantage(Scene):
    def construct(self):
        title = ink("File Format → Agent Reach", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        engines = [
            ("Godot",  "Text (.tscn / .tres)",  "reads, diffs, verifies properties", GREEN_OK),
            ("Unity Built-in", "YAML (.prefab)", "reads and diffs",                   ACCENT2),
            ("Unity VFX Graph","Binary (.vfx)",  "cannot read effect stack",          RED_ERR),
            ("Unreal Niagara", "Binary (.uasset)","cannot read effect stack",         RED_ERR),
        ]
        y0 = 1.5
        boxes = []
        for i, (engine, fmt, reach, col) in enumerate(engines):
            y = y0 - i * 1.05
            box = RoundedRectangle(width=12.0, height=0.82, corner_radius=0.1,
                                   color=col, fill_color=col, fill_opacity=0.10,
                                   stroke_width=2).move_to([0, y, 0])
            eng_t  = Text(engine, color=col, font_size=40, weight=BOLD).move_to([-4.0, y, 0])
            fmt_t  = label(fmt, scale=0.68).move_to([0.0, y, 0])
            reach_t = label(reach, scale=0.65).set_color(col).move_to([4.5, y, 0])
            boxes.append((box, eng_t, fmt_t, reach_t))

        for box, eng_t, fmt_t, reach_t in boxes[:2]:
            self.play(FadeIn(box), FadeIn(eng_t), FadeIn(fmt_t), FadeIn(reach_t), run_time=0.35)
        for box, eng_t, fmt_t, reach_t in boxes[2:]:
            self.play(FadeIn(box), FadeIn(eng_t), FadeIn(fmt_t), FadeIn(reach_t), run_time=0.35)

        self.wait(0.5)


# ── B10: .tres Pattern ───────────────────────────────────────────────
class B10_TresPattern(Scene):
    def construct(self):
        title = ink("The .tres Pattern — One Draw File, Shared", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Central .tres file
        tres_box = RoundedRectangle(width=4.0, height=1.2, corner_radius=0.15,
                                     color=TERRA, fill_color=TERRA, fill_opacity=0.15,
                                     stroke_width=3).move_to([0, 0.3, 0])
        tres_t = Text("particle_material.tres", color=TERRA, font_size=40, weight=BOLD)
        tres_t.move_to([0, 0.3, 0])
        self.play(FadeIn(tres_box), FadeIn(tres_t), run_time=0.4)

        # Three effects fanning out
        effects = [("Coin burst", -4.5, 2.2),
                   ("Enemy explosion", 0, 2.2),
                   ("Bullet glow", 4.5, 2.2)]
        eff_boxes = []
        arrows = []
        for name, x, y in effects:
            box = RoundedRectangle(width=3.0, height=0.75, corner_radius=0.1,
                                   color=BLUE_GPU, fill_color=BLUE_GPU, fill_opacity=0.12,
                                   stroke_width=2).move_to([x, y, 0])
            t = label(name, scale=0.75, weight=BOLD).set_color(BLUE_GPU).move_to([x, y, 0])
            arr = Arrow([x, y - 0.42, 0], [tres_box.get_top()[0] * 0.3 + x * 0.7,
                                             tres_box.get_top()[1], 0],
                         color=WARM, buff=0, stroke_width=3)
            eff_boxes.append((box, t))
            arrows.append(arr)

        self.play(*[FadeIn(box) for box, t in eff_boxes],
                  *[FadeIn(t) for box, t in eff_boxes], run_time=0.4)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.4)

        # Flags label
        flags = label("additive · unshaded · billboard · proximity_fade", scale=0.68)
        flags.set_color(TERRA).move_to([0, -0.8, 0])
        self.play(FadeIn(flags), run_time=0.3)

        note = label("Change once — all three effects update", scale=0.72, slant="ITALIC")
        note.set_color(ACCENT2).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


# ── B11: Library Entry Card ──────────────────────────────────────────
class B11_LibraryCard(Scene):
    def construct(self):
        title = ink("Library Entry — Five Fields", scale=1.0).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        fields = [
            ("Name",       "what the effect is called in this project",          INK),
            ("Renderer",   "Compatibility / Mobile / Forward+",                   TERRA),
            ("Node type",  "CPU or GPU",                                          GREY_CPU),
            ("Draw .tres", "the draw material file (shared if same look)",        ACCENT2),
            ("Test status","what the headless checks establish (not visual proof)",BLUE_GPU),
        ]
        y0 = 1.5
        dots = []
        for i, (field, desc, col) in enumerate(fields):
            y = y0 - i * 0.80
            d = Dot([-5.5, y, 0], radius=0.14, color=col)
            f_t = Text(field, color=col, font_size=42, weight=BOLD).next_to(d, RIGHT, buff=0.25)
            f_t.set_y(y)
            d_t = label(desc, scale=0.70).set_color(INK).next_to(f_t, RIGHT, buff=0.4)
            d_t.set_y(y)
            dots.append((d, f_t, d_t))

        for d, f_t, d_t in dots[:3]:
            self.play(FadeIn(d), FadeIn(f_t), FadeIn(d_t), run_time=0.35)
        for d, f_t, d_t in dots[3:]:
            self.play(FadeIn(d), FadeIn(f_t), FadeIn(d_t), run_time=0.35)

        note = label("Build the card before you build the effect.", scale=0.72, slant="ITALIC")
        note.set_color(TERRA).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)
