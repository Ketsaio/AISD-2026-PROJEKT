import random
import sys
import pygame
import time

# Zakładamy, że skompilowany moduł models (z pybind11) znajduje się w tym samym katalogu
import models
from geometry import graham_scan, perimeter
from range_query import SparseTable
from archive import Huffman, KMP

def visualize_pygame(workers, mines, assignments, hull_points):
    """
    Uruchamia interaktywną, sekwencyjną animację w Pygame.
    Kliknięcie myszą (lub spacja) przechodzi do kolejnego etapu.
    """
    pygame.init()
    pygame.font.init()
    
    WIDTH, HEIGHT = 1728, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("System Zarządzania: Królestwo Śnieżki")

    font = pygame.font.SysFont("Arial", 24, bold=True)

    # Definicje kolorów
    WHITE = (250, 250, 250)
    BLUE = (65, 105, 225)       # Krasnoludki
    RED = (220, 20, 60)         # Kopalnie
    GREEN = (34, 139, 34)       # Trasa patrolu
    GRAY = (150, 150, 150)      # Ścieżki przydziału 
    GOLD = (255, 215, 0)        # Książę
    TEXT_COLOR = (50, 50, 50)

    def scale(x, y):
        margin = 100
        scaled_x = int(margin + (x / 100.0) * (WIDTH - 2 * margin))
        scaled_y = int(margin + (y / 100.0) * (HEIGHT - 2 * margin))
        return scaled_x, scaled_y

    # Stan maszyny
    # 0 - Czeka na start ruchu krasnoludków
    # 1 - Krasnoludki w drodze
    # 2 - Czeka na start patrolu księcia
    # 3 - Książę w drodze
    # 4 - Koniec
    state = 0
    
    progress_dwarves = 0.0
    speed_dwarves = 0.008

    progress_prince = 0.0
    speed_prince = 0.02
    
    # Zamknięcie otoczki wypukłej (aby patrol okrążył teren i wrócił na start)
    if hull_points and len(hull_points) >= 3:
        hull_closed = hull_points + [hull_points[0]]
    else:
        hull_closed = []

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Reagowanie na kliknięcie lub nacisnięcie klawisza (np. spacji)
            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                state += 1

        screen.fill(WHITE)

        # Rysowanie wypełnienia otoczki wypukłej, jeśli patrol się skończył
        if state == 4 and hull_closed:
            scaled_hull = [scale(p.x, p.y) for p in hull_closed]
            surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(surface, (34, 139, 34, 30), scaled_hull)
            screen.blit(surface, (0, 0))

        # Rysowanie kopalń
        for m in mines:
            mx, my = scale(m.x, m.y)
            rect = pygame.Rect(mx - 10, my - 10, 20, 20)
            pygame.draw.rect(screen, RED, rect)

        # Rysowanie krasnoludków i ich śladów (ZMIENIONA LOGIKA)
        for dwarf_idx, mine_idx in assignments:
            w = workers[dwarf_idx]
            m = mines[mine_idx]
            sx, sy = w.x, w.y
            ex, ey = m.x, m.y

            # Obliczanie obecnej pozycji w zależności od postępu (zabezpieczone do max 1.0)
            current_p = min(progress_dwarves, 1.0)
            curr_x = sx + (ex - sx) * current_p
            curr_y = sy + (ey - sy) * current_p

            curr_scaled = scale(curr_x, curr_y)
            target_scaled = scale(ex, ey)

            # ZMIANA: Rysowanie linii od OBECNEJ pozycji krasnoludka do CELU (kopalni).
            # Linie wyświetlamy już od stanu 0, znikają całkowicie, gdy krasnoludek dotrze do celu (current_p == 1.0)
            if current_p < 1.0:
                pygame.draw.line(screen, GRAY, curr_scaled, target_scaled, 2)
            
            # Rysowanie krasnoludka na jego obecnej pozycji
            pygame.draw.circle(screen, BLUE, curr_scaled, 6)

        # Rysowanie patrolu księcia
        if state >= 3 and hull_closed:
            num_segments = len(hull_closed) - 1
            current_segment = int(progress_prince)

            # Rysowanie już w pełni przejechanych odcinków
            for i in range(min(current_segment, num_segments)):
                p1 = scale(hull_closed[i].x, hull_closed[i].y)
                p2 = scale(hull_closed[i+1].x, hull_closed[i+1].y)
                pygame.draw.line(screen, GREEN, p1, p2, 4)

            # Rysowanie bieżącego, trwającego odcinka
            if current_segment < num_segments:
                p1_x, p1_y = hull_closed[current_segment].x, hull_closed[current_segment].y
                p2_x, p2_y = hull_closed[current_segment+1].x, hull_closed[current_segment+1].y
                
                segment_progress = progress_prince - current_segment
                curr_prince_x = p1_x + (p2_x - p1_x) * segment_progress
                curr_prince_y = p1_y + (p2_y - p1_y) * segment_progress
                
                p1_scaled = scale(p1_x, p1_y)
                curr_prince_scaled = scale(curr_prince_x, curr_prince_y)
                
                # Zielona linia rysująca się za księciem
                pygame.draw.line(screen, GREEN, p1_scaled, curr_prince_scaled, 4)
                
                # Złota kropka (książę)
                pygame.draw.circle(screen, GOLD, curr_prince_scaled, 8)
            else:
                # Książę dotarł do końca, rysujemy go na mecie (początku)
                pygame.draw.circle(screen, GOLD, scale(hull_closed[-1].x, hull_closed[-1].y), 8)


        if state == 5:
                pygame.quit()


        # Interfejs tekstowy / Instrukcje u dołu ekranu
        instruction_text = ""
        if state == 0:
            instruction_text = "Kliknij myszką, aby wysłać krasnoludki do kopalń (MCMF)"
        elif state == 1:
            instruction_text = "Krasnoludki maszerują do pracy..."
        elif state == 2:
            instruction_text = "Kliknij myszką, aby rozpocząć patrol Księcia (Otoczka Wypukła)"
        elif state == 3:
            instruction_text = "Książę wizytuje obszar kopalń..."
        elif state == 4:
            instruction_text = "Wizualizacja zakończona. Możesz zamknąć okno."

        text_surf = font.render(instruction_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(text_surf, text_rect)

        # Aktualizacja logiki animacji
        if state == 1:
            progress_dwarves += speed_dwarves
            if progress_dwarves >= 1.0:
                progress_dwarves = 1.0
                state = 2  # Przechodzi do oczekiwania na księcia

        if state == 3 and hull_closed:
            progress_prince += speed_prince
            if progress_prince >= len(hull_closed) - 1:
                progress_prince = len(hull_closed) - 1
                state = 4  # Koniec animacji

        pygame.display.flip()
        clock.tick(60)


def main():
    print("=== System Zarządzania Królestwem Królewny Śnieżki ===\n")

    # ---------------------------------------------------------
    # 1. Przydział krasnoludków do pracy (MCMF)
    # ---------------------------------------------------------
    print("--- ETAP 1: Przydział pracy ---")
    num_workers = 5000
    num_mines = 1000
    mine_capacity = 5

    workers = []
    mines = []

    '''
    POPRAWIĆ BO LOSOWOŚĆ ZWIEDZIE

    Kransolodek może być uran, kopalnia możę być miedź i Kazahstańczyk i tak tam idzie
    '''

    start = time.time()

    # Generowanie losowych krasnoludków i ich preferencji
    for _ in range(num_workers):
        surowiec = random.choice([models.Surowiec.ZLOTO, models.Surowiec.WEGIEL, models.Surowiec.MIEDZ, models.Surowiec.URAN])
        workers.append(models.Krasnoludek(random.uniform(0, 100), random.uniform(0, 100), surowiec))

    # Generowanie kopalni
    for _ in range(num_mines):
        surowiec = random.choice([models.Surowiec.ZLOTO, models.Surowiec.WEGIEL, models.Surowiec.MIEDZ, models.Surowiec.URAN])
        mines.append(models.Kopalnia(random.uniform(0, 100), random.uniform(0, 100), surowiec, mine_capacity))

    # Algorytm MCMF przydziela pracę minimalizując sumaryczną odległość

    assignments = models.mcmf(workers, mines)
    
    print(time.time() - start)

    print(f"Przydzielono {len(assignments)} krasnoludków do pracy.")
    for dwarf_idx, mine_idx in assignments[:5]:
        print(f"  Krasnoludek #{dwarf_idx} -> Kopalnia #{mine_idx}")
    if len(assignments) > 5:
        print("  ...")

    # ---------------------------------------------------------
    # 2. Patrol Księcia (Otoczka Wypukła / Graham Scan)
    # ---------------------------------------------------------
    print("\n--- ETAP 2: Wyznaczanie trasy patrolu ---")
    # Zbieramy tylko te kopalnie, które są obecnie użytkowane
    used_mine_indices = set(mine_idx for _, mine_idx in assignments)
    used_mines = [mines[i] for i in used_mine_indices]

    print(f"Liczba używanych kopalni (wierzchołków do otoczenia): {len(used_mines)}")
    
    hull_points = graham_scan(used_mines)
    patrol_dist = perimeter(hull_points)
    
    print(f"Liczba wierzchołków otoczki wypukłej: {len(hull_points)}")
    print(f"Codzienny dystans patrolu księcia: {patrol_dist:.2f} metrów")

    # ---------------------------------------------------------
    # 3. Obrona przed jabłkami (Range Maximum Query)
    # ---------------------------------------------------------
    print("\n--- ETAP 3: Dekametrowcy i rozkazy (RMQ) ---")
    # Zakładamy rozstawienie 1000 dekametrowców na granicach z różnymi poziomami głośności
    guards_volumes = [random.randint(10, 150) for _ in range(1000)]
    
    # Inicjalizacja Sparse Table (O(n log n))
    st = SparseTable(guards_volumes)

    # Symulacja ataku na odcinek [150, 250]
    atak_start = 150
    atak_end = 250
    # Zapytanie w czasie O(1)
    loudest_volume = st.query(atak_start, atak_end)
    
    print(f"Atak jabłkami na odcinek od {atak_start} do {atak_end}!")
    print(f"Najgłośniejszy krasnoludek wyda rozkaz z głośnością: {loudest_volume}")

    # ---------------------------------------------------------
    # 4. Zapis wiedzy w księgach (Huffman & KMP)
    # ---------------------------------------------------------
    print("\n--- ETAP 4: Archiwizacja wiedzy ---")
    
    tekst_wiedzy = "strzały na cięciwy naciągnąć cięciwy strzał! królewna z księciem rządzą królestwem"
    
    # Kompresja Huffmana
    huffman = Huffman(tekst_wiedzy)
    skompresowany = huffman.kompresuj()
    
    print(f"Oryginalny tekst (długość {len(tekst_wiedzy)} znaków): '{tekst_wiedzy}'")
    print(f"Skompresowany tekst bitowy (długość {len(skompresowany)} bitów): {skompresowany[:50]}...")
    
    # Sprawdzenie bezstratności
    assert huffman.dekompresuj() == tekst_wiedzy
    print("Dekompresja przebiegła pomyślnie i bezstratnie.")

    # Wyszukiwanie wzorca KMP w zarchiwizowanych tekstach
    wzorzec = "cięciwy"
    wyniki_kmp = KMP.algorytm_KMP(tekst_wiedzy, wzorzec)
    print(f"Wyszukiwanie wzorca KMP dla słowa '{wzorzec}': Znaleziono na indeksach {wyniki_kmp}")
    visualize_pygame(workers, mines, assignments, hull_points)


if __name__ == "__main__":
    main()