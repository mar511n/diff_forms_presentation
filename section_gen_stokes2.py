"""Generalized Stokes theorem: the table of its special cases."""

from typing import TYPE_CHECKING

import manimgx as m

from deck import CONTENT_FONT_SIZE, FRONTCOL, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class GenStokes2Section(_SectionBase):
    PAGE = 9
    TITLE = r"Generalized Stokes theorem: special cases"

    def play_gen_stokes2(self):
        self.nslide()
        font_size = 0.55 * CONTENT_FONT_SIZE
        preamble = typst_preamble(font_size)

        def math(code):
            return m.MathTypst(code, font_size=font_size, typst_preamble=preamble)

        def text(code):
            return m.Typst(code, font_size=font_size, typst_preamble=preamble)

        #   The table from the notes: one row per theorem, one column per ingredient.
        #   The text cells are broken by hand so the columns stay narrow; `#linebreak()`
        #   also works inside a MathTypst cell.
        table = m.MobjectTable(
            [
                [
                    text("Generalized Stokes"),
                    text(r"oriented $(k+1)$-manifold #linebreak() with boundary"),
                    text(r"$k$-form"),
                    text("exterior derivative"),
                    math(r"integral_M d omega = integral_(partial M) omega"),
                ],
                [
                    text("Fundamental theorem #linebreak() of calculus"),
                    text(r"$[a,b]$"),
                    text(r"$f$"),
                    math(r"f'(x) d x"),
                    math(r"integral_a^b f'(x) d x = f(b) - f(a)"),
                ],
                [
                    text("Gradient theorem"),
                    text(r"oriented curve $gamma$ #linebreak() from $a$ to $b$"),
                    text(r"$f$"),
                    math(r"d f"),
                    math(r"integral_gamma bold(nabla) f dot d bold(r) = f(b) - f(a)"),
                ],
                [
                    text("Green's theorem"),
                    text(r"plane region $D$"),
                    math(r"P d x + Q d y"),
                    math(r"(partial_x Q - partial_y P) d x and d y"),
                    math(
                        r"integral.double_D (partial_x Q - partial_y P) d A "
                        r"= integral.cont_(partial D) P d x + Q d y"
                    ),
                ],
                [
                    text("Stokes theorem"),
                    text(r"oriented surface $S$"),
                    math(r"F_x d x + F_y d y + F_z d z"),
                    math(r"(bold(nabla) times bold(F)) dot d bold(A)"),
                    math(
                        r"integral.double_S (bold(nabla) times bold(F)) dot d bold(A) "
                        r"= integral.cont_(partial S) bold(F) dot d bold(r)"
                    ),
                ],
                [
                    text("Gauss theorem"),
                    text(r"volume $V$"),
                    math(
                        r"F_x d y and d z + F_y d z and d x "
                        r"#linebreak() + F_z d x and d y"
                    ),
                    math(r"(bold(nabla) dot bold(F)) d V"),
                    math(
                        r"integral.triple_V (bold(nabla) dot bold(F)) d V "
                        r"= integral.double_(partial V) bold(F) dot d bold(A)"
                    ),
                ],
            ],
            col_labels=[
                text("*Theorem*"),
                math("M"),
                math("omega"),
                math("d omega"),
                text("*Equation*"),
            ],
            v_buff=0.22,
            h_buff=0.2,
            include_outer_lines=True,
            line_config={"color": FRONTCOL, "stroke_width": 1.5},
        )
        table.next_to(self.slide_title, m.DOWN, buff=m.MED_LARGE_BUFF).set_x(0)

        #   The entries are written row by row, so only the lines are shown at first.
        rows = table.get_rows()
        table.remove(table.elements)
        self.camera.add_fixed_in_frame_mobjects(table, *rows)

        self.play(m.Create(table), m.Write(rows[0]))
        self.nslide()
        for row in rows[1:]:
            self.play(m.Write(row))
            self.nslide()


class GenStokes2Preview(GenStokes2Section, DeckScene):
    def construct(self) -> None:
        self.prepare_section(GenStokes2Section)
        self.play_gen_stokes2()
