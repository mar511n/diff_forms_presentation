"""Local differential forms visualization section."""

from typing import TYPE_CHECKING

import numpy as np

import manimgx as m

from deck import (
    CONTENT_FONT_SIZE,
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
        points = self.get_lines(self.slide_title, """- locally a $k$-form in an $n$-dimensional manifold corresponds to a set of $(n - k)$-dimensional objects""")
        self.camera.add_fixed_in_frame_mobjects(*points)
        for point in points:
            self.play(m.Write(point))
            self.nslide()

        self.set_camera_orientation(
            phi=65 * m.DEGREES, theta=-25 * m.DEGREES, zoom=1.0, frame_center=(0,0,m.config.frame_height*0.09)
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
                    fill_color=m.RED,
                    fill_opacity=0.5,
                    stroke_color=m.RED,
                    stroke_width=1.5,
                )
                for y in plane_ys
            ]
        )

        def gamma(t):
            return np.array(
                [
                    1.1 * np.cos(m.TAU * t + m.PI),
                    -2 + 4 * t,
                    1.1 * np.sin(m.TAU * t + m.PI),
                ]
            )

        curve = m.ParametricFunction(
            gamma, t_range=[-0.05, 1.05, 0.01], color=m.BLUE, stroke_width=4
        )
        intersections = m.VGroup(
            *[
                m.Dot3D(gamma((y + 2) / 4), radius=0.07, color=m.YELLOW)
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
        self.play(m.Create(intersections))
        self.nslide()
        self.play(m.FadeOut(planes))
        self.nslide()

        #   2-form: the level sets of dx and dy are lines in the z direction.
        grid = np.linspace(-2.0, 2.0, 3)

        def plane_z(x, y):
            return 0.28 * x + 0.16 * y

        lines = m.VGroup(
            *[
                m.Line3D(
                    [x, y, -1.35],
                    [x, y, 1.35],
                    thickness=0.02,
                    resolution=6,
                    color=m.RED,
                )
                for x in grid
                for y in grid
            ]
        )
        surface = m.Polygon(
            [-2.2, -2.2, plane_z(-2.2, -2.2)],
            [2.2, -2.2, plane_z(2.2, -2.2)],
            [2.2, 2.2, plane_z(2.2, 2.2)],
            [-2.2, 2.2, plane_z(-2.2, 2.2)],
            fill_color=m.BLUE,
            fill_opacity=0.5,
            stroke_color=m.BLUE,
            stroke_width=1.5,
        )
        surface_cuts = m.VGroup(
            *[
                m.Dot3D([x, y, plane_z(x, y)], radius=0.06, color=m.YELLOW)
                for x in grid
                for y in grid
            ]
        )

        self.play(
            m.Uncreate(curve),
            m.Uncreate(intersections),
            m.ReplacementTransform(label1, label2),
            m.LaggedStart(
                *[m.Create(line) for line in lines], lag_ratio=0.02, run_time=2
            ),
        )
        self.nslide()
        self.play(m.DrawBorderThenFill(surface))
        self.nslide()
        self.play(m.Create(surface_cuts))
        self.nslide()
        self.play(m.Uncreate(lines))
        self.nslide()
        


class FormsVis2Preview(FormsVis2Section, DeckScene):
    def construct(self) -> None:
        self.prepare_section(FormsVis2Section)
        self.play_formsvis2()
