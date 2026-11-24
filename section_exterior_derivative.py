"""Exterior derivative section."""

from typing import TYPE_CHECKING

import manimgx as m

from deck import CONTENT_FONT_SIZE, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class ExteriorDerivativeSection(_SectionBase):
    PAGE = 6
    TITLE = r"Exterior derivative $d$"

    def play_ext_deriv(self):
        self.nslide()
        points = self.get_lines(self.slide_title, """
        - *unique* $RR$-linear operator $d : Omega^k (M) arrow.r.long Omega^(k+1)(M)$ which fulfills:
         - for a $0$-form $f$, the exterior derivative $d f$ is the differential
         - graded Leibniz rule: $d(alpha and beta) = d alpha and beta + (-1)^k alpha and d beta$ #h(0.3cm) for $alpha in Omega^k (M)$
         - nilpotence: $d^2 = 0$
        - For a $k$-form expressed in a coordinate basis:
        """)
        self.camera.add_fixed_in_frame_mobjects(*points)
        for point in points:
            self.play(m.Write(point))
            self.nslide()
        kform = m.MathTypst('omega = sum_(i_1 < dots.h.c < i_k) f_(i_1 dots.h.c i_k) d x^(i_1) and dots.h.c and d x^(i_k)', typst_preamble=typst_preamble())
        kform.next_to((0, points[-1].get_bottom()[1],0),m.DOWN)
        #dkform = m.MathTypst('d omega = sum_(i_1 < dots.h.c < i_k) sum_j (partial f_(i_1 dots.h.c i_k))/(partial x^j) d x^j and d x^(i_1) and dots.h.c and d x^(i_k)', typst_preamble=typst_preamble())
        dkform1 = m.MathTex(r'd \omega = \sum_{i_1 < \cdots < i_k}', r'd f_{i_1 \cdots i_k}', r'\wedge d x^{i_1} \wedge \cdots \wedge d x^{i_k}', typst_preamble=typst_preamble())
        dkform2 = m.MathTex(r'd \omega = \sum_{i_1 < \cdots < i_k}', r'\sum_j \frac{\partial f_{i_1 \cdots i_k}}{\partial x^j} d x^j', r'\wedge d x^{i_1} \wedge \cdots \wedge d x^{i_k}', typst_preamble=typst_preamble())
        dkform1.next_to(kform,m.DOWN)
        dkform2.next_to(kform,m.DOWN)
        self.play(m.Write(kform))
        self.nslide()
        self.play(m.Write(dkform1))
        self.nslide()
        self.play(m.TransformMatchingTex(dkform1,dkform2,transform_mismatches=True,fade_transform_mismatches=True))
        self.nslide()


class ExteriorDerivativePreview(ExteriorDerivativeSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(ExteriorDerivativeSection)
        self.play_ext_deriv()
