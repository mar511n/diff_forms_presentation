"""The full talk: the sections composed in order.

Each section lives in its own `section_*.py`, which also defines a preview scene
for rendering just that section. See `deck.py` for the shared setup.
"""

from deck import DeckScene
from section_title import TitleSection
from section_contents import ContentsSection
from section_forms import FormsSection
from section_forms_vis import FormsVisSection
from section_forms_vis2 import FormsVis2Section
from section_wedge import WedgeSection
from section_exterior_derivative import ExteriorDerivativeSection



class Presentation(
    TitleSection,
    ContentsSection,
    FormsSection,
    FormsVisSection,
    FormsVis2Section,
    WedgeSection,
    ExteriorDerivativeSection,
    DeckScene,
):
    def construct(self) -> None:
        self.play_title()
        self.play_contents()
        self.start_section(FormsSection)
        self.play_forms()
        self.start_section(FormsVisSection)
        self.play_formsvis()
        self.start_section(FormsVis2Section)
        self.play_formsvis2()
        self.start_section(WedgeSection)
        self.play_wedge()
        self.start_section(ExteriorDerivativeSection)
        self.play_ext_deriv()
