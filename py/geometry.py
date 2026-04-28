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
    """
    Implementacja algorytmu Grahama (otoczka wypukła).

    Wejście:
        mines - lista kopalń

    Wyjście:
        lista punktów tworzących otoczkę wypukłą (hull)
    """

    # Konwersja kopalń na punkty geometryczne
    points = [Punkt(m.x, m.y) for m in mines]

    # Jeśli mamy 0-1 punktów, zwracamy od razu
    if len(points) <= 1:
        return points

    # Punkt startowy - najniższy (y), a potem najmniejszy x
    start = min(points, key=lambda p: (p.y, p.x))

    # Funkcja pomocnicza do sortowania kątowego
    def polar(p: Punkt):
        return (p.y - start.y, p.x - start.x)

    # Sortowanie punktów względem kąta polarnego
    points.sort(key=lambda p: polar(p))

    hull = []  # stos przechowujący otoczkę

    # Budowanie otoczki wypukłej
    for p in points:
        # Usuwamy punkty, które psują wypukłość (skręt w prawo)
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