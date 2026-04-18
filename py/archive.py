from __future__ import annotations
from collections import Counter
import heapq

# przygotowanie obiktu Node służącego za węzeł
class Node:
    def __init__(self, znak : str, czestotliwosc : int):
        self.lewo = None
        self.prawo = None
        self.znak = znak
        self.czestotliwosc = czestotliwosc

    def __lt__(self, other : Node):
        return self.czestotliwosc < other.czestotliwosc
    
    def __repr__(self):
        return f"Node({self.znak}, {self.czestotliwosc})"

class Huffman:

    def __init__(self, tekst : str):

        self.tekst = tekst
        if len(tekst) == 1:
            self.kod = 0
            self.kody = {tekst : "0"}
            self.korzen = Node(None, 1)
            self.korzen.lewo = Node(tekst, 1)
            print("Jeden znak")
        
        else:
            self.kolejka = self.przygotowanie_kolejki_priorytetowej()
            self.korzen = self.drzewo_huffmana()
            self.kody = {}
            self.kod = None
            self.generowanie_kodow(self.korzen)
            print("1 < znaków")

    # przygotowanie kolejki priorytetowej opartej na kopcu aby otrzymać złożoność O(n log n)
    def _przygotowanie_kolejki_priorytetowej(self) -> list:

        czestotliwosci = Counter(self.tekst)

        priorytetowa = []

        for znak, czestotliwosc in czestotliwosci.items():
            node = Node(znak, czestotliwosc)
            heapq.heappush(priorytetowa, node)

        return priorytetowa

    # tworzy drzewo huffmana i zwraca korzeń drzewa
    def _drzewo_huffmana(self) -> Node:

        while len(self.kolejka) > 1:
            lewo = heapq.heappop(self.kolejka)
            prawo = heapq.heappop(self.kolejka)
            
            rodzic = Node(None, lewo.czestotliwosc + prawo.czestotliwosc)

            rodzic.lewo = lewo
            rodzic.prawo = prawo

            heapq.heappush(self.kolejka, rodzic)

        return heapq.heappop(self.kolejka)

    # funkcja generująca kody do kompresji przy użyciu drzewa Huffmana
    def _generowanie_kodow(self, wezel : Node, aktualny_kod = "") -> dict:
        
        if wezel is None:
            return
        
        if wezel.znak is not None:
            self.kody[wezel.znak] = aktualny_kod
            return
        
        self.generowanie_kodow(wezel.lewo, aktualny_kod + "0")
        self.generowanie_kodow(wezel.prawo, aktualny_kod + "1")

    def kompresuj(self) -> str:
        skompresowany = ""
        for znak in self.tekst:
            skompresowany += self.kody[znak]

        self.kod = skompresowany
        return skompresowany

    def dekompresuj(self) -> str:
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


if __name__ == "__main__":

    test = Huffman(input("> "))
    skompresowane = test.kompresuj()
    odpakowane = test.dekompresuj()

    print(skompresowane)
    print(odpakowane)
