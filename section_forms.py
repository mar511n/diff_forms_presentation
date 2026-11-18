"""Differential forms: the definition bullets and the machines visualization."""

from typing import TYPE_CHECKING

import numpy as np

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


class FormsSection(_SectionBase):
    PAGE = 2
    TITLE = r"Differential $k$-form $omega in Omega^k (M)$"

    def play_forms(self):
        self.nslide()
        points = self.get_lines(self.slide_title, """
        - smooth assignment $p arrow.r.long.bar omega|_p$ for a point $p$ on the Manifold $M$
        - $omega|_p$ is an _alternating_ *$k$-linear* map $omega|_p: underbrace(T_p M times dots.c times T_p M, k " times") arrow.r.long RR$
        """)
        self.camera.add_fixed_in_frame_mobjects(*points)
        for point in points:
            self.play(m.Write(point))
            self.nslide()

        machine_bullet = m.Typst(
            r"- Interpretation: Different machines "
            r'#box[$omega$]<omega>$|_p (manimgrp("v1", v_1), manimgrp("v2", v_2), v_3) '
            r'manimgrp("eq", eq) #h(2.6em)$',
            typst_preamble=(
                typst_preamble()
                + "\n#let manimgrp(lbl, body) = [#box(math.inline(body)) #label(lbl)]"
            ),
        )
        machine_bullet.next_to(points[-1], m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        self.camera.add_fixed_in_frame_mobjects(machine_bullet)
        omega = machine_bullet.select("omega")
        v1 = machine_bullet.select("v1")
        v2 = machine_bullet.select("v2")
        eq = machine_bullet.select("eq")

        def machine_value(p):
            return 50.0 + 20.0 * np.sin(2.3 * p[0]) + 10.0 * np.cos(1.9 * p[1])

        region_points = []
        for t in np.linspace(0.0, m.TAU, 240, endpoint=False):
            r = 1.5 + 0.28 * np.cos(3 * t) + 0.12 * np.sin(2 * t) + 0.07 * np.cos(5 * t)
            region_points.append([r * np.cos(t), r * np.sin(t), 0.0])
        region_center = np.array([0.6, -1.75, 0.0])
        region = m.Polygon(
            *region_points,
            fill_color=FRONTCOL,
            fill_opacity=0.08,
            stroke_color=FRONTCOL,
            stroke_width=2.5,
        )
        region.move_to(region_center)
        self.camera.add_fixed_in_frame_mobjects(region)

        gears = [
            m.Typst("#text[⚙]", font_size=50).set_color(color)
            for color in (m.RED, m.YELLOW, m.BLUE)
        ]
        machine_offsets = (
            np.array([-0.25, 1.1, 0.0]),
            np.array([-0.5, 0.2, 0.0]),
            np.array([-0.5, -0.9, 0.0]),
        )
        for gear, offset in zip(gears, machine_offsets):
            gear.move_to(region_center + offset)
        self.camera.add_fixed_in_frame_mobjects(*gears)

        #   The selected machine and its vector arguments, next to it
        gear_sel = gears[1]
        color_sel = m.YELLOW
        vec_label = m.Typst(
            r'(#box[$arrow.tl$]<a1>,#box[$arrow.r$]<a2>,$arrow.b$)',
            typst_preamble=typst_preamble(),
        )
        vec_label.next_to(gear_sel, m.RIGHT, buff=0.2)
        self.camera.add_fixed_in_frame_mobjects(vec_label)
        a1 = vec_label.select("a1")
        a2 = vec_label.select("a2")

        #   Equals sign and example number: invisible until a machine is selected
        number = m.DecimalNumber(0.0, num_decimal_places=1, font_size=CONTENT_FONT_SIZE)
        number.set_value(machine_value(gear_sel.get_center()))
        number.next_to(eq, m.RIGHT, buff=0.12)
        eq.set_opacity(0)
        number.set_opacity(0)
        self.camera.add_fixed_in_frame_mobjects(number)

        self.play(m.Write(machine_bullet))
        self.nslide()
        self.play(m.DrawBorderThenFill(region))
        self.play(m.Create(gears[0]), m.Create(gears[1]), m.Create(gears[2]))
        self.nslide()

        #   Select the machine: flash gear and omega, and recolor omega
        flash = m.VGroup(
            gear_sel.copy().set_stroke(color_sel, width=5).set_fill(opacity=0),
            omega.copy().set_stroke(color_sel, width=3).set_fill(opacity=0),
        )
        self.play(
            m.ShowPassingFlashWithThinningStrokeWidth(flash, time_width=0.5),
            omega.animate.set_color(color_sel),
        )
        self.play(
            eq.animate.set_opacity(1),
            number.animate.set_opacity(1),
            m.Write(vec_label),
        )
        self.nslide()

        #   Move the selected machine: the example number follows its position
        sign = m.ValueTracker(1.0)
        number.add_updater(
            lambda d: d.set_value(sign.get_value() * machine_value(gear_sel.get_center()))
        )
        drift = np.array([1.8, 0.0, 0.0])
        self.play(
            gear_sel.animate.shift(drift),
            vec_label.animate.shift(drift),
            run_time=3.0,
            rate_func=m.linear,
        )
        self.nslide()

        #   Swap two vector arguments: the alternating map flips the sign
        self.play(
            m.CyclicReplace(v1, v2),
            m.CyclicReplace(a1, a2),
            run_time=1.5,
        )
        sign.set_value(-1.0)
        self.wait(1/m.config.frame_rate)
        number.clear_updaters()
        self.nslide()


class FormsPreview(FormsSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(FormsSection)
        self.play_forms()
