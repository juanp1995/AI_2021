import numpy as np
from random import randint
k1f=0
k2f=32
k3f=64
k4f=96
k1g=128
k2g=160
k3g=192
k4g=224

def mutar(genoma, posibilidad):
    lista=list(genoma)#se pasa a lista
    muta=np.random.choice([0,1], 1, p=[(1-posibilidad), posibilidad]) #muta
    if muta:
        am=randint(0,255)
        if int(lista[am]):
            lista[am]='0'
            return genoma 
        else:
            lista[gen]='1'
    genoma=''.join(lista)
    return genoma    
