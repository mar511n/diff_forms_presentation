""" Generalized Stokes section. """

from typing import TYPE_CHECKING

import numpy as np

import manimgx as m

from deck import CONTENT_FONT_SIZE, FRONTCOL, DeckScene, typst_preamble, split_typst_lines

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


def inside_polygon(points, x, y):
    """Whether (x, y) lies inside the closed polygon `points` (even-odd rule)."""
    inside = False
    xj, yj = points[-1][0], points[-1][1]
    for point in points:
        xi, yi = point[0], point[1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        xj, yj = xi, yi
    return inside


def closest_on_boundary(points, point):
    """The closed polygon's boundary point nearest to `point`, and its edge's direction."""
    x, y = point[0], point[1]
    best, best_dist, best_dir = (0,0), np.inf, np.array([1.0, 0.0, 0.0])
    for i, (ax, ay, _) in enumerate(points):
        bx, by, _ = points[(i + 1) % len(points)]
        dx, dy = bx - ax, by - ay
        t = np.clip(((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy), 0.0, 1.0)
        qx, qy = ax + t * dx, ay + t * dy
        dist = (qx - x) ** 2 + (qy - y) ** 2
        if dist < best_dist:
            best_dist, best = dist, (qx, qy)
            best_dir = np.array([dx, dy, 0.0]) / np.hypot(dx, dy)
    return np.array([best[0], best[1], 0.0]), best_dir


class GenStokesSection(_SectionBase):
    PAGE = 8
    TITLE = r"Generalized Stokes' theorem"

    def play_gen_stokes(self):
        self.nslide()
        theorem = m.MathTypst('integral_M d omega = integral_(partial M) omega #h(0.3cm) " for" omega in Omega^(n-1) (M) ", dim"(M) = n', typst_preamble=typst_preamble())
        self.add_fixed_in_frame_mobjects(theorem)
        self.play(m.Write(theorem))
        self.nslide()
        self.play(theorem.animate.next_to(self.slide_title, m.DOWN, aligned_edge=m.LEFT))
        #   The entries are separate typeset objects, evenly stacked below the theorem.
        #   The aligned pair stays one Typst object, so its `&` alignment holds, and is
        #   split into its two lines only to write them at different moments.
        font_size = 0.68 * CONTENT_FONT_SIZE
        preamble = typst_preamble(font_size)
        cube = m.Typst(
            r"Cube #h(0.3cm) $C(n)=[a,b]^n subset RR^n$",
            font_size=font_size,
            typst_preamble=preamble,
        )
        omega = m.MathTypst(
            r"omega = sum_(i=1)^n f_i (x) d x^1 and dots.h.c and d x^(i-1) and d x^(i+1) and dots.h.c and d x^n",
            font_size=font_size,
            typst_preamble=preamble,
        )
        domega = m.MathTypst(
            r"d omega = sum_(i=1)^n (-1)^(i-1) (partial f_i)/(partial x^i) d x^1 and dots.h.c and d x^n",
            font_size=font_size,
            typst_preamble=preamble,
        )
        aligned = m.MathTypst(
            r"integral_(C(n)) d omega &= sum_(i=1)^n integral_(C(n-1)) (-1)^(i-1) "
            r"({{f_i|_(x^i=b) : fidx_b}} - {{f_i|_(x^i=a) : fidx_a}}) "
            r"d x^1 dots.h.c d x^(i-1) d x^(i+1) dots.h.c d x^n \ "
            r"&= integral_(partial C(n)) omega",
            font_size=font_size,
            typst_preamble=preamble,
        )
        aligned_top, aligned_bottom = split_typst_lines(aligned)
        #   The conclusion is four display equations, each written on its own slide. They
        #   are put on one line by matching the `=` (and `⇒`) marks, which sit on the math
        #   axis: display equations are otherwise centered differently.
        def segment(code):
            return m.MathTypst(code, font_size=font_size, typst_preamble=preamble)

        terms = [
            segment(r"{{arrow.r.double : mark}} integral_M d omega"),
            segment(r"{{= : mark}} sum_i integral_(C_i) d omega"),
            segment(r"{{= : mark}} sum_i integral_(partial C_i) omega"),
            segment(r"{{= : mark}} integral_(partial M) omega"),
        ]
        axis = terms[0].select("mark").get_center()[1]
        for previous, term in zip(terms, terms[1:]):
            term.next_to(previous, m.RIGHT, buff=0.08)
            term.shift(m.UP * (axis - term.select("mark").get_center()[1]))
        integral_M, cubes, boundaries, boundary = terms
        final = m.VGroup(*terms)
        points = m.VGroup(
            cube, omega, domega, m.VGroup(aligned_top, aligned_bottom), final
        )
        points.arrange(m.DOWN, buff=0.2, aligned_edge=m.LEFT)
        points.next_to(theorem, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        self.camera.add_fixed_in_frame_mobjects(points)
        square = m.Square(3, color=m.TEAL, fill_opacity=0.5).to_edge(m.RIGHT, 1.0)
        ar = m.Arrow(square.get_corner(m.DR),square.get_corner(m.UR),buff=0, color=m.RED, max_stroke_width_to_length_ratio=10)
        al = m.Arrow(square.get_corner(m.UL),square.get_corner(m.DL),buff=0, color=m.BLUE, max_stroke_width_to_length_ratio=10)
        au = m.Arrow(square.get_corner(m.UR),square.get_corner(m.UL),buff=0, color=m.RED, max_stroke_width_to_length_ratio=10)
        ad = m.Arrow(square.get_corner(m.DL),square.get_corner(m.DR),buff=0, color=m.BLUE, max_stroke_width_to_length_ratio=10)
        square_with_arrows = m.VGroup(square, ar, al, au, ad)
        #   The whole 2D composition is pinned, like the rest of the slide's content: some
        #   earlier section leaves the camera zoomed, which would otherwise move the cube.
        self.camera.add_fixed_in_frame_mobjects(square_with_arrows)

        #   Region M: the smooth blob from section_forms, on the right side of the slide
        region_points = []
        for t in np.linspace(0.0, m.TAU, 240, endpoint=False):
            r = 1.5 + 0.28 * np.cos(3 * t) + 0.12 * np.sin(2 * t) + 0.07 * np.cos(5 * t)
            region_points.append(np.array([r * np.cos(t), r * np.sin(t), 0.0]))
        region_center = np.array([4.5, 0.1, 0.0])
        region_points = [point + region_center for point in region_points]
        region = m.Polygon(
            *region_points,
            fill_color=FRONTCOL,
            fill_opacity=0.08,
            stroke_color=FRONTCOL,
            stroke_width=2.5,
        )
        self.camera.add_fixed_in_frame_mobjects(region)

        #   Cubes: small copies of the square, without arrows, covering M's inside
        patch_side = 0.32
        half = patch_side / 2
        patch_template = m.Square(
            patch_side, color=m.TEAL, fill_opacity=0.5, stroke_width=2
        )
        patches = m.VGroup()
        patch_arrows = m.VGroup()
        inner_arrows = m.VGroup()
        outer_arrows = []
        cells = {}
        reach = int(np.ceil(2.0 / patch_side)) + 1
        for i in range(-reach, reach + 1):
            for j in range(-reach, reach + 1):
                cx = region_center[0] + i * patch_side
                cy = region_center[1] + j * patch_side
                if not inside_polygon(region_points, cx, cy):
                    continue
                patch = patch_template.copy().move_to([cx, cy, 0])
                patches.add(patch)
                cells[(i, j)] = (
                    ((i + 1, j), patch.get_corner(m.DR), patch.get_corner(m.UR), m.RED),
                    ((i, j + 1), patch.get_corner(m.UR), patch.get_corner(m.UL), m.RED),
                    ((i - 1, j), patch.get_corner(m.UL), patch.get_corner(m.DL), m.BLUE),
                    ((i, j - 1), patch.get_corner(m.DL), patch.get_corner(m.DR), m.BLUE),
                )

        #   Every patch gets the square's four arrows; on shared edges they cancel
        for (i, j), sides in cells.items():
            for (ni, nj), start, end, color in sides:
                arrow = m.Arrow(start, end, buff=0, color=color, max_stroke_width_to_length_ratio=10)
                patch_arrows.add(arrow)
                if (ni, nj) in cells:
                    arrow.set_opacity(0.5)
                    inner_arrows.add(arrow)
                else:
                    outer_arrows.append(arrow)
        self.camera.add_fixed_in_frame_mobjects(patches, patch_arrows)

        def snapped(arrow):
            """The arrow moved onto the nearest points of M's boundary."""
            start, _ = closest_on_boundary(region_points, arrow.get_start())
            end, _ = closest_on_boundary(region_points, arrow.get_end())
            return m.Arrow(start, end, buff=0, color=arrow.get_color(), max_stroke_width_to_length_ratio=10)

        self.play(m.Write(cube), m.Create(square))
        self.nslide()
        self.play(m.Write(omega))
        self.nslide()
        self.play(m.Write(domega))
        self.nslide()
        self.play(m.Write(aligned_top))
        self.nslide()
        self.play(m.Create(ar), aligned.select("fidx_b").animate(run_time=0.5).set_color(m.RED), aligned.select("fidx_b").animate(rate_func=m.there_and_back).scale(1.2))
        self.nslide()
        self.play(m.Create(al), aligned.select("fidx_a").animate(run_time=0.5).set_color(m.BLUE), aligned.select("fidx_a").animate(rate_func=m.there_and_back).scale(1.2))
        self.nslide()
        self.play(m.Create(au), aligned.select("fidx_b").animate(run_time=0.5).set_color(m.RED), aligned.select("fidx_b").animate(rate_func=m.there_and_back).scale(1.2))
        self.nslide()
        self.play(m.Create(ad), aligned.select("fidx_a").animate(run_time=0.5).set_color(m.BLUE), aligned.select("fidx_a").animate(rate_func=m.there_and_back).scale(1.2))
        self.nslide()
        self.play(m.Write(aligned_bottom))
        self.nslide()

        #   1. The cube becomes one patch beside the equation's last line
        self.play(
            square_with_arrows.animate.scale(0.2, scale_stroke=True).next_to(
                aligned_bottom, m.RIGHT, buff=0.35
            )
        )
        self.nslide()

        #   2. The integral over M: M is a smooth region
        self.play(m.Write(integral_M), m.DrawBorderThenFill(region))
        self.nslide()

        #   3. Cut M into cubes: the region's fill goes, its patches come in
        self.play(
            m.Write(cubes),
            region.animate.set_fill(opacity=0),
            m.DrawBorderThenFill(patches),
        )
        self.nslide()

        #   4. Every cube gets the square's boundary arrows
        self.play(m.Write(boundaries), m.Create(patch_arrows), patches.animate.set_fill(opacity=0), patches.animate.set_stroke(opacity=0.3))
        self.nslide()

        #   5. Neighbouring arrows cancel: only the boundary's remain
        self.play(m.FadeOut(inner_arrows))
        self.nslide()

        #   6. The boundary arrows move onto the smooth boundary of M
        self.play(
            m.Write(boundary),
            *[m.Transform(arrow, snapped(arrow)) for arrow in outer_arrows],
        )
        self.nslide()
        

class GenStokesPreview(GenStokesSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(GenStokesSection)
        self.play_gen_stokes()
