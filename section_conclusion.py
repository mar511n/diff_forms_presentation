"""Conclusion: the talk's threads, one point and one result per row.

Each point is written on the left while its formula or picture appears on the
right. When the next point arrives, the previous result shrinks into the margin
and stays there, so the whole argument remains visible at the end.
"""

from typing import TYPE_CHECKING

import manimgx as m
import numpy as np

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


LEFT_FONT_SIZE = CONTENT_FONT_SIZE
MATH_FONT_SIZE = 1.2 * CONTENT_FONT_SIZE

#   The six rows share the slide height. The left column holds the sentence,
#   the right column the matching formula or picture. The right column
#   alternates between two centres, so consecutive results sit left and right
#   of each other instead of directly above one another.
ROW_Y = [2.15 - index * 0.92 for index in range(6)]
LEFT_X = -6.75
LEFT_WIDTH = 5.2
RIGHT_CENTERS = [1.9, 4.0]
ACTIVE_WIDTH = 5.8
ACTIVE_HEIGHT = 1.3
PREVIOUS_SCALE = 0.62

def text_preamble(width, font_size=LEFT_FONT_SIZE):
    """Typst page setup that wraps text at `width` scene units."""
    width_pt = width / (font_size * m.SCALE_FACTOR_PER_FONT_POINT)
    return (
        f"\n#set page(width: {width_pt:.3f}pt, height: auto, margin: 0pt, fill: none)"
    )


def formula(*parts):
    """A formula at this slide's size, split into separately addressable parts."""
    return m.MathTex(
        *parts,
        font_size=MATH_FONT_SIZE,
        typst_preamble=typst_preamble(MATH_FONT_SIZE),
    )


def form_picture():
    """A blue plane pierced by nine upward red lines at yellow points."""
    #   A shallow parallelogram in perspective: the 3×3 points sit on it and
    #   the lines rise out of them, so the picture has room to be large.
    first = np.array([1.35, 0.08, 0.0])
    second = np.array([0.38, 0.24, 0.0])
    corner = 1.2
    plane = m.Polygon(
        corner * first + corner * second,
        corner * first - corner * second,
        -corner * first - corner * second,
        -corner * first + corner * second,
        fill_color=m.BLUE,
        fill_opacity=0.28,
        stroke_color=m.BLUE,
        stroke_width=2.4,
    )
    points = [
        offset * first + other * second
        for offset in (-1, 0, 1)
        for other in (-1, 0, 1)
    ]
    lines = m.VGroup(
        *[
            m.Line(
                point - 0.50 * m.UP,
                point + 0.50 * m.UP,
                color=m.RED,
                stroke_width=3.2,
            )
            for point in points
        ]
    )
    dots = m.VGroup(
        *[m.Dot(point, radius=0.085, color=m.YELLOW) for point in points]
    )
    return m.VGroup(plane, lines, dots)


def stokes_formula():
    return formula(
        r"\int_{\partial M}", r"\omega", "=", r"\int_M", r"d\omega"
    )


def poincare_formula():
    return formula(
        r"d\beta",
        "=",
        "0",
        r"\;\Longrightarrow\;",
        r"\beta",
        "=",
        r"d\alpha",
    )


def cartan_formulas():
    torsion = formula("T^a", "=", r"d e^a", "+", r"\omega^a{}_b", r"\wedge e^b")
    curvature = formula(
        "R^a{}_b", "=", r"d\omega^a{}_b", "+", r"\omega^a{}_c", r"\wedge\omega^c{}_b"
    )
    return m.VGroup(torsion, curvature).arrange(m.DOWN, buff=0.06, aligned_edge=m.LEFT)


def burgers_formula():
    return formula("b^a", "=", r"\int_S", "T^a")


def maxwell_formulas():
    return formula(
        r"dF",
        "=",
        "0",
        r",\qquad",
        r"d\star F",
        "=",
        "J",
    )


class ConclusionSection(_SectionBase):
    PAGE = 16
    TITLE = r"Conclusion"

    def play_conclusion(self):
        self.set_camera_orientation(phi=0, theta=-90 * m.DEGREES)
        self.nslide()

        points = [
            r"- interpretation of differential $k$-forms",
            r"- generalized Stokes' theorem",
            r"- Poincaré lemma",
            r"- Cartan structure equations",
            r"- dislocations as torsion",
            r"- less indices, simpler equations",
        ]
        results = [
            form_picture(),
            stokes_formula(),
            poincare_formula(),
            cartan_formulas(),
            burgers_formula(),
            maxwell_formulas(),
        ]

        #   Place every row before the reveal, so each point and its result are
        #   written at the same moment.
        rows = []
        for index, (y, text, result) in enumerate(zip(ROW_Y, points, results)):
            point = m.Typst(
                text,
                font_size=LEFT_FONT_SIZE,
                typst_preamble=text_preamble(LEFT_WIDTH),
            )
            point.move_to([LEFT_X, y, 0], aligned_edge=m.LEFT)
            factor = min(ACTIVE_WIDTH / result.width, ACTIVE_HEIGHT / result.height)
            if factor < 1.0:
                result.scale(factor)
            result.move_to([RIGHT_CENTERS[index % 2], y, 0])
            self.camera.add_fixed_in_frame_mobjects(point, result)
            rows.append((point, result))

        #   The first row: the 3×3 picture is drawn while its point is written.
        first_point, first = rows[0]
        self.play(
            m.Write(first_point),
            m.DrawBorderThenFill(first[0]),
            m.Create(first[1]),
            m.FadeIn(first[2]),
        )
        self.nslide()

        #   Each later result appears large; the result before it shrinks in
        #   place. Because the rows alternate sides, the shrunken results form
        #   a readable zig-zag down the right half of the slide.
        for index in range(1, len(rows)):
            point, current = rows[index]
            previous = rows[index - 1][1]
            self.play(
                m.Write(point),
                m.Write(current),
                previous.animate.scale(PREVIOUS_SCALE),
            )
            self.nslide()


class ConclusionPreview(ConclusionSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(ConclusionSection)
        self.play_conclusion()
