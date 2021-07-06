from numpy import float128
import math

class Individual:
    lifeSpan = None
    genome = None
    fitness = None
    func_F = None
    func_G = None

    def __init__(self, pLifeSpan, pChromosome, pFuncF, pFuncG):
        self.lifeSpan = pLifeSpan
        self.genome = pChromosome
        self.func_F = pFuncF
        self.func_G = pFuncG

    def decode(self, pBounds, pNbits, pNk):
        decoded = list()
        largest = 2**pNbits
        for i in range(pNk*2):
            start, end = i * pNbits, (i * pNbits) + pNbits
            substring = self.genome[start:end]

            chars = "".join([str(s) for s in substring])
            integer = int(chars, 2)
            value = pBounds[0][0] + (integer/largest) * (pBounds[0][1] - pBounds[0][0])
            decoded.append(round(value, 8))
        return decoded

    def calcFitness(self, pFunctions, pData, pBounds, pNbits, pNk):
        decoded = self.decode(pBounds, pNbits, pNk)
        self.fitness = 0

        tmp = 0
        for i in range(len(pData)):
            # fx = pFunctions[self.func_F](decoded[0], decoded[1], 
            #     decoded[2], decoded[3], pData[i][0])
            # gx = pFunctions[self.func_G](decoded[4], decoded[5], 
            #     decoded[6], decoded[7], pData[i][0])
            fx = pFunctions[self.func_F](float128(decoded[0]), float128( decoded[1]), 
                float128(decoded[2]), float128(decoded[3]), float128(pData[i][0]))
            gx = pFunctions[self.func_G](float128(decoded[4]), float128( decoded[5]), 
                float128(decoded[6]), float128(decoded[7]), float128(pData[i][0]))

            hx = fx + gx
            tmp += (pData[i][1] - hx)**2
        
        #Root-mean-square deviation
        #Minimum fitness (best): 0
        #Maximun fitness (worst): inf
        self.fitness = math.sqrt(tmp/len(pData)) 