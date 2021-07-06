import matplotlib.pyplot as plt
from sympy import latex

def plotCurves(pReal, pAprox, pFunc):
    realX = [real[0] for real in pReal]
    realY = [real[1] for real in pReal]

    aproxX = [aprox[0] for aprox in pAprox]
    aproxY = [aprox[1] for aprox in pAprox]

    realPlot = plt.plot(realX, realY, label='Real data')
    aproxPlot = plt.plot(aproxX, aproxY, label='Aproximation')

    plt.title(latex(pFunc))
    plt.legend(loc="upper left")
    plt.show()