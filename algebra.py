import math
import numpy as np
import typing
from typing import Literal, Sequence, Optional, Union
import numpy.typing as npt
from decimal import Decimal
from fractions import Fraction


_legalNumType = [Decimal, Fraction, float, int]
LegalNumType = Union[Decimal, Fraction, float, int]

class Multi3D:
    i = np.array([1, 0, 0])
    j = np.array([0, 1, 0])
    k = np.array([0, 0, 1])

    @staticmethod
    def cross(v1: Sequence, v2: Sequence) -> np.ndarray:
        return np.array([
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ])

    @staticmethod
    def dot(v1: Sequence, v2: Sequence) -> float:
        assert len(v1) == len(v2)
        return sum(_a * _b for _a, _b in zip(v1, v2))

    @ staticmethod
    def execute():
        print(
            ""
        )

    @staticmethod
    def vector(*args: list, dim=3, arr: Optional[npt.ArrayLike] = None) -> np.ndarray:
        if arr is not None:
            return np.array(arr)
        if len(args) > 0:
            return np.array(args)
        return np.array([0] * dim)
    

class BaseMathExpression:
    _content: Union[str, LegalNumType]
    _mode: type[LegalNumType]
    _special_constant_mode: bool = False
    isNum: bool
    val: LegalNumType

    def __init__(
        self, 
        content: Union[str, LegalNumType], 
        mode: type[LegalNumType] = float,
        special_constant_mode = False
    ) -> None:
        self._content = content
        self._mode = mode
        self._special_constant_mode = special_constant_mode

    def __float__(self) -> float:
        if self._special_constant_mode:
            if self._content.lower() == "e":
                return math.e
            elif self._content.lower() == "pi":
                return math.pi
            else:
                raise ValueError("Unsupported Special Index")
        try: 
            return float(self._content)
        except ValueError:
            return 0

    def __str__(self) -> str:
        return str(float(self))

    @property
    def val(self) -> LegalNumType:
        if self._special_constant_mode:
            return float(self)
        if self._mode is float:
            return float(self)
        elif self._mode in _legalNumType:
            return self._content
        return 0.

    @property
    def isNum(self) -> bool:
        if self._special_constant_mode:
            return True
        try: 
            float(self._content)
        except ValueError:
            return False
        return True

    def __add__(self, other: "BaseMathExpression"):
        if self.isNum:
            if other.isNum:
                new_content = self.val + other.val
                return BaseMathExpression(new_content, type(new_content), False)

cross = Multi3D.cross
dot = Multi3D.dot
i = Multi3D.i
j = Multi3D.j
k = Multi3D.k
vector = vec = Multi3D.vector

test = True
if __name__ == "__main__" and test:
    a = BaseMathExpression("e", float, True)
    print(a._content)
    print(a.isNum)
    print(a.val)
    print(Multi3D.dot([1,2,3], [4,5,6]))




a = vector(-2, 3, 4)
b = vector(4, 5, -2)
c = vector(2, 0, 1)
print(
    cross(cross(a, b), c) - cross(a, cross(b, c))
)
