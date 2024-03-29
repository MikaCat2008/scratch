from pygame import SRCALPHA
from pygame.draw import rect
from pygame.surface import Surface, SurfaceType

from ..template_element import TemplateElement


class BlocksBottomTemplateElement(TemplateElement):
    def render(self, sy: int = 0) -> SurfaceType:
        surface = Surface((self.template.width, 20), SRCALPHA, 32)

        rect(surface, self.template.color, (0, 0, self.template.width, 20))

        return surface
