from typing import Tuple

class RGB:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other):
        return self.r == other.r and self.g == self.g and self.b == other.b

    def __add__(self, other):
        return RGB(min(255, self.r + other.r),
                   min(255, self.g + other.g),
                   min(255, self.b + other.b))

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __sub__(self, other):
        return RGB(self.r - other.r,
                   self.g - other.g,
                   self.b - other.b)

    @property
    def tuple(self) -> Tuple:
        return (self.r, self.g, self.b)