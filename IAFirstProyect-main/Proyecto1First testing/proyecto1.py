#imports
import networkx as nx
import tkinter as tk
import numpy as np
import view
from time import sleep 


posiciones={}
tablero=[]
global lista_nodo_bloqueado
global lista_nodo_abierto
global lista_de_tableros
lista_nodo_bloqueado =[]
lista_nodo_abierto =[]
lista_de_tableros =[]

class Nodo:
    def __init__(self, num):
        self.pos=num
        self.posXY=[0,0]
        self.padre=0
        self.matriz=np.zeros((6,6))
        self.G=0
        self.H=5
        self.F=self.G+self.H
        self.vecinos=[]
        self.bloq=[]
        

    def setPadre(self,num):
        self.padre=num
    
    def setG(self,num): #coste del camino de la casilla hasta donde estoy
        self.G=num

    def setH(self,num): #coste del nodo en el que estoy hasta el objetivo
        self.H=num

    def calcF(self):
        self.F=self.G+self.H
        if self.pos==1 or self.pos==6 or self.pos==31 or self.pos==36:
            self.F=self.F+10

    def calcposXY(self):
        self.posXY=posiciones[self.pos]

    def calcBloq(self):   #Lo que hace es calcular cuales son las casillas que el nodo actual bloquea
        if (self.pos==0):
            self.bloq=[]
        else:
            for x in range (1,37):
                if (posiciones[x][0]==self.posXY[0] or posiciones[x][1]==self.posXY[1]):
                    self.bloq.append(x)
                else:
                    var=posiciones[x]
                    x1=abs(var[0]-self.posXY[0])
                    y1=abs(var[1]-self.posXY[1])
                    if (x1==y1):
                        self.bloq.append(x)

    def calcVecinos(self):
        if (self.pos==0):
            self.vecinos=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
        else:
            for x in range (1,37):
                if x not in self.bloq and x not in self.vecinos:
                    self.vecinos.append(x)

    
    def calcMatriz(self):
        self.matriz[self.posXY[0]][self.posXY[1]]=1





def main():
    cuadricula=np.zeros((6,6))
    genDicc()
    #Creación del grafo
    Grafo = nx.Graph()
    Grafo.add_node(Nodo(0))
    list(Grafo)[0].setG(0)
    list(Grafo)[0].calcBloq()
    list(Grafo)[0].calcVecinos()
    for x in range(1,37):
        Grafo.add_node(Nodo(x))

    for x in range(1,37):
        list(Grafo)[x].calcposXY()
        list(Grafo)[x].calcBloq()
        list(Grafo)[x].calcVecinos()
        list(Grafo)[x].setG(len(list(Grafo)[x].bloq))
        list(Grafo)[x].calcF()
        list(Grafo)[x].calcMatriz()
    AEstrella(Grafo)

def setEdges(grf):
    for x in range(37):
        var=list(Grafo)[x]

#Diccionario de posiciones
def genDicc():
    var=1
    x=0
    y=2
    for x in range(6):
        for y in range(6):
            posiciones.setdefault(var,[x,y])
            var+=1

def buscarpos(posXY):
    for pos in posiciones:
        if (posiciones[pos]==posXY):
            return pos

def menor(grafo,lista):#retorna el indice del nodo con menor F en el grafo
    var=lista[0]
    for ele in lista:
        if list(grafo)[ele].F<list(grafo)[var].F:
            var=ele
    return var

def calcNewG(nodo,vecino):
    newg=nodo.G
    if vecino.posXY[0]==(nodo.posXY[0]):
        newg=nodo.G
    if vecino.posXY[0]==(nodo.posXY[0]+1):
        newg=nodo.G+10
        if nodo.pos==0:
            newg=nodo.G+11
        else:
            if (vecino.posXY[1])<=(nodo.posXY[1]+2):
                newg=newg-1
    if vecino.posXY[0]==(nodo.posXY[0]+2):
        newg=nodo.G+21
    if vecino.posXY[0]==(nodo.posXY[0]+3):
        newg=nodo.G+31
    if vecino.posXY[0]==(nodo.posXY[0]+4):
        newg=nodo.G+41
    if vecino.posXY[0]==(nodo.posXY[0]+5):
        newg=nodo.G+51
    if vecino.posXY[0]==(nodo.posXY[0]+6):
        newg=nodo.G+61
    if nodo.pos==0:
        newg=newg+10
    return newg

def calcNewH(nodo,vecino):
    newh=0
    for bloque in vecino.bloq:
        if bloque not in nodo.bloq:
           newh=newh+1
    return newh

def defRuta(nodo,grafo):
    ruta=[nodo.pos]
    var1=nodo
    for x in range(6):
        var2=var1.padre
        ruta.append(var2)
        var1=list(grafo)[var2]
    return ruta

def rutaParcial(nodo,grafo):  #genera una ruta parcial
    ruta = [nodo.pos]
    var1 = nodo
    while var1.pos != 0:
        var2=var1.padre
        ruta.append(var2)
        var1=list(grafo)[var2]
    return ruta

def crearTablero(ruta):
    global tablero
    num = len(ruta)-2
    print(num)
    for x in range(6):
        lista=[]
        for y in range(6):
            var=[x,y]
            posi=ruta[num]
            if buscarpos(var)==posi:
                lista.append("Q")
                num=num-1
            else:
                lista.append("0")
        tablero.append(lista)
    print(tablero)

def crearTablero2(ruta,grafo):
    global tablero
    tablero = []
    num = len(ruta)-2
    for x in range(6):
        lista=[]
        for y in range(6):
            var=[x,y]
            posi=ruta[num]
            if buscarpos(var)==posi:
                lista.append("Q")
                num=num-1
            else:
                varComoSea = list(grafo)[buscarpos(var)].F
                lista.append(str(varComoSea))
        tablero.append(lista)



def AEstrella(grf):
    fin=False
    cerrado=[0]
    abierto=list(grf)[0].vecinos
    ruta=[]
    for veci in list(grf)[0].vecinos: ##tablero vacio todos son los vecinos calcula H y G y setea a todo el tablero
        G=calcNewG(list(grf)[0],list(grf)[veci])
        H=calcNewH(list(grf)[0],list(grf)[veci])
        list(grf)[veci].setG(G) #cuando accede "veci" es el numero de posicion del vecino 
        list(grf)[veci].setH(H)
        list(grf)[veci].calcF()

    while not fin: #
        if len(abierto)==0: #si ya no hay abiertos   #Nota No usar para interfaz
            ruta=defRuta(list(grf)[men],grf)
            print(ruta)
            crearTablero(ruta)
            break
        men=menor(grf,abierto) # Calcula en el grupo de los abiertos el menor F

        for vec in list(grf)[men].vecinos: #Los vecinos de la casilla del grafo de menor F se analizan      
            newG=calcNewG(list(grf)[men],list(grf)[vec]) #se calcula el nuevo G 
            if newG<list(grf)[vec].G: #si el nuevo G es menor se actualiza el G y H, y se coloca el nuevo padre
                list(grf)[vec].setG(newG)
                list(grf)[vec].setH(calcNewH(list(grf)[men],list(grf)[vec]))
                list(grf)[vec].setPadre(men)
                list(grf)[vec].calcF() #se recalcula F
                list(grf)[vec].bloq=[] #Hace un append que quita todos los bloqueados y se vuelven a poner vacios
                list(grf)[vec].calcBloq() #bloqueamos los correspondientes al nodo actual
                
                for bloque in list(grf)[men].bloq: #Se toman los bloqueados desde el nodo padre y se le colocan al hijo
                    if bloque not in list(grf)[vec].bloq: #Si no se encuentra en la lista de bloqueados del hijo se agregan (validacion para evitar duplicados)
                        list(grf)[vec].bloq.append(bloque) #se agregan bloqueados no repetidos
                        if bloque in list(grf)[vec].vecinos:    #si el bloque es un vecino del hijo se quita de la lista de vecinos del hijo  
                            list(grf)[vec].vecinos.remove(bloque) #se quita el nodo bloqueado de la lista de vecinos
                    list(grf)[vec].calcVecinos() #se actualizan los vecinos
                    list(grf)[vec].bloq.sort() #ordenamos la lista
                    list(grf)[vec].vecinos.sort() #ordenamos la lista
            
        ruta = rutaParcial(list(grf)[men],grf)
        crearTablero2(ruta,grf)
        lista_nodo_bloqueado.append(list(grf)[men].bloq);
        lista_nodo_abierto.append(list(grf)[men].vecinos);
        lista_de_tableros.append(tablero)
        
        


        if men in abierto:
            abierto.remove(men)#se elimina de la lista de abiertos
            cerrado.append(men)#se incluye a la lista de cerrados
            if list(grf)[men].posXY[0]==5:
                ruta=defRuta(list(grf)[men],grf)
                crearTablero2(ruta,grf)
                fin=True


main()
root = tk.Tk()

app = view.Application(master=root,Matrix=lista_de_tableros,open_nodes = lista_nodo_abierto,close_nodes = lista_nodo_bloqueado)

app.mainloop()



