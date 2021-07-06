from numpy import random
from numpy.random import randint
from numpy.random import rand
from numpy import float128
import sympy
from sympy.utilities.lambdify import lambdify

#Posible functions
k1, k2, k3, k4, x = sympy.symbols('k1 k2 k3 k4 x')
f0 = k1
f1 = k1*x**4 + k2*x**3 + k3*x**2 + k4*x**3
f2 = k1*sympy.exp(k2*x)
f3 = k1 * sympy.sin(k2*x)
f4 = k1 * sympy.cos(k2*x)
functionsDisp = [f0, f1, f2, f3, f4]
functions = [lambdify((k1,k2,k3,k4,x), f0, 'numpy'),
    lambdify((k1,k2,k3,k4,x), f1, 'numpy'),
    lambdify((k1,k2,k3,k4,x), f2, 'numpy'),
    lambdify((k1,k2,k3,k4,x), f3, 'numpy'),
    lambdify((k1,k2,k3,k4,x), f4, 'numpy')]

class Individual:
    lifeSpan = 5
    def __init__(self, pGenome):
        self.genome = pGenome


#
# Read the files with the x and f(x) data
#
def readData(xFilePath, fFilePath):
    x = open(xFilePath, 'r')
    f = open(fFilePath, 'r')
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
def randomGenome(nBits, nK):
    genome = []
    for _ in range(2):
        num = randint(0, 5)
        newBits = [int(x) for x in '{:0{size}b}'.format(num, size=3)]
        newBits = newBits + randint(0, 2, nBits * nK).tolist()
        genome = genome + newBits
    return genome


#
#Decodes an individual genome to the corresponding values of Ks
#
def decode(bounds, nBits, nK, bitstring):
    decoded = list()
    largest = 2**nBits
    for i in range(nK*2):
        if(i == 4):
            start, end = (i * nBits)+6, (i * nBits) + 6 + nBits
        else:
            start, end = (i * nBits)+3, (i * nBits) + 3 + nBits
        substring = bitstring[start:end]

        chars = "".join([str(s) for s in substring])
        integer = int(chars, 2)
        value = bounds[0][0] + (integer/largest) * (bounds[0][1] - bounds[0][0])
        decoded.append(round(value, 4))
    return decoded


def getFuncTypes(genome, nBits, nK):
    fType = genome[0:3]
    gType = genome[(nBits*nK)+3:(nBits*nK)+6]
    fChars = "".join([str(x) for x in fType])
    gChars = "".join([str(x) for x in gType])
    return [int(fChars, 2), int(gChars, 2)]


def calcFitness(individual, bounds, nBits, nK, data):
    funcTypes = getFuncTypes(individual.genome, nBits, nK)
    decoded = decode(bounds, nBits, nK, individual.genome)

    fitness = 0
    
    for i in range(len(data)):
        fx = functions[funcTypes[0]](float128(decoded[0]), float128( decoded[1]), 
            float128(decoded[2]), float128(decoded[3]), float128(data[i][0]))
        gx = functions[funcTypes[1]](float128(decoded[4]), float128( decoded[5]), 
            float128(decoded[6]), float128(decoded[7]), float128(data[i][0]))
        # gx = functions[funcTypes[1]](decoded[4], decoded[5], decoded[6], decoded[7], data[i][0])
        # fx = functionsDisp[funcTypes[0]].evalf(subs = {k1: decoded[0],
        #     k2: decoded[1], k3: decoded[2],
        #     k4: decoded[3], x: data[i][0]})
        # gx = functionsDisp[funcTypes[1]].evalf(subs = {k1: decoded[4],
        #     k2: decoded[5], k3: decoded[6],
        #     k4: decoded[7], x: data[i][0]})
        
        hx = fx + gx
        fitness += 1/abs(hx - data[i][1])

    individual.fitness = fitness


def selection(population, k=3):
    selection_ix = randint(len(population))
    for ix in randint(0, len(population), k-1):
        if population[ix].fitness > population[selection_ix].fitness:
            selection_ix = ix
    return population[selection_ix]


def crossover(parent1, parent2, rateCross):
    c1 = Individual(parent1.genome)
    c2 = Individual(parent2.genome)
    if rand() < rateCross:
        pt = 131 #Crossover point in the middle
        c1.genome = parent1.genome[:pt] + parent2.genome[pt:]
        c2.genome = parent2.genome[:pt] + parent1.genome[pt:]
    return [c1, c2]


def mutation(individual, rateMut):
    for i in range(len(individual.genome)):
        if (i>2 and i<131) or i>134:
            individual.genome[i] = 1-individual.genome[i]

def getNewBest(population):
    maxFitness = 0
    for i in range(len(population)):
        if(population[i].fitness > population[maxFitness].fitness):
            maxFitness = i
    return population[maxFitness]


def printFunc(genome, bounds, nBits, nK):
    funcTypes = getFuncTypes(genome, nBits, nK)
    decoded = decode(bounds, nBits, nK, genome)

    fx = functionsDisp[funcTypes[0]].evalf(subs = {k1: decoded[0],
        k2: decoded[1], k3: decoded[2],
        k4: decoded[3]})
    gx = functionsDisp[funcTypes[1]].evalf(subs = {k1: decoded[4],
        k2: decoded[5], k3: decoded[6],
        k4: decoded[7]})
        
    hx = fx + gx
    print("H(x) = ", hx)



def GA(nBits, bounds, nK, nIter, popSize, rateCross, rateMut):
    population = []
    data = readData('../x.txt', '../f.txt')

    #Create random initial population
    for _ in range(popSize):
        newIndividual = Individual(randomGenome(nBits, nK))
        population.append(newIndividual)

    best = population[0]

    for gen in range(nIter):
        #Calculate fitness
        for individual in population:
            calcFitness(individual, bounds, nBits, nK, data)

        #Check new best solution
        best = getNewBest(population)
        printFunc(best.genome, bounds, nBits, nK)

        #Select parents
        selected = [selection(population) for _ in range(_populationSize)]
        #Create next generation
        children = list()
        for i in range(0, popSize, 2):
            p1, p2 = selected[i], selected[i+1]
            #Crossover and mutation
            for c in crossover(p1, p2, rateCross):
                mutation(c, rateMut)
                children.append(c)
        
        #Replace population
        population = children
    return best


_populationSize = 100
_nBits = 32
_nK = 4
_bounds = [[-175.0, 175.0]]
_rateCross = 0.9
_rateMut = 1.0/float(_nBits)
_nIter = 100

best = GA(_nBits, _bounds, _nK, _nIter, _populationSize, _rateCross, _rateMut)
print("Done!!!!")
printFunc(best.genome, _bounds, _nBits, _nK)






# print("Size of selected list = ", len(selected))


# maxFitness = 0
# for i in range(len(population)):
#     if(population[i].fitness > population[maxFitness].fitness):
#         maxFitness = i

# print("Max fitness at index: ", maxFitness)
# print("Fitness = ", population[maxFitness].fitness)
# funcTypes = getFuncTypes(population[maxFitness].genome, _nBits, _nK)
# decoded = decode(_bounds, _nBits, _nK, population[maxFitness].genome)
# fx = functionsDisp[funcTypes[0]]
# gx = functionsDisp[funcTypes[1]]

# hx = fx + gx
# print("H(x) = ", hx)

# print("Values are: ")
# for i in range(len(data)):
#     fx = functions[funcTypes[0]](decoded[0], decoded[1], decoded[2], decoded[3], data[i][0])
#     gx = functions[funcTypes[1]](decoded[4], decoded[5], decoded[6], decoded[7], data[i][0])
    
#     hx = (fx + gx).round(4)
#     fitness = 1/abs(hx - data[i][1])
#     print("Aprox = ", hx, " Real = ", data[i][1], "Value fitness = ", fitness)


