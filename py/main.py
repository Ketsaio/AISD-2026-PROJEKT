import random
import models
from time import time

from geometry import graham_scan, perimeter
from range_query import SparseTable
from archive import Huffman, KMP

def main():

    print("--- ETAP 1: Przydział pracy ---")
    num_workers = 50
    num_mines = 10
    mine_capacity = 5

    workers = []
    mines = []

    start = time()

    mozliwe_surowce = []

    for _ in range(num_workers):
        surowiec = random.choice([models.Surowiec.ZLOTO, models.Surowiec.WEGIEL, models.Surowiec.MIEDZ, models.Surowiec.URAN])

        if surowiec not in mozliwe_surowce:
            mozliwe_surowce.append(surowiec)

        workers.append(models.Krasnoludek(random.uniform(0, 100), random.uniform(0, 100), surowiec))

    for _ in range(num_mines):
        surowiec = random.choice(mozliwe_surowce)
        mines.append(models.Kopalnia(random.uniform(0, 100), random.uniform(0, 100), surowiec, mine_capacity))

    assignments = models.mcmf(workers, mines)
    
    print(time() - start)

    print(f"Przydzielono {len(assignments)} krasnoludków do pracy.")
    for dwarf_idx, mine_idx in assignments[:5]:
        print(f"  Krasnoludek #{dwarf_idx} -> Kopalnia #{mine_idx}")
    if len(assignments) > 5:
        print("  ...")

    print("\n--- ETAP 2: Wyznaczanie trasy patrolu ---")
    used_mine_indices = set(mine_idx for _, mine_idx in assignments)
    used_mines = [mines[i] for i in used_mine_indices]

    print(f"Liczba używanych kopalni (wierzchołków do otoczenia): {len(used_mines)}")
    
    hull_points = graham_scan(used_mines)
    patrol_dist = perimeter(hull_points)
    
    print(f"Liczba wierzchołków otoczki wypukłej: {len(hull_points)}")
    print(f"Codzienny dystans patrolu księcia: {patrol_dist:.2f} metrów")

    print("\n--- ETAP 3: Dekametrowcy i rozkazy (RMQ) ---")
    guards_volumes = [random.randint(10, 150) for _ in range(1000)]
    
    st = SparseTable(guards_volumes)

    atak_start = 150
    atak_end = 250
    loudest_volume = st.query(atak_start, atak_end)
    
    print(f"Atak jabłkami na odcinek od {atak_start} do {atak_end}!")
    print(f"Najgłośniejszy krasnoludek wyda rozkaz z głośnością: {loudest_volume}")


    print("\n--- ETAP 4: Archiwizacja wiedzy ---")
    
    tekst_wiedzy = ""

    with open("zadanie_out.txt", "w") as plik:
        pass

    with open("zadanie.txt", "r", encoding="UTF-8") as plik:
        tekst_wiedzy = plik.read()

    huffman = Huffman(tekst_wiedzy)
    skompresowany = huffman.kompresuj()
    
    # print(f"Oryginalny tekst (długość {len(tekst_wiedzy)} znaków): '{tekst_wiedzy}'")
    print(f"Skompresowany tekst bitowy (długość {len(skompresowany)} bitów): {skompresowany[:50]}...")

    print(huffman.dekompresuj(skompresowany))

    with open("zadanie_out.txt", "w", encoding="UTF-8") as plik:
        plik.write(skompresowany)
    
    assert huffman.dekompresuj() == tekst_wiedzy
    print("Dekompresja przebiegła pomyślnie i bezstratnie.")

    wzorzec = "nie"
    wyniki_kmp = KMP.algorytm_KMP(tekst_wiedzy, wzorzec)
    print(f"Wyszukiwanie wzorca KMP dla słowa '{wzorzec}': Znaleziono na indeksach {wyniki_kmp}")


if __name__ == "__main__":
    main()