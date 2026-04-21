import models
import random
import time

workers = []
mines = []

w = int(input("num of workers: "))
m = int(input("num of mines: "))
c = int(input("mine capacity: "))

print(f"testing {w} workers with {m} mines of capacity {c}")
startTime = time.perf_counter()

for _ in range(w):	
	workers.append(models.Krasnoludek(random.random() * 1000, random.random() * 1000, models.Surowiec.URAN))

for _ in range(m):
	mines.append(models.Kopalnia(random.random() * 1000, random.random() * 1000, models.Surowiec.MIEDZ, c))

models.mcmf(workers, mines)

endTime = time.perf_counter()
print(f"time: {endTime - startTime:.6f} seconds")