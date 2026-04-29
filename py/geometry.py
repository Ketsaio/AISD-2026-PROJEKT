import sys

# Dodanie ścieżki do projektu, aby można było importować models2.py
sys.path.append(r"C:\Users\Filip\Desktop\AISD-2026-PROJEKT")

from typing import List
from models2 import Punkt, Kopalnia


def orientation(a: Punkt, b: Punkt, c: Punkt) -> float:
    """
    Oblicza orientację trzech punktów.
    Zwraca:
    > 0 jeśli skręt w lewo
    < 0 jeśli skręt w prawo
    = 0 jeśli punkty są współliniowe
    """
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def graham_scan(mines: List[Kopalnia]) -> List[Punkt]:
    points = [Punkt(m.x, m.y) for m in mines]

    if len(points) <= 1:
        return points

    start = min(points, key=lambda p: (p.y, p.x))

    def polar_angle(p: Punkt):
        return math.atan2(p.y - start.y, p.x - start.x)

    def distance(p: Punkt):
        return (p.x - start.x)**2 + (p.y - start.y)**2

    
    points.sort(key=lambda p: (polar_angle(p), distance(p)))

    hull = []

    for p in points:
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull



def perimeter(hull: List[Punkt]) -> float:
    """
    Oblicza obwód wielokąta (otoczki wypukłej).

    Wejście:
        hull - lista punktów tworzących otoczkę

    Wyjście:
        długość obwodu
    """

    if len(hull) < 2:
        return 0.0

    def dist(a: Punkt, b: Punkt):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    total = 0.0

    # Sumujemy odległości między kolejnymi punktami
    for i in range(len(hull)):
        total += dist(hull[i], hull[(i + 1) % len(hull)])

    return total
