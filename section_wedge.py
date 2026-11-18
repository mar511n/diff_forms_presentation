"""Wedge product section."""

from typing import TYPE_CHECKING

import numpy as np

import manimgx as m

from deck import CONTENT_FONT_SIZE, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class WedgeSection(_SectionBase):
    PAGE = 5
    TITLE = r"Wedge product $and$"

    def play_wedge(self):
        self.nslide()
        formula = m.MathTypst('(alpha and beta)(v_1, dots, v_(k+l)) = 1/(k! l!) sum_(sigma) "sgn"(sigma) alpha(v_(sigma(1)), dots, v_(sigma(k))) beta(v_(sigma(k+1)), dots, v_(sigma(k+l)))', typst_preamble=typst_preamble())
        formula.next_to(self.slide_title, m.DOWN, m.MED_SMALL_BUFF, m.LEFT)
        self.camera.add_fixed_in_frame_mobjects(formula)
        self.play(m.Write(formula))
        self.nslide()

        self.set_camera_orientation(
            phi=65 * m.DEGREES, theta=-25 * m.DEGREES, zoom=1.0, frame_center=(0,0,m.config.frame_height*0.09)
        )

        label_size = CONTENT_FONT_SIZE
        dx_label = m.Typst(
            r"$d x$",
            font_size=label_size,
            fill_color=m.BLUE,
            typst_preamble=typst_preamble(label_size),
        ).next_to(formula, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        dy_label = m.Typst(
            r"$d y$",
            font_size=label_size,
            fill_color=m.RED,
            typst_preamble=typst_preamble(label_size),
        ).next_to(dx_label, m.DOWN, buff=m.SMALL_BUFF, aligned_edge=m.LEFT)
        wedge_label = m.Typst(
            r"$d x and d y$",
            font_size=label_size,
            fill_color=m.YELLOW,
            typst_preamble=typst_preamble(label_size),
        ).next_to(dy_label, m.DOWN, buff=m.SMALL_BUFF, aligned_edge=m.LEFT)
        self.camera.add_fixed_in_frame_mobjects(dx_label, dy_label, wedge_label)

        #   dx: the level sets of dx are planes y-z at equally spaced x.
        plane_xs = np.linspace(-2.0, 2.0, 3)
        dx_planes = m.VGroup(
            *[
                m.Polygon(
                    [x, -2.2, -1.35],
                    [x, 2.2, -1.35],
                    [x, 2.2, 1.35],
                    [x, -2.2, 1.35],
                    fill_color=m.BLUE,
                    fill_opacity=0.5,
                    stroke_color=m.BLUE,
                    stroke_width=1.5,
                )
                for x in plane_xs
            ]
        )

        #   dy: the level sets of dy are planes x-z at equally spaced y.
        plane_ys = np.linspace(-2.0, 2.0, 3)
        dy_planes = m.VGroup(
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

        #   dx and dy agree on the lines where their planes cross.
        intersection_lines = m.VGroup(
            *[
                m.Line3D(
                    [x, y, -1.35],
                    [x, y, 1.35],
                    thickness=0.02,
                    resolution=6,
                    color=m.YELLOW,
                )
                for x in plane_xs
                for y in plane_ys
            ]
        )

        self.play(
            m.Write(dx_label),
            m.LaggedStart(
                *[m.FadeIn(plane, shift=0.2 * m.RIGHT) for plane in dx_planes],
                lag_ratio=0.15,
            ),
        )
        self.nslide()

        self.play(
            m.Write(dy_label),
            m.LaggedStart(
                *[m.FadeIn(plane, shift=0.2 * m.UP) for plane in dy_planes],
                lag_ratio=0.15,
            ),
        )
        self.nslide()

        self.play(
            m.Write(wedge_label),
            m.LaggedStart(
                *[m.Create(line) for line in intersection_lines],
                lag_ratio=0.02,
                run_time=2,
            ),
        )
        self.nslide()

        self.play(m.FadeOut(dx_planes), m.FadeOut(dy_planes))
        self.nslide()


class WedgePreview(WedgeSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(WedgeSection)
        self.play_wedge()
