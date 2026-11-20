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
from section_exterior_derivative2 import ExteriorDerivative2Section
from section_gen_stokes import GenStokesSection
from section_gen_stokes2 import GenStokes2Section
from section_poincare import PoincareSection
from section_cartan import (
    CartanSetupSection,
    CartanFirstSection,
    CartanSecondSection,
)


class Presentation(
    TitleSection,
    ContentsSection,
    FormsSection,
    FormsVisSection,
    FormsVis2Section,
    WedgeSection,
    ExteriorDerivativeSection,
    ExteriorDerivative2Section,
    GenStokesSection,
    GenStokes2Section,
    PoincareSection,
    CartanSetupSection,
    CartanFirstSection,
    CartanSecondSection,
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
        self.start_section(ExteriorDerivative2Section)
        self.play_ext_deriv2()
        self.start_section(GenStokesSection)
        self.play_gen_stokes()
        self.start_section(GenStokes2Section)
        self.play_gen_stokes2()
        self.start_section(PoincareSection)
        self.play_poincare()
        self.start_section(CartanSetupSection)
        self.play_cartan_setup()
        self.start_section(CartanFirstSection)
        self.play_cartan_first()
        self.start_section(CartanSecondSection)
        self.play_cartan_second()
