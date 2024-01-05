import math

from ..abstractions import Number, String
from ..nodes.NumberNode import NumberNode


class MathFuncOfNode(NumberNode):
    func: String
    number: Number
    
    def __init__(self, func: String, number: Number) -> None:
        super().__init__()

        self.func = func
        self.number = number

    def get_value(self) -> float:
        if str(self.func) == "sin":
            return math.sin(float(self.number))
        elif str(self.func) == "cos":
            return math.cos(float(self.number))