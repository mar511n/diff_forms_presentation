"""Metric <--> torsion mapping: the two geometries and the arrow between them."""

from typing import TYPE_CHECKING

import manimgx as m

from deck import (
    CONTENT_FONT_SIZE,
    FRONTCOL,
    MAX_TEXT_WIDTH,
    DeckScene,
    typst_preamble,
)

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


def block_preamble(width, font_size=CONTENT_FONT_SIZE):
    """Typst page setup that wraps a block at `width` scene units, centred."""
    width_pt = width / (font_size * m.SCALE_FACTOR_PER_FONT_POINT)
    return (
        f"\n#set page(width: {width_pt:.3f}pt, height: auto, margin: 0pt, fill: none)"
        "\n#set align(center)"
    )


class MetricTorsionSection(_SectionBase):
    PAGE = 15
    TITLE = r"Metric $arrow.l.r$ torsion mapping"

    def play_metric_torsion(self):
        self.nslide()

        left_block = (
            "geometry with nontrivial vielbein $e^a$ / metric $g$ and $R eq.not 0$"
        )
        right_block = r"geometry with torsion induced dynamics \ ($T eq.not 0$)"

        #   Each block wraps at a bit under half the slide width, so the pair stays
        #   side by side; the fixed page width makes both boxes the same size. The
        #   width keeps `(R != 0)` on one line.
        block_width = 0.3 * MAX_TEXT_WIDTH
        preamble = block_preamble(block_width)
        left = m.Typst(left_block, font_size=CONTENT_FONT_SIZE, typst_preamble=preamble)
        right = m.Typst(right_block, font_size=CONTENT_FONT_SIZE, typst_preamble=preamble)

        arrow = m.DoubleArrow(left.get_right(), right.get_left())

        m.VGroup(left, arrow, right).arrange(m.RIGHT, buff=m.MED_LARGE_BUFF).move_to(m.ORIGIN)
        left_box = m.SurroundingRectangle(left, color=FRONTCOL, buff=m.MED_SMALL_BUFF)
        right_box = m.SurroundingRectangle(right, color=FRONTCOL, buff=m.MED_SMALL_BUFF)

        self.play(m.Write(left), m.Create(left_box))
        self.nslide()
        self.play(m.Write(right), m.Create(right_box), m.Create(arrow))
        self.nslide()

        dirac_eq = m.MathTex(r"\text{Dirac equation} \\", r"$i \gamma^a \left(", r"(d \psi)(e", r"_a", r") + \frac{1}{4} \omega", r"_{b c}", r"(e", r"_a", r") \gamma", r"^{b c}", r"\psi", r"\right)$")
        dirac_eq_simple = m.MathTex(r"\text{Dirac equation} \\", r"(d \psi)(e", r") + \frac{1}{4} \omega", r"(e", r") \gamma", r"\psi")
        d_arrow = m.Arrow(arrow.get_center()+m.UP, arrow.get_center(), buff=0)
        dirac_eq.next_to(d_arrow, m.UP)
        #dirac_eq_simple[1:].next_to(left_box, m.DOWN, aligned_edge=m.LEFT)
        quant_l = m.MathTex(r"e", r", \quad", r"\omega_{\text{(LC)}}").next_to(left_box, m.DOWN)

        self.play(m.Create(d_arrow), m.Write(dirac_eq), m.VGroup(left, left_box, right, right_box, arrow, d_arrow, dirac_eq).animate.next_to(self.slide_title, m.DOWN).set_x(0))
        self.nslide()
        dirac_eq_simple.next_to(d_arrow, m.UP)
        self.play(m.TransformMatchingTex(dirac_eq, dirac_eq_simple, transform_mismatches=True, fade_transform_mismatches=True), m.Write(quant_l))
        self.nslide()

        cse = m.MathTex(r"e', \quad", r"T^a", "=", "d e'^a", "+", r"\omega'^a{}_b \wedge e'^b").next_to(right_box, m.DOWN)
        cse2 = m.MathTex(r"e', \quad", r"\omega'^a{}_b \wedge e'^b", "=", "-", "d e'^a", "+", r"T^a").next_to(right_box, m.DOWN)
        cse3 = m.MathTex(r"e', \quad", r"\omega'", "=", r"\omega'_{\mathrm{(LC)}}", "+", r"\omega'_T").next_to(right_box, m.DOWN)
        self.play(m.Write(cse))
        self.nslide()
        self.play(m.TransformMatchingTex(cse, cse2, transform_mismatches=True, fade_transform_mismatches=True))
        self.nslide()
        self.play(m.TransformMatchingTex(cse2, cse3, transform_mismatches=True, fade_transform_mismatches=True))
        self.nslide()
        

        


class MetricTorsionPreview(MetricTorsionSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(MetricTorsionSection)
        self.play_metric_torsion()
