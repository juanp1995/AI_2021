from numpy import float128
import math

class Individual:
    lifeSpan = None
    genome = None
    fitness = None

    def __init__(self, pLifeSpan, pGenome):
        self.lifeSpan = pLifeSpan
        self.genome = pGenome

    def decode(self, pBounds, pNbits, pNk):
        decoded = list()
        largest = 2**pNbits

        #Decode function type
        binFuncF, binFuncG = self.genome[0:3], self.genome[(pNbits*pNk)+3:(pNbits*pNk)+6]
        funcF = int("".join([str(s) for s in binFuncF]), 2)
        funcG = int("".join([str(s) for s in binFuncG]), 2)
        decoded.append(funcF)
        decoded.append(funcG)

        #Decode value of Ks
        offset = 3 #First 3 bits encondig function F
        for i in range(pNk*2):
            if i >= pNk:
                offset = 6 #3 bits of function F and 3 of G

            start, end = (i * pNbits)+offset, (i * pNbits) + pNbits + offset
            substring = self.genome[start:end]

            chars = "".join([str(s) for s in substring])
            integer = int(chars, 2)
            value = pBounds[0][0] + (integer/largest) * (pBounds[0][1] - pBounds[0][0])
            decoded.append(round(value, 8))
        return decoded

    def calcFitness(self, pFunctions, pData, pBounds, pNbits, pNk):
        decoded = self.decode(pBounds, pNbits, pNk)
        funcF = decoded[0]
        funcG = decoded[1]
        self.fitness = 0

        tmp = 0
        for i in range(len(pData)):
            fx = pFunctions[funcF](float128(decoded[2]), float128( decoded[3]), 
                float128(decoded[4]), float128(decoded[5]), float128(decoded[6]), float128(pData[i][0]))
            gx = pFunctions[funcG](float128(decoded[7]), float128(decoded[8]), 
                float128(decoded[9]), float128(decoded[10]), float128(decoded[11]), float128(pData[i][0]))

            hx = fx + gx
            error = float128(pData[i][1] - hx)
            squareError = error * error
            tmp += squareError
        
        #Root-mean-square deviation
        #Minimum fitness (best): 0
        #Maximun fitness (worst): inf
        self.fitness = float128(math.sqrt(tmp/len(pData))) 