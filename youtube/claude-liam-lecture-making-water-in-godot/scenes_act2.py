"""Act II (B14, B16; the rest of the act is captures and Remotion). Manim only, kit objects. Both beats are DRAWINGS (B14 says so in a corner tag).
Cast: the series pixel grid (six by four outline squares), one terracotta dot (grey-ringed) in each square, one cream pixel with a dark ring.
The 24 points are the SAME in both beats (one seeded layout below), and the dashed line in B14 is the true cell edge: it runs only as far as those two points
are still the two closest of all 24, so nothing on screen claims more than the drawing shows. Numbers: none are invented (no figures on screen)."""

a2_COLS, a2_ROWS = 6, 4
a2_OWN = (2, 2)                       # (col, row) of the square the pixel sits in; its right-hand neighbour is (3, 2)
a2_SEED = 66


def a2_points(seed):
    """24 points in CELL UNITS (cell centre (c - 2.5, 1.5 - r), a jitter of up to 0.36 so every point stays well inside its square)."""
    rng = np.random.RandomState(seed)
    J = rng.uniform(-0.36, 0.36, size=(a2_ROWS, a2_COLS, 2))
    pts = np.zeros((a2_ROWS, a2_COLS, 2))
    for r in range(a2_ROWS):
        for c in range(a2_COLS):
            pts[r, c] = (c - 2.5 + J[r, c, 0], 1.5 - r + J[r, c, 1])
    return pts


def a2_edge(pts, P, Q):
    """The part of the perpendicular bisector of P and Q where P and Q are still the closest points of all 24 (the true cell edge)."""
    allp = pts.reshape(-1, 2)
    M = (P + Q) / 2.0
    d = Q - P
    n = np.array([-d[1], d[0]]) / np.linalg.norm(d)

    def ok(t):
        x = M + t * n
        return np.linalg.norm(x - P) <= np.linalg.norm(allp - x, axis=1).min() + 1e-9
    lo = 0.0
    while lo > -4 and ok(lo - 0.005):
        lo -= 0.005
    hi = 0.0
    while hi < 4 and ok(hi + 0.005):
        hi += 0.005
    return M + lo * n, M + hi * n


def a2_layout():
    pts = a2_points(a2_SEED)
    c, r = a2_OWN
    P, Q = pts[r, c], pts[r, c + 1]
    e0, e1 = a2_edge(pts, P, Q)
    block = [pts[rr, cc] for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)]
    best = None
    for py in np.arange((1.5 - r) - 0.42, (1.5 - r) + 0.42, 0.02):          # the pixel: just inside the right border of its own square
        p = np.array([-0.09, py])
        d = np.array([np.linalg.norm(p - b) for b in block])
        o = np.argsort(d)
        if np.allclose(block[o[0]], Q) and np.allclose(block[o[1]], P):    # nearest is the neighbour's point, second is its own
            s = min(d[o[1]] - d[o[0]], d[o[2]] - d[o[1]])
            if best is None or s > best[0]:
                best = (s, p)
    return pts, P, Q, (e0, e1), best[1], block


a2_PTS, a2_P, a2_Q, a2_EDGE, a2_PIX, a2_BLOCK = a2_layout()


def a2_sc(p, cell, gx, gy):
    """Cell units -> scene point."""
    return np.array([gx + p[0] * cell, gy + p[1] * cell, 0.0])


def a2_dot(p, r=0.11):
    return Dot(np.array([p[0], p[1], 0.0], dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a2_left(mob, x, y):
    mob.move_to([x + mob.width / 2.0, y, 0])
    return mob


# ═════════════════════════ B14 · one point each ═════════════════════════
class B14_OnePointEach(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        cell, gx, gy = 1.2, 0.0, 0.05
        grid = pixel_grid(cols=a2_COLS, rows=a2_ROWS, cell=cell, x=gx, y=gy, color=DIM, sw=2)
        dots = [[a2_dot(a2_sc(a2_PTS[r, c], cell, gx, gy), 0.12) for c in range(a2_COLS)] for r in range(a2_ROWS)]
        flat = [d for row in dots for d in row]
        P, Q = dots[a2_OWN[1]][a2_OWN[0]], dots[a2_OWN[1]][a2_OWN[0] + 1]
        e0, e1 = a2_sc(a2_EDGE[0], cell, gx, gy), a2_sc(a2_EDGE[1], cell, gx, gy)
        p_sc, q_sc = a2_sc(a2_P, cell, gx, gy), a2_sc(a2_Q, cell, gx, gy)
        join = Line(p_sc, q_sc, color=INK, stroke_width=3)
        mp = (p_sc + q_sc) / 2.0
        half_a = DashedLine(mp, e0, color=DIM, stroke_width=5, dash_length=0.12)
        half_b = DashedLine(mp, e1, color=DIM, stroke_width=5, dash_length=0.12)
        l_one = T("one  point  each", 40).move_to([0, 2.95, 0])
        l_eq = T("equally close", 40).move_to([e0[0], -2.9, 0])
        lead = arrow([e0[0], -2.55, 0], [e0[0], e0[1] - 0.14, 0], color=DIM, w=3, tip=0.16)       # a callout, so the label never reads as a longer dashed line
        tag = a2_left(T("drawing", 32, DIM), -6.0, -3.15)

        # the surface cut into squares
        self.play(FadeIn(VGroup(*[s for row in grid.cells for s in row]), lag_ratio=0.03), FadeIn(tag), run_time=0.9)
        # one point drops into each square, at a different spot
        until(self, "put one point in each", lead=0.5)
        self.play(FadeIn(l_one), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.5) for d in flat], lag_ratio=0.05), run_time=1.5)
        # --- after the 45 to 55 percent window: two neighbours, the line of equal distance ---
        until(self, "Foam will live", lead=-0.1)
        self.play(Create(join), Indicate(P, scale_factor=1.9, color=TERRA), Indicate(Q, scale_factor=1.9, color=TERRA), run_time=0.7)
        until(self, "where two points", lead=0.4)
        self.play(Create(half_a), Create(half_b), run_time=1.0)
        until(self, "equally close", lead=0.5)
        self.play(FadeIn(l_eq), Create(lead), run_time=0.5)
        done(self)


# ═════════════════════════ B16 · the nine squares ═════════════════════════
class B16_NineSquares(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        cell, gx, gy = 1.2, -2.2, 0.05
        grid = pixel_grid(cols=a2_COLS, rows=a2_ROWS, cell=cell, x=gx, y=gy, color=DIM, sw=2)
        dots = [[a2_dot(a2_sc(a2_PTS[r, c], cell, gx, gy), 0.12) for c in range(a2_COLS)] for r in range(a2_ROWS)]
        c0, r0 = a2_OWN
        inside = [dots[r][c] for r in range(r0 - 1, r0 + 2) for c in range(c0 - 1, c0 + 2)]
        outside = [dots[r][c] for r in range(a2_ROWS) for c in range(a2_COLS) if not (c0 - 1 <= c <= c0 + 1 and r0 - 1 <= r <= r0 + 1)]
        own, nb = dots[r0][c0], dots[r0][c0 + 1]
        pix_p = a2_sc(a2_PIX, cell, gx, gy)
        pix = Dot(pix_p, radius=0.12, color=CARD).set_stroke(INK, width=5)
        # the 3 by 3 block of squares around the pixel's own square
        bx = gx + (c0 - 2.5) * cell; by = gy + (1.5 - r0) * cell
        block = RoundedRectangle(width=3 * cell, height=3 * cell, corner_radius=0.1, stroke_color=INK, stroke_width=6).move_to([bx, by, 0])
        in_sc = [a2_sc(b, cell, gx, gy) for b in a2_BLOCK]                   # the nine points, in the same order as `inside`
        lines = [Line(pix_p, q, color=DIM, stroke_width=3) for q in in_sc]
        self.add(a2_left(T("drawing", 32, DIM), -6.0, -3.15))                                    # the same small tag as B14: this is a schematic
        near_i = inside.index(nb); sec_i = inside.index(own)
        lnear, lsec = lines[near_i], lines[sec_i]
        others = [ln for i, ln in enumerate(lines) if i not in (near_i, sec_i)]
        # legend for the two lines that will be kept
        ly1, ly2 = 0.8, -0.05
        k1 = Line([2.9, ly1, 0], [4.1, ly1, 0], color=INK, stroke_width=12); t1 = a2_left(T("nearest", 40), 4.35, ly1)
        k2 = Line([2.9, ly2, 0], [4.1, ly2, 0], color=INK, stroke_width=6); t2 = a2_left(T("second", 40), 4.35, ly2)

        self.play(FadeIn(VGroup(*[s for row in grid.cells for s in row]), lag_ratio=0.02), FadeIn(VGroup(*[d for row in dots for d in row])), run_time=0.8)
        # one pixel, near the border of its square
        until(self, "A pixel can be closest", lead=0.0)
        self.play(FadeIn(pix, scale=1.8), run_time=0.4)
        until(self, "neighboring square", lead=0.4)
        self.play(Indicate(nb, scale_factor=2.0, color=TERRA), run_time=0.6)
        # check all nine squares around it
        until(self, "check all nine squares", lead=0.55)
        self.play(Create(block), *[d.animate.set_opacity(0.3) for d in outside], run_time=0.7)
        self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.07), FadeIn(VGroup(k1, k2, t1, t2)), run_time=0.7)
        self.bring_to_front(*inside, pix)
        # --- after the 45 to 55 percent window ---
        until(self, "its own and the eight", lead=-0.2)
        self.play(Indicate(own, scale_factor=2.0, color=TERRA), run_time=0.6)
        # keep the nearest distance, and the second nearest
        until(self, "Keep the nearest", lead=0.3)
        self.play(*[FadeOut(ln) for ln in others], lnear.animate.set_stroke(INK, width=12), run_time=0.7)
        until(self, "the second nearest", lead=0.4)
        self.play(lsec.animate.set_stroke(INK, width=6), run_time=0.5)
        done(self)
