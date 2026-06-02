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
        # ZMIANA: przechowujemy teraz tuple (wartosc, indeks)
        self.st = [[(0, 0)] * self.n for _ in range(k)]

        # poziom 0 = pojedyncze elementy
        # ZMIANA: inicjalizacja krotką
        for i in range(self.n):
            self.st[0][i] = (arr[i], i)

        # budowa tabeli
        j = 1
        while (1 << j) <= self.n:
            i = 0
            while i + (1 << j) <= self.n:
                # ZMIANA: porównanie krotek po wartościach
                val1 = self.st[j - 1][i]
                val2 = self.st[j - 1][i + (1 << (j - 1))]
                self.st[j][i] = val1 if val1[0] >= val2[0] else val2
                i += 1
            j += 1

    def query(self, l: int, r: int):
        """
        Zwraca maksimum na przedziale [l, r] w czasie O(1).
        ZMIANA: teraz zwraca krotkę (wartość, indeks)
        """

        j = self.log[r - l + 1]

        left = self.st[j][l]
        right = self.st[j][r - (1 << j) + 1]
        
        return left if left[0] >= right[0] else right