from ..abstractions import String, Boolean
from ..memory import memory
from ..motion_block import MotionBlock


class GoToBlock(MotionBlock):
    sprite_name: String
    mouse_pointer: Boolean

    def __init__(self, sprite_name: String, mouse_pointer: Boolean = False) -> None:
        super().__init__()

        self.sprite_name = sprite_name
        self.mouse_pointer = mouse_pointer

    def execute(self) -> bool:
        if bool(self.mouse_pointer):
            self.sprite.coords = memory.mouse_pos
        else:
            sprite = self.get_sprite_by_name(str(self.sprite_name))

            self.sprite.coords = sprite.coords

        return True
