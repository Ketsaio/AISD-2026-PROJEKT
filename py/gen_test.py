import random
import sys
from main import main


ILE_TESTOW = 40

def test(krasnale, miejsce, ataki):

    with open("czasowe.txt", "w", encoding="utf-8") as plik:
        for i in range(ILE_TESTOW):
            liczba_krasnali = random.randint(*krasnale)
            miejsce_w_kopalni = random.randint(*miejsce)
            liczba_atakow = random.randint(*ataki)

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

if __name__ == "__main__":

    krasnale = tuple(map(int, input("Podaj zakres krasnali\n> ").split()))
    miejsce = tuple(map(int, input("Podaj zakres miejsca\n> ").split()))
    ataki = tuple(map(int, input("Podaj zakres ataków\n> ").split()))

    test(krasnale, miejsce, ataki)