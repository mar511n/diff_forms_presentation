"""Local differential forms visualization section."""

from typing import TYPE_CHECKING, NamedTuple, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path

import manimgx as m

from deck import (
    CONTENT_FONT_SIZE,
    FRONTCOL,
    DeckScene,
    typst_preamble,
)

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class FormsVis2Section(_SectionBase):
    PAGE = 4
    TITLE = r"Differential forms in higher dimensions"

    def play_formsvis2(self):
        self.nslide()
        points = self.get_lines(self.slide_title, """- locally a $k$-form in an $n$-dimensional Manifold corresponds to a set of $(n - k)$-dimensional objects""")
        self.camera.add_fixed_in_frame_mobjects(*points)
        for point in points:
            self.play(m.Write(point))
            self.nslide()

        self.set_camera_orientation(
            phi=65 * m.DEGREES, theta=-55 * m.DEGREES, zoom=0.85
        )

        label_size = CONTENT_FONT_SIZE
        label1 = m.Typst(
            r"*1-forms in 3D*",
            font_size=label_size,
            typst_preamble=typst_preamble(label_size),
        ).next_to(points[-1], m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        label2 = m.Typst(
            r"*2-forms in 3D*",
            font_size=label_size,
            typst_preamble=typst_preamble(label_size),
        ).move_to(label1)
        self.camera.add_fixed_in_frame_mobjects(label1, label2)

        #   1-form: the level sets of dy are planes x-z at equally spaced y.
        plane_ys = np.linspace(-2.0, 2.0, 5)
        planes = m.VGroup(
            *[
                m.Polygon(
                    [-2.2, y, -1.35],
                    [2.2, y, -1.35],
                    [2.2, y, 1.35],
                    [-2.2, y, 1.35],
                    fill_color=m.BLUE,
                    fill_opacity=0.12,
                    stroke_color=m.BLUE,
                    stroke_width=1.5,
                )
                for y in plane_ys
            ]
        )

        def gamma(t):
            return np.array(
                [
                    1.1 * np.cos(m.TAU * t),
                    -2.2 + 4.4 * t,
                    0.9 * np.sin(m.TAU * t),
                ]
            )

        curve = m.ParametricFunction(
            gamma, t_range=[0.0, 1.0, 0.01], color=m.YELLOW, stroke_width=4
        )
        intersections = m.VGroup(
            *[
                m.Dot3D(gamma((y + 2.2) / 4.4), radius=0.07, color=m.RED)
                for y in plane_ys
            ]
        )

        self.play(m.Write(label1))
        self.play(
            m.LaggedStart(
                *[m.FadeIn(plane, shift=0.2 * m.OUT) for plane in planes],
                lag_ratio=0.15,
            )
        )
        self.nslide()

        self.play(m.Create(curve))
        self.nslide()

        self.play(m.FadeOut(planes), m.FadeIn(intersections))
        self.nslide()

        self.play(
            m.FadeOut(curve),
            m.FadeOut(intersections),
            m.ReplacementTransform(label1, label2),
        )
        self.nslide()

        #   2-form: the level sets of dx and dy are lines in the z direction.
        grid = np.linspace(-2.0, 2.0, 5)

        def plane_z(x, y):
            return 0.28 * x + 0.16 * y

        lines = m.VGroup(
            *[
                m.Line3D(
                    [x, y, -1.35],
                    [x, y, 1.35],
                    thickness=0.012,
                    resolution=6,
                    color=FRONTCOL,
                )
                for x in grid
                for y in grid
            ]
        )
        base_dots = m.VGroup(
            *[
                m.Dot3D([x, y, -1.35], radius=0.03, color=FRONTCOL)
                for x in grid
                for y in grid
            ]
        )
        surface = m.Polygon(
            [-2.2, -2.2, plane_z(-2.2, -2.2)],
            [2.2, -2.2, plane_z(2.2, -2.2)],
            [2.2, 2.2, plane_z(2.2, 2.2)],
            [-2.2, 2.2, plane_z(-2.2, 2.2)],
            fill_color=m.TEAL,
            fill_opacity=0.18,
            stroke_color=m.TEAL,
            stroke_width=2,
        )
        surface_cuts = m.VGroup(
            *[
                m.Dot3D([x, y, plane_z(x, y)], radius=0.06, color=m.YELLOW)
                for x in grid
                for y in grid
            ]
        )

        self.play(
            m.LaggedStart(
                *[m.Create(line) for line in lines], lag_ratio=0.02, run_time=2
            ),
            m.FadeIn(base_dots),
        )
        self.nslide()

        self.play(m.DrawBorderThenFill(surface))
        self.nslide()

        self.play(
            m.FadeOut(lines),
            m.FadeOut(base_dots),
            m.FadeIn(surface_cuts),
        )
        self.nslide()
        


class FormsVisPreview(FormsVis2Section, DeckScene):
    def construct(self) -> None:
        self.prepare_section(FormsVis2Section)
        self.play_formsvis2()
