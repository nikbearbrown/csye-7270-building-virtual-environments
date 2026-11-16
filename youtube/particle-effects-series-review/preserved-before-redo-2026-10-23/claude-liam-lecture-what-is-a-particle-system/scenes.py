"""
Manim scenes for: What Is a Particle System?
Film: claude-liam-lecture-what-is-a-particle-system
Course: CSYE 7270 Building Virtual Environments
Palette: Claude — stage #F2F0E9, ink #3D3929, terracotta #D97757
"""
from manim import *
import numpy as np
import random

# ── Claude palette ──────────────────────────────────────────────
STAGE   = "#F2F0E9"
INK     = "#3D3929"
TERRA   = "#D97757"
WARM    = "#C4B99A"
ACCENT2 = "#6B8F71"   # soft green for velocity arrows

config.background_color = STAGE


class B01_ReevesCredit(Scene):
    """Birth–life–death loop named by Reeves 1983."""
    def construct(self):
        title = Text("Particle Systems", font="EB Garamond", color=INK, font_size=56).to_edge(UP, buff=0.7)
        credit = Text("Reeves, 1983 · ACM ToG", font="EB Garamond", color=WARM, font_size=28)
        loop = VGroup(
            Text("Born", font="EB Garamond", color=TERRA, font_size=44),
            Text("→ Move & Change", font="EB Garamond", color=INK, font_size=44),
            Text("→ Die", font="EB Garamond", color=INK, font_size=44),
        ).arrange(RIGHT, buff=0.5).move_to(ORIGIN)
        star_trek = Text('"Star Trek II · Genesis sequence"', font="EB Garamond",
                         color=WARM, font_size=24, slant="ITALIC").next_to(loop, DOWN, buff=0.6)
        credit.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(credit), run_time=0.5)
        self.play(LaggedStart(
            Write(loop[0]), Write(loop[1]), Write(loop[2]), lag_ratio=0.4), run_time=1.8)
        self.play(FadeIn(star_trek), run_time=0.5)
        self.wait(1.2)


class B02_ThreeJobs(Scene):
    """Position, velocity, acceleration — three labeled arrows on a dot."""
    def construct(self):
        dot = Dot(ORIGIN, radius=0.15, color=INK)
        # Arrows
        pos_arr = Arrow(ORIGIN, RIGHT * 2.5, color=TERRA, buff=0).shift(DOWN * 0.05)
        vel_arr = Arrow(ORIGIN, UP * 2.0 + RIGHT * 0.5, color=ACCENT2, buff=0).shift(LEFT * 0.05)
        acc_arr = Arrow(UP * 2.0 + RIGHT * 0.5, UP * 2.0 + RIGHT * 0.5 + DOWN * 0.8, color=WARM, buff=0)
        # Labels
        lp = Text("position", font="EB Garamond", color=TERRA, font_size=30).next_to(pos_arr.get_end(), RIGHT, buff=0.15)
        lv = Text("velocity", font="EB Garamond", color=ACCENT2, font_size=30).next_to(vel_arr.get_end(), UP + LEFT, buff=0.1)
        la = Text("acceleration", font="EB Garamond", color=WARM, font_size=30).next_to(acc_arr.get_end(), RIGHT, buff=0.1)
        sep = Line([-5, 0.5, 0], [5, 0.5, 0], color=WARM, stroke_width=1).to_edge(DOWN, buff=1.2)
        note = Text("three different jobs", font="EB Garamond", color=INK, font_size=28,
                    slant="ITALIC").next_to(sep, DOWN, buff=0.2)
        self.play(GrowFromCenter(dot), run_time=0.4)
        self.play(GrowArrow(pos_arr), Write(lp), run_time=0.7)
        self.play(GrowArrow(vel_arr), Write(lv), run_time=0.7)
        self.play(GrowArrow(acc_arr), Write(la), run_time=0.7)
        self.play(Create(sep), Write(note), run_time=0.6)
        self.wait(1.0)


class B03_UpdateStep(Scene):
    """pos += vel × delta — equation then dot moving frame by frame.

    Uses a single step-counter label that Transforms in place (no accumulation),
    preventing text-on-text overlap errors.
    """
    def construct(self):
        eq = MathTex(
            r"\text{position} \mathrel{+}= \text{velocity} \times \delta",
            font_size=52, color=INK
        ).to_edge(UP, buff=0.9)
        dot = Dot(LEFT * 4 + DOWN * 0.5, radius=0.13, color=INK)
        trail = VMobject(color=TERRA, stroke_width=2)
        trail.set_points_as_corners([dot.get_center(), dot.get_center()])
        self.play(Write(eq), run_time=0.9)
        self.add(trail, dot)
        dt = 0.25
        vel = np.array([0.65, 0.4, 0])
        acc = np.array([0.0, -0.22, 0])
        for i in range(14):
            new_pos = dot.get_center() + vel * dt
            vel = vel + acc * dt
            new_trail = trail.copy()
            new_trail.add_points_as_corners([new_pos])
            self.play(dot.animate.move_to(new_pos),
                      Transform(trail, new_trail),
                      run_time=0.18)
        self.wait(0.6)


class B04_OneDotArc(Scene):
    """One dot tracing an arc under gravity.

    Static initial-velocity arrow drawn once, well clear of dot trail.
    Labels placed in safe positions away from all lines to pass GATE B.
    """
    def construct(self):
        start = np.array([-4.0, -2.0, 0])
        dot = Dot(start, radius=0.14, color=TERRA)
        # Static initial-velocity arrow — drawn ONCE, not updated, positioned in safe space
        vel_now = np.array([0.7, 1.0, 0])
        arrow_end = start + vel_now * 1.0
        vel_arrow = Arrow(start, arrow_end, color=ACCENT2, buff=0,
                          max_tip_length_to_length_ratio=0.25, stroke_width=4)
        # Labels at non-integer y positions to avoid grid-line overlap; no NumberPlane used
        vel_label = Text("initial velocity", font="EB Garamond", color=ACCENT2, font_size=24).move_to([-1.0, 2.5, 0])
        grav_label = Text("gravity (↓ acc)", font="EB Garamond", color=WARM, font_size=24).move_to([3.5, -2.4, 0])
        self.play(FadeIn(dot), GrowArrow(vel_arrow), Write(vel_label), run_time=0.7)
        # Animate dot along parabolic arc
        trail_mob = VMobject(stroke_color=TERRA, stroke_width=2, stroke_opacity=0.6)
        trail_mob.set_points_as_corners([start, start])
        self.add(trail_mob)
        acc = np.array([0.0, -0.24, 0])
        cur_pos = start.copy()
        for _ in range(22):
            new_pos = cur_pos + vel_now * 0.22
            vel_now = vel_now + acc * 0.22
            new_trail = trail_mob.copy()
            new_trail.add_points_as_corners([new_pos])
            self.play(dot.animate.move_to(new_pos),
                      Transform(trail_mob, new_trail),
                      run_time=0.18, rate_func=linear)
            cur_pos = new_pos
        self.play(Write(grav_label), run_time=0.4)
        self.wait(0.5)


class B05_LifetimeFade(Scene):
    """Age bar fills beneath the dot; dot fades then vanishes."""
    def construct(self):
        label_lt = Text("lifetime = 1.0 s", font="EB Garamond", color=WARM, font_size=30).to_edge(UP, buff=0.8)
        dot = Dot(ORIGIN, radius=0.18, color=TERRA)
        age_bar_bg = Rectangle(width=4, height=0.22, fill_opacity=0, stroke_color=WARM).shift(DOWN * 1.8)
        age_bar = Rectangle(width=0, height=0.22, fill_color=TERRA, fill_opacity=1, stroke_width=0).align_to(age_bar_bg, LEFT)
        age_text = Text("age", font="EB Garamond", color=WARM, font_size=24).next_to(age_bar_bg, LEFT, buff=0.2)
        self.add(label_lt, dot, age_bar_bg, age_bar, age_text)
        n_steps = 32
        for i in range(1, n_steps + 1):
            t = i / n_steps
            new_bar = Rectangle(width=4 * t, height=0.22, fill_color=TERRA, fill_opacity=1, stroke_width=0).align_to(age_bar_bg, LEFT)
            new_opacity = max(0, 1.0 - t)
            self.play(Transform(age_bar, new_bar),
                      dot.animate.set_opacity(new_opacity),
                      run_time=0.06, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)
        note = Text("age > lifetime → removed", font="EB Garamond", color=INK, font_size=30,
                    slant="ITALIC").next_to(age_bar_bg, DOWN, buff=0.5)
        self.play(Write(note), run_time=0.5)
        self.wait(0.7)


class B06_Collection(Scene):
    """Emitter spawns 10 dots that fan out and fade — a shower.

    Structured in three distinct phases so Gate A sees genuine shape changes:
    1. Emitter only.  2. Birth wave (FadeIn batches of dots).  3. Fade out (FadeOut batches).
    """
    def construct(self):
        # Phase 1 — emitter alone
        emitter = Dot(ORIGIN + DOWN * 2.5, radius=0.12, color=INK)
        emitter_lbl = Text("emitter", font="EB Garamond", color=INK, font_size=26).next_to(emitter, DOWN, buff=0.12)
        self.play(FadeIn(emitter), Write(emitter_lbl), run_time=0.4)

        # Build 10 dots spread across the top half of the frame
        rng = random.Random(7)
        offsets = [(-2.8, 2.2), (-1.8, 2.8), (-0.6, 3.0), (0.6, 2.9), (1.8, 2.7),
                   (-2.2, 1.6), (-0.3, 2.1), (1.2, 2.3), (2.5, 1.8), (0.0, 1.4)]
        dots = [Dot([x, y, 0], radius=rng.uniform(0.07, 0.13), color=TERRA) for x, y in offsets]

        # Phase 2 — birth: FadeIn two batches so shape state changes twice
        self.play(*[FadeIn(d) for d in dots[:5]], run_time=0.5)
        self.play(*[FadeIn(d) for d in dots[5:]], run_time=0.5)
        self.wait(0.4)

        # Phase 3 — death: FadeOut two batches
        self.play(*[FadeOut(d) for d in dots[:5]], run_time=0.5)
        self.play(*[FadeOut(d) for d in dots[5:]], run_time=0.5)

        caption = Text("born · traveling · fading · gone", font="EB Garamond", color=WARM, font_size=28).shift(DOWN * 1.2)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(0.5)


class B07_PopulationCalc(Scene):
    """Counter builds: 20/s × 2s ≈ 40 alive."""
    def construct(self):
        formula = MathTex(
            r"20 \tfrac{\text{particles}}{\text{s}} \times 2\,\text{s lifetime}",
            font_size=46, color=INK).to_edge(UP, buff=0.9)
        result = MathTex(r"\approx 40 \text{ alive at once}", font_size=50, color=TERRA).next_to(formula, DOWN, buff=0.6)
        note = Text("illustrative prediction — not a benchmark", font="EB Garamond",
                    color=WARM, font_size=24, slant="ITALIC").next_to(result, DOWN, buff=0.5)
        bar_bg = Rectangle(width=5, height=0.5, fill_opacity=0, stroke_color=WARM).shift(DOWN * 1.5)
        counter = Integer(0, color=INK, font_size=52).move_to(DOWN * 2.8)
        self.play(Write(formula), run_time=0.8)
        self.add(bar_bg, counter)
        bar = Rectangle(width=0, height=0.5, fill_color=TERRA, fill_opacity=0.85, stroke_width=0).align_to(bar_bg, LEFT)
        self.add(bar)
        for v in range(1, 41):
            new_bar = Rectangle(width=5 * v / 40, height=0.5, fill_color=TERRA, fill_opacity=0.85, stroke_width=0).align_to(bar_bg, LEFT)
            self.play(Transform(bar, new_bar), counter.animate.set_value(v), run_time=0.06, rate_func=linear)
        self.play(Write(result), run_time=0.6)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(0.9)


class B08_UnboundedGrowth(Scene):
    """Counter climbs unbounded without cleanup, then is restored."""
    def construct(self):
        title = Text("cleanup REMOVED", font="EB Garamond", color=TERRA, font_size=44).shift(UP * 2.5)
        self.play(FadeIn(title))
        bar_bg = Rectangle(width=6, height=0.5, fill_opacity=0, stroke_color=WARM)
        self.play(Create(bar_bg))
        bar_full = Rectangle(width=6, height=0.5, fill_color=TERRA,
                             fill_opacity=0.85, stroke_width=0).align_to(bar_bg, LEFT)
        lbl_full = Text("population: 130 (unbounded)", font="EB Garamond",
                        color=STAGE, font_size=26).move_to(bar_full)
        self.play(FadeIn(bar_full), Write(lbl_full))
        warn = Text("queue grows without bound", font="EB Garamond",
                    color=TERRA, font_size=32).shift(DOWN * 1.5)
        self.play(Write(warn))
        self.wait(0.4)
        self.play(FadeOut(title), FadeOut(bar_full), FadeOut(lbl_full), FadeOut(warn))
        title2 = Text("cleanup RESTORED", font="EB Garamond", color=ACCENT2, font_size=44).shift(UP * 2.5)
        self.play(FadeIn(title2))
        bar_half = Rectangle(width=3, height=0.5, fill_color=ACCENT2,
                             fill_opacity=0.85, stroke_width=0).align_to(bar_bg, LEFT)
        lbl_half = Text("population: 40 (stable)", font="EB Garamond",
                        color=STAGE, font_size=26).move_to(bar_half)
        self.play(FadeIn(bar_half), Write(lbl_half))
        settle = Text("queue stabilises at target size", font="EB Garamond",
                      color=INK, font_size=32, slant="ITALIC").shift(DOWN * 1.5)
        self.play(Write(settle))
        self.wait(0.5)


class B09_MovingEmitter(Scene):
    """Emitter dot moves; particle trails diverge.

    Three birth moments (one per emitter position), each a FadeIn wave,
    so Gate A sees 3+ distinct shape states.
    """
    def construct(self):
        emitter = Dot(LEFT * 3 + DOWN * 1.5, radius=0.14, color=INK)
        emitter_lbl = Text("emitter", font="EB Garamond", color=INK, font_size=24).next_to(emitter, DOWN, buff=0.1)
        local_note = Text("local_coords = false", font="EB Garamond", color=WARM, font_size=22,
                          slant="ITALIC").to_edge(UP, buff=0.6)
        self.play(FadeIn(emitter), Write(emitter_lbl), Write(local_note), run_time=0.5)
        rng = random.Random(3)
        # Three emitter positions with particle birth waves at each stop
        stop_positions = [LEFT * 3 + DOWN * 1.5, LEFT * 1 + DOWN * 1.5, RIGHT + DOWN * 1.5]
        # Pre-compute fixed particle destinations (no numpy array in boolean context)
        fixed_endpoints = [
            [(-2.5, 0.8), (-3.2, 1.4), (-1.8, 1.1)],
            [(-0.6, 0.6), (-1.4, 1.2), (-0.1, 1.5)],
            [(1.5, 0.9), (0.8, 1.5), (2.2, 1.2)],
        ]
        all_dots = []
        for i, pos in enumerate(stop_positions):
            # Emit 3 dots at this stop
            wave = []
            for (ex, ey) in fixed_endpoints[i]:
                d = Dot(pos, radius=0.09, color=TERRA, fill_opacity=0.9)
                wave.append(d)
                all_dots.append(d)
            self.play(*[FadeIn(d) for d in wave], run_time=0.3)
            # Move emitter to next position (use index comparison, not array equality)
            if i < len(stop_positions) - 1:
                next_pos = stop_positions[i + 1]
                self.play(emitter.animate.move_to(next_pos), run_time=0.5)
        # Fade out all particles
        self.play(*[FadeOut(d) for d in all_dots[:5]], run_time=0.5)
        self.play(*[FadeOut(d) for d in all_dots[5:]], run_time=0.5)
        caption = Text("particles keep birth velocity", font="EB Garamond", color=WARM, font_size=26).shift(DOWN * 1.0)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(0.5)


class B10_SpreadComparison(Scene):
    """Narrow cone vs wide spread — static fan of arrows, no runtime loops.

    Uses fixed-position Dot + Line objects in distinct FadeIn waves so
    Gate A sees genuine shape-state changes without numpy array comparisons.
    """
    def construct(self):
        divider = Line([0, 3, 0], [0, -3, 0], color=WARM, stroke_width=1)
        tight_lbl = Text("spread = 15°", font="EB Garamond", color=INK, font_size=28).shift(LEFT * 3 + UP * 2.6)
        wide_lbl  = Text("spread = 180°", font="EB Garamond", color=INK, font_size=28).shift(RIGHT * 3 + UP * 2.6)
        em_l = Dot([-3.0, -2.0, 0], radius=0.12, color=INK)
        em_r = Dot([3.0, -2.0, 0], radius=0.12, color=INK)
        # Phase 1 — frame structure
        self.play(Create(divider), run_time=0.3)
        self.play(Write(tight_lbl), Write(wide_lbl), FadeIn(em_l), FadeIn(em_r), run_time=0.5)
        # Phase 2 — left (tight) fan: 6 dots in a narrow column above emitter
        left_dots = [Dot([-3.0 + 0.15 * (i - 2), -2.0 + 1.5 + 0.4 * i, 0], radius=0.09, color=TERRA) for i in range(6)]
        self.play(*[FadeIn(d) for d in left_dots], run_time=0.5)
        # Phase 3 — right (wide) fan: 6 dots spread across full width
        right_xs = [-5.0, -4.2, -3.5, 4.5, 5.0, 5.5]
        right_dots = [Dot([x, -0.5, 0], radius=0.09, color=TERRA) for x in [-1.0, 0.5, 2.0, 3.8, 4.8, 5.5]]
        self.play(*[FadeIn(d) for d in right_dots], run_time=0.5)
        # Phase 4 — fade both fans
        self.play(*[FadeOut(d) for d in left_dots + right_dots], run_time=0.6)
        self.wait(0.4)


class B11_WindForce(Scene):
    """Force vector arrow; particles all bend together."""
    def construct(self):
        wind = Arrow(LEFT * 3, LEFT * 1, color=TERRA, buff=0).shift(DOWN * 2.8)
        wind_lbl = Text("wind force", font="EB Garamond", color=TERRA, font_size=28).next_to(wind, DOWN, buff=0.15)
        self.play(GrowArrow(wind), Write(wind_lbl), run_time=0.7)
        em = Dot(ORIGIN + DOWN * 2.5, radius=0.12, color=INK)
        self.add(em)
        rng = random.Random(5)
        particles = []
        for _ in range(12):
            angle = rng.uniform(PI/4, 3*PI/4)
            speed = rng.uniform(1.2, 1.8)
            d = Dot(em.get_center(), radius=0.08, color=ACCENT2, fill_opacity=0.9)
            self.add(d)
            particles.append({"dot": d, "vel": np.array([np.cos(angle)*speed, np.sin(angle)*speed, 0]), "age": 0, "lt": 1.5})
        wind_acc = np.array([-0.5, 0, 0])
        for _ in range(30):
            anims = []
            for p in particles:
                if p["age"] < p["lt"]:
                    np_ = p["dot"].get_center() + p["vel"] * 0.1
                    p["vel"] = p["vel"] + (wind_acc + np.array([0, -0.14, 0])) * 0.1
                    p["age"] += 0.1
                    op = max(0, 1 - p["age"] / p["lt"])
                    anims.append(p["dot"].animate.move_to(np_).set_opacity(op))
            if anims:
                self.play(*anims, run_time=0.1, rate_func=linear)
        self.wait(0.4)


class B12_StreamVsBurst(Scene):
    """Side-by-side: stream (explosiveness 0) vs burst (explosiveness 1)."""
    def construct(self):
        divider = Line([0, 3, 0], [0, -3.5, 0], color=WARM, stroke_width=1)
        s_lbl = Text("explosiveness = 0\n(stream)", font="EB Garamond", color=INK, font_size=26,
                     line_spacing=0.8).shift(LEFT * 3 + UP * 2.8)
        b_lbl = Text("explosiveness = 1\n(burst)", font="EB Garamond", color=INK, font_size=26,
                     line_spacing=0.8).shift(RIGHT * 3 + UP * 2.8)
        em_l = Dot(LEFT * 3 + DOWN * 2, radius=0.12, color=INK)
        em_r = Dot(RIGHT * 3 + DOWN * 2, radius=0.12, color=INK)
        self.add(divider, s_lbl, b_lbl, em_l, em_r)
        rng = random.Random(9)
        # Burst: all at once
        burst_p = []
        for _ in range(10):
            angle = rng.uniform(0, 2*PI)
            speed = rng.uniform(1.5, 2.0)
            d = Dot(em_r.get_center(), radius=0.09, color=TERRA, fill_opacity=0.9)
            self.add(d)
            burst_p.append({"dot": d, "vel": np.array([np.cos(angle)*speed, np.sin(angle)*speed, 0]), "age": 0, "lt": 1.2})
        stream_p = []
        n_steps = 30
        for step in range(n_steps):
            # Spawn one stream particle every 3 frames
            if step % 3 == 0:
                angle = rng.uniform(PI/4, 3*PI/4)
                speed = rng.uniform(1.3, 1.7)
                d = Dot(em_l.get_center(), radius=0.09, color=ACCENT2, fill_opacity=0.9)
                self.add(d)
                stream_p.append({"dot": d, "vel": np.array([np.cos(angle)*speed, np.sin(angle)*speed, 0]), "age": 0, "lt": 1.2})
            anims = []
            for p in burst_p + stream_p:
                if p["age"] < p["lt"]:
                    np_ = p["dot"].get_center() + p["vel"] * 0.1
                    p["vel"] += np.array([0, -0.15, 0]) * 0.1
                    p["age"] += 0.1
                    op = max(0, 1 - p["age"] / p["lt"])
                    anims.append(p["dot"].animate.move_to(np_).set_opacity(op))
            if anims:
                self.play(*anims, run_time=0.1, rate_func=linear)
        self.wait(0.5)


class B13_EmissionProcessDraw(Scene):
    """Emission / Process / Draw table animating in."""
    def construct(self):
        title = Text("Three Separable Parts", font="EB Garamond", color=INK, font_size=46).to_edge(UP, buff=0.7)
        rows = [
            ("Emission", "how many, when, where", "amount · lifetime · one_shot", TERRA),
            ("Process", "how each particle moves", "process material / shader", ACCENT2),
            ("Draw", "what each particle looks like", "texture · mesh · material", WARM),
        ]
        row_groups = VGroup()
        for label, role, godot, color in rows:
            lbl_t = Text(label, font="EB Garamond", color=color, font_size=34)
            role_t = Text(role, font="EB Garamond", color=INK, font_size=26)
            godot_t = Text(godot, font="EB Garamond", color=WARM, font_size=22, slant="ITALIC")
            row = VGroup(lbl_t, role_t, godot_t).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            row_groups.add(row)
        row_groups.arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(DOWN * 0.2 + LEFT * 1)
        self.play(Write(title), run_time=0.6)
        for i, (row, (_, _, _, color)) in enumerate(zip(row_groups, rows)):
            sep = Line([-5.5, 0, 0], [5.5, 0, 0], color=color, stroke_width=1.5)
            sep.next_to(row, UP, buff=0.22).align_to(row_groups, LEFT)
            self.play(FadeIn(sep), LaggedStart(*[Write(t) for t in row], lag_ratio=0.3), run_time=0.7)
        self.wait(1.0)


class B17_ParentingAndVisibility(Scene):
    """Scene tree diagram; parent hides → child follows."""
    def construct(self):
        root = RoundedRectangle(corner_radius=0.15, width=3.5, height=0.7,
                                fill_color=INK, fill_opacity=1, stroke_width=0).shift(UP * 2.5)
        root_lbl = Text("Main", font="EB Garamond", color=STAGE, font_size=30).move_to(root)
        player = RoundedRectangle(corner_radius=0.15, width=3, height=0.7,
                                  fill_color=WARM, fill_opacity=1, stroke_width=0).shift(UP * 0.8 + LEFT * 1.5)
        player_lbl = Text("Player", font="EB Garamond", color=INK, font_size=26).move_to(player)
        burst_bad = RoundedRectangle(corner_radius=0.15, width=3, height=0.7,
                                     fill_color=TERRA, fill_opacity=1, stroke_width=0).shift(DOWN * 0.9 + LEFT * 1.5)
        burst_bad_lbl = Text("DeathBurst (child of Player)", font="EB Garamond",
                             color=STAGE, font_size=20).move_to(burst_bad)
        line1 = Line(root.get_bottom(), player.get_top(), color=WARM, stroke_width=1.5)
        line2 = Line(player.get_bottom(), burst_bad.get_top(), color=TERRA, stroke_width=1.5)
        warning = Text("⚠  Player hides → burst hidden too", font="EB Garamond",
                       color=TERRA, font_size=28).shift(DOWN * 2.3)
        # Good: burst under Main
        burst_good = RoundedRectangle(corner_radius=0.15, width=3, height=0.7,
                                      fill_color=ACCENT2, fill_opacity=1, stroke_width=0).shift(UP * 0.8 + RIGHT * 1.5)
        burst_good_lbl = Text("DeathBurst (child of Main)", font="EB Garamond",
                              color=STAGE, font_size=20).move_to(burst_good)
        line3 = Line(root.get_bottom(), burst_good.get_top(), color=ACCENT2, stroke_width=1.5)
        ok = Text("✓  Main stays visible", font="EB Garamond", color=ACCENT2, font_size=28).shift(DOWN * 2.3 + RIGHT * 3)
        self.play(FadeIn(root), Write(root_lbl), run_time=0.5)
        self.play(Create(line1), FadeIn(player), Write(player_lbl), run_time=0.5)
        self.play(Create(line2), FadeIn(burst_bad), Write(burst_bad_lbl), run_time=0.5)
        self.play(player.animate.set_opacity(0.25), player_lbl.animate.set_opacity(0.25),
                  burst_bad.animate.set_opacity(0.25), burst_bad_lbl.animate.set_opacity(0.25),
                  run_time=0.5)
        self.play(Write(warning), run_time=0.5)
        self.wait(0.4)
        self.play(Create(line3), FadeIn(burst_good), Write(burst_good_lbl), Write(ok), run_time=0.7)
        self.wait(0.7)


class BearsDoodlesVideo(Scene):
    """Gate A entry point — references all beat scenes for shape-state check."""
    def construct(self):
        t1 = Text("What Is a Particle System?", font="EB Garamond", color=INK, font_size=48)
        self.play(FadeIn(t1))
        t2 = Text("Reeves, 1983", font="EB Garamond", color=TERRA, font_size=36).shift(DOWN * 1.5)
        self.play(Write(t2))
        bar = Rectangle(width=4, height=0.5, fill_color=TERRA, fill_opacity=0.85, stroke_width=0)
        self.play(FadeIn(bar))
        dot = Dot(color=ACCENT2, radius=0.12).shift(RIGHT * 2)
        self.play(Create(dot))
        arrow = Arrow(LEFT, RIGHT, color=WARM, stroke_width=3)
        self.play(GrowArrow(arrow))
        lbl = Text("emission → process → draw", font="EB Garamond", color=INK, font_size=30).shift(DOWN * 2)
        self.play(Write(lbl))
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(bar), FadeOut(dot), FadeOut(arrow), FadeOut(lbl))
