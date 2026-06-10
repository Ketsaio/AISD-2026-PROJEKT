import random
from main import main
from openpyxl import Workbook, load_workbook # pyright: ignore[reportMissingModuleSource]
from openpyxl.styles import Font # pyright: ignore[reportMissingModuleSource]
from pathlib import Path


ILE_TESTOW = 40
NAZWA_PLIKU = "czasowe.xlsx"


def test(krasnale, miejsce, ataki):
    wyniki = []

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

        wyniki.append((
            i + 1,
            liczba_krasnali,
            miejsce_w_kopalni,
            liczba_atakow,
            czas
        ))

        print(f"Test {i + 1}: {czas:.6f}")

    sredni_czas = sum(wynik[4] for wynik in wyniki) / len(wyniki)

    if(Path(NAZWA_PLIKU).exists()):
        workbook = load_workbook(NAZWA_PLIKU)
        arkusz = workbook.active
    
    else:
        workbook = Workbook()
        arkusz = workbook.active
        arkusz.title = "Wyniki"


    arkusz.append([
        "Nr testu",
        "Liczba krasnali",
        "Miejsca w kopalni",
        "Liczba ataków",
        "Czas [s]"
    ])


    for nr_testu, liczba_krasnali, miejsce_w_kopalni, liczba_atakow, czas in wyniki:
        arkusz.append([
            nr_testu,
            liczba_krasnali,
            miejsce_w_kopalni,
            liczba_atakow,
            f"{czas:.9f}"
        ])

    arkusz.append([])
    arkusz.append(["Średni czas", f"{sredni_czas:.9f}"])

    arkusz.append([""])

    workbook.save("czasowe.xlsx")

    print(f"Średni czas: {sredni_czas:.6f}")


if __name__ == "__main__":
    krasnale = tuple(map(int, input("Podaj zakres krasnali\n> ").split()))
    miejsce = tuple(map(int, input("Podaj zakres miejsca\n> ").split()))
    ataki = tuple(map(int, input("Podaj zakres ataków\n> ").split()))

    if len(krasnale) == 1:
        krasnale = (*krasnale, *krasnale)

    if len(miejsce) == 1:
        miejsce = (*miejsce, *miejsce)

    if len(ataki) == 1:
        ataki = (*ataki, *ataki)

    test(krasnale, miejsce, ataki)