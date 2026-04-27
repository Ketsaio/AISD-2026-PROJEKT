import unittest
from archive import Huffman, KMP

class TestHuffman(unittest.TestCase):

    def test_zwykly_tekst(self):
        tekst = "Znalazlem wczoraj dwie antonowki"
        huffman = Huffman(tekst)
        skompresowany = huffman.kompresuj()
        odpakowany = huffman.dekompresuj()

        self.assertEqual(tekst, odpakowany)
        self.assertTrue(all(znak in '01' for znak in skompresowany))

    def test_jeden_znak(self):
        tekst = "AAAAAAA"
        huffman = Huffman(tekst)
        skompresowany = huffman.kompresuj()
        odpakowany = huffman.dekompresuj()
        
        self.assertEqual(tekst, odpakowany)

    def test_krotki_tekst(self):
        tekst = "a"
        huffman = Huffman(tekst)
        skompresowany = huffman.kompresuj()
        odpakowany = huffman.dekompresuj()
        
        self.assertEqual(tekst, odpakowany)


class TestKMP(unittest.TestCase):

    def setUp(self):
        self.kmp = KMP()

    def test_tworzenie_LPS_klasyk(self):
        wzorzec = "ABABACA"
        oczekiwana_lista = [0, 0, 1, 2, 3, 0, 1]
        wynik = KMP._stworz_LPS(wzorzec)

        self.assertEqual(wynik, oczekiwana_lista)

    def test_tworzenie_LPS_brak_powtorzen(self):
        wzorzec = "ABCDEF"
        oczekiwana_lista = [0, 0, 0, 0, 0, 0]
        wynik = KMP._stworz_LPS(wzorzec)

        self.assertEqual(wynik, oczekiwana_lista)

    def test_algorytm_szukanie_zwykle(self):
        tekst = "To jest wielki raport o antonowkach."
        wzorzec = "raport"
        
        self.assertEqual(self.kmp.algorytm_KMP(tekst, wzorzec), [15])

    def test_algorytm_wiele_wystapien(self):
        tekst = "KOT i inny KOT to dwa KOTy"
        wzorzec = "KOT"
        
        self.assertEqual(self.kmp.algorytm_KMP(tekst, wzorzec), [0, 11, 22])

    def test_algorytm_zachodzenie_na_siebie(self):
        tekst = "AAAA"
        wzorzec = "AA"
        
        self.assertEqual(self.kmp.algorytm_KMP(tekst, wzorzec), [0, 1, 2])

    def test_algorytm_brak_wzorca(self):
        tekst = "Tutaj nie ma szukanego slowa"
        wzorzec = "Ziemniak"
        
        self.assertEqual(self.kmp.algorytm_KMP(tekst, wzorzec), [])

    def test_algorytm_wzorzec_dluzszy_niz_tekst(self):
        tekst = "Krotko"
        wzorzec = "Bardzo dlugi wzorzec"
        
        self.assertEqual(self.kmp.algorytm_KMP(tekst, wzorzec), [])


class TestIntegracjiAlgorytmow(unittest.TestCase):

    def setUp(self):
        self.kmp = KMP()

    def test_huffman_i_kmp_klasycznie(self):
        tekst = "TAJNY RAPORT BAZY O TAJNYCH DZIALANIACH W TAJNYM MIEJSCU"
        wzorzec = "TAJNY"

        huffman = Huffman(tekst)
        huffman.kompresuj()
        odpakowany_tekst = huffman.dekompresuj()

        wyniki = self.kmp.algorytm_KMP(odpakowany_tekst, wzorzec)
        
        self.assertEqual(wyniki, [0, 20, 42])

    def test_kmp_szuka_w_skompresowanych_danych(self):
        tekst = "ABRAKADABRA"
        szukany_wzorzec = "DAB"

        huffman = Huffman(tekst)
        skompresowany_tekst = huffman.kompresuj()

        wzorzec_binarnie = ""
        for znak in szukany_wzorzec:
            wzorzec_binarnie += huffman.kody[znak]

        wyniki_binarne = self.kmp.algorytm_KMP(skompresowany_tekst, wzorzec_binarnie)

        self.assertEqual(len(wyniki_binarne), 1)

    def test_pusty_wzorzec_w_skompresowanym_tekscie(self):
        tekst = "ZABEZPIECZONY PLIK ARCHIWUM"
        szukany_wzorzec = "BRAK_TEGO_SLOWA"

        huffman = Huffman(tekst)
        skompresowany = huffman.kompresuj()
        
        wzorzec_binarnie = ""
        for znak in szukany_wzorzec:
            if znak in huffman.kody:
                wzorzec_binarnie += huffman.kody[znak]
            else:
                wzorzec_binarnie = "NIE_ISTNIEJE"
                break
                
        if wzorzec_binarnie == "NIE_ISTNIEJE":
            wynik = []
        else:
            wynik = self.kmp.algorytm_KMP(skompresowany, wzorzec_binarnie)

        self.assertEqual(wynik, [])


if __name__ == '__main__':
    unittest.main()