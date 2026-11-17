"""Exterior derivative section."""

from typing import TYPE_CHECKING

from deck import DeckScene

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class ExteriorDerivativeSection(_SectionBase):
    PAGE = 6
    TITLE = r"Exterior derivative"

    def play_ext_deriv(self):
        self.nslide()


class ExteriorDerivativePreview(ExteriorDerivativeSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(ExteriorDerivativeSection)
        self.play_ext_deriv()
