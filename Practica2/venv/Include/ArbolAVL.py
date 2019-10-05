import os

class NodoAVL:
    def __init__(self,carne,nombre):
        self.carne=carne
        self.nombre=nombre
        self.altura=0
        self.izquierdo=None
        self.derecho=None



class ArbolAVL:
    def __init__(self):
        self.raiz=None

    def ObtenerFe(self,nodo):
        if n == None:
            return -1
        return nodo.altura

    def max(self,a,b):
        if a > b:
            return a
        else:
            return b

    def rotarizquierda(self):
        avlnodo=nodo.izquierdo
        nodo.izquierdo=avlnodo.derecho
        avlnodo.derecho=nodo
        nodo.altura=max(ObtenerFe(nodo.izquierdo),ObtenerFe(n.derecho)+1)
        avlnodo.altura=max(ObtenerFe(nodo.izquierdo),ObtenerFe(n.derecho)+1)
        return avlnodo

    def rotarderecha(self,nodo):
        avl=nodo.derecho
        nodo.derecho=avlnodo.izquierdo
        avlnodo.izquierdo=nodo
        nodo.altura=max(ObtenerFe(nodo.izquierdo),ObtenerFe(n.derecho)+1)
        avlnodo.altura=max(ObtenerFe(nodo.izquierdo),ObtenerFe(n.derecho)+1)
        return avlnodo

    def rotarDobleIzq(self,nodo):
        avl=None
        nodo.izquierdo=rotarderecha(nodo.izquierdo)
        avl=rotarizquierda(nodo)
        return  avl

    def rotarDobleDer(self,nodo):
        avl=None
        nodo.derecho=rotarizquierda(nodo.derecho)
        avl=rotarderecha(nodo)
        return avl

    def insertar(self,nuevo,subA):
        nuevopadre=subA
        if nuevo < subA:
            if subA.izquierdo == None:
                subA.izquierdo = nuevo
            else:
                subA.izquierdo=insertar(nuevo,subA.izquierdo)
                if (ObtenerFe(subA.izquierdo) - ObtenerFe(subA.derecho)) == 2:
                    if nuevo < subA.izquierdo.carnet:
                        nuevopadre=rotarizquierda(subA)
                    else:
                        nuevopadre=rotarDobleIzq(subA)
        elif nuevo > subA:
            if subA.derecho==None:
                subA.derecho=nuevo
            else:
                subA.derecho=insertar(nuevo,subA.derecho)
                if (ObtenerFe(subA.derecho) - ObtenerFe(subA.izquierdo)) == 2:
                    if nuevo > subA.derecho.carnet:
                        nuevopadre=rotarderecha(subA)
                    else:
                        nuevopadre=rotarDobleDer(subA)

        if subA.izquierdo == None and subA.derecho != None:
            subA.altura=subA.derecho.altura+1
        elif subA.derecho == None and subA.izquierdo != None:
            subA.altura=subA.izquierdo.altura+1
        else:
            subA.altura=max(ObtenerFe(subA.izquierdo),ObtenerFe(subA.derecho))+1

        return  nuevopadre


    def insertartodo(self,carne,nombre):
        nuevo=NodoAVL(carne,nombre)
        if self.raiz == None:
            self.raiz=nuevo
        else:
            self.raiz=insertar(nuevo,self.raiz)


    def inorden(self,nodo):
        if nodo != None:
            inorden(nodo.izquierdo)
            print(nodo.carne)
            inorden(nodo.derecho)




if __name__=="__main__":
    arbol=ArbolAVL()
    arbol.insertar("1","3")
    arbol.inorden(arbol.raiz)














