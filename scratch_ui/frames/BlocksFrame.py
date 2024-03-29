import pygame
from pygame import mouse
from pygame.event import EventType
from pygame.surface import SurfaceType

from ..abstractions import BlockType, GameBlockType, GameObjectType, SpawnerType
from ..frame import Frame
from ..node_spawner import NodeSpawner
from ..block_spawner import BlockSpawner
from ..select_manager import select_manager
from ..sprite_manager import sprite_manager

from scratch_api.objects import *


def get_spawners(
    *game_object_groups: tuple[tuple[tuple[GameObjectType], ...], tuple[int, int]]
) -> list[BlockType]:
    spawners = [None] * sum(map(len, game_object_groups))
    
    i, y = 0, 10
    for game_blocks in game_object_groups:
        for game_object in game_blocks:
            if isinstance(game_object, GameBlockType):
                spawner = BlockSpawner(
                    (10, y),
                    game_object
                )
            else:
                spawner = NodeSpawner(
                    (10, y),
                    game_object
                )

            spawners[i] = spawner
            
            i += 1
            y += 5 + spawner.render().get_height()
        y += 20
    
    return spawners


def update_spawners(spawners: list[SpawnerType], mx: int, my: int) -> None:
    m0 = mouse.get_pressed()[0]

    for spawner in spawners:
        x, y = spawner.coords
        w, h = spawner.render().get_size()
        
        if x <= mx <= x + w and y <= my <= y + h:
            if m0 and not select_manager.selected_object:
                select_manager.select(spawner.spawn(sprite_manager.selected_sprite))
                select_manager.free()

            break


def draw_spawners(screen: SurfaceType, scroll: int) -> None:
    for spawner in spawners:
        bx, by = spawner.coords

        screen.blit(spawner.render(), (bx, by - scroll))


spawners = None


class BlocksFrame(Frame):
    def start(self) -> None:
        global spawners

        self.scroll = 0

        spawners = get_spawners(
            (
                MoveBlock(NumberNode(10)),
                TurnRightBlock(NumberNode(15)),
                TurnLeftBlock(NumberNode(15)),
            ),
            (
                PointInDirectionBlock(NumberNode(90)),
                PointTowardsBlock(StringNode("mouse-pointer"), BooleanNode(True))
            ),
            (
                GoToXYBlock(NumberNode(0), NumberNode(0)),
                GoToBlock(StringNode("mouse-pointer"), BooleanNode(True)),
                GlideToBlock(NumberNode(1), NumberNode(0), NumberNode(0))
            ),
            (
                ChangeXByBlock(NumberNode(10)),
                SetXToBlock(NumberNode(0)),
                ChangeYByBlock(NumberNode(10)),
                SetYToBlock(NumberNode(0))
            ),
            (
                IfOnEdgeBounceBlock(),
            ),
            (
                SetRotationStyleBlock(NumberNode(1)),
            ),
            (
                XPositionNode(),
                YPositionNode(),
                DirectionNode()
            ),
            (
                ShowBlock(),
                HideBlock()
            ),
            (
                ClearBlock(),
            ),
            (
                StampBlock(),
            ),
            (
                PenDownBlock(),
                PenUpBlock()
            ),
            (
                VariableNode(StringNode("variable")),
            ),
            (
                SetValueToBlock(StringNode("variable"), NumberNode(0)),
                ChangeValueByBlock(StringNode("variable"), NumberNode(10)),
            ),
            (
                OnStartBlock([]),
                OnKeyPressBlock(StringNode("space"), [])
            ),
            (
                WaitBlock(NumberNode(1)),
            ),
            (
                RepeatBlock(NumberNode(5), []),
                ForeverBlock([])
            ),
            (
                IfThenBlock(BooleanNode(False), []),
                IfThenElseBlock(BooleanNode(False), [], []),
                WaitUntilBlock(BooleanNode(True)),
                RepeatUntilBlock(BooleanNode(True), [])
            ),
            (
                AddNode(NumberNode(0), NumberNode(0)),
                SubNode(NumberNode(0), NumberNode(0)),
                MulNode(NumberNode(0), NumberNode(0)),
                DivNode(NumberNode(0), NumberNode(0))
            ),
            (
                RandomNumberNode(NumberNode(0), NumberNode(10)),
            ),
            (
                LessThanNode(NumberNode(0), NumberNode(0)),
                EqualsToNode(NumberNode(0), NumberNode(0)),
                BiggerThanNode(NumberNode(0), NumberNode(0)),
            ),
            (
                AndNode(BooleanNode(False), BooleanNode(False)),
                OrNode(BooleanNode(False), BooleanNode(False)),
                NotNode(BooleanNode(False)),
            ),
            (
                MathFuncOfNode(StringNode("sin"), NumberNode(0)),
            )
        )

    def update(self, events: list[EventType], mouse_coords: tuple[int, int]) -> None:
        self.screen.fill((255, 255, 255))

        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.scroll -= event.y * 25

        draw_spawners(self.screen, self.scroll)

        mx, my = mouse_coords

        if mx <= self.screen.get_width():
            update_spawners(spawners, mx, my + self.scroll)
