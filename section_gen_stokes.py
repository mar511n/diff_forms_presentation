""" Generalized Stokes section. """

from typing import TYPE_CHECKING

import manimgx as m

from deck import CONTENT_FONT_SIZE, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class GenStokesSection(_SectionBase):
    PAGE = 8
    TITLE = r"Generalized Stokes theorem"

    def play_gen_stokes(self):
        self.nslide()
        theorem = m.MathTypst('integral_M d omega = integral_(partial M) omega #h(0.3cm) " for" omega in Omega^(n-1) (M) ", dim"(M) = n', typst_preamble=typst_preamble())
        self.add_fixed_in_frame_mobjects(theorem)
        self.play(m.Write(theorem))
        self.nslide()
        self.play(theorem.animate.next_to(self.slide_title, m.DOWN, aligned_edge=m.LEFT))
        points = self.get_lines(theorem, """
            Cube #h(0.3cm) $C(n)=[a,b]^n in RR^n$ \n
            $omega = sum_(i=1)^n (-1)^(i-1) f_i (x) d x^1 and dots.h.c and d x^(i-1) and d x^(i+1) and dots.h.c and d x^n$ \n
            $d omega = sum_(i=1)^n (partial f_i)/(partial x^i) d x^1 and dots.h.c and d x^n$ \n
            """
            +r"$integral_(C(n)) d omega &= sum_(i=1)^n integral_(C(n-1)) (f_i|_(x^i=b)-f_i|_(x^i=a)) d x^1 dots.h.c d x^(i-1) d x^(i+1) dots.h.c d x^n \ &= integral_(partial C(n)) omega$",
            buff=m.DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            font_size=0.6*CONTENT_FONT_SIZE,
            preamble=typst_preamble(0.6*CONTENT_FONT_SIZE, leading="0.3em", display_math=True)
        )
        self.camera.add_fixed_in_frame_mobjects(*points)
        self.play(m.Write(points[3]))
        #self.play(*[m.Write(point) for point in points])
        self.nslide()

class GenStokesPreview(GenStokesSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(GenStokesSection)
        self.play_gen_stokes()
