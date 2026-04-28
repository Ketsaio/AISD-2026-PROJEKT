from enum import Enum
from math import sqrt
from typing import List


class Surowiec(Enum):
    ZLOTO = 0
    WEGIEL = 1
    MIEDZ = 2
    URAN = 3


class Punkt:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def dystans(self, other: "Punkt") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Kopalnia:
    def __init__(self, x: float, y: float, s: Surowiec, c: int) -> None:
        self.punkt = Punkt(x, y)
        self.surowiec = s
        self.capacity = c

    @property
    def x(self) -> float:
        return self.punkt.x

    @property
    def y(self) -> float:
        return self.punkt.y

    def dystans(self, other: Punkt) -> float:
        return self.punkt.dystans(other)


class Krasnoludek:
    def __init__(self, x: float, y: float, s: Surowiec) -> None:
        self.punkt = Punkt(x, y)
        self.surowiec = s

    @property
    def x(self) -> float:
        return self.punkt.x

    @property
    def y(self) -> float:
        return self.punkt.y

    def dystans(self, other: Punkt) -> float:
        return self.punkt.dystans(other)