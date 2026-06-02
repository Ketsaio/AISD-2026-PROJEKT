import sys
import math

sys.path.append(r"C:\Users\Filip\Desktop\AISD-2026-PROJEKT")

from typing import List
from models2 import Punkt, Kopalnia


def orientation(a: Punkt, b: Punkt, c: Punkt) -> float:
    """
    Sprawdza orientację trzech punktów
    przy użyciu iloczynu wektorowego.

    > 0  - skręt w lewo
    < 0  - skręt w prawo
    = 0  - punkty współliniowe
    """

    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def graham_scan(mines: List[Kopalnia]) -> List[Punkt]:
    """
    Implementacja algorytmu Graham Scan.

    Algorytm wyznacza otoczkę wypukłą
    dla zbioru punktów w czasie O(N log N).
    """

    # Zamiana kopalń na punkty
    points = [Punkt(m.x, m.y) for m in mines]

    if len(points) <= 1:
        return points

    # Punkt startowy
    start = min(points, key=lambda p: (p.y, p.x))

    # Kąt względem punktu startowego
    def polar_angle(p: Punkt):
        return math.atan2(p.y - start.y, p.x - start.x)

    # Pomocnicze sortowanie przy równych kątach
    def distance(p: Punkt):
        return (p.x - start.x)**2 + (p.y - start.y)**2

    # Sortowanie punktów według kąta
    points.sort(key=lambda p: (polar_angle(p), distance(p)))

    # Stos przechowujący otoczkę
    hull = []

    for p in points:

        # Usuwanie punktów psujących wypukłość
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) <= 0:
            hull.pop()

        hull.append(p)

    return hull


def perimeter(hull: List[Punkt]) -> float:
    """
    Oblicza obwód otoczki wypukłej.

    Sumuje odległości pomiędzy
    kolejnymi punktami wielokąta.
    """

    if len(hull) < 2:
        return 0.0

    # Odległość euklidesowa
    def dist(a: Punkt, b: Punkt):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    total = 0.0

    # Sumowanie długości boków
    for i in range(len(hull)):
        total += dist(hull[i], hull[(i + 1) % len(hull)])

    return total