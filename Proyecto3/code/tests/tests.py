from numpy.core.fromnumeric import product, repeat
from numpy.random import rand
from numpy.random import randint
from numpy import random
from itertools import combinations, combinations_with_replacement
from itertools import product

def remove(pL):
    del pL[3]

class Test:
    fitness = None

    def __init__(self, pFitness):
        self.fitness = pFitness


l = [Test(rand()) for _ in range(5)]

l = [1,2,3,4,5,6,7,8,9]

def change(pL):
    del l[0]


change(l)
print(l)




