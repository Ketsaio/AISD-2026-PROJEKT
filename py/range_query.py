import sys

# Dodanie ścieżki do projektu
sys.path.append(r"C:\Users\Filip\Desktop\AISD-2026-PROJEKT")

from typing import List


class SparseTable:
    """
    Struktura danych Sparse Table do zapytań RMQ (Range Maximum Query).

    Umożliwia:
        - preprocess: O(n log n)
        - zapytanie: O(1)
    """

    def __init__(self, arr: List[int]):
        """
        Konstruktor budujący tablicę sparse table.
        arr - wejściowa tablica (np. głośności krasnoludków)
        """

        self.n = len(arr)

        # log[i] = floor(log2(i))
        self.log = [0] * (self.n + 1)

        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1

        # liczba poziomów w tabeli
        k = self.log[self.n] + 1

        # st[k][i] - maksimum na przedziale o długości 2^k zaczynającym się od i
        self.st = [[0] * self.n for _ in range(k)]

        # poziom 0 = pojedyncze elementy
        for i in range(self.n):
            self.st[0][i] = arr[i]

        # budowa tabeli
        j = 1
        while (1 << j) <= self.n:
            i = 0
            while i + (1 << j) <= self.n:
                self.st[j][i] = max(
                    self.st[j - 1][i],
                    self.st[j - 1][i + (1 << (j - 1))]
                )
                i += 1
            j += 1

    def query(self, l: int, r: int) -> int:
        """
        Zwraca maksimum na przedziale [l, r] w czasie O(1).
        """

        j = self.log[r - l + 1]

        return max(
            self.st[j][l],
            self.st[j][r - (1 << j) + 1]
        )