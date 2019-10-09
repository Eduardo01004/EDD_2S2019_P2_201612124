import os
import hashlib
import json
from ArbolAVL import NodoAVL,ArbolAVL

class NodoBlock:
    def __init__(self,INDEX,TIMESTAMP,CLASS,DATA,PREVIOUSHASH,HASH):
        self.INDEX=INDEX
        self.TIMESTAMP=TIMESTAMP
        self.CLASS=CLASS
        self.DATA=DATA
        self.PREVIOUSHASH=PREVIOUSHASH
        self.HASH=HASH
        self.arbol=ArbolAVL()
        self.siguiente=None
        self.atras=None

class BlockChain:
    def __init__(self):
        self.primero=None
        self.ultimo=None

    def Insertar(self,INDEX,TIMESTAMP,CLASS,DATA,PREVIOUSHASH,HASH):
        nuevo = NodoBlock(INDEX,TIMESTAMP,CLASS,DATA,PREVIOUSHASH,HASH)
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

    def GraficarBloque(self):
        file = open("ListaBloques.dot", "w")
        file.write("digraph G { \n")
        auxiliar = self.primero
        if self.primero != None:
            while (auxiliar != None):
                aux2 = auxiliar.siguiente
                if auxiliar != self.ultimo:
                    c = str(hash(auxiliar))
                    ca = str(hash(aux2))
                    file.write( c + "[shape=record, style=filled, fillcolor=seashell2,label=\""+"INDEX: "+str(auxiliar.INDEX) + "&#92;n Class= " + auxiliar.CLASS + " &#92;n TimeStamp= " + auxiliar.TIMESTAMP + "&#92;n PHASH= " + auxiliar.PREVIOUSHASH + "&#92;n HASH= " + auxiliar.HASH + "\"];\n")
                    file.write(c + "->" + ca + "\n")
                    file.write(ca + "->" + c + "\n")
                elif auxiliar == self.primero or auxiliar == self.ultimo:
                    c = str(hash(auxiliar))
                    file.write( c + "[shape=record, style=filled, fillcolor=seashell2,label=\"" +"INDEX: "+str(auxiliar.INDEX)+ " &#92;n Class= " + auxiliar.CLASS + " &#92;n TimeStamp= " + auxiliar.TIMESTAMP + "&#92;n PHASH= " + auxiliar.PREVIOUSHASH + "&#92;n HASH= " + auxiliar.HASH + "\"];\n")
                auxiliar = auxiliar.siguiente
        file.write("}\n")
        file.close()
        os.system("dot -Tpng ListaBloques.dot -o ListaBloques.png")
        os.system(" ListaBloques.png")


if __name__=="__main__":
    bloque=BlockChain()
    bloque.Insertar(0,"15-15-15","EDD","popo","skldksal","ksapqoq")
    bloque.Insertar(1,"14-14-14","COMPI","popo","skldksal","ksapqoq")
    bloque.Insertar(2,"12-12-12","ORGA","popo","skldksal","ksapqoq")
    bloque.Insertar(3,"11-11-11","IO","popo","skldksal","ksapqoq")
    m = hashlib.sha256()
    q="028-09-2019::10-50-25Estructuras"
    a="0000"
    p="""{"value":"201403525-Nery", "left":{"value":"201212963-Andres", "left":{"value":"201005874-Estudiante1", "left":null, "right":null}, "right":{"value":"201313526-Alan", "left":null, "right":null}}, "right":{"value":"201403819-Anne", "left":{"value":"201403624-Fernando", "left":null, "right":null}, "right":{"value":"201602255-Estudiante2", "left":null, "right":null}}}"""
    #my_str_as_bytes = str.encode(q+p+a)
    #m.update(my_str_as_bytes)
    #print(m.hexdigest())
    #bloque.Insertar(4,"11-11-11","IO",str(m.hexdigest()),str(m.hexdigest()),"ksapqoq")
    #bloque.GraficarBloque()
    c=json.dumps(p,sort_keys=True, indent=4)
    data=json.loads(p)
    popo=""
    pito=""
    print(json.dumps(p,sort_keys=True, indent=4))

        
    #print(popo)
        