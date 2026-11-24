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
            "geometry with nontrivial coframe $e^a$ / metric $g$ and $R eq.not 0$"
        )
        right_block = r"geometry with torsion induced dynamics ($T eq.not 0$)"

        #   Each block wraps at a bit under half the slide width, so the pair stays
        #   side by side; the fixed page width makes both boxes the same size. The
        #   width keeps `(R != 0)` on one line.
        block_width = 0.43 * MAX_TEXT_WIDTH
        preamble = block_preamble(block_width)
        left = m.Typst(left_block, font_size=CONTENT_FONT_SIZE, typst_preamble=preamble)
        right = m.Typst(right_block, font_size=CONTENT_FONT_SIZE, typst_preamble=preamble)

        arrow = m.DoubleArrow(m.ORIGIN, 2*m.RIGHT)

        m.VGroup(left, arrow, right).arrange(m.RIGHT, buff=m.MED_LARGE_BUFF).move_to(m.ORIGIN)
        left_box = m.SurroundingRectangle(left, color=FRONTCOL, buff=m.MED_SMALL_BUFF)
        right_box = m.SurroundingRectangle(right, color=FRONTCOL, buff=m.MED_SMALL_BUFF)

        self.play(m.Write(left), m.Create(left_box))
        self.nslide()
        self.play(m.Write(right), m.Create(right_box), m.Create(arrow))
        self.nslide()

        dirac_eq = m.MathTex(r"\text{minimally coupled Dirac equation} \\", r"i \gamma^a \left(", r"(d \psi)(", "e", r"_a", r") + \frac{1}{4}", r"\omega", r"_{b c}", "(", "e", r"_a", r") \gamma", r"^{b c}", r"\psi", r"\right)", "= 0")
        dirac_eq_simple = m.MathTex(r"\text{minimally coupled Dirac equation} \\", r"(d \psi)(", "e", r") + \frac{1}{4}", r"\omega", "(", "e", r") \gamma", r"\psi")
        d_arrow = m.Arrow(arrow.get_center()+0.8*m.UP, arrow.get_center(), buff=0)
        dirac_eq.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        #dirac_eq_simple[1:].next_to(left_box, m.DOWN, aligned_edge=m.LEFT)
        quant_l = m.MathTex(r"e", r", \quad", r"\omega = \omega_{\text{(LC)}}")

        self.play(m.Create(d_arrow), m.Write(dirac_eq), m.VGroup(left, left_box, right, right_box, arrow, d_arrow, dirac_eq).animate.next_to(self.slide_title, m.DOWN).set_x(0))
        self.nslide()
        dirac_eq_simple.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        quant_l.next_to(left_box, m.DOWN)
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

        point1 = m.Tex(r"$(d \psi)(e) = (d \psi)(e')\  \Longrightarrow \  e' = e$").next_to(quant_l, m.DOWN).set_x(0)
        self.play(m.Write(point1))
        self.nslide()
        point2 = m.Tex(r"$\Longrightarrow \ \omega'_{\mathrm{(LC)}}=\omega$").next_to(point1, m.DOWN).set_x(0)
        self.play(m.Write(point2))
        self.nslide()
        point3 = m.Tex(r"$\omega(e) = \omega'(e')\  \Longrightarrow \  \omega'_T = 0$").next_to(point2, m.DOWN).set_x(0)
        smiley_sad = m.Tex("🙁", font_size=3*CONTENT_FONT_SIZE).next_to(point2, m.RIGHT, buff=1.6)
        self.play(m.Write(point3), m.Write(smiley_sad))
        self.nslide()

        dirac_eq_s = m.MathTex(r"\text{Dirac equation from symmetric action} \\", r"(d \psi)(", "e", r") + \frac{1}{4}", r"\omega", "(", "e", r") \gamma", r"\psi", "-", r"\frac{1}{2}T \psi")
        dirac_eq_s.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        cond2d = m.Tex(r"in 2D: ", r"$\frac{1}{2}T = \frac{1}{4}\omega'_T(e') \gamma$")
        cond2d.next_to(quant_l, m.DOWN).set_x(0)
        wb = m.Tex(r"choose ", r"$\omega' = 0$", ", ", "$e' = e$").next_to(cond2d, m.DOWN).set_x(0)
        concl = m.Tex(r"$\Longrightarrow$ ", r"$\omega'_T = -\omega_{\mathrm{(LC)}}$").next_to(wb, m.DOWN).set_x(0)

        self.play(m.TransformMatchingTex(dirac_eq_simple, dirac_eq_s, transform_mismatches=True, fade_transform_mismatches=True), m.FadeOut(point1,point2,point3,smiley_sad))
        self.nslide()
        self.play(m.Write(cond2d))
        self.nslide()
        self.play(m.Write(wb))
        self.nslide()
        self.play(m.Write(concl))
        self.nslide()

        dirac_eq_s_r = m.MathTex(r"\text{Dirac equation from symmetric action} \\", r"(d \psi)(", "e", "'", r") + \frac{1}{4}", r"\omega", "'", "(", "e", "'", r") \gamma", r"\psi", "-", r"\frac{1}{2}T \psi")
        dirac_eq_s_r.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        self.play(m.TransformMatchingTex(dirac_eq_s, dirac_eq_s_r, transform_mismatches=True, fade_transform_mismatches=True))
        self.nslide()

        dirac_eq_s_r2 = m.MathTex(r"\text{Dirac equation from symmetric action} \\", r"(d \psi)(", "e", "'", r")", "-", r"\frac{1}{2}T \psi")
        dirac_eq_s_r2.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        self.play(
            m.TransformMatchingTex(dirac_eq_s_r, dirac_eq_s_r2, transform_mismatches=True, fade_transform_mismatches=True),
            m.Circumscribe(wb[1]),
        )
        self.remove(dirac_eq_s_r2)
        dirac_eq_s_r21 = m.MathTex(r"\text{Dirac equation from symmetric action} \\", r"(d \psi)(", "e", "'", r")", "-", r"\frac{1}{2}T", r"\psi").next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        self.add(dirac_eq_s_r21)
        self.nslide()

        dirac_eq_s_r3 = m.MathTex(r"\text{Dirac equation from symmetric action} \\", r"(d \psi)(", "e", "'", r")", "-", r"\frac{1}{4}", r"\omega", "'_T", "(e", "'", ")", r"\gamma", r"\psi")
        dirac_eq_s_r3.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        self.play(
            m.TransformMatchingTex(dirac_eq_s_r21, dirac_eq_s_r3, transform_mismatches=True, fade_transform_mismatches=True),
            m.Circumscribe(cond2d[1]),
        )
        self.nslide()

        dirac_eq_s_r4 = m.MathTex(r"\text{Dirac equation from symmetric action} \\", r"(d \psi)(", "e", r")", "+", r"\frac{1}{4}", r"\omega", r"_{\mathrm{(LC)}}", "(e", ")", r"\gamma", r"\psi")
        dirac_eq_s_r4.next_to(d_arrow, m.UP, buff=m.SMALL_BUFF)
        smiley = m.Tex("🙂", font_size=3*CONTENT_FONT_SIZE).next_to(wb, m.RIGHT, buff=1.0)
        self.play(
            m.TransformMatchingTex(dirac_eq_s_r3, dirac_eq_s_r4, transform_mismatches=True, fade_transform_mismatches=True),
            m.Circumscribe(wb[3]),
            m.Circumscribe(concl[1]),
        )
        self.play(m.Write(smiley))
        self.nslide()

        

        


class MetricTorsionPreview(MetricTorsionSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(MetricTorsionSection)
        self.play_metric_torsion()
