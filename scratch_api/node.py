from .abstractions import NodeType, SpriteType


class Node(NodeType):
    def __init__(self) -> None:
        super().__init__()

        self.nodes = []
        self.block = None
        self.inited = False

        self.parent_node = None
        self.parent_block = None

    def init(self, sprite: SpriteType) -> None:
        self.inited = True
        self.nodes = [node for k, node in self.__dict__.items() if isinstance(node, NodeType) and k != "parent_node"]
        
        for node in self.nodes:
            node.init(sprite)

            node.parent_node = self
        
        self.sprite = sprite

    def replace_node(self, node_a: NodeType, node_b: NodeType) -> None:        
        for k, v in self.__dict__.items():
            if v is node_a:
                setattr(self, k, node_b)

    def reset(self) -> None:
        for node in self.nodes:
            node.reset()
