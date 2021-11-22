from classes import Scout
import time

start = time.time()
scout = Scout(3)
print(scout.scores)
print(f'scout.scores took {round(time.time() - start, 2)}')
