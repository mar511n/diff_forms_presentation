import numpy as np

import manimgx as m

DARK_MODE: bool = True
LIGHT_MODE: bool = False # experimental
Theme = DARK_MODE
OFFBLACK = m.ManimColor("#121317")
OFFWHITE = m.ManimColor("#F0F8FF")
BACKCOL = OFFBLACK if Theme else OFFWHITE
FRONTCOL = OFFWHITE if Theme else OFFBLACK
TITLE_FONT_SIZE = 52
CONTENT_FONT_SIZE = 0.75 * TITLE_FONT_SIZE
m.config.background_color = BACKCOL

# The largest width a Typst text may use, in scene units. Typst is typeset at
# SCALE_FACTOR_PER_FONT_POINT scene units per point and then scaled by its font size,
# so the page width in points depends on the font size.
MAX_TEXT_WIDTH = m.config.frame_width-2*m.DEFAULT_MOBJECT_TO_EDGE_BUFFER


def typst_preamble(font_size=CONTENT_FONT_SIZE):
    """Typst page setup that wraps text at MAX_TEXT_WIDTH scene units."""
    width_pt = MAX_TEXT_WIDTH / (font_size * m.SCALE_FACTOR_PER_FONT_POINT)
    return (
        f"#set page(width: {width_pt:.3f}pt, height: auto, margin: 0pt, fill: none)"
    )


# Defaults for all typeset text (Text, Typst, ...)
m.Typst.set_default(font_size=CONTENT_FONT_SIZE, fill_color=FRONTCOL)
# Numbers manage their own font size and glyph colors
m.DecimalNumber.set_default(font_size=CONTENT_FONT_SIZE, fill_color=FRONTCOL)

PresentationTitle = r"*Cartan's Differential Calculus on Manifolds*"
PresentationTitleShort = "Cartan's Differential Calculus on Manifolds"
PresentationInfo = r"""Marvin Henke - 24.11.2026 \
Supervisor: Dr. Nikodem Szpak \
Group seminar AG König"""
PresentationContactInfo = r'marvin.henke\@stud.uni-due.de'
PresentationContents = """- differential forms
- wedge product
- generalized Stokes theorem
- Poincaré lemma
"""

class Presentation(m.ThreeDScene):
    def construct(self) -> None:
        #self.set_camera_orientation(
        #    phi=65 * m.DEGREES, theta=-50 * m.DEGREES, zoom=0.6
        #)
        self.canvas_objs = []

        # Titlepage
        background_render = m.ImageMobject('./assets/title_background.png')
        self.camera.add_fixed_in_frame_mobjects(background_render)
        self.bring_to_back(background_render)
        
        
        self.nslide()
        render_height = 0.67
        TextBox = m.Rectangle(height=self.camera.frame_height*(1-render_height), width=self.camera.frame_width)
        TextBox.set_style(fill_color=BACKCOL, fill_opacity=0.8, stroke_width=0)
        TextBox.to_edge(m.DOWN,buff=0)
        self.camera.add_fixed_in_frame_mobjects(TextBox)

        slide_title_long = m.Typst(PresentationTitle, font_size=TITLE_FONT_SIZE, typst_preamble=typst_preamble(TITLE_FONT_SIZE))
        slide_title_long.next_to(TextBox.get_corner(m.UL), m.RIGHT+m.DOWN, m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(slide_title_long)
        self.slide_title = m.Typst(f"*{PresentationTitleShort}*", font_size=TITLE_FONT_SIZE, typst_preamble=typst_preamble(TITLE_FONT_SIZE))
        self.slide_title.to_corner(m.UL)
        self.camera.add_fixed_in_frame_mobjects(self.slide_title)
        self.canvas_objs.append(self.slide_title)

        presentation_info = m.Typst(PresentationInfo, font_size=CONTENT_FONT_SIZE, typst_preamble=typst_preamble(CONTENT_FONT_SIZE))
        presentation_info.next_to(TextBox.get_corner(m.DL), m.RIGHT+m.UP, m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(presentation_info)

        ude_logo = m.SVGMobject('./assets/logo/logo_claim_rgb.svg' if Theme else './assets/logo/logo_claim_rgb_neg.svg', height=1)
        ude_logo.to_corner(m.UR, buff=0)
        ude_logo.shift(m.DOWN*0.1)
        self.camera.add_fixed_in_frame_mobjects(ude_logo)
        self.canvas_objs.append(ude_logo)

        self.play(m.FadeIn(TextBox), m.Write(slide_title_long), m.Write(ude_logo), m.Write(presentation_info))
        
        
        self.nslide()
        # Layout stuff
        #   Contact info
        contact_info = m.Typst(PresentationContactInfo, font_size=CONTENT_FONT_SIZE*0.6, typst_preamble=typst_preamble(CONTENT_FONT_SIZE*0.6)).to_corner(m.DL,buff=m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(contact_info)
        self.canvas_objs.append(contact_info)
        #   Presentation title
        presentation_title = m.Typst(PresentationTitleShort, font_size=CONTENT_FONT_SIZE*0.6, typst_preamble=typst_preamble(CONTENT_FONT_SIZE*0.6)).align_to(contact_info, m.UP)
        self.camera.add_fixed_in_frame_mobjects(presentation_title)
        self.canvas_objs.append(presentation_title)
        #   Page number
        self.slide_number_val = 1
        self.slide_number = m.Integer(1, font_size=CONTENT_FONT_SIZE*0.6).to_corner(m.DR,buff=m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(self.slide_number)
        self.canvas_objs.append(self.slide_number)
        self.play(m.FadeOut(presentation_info,background_render,TextBox),m.ReplacementTransform(slide_title_long, self.slide_title))
        self.play(m.Write(contact_info), m.Write(presentation_title), m.Write(self.slide_number))
        
        
        # Contents
        self.nslide()
        back_rects = []
        back_rects_vmobj = m.VGroup(*back_rects)
        def update_back_rects():
            nonlocal back_rects,back_rects_vmobj
            if len(back_rects) > 0:
                self.canvas_objs.remove(back_rects_vmobj)
                self.remove(back_rects_vmobj)
                back_rects = []
            for i,obj in enumerate([self.slide_title,ude_logo,contact_info,presentation_title,self.slide_number]):
                rect = m.SurroundingRectangle(obj, color=BACKCOL, fill_opacity=0.6, stroke_width=0, z_index=-1)
                self.camera.add_fixed_in_frame_mobjects(rect)
                back_rects.append(rect)
            back_rects_vmobj = m.VGroup(*back_rects)
            self.add(back_rects_vmobj)
            self.canvas_objs.append(back_rects_vmobj)
        update_back_rects()
        contents = self.get_lines(self.slide_title, PresentationContents)
        self.camera.add_fixed_in_frame_mobjects(*contents)
        for point in contents:
            self.play(m.Write(point))
            self.nslide()
        
        
        # Differential forms
        self.setup_new_slide(r"Differential $k$-form $omega in Omega^k (M)$", cleanup=True)
        update_back_rects()
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
            font_size=CONTENT_FONT_SIZE,
            typst_preamble=(
                typst_preamble(CONTENT_FONT_SIZE)
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
            font_size=CONTENT_FONT_SIZE,
            typst_preamble=typst_preamble(CONTENT_FONT_SIZE),
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
        self.play(m.FadeIn(gears[0]), m.FadeIn(gears[1]), m.FadeIn(gears[2]))
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
        self.wait(0.5)
        self.nslide()


        # exterior derivative
        self.setup_new_slide(r"Exterior derivative", cleanup=True)



    def get_lines(self, anchor, points):
        """Place a Typst object below `anchor` and return its lines.

        `points` is Typst code. Each non-empty newline-separated source line becomes
        one group: the function creates a single Typst object and returns an ordered
        list of references to its lines, which can e.g. be used to Write the lines one
        at a time with Write(lines[0]), ...

        A zero-size transparent marker is appended to every non-empty source line. The
        markers are parts of the Typst object in document order, so the object's parts
        can be split at them without measuring positions, and their labels let
        `select` find them. Lines are the source's newline-separated lines (even where
        Typst joins them into one visual line), and lines with no visible parts are
        omitted. Each non-empty line should be complete Typst markup: a construct that
        spans several source lines would receive a marker inside itself.
        """
        if not any(line.strip() for line in points.split("\n")):
            return []

        # A label that the points' own labels cannot collide with.
        marker_label = "_get_lines_break"
        while f"<{marker_label}>" in points:
            marker_label += "_"
        marker = (
            "#box(width: 0pt, height: 0pt, clip: true)"
            f'[#text(fill: rgb("#00000000"), size: 0.1pt)[|]] <{marker_label}>'
        )
        marked = "\n".join(
            line + marker if line.strip() else line for line in points.split("\n")
        )

        text = m.Typst(marked, font_size=CONTENT_FONT_SIZE, typst_preamble=typst_preamble(CONTENT_FONT_SIZE))
        text.next_to(anchor, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        try:
            breaks = {id(part) for part in text.select(marker_label).submobjects}
        except KeyError:  # no marker survived: return the object as one line
            return [text]

        lines = []
        current = m.VGroup()
        for part in text.submobjects:
            if id(part) in breaks:
                if len(current) > 0:
                    lines.append(current)
                    current = m.VGroup()
            else:
                current.add(part)
        if len(current) > 0:
            lines.append(current)

        return lines

    def nslide(self,name="",notes="",loop=False,auto_next=False):
        sect = 'presentation.normal'
        if loop:
            sect = 'presentation.loop'
        if auto_next:
            sect = 'presentation.skip'
        self.next_section(name=name,notes=notes,section_type=sect,skip_animations=False)
        self.wait(2/m.config.frame_rate)
    
    def get_non_canvas_mobjs(self):
        return [mobj for mobj in self.mobjects if mobj not in self.canvas_objs]

    def next_slide_number_animation(self):
        self.slide_number_val += 1
        return self.slide_number.animate(run_time=0.5).set_value(
            self.slide_number_val
        )

    def next_slide_title_animation(self, title):
        newT = m.Typst(f"*{title}*", font_size=TITLE_FONT_SIZE, typst_preamble=typst_preamble(TITLE_FONT_SIZE)).move_to(self.slide_title, m.UP).align_to(self.slide_title, m.LEFT)
        self.camera.add_fixed_in_frame_mobjects(newT)
        return m.Transform(
            self.slide_title,
            newT,
            run_time=0.5,
        )

    def setup_new_slide(self, title, cleanup=False):
        print(f"{self.slide_number_val}:{title}")
        if cleanup:
            ncos = self.get_non_canvas_mobjs()
            self.play(
                self.next_slide_number_animation(),
                self.next_slide_title_animation(title),
                m.FadeOut(*ncos, shift=m.LEFT)
            )
            for nco in ncos:
                del nco
        else:
            self.play(
                self.next_slide_number_animation(),
                self.next_slide_title_animation(title),
            )