from __future__ import annotations
from collections import Counter
import heapq

# przygotowanie obiktu Node służącego za węzeł
class Node:
    """
    Węzeł używany do budowy drzewa Huffmana.
    Przechowuje znak, częstotliwość występowania i dzieci.
    """

    def __init__(self, znak : str, czestotliwosc : int):
        self.lewo = None
        self.prawo = None
        self.znak = znak
        self.czestotliwosc = czestotliwosc

    # magiczna metoda (przeciążenie w C++) potrzebne do powrónania które wykonuje heapq
    def __lt__(self, other : Node) -> bool:
        return self.czestotliwosc < other.czestotliwosc
    
    def __repr__(self) -> str:
        return f"Node({self.znak}, {self.czestotliwosc})"

class Huffman:
    """
    Klasa odpowiadająca za generowanie drzewa Huffmana, przechowywanie go oraz kompresje i dekompresje.
    """

    def __init__(self, tekst : str):

        # obsługa edgecase gdy tekst składa sie z jednego tego samego znaku
        self.tekst = tekst
        if len(set(tekst)) == 1:
            znak = tekst[0]
            self.kody = {znak : "0"}
            self.korzen = Node(None, len(tekst))
            self.korzen.lewo = Node(znak, len(tekst))
            self.kod = None
            # print("Jeden znak")
        
        else:
            self.kolejka = self._przygotowanie_kolejki_priorytetowej()
            self.korzen = self._drzewo_huffmana()
            self.kody = {}
            self.kod = None
            self._generowanie_kodow(self.korzen)
            # print("1 < znaków")


    def _przygotowanie_kolejki_priorytetowej(self) -> list:
        """
        Zlicza znaki i przygotowuje kolejke priorytetową (kopiec minimalny) aby uzyskać złożoność O(n log n)
        zamiast O(n^2) w przypadku zwykłej implementacji kolejki priorytetowej.
        """

        czestotliwosci = Counter(self.tekst)

        priorytetowa = []

        for znak, czestotliwosc in czestotliwosci.items():
            node = Node(znak, czestotliwosc)
            heapq.heappush(priorytetowa, node)

        return priorytetowa

    def _drzewo_huffmana(self) -> Node:
        """
        Buduje drzewo Huffmana, łączy węzły o najmniejszych częstotliwościach.
        """

        while len(self.kolejka) > 1:
            lewo = heapq.heappop(self.kolejka)
            prawo = heapq.heappop(self.kolejka)
            
            rodzic = Node(None, lewo.czestotliwosc + prawo.czestotliwosc)

            rodzic.lewo = lewo
            rodzic.prawo = prawo

            heapq.heappush(self.kolejka, rodzic)

        return heapq.heappop(self.kolejka)

    def _generowanie_kodow(self, wezel : Node, aktualny_kod = "") -> None:
        """
        Rekurencyjnie przechodzi przez drzewo i generuje kody binarne dla drzewa Huffmana
        które są używane przy kompresji i dekompresji.
        """

        if wezel is None:
            return
        
        if wezel.znak is not None:
            self.kody[wezel.znak] = aktualny_kod
            return
        
        self._generowanie_kodow(wezel.lewo, aktualny_kod + "0")
        self._generowanie_kodow(wezel.prawo, aktualny_kod + "1")

    
    def kompresuj(self) -> str:
        """
        Kompresuje tekst do kodu używanego w drzewie Huffmana.
        """

        skompresowany = ""
        for znak in self.tekst:
            skompresowany += self.kody[znak]

        self.kod = skompresowany
        return skompresowany

    def dekompresuj(self) -> str:
        """
        Dekompresuje kod do czytelnego tekstu.
        """

        odpakowany = ""
        obecny_wezel = self.korzen

        for znak in self.kod:
            if znak == "0":
                obecny_wezel = obecny_wezel.lewo
            else:
                obecny_wezel = obecny_wezel.prawo

            if obecny_wezel.znak is not None:
                odpakowany += obecny_wezel.znak
                obecny_wezel = self.korzen

        return odpakowany

    # zwraca tekst podany przy inicjalizacji
    @property
    def oryginalny_tekst(self) -> str:
        return self.tekst
    
class KMP:
    """
    Klasa realizująca algorytm KMP (Knutha-Morrisa-Pratta).
    Nie wymaga istnienia obiektu przez użycie @staticmethod.
    """

    @staticmethod
    def _stworz_LPS(wzorzec : str) -> list[int]:
        """
        Tworzy tablice LPS (TU OPISAĆ DOKŁADNIE)

        """
        
        lista = [0] * len(wzorzec)
        dlugosc = 0
        i = 1
        
        while i < len(wzorzec):

            if wzorzec[i] == wzorzec[dlugosc]:
                dlugosc += 1
                lista[i] = dlugosc
                i += 1

            else:
                if dlugosc != 0:
                    dlugosc = lista[dlugosc-1]

                else:
                    lista[i] = 0
                    i += 1

        return lista

    @staticmethod
    def algorytm_KMP(tekst : str, wzorzec : str) -> list[int]:
        """
        Wyszukuje wszystkie wystąpienia wzorca z złożonością O(n + m)
        """
        
        lista = KMP._stworz_LPS(wzorzec)

        wyniki = []

        i = 0
        j = 0

        while i < len(tekst):
            if tekst[i] == wzorzec[j]:
                j += 1
                i += 1
                if j == len(wzorzec):
                    pozycja_startowa = i - j
                    wyniki.append(pozycja_startowa)

                    j = lista[j-1]
            
            else:
                if j != 0:
                    j = lista[j-1]
                    
                else:
                    i += 1

        return wyniki

        


if __name__ == "__main__":

    # test = Huffman(input("> "))
    # print(test.oryginalny_tekst)
    # skompresowane = test.kompresuj()
    # odpakowane = test.dekompresuj()

    # print(skompresowane)
    # print(odpakowane)
    
    # test2 = KMP()
    # print(test2.stworz_LPS("ABABACA"))
    print(KMP._stworz_LPS("ABABACA"))
