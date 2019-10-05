import os

class NodoBlock:
    def __init__(self,indice,timestamp,Class,prevHash,Hash):
        self.indice=0
        self.timestamp=timestamp
        self.Class=Class
        self.prevhash=prevHash
        self.Hash=Hash
        self.siguiente=None
        self.atras=None

class BlockChain:
    def __init__(self):
        self.primero=None
        self.ultimo=None

    def Insertar(self, indice,timestamp,Class,prevHash,Hash):
        nuevo = NodoBlock(indice,timestamp,Class,prevHash,Hash)
        if self.primero == None:
            self.primero = nuevo
            self.primero.siguiente = None
            self.primero.atras = None
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.siguiente = None
            nuevo.atras = self.ultimo
            self.ultimo = nuevo

    def GraficarDobleSnake(self):
        file = open("ListaBloques.dot", "w")
        file.write("digraph G { \n")
        auxiliar = self.primero
        if self.primero != None:
            while (auxiliar != None):
                aux2 = auxiliar.siguiente
                if auxiliar != self.ultimo:
                    c = str(hash(auxiliar))
                    ca = str(hash(aux2))
                    file.write( c + "[shape=record, style=filled, fillcolor=seashell2,label=\"" + "Class= " + auxiliar.Class + " &#92;n TimeStamp= " + str( auxiliar.timestamp) + "&#92;n PHASH= " + str(auxiliar.prevhash) + "&#92;n HASH= " + str(auxiliar.Hash) + "\"];\n")
                    file.write(c + "->" + ca + "\n")
                    file.write(ca + "->" + c + "\n")

                elif auxiliar == self.primero or auxiliar == self.ultimo:
                    c = str(hash(auxiliar))
                    file.write(
                        c + "[shape=record, style=filled, fillcolor=seashell2,label=\"" + "Class= " + auxiliar.Class + " &#92;n TimeStamp= " + str(
                            auxiliar.timestamp) + "&#92;n PHASH= " + str(auxiliar.prevhash) + "&#92;n HASH= " + str(
                            auxiliar.Hash) + "\"];\n")
                auxiliar = auxiliar.siguiente
        file.write("}\n")
        file.close()
        os.system("dot -Tpng ListaBloques.dot -o ListaBloques.png")
        os.system(" ListaBloques.png")


if __name__=="__main__":
    bloque=BlockChain()
    bloque.Insertar(0,"15-15-15","EDD",0000,000)
    bloque.GraficarDobleSnake()