from pygame.surface import SurfaceType

from .abstractions import Blocks, SpriteType

from .sprite import Sprite


class SpriteManager:
    def create_sprite(
        self, 
        blocks: Blocks,
        variable_names: list[str],
        name: str,
        coords: tuple[float, float],
        direction: float,
        surface: SurfaceType,
        rotate_style: int
    ) -> SpriteType:        
        sprite = Sprite(blocks, variable_names, name, coords, direction, surface, rotate_style)

        for block in blocks:
            block.set_sprite(sprite)
            block.set_main(block)
            block.set_parent()

        return sprite