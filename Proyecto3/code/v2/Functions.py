import sympy
from Individual import *
from itertools import combinations_with_replacement
from sympy.utilities.lambdify import lambdify
from numpy.random import randint
from numpy.random import rand
from numpy import random

#Function Symbols
k1, k2, k3, k4, k5, x = sympy.symbols('k1 k2 k3 k4 k5 x')

#Possible functions
f0 = k1
f1 = k1*x + k2
f2 = k1*x**2 + k2*x + k3
f3 = k1*x**3 + k2*x**2 + k3*x + k4
f4 = k1*x**4 + k2*x**3 + k3*x**2 + k4*x + k5
f5 = k1*sympy.exp(k2*x)
f6 = k1 * sympy.sin(k2*x)
f7 = k1 * sympy.cos(k2*x)

#Functions used to print only
functionsDisp = [f0, f1, f2, f3, f4, f5, f6, f7]

#Lambda functions used for calculation of fitness
functions = [lambdify((k1,k2,k3,k4,k5,x), f0, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f1, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f2, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f3, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f4, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f5, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f6, 'numpy'),
            lambdify((k1,k2,k3,k4,k5,x), f7, 'numpy')]

#List with all the possible combinations of functions for f(x) and g(x)
_funcCombinations = list(combinations_with_replacement([0,1,2,3,4,5,6,7], 2))


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
    genome = randint(0, 2, (pNbits * pNk * 2)).tolist()
    return genome


"""
    Creates a random initial population

    A random combination of functions for f(x) and g(x) is picked
    from the "_funcCombinations" list

    The genome of each indivual is composed by the following items:
        genome = <funcF> + <K values> + <funcG> + <K values>

        where:
            funcF       -> 3 bits enconding the type of function for f(x)
            funcG       -> 3 bits enconding the type of function for g(x)
            K values    -> pNk number of constants encoded with a size 
                            of pNbits each
"""
def initialPopulation(pPopSize, pLifeSpan, pNbits, pNk):

    #Select a random function combination to test
    ix = randint(0, len(_funcCombinations))
    combination = _funcCombinations[ix]
    del _funcCombinations[ix]

    #Enconde functions type in bitstrings
    binFuncF = [int(x) for x in '{:03b}'.format(combination[0])]
    binFuncG = [int(x) for x in '{:03b}'.format(combination[1])]

    #Create random individuals
    population = []
    for i in range(pPopSize):
        randomBits = randomGenome(pNbits, pNk)
        genome = binFuncF + randomBits[:(pNbits*pNk)] + binFuncG + randomBits[(pNbits*pNk):]
        population.append(Individual(pLifeSpan, genome))

    return population



"""
    Roulette selection (fitness proportionate selection)
    
    Because the purpose of the algorithm is to minimize the value 
    of fitness, the probability is calculated using the inverse (1/fitness)
    This way individuals with lower fitness will have more probability
    of being selected than individuals with higher fitness
"""
def rouletteSelection(pPop):
    totalFitness = sum((1/ind.fitness) for ind in pPop)
    # 1/fitness is used to give the individuals with lower fitness
    #more probability of selection
    for ind in pPop:
        ind.probability = (1/ind.fitness) / totalFitness
    
    probs = []
    for i in range(len(pPop)):
        acc = sum(pPop[i].probability for i in range(0, i+1))
        probs.append(acc)

    selected = list()

    for n in range(len(pPop)):
        r = rand()
        for (i, individual) in enumerate(pPop):
            if r <= probs[i]:
                selected.append(individual)
                break
    
    return selected


def earlyTermination(pPop):
    n = 0
    minFitness = min(pPop, key=lambda x: x.fitness).fitness - 1
    totalScaledFitness = sum((ind.fitness - minFitness) for ind in pPop)
    for (i, individual) in enumerate(pPop):
        if math.isinf(individual.fitness):
            del pPop[i]
            n += 1
        elif individual.lifeSpan <= 0:
            del pPop[i]
            n += 1
        else:
            deathProbability = (individual.fitness - minFitness) / totalScaledFitness
            dies = random.choice([0,1], 1, p=[(1-deathProbability), deathProbability])
            if dies:
                del pPop[i]
                n += 1


"""
    Crossover is done between the bits that encodes each of the 
    K constants (k1,k2,k3,k4,k5) for f(x) and g(x)

    A random point is choosen to make the crossover between
    the genome of the two parents

    Example using 9 bits to encode each K:
                                 ↓
        Parent1(p1) ->  |0|1|1|0|1|0|1|0|0|
                                 ↓
        Parent2(p2) ->  |1|1|1|0|0|0|1|1|1|    

        Child1(c1) ->   |0|1|1|0|0|0|1|1|1|
                        ---p1---|----p2---

        Child2(c2) ->   |1|1|1|0|1|0|1|0|0|
                        ---p2---|----p1---

"""
def crossover(pParent1, pParent2, pNbits, pNk, pRcross, pLifeSpan):
    c1 = Individual(pLifeSpan, pParent1.genome)
    c2 = Individual(pLifeSpan, pParent2.genome)

    if rand() < pRcross:
        #Extract the type of functions f(x) and g(x)
        funcF = pParent1.genome[0 : 3]
        funcG = pParent1.genome[(pNbits*pNk)+3 : (pNbits*pNk)+6] 

        #Extract the bitstrings for all the Ks of f(x) and g(x)
        kF1 = pParent1.genome[3 : (pNk * pNbits)+3] 
        kG1 = pParent1.genome[(pNk * pNbits)+6 : ] 
        kF2 = pParent2.genome[3 : (pNk * pNbits)+3] 
        kG2 = pParent2.genome[(pNk * pNbits)+6 : ] 

        #Get the bits of each K (k1, k2, etc)
        nKF1 = [kF1[(i*pNbits):(i*pNbits)+pNbits] for i in range(pNk)]
        nKG1 = [kG1[(i*pNbits):(i*pNbits)+pNbits] for i in range(pNk)]
        nKF2 = [kF2[(i*pNbits):(i*pNbits)+pNbits] for i in range(pNk)]
        nKG2 = [kG2[(i*pNbits):(i*pNbits)+pNbits] for i in range(pNk)]

        pt = randint(1, pNbits-2) #Random point of crossover
        c1_F, c1_G = list(), list()
        c2_F, c2_G = list(), list()
        for i in range(pNk):
            c1_F = c1_F + (nKF1[i][:pt] + nKF2[i][pt:])
            c1_G = c1_G + (nKG1[i][:pt] + nKG2[i][pt:])
            
            c2_F = c2_F + (nKF2[i][:pt] + nKF1[i][pt:])
            c2_G = c2_G + (nKG2[i][:pt] + nKG1[i][pt:])
            
        c1.genome = funcF + c1_F + funcG + c1_G
        c2.genome = funcF + c2_F + funcG + c2_G

    return [c1, c2]


"""
    Mutation is done using pRmut, which is the probability
    of mutation

    The decision to change the constants of f(x) or g(x)
    is done using a 50-50 probability
"""
def mutation(pIndividual, pNbits, pNk, pRmut):
    mutates = random.choice([0,1], 1, p=[(1-pRmut), pRmut]) 
    if mutates:
        function = random.choice([0,1], 1, p=[(1-0.5), 0.5]) 
        if function: #Mutate Ks of function F
            for k in range(pNk):
                mutates = random.choice([0,1], 1, p=[(1-pRmut), pRmut]) 
                gene = randint((k * pNbits)+3, ((k+1) * pNbits)+3)
                if mutates:
                    pIndividual.genome[gene] = 1 - pIndividual.genome[gene]

        else: #Mutate Ks of function G
            for k in range(pNk):
                mutates = random.choice([0,1], 1, p=[(1-pRmut), pRmut]) 
                gene = randint((k * pNbits)+(pNk*pNbits)+6, ((k+1) * pNbits)+(pNk*pNbits)+6)
                if mutates:
                    pIndividual.genome[gene] = 1 - pIndividual.genome[gene]


"""
    Used to print the function represented by an individual of the population

    The genome of the individual is decoded to determine the type of
    functions that are f(x) and g(x). Later, the value of constants 
    (k1,k2,etc) is substituted in the corresponding functions
"""
def printFunc(pIndividual, pBounds, pNbits, pNk):
    # funcTypes = getFuncTypes(genome, nBits, nK)
    decoded = pIndividual.decode(pBounds, pNbits, pNk)
    funcF = decoded[0]
    funcG = decoded[1]

    fx = functionsDisp[funcF].evalf(subs = {k1: decoded[2],
        k2: decoded[3], k3: decoded[4], k4: decoded[5], k5: decoded[6]})
    gx = functionsDisp[funcG].evalf(subs = {k1: decoded[7],
        k2: decoded[8], k3: decoded[9], k4: decoded[10], k5: decoded[11]})

    hx = fx + gx
        
    print("H(x) = ", fx + gx, " with fitness = ", pIndividual.fitness)
    return hx

