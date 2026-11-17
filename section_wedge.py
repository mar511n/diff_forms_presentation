"""Wedge product section."""

from typing import TYPE_CHECKING

from deck import DeckScene

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class WedgeSection(_SectionBase):
    PAGE = 5
    TITLE = r"Wedge product"
    
    def play_wedge(self):
        self.nslide()


class WedgePreview(WedgeSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(WedgeSection)
        self.play_wedge()
