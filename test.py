from benchmark import *
import time

@benchmark
def lol():
    time.sleep(0.2)

@benchmark
def lol2():
    time.sleep(0.1)

for i in range(5):
    lol()
    lol2()

show_stats()