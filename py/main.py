from time import time
from collections import Counter
import random
import models
import pygame
import math
from datetime import datetime

from geometry import graham_scan, perimeter
from range_query import SparseTable
from archive import Huffman, KMP

def wizualizacja(krasnale, kopalnie, przydzial, punkty_otoczki):
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    czcionka = pygame.font.Font(None, 20)
    
    KOLOR_CZCIONKI = (0,0,0)

    przydzielenie = {}
    for worker_id, mine_id in przydzial:
        przydzielenie[krasnale[worker_id]] = kopalnie[mine_id]

    print(przydzielenie)

    sciezki = {}
    for krasnal, kopalnia in przydzielenie.items():
        punkty = []

        obecny_x = krasnal.x
        obecny_y = krasnal.y

        while True:

            kierunki = []

            if obecny_x != kopalnia.x:
                kierunki.append("X")

            if obecny_y != kopalnia.y:
                kierunki.append("Y")
 

            if not kierunki:
                break

            kierunek = random.choice(kierunki)

            if kierunek == "X":
                
                znak = 1 if kopalnia.x > obecny_x else -1

                ile_krokow = random.randint(1,4)
                
                for _ in range(ile_krokow):
                    dystans_x = abs(kopalnia.x - obecny_x)

                    if dystans_x == 0:
                        break

                    elif dystans_x <= 4:
                        obecny_x = kopalnia.x
                    
                    else:
                        obecny_x += 4 * znak

                    punkty.append((obecny_x, obecny_y))


            if kierunek == "Y":
                
                znak = 1 if kopalnia.y > obecny_y else -1

                ile_krokow = random.randint(1,4)
                
                for _ in range(ile_krokow):
                    dystans_y = abs(kopalnia.y - obecny_y)

                    if dystans_y == 0:
                        break

                    elif dystans_y <= 4:
                        obecny_y = kopalnia.y
                    
                    else:
                        obecny_y += 4 * znak

                    punkty.append((obecny_x, obecny_y))

        sciezki[krasnal] = punkty

    state = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state += 1

        screen.fill((255,255,255))
        
        if state == 1:
            for krasnal in krasnale:
                if krasnal in sciezki:
                    punkty = sciezki[krasnal]
                    if punkty:
                        next_punkt = punkty[0]
                        dx = next_punkt[0] - krasnal.x
                        dy = next_punkt[1] - krasnal.y

                        krasnal.x += dx
                        krasnal.y += dy

                        punkty.pop(0)
        

        for mine in kopalnie:
            x,y = mine.x, mine.y
            tekst = ""

            match mine.getSurowiec():
                case models.Surowiec.ZLOTO: 
                    tekst = "Złoto"
                case models.Surowiec.WEGIEL:
                    tekst = "Węgiel"
                case models.Surowiec.MIEDZ:
                    tekst = "Miedź"
                case models.Surowiec.URAN:
                    tekst = "Uran"

            napis = czcionka.render(tekst, True, KOLOR_CZCIONKI)

            pole_napisu = napis.get_rect()
            pole_napisu.centerx = x + 5
            pole_napisu.bottom = y - 5

            pygame.draw.rect(screen, (0, 255, 0), (x, y, 10, 10))
            screen.blit(napis, pole_napisu)

        for krasnal, punkty in sciezki.items():
            for p in punkty:
                pygame.draw.rect(screen, (150,150,150), (p[0], p[1], 4 ,4))


        for worker in krasnale:
            x,y = worker.x, worker.y

            tekst = ""

            match worker.getSurowiec():
                case models.Surowiec.ZLOTO: 
                    tekst = "Z"
                case models.Surowiec.WEGIEL:
                    tekst = "W"
                case models.Surowiec.MIEDZ:
                    tekst = "M"
                case models.Surowiec.URAN:
                    tekst = "U"            

            napis = czcionka.render(tekst, True, KOLOR_CZCIONKI)

            pygame.draw.rect(screen, (255, 0, 0), (x, y, 10, 10))
            screen.blit(napis, (x, y-20))

    
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    
def generuj_raport_dzienny(liczba_krasnali, liczba_kopalni, przydzial, dystans_patrolu, punkty_otoczki, liczba_straznikow, liczba_atakow):
    data_utworzenia = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linie = [
        f"RAPORT Z DNIA {data_utworzenia} \n",
        "I. Krasnoludki i kopalnie:",
        f"    - Pracujące krasnoludki: {liczba_krasnali}",
        f"    - Aktywne kopalnie: {liczba_kopalni}\n",
        "Przykładowe przydziały:"
    ]

    for krasnal, kopalnia in przydzial[:5]:
        linie.append(f"  -> Krasnoludek (ID: {krasnal}) skierowany do kopalni (ID: {kopalnia})")

    linie.extend([
        "\nII. Bezpieczeństwo królestwa:",
        f"    - Długość trasy księcia: {dystans_patrolu:.2f} metrów",
        f"    - Obejmuje {len(punkty_otoczki)} punktów\n",
        "III. Obrona granic:",
        f"    - Granic chronią {liczba_straznikow} strazników",
        f"    - Liczba ataków na królestwo: {liczba_atakow}\n"
    ])

    return "\n".join(linie)


def main():
    print("--- ETAP 1: Przydział pracy ---")
    liczba_krasnali = 10
    miejsce_w_kopalniach = 5

    krasnale = []
    kopalnie = []

    start = time()

    mozliwe_surowce = [models.Surowiec.ZLOTO, models.Surowiec.WEGIEL, models.Surowiec.MIEDZ, models.Surowiec.URAN]

    ile_pracowników = Counter()
    for _ in range(liczba_krasnali):
        surowiec = random.choice(mozliwe_surowce)
        ile_pracowników[surowiec] += 1

        x = random.uniform(350, 930)
        y = random.uniform(250, 470)

        krasnale.append(models.Krasnoludek(x, y, surowiec))

    for surowiec in mozliwe_surowce:
        liczba_gornikow = ile_pracowników[surowiec]
        liczba_kopalni = math.ceil(liczba_gornikow / miejsce_w_kopalniach)

        for _ in range(liczba_kopalni):
            match surowiec:
                case models.Surowiec.ZLOTO:
                    x = random.uniform(50, 300)
                    y = random.uniform(50, 200)
                case models.Surowiec.WEGIEL:
                    x = random.uniform(980, 1230)
                    y = random.uniform(50, 200)
                case models.Surowiec.MIEDZ:
                    x = random.uniform(50, 300)
                    y = random.uniform(520, 670)
                case models.Surowiec.URAN:
                    x = random.uniform(980, 1230)
                    y = random.uniform(520, 670)

            kopalnie.append(models.Kopalnia(x, y, surowiec, miejsce_w_kopalniach))

    przydzial = models.mcmf(krasnale, kopalnie)
    
    print(time() - start)

    print(f"Przydzielono {len(przydzial)} krasnoludków do pracy.")
    for krasnal, kopalnia in przydzial[:5]:
        print(f"  Krasnoludek #{krasnal} -> Kopalnia #{kopalnia}")
    if len(przydzial) > 5:
        print("  ...")

    print("\n--- ETAP 2: Wyznaczanie trasy patrolu ---")
    uzyte_indeksy = set(kopalnia for _, kopalnia in przydzial)
    uzyte_kopalnie = [kopalnie[i] for i in uzyte_indeksy]

    print(f"Liczba używanych kopalni (wierzchołków do otoczenia): {len(uzyte_kopalnie)}")
    
    punkty_otoczki = graham_scan(uzyte_kopalnie)
    dystans_patrolu = perimeter(punkty_otoczki)
    
    print(f"Liczba wierzchołków otoczki wypukłej: {len(punkty_otoczki)}")
    print(f"Codzienny dystans patrolu księcia: {dystans_patrolu:.2f} metrów")

    print("\n--- ETAP 3: Dekametrowcy i rozkazy (RMQ) ---")

    liczba_straznikow = max(2, int(dystans_patrolu // 10))
    print(f"Na trasie patrolu rozstawiono {liczba_straznikow} dekametrowców (co 10 metrów).")

    glosnosc_straznikow = [random.randint(10, 150) for _ in range(1000)]
    
    st = SparseTable(glosnosc_straznikow)

    liczba_atakow = 5
    print(f"Symulacja {liczba_atakow} nagłych ataków na granice:")

    for i in range(1, liczba_atakow + 1):
        poczatek_ataku = random.randint(0, liczba_straznikow - 2)
        koniec_ataku = random.randint(poczatek_ataku + 1, liczba_straznikow - 1)
        
        najglosniejszy = st.query(poczatek_ataku, koniec_ataku)
        
        print(f"  [Atak #{i}] Odcinek {poczatek_ataku}-{koniec_ataku}: Rozkaz do salwy wydaje krasnoludek o głośności {najglosniejszy}")
    
    print(f"Atak jabłkami na odcinek od {poczatek_ataku} do {koniec_ataku}!")
    print(f"Najgłośniejszy krasnoludek wyda rozkaz z głośnością: {najglosniejszy}")


    print("\n--- ETAP 4: Archiwizacja wiedzy ---")

    raport = generuj_raport_dzienny(liczba_krasnali, liczba_kopalni, przydzial, dystans_patrolu, punkty_otoczki, liczba_straznikow, liczba_atakow)

    huffman = Huffman(raport)
    skompresowany = huffman.kompresuj()
    
    print(f"Oryginalny tekst (długość {len(raport)} znaków): '{raport}'")
    print(f"Skompresowany tekst bitowy (długość {len(skompresowany)} bitów): {skompresowany[:50]}...")

    with open("zadanie_out.txt", "w", encoding="UTF-8") as plik:
        plik.write(skompresowany)
    
    assert huffman.dekompresuj() == raport
    print("Dekompresja przebiegła pomyślnie i bezstratnie.")

    wzorzec = "nie"
    wyniki_kmp = KMP.algorytm_KMP(raport, wzorzec)
    print(f"Wyszukiwanie wzorca KMP dla słowa '{wzorzec}': Znaleziono na indeksach {wyniki_kmp}")

    print(przydzial)

    wizualizacja(krasnale, kopalnie, przydzial, punkty_otoczki)


if __name__ == "__main__":
    main()