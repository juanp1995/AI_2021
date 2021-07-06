import sympy
from Individual import *
from itertools import combinations
from sympy.utilities.lambdify import lambdify
from numpy.random import randint
from numpy.random import rand
from numpy import random

#Function Symbols
k1, k2, k3, k4, x = sympy.symbols('k1 k2 k3 k4 x')

#Possible functions
f0 = k1
f1 = k1*x + k2
f2 = k1*x**2 + k2*x + k3
f3 = k1*x**3 + k2*x**2 + k3*x + k4
f4 = k1*x**4 + k2*x**3 + k3*x**2 + k4*x
f5 = k1*sympy.exp(k2*x)
f6 = k1 * sympy.sin(k2*x)
f7 = k1 * sympy.cos(k2*x)

#Functions used for display
functionsDisp = [f0, f1, f2, f3, f4, f5, f6, f7]

#Lambda functions used for calculation of fitness
functions = [lambdify((k1,k2,k3,k4,x), f0, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f1, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f2, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f3, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f4, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f5, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f6, 'numpy'),
            lambdify((k1,k2,k3,k4,x), f7, 'numpy')]


#
# Read the files with the x and f(x) data
#
def readData(pXpath, pFpath):
    x = open(pXpath, 'r')
    f = open(pFpath, 'r')
    data = []

    while True:
        xValue, fValue = x.readline(), f.readline()
        if not xValue:
            break
    
        newVal = [int(xValue, 10), int(fValue, 10)]
        data.append(newVal)    
    x.close()
    f.close()
    return data


#
#Generates a random genome used for the initial population
#
def randomGenome(pNbits, pNk):
    genome = randint(0, 2, pNbits * pNk * 2).tolist()
    return genome


def selection(pPop, k=40):
    selection_ix = randint(len(pPop))
    for ix in randint(0, len(pPop), k-1):
        if pPop[ix].fitness < pPop[selection_ix].fitness:
            # if ((pPop[ix].func_F == pPop[selection_ix].func_F) and (pPop[ix].func_G == pPop[selection_ix].func_G)):
            selection_ix = ix
    return pPop[selection_ix]



def rouletteSelection(pPop, pNcandidates):
    totalFitness = sum((1/ind.fitness) for ind in pPop)
    # 1/fitness is used to give the individuals with lower fitness
    #more probability of selection
    for ind in pPop:
        ind.probability = (1/ind.fitness) / totalFitness

    pPop = sorted(pPop, key=lambda x: x.probability, reverse=True)
    
    probs = []
    for i in range(len(pPop)):
        acc = sum(pPop[i].probability for i in range(0, i+1))
        probs.append(acc)

    selected = []

    for n in range(len(pPop)):
        r = rand()
        for (i, individual) in enumerate(pPop):
            if r <= probs[i]:
                selected.append(individual)
                break
    
    return selected



def crossover(pParent1, pParent2, pRcross):
    c1 = Individual(pParent1.lifeSpan, pParent1.genome, pParent1.func_F, pParent1.func_G)
    c2 = Individual(pParent2.lifeSpan, pParent2.genome, pParent2.func_F, pParent2.func_G)

    if rand() < pRcross:
        kF1 = pParent1.genome[:int(len(pParent1.genome)/2)] 
        kG1 = pParent1.genome[int(len(pParent1.genome)/2):] 
        kF2 = pParent2.genome[:int(len(pParent2.genome)/2)] 
        kG2 = pParent2.genome[int(len(pParent2.genome)/2):] 

        nKF1 = [kF1[(i*32):(i*32)+32] for i in range(4)]
        nKG1 = [kG1[(i*32):(i*32)+32] for i in range(4)]
        nKF2 = [kF2[(i*32):(i*32)+32] for i in range(4)]
        nKG2 = [kG2[(i*32):(i*32)+32] for i in range(4)]

        pt = randint(1, len(nKF1)-2)
        c1_F, c2_F = list(), list()
        c1_G, c2_G = list(), list()
        for i in range(4):
            c1_F = c1_F + (nKF1[i][:pt] + nKF2[i][pt:])
            c1_G = c1_G + (nKG1[i][:pt] + nKG2[i][pt:])
            
            c2_F = c2_F + (nKF2[i][:pt] + nKF1[i][pt:])
            c2_G = c2_G + (nKG2[i][:pt] + nKG1[i][pt:])
            
        c1.genome = c1_F + c1_G
        c2.genome = c2_F + c2_G


        # pt = randint(1, int((len(pParent1.genome)/2)-2))
        # partF1 = pParent1.genome[:pt] + pParent2.genome[pt:int(len(pParent2.genome)/2)]
        # partF2 = pParent2.genome[:pt] + pParent1.genome[pt:int(len(pParent1.genome)/2)]

        # pt = randint(int(len(pParent1.genome)/2)+1, int(len(pParent1.genome)-2))
        # partG1 = pParent1.genome[int(len(pParent1.genome)/2):pt] + pParent2.genome[pt:]
        # partG2 = pParent2.genome[int(len(pParent2.genome)/2):pt] + pParent1.genome[pt:]


        # c1.genome = partF1 + partG1
        # c2.genome = partF2 + partG2
    return [c1, c2]


def mutation(pIndividual, pRmut):
    mutates = random.choice([0,1], 1, p=[(1-pRmut), pRmut]) 
    if mutates:
        gene = randint(0, len(pIndividual.genome))
        pIndividual.genome[gene] = 1 - pIndividual.genome[gene]
    # for i in range(len(pIndividual.genome)):
    #     if rand() < pRmut:
    #         pIndividual.genome[i] = 1-pIndividual.genome[i]

def getNewBest(pPop):
    minFitness = 0
    for i in range(len(pPop)):
        if(pPop[i].fitness < pPop[minFitness].fitness):
            minFitness = i
    return pPop[minFitness]


def printFunc(pIndividual, pBounds, pNbits, pNk):
    # funcTypes = getFuncTypes(genome, nBits, nK)
    decoded = pIndividual.decode(pBounds, pNbits, pNk)

    fx = functionsDisp[pIndividual.func_F].evalf(subs = {k1: decoded[0],
        k2: decoded[1], k3: decoded[2], k4: decoded[3]})
    gx = functionsDisp[pIndividual.func_G].evalf(subs = {k1: decoded[4],
        k2: decoded[5], k3: decoded[6], k4: decoded[7]})

    hx = fx + gx
        
    print("H(x) = ", fx + gx, " with fitness = ", pIndividual.fitness)
    return hx


def initialPopulation(pPopSize, pNcandidates, pLifeSpan, pNbits, pNk):
    #List possible combinations of functions F(x) and G(x)
    comb = list(combinations([0,1,2,3,4,5,6,7], 2))

    #Select randomly, <pNcandidates> unique combinations as candidates for the solution
    candidates = list()
    for _ in range(pNcandidates):
        ix = randint(0, len(comb))
        candidates.append(comb[ix])
        del comb[ix]


    #Determine how many individuals needs to be generated
    #for each candidate solution
    sliceSize = int(pPopSize/pNcandidates)
    remainder = pPopSize - (sliceSize*pNcandidates)
    print("Slice size: ", sliceSize, " Remainder: ", remainder)


    #Create random individuals for each candidate solution
    population = []
    for i in range(pNcandidates):
        funcs = candidates[i]
        for j in range(sliceSize):
            newIndividual = Individual(pLifeSpan, randomGenome(pNbits, pNk), funcs[0], funcs[1])
            population.append(newIndividual)
        
    #If there are more individuals to be generated, add them to the last candidate
    # if remainder > 0:
    #     funcs = candidates[pNcandidates-1]
    #     for i in range(remainder):
    #         newIndividual = Individual(pLifeSpan, randomGenome(pNbits, pNk), funcs[0], funcs[1])
    #         population.append(newIndividual)

    return population

