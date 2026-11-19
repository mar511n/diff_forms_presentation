"""Poincaré lemma: exact and closed forms, and the vector-calculus special cases."""

from typing import TYPE_CHECKING

import manimgx as m

from deck import CONTENT_FONT_SIZE, FRONTCOL, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class PoincareSection(_SectionBase):
    PAGE = 10
    TITLE = r"Poincaré lemma"

    def play_poincare(self):
        self.nslide()
        statement_size = 1.25 * CONTENT_FONT_SIZE
        arrow_size = 1.8 * CONTENT_FONT_SIZE
        label_size = 0.8 * CONTENT_FONT_SIZE
        table_size = 0.9 * CONTENT_FONT_SIZE
        statement_preamble = typst_preamble(statement_size)
        arrow_preamble = typst_preamble(arrow_size)
        label_preamble = typst_preamble(label_size)
        table_preamble = typst_preamble(table_size)

        def math(code):
            return m.MathTypst(
                code, font_size=table_size, typst_preamble=table_preamble
            )

        def text(code):
            return m.Typst(code, font_size=table_size, typst_preamble=table_preamble)

        #   β = dα on the left, dβ = 0 on the right: nilpotence points right, the
        #   Poincaré lemma points back.
        exact = m.MathTypst(
            r"beta = d alpha",
            font_size=statement_size,
            typst_preamble=statement_preamble,
        )
        closed = m.MathTypst(
            r"d beta = 0",
            font_size=statement_size,
            typst_preamble=statement_preamble,
        )
        statements = m.VGroup(exact, closed).arrange(m.RIGHT, buff=2.4)
        statements.move_to([0, 1.8, 0])

        forward = m.Typst(
            r"$arrow.r.double.long$",
            font_size=arrow_size,
            typst_preamble=arrow_preamble,
        )
        forward.next_to([0,exact.get_center()[1],0], m.UP, buff=0)
        nilpotence = m.Typst(
            "nilpotence", font_size=label_size, typst_preamble=label_preamble
        ).next_to(forward, m.UP, buff=0.1)

        backward = m.Typst(
            r"$arrow.l.double.long$",
            font_size=arrow_size,
            typst_preamble=arrow_preamble,
        ).next_to([0,exact.get_center()[1],0], m.DOWN, buff=0)
        poincare = m.Typst(
            "Poincaré lemma", font_size=label_size, typst_preamble=label_preamble
        ).next_to(backward, m.DOWN, buff=0.1)

        #   The vector-calculus special cases, one row per potential.
        table = m.MobjectTable(
            [
                [
                    text("Gradient potential"),
                    math(r"F_x d x + F_y d y + F_z d z"),
                    math(r"bold(nabla) times bold(F) = 0"),
                    math(r"bold(F) = bold(nabla) f"),
                ],
                [
                    text("Vector potential"),
                    math(
                        r"F_x d y and d z #linebreak() + F_y d z and d x + F_z d x and d y"
                    ),
                    math(r"bold(nabla) dot bold(F) = 0"),
                    math(r"bold(F) = bold(nabla) times bold(A)"),
                ],
            ],
            col_labels=[
                text("*Potential*"),
                math("beta"),
                math("d beta = 0"),
                math("beta = d alpha"),
            ],
            v_buff=0.25,
            h_buff=0.5,
            include_outer_lines=True,
            line_config={"color": FRONTCOL, "stroke_width": 1.5},
        )
        table.next_to(poincare, m.DOWN, buff=m.LARGE_BUFF).set_x(0)

        rows = table.get_rows()
        table.remove(table.elements)

        self.camera.add_fixed_in_frame_mobjects(
            exact,
            closed,
            forward,
            nilpotence,
            backward,
            poincare,
            table,
            *rows,
        )

        self.play(m.Write(exact))
        self.nslide()
        self.play(m.Write(forward), m.Write(nilpotence), m.Write(closed))
        self.nslide()
        self.play(m.Write(backward), m.Write(poincare))
        self.nslide()
        self.play(m.Create(table), m.Write(rows[0]))
        self.nslide()
        for row in rows[1:]:
            self.play(m.Write(row))
            self.nslide()


class PoincarePreview(PoincareSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(PoincareSection)
        self.play_poincare()
