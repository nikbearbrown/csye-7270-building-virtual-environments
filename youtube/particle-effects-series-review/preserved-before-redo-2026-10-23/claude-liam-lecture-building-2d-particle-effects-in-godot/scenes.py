"""
Manim scenes for: Building 2D Particle Effects in Godot
Film: claude-liam-lecture-building-2d-particle-effects-in-godot
Course: CSYE 7270 Building Virtual Environments
Palette: Claude — stage #F2F0E9, ink #3D3929, terracotta #D97757
"""
from manim import *
import numpy as np
import random

# ── Claude palette ───────────────────────────────────────────────
STAGE   = "#F2F0E9"
INK     = "#3D3929"
TERRA   = "#D97757"
WARM    = "#C4B99A"
ACCENT2 = "#6B8F71"
RED_ERR = "#C0392B"
GREEN_OK = "#27AE60"

config.background_color = STAGE


class B01_GameTree(Scene):
    """Scene tree: Main → Player (Trail inside), MobTimer, HUD."""
    def construct(self):
        title = Text("walker-2d-dodge-the-creeps", font="EB Garamond",
                     color=INK, font_size=34).to_edge(UP, buff=0.5)
        sub = Text("480 × 720 · Compatibility renderer", font="EB Garamond",
                   color=WARM, font_size=24).next_to(title, DOWN, buff=0.15)

        # Tree nodes
        main_node = Text("Main", font="EB Garamond", color=INK, font_size=36)
        player_node = Text("Player  (Area2D)", font="EB Garamond", color=TERRA, font_size=30)
        trail_node = Text("Trail  (GPUParticles2D)", font="EB Garamond", color=ACCENT2, font_size=26)
        mob_timer = Text("MobTimer", font="EB Garamond", color=INK, font_size=26)
        hud_node = Text("HUD", font="EB Garamond", color=INK, font_size=26)

        main_node.move_to([-2.5, 1.0, 0])
        player_node.move_to([-0.5, 0.1, 0])
        trail_node.move_to([1.5, -0.8, 0])
        mob_timer.move_to([-0.5, -1.5, 0])
        hud_node.move_to([-0.5, -2.3, 0])

        arrow1 = Arrow(main_node.get_right(), player_node.get_left(),
                       buff=0.15, color=WARM, stroke_width=2)
        arrow2 = Arrow(player_node.get_right(), trail_node.get_left(),
                       buff=0.15, color=ACCENT2, stroke_width=2)
        arrow3 = Arrow(main_node.get_right(), mob_timer.get_left(),
                       buff=0.15, color=WARM, stroke_width=2)
        arrow4 = Arrow(main_node.get_right(), hud_node.get_left(),
                       buff=0.15, color=WARM, stroke_width=2)

        self.play(Write(title), Write(sub), run_time=0.5)
        self.play(FadeIn(main_node), run_time=0.4)
        self.play(GrowArrow(arrow1), FadeIn(player_node), run_time=0.5)
        self.play(GrowArrow(arrow2), FadeIn(trail_node), run_time=0.5)
        self.play(GrowArrow(arrow3), FadeIn(mob_timer),
                  GrowArrow(arrow4), FadeIn(hud_node), run_time=0.5)
        note = Text("Trail is a child of Player — that matters", font="EB Garamond",
                    color=TERRA, font_size=22, slant="ITALIC").to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


class B02_TrailConfig(Scene):
    """Trail GPUParticles2D properties card."""
    def construct(self):
        title = Text("The Trail node", font="EB Garamond",
                     color=INK, font_size=40).to_edge(UP, buff=0.5)
        sub = Text("GPUParticles2D — child of Player", font="EB Garamond",
                   color=WARM, font_size=26).next_to(title, DOWN, buff=0.15)

        props = [
            ("amount", "10"),
            ("speed_scale", "2"),
            ("gravity", "(0, 0, 0)"),
            ("z_index", "−1  (draws behind player)"),
            ("emitting", "true  (default — always on)"),
        ]
        rows = VGroup()
        for key, val in props:
            key_t = Text(key, font="EB Garamond", color=TERRA, font_size=28)
            val_t = Text(val, font="EB Garamond", color=INK, font_size=28)
            sep   = Text("  =  ", font="EB Garamond", color=WARM, font_size=28)
            row   = VGroup(key_t, sep, val_t).arrange(RIGHT, buff=0.1)
            rows.add(row)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0.3, -0.3, 0])

        self.play(Write(title), Write(sub), run_time=0.5)
        for row in rows:
            self.play(FadeIn(row), run_time=0.3)
        note = Text("texture = walk frame · colour ramp: half-transparent → transparent",
                    font="EB Garamond", color=WARM, font_size=21).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.5)


class B03_ParentTrap(Scene):
    """Parent visibility propagation: hide() cascades to children."""
    def construct(self):
        title = Text("The Parenting Trap", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        # Scenario A — burst under Player
        bad_label = Text("burst under Player", font="EB Garamond",
                         color=RED_ERR, font_size=28).move_to([-3.0, 1.1, 0])
        player_box = Rectangle(width=2.6, height=0.6, color=TERRA, stroke_width=2)
        player_box.move_to([-3.0, 0.35, 0])
        player_text = Text("Player", font="EB Garamond", color=TERRA, font_size=26)
        player_text.move_to(player_box.get_center())
        burst_box = Rectangle(width=2.6, height=0.6, color=RED_ERR, stroke_width=2)
        burst_box.move_to([-3.0, -0.45, 0])
        burst_text = Text("DeathBurst ← hidden", font="EB Garamond", color=RED_ERR, font_size=22)
        burst_text.move_to(burst_box.get_center())
        arrow_bad = Arrow(player_box.get_bottom(), burst_box.get_top(),
                          buff=0.05, color=RED_ERR, stroke_width=2)

        hide_label = Text("player.hide()", font="Courier New", color=RED_ERR,
                          font_size=22).next_to(player_box, RIGHT, buff=0.2)

        # Scenario B — burst under Main
        good_label = Text("burst under Main", font="EB Garamond",
                          color=GREEN_OK, font_size=28).move_to([3.0, 1.1, 0])
        main_box = Rectangle(width=2.6, height=0.6, color=ACCENT2, stroke_width=2)
        main_box.move_to([3.0, 0.35, 0])
        main_text = Text("Main", font="EB Garamond", color=ACCENT2, font_size=26)
        main_text.move_to(main_box.get_center())
        burst_good_box = Rectangle(width=2.6, height=0.6, color=GREEN_OK, stroke_width=2)
        burst_good_box.move_to([3.0, -0.45, 0])
        burst_good_text = Text("DeathBurst ← visible", font="EB Garamond", color=GREEN_OK, font_size=22)
        burst_good_text.move_to(burst_good_box.get_center())
        arrow_good = Arrow(main_box.get_bottom(), burst_good_box.get_top(),
                           buff=0.05, color=GREEN_OK, stroke_width=2)

        rule = Text("emitting = true  ≠  visible", font="EB Garamond",
                    color=TERRA, font_size=30, slant="ITALIC").move_to([0, -1.9, 0])

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(bad_label), FadeIn(player_box), FadeIn(player_text), run_time=0.4)
        self.play(GrowArrow(arrow_bad), FadeIn(burst_box), FadeIn(burst_text),
                  FadeIn(hide_label), run_time=0.5)
        self.play(FadeIn(good_label), FadeIn(main_box), FadeIn(main_text), run_time=0.4)
        self.play(GrowArrow(arrow_good), FadeIn(burst_good_box), FadeIn(burst_good_text), run_time=0.5)
        self.play(FadeIn(rule), run_time=0.4)
        self.wait(0.6)


class B04_AllowListTrap(Scene):
    """Allow list Bash(godot:*) vs absolute path — the access denial."""
    def construct(self):
        title = Text("The Allow List Trap", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        rule_box = Rectangle(width=5.5, height=0.65, color=WARM, stroke_width=2)
        rule_box.move_to([0, 1.55, 0])
        rule_text = Text("Bash(godot:*)", font="Courier New", color=INK, font_size=26)
        rule_text.move_to(rule_box.get_center())
        rule_lbl = Text("allow list rule", font="EB Garamond", color=WARM, font_size=22)
        rule_lbl.next_to(rule_box, RIGHT, buff=0.3)

        path_box = Rectangle(width=5.5, height=0.65, color=TERRA, stroke_width=2)
        path_box.move_to([0, 0.6, 0])
        path_text = Text("/Applications/Godot.app/…/Godot", font="Courier New", color=RED_ERR, font_size=22)
        path_text.move_to(path_box.get_center())
        path_lbl = Text("agent's attempt", font="EB Garamond", color=TERRA, font_size=22)
        path_lbl.next_to(path_box, RIGHT, buff=0.3)

        cross = Text("✗  5 calls refused", font="EB Garamond", color=RED_ERR, font_size=32)
        cross.move_to([0, -0.5, 0])

        fix = Text("Fix: add godot path to CLAUDE.md or AGENTS.md", font="EB Garamond",
                   color=ACCENT2, font_size=25).move_to([0, -1.5, 0])

        note = Text("'godot' on PATH ≠ '/Applications/Godot.app/…'",
                    font="EB Garamond", color=WARM, font_size=22).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(rule_box), FadeIn(rule_text), FadeIn(rule_lbl), run_time=0.4)
        self.play(FadeIn(path_box), FadeIn(path_text), FadeIn(path_lbl), run_time=0.4)
        self.play(FadeIn(cross), run_time=0.4)
        self.play(FadeIn(fix), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B05_PredictedVsReal(Scene):
    """Agent predicted output vs actual test output — two wrong predictions."""
    def construct(self):
        title = Text("Predicted vs Real", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        col_predicted = Text("Agent's Prediction", font="EB Garamond",
                             color=WARM, font_size=26).move_to([-2.8, 1.5, 0])
        col_actual = Text("Actual Output", font="EB Garamond",
                          color=ACCENT2, font_size=26).move_to([2.8, 1.5, 0])

        rows_data = [
            ("emitting after hit", "PASS", "PASS", False),
            ("is_visible_in_tree", "PASS", "PASS", False),
            ("global_position", "PASS", "PASS", False),
            ("finished signal", "FAIL ✗", "FAIL ✗", False),
            ("emits on 2nd death", "FAIL ✗", "PASS ✓", True),  # wrong prediction — highlight
        ]

        row_groups = []
        for i, (check, pred, actual, highlight) in enumerate(rows_data):
            y = 0.8 - i * 0.52
            check_t = Text(check, font="EB Garamond", color=INK, font_size=22)
            check_t.move_to([-5.0, y, 0])
            pred_color = RED_ERR if "FAIL" in pred else GREEN_OK
            if highlight:
                pred_color = TERRA  # wrong prediction gets terracotta
            pred_t = Text(pred, font="EB Garamond", color=pred_color, font_size=22)
            pred_t.move_to([-2.0, y, 0])
            act_color = RED_ERR if "FAIL" in actual else GREEN_OK
            act_t = Text(actual, font="EB Garamond", color=act_color, font_size=22)
            act_t.move_to([3.0, y, 0])
            row_groups.append(VGroup(check_t, pred_t, act_t))

        wrong_note = Text("2 of 3 predicted failures were wrong",
                          font="EB Garamond", color=TERRA, font_size=26,
                          slant="ITALIC").move_to([0, -2.0, 0])

        self.play(Write(title), FadeIn(col_predicted), FadeIn(col_actual), run_time=0.4)
        for rg in row_groups:
            self.play(FadeIn(rg), run_time=0.3)
        self.play(FadeIn(wrong_note), run_time=0.4)
        self.wait(0.6)


class B07_LambdaBug(Scene):
    """GDScript lambda captures by value — fix: use Dictionary."""
    def construct(self):
        title = Text("The Lambda Bug", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        broken_lbl = Text("Broken", font="EB Garamond", color=RED_ERR, font_size=26)
        broken_lbl.move_to([-3.2, 1.55, 0])

        code_broken = VGroup(
            Text("var finished_received := false", font="Courier New", color=INK, font_size=20),
            Text("burst.finished.connect(", font="Courier New", color=INK, font_size=20),
            Text("  func(): finished_received = true", font="Courier New", color=RED_ERR, font_size=20),
            Text("  CONNECT_ONE_SHOT)", font="Courier New", color=INK, font_size=20),
            Text("# lambda sets its own copy — outer var unchanged", font="Courier New",
                 color=WARM, font_size=18),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-1.5, 0.4, 0])

        fix_lbl = Text("Fixed", font="EB Garamond", color=GREEN_OK, font_size=26)
        fix_lbl.move_to([3.5, -1.0, 0])

        code_fixed = VGroup(
            Text("var state := {\"done\": false}", font="Courier New", color=INK, font_size=20),
            Text("burst.finished.connect(", font="Courier New", color=INK, font_size=20),
            Text("  func(): state[\"done\"] = true", font="Courier New", color=GREEN_OK, font_size=20),
            Text("  CONNECT_ONE_SHOT)", font="Courier New", color=INK, font_size=20),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-1.0, -1.95, 0])

        rule = Text("Dictionary is a reference type — lambda and caller share the same object",
                    font="EB Garamond", color=TERRA, font_size=21).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(broken_lbl), FadeIn(code_broken), run_time=0.5)
        self.play(FadeIn(fix_lbl), FadeIn(code_fixed), run_time=0.5)
        self.play(FadeIn(rule), run_time=0.4)
        self.wait(0.5)


class B08_NullTexture(Scene):
    """null texture → 1×1 pixels; fix: 16×16 GradientTexture2D."""
    def construct(self):
        title = Text("The Null Texture", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        screen_rect = Rectangle(width=1.44, height=2.16, color=WARM, stroke_width=2)
        screen_rect.move_to([-3.5, -0.3, 0])
        screen_lbl = Text("480 × 720", font="EB Garamond", color=WARM, font_size=20)
        screen_lbl.next_to(screen_rect, DOWN, buff=0.15)

        # tiny pixel dots inside the screen
        rng = random.Random(42)
        pixels = VGroup(*[
            Dot([rng.uniform(-4.2, -2.8), rng.uniform(-1.3, 0.7), 0],
                radius=0.03, color=INK)
            for _ in range(32)
        ])
        pixel_note = Text("32 × 1-pixel squares", font="EB Garamond", color=RED_ERR, font_size=22)
        pixel_note.move_to([-3.5, -2.0, 0])

        fix_lbl = Text("Fix: 16×16 GradientTexture2D", font="EB Garamond",
                       color=GREEN_OK, font_size=26).move_to([2.5, 1.55, 0])

        # Gradient circle representation
        circle = Circle(radius=0.55, color=TERRA, fill_color=WHITE, fill_opacity=0.85)
        circle.move_to([2.5, 0.35, 0])
        circle_lbl = Text("radial · white → transparent", font="EB Garamond",
                          color=WARM, font_size=20).next_to(circle, DOWN, buff=0.2)

        null_code = Text("texture = null  →  1×1 px", font="Courier New",
                         color=RED_ERR, font_size=22).move_to([2.5, -1.2, 0])
        fix_code = Text("texture = GradientTexture2D  →  16×16 px", font="Courier New",
                        color=GREEN_OK, font_size=20).move_to([2.5, -1.8, 0])

        note = Text("Found by reading the class reference, not by running the game",
                    font="EB Garamond", color=TERRA, font_size=21,
                    slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(screen_rect), FadeIn(screen_lbl), run_time=0.4)
        self.play(FadeIn(pixels), FadeIn(pixel_note), run_time=0.4)
        self.play(FadeIn(fix_lbl), FadeIn(circle), FadeIn(circle_lbl), run_time=0.4)
        self.play(FadeIn(null_code), FadeIn(fix_code), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B09_DisableZ(Scene):
    """ParticleProcessMaterial is 3D; spread 180 bleeds into Z; fix: disable_z."""
    def construct(self):
        title = Text("Disable Z", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        prob_lbl = Text("Default: particle_flag_disable_z = false",
                        font="EB Garamond", color=RED_ERR, font_size=26).move_to([0, 1.45, 0])

        # Show spread directions: some going into screen (Z)
        center = np.array([-3.0, -0.3, 0])
        emitter_dot = Dot(center, radius=0.15, color=TERRA)
        angles_xy = [45, 120, 200, 310]
        arrows_visible = VGroup(*[
            Arrow(center, center + 1.4 * np.array([np.cos(np.radians(a)),
                                                    np.sin(np.radians(a)), 0]),
                  buff=0, color=ACCENT2, stroke_width=2.5)
            for a in angles_xy
        ])
        z_arrow = Arrow(center, center + np.array([0.0, 0.0, 0]) + np.array([0.3, -0.3, 0]),
                        buff=0, color=RED_ERR, stroke_width=3)
        z_lbl = Text("Z (invisible)", font="EB Garamond", color=RED_ERR, font_size=20)
        z_lbl.move_to([-1.8, -0.9, 0])

        visible_lbl = Text("XY — visible", font="EB Garamond", color=ACCENT2, font_size=20)
        visible_lbl.move_to([-3.0, -2.0, 0])

        fix_lbl = Text("Fix: particle_flag_disable_z = true",
                       font="EB Garamond", color=GREEN_OK, font_size=26).move_to([2.3, 1.45, 0])
        fix_arrows = VGroup(*[
            Arrow(np.array([2.3, -0.3, 0]),
                  np.array([2.3, -0.3, 0]) + 1.4 * np.array([np.cos(np.radians(a)),
                                                               np.sin(np.radians(a)), 0]),
                  buff=0, color=GREEN_OK, stroke_width=2.5)
            for a in range(0, 360, 45)
        ])
        fix_dot = Dot([2.3, -0.3, 0], radius=0.15, color=TERRA)
        fix_note = Text("all velocity in XY plane", font="EB Garamond",
                        color=GREEN_OK, font_size=20).move_to([2.3, -2.0, 0])

        note = Text("ParticleProcessMaterial is shared between 2D and 3D nodes",
                    font="EB Garamond", color=WARM, font_size=22).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        self.play(FadeIn(prob_lbl), run_time=0.3)
        self.play(FadeIn(emitter_dot), FadeIn(arrows_visible), run_time=0.4)
        self.play(FadeIn(z_arrow), FadeIn(z_lbl), FadeIn(visible_lbl), run_time=0.4)
        self.play(FadeIn(fix_lbl), FadeIn(fix_dot), FadeIn(fix_arrows),
                  FadeIn(fix_note), run_time=0.5)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(0.5)


class B10_NineChecks(Scene):
    """9-check summary: what the tests prove and what they don't."""
    def construct(self):
        title = Text("9 Checks — All Pass", font="EB Garamond",
                     color=INK, font_size=40).to_edge(UP, buff=0.5)

        checks = [
            "texture = GradientTexture2D",
            "particle_flag_disable_z enabled",
            "not emitting at load",
            "not emitting before hit",
            "emitting after hit",
            "visible in tree after hit",
            "global_position = player hit position",
            "finished within lifetime + 0.5 s",
            "emits again on 2nd death",
        ]
        # Dot bullets (shapes tracked by checker) + text labels
        dots = []
        texts = []
        y_start = 1.4
        for i, c in enumerate(checks):
            y = y_start - i * 0.38
            d = Dot([-4.8, y, 0], radius=0.12, color=GREEN_OK)
            t = Text(c, font="EB Garamond", color=INK, font_size=22)
            t.move_to([-1.5, y, 0])
            dots.append(d)
            texts.append(t)

        divider = Line([-6.0, -2.1, 0], [6.0, -2.1, 0], color=WARM, stroke_width=1.5)
        not_proven = Text("State only — not: visible · readable · GPU cost",
                          font="EB Garamond", color=TERRA, font_size=24,
                          slant="ITALIC").to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        # Reveal in three batches to create distinct shape states
        batch1 = dots[:3]
        batch2 = dots[3:6]
        batch3 = dots[6:]
        self.play(*[FadeIn(d) for d in batch1],
                  *[FadeIn(t) for t in texts[:3]], run_time=0.4)
        self.play(*[FadeIn(d) for d in batch2],
                  *[FadeIn(t) for t in texts[3:6]], run_time=0.4)
        self.play(*[FadeIn(d) for d in batch3],
                  *[FadeIn(t) for t in texts[6:]], run_time=0.4)
        self.play(FadeIn(divider), run_time=0.3)
        self.play(FadeIn(not_proven), run_time=0.4)
        self.wait(0.6)


class B11_SleepTrap(Scene):
    """Godot headless frame loop: 6.9ms sleep hides all work below it."""
    def construct(self):
        title = Text("The Sleep Trap", font="EB Garamond",
                     color=INK, font_size=42).to_edge(UP, buff=0.5)

        # Frame bar: work + sleep
        work_bar = Rectangle(width=0.4, height=1.8, color=ACCENT2,
                             fill_color=ACCENT2, fill_opacity=0.8)
        sleep_bar = Rectangle(width=5.2, height=1.8, color=WARM,
                              fill_color=WARM, fill_opacity=0.6)
        bars = VGroup(work_bar, sleep_bar).arrange(RIGHT, buff=0)
        bars.move_to([0, 0.35, 0])

        work_lbl = Text("work\n< 0.1ms", font="EB Garamond", color=ACCENT2, font_size=20)
        work_lbl.next_to(work_bar, DOWN, buff=0.2)
        sleep_lbl = Text("OS::add_frame_delay\n6.9 ms sleep", font="EB Garamond",
                         color=INK, font_size=22)
        sleep_lbl.move_to(sleep_bar.get_center())

        total_lbl = Text("Every case = 6.9 ms", font="EB Garamond",
                         color=RED_ERR, font_size=28).move_to([0, -1.55, 0])

        fix_lbl = Text("--fixed-fps 60 → skips the sleep → real measurements",
                       font="EB Garamond", color=GREEN_OK, font_size=24).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.4)
        # Sequential adds create distinct shape states
        self.play(FadeIn(work_bar), run_time=0.4)
        self.play(FadeIn(sleep_bar), run_time=0.5)
        self.play(FadeIn(work_lbl), FadeIn(sleep_lbl), run_time=0.4)
        self.play(FadeIn(total_lbl), run_time=0.4)
        self.play(FadeIn(fix_lbl), run_time=0.4)
        self.wait(0.5)


class B12_CostTable(Scene):
    """CPU particle cost table: without vs with --fixed-fps 60."""
    def construct(self):
        title = Text("Particle Cost — Headless", font="EB Garamond",
                     color=INK, font_size=40).to_edge(UP, buff=0.5)

        # Header
        hdr = VGroup(
            Text("", font="EB Garamond", color=INK, font_size=22),
            Text("1 k", font="EB Garamond", color=INK, font_size=22),
            Text("10 k", font="EB Garamond", color=INK, font_size=22),
            Text("50 k", font="EB Garamond", color=INK, font_size=22),
        ).arrange(RIGHT, buff=0.9).move_to([1.0, 1.45, 0])

        rows_data = [
            ("(no flag)  GPU", "6.9 ms", "6.9 ms", "6.9 ms", RED_ERR),
            ("(no flag)  CPU", "6.9 ms", "6.9 ms", "6.9 ms", RED_ERR),
            ("--fixed-fps  GPU", "0.002 ms", "0.002 ms", "0.002 ms", WARM),
            ("--fixed-fps  CPU", "0.035 ms", "0.33 ms", "1.61 ms", ACCENT2),
        ]
        row_groups = []
        for i, (label, v1, v2, v3, color) in enumerate(rows_data):
            y = 0.65 - i * 0.52
            lbl_t = Text(label, font="EB Garamond", color=INK, font_size=21)
            lbl_t.move_to([-2.5, y, 0])
            v1_t = Text(v1, font="EB Garamond", color=color, font_size=21)
            v1_t.move_to([1.2, y, 0])
            v2_t = Text(v2, font="EB Garamond", color=color, font_size=21)
            v2_t.move_to([2.6, y, 0])
            v3_t = Text(v3, font="EB Garamond", color=color, font_size=21)
            v3_t.move_to([4.1, y, 0])
            row_groups.append(VGroup(lbl_t, v1_t, v2_t, v3_t))

        note_gpu = Text("GPU rows = dummy renderer — not the real GPU cost",
                        font="EB Garamond", color=WARM, font_size=20)
        note_gpu.move_to([0, -1.65, 0])
        note_cpu = Text("CPU cost is linear  ·  50 k = 1.61 ms ≈ 1/10 of a 16.7 ms frame",
                        font="EB Garamond", color=TERRA, font_size=22)
        note_cpu.to_edge(DOWN, buff=0.45)

        self.play(Write(title), FadeIn(hdr), run_time=0.4)
        for rg in row_groups:
            self.play(FadeIn(rg), run_time=0.3)
        self.play(FadeIn(note_gpu), run_time=0.3)
        self.play(FadeIn(note_cpu), run_time=0.4)
        self.wait(0.6)
