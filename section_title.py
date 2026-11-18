"""Title slide and the transition into the deck layout."""

from typing import TYPE_CHECKING

import manimgx as m

from deck import (
    BACKCOL,
    CONTENT_FONT_SIZE,
    DeckScene,
    PresentationInfo,
    PresentationTitle,
    PresentationTitleShort,
    TITLE_FONT_SIZE,
    typst_preamble,
)

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class TitleSection(_SectionBase):
    PAGE = 0
    TITLE = PresentationTitleShort

    def play_title(self):
        self.begin_deck()
        self.make_hud(1, PresentationTitleShort)

        # Titlepage
        background_render = m.ImageMobject('./assets/title_math_background.png')
        self.camera.add_fixed_in_frame_mobjects(background_render)
        self.bring_to_back(background_render)

        self.wait(1/m.config.frame_rate)
        self.nslide()
        render_height = 0.67
        TextBox = m.Rectangle(
            height=self.camera.frame_height * (1 - render_height),
            width=self.camera.frame_width,
        )
        TextBox.set_style(
            fill_color=BACKCOL, fill_opacity=0.8, stroke_width=0
        )
        TextBox.to_edge(m.DOWN, buff=0)
        self.camera.add_fixed_in_frame_mobjects(TextBox)

        slide_title_long = m.Typst(
            PresentationTitle,
            font_size=TITLE_FONT_SIZE,
            typst_preamble=typst_preamble(TITLE_FONT_SIZE),
        )
        slide_title_long.next_to(
            TextBox.get_corner(m.UL), m.RIGHT + m.DOWN, m.MED_SMALL_BUFF
        )
        self.camera.add_fixed_in_frame_mobjects(slide_title_long)

        presentation_info = m.Typst(
            PresentationInfo,
            typst_preamble=typst_preamble(),
        )
        presentation_info.next_to(
            TextBox.get_corner(m.DL), m.RIGHT + m.UP, m.MED_SMALL_BUFF
        )
        self.camera.add_fixed_in_frame_mobjects(presentation_info)

        self.play(
            m.FadeIn(TextBox),
            m.Write(slide_title_long),
            m.Write(self.ude_logo),
            m.Write(presentation_info),
            background_render.animate.shift(m.UP*m.config.frame_height*0.22)
        )

        self.nslide()
        self.play(
            m.FadeOut(presentation_info, background_render, TextBox),
            m.ReplacementTransform(slide_title_long, self.slide_title),
        )
        self.play(
            m.Write(self.contact_info),
            m.Write(self.presentation_title),
            m.Write(self.slide_number),
        )
        self.update_back_rects()


class TitlePreview(TitleSection, DeckScene):
    def construct(self) -> None:
        self.play_title()
