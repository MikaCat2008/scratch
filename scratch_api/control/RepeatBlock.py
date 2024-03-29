from ..abstractions import Blocks, Number
from ..block import StructureBlock
from ..block_iterator import BlockIterator


@StructureBlock
class RepeatBlock(BlockIterator):
    index: int
    end: Number
    blocks: Blocks

    def __init__(self, end: Number, blocks: Blocks) -> None:
        super().__init__()

        self.index = 0
        self.end = end
        self.blocks = blocks

    def execute(self) -> bool:
        if len(self.blocks) == 0 or int(self.end) == 1:
            return True

        self.index += 1

        if self.index >= int(self.end):
            self.index = 0
            
            return True

        return False

    def iter(self) -> None:
        if int(self.end) == 0:
            return []
        return self.blocks

    def stop(self) -> None:
        super().stop()

        self.index = 0
        
        for block in self.blocks:
            block.stop()
