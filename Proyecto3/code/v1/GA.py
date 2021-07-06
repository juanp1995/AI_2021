from sympy.interactive.printing import init_printing
from Plot import plotCurves
from Functions import *
from Plot import *

def GA(pNbits, pBounds, pNk, pIter, pPopSize, pCandidates, pRcross, pRmut, pLifeSpan):
    population = []
    data = readData('../x.txt', '../f.txt')

    #Create random initial population
    population = initialPopulation(pPopSize, pCandidates, pLifeSpan, pNbits, pNk)
    # for _ in range(pPopSize):
    #     fx = int(random.uniform(0, 8))
    #     gx = int(random.uniform(0, 8))
    #     newIndividual = Individual(pLifeSpan, randomGenome(pNbits, pNk), fx, gx)
    #     population.append(newIndividual)

    best, newBest = population[0], population[randint(0, pPopSize)]

    for gen in range(pIter):
        #Calculate fitness
        totalFitness = 0
        [individual.calcFitness(functions, data, pBounds, pNbits, pNk) for individual in population]

        #Sort population by fitness
        population = sorted(population, key=lambda x: x.fitness, reverse=False)
        #If population is bigger (due to previous iteration)
        #remove the individuals with lower fitness
        if len(population) > pPopSize:
            population = population[:pPopSize]

        # for ind in population:
        #     totalFitness += 1/ind.fitness
        # for ind in population:
        #     ind.probability = (1/ind.fitness) / totalFitness

        # print("INITITAL POPULATION: ")
        # [printFunc(ind, pBounds, pNbits, pNk) for ind in population]

        #Check new best solution
        # print("\n BEST: ")
        newBest = getNewBest(population)
        if newBest.fitness < best.fitness:
            best = Individual(newBest.lifeSpan, newBest.genome, newBest.func_F, newBest.func_G)
            best.fitness = newBest.fitness
        printFunc(best, pBounds, pNbits, pNk)
        
        # print("\n SELECTED POPULATION: ")
        # [printFunc(ind, pBounds, pNbits, pNk) for ind in selected]

        #Select parents
        # selected = [selection(population) for _ in range(pPopSize)]
        selected = rouletteSelection(population, pCandidates)
        #Create next generation

        newPop = list()
        newPop = newPop + selected
        for i in range(0, pPopSize, 2):
            p1, p2 = selected[i], selected[i+1]
            if p1.func_F == p2.func_F and p1.func_G == p2.func_G:
                #Crossover and mutation
                for c in crossover(p1, p2, pRcross):
                    mutation(c, pRmut)
                    newPop.append(c)
        

        #Replace population
        population = newPop

    print("Done!!!!")
    found = printFunc(best, pBounds, pNbits, pNk)

    #Generate data for plot
    decoded = best.decode(pBounds, pNbits, pNk)
    aproxData = list()
    for i in range(len(data)):
        fx = functions[newBest.func_F](float128(decoded[0]), float128( decoded[1]), 
            float128(decoded[2]), float128(decoded[3]), float128(data[i][0]))
        gx = functions[newBest.func_G](float128(decoded[4]), float128( decoded[5]), 
            float128(decoded[6]), float128(decoded[7]), float128(data[i][0]))

        hx = fx + gx
        aproxData.append([data[i][0], hx])

    plotCurves(data, aproxData, found)
    return best


_populationSize = 4000
_candidates = 5
_nBits = 32
_nK = 4
_bounds = [[-20.0, 20.0]]
_rateCross = 0.95
_rateMut = 0.1
_lifeSpan = 5
_nIter = 150

best = GA(_nBits, _bounds, _nK, _nIter, _populationSize, _candidates, _rateCross, _rateMut, _lifeSpan)
