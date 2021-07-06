import threading, time
from sympy.interactive.printing import init_printing
from Plot import plotCurves
from Functions import *
from Plot import *

_exit = False

def GA(pNbits, pBounds, pNk, pPopSize, pAttempts, pRcross, pRmut, pLifeSpan):
    global _exit

    population = []
    data = readData('../x.txt', '../f.txt')

    bestIndividuals = list()
    
    for attempt in range(pAttempts):
        if _exit:
            break

        population = initialPopulation(pPopSize, pLifeSpan, pNbits, pNk)

        best, currentBest = population[0], population[0]
        prevAvgFitness, avgFitness = 0, 0
        gen = 0

        while True:
        # for _ in range(50):
            if _exit:
                break

            #Calculate fitness of each individual
            [individual.calcFitness(functions, data, pBounds, pNbits, pNk) for individual in population]

            for individual in population:
                individual.lifeSpan -= 1

            # print("POPULATION ORIGINAL SIZE: ", len(population))

            if gen != 0:
                earlyTermination(population)

            # print("POPULATION SIZE AFTER EARLY TERMINATION: ", len(population))

            if len(population) > pPopSize:
                population = sorted(population, key=lambda x: x.fitness, reverse=False)
                population = population[:pPopSize]

            currentBest = min(population, key=lambda x: x.fitness)
            if currentBest.fitness < best.fitness:
                best = currentBest

            #Print info
            if gen%5 == 0:
                print("-- Generation ", gen)
                printFunc(currentBest, pBounds, pNbits, pNk)

            #Detect stagnation in the population
            prevAvgFitness = sum(population[i].fitness for i in range(len(population)))
            prevAvgFitness /= len(population)
            if abs(prevAvgFitness - avgFitness) < 0.0001:
                print("--- NO MORE IMPROVEMENT!!!")
                print("--- Best solution found after ", gen, "generations: ")
                printFunc(best, pBounds, pNbits, pNk)
                print("\n")
                bestIndividuals.append(best)
                break
            avgFitness = prevAvgFitness            
            
            #Selection of individuals
            selected = rouletteSelection(population)

            #Crossover and mutation
            offspring = list()
            for i in range(0, pPopSize, 2):
                p1, p2 = selected[i], selected[i+1]
                #Crossover and mutation
                for c in crossover(p1, p2, pNbits, pNk, pRcross, pLifeSpan):
                    mutation(c, pNbits, pNk, pRmut)
                    offspring.append(c)

            #Replace population
            population = selected + offspring

            gen += 1
        #End while
    #End for

    if len(bestIndividuals) > 0:
        if _exit:
            print("--- Execution stopped!")
        print("\n Best individuals of ", pAttempts, " attempts")
        for ind in bestIndividuals:
            printFunc(ind, pBounds, pNbits, pNk)

        solution = min(bestIndividuals, key=lambda x: x.fitness) 

        print("\n -- Solution found: ")
        found = printFunc(solution, pBounds, pNbits, pNk)

        #Generate data for plot
        decoded = solution.decode(pBounds, pNbits, pNk)
        funcF = decoded[0]
        funcG = decoded[1]
        aproxData = list()
        for i in range(len(data)):

            fx = functions[funcF](float128(decoded[2]), float128( decoded[3]), 
                    float128(decoded[4]), float128(decoded[5]), float128(decoded[6]), float128(data[i][0]))
            gx = functions[funcG](float128(decoded[7]), float128(decoded[8]), 
                float128(decoded[9]), float128(decoded[10]), float128(decoded[11]), float128(data[i][0]))

            hx = fx + gx
            aproxData.append([data[i][0], hx])

        plotCurves(data, aproxData, found)
        _exit = True
        return solution

    else:
        print("\n --- Execution terminated!")



"""
Listens for user input
Press "q" to stop execution
"""
def userInput():
    global _exit

    while not _exit:
        string = input("")
        if string == 'q':
            _exit = True
       


def main():
    _populationSize = 200
    _attempts = 5               #Numbers of functions tested
    _nBits = 8                  #Size in bits of each K
    _nK = 5
    _bounds = [[-40.0, 40.0]]
    _rateCross = 0.95           #Crossover probability
    _rateMut = 0.1              #Mutation probability
    _lifeSpan = 3               

    #Thread to listen for user input (to stop execution)
    thread = threading.Thread(target=userInput)
    thread.setDaemon(True)
    thread.start()

    best = GA(_nBits, _bounds, _nK, _populationSize, _attempts, _rateCross, _rateMut, _lifeSpan)


if __name__ == "__main__":
    main()



