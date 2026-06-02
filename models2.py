from enum import Enum
from math import sqrt
from typing import List


# Enum przechowujący typy surowców
class Surowiec(Enum):
    ZLOTO = 0
    WEGIEL = 1
    MIEDZ = 2
    URAN = 3


# Reprezentacja punktu na płaszczyźnie
class Punkt:

    # Inicjalizacja współrzędnych x i y
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # Obliczanie odległości euklidesowej
    def dystans(self, other: "Punkt") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


# Reprezentacja kopalni
class Kopalnia:

    # x, y - pozycja kopalni
    # s - typ surowca
    # c - liczba dostępnych miejsc
    def __init__(self, x: float, y: float, s: Surowiec, c: int) -> None:
        self.punkt = Punkt(x, y)
        self.surowiec = s
        self.capacity = c

    # Ułatwiony dostęp do współrzędnej x
    @property
    def x(self) -> float:
        return self.punkt.x

    # Ułatwiony dostęp do współrzędnej y
    @property
    def y(self) -> float:
        return self.punkt.y

    # Obliczanie odległości od innego punktu
    def dystans(self, other: Punkt) -> float:
        return self.punkt.dystans(other)


# Reprezentacja krasnoludka
class Krasnoludek:

    # x, y - lokalizacja domku
    # s - preferowany surowiec / umiejętność
    def __init__(self, x: float, y: float, s: Surowiec) -> None:
        self.punkt = Punkt(x, y)
        self.surowiec = s

    # Ułatwiony dostęp do współrzędnej x
    @property
    def x(self) -> float:
        return self.punkt.x

    # Ułatwiony dostęp do współrzędnej y
    @property
    def y(self) -> float:
        return self.punkt.y

    # Obliczanie odległości od innego punktu
    def dystans(self, other: Punkt) -> float:
        return self.punkt.dystans(other)