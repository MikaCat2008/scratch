from .. import sprite as sprite_module
from ..abstractions import NodeType, BlockType, SpriteType, Blocks
from ..emit import emit
from ..block import Block
from ..memory import memory
from ..sprite_manager import SpriteManager
from ..block_container import BlockContainer

from ..objects import *

sprite_module.STRUCTURE_BLOCK_DELAY = 0
sprite_manager = SpriteManager()


class TestELActivateBlock(Block):
    is_activate: bool

    def __init__(self) -> None:
        super().__init__()

        self.is_activate = False

    def execute(self) -> bool:
        self.is_activate = True

        return True


def sprite(
    *blocks: list[Blocks],
    x: float = 0.0,
    y: float = 0.0,
    direction: float = 0.0,
    name: str = None,
    variables: dict[str, object] = None
) -> SpriteType:
    variables = variables or {}
    blocks = blocks or []

    new_sprite = sprite_manager.create_sprite(
        blocks = [BlockContainer(_blocks) for _blocks in blocks],
        variable_names = list(variables),
        name = name,
        coords = (x, y),
        direction = direction
    )

    for name, value in variables.items():
        if isinstance(value, NodeType):
            node = value
        elif isinstance(value, int):
            node = NumberNode(value)
        elif isinstance(value, str):
            node = StringNode(value)
        elif isinstance(value, bool):
            node = BooleanNode(value)

        new_sprite.set_value(name, node)

    memory.sprites.append(new_sprite)

    return new_sprite


def test_listener_block(
    listener_block: BlockType,
    event: str,
    blocks: Blocks = None,
    args: tuple = (),
    test_data: dict[str, object] = None
) -> bool:
    blocks = blocks or []
    test_data = test_data or {}
    test_el_activate_block = TestELActivateBlock()
    blocks = [test_el_activate_block] + blocks
    
    test_sprite = sprite_manager.create_sprite(
        blocks = [
            listener_block(*args, blocks)
        ]
    )

    memory.sprites.append(test_sprite)
    
    emit(event, **test_data)
    update()

    return test_el_activate_block.is_activate


def update() -> None:
    emit("update")

    ok = False

    while not ok:
        ok = True

        for sprite in memory.sprites:
            if sprite.update():
                ok = False

    memory.sprites = []
