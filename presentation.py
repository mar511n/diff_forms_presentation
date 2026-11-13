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
# Defaults for all typeset text (Text, Tex, MathTex, ...)
m.Typst.set_default(font_size=CONTENT_FONT_SIZE, fill_color=FRONTCOL)
# Numbers manage their own font size and glyph colors
m.DecimalNumber.set_default(font_size=CONTENT_FONT_SIZE, fill_color=FRONTCOL)

PresentationTitle = r'\textbf{A physical mapping between metric}\\ \textbf{and torsionful geometry in 2D}'
PresentationTitleShort = 'Torsionful geometry mapping in 2D'
PresentationInfo = r"""
{
Marvin Henke - 24.11.2026 \\
Supervisor: Dr. Nikodem Szpak \\
Group seminar AG König \\
}
"""
PresentationContactInfo = 'marvin.henke@stud.uni-due.de'

class Presentation(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(
            phi=65 * m.DEGREES, theta=-50 * m.DEGREES, zoom=0.6
        )
        self.canvas_objs = []

        # Titlepage (0)
        background_render = m.ImageMobject('./assets/title_background.png')
        self.camera.add_fixed_in_frame_mobjects(background_render)
        self.bring_to_back(background_render)
        
        
        self.nslide()
        render_height = 0.57
        TextBox = m.Rectangle(height=self.camera.frame_height*(1-render_height), width=self.camera.frame_width)
        TextBox.set_style(fill_color=BACKCOL, fill_opacity=0.8, stroke_width=0)
        TextBox.to_edge(m.DOWN,buff=0)
        self.camera.add_fixed_in_frame_mobjects(TextBox)

        slide_title_long = m.Tex(PresentationTitle, font_size=TITLE_FONT_SIZE, tex_environment="")
        slide_title_long.next_to(TextBox.get_corner(m.UL), m.RIGHT+m.DOWN, m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(slide_title_long)
        self.slide_title = m.Tex(rf'\textbf{{{PresentationTitleShort}}}', font_size=TITLE_FONT_SIZE)
        self.slide_title.to_corner(m.UL)
        self.camera.add_fixed_in_frame_mobjects(self.slide_title)
        self.canvas_objs.append(self.slide_title)

        presentation_info = m.Tex(PresentationInfo, tex_environment="")
        presentation_info.next_to(TextBox.get_corner(m.DL), m.RIGHT+m.UP, m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(presentation_info)

        ude_logo = m.SVGMobject('./assets/logo/logo_claim_rgb.svg' if Theme else './assets/logo/logo_claim_rgb_neg.svg', height=1)
        ude_logo.to_corner(m.UR, buff=0)
        ude_logo.shift(m.DOWN*0.1)
        self.camera.add_fixed_in_frame_mobjects(ude_logo)
        self.canvas_objs.append(ude_logo)

        self.play(m.FadeIn(TextBox), m.Write(slide_title_long), m.Write(ude_logo), m.Write(presentation_info))
        
        
        self.nslide()
        # Layout stuff (1)
        #   Contact info
        contact_info = m.Tex(PresentationContactInfo, font_size=CONTENT_FONT_SIZE*0.6).to_corner(m.DL,buff=m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(contact_info)
        self.canvas_objs.append(contact_info)
        #   Presentation title
        presentation_title = m.Tex(PresentationTitleShort, font_size=CONTENT_FONT_SIZE*0.6).align_to(contact_info, m.UP)
        self.camera.add_fixed_in_frame_mobjects(presentation_title)
        self.canvas_objs.append(presentation_title)
        #   Page number
        self.slide_number_val = 1
        self.slide_number = m.Integer(1, font_size=CONTENT_FONT_SIZE*0.6).to_corner(m.DR,buff=m.MED_SMALL_BUFF)
        self.camera.add_fixed_in_frame_mobjects(self.slide_number)
        self.canvas_objs.append(self.slide_number)
        self.play(m.FadeOut(presentation_info,background_render,TextBox),m.ReplacementTransform(slide_title_long, self.slide_title))
        self.play(m.Write(contact_info), m.Write(presentation_title), m.Write(self.slide_number))
        
        
        self.nslide()
        # Table of Contents (2-6)
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
        contents = m.Tex(r"table of contents")
        self.camera.add_fixed_in_frame_mobjects(contents)
        self.play(m.Write(contents))
        
        
        self.nslide()
        self.setup_new_slide("Part 1", cleanup=True)
        update_back_rects()
        self.play(m.Write(m.Tex(r"Something...")))

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
        newT = m.Tex(rf"\textbf{{{title}}}", font_size=TITLE_FONT_SIZE).move_to(self.slide_title, m.UP).align_to(self.slide_title, m.LEFT)
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