import models

x = models.Punkt(2, 3)
y = models.Punkt(3, 2)

a1 = models.Krasnoludek(5, 5, models.Surowiec.MIEDZ)
a2 = models.Krasnoludek(2, 3, models.Surowiec.MIEDZ)
a3 = models.Krasnoludek(50, 50, models.Surowiec.MIEDZ)
b1 = models.Kopalnia(10, 10, models.Surowiec.WEGIEL, 5)
b2 = models.Kopalnia(55, 55, models.Surowiec.WEGIEL, 2)

print(x.dystans(y))
print(a1.dystans(b1))

lista = models.mcmf([a1, a2, a3], [b1, b2])
print(lista)
