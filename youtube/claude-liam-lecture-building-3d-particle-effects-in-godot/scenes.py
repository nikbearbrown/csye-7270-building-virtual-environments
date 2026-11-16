"""
Manim scenes for: Building 3D Particle Effects in Godot
Film: claude-liam-lecture-building-3d-particle-effects-in-godot
Course: CSYE 7270 Building Virtual Environments
Palette: Claude — stage #F2F0E9, ink #3D3929, terracotta #D97757
"""
from manim import *
import numpy as np
import random

# ── Claude palette ────────────────────────────────────────────────
STAGE   = "#F2F0E9"
INK     = "#3D3929"
TERRA   = "#D97757"
WARM    = "#C4B99A"
ACCENT2 = "#6B8F71"
RED_ERR = "#C0392B"
GREEN_OK = "#27AE60"

config.background_color = STAGE


class B01_ThreeEffects(Scene):
    """Three CPUParticles3D effects in walker-3d-platformer."""
    def construct(self):
        title = Text("walker-3d-platformer — 3D effects", font="EB Garamond",
                     color=INK, font_size=38).to_edge(UP, buff=0.5)

        effects = [
            ("coin burst",      "CPUParticles3D", "16", "0.5 s", "one_shot · explosiveness=1 · sphere"),
            ("enemy explosion", "CPUParticles3D", "16", "0.8 s", "one_shot · explosiveness=1 · mesh"),
            ("bullet glow",     "CPUParticles3D", "16", "0.4 s", "looping · runs continuously"),
        ]
        colors = [TERRA, RED_ERR, ACCENT2]

        dots = []
        rows_g = []
        for i, (name, node, amt, life, notes) in enumerate(effects):
            y = 0.8 - i * 1.1
            d = Dot([-5.5, y, 0], radius=0.15, color=colors[i])
            name_t = Text(name, font="EB Garamond", color=colors[i], font_size=28)
            name_t.move_to([-3.0, y, 0])
            node_t = Text(node, font="Courier New", color=WARM, font_size=20)
            node_t.move_to([0.5, y, 0])
            amt_t = Text(f"amt={amt}", font="EB Garamond", color=INK, font_size=22)
            amt_t.move_to([2.8, y, 0])
            life_t = Text(life, font="EB Garamond", color=INK, font_size=22)
            life_t.move_to([4.3, y, 0])
            notes_t = Text(notes, font="EB Garamond", color=WARM, font_size=19)
            notes_t.move_to([0.5, y - 0.42, 0])
            dots.append(d)
            rows_g.append(VGroup(name_t, node_t, amt_t, life_t, notes_t))

        note = Text("All three — no sub-emitters · no trails · no particle shaders",
                    font="EB Garamond", color=TERRA, font_size=21,
                    slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        for d, rg in zip(dots, rows_g):
            self.play(FadeIn(d), FadeIn(rg), run_time=0.4)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


class B02_CPUvsGPU3D(Scene):
    """Feature comparison: GPUParticles3D vs CPUParticles3D."""
    def construct(self):
        title = Text("GPU vs CPU — Feature Table (3D)", font="EB Garamond",
                     color=INK, font_size=38).to_edge(UP, buff=0.5)

        col_gpu = Text("GPUParticles3D", font="EB Garamond", color=GREEN_OK, font_size=26)
        col_gpu.move_to([-1.0, 1.45, 0])
        col_cpu = Text("CPUParticles3D", font="EB Garamond", color=RED_ERR, font_size=26)
        col_cpu.move_to([3.5, 1.45, 0])

        features = [
            ("process_material", "YES (on node)", "NO (node props)"),
            ("sub_emitter",      "YES",            "NO"),
            ("trail_enabled",    "YES",            "NO"),
            ("particle shader",  "YES",            "NO"),
            ("hardware support", "Modern GPU",     "Wider (mobile OK)"),
        ]

        row_groups = []
        for i, (feat, gpu_val, cpu_val) in enumerate(features):
            y = 0.65 - i * 0.52
            feat_t = Text(feat, font="EB Garamond", color=INK, font_size=22)
            feat_t.move_to([-3.5, y, 0])
            gpu_c = GREEN_OK if "YES" in gpu_val else WARM
            gpu_t = Text(gpu_val, font="EB Garamond", color=gpu_c, font_size=22)
            gpu_t.move_to([-0.5, y, 0])
            cpu_c = RED_ERR if "NO" in cpu_val else ACCENT2
            cpu_t = Text(cpu_val, font="EB Garamond", color=cpu_c, font_size=22)
            cpu_t.move_to([3.5, y, 0])
            row_groups.append(VGroup(feat_t, gpu_t, cpu_t))

        note = Text("'No plans to add new features to CPUParticles' — Godot docs",
                    font="EB Garamond", color=WARM, font_size=21,
                    slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), FadeIn(col_gpu), FadeIn(col_cpu), run_time=0.5)
        for rg in row_groups:
            self.play(FadeIn(rg), run_time=0.3)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B03_AnimTrack(Scene):
    """Animation track as trigger: AnimationPlayer keys emitting to true."""
    def construct(self):
        title = Text("Animation Track Trigger", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        # Diagram: AnimationPlayer → track → emitting
        anim_box = Rectangle(width=3.0, height=0.8, color=TERRA, stroke_width=2)
        anim_box.move_to([-3.5, 0.55, 0])
        anim_lbl = Text("AnimationPlayer\n'take'", font="EB Garamond", color=TERRA, font_size=24)
        anim_lbl.move_to(anim_box.get_center())

        arrow = Arrow(anim_box.get_right(), np.array([0.0, 0.55, 0]),
                      buff=0.1, color=WARM, stroke_width=2.5)

        track_box = Rectangle(width=3.5, height=0.8, color=ACCENT2, stroke_width=2)
        track_box.move_to([1.8, 0.55, 0])
        track_lbl = Text("CPUParticles3D:emitting\n= true   at t=0", font="Courier New",
                         color=ACCENT2, font_size=20)
        track_lbl.move_to(track_box.get_center())

        tip_box = Rectangle(width=5.5, height=0.7, color=WARM, stroke_width=1.5)
        tip_box.move_to([0, -0.9, 0])
        tip_lbl = Text("When agent can't find the trigger — look in AnimationPlayer",
                       font="EB Garamond", color=INK, font_size=22)
        tip_lbl.move_to(tip_box.get_center())

        code = Text("# any exported property can be keyed\n# not just emitting",
                    font="Courier New", color=WARM, font_size=20)
        code.move_to([0, -2.1, 0])

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(anim_box), FadeIn(anim_lbl), run_time=0.4)
        self.play(GrowArrow(arrow), FadeIn(track_box), FadeIn(track_lbl), run_time=0.5)
        self.play(FadeIn(tip_box), FadeIn(tip_lbl), run_time=0.4)
        self.play(FadeIn(code), run_time=0.3)
        self.wait(0.5)


class B04_SubEmitterChain(Scene):
    """Sub-emitter chain: parent → AT_END → child fires at particle death."""
    def construct(self):
        title = Text("Sub-Emitter Chain", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        # Parent emitter
        parent_dot = Dot([-4.5, 0.3, 0], radius=0.2, color=TERRA)
        parent_lbl = Text("GPUParticles3D\n(parent)", font="EB Garamond", color=TERRA, font_size=22)
        parent_lbl.move_to([-4.5, -0.45, 0])

        # Particle traveling
        spark = Dot([-2.0, 0.3, 0], radius=0.12, color=TERRA)
        spark_lbl = Text("particle\ntraveling", font="EB Garamond", color=WARM, font_size=20)
        spark_lbl.move_to([-2.0, -0.45, 0])

        # AT_END death point
        death_dot = Dot([0.5, 0.3, 0], radius=0.08, color=RED_ERR)
        death_lbl = Text("dies\n(AT_END)", font="EB Garamond", color=RED_ERR, font_size=20)
        death_lbl.move_to([0.5, -0.45, 0])

        # Child emitter cloud
        child_dots = VGroup(*[
            Dot([0.5 + 1.2 * np.cos(np.radians(a)),
                 0.3 + 0.8 * np.sin(np.radians(a)), 0],
                radius=0.08, color=ACCENT2)
            for a in range(0, 360, 50)
        ])
        child_lbl = Text("sub-emitter\nfires puff", font="EB Garamond",
                         color=ACCENT2, font_size=22).move_to([3.0, -0.45, 0])

        arrow1 = Arrow(parent_dot.get_right(), spark.get_left(),
                       buff=0.05, color=WARM, stroke_width=2)
        arrow2 = Arrow(spark.get_right(), death_dot.get_left(),
                       buff=0.05, color=WARM, stroke_width=2)

        mode_lbl = Text("sub_emitter_mode = AT_END", font="Courier New",
                        color=TERRA, font_size=24).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(parent_dot), FadeIn(parent_lbl), run_time=0.4)
        self.play(GrowArrow(arrow1), FadeIn(spark), FadeIn(spark_lbl), run_time=0.4)
        self.play(GrowArrow(arrow2), FadeIn(death_dot), FadeIn(death_lbl), run_time=0.4)
        self.play(FadeIn(child_dots), FadeIn(child_lbl), run_time=0.5)
        self.play(FadeIn(mode_lbl), run_time=0.3)
        self.wait(0.5)


class B05_SubEmitterModes(Scene):
    """Sub-emitter mode enum table."""
    def construct(self):
        title = Text("sub_emitter_mode — Godot 4.7.2", font="EB Garamond",
                     color=INK, font_size=38).to_edge(UP, buff=0.5)

        modes = [
            ("DISABLED",      "No sub-emitter",                                            WARM),
            ("CONSTANT",      "Sub-particles spawn from live parent particles continuously", INK),
            ("AT_END",        "Sub-particles spawn when a parent particle dies",             TERRA),
            ("AT_COLLISION",  "Sub-particles spawn on collision · needs SDF + Forward+",    RED_ERR),
            ("AT_START",      "Sub-particles spawn when a parent particle is born",          ACCENT2),
        ]

        dots = []
        texts = []
        for i, (mode, desc, color) in enumerate(modes):
            y = 0.85 - i * 0.58
            d = Dot([-5.5, y, 0], radius=0.12, color=color)
            m = Text(mode, font="Courier New", color=color, font_size=22)
            m.move_to([-3.0, y, 0])
            d2 = Text(desc, font="EB Garamond", color=INK, font_size=20)
            d2.move_to([1.8, y, 0])
            dots.append(d)
            texts.append(VGroup(m, d2))

        note = Text("CPU nodes have no sub-emitter at all", font="EB Garamond",
                    color=TERRA, font_size=24, slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        for d, t in zip(dots, texts):
            self.play(FadeIn(d), FadeIn(t), run_time=0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


class B06_SubEmitterSurprises(Scene):
    """Three sub-emitter gotchas: stops emitting, amount capped, no self-sub."""
    def construct(self):
        title = Text("Sub-Emitter Surprises", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        surprises = [
            ("1", "A sub-emitter stops its own emitting — even if Emitting was checked",     RED_ERR),
            ("2", "Total particles capped by sub-emitter's own Amount property",             TERRA),
            ("3", "A system cannot be its own sub-emitter",                                  RED_ERR),
        ]

        boxes = []
        for i, (num, text, color) in enumerate(surprises):
            y = 0.7 - i * 1.1
            num_circle = Circle(radius=0.3, color=color, fill_color=color, fill_opacity=0.15)
            num_circle.move_to([-4.5, y, 0])
            num_t = Text(num, font="EB Garamond", color=color, font_size=28)
            num_t.move_to(num_circle.get_center())
            body_t = Text(text, font="EB Garamond", color=INK, font_size=22)
            body_t.move_to([0.5, y, 0])
            boxes.append(VGroup(num_circle, num_t, body_t))

        note = Text("Read the sub-emitter docs before assuming it's broken",
                    font="EB Garamond", color=WARM, font_size=22,
                    slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        for box in boxes:
            self.play(FadeIn(box), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B07_ShaderStructure(Scene):
    """Particle shader anatomy: shader_type particles; start()/process()."""
    def construct(self):
        title = Text("Particle Shader — Anatomy", font="EB Garamond",
                     color=INK, font_size=40).to_edge(UP, buff=0.5)

        lines = [
            ("shader_type particles;",                    TERRA),
            ("",                                          INK),
            ("void start() {",                            ACCENT2),
            ("    if (RESTART_POSITION) {",               INK),
            ("        TRANSFORM = EMISSION_TRANSFORM;",   INK),
            ("    }",                                     INK),
            ("    if (RESTART_VELOCITY) {",               INK),
            ("        VELOCITY = initial_velocity;",      INK),
            ("    }",                                     INK),
            ("}",                                         ACCENT2),
            ("void process() {",                          ACCENT2),
            ("    VELOCITY += gravity * DELTA;",          INK),
            ("}",                                         ACCENT2),
        ]

        code_group = VGroup()
        for text, color in lines:
            t = Text(text if text else " ", font="Courier New", color=color, font_size=20)
            code_group.add(t)
        code_group.arrange(DOWN, buff=0.10, aligned_edge=LEFT).move_to([-1.0, -0.1, 0])

        note = Text("Runs before drawing — writes TRANSFORM / VELOCITY / COLOR / ACTIVE",
                    font="EB Garamond", color=WARM, font_size=21).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        # Show code in two batches for distinct states
        batch1 = VGroup(*list(code_group)[:7])
        batch2 = VGroup(*list(code_group)[7:])
        self.play(FadeIn(batch1), run_time=0.5)
        self.play(FadeIn(batch2), run_time=0.5)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B08_HeadlessCompile(Scene):
    """Headless dummy renderer compiles shader source — type errors catchable."""
    def construct(self):
        title = Text("Headless Shader Compilation", font="EB Garamond",
                     color=INK, font_size=40).to_edge(UP, buff=0.5)

        # Valid shader
        valid_box = Rectangle(width=5.5, height=1.0, color=GREEN_OK, stroke_width=2)
        valid_box.move_to([-0.5, 1.45, 0])
        valid_lbl = Text("VELOCITY = initial_velocity;  // vec3 = vec3  ✓",
                         font="Courier New", color=GREEN_OK, font_size=20)
        valid_lbl.move_to(valid_box.get_center())
        valid_result = Text("→ shader parses clean", font="EB Garamond",
                            color=GREEN_OK, font_size=24).next_to(valid_box, RIGHT, buff=0.3)

        # Broken shader
        broken_box = Rectangle(width=5.5, height=1.0, color=RED_ERR, stroke_width=2)
        broken_box.move_to([-0.5, 0.1, 0])
        broken_lbl = Text("VELOCITY = vec2(1.0);         // vec3 = vec2  ✗",
                          font="Courier New", color=RED_ERR, font_size=20)
        broken_lbl.move_to(broken_box.get_center())

        error_text = Text("SHADER ERROR: Invalid arguments to operator '=':\n  vec3, vec2",
                          font="Courier New", color=RED_ERR, font_size=20)
        error_text.move_to([0, -1.25, 0])

        note = Text("No window needed — headless dummy renderer still compiles shader source",
                    font="EB Garamond", color=TERRA, font_size=22,
                    slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(valid_box), FadeIn(valid_lbl), FadeIn(valid_result), run_time=0.4)
        self.play(FadeIn(broken_box), FadeIn(broken_lbl), run_time=0.4)
        self.play(FadeIn(error_text), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B09_ShaderVsMaterial(Scene):
    """What a particle shader adds over the material."""
    def construct(self):
        title = Text("Shader vs Material", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        cols = [
            ("Custom Forces",        "turbulence, vortices,\nany GLSL math",       TERRA),
            ("Procedural Shapes",    "parametric curves,\nmesh UV sampling",        ACCENT2),
            ("CUSTOM Channel",       "4 floats/particle:\ntemp → colour in draw",  GREEN_OK),
        ]

        col_groups = []
        for i, (head, desc, color) in enumerate(cols):
            x = -3.5 + i * 3.5
            circle = Circle(radius=0.5, color=color, fill_color=color, fill_opacity=0.15)
            circle.move_to([x, 0.7, 0])
            head_t = Text(head, font="EB Garamond", color=color, font_size=24)
            head_t.next_to(circle, DOWN, buff=0.2)
            desc_t = Text(desc, font="EB Garamond", color=INK, font_size=20)
            desc_t.next_to(head_t, DOWN, buff=0.15)
            col_groups.append(VGroup(circle, head_t, desc_t))

        note = Text("The material's built-in options still work — shader replaces when they run out",
                    font="EB Garamond", color=WARM, font_size=21).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        for cg in col_groups:
            self.play(FadeIn(cg), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B10_DrawMaterial(Scene):
    """StandardMaterial3D flags for particle rendering."""
    def construct(self):
        title = Text("The Draw Half — StandardMaterial3D", font="EB Garamond",
                     color=INK, font_size=36).to_edge(UP, buff=0.5)

        flags = [
            ("Blend Mode",       "additive",         "Overlapping particles ADD brightness — sparks, fire, glow"),
            ("Shading Mode",     "unshaded",          "Ignore scene lights — a spark in shadow stays bright"),
            ("Billboard Mode",   "particle",          "Each quad always faces the camera — round dot stays round"),
            ("Proximity Fade",   "enabled",           "Fades out near geometry — no hard clip through floors"),
        ]

        flag_groups = []
        for i, (prop, val, desc) in enumerate(flags):
            y = 0.8 - i * 0.8
            prop_t = Text(prop, font="EB Garamond", color=TERRA, font_size=24)
            prop_t.move_to([-4.0, y, 0])
            val_t = Text(f"= {val}", font="Courier New", color=ACCENT2, font_size=22)
            val_t.move_to([-1.0, y, 0])
            desc_t = Text(desc, font="EB Garamond", color=INK, font_size=19)
            desc_t.move_to([2.5, y, 0])
            flag_groups.append(VGroup(prop_t, val_t, desc_t))

        note = Text("Kept in particle_material.tres — reusable across nodes",
                    font="EB Garamond", color=WARM, font_size=22).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        for fg in flag_groups:
            self.play(FadeIn(fg), run_time=0.3)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B11_CostLevers(Scene):
    """Six particle cost levers and where each lands."""
    def construct(self):
        title = Text("Six Cost Levers", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        levers = [
            ("amount",          "direct multiplier",                "CPU / GPU"),
            ("lifetime",        "fewer births/s at fixed amount",   "CPU / GPU"),
            ("fixed_fps",       "update less often (interpolate)",  "CPU / GPU"),
            ("visibility_aabb", "real footprint = no off-screen work","CPU / GPU"),
            ("texture size",    "smaller = cheaper fill rate",      "GPU"),
            ("overdraw",        "transparent overlap = fill rate",  "GPU"),
        ]

        dots = []
        row_groups = []
        for i, (lever, desc, where) in enumerate(levers):
            y = 1.0 - i * 0.52
            d = Dot([-5.5, y, 0], radius=0.12, color=TERRA)
            lev_t = Text(lever, font="Courier New", color=TERRA, font_size=22)
            lev_t.move_to([-3.0, y, 0])
            desc_t = Text(desc, font="EB Garamond", color=INK, font_size=20)
            desc_t.move_to([0.8, y, 0])
            where_c = ACCENT2 if "GPU" in where else WARM
            where_t = Text(where, font="EB Garamond", color=where_c, font_size=20)
            where_t.move_to([4.5, y, 0])
            dots.append(d)
            row_groups.append(VGroup(lev_t, desc_t, where_t))

        note = Text("GPU cost (sim + fill) needs a real GPU — Chapter 13 Profiler",
                    font="EB Garamond", color=WARM, font_size=22).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        batch1 = list(zip(dots[:3], row_groups[:3]))
        batch2 = list(zip(dots[3:], row_groups[3:]))
        self.play(*[FadeIn(d) for d, _ in batch1],
                  *[FadeIn(r) for _, r in batch1], run_time=0.4)
        self.play(*[FadeIn(d) for d, _ in batch2],
                  *[FadeIn(r) for _, r in batch2], run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)
