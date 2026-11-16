"""Act IV (B40): one clock. A schematic (tagged 'drawing'): two time lines, the gap between their starts on three real runs, a uniform that carries one number.
Measured offsets (script clock minus shader TIME, E10 real-time runs, logs/e10-clock.txt and logs/e10-clock-rerun.txt): 0.32 s, 0.28 s, 0.31 s. Drawn to one scale (2.4 units per second), so the bars are honest."""


def a4_at(mob, x, y, left=False):
    """Place a mob by its left edge (left=True) or centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a4_dot(p, r=0.14):
    return Dot(np.array(p, dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════ B40 · one clock ═════════════════════════
class B40_OneClock(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        X0, LEN, K = -4.5, 8.6, 2.4                 # line start x, line length, scene units per second
        ys, yc = 1.9, -1.2                          # shader line, script line
        ym = (ys + yc) / 2.0                        # the strip between them
        rows = [1.1, 0.5, -0.1]                     # one bracket row per run

        def clock(y, color):
            line = arrow([X0, y, 0], [X0 + LEN, y, 0], color=color, w=6, tip=0.24)
            ticks = VGroup(*[Line([X0 + 0.5 * K * k, y - 0.14, 0], [X0 + 0.5 * K * k, y + 0.14, 0], color=DIM, stroke_width=4) for k in range(1, 7)])
            return VGroup(line, ticks, a4_dot([X0, y, 0]))

        sh = clock(ys, INK); shl = a4_at(T("shader time", 36), X0 - 0.1, ys + 0.5, left=True)
        sc = clock(yc, TEAL); scl = a4_at(T("script clock", 36), X0 - 0.1, yc - 0.55, left=True)
        scg = VGroup(sc, scl)
        drawing = T("drawing", 32, DIM).move_to([5.3, -3.05, 0])

        self.wait(0.3)
        self.play(Create(sh[0]), FadeIn(sh[1]), FadeIn(sh[2]), FadeIn(shl), FadeIn(drawing), run_time=0.9)
        # "the script's clock": the second line, starting level with the first (the naive picture)
        until(self, "the script's clock", lead=0.3)
        self.play(Create(sc[0]), FadeIn(sc[1]), FadeIn(sc[2]), FadeIn(scl), run_time=0.9)

        # "start at different moments ... on three runs": the script line slides to the right, once per run, one bracket per run
        gaps = [0.32, 0.28, 0.31]
        cur = 0.0
        brs, lbs, prev_guide = [], [], None
        sg = DashedLine([X0, ys - 0.2, 0], [X0, rows[-1] - 0.2, 0], color=DIM, stroke_width=3, dash_length=0.1)   # the shader's start, carried down
        until(self, "start at different", lead=0.3)
        for k, g in enumerate(gaps):
            ex = X0 + g * K
            slide = [scg.animate.shift([(g - cur) * K, 0, 0])]
            if prev_guide is not None:
                slide.append(FadeOut(prev_guide))
            self.play(*slide, run_time=0.85 if k == 0 else 0.5, rate_func=smooth)
            cur = g
            guide = DashedLine([ex, yc + 0.12, 0], [ex, rows[k], 0], color=DIM, stroke_width=3, dash_length=0.1)
            br = dim_arrow([X0, rows[k], 0], [ex, rows[k], 0], color=DIM, w=5, tip=0.14)
            lb = a4_at(T(f"{g:.2f} s", 36), ex + 0.2, rows[k], left=True)
            anims = [Create(br), Create(guide), FadeIn(lb)]
            if k == 0:
                anims.append(Create(sg))
            self.play(*anims, run_time=0.4)
            brs.append(br); lbs.append(lb); prev_guide = guide

        # "So the script writes its clock into a uniform": clear the runs, the uniform box appears
        until(self, "So the script writes", lead=0.4)
        self.play(FadeOut(VGroup(*brs, *lbs, prev_guide, sg)), run_time=0.4)
        bx = box(1.0, ym, 3.1, 0.95, color=INK, sw=5)
        wl = M("wave_clock", 32).move_to([1.0, ym, 0])
        self.play(Create(bx), FadeIn(wl), run_time=0.5)
        # "writes its clock": an arrow from the script line into the box, and the script line is pulled into line with the shader's
        until(self, "writes its clock", lead=0.15)
        a_in = arrow([1.0, yc + 0.06, 0], [1.0, ym - 0.475, 0], color=INK, w=6, tip=0.2)
        self.play(GrowArrow(a_in), scg.animate.shift([-cur * K, 0, 0]), run_time=0.9, rate_func=smooth)
        # "the shader reads that": an arrow out of the box into the shader line; both lines now run on one number
        until(self, "the shader reads", lead=0.3)
        a_out = arrow([1.0, ym + 0.475, 0], [1.0, ys - 0.07, 0], color=INK, w=6, tip=0.2)
        self.play(GrowArrow(a_out), Indicate(sh[0], color=TEAL, scale_factor=1.0), run_time=0.55)
        one = a4_at(T("one number", 36), -3.5, ym, left=True)
        self.play(FadeIn(one), run_time=0.4)
        done(self)
