import models

x = models.Punkt(2, 3)
y = models.Punkt(3, 2)

a = models.Krasnoludek(5, 5, models.Surowiec.MIEDZ)
b = models.Kopalnia(10, 10, models.Surowiec.WEGIEL, 5)

print(x.dystans(y))
print(a.dystans(b))
