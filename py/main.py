from time import perf_counter
from collections import Counter
import random
import models
import pygame
import math
import logging
from datetime import datetime

from geometry import graham_scan, perimeter
from range_query import SparseTable
from archive import Huffman, KMP

def wizualizacja(krasnale, kopalnie, przydzial, punkty_otoczki, liczba_atakow, st, raport, skompresowany):
    pygame.init()
    ekran = pygame.display.set_mode((1280, 720))
    zegar = pygame.time.Clock()
    dziala = True
    czcionka = pygame.font.Font(None, 20)
    czcionka_duza = pygame.font.Font(None, 40)
    czcionka_tytul = pygame.font.Font(None, 50)
    
    KOLOR_CZCIONKI = (0, 0, 0)

    przydzielenie = {}
    for id_pracownika, id_kopalni in przydzial:
        przydzielenie[krasnale[id_pracownika]] = kopalnie[id_kopalni]

    sciezki = {}
    for krasnal, kopalnia in przydzielenie.items():
        punkty = []
        obecny_x = krasnal.x
        obecny_y = krasnal.y

        while True:
            kierunki = []
            if obecny_x != kopalnia.x: kierunki.append("X")
            if obecny_y != kopalnia.y: kierunki.append("Y")
 
            if not kierunki:
                break

            kierunek = random.choice(kierunki)

            if kierunek == "X":
                znak = 1 if kopalnia.x > obecny_x else -1
                ile_krokow = random.randint(1, 4)
                for _ in range(ile_krokow):
                    dystans_x = abs(kopalnia.x - obecny_x)
                    if dystans_x == 0: break
                    elif dystans_x <= 4: obecny_x = kopalnia.x
                    else: obecny_x += 4 * znak
                    punkty.append((obecny_x, obecny_y))

            if kierunek == "Y":
                znak = 1 if kopalnia.y > obecny_y else -1
                ile_krokow = random.randint(1, 4)
                for _ in range(ile_krokow):
                    dystans_y = abs(kopalnia.y - obecny_y)
                    if dystans_y == 0: break
                    elif dystans_y <= 4: obecny_y = kopalnia.y
                    else: obecny_y += 4 * znak
                    punkty.append((obecny_x, obecny_y))

        sciezki[krasnal] = punkty

    przesuniete_punkty_otoczki = [(p.x + 5, p.y + 5) for p in punkty_otoczki]
    zamknieta_otoczka = przesuniete_punkty_otoczki + [przesuniete_punkty_otoczki[0]]

    straznicy_na_sciezce = []
    odstep = 10 
    
    for i in range(len(zamknieta_otoczka) - 1):
        p1 = zamknieta_otoczka[i]
        p2 = zamknieta_otoczka[i+1]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        odleglosc = math.hypot(dx, dy)
        
        for d in range(0, int(odleglosc), odstep):
            proporcja = d / odleglosc
            sx = p1[0] + dx * proporcja
            sy = p1[1] + dy * proporcja
            czy_widoczny = True #(d % 30 == 0)
            straznicy_na_sciezce.append({'pozycja': (sx, sy), 'segment': i, 'proporcja': proporcja, 'widoczny': czy_widoczny})

    postep_ksiecia = 0.0

    wygenerowane_ataki = []
    liczba_straznikow = len(straznicy_na_sciezce)
    maksymalna_dlugosc_ataku = max(5, liczba_straznikow // 5) 
    
    for _ in range(liczba_atakow):
        poczatek = random.randint(0, max(0, liczba_straznikow - 2))
        koniec = random.randint(poczatek + 1, min(poczatek + maksymalna_dlugosc_ataku, liczba_straznikow - 1))
        
        wynik = st.query(poczatek, koniec) 
        
        wygenerowane_ataki.append({
            'poczatek': poczatek, 
            'koniec': koniec, 
            'najglosniejsza_wartosc': wynik[0],
            'indeks_najglosniejszego': wynik[1]
        })
        
    stan = 0
    ZIELONY = (0, 200, 0)
    ZLOTY = (255, 215, 0)
    NIEBIESKI = (0, 0, 255)

    STAN_WYKRESU = 3 + liczba_atakow

    while dziala:
        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT:
                dziala = False
            if zdarzenie.type == pygame.KEYDOWN:
                if zdarzenie.key == pygame.K_SPACE:
                    stan += 1
                    if STAN_WYKRESU + 1 == stan:
                        return

        ekran.fill((255, 255, 255))
        
        if stan < STAN_WYKRESU:
            if stan == 1:
                for krasnal in krasnale:
                    if krasnal in sciezki:
                        punkty = sciezki[krasnal]
                        if punkty:
                            nastepny_punkt = punkty[0]
                            krasnal.x += (nastepny_punkt[0] - krasnal.x)
                            krasnal.y += (nastepny_punkt[1] - krasnal.y)
                            punkty.pop(0)

            if stan >= 2:
                liczba_segmentow = len(zamknieta_otoczka) - 1
                obecny_segment = int(postep_ksiecia)
                postep_segmentu = postep_ksiecia - obecny_segment

                for i in range(min(obecny_segment, liczba_segmentow)):
                    pygame.draw.line(ekran, ZIELONY, zamknieta_otoczka[i], zamknieta_otoczka[i+1], 10)

                if obecny_segment < liczba_segmentow:
                    p1 = zamknieta_otoczka[obecny_segment]
                    p2 = zamknieta_otoczka[obecny_segment + 1]
                    obecny_x_ksiecia = p1[0] + (p2[0] - p1[0]) * postep_segmentu
                    obecny_y_ksiecia = p1[1] + (p2[1] - p1[1]) * postep_segmentu
                    pygame.draw.line(ekran, ZIELONY, p1, (obecny_x_ksiecia, obecny_y_ksiecia), 10)
                    pygame.draw.circle(ekran, ZLOTY, (int(obecny_x_ksiecia), int(obecny_y_ksiecia)), 8)
                    postep_ksiecia += 0.02 
                else:
                    pygame.draw.line(ekran, ZIELONY, zamknieta_otoczka[-2], zamknieta_otoczka[-1], 10)
                    pygame.draw.circle(ekran, ZLOTY, zamknieta_otoczka[-1], 8)

                for straznik in straznicy_na_sciezce:
                    if straznik['widoczny'] and ((straznik['segment'] < obecny_segment) or straznik['segment'] == obecny_segment and straznik['proporcja'] <= postep_segmentu):
                        pygame.draw.circle(ekran, NIEBIESKI, (int(straznik['pozycja'][0]), int(straznik['pozycja'][1])), 4)

            if stan >= 3:
                indeks_obecnego_ataku = stan - 3 
                if indeks_obecnego_ataku < len(wygenerowane_ataki):
                    atak = wygenerowane_ataki[indeks_obecnego_ataku]
                    
                    pozycja_poczatkowa = straznicy_na_sciezce[atak['poczatek']]['pozycja']
                    pozycja_koncowa = straznicy_na_sciezce[atak['koniec']]['pozycja']
                    pygame.draw.line(ekran, (255, 200, 200), pozycja_poczatkowa, pozycja_koncowa, 20) 
                    
                    for i in range(atak['poczatek'], atak['koniec'] + 1):
                        pozycja_straznika = straznicy_na_sciezce[i]['pozycja']
                        pygame.draw.circle(ekran, (255, 0, 0), (int(pozycja_straznika[0]), int(pozycja_straznika[1])), 6)
                    
                    indeks = atak['indeks_najglosniejszego']
                    pozycja_zwyciezcy = straznicy_na_sciezce[indeks]['pozycja']
                    pygame.draw.circle(ekran, (255, 255, 0), (int(pozycja_zwyciezcy[0]), int(pozycja_zwyciezcy[1])), 10, 3)
                    
                    tekst_informacyjny = f"ATAK #{indeks_obecnego_ataku + 1}: Najgłośniejszy (ID {indeks}): {atak['najglosniejsza_wartosc']} dB"
                    napis = czcionka_duza.render(tekst_informacyjny, True, KOLOR_CZCIONKI)
                    ekran.blit(napis, (350, 300))

            for kopalnia in kopalnie:
                x, y = kopalnia.x, kopalnia.y
                tekst = ""
                match kopalnia.getSurowiec():
                    case models.Surowiec.ZLOTO: tekst = "Złoto"
                    case models.Surowiec.WEGIEL: tekst = "Węgiel"
                    case models.Surowiec.MIEDZ: tekst = "Miedź"
                    case models.Surowiec.URAN: tekst = "Uran"

                napis = czcionka.render(tekst, True, KOLOR_CZCIONKI)
                pole_napisu = napis.get_rect()
                pole_napisu.centerx = x + 5
                pole_napisu.bottom = y - 5

                pygame.draw.rect(ekran, (0, 255, 0), (x, y, 10, 10))
                ekran.blit(napis, pole_napisu)

            for krasnal, punkty in sciezki.items():
                for p in punkty:
                    pygame.draw.rect(ekran, (150, 150, 150), (p[0], p[1], 4, 4))

            for pracownik in krasnale:

                kopalnia = przydzielenie.get(pracownik)

                if kopalnia is not None and abs(pracownik.x - kopalnia.x) < 0.1 and abs(pracownik.y - kopalnia.y) < 0.1:
                    continue

                x, y = pracownik.x, pracownik.y
                tekst = ""
                match pracownik.getSurowiec():
                    case models.Surowiec.ZLOTO: tekst = "Z"
                    case models.Surowiec.WEGIEL: tekst = "W"
                    case models.Surowiec.MIEDZ: tekst = "M"
                    case models.Surowiec.URAN: tekst = "U"            

                napis = czcionka.render(tekst, True, KOLOR_CZCIONKI)
                pygame.draw.rect(ekran, (255, 0, 0), (x, y, 10, 10))
                ekran.blit(napis, (x, y - 20))

        else:
            ekran.fill((245, 245, 250))
            
            rozmiar_oryginalu_bity = len(raport) * 8
            rozmiar_skompresowany_bity = len(skompresowany)
            maksymalna_wartosc = max(rozmiar_oryginalu_bity, rozmiar_skompresowany_bity, 1)

            szerokosc_wykresu, wysokosc_wykresu = 700, 400
            x_wykresu = (1280 - szerokosc_wykresu) // 2
            y_wykresu = (720 - wysokosc_wykresu) // 2

            pygame.draw.rect(ekran, (255, 255, 255), (x_wykresu, y_wykresu, szerokosc_wykresu, wysokosc_wykresu))
            pygame.draw.rect(ekran, (200, 200, 200), (x_wykresu, y_wykresu, szerokosc_wykresu, wysokosc_wykresu), 2)

            wysokosc_oryginalu = int((rozmiar_oryginalu_bity / maksymalna_wartosc) * (wysokosc_wykresu - 100))
            wysokosc_skompresowanego = int((rozmiar_skompresowany_bity / maksymalna_wartosc) * (wysokosc_wykresu - 100))
            
            szerokosc_slupka = 150
            odstep_slupkow = 150

            slupek1_x = x_wykresu + szerokosc_wykresu // 2 - szerokosc_slupka - odstep_slupkow // 2
            slupek1_y = y_wykresu + wysokosc_wykresu - 50 - wysokosc_oryginalu
            pygame.draw.rect(ekran, (255, 100, 100), (slupek1_x, slupek1_y, szerokosc_slupka, wysokosc_oryginalu))
            pygame.draw.rect(ekran, (0, 0, 0), (slupek1_x, slupek1_y, szerokosc_slupka, wysokosc_oryginalu), 2)

            slupek2_x = x_wykresu + szerokosc_wykresu // 2 + odstep_slupkow // 2
            slupek2_y = y_wykresu + wysokosc_wykresu - 50 - wysokosc_skompresowanego
            pygame.draw.rect(ekran, (100, 100, 255), (slupek2_x, slupek2_y, szerokosc_slupka, wysokosc_skompresowanego))
            pygame.draw.rect(ekran, (0, 0, 0), (slupek2_x, slupek2_y, szerokosc_slupka, wysokosc_skompresowanego), 2)

            etykieta_oryginal = czcionka_duza.render(f"{rozmiar_oryginalu_bity} bitów", True, (0, 0, 0))
            etykieta_skompresowany = czcionka_duza.render(f"{rozmiar_skompresowany_bity} bitów", True, (0, 0, 0))
            ekran.blit(etykieta_oryginal, (slupek1_x + (szerokosc_slupka - etykieta_oryginal.get_width()) // 2, slupek1_y - 35))
            ekran.blit(etykieta_skompresowany, (slupek2_x + (szerokosc_slupka - etykieta_skompresowany.get_width()) // 2, slupek2_y - 35))

            opis_oryginalu = czcionka_duza.render("Przed kompresją", True, (0, 0, 0))
            opis_skompresowanego = czcionka_duza.render("Po alg. Huffmana", True, (0, 0, 0))
            ekran.blit(opis_oryginalu, (slupek1_x + (szerokosc_slupka - opis_oryginalu.get_width()) // 2, y_wykresu + wysokosc_wykresu - 30))
            ekran.blit(opis_skompresowanego, (slupek2_x + (szerokosc_slupka - opis_skompresowanego.get_width()) // 2, y_wykresu + wysokosc_wykresu - 30))

            tytul = czcionka_tytul.render("ARCHIWIZACJA WIEDZY - KOMPRESJA DANYCH", True, (50, 50, 50))
            ekran.blit(tytul, ((1280 - tytul.get_width()) // 2, y_wykresu - 80))

            stopien = (1 - rozmiar_skompresowany_bity / rozmiar_oryginalu_bity) * 100
            podsumowanie = czcionka_tytul.render(f"Zaoszczędzono: {stopien:.2f}% miejsca!", True, (0, 150, 0))
            ekran.blit(podsumowanie, ((1280 - podsumowanie.get_width()) // 2, y_wykresu + wysokosc_wykresu + 50))

        pygame.display.flip()
        zegar.tick(60)

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


def main(liczba_krasnali, miejsce_w_kopali, ile_atakow, czy_gui, czy_wizualizacja):

    if czy_gui:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, format="%(message)s")

    start = perf_counter()
    


    logging.info("--- ETAP 1: Przydział pracy ---")
    liczba_krasnali = liczba_krasnali           #REASONALBE LICZBY TO 250 50
    miejsce_w_kopalniach = miejsce_w_kopali

    krasnale = []
    kopalnie = []


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
    
    logging.info(f"Przydzielono {len(przydzial)} krasnoludków do pracy.")
    for krasnal, kopalnia in przydzial[:5]:
        logging.info(f"  Krasnoludek #{krasnal} -> Kopalnia #{kopalnia}")
    if len(przydzial) > 5:
        logging.info("  ...")

    logging.info("\n--- ETAP 2: Wyznaczanie trasy patrolu ---")
    uzyte_indeksy = set(kopalnia for _, kopalnia in przydzial)
    uzyte_kopalnie = [kopalnie[i] for i in uzyte_indeksy]

    logging.info(f"Liczba używanych kopalni (wierzchołków do otoczenia): {len(uzyte_kopalnie)}")
    
    punkty_otoczki = graham_scan(uzyte_kopalnie)
    dystans_patrolu = perimeter(punkty_otoczki)
    
    logging.info(f"Liczba wierzchołków otoczki wypukłej: {len(punkty_otoczki)}")
    logging.info(f"Codzienny dystans patrolu księcia: {dystans_patrolu:.2f} metrów")

    logging.info("\n--- ETAP 3: Dekametrowcy i rozkazy (RMQ) ---")

    liczba_straznikow = max(2, int(dystans_patrolu // 10))
    logging.info(f"Na trasie patrolu rozstawiono {liczba_straznikow} dekametrowców (co 10 metrów).")

    glosnosc_straznikow = [random.randint(10, 150) for _ in range(1000)]
    
    st = SparseTable(glosnosc_straznikow)

    liczba_atakow = ile_atakow
    logging.info(f"Symulacja {liczba_atakow} nagłych ataków na granice:")

    for i in range(1, liczba_atakow + 1):
        poczatek_ataku = random.randint(0, liczba_straznikow - 2)
        koniec_ataku = random.randint(poczatek_ataku + 1, liczba_straznikow - 1)
        
        najglosniejszy = st.query(poczatek_ataku, koniec_ataku)
        
        logging.info(f"  [Atak #{i}] Odcinek {poczatek_ataku}-{koniec_ataku}: Rozkaz do salwy wydaje krasnoludek o głośności {najglosniejszy}")
    
    logging.info(f"Atak jabłkami na odcinek od {poczatek_ataku} do {koniec_ataku}!")
    logging.info(f"Najgłośniejszy krasnoludek wyda rozkaz z głośnością: {najglosniejszy}")


    logging.info("\n--- ETAP 4: Archiwizacja wiedzy ---")

    raport = generuj_raport_dzienny(liczba_krasnali, liczba_kopalni, przydzial, dystans_patrolu, punkty_otoczki, liczba_straznikow, liczba_atakow)

    huffman = Huffman(raport)
    skompresowany = huffman.kompresuj()
    
    logging.info(f"Oryginalny tekst (długość {len(raport)} znaków): '{raport}'")
    logging.info(f"Skompresowany tekst bitowy (długość {len(skompresowany)} bitów): {skompresowany[:50]}...")

    with open("zadanie_out.txt", "w", encoding="UTF-8") as plik:
        plik.write(skompresowany)
    
    assert huffman.dekompresuj() == raport
    logging.info("Dekompresja przebiegła pomyślnie i bezstratnie.")

    wzorzec = "I."
    wyniki_kmp = KMP.algorytm_KMP(raport, wzorzec)
    logging.info(f"Wyszukiwanie wzorca KMP dla słowa '{wzorzec}': Znaleziono na indeksach {wyniki_kmp}")

    if czy_wizualizacja and czy_gui:
        wizualizacja(krasnale, kopalnie, przydzial, punkty_otoczki, liczba_atakow, st, raport, skompresowany)

    czas = perf_counter() - start

    if czy_gui:
        logging.info(f"Zakończono obliczenia, czas potrzebny do wykonania: {czas:.6f} sekund")
    else:
        return czas


def startup():

    liczba_krasnali = int(input("Podaj liczbe krasnali\n> "))

    miejsce_w_kopali = int(input("Podaj ilość miejsca w kopali\n> "))

    ile_atakow = int(input("Podaj liczbe ataków\n> "))

    czy_gui_holder = ""
    czy_wizualizacja_holder = ""

    czy_gui = False
    czy_wizualizacja = False

    while czy_gui_holder.lower() != "t" and czy_gui_holder.lower() != "n":
        czy_gui_holder = input("Czy włączyć gui? [T/N]\n> ")


    if czy_gui_holder.lower() == "t":
        czy_gui = True

        while czy_wizualizacja_holder.lower() != "t" and czy_wizualizacja_holder.lower() != "n":
            czy_wizualizacja_holder = input("Czy włączyć wizualiacje? [T/N]\n> ")

        if czy_wizualizacja_holder.lower() == "t":
            czy_wizualizacja = True

    main(liczba_krasnali, miejsce_w_kopali, ile_atakow, czy_gui, czy_wizualizacja)


if __name__ == "__main__":
    startup()