import random
import sys
from main import main


ILE_TESTOW = 40

with open("czasowe.txt", "w", encoding="utf-8") as plik:
    for i in range(ILE_TESTOW):
        liczba_krasnali = random.randint(100, 1000)
        miejsce_w_kopalni = random.randint(10, 100)
        liczba_atakow = random.randint(1, 30)

        czas = main(
            liczba_krasnali,
            miejsce_w_kopalni,
            liczba_atakow,
            False,
            False
        )

        plik.write(
            f"{liczba_krasnali};{miejsce_w_kopalni};{liczba_atakow};{czas:.6f}\n"
        )

        print(f"Test {i + 1}: {czas}")