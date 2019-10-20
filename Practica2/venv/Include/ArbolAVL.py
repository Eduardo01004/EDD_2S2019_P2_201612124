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
        if nodo == None:
            return -1
        return nodo.altura

    def max(self,a,b):
        if a > b:
            return a
        else:
            return b

    def rotarizquierda(self,nodo):
        avlnodo=nodo.izquierdo
        nodo.izquierdo=avlnodo.derecho
        avlnodo.derecho=nodo
        nodo.altura = self.max(self.ObtenerFe(nodo.izquierdo), self.ObtenerFe(nodo.derecho) + 1)
        avlnodo.altura = self.max(self.ObtenerFe(avlnodo.izquierdo), self.ObtenerFe(avlnodo.derecho) + 1)
        return avlnodo

    def rotarderecha(self,nodo):
        avlnodo=nodo.derecho
        nodo.derecho=avlnodo.izquierdo
        avlnodo.izquierdo=nodo
        nodo.altura = self.max(self.ObtenerFe(nodo.izquierdo), self.ObtenerFe(nodo.derecho) + 1)
        avlnodo.altura = self.max(self.ObtenerFe(avlnodo.izquierdo), self.ObtenerFe(avlnodo.derecho) + 1)
        return avlnodo

    def rotarDobleIzq(self,nodo):
        avl=None
        nodo.izquierdo=self.rotarderecha(nodo.izquierdo)
        avl=self.rotarizquierda(nodo)
        return  avl

    def rotarDobleDer(self,nodo):
        avl=None
        nodo.derecho=self.rotarizquierda(nodo.derecho)
        avl=self.rotarderecha(nodo)
        return avl

    def insertar(self,nuevo,subA):
        nuevopadre=subA
        if nuevo.carne < subA.carne:
            if subA.izquierdo == None:
                subA.izquierdo = nuevo
            else:
                subA.izquierdo=self.insertar(nuevo,subA.izquierdo)
                if (self.ObtenerFe(subA.izquierdo) - self.ObtenerFe(subA.derecho)) == 2:
                    if nuevo.carne < subA.izquierdo.carne:
                        nuevopadre=self.rotarizquierda(subA)
                    else:
                        nuevopadre=self.rotarDobleIzq(subA)
        elif nuevo.carne > subA.carne:
            if subA.derecho == None:
                subA.derecho = nuevo
            else:
                subA.derecho=self.insertar(nuevo,subA.derecho)
                if (self.ObtenerFe(subA.derecho) - self.ObtenerFe(subA.izquierdo)) == 2:
                    if nuevo.carne > subA.derecho.carne:
                        nuevopadre=self.rotarderecha(subA)
                    else:
                        nuevopadre=self.rotarDobleDer(subA)

        if subA.izquierdo == None and subA.derecho != None:
            subA.altura=subA.derecho.altura+1
        elif subA.derecho == None and subA.izquierdo != None:
            subA.altura=subA.izquierdo.altura+1
        else:
            subA.altura=self.max(self.ObtenerFe(subA.izquierdo),self.ObtenerFe(subA.derecho))+1

        return  nuevopadre


    def insertartodo(self,carne,nombre):
        nuevo=NodoAVL(carne,nombre)
        if self.raiz == None:
            self.raiz=nuevo
        else:
            self.raiz=self.insertar(nuevo,self.raiz)

    def GraficarAVL(self):
        file = open("ArbolAVL.dot", "w")
        file.write("digraph ArbolAVL{\n rankdir=TB;\n")
        file.write(" graph [splines=compound, nodesep=0.5];\n")
        file.write("node [shape = record, style=filled, fillcolor=seashell2,width=0.7,height=0.2];\n")
        self.CodigoInterno(self.raiz,file)
        file.write("}\n")
        file.close()
        os.system("dot -Tpng ArbolAVL.dot -o ArbolAVL.png")
        os.system("ArbolAVL.png")

    def CodigoInterno(self, raiz,file):
        if raiz != None:
            self.CodigoInterno(raiz.izquierdo,file)
            Fe=self.ObtenerFe(raiz.izquierdo)-self.ObtenerFe(raiz.derecho)
            file.write(str(raiz.carne)+"[label=\"<C0>|Carne: "+str(raiz.carne)+"&#92;n Nombre: "+raiz.nombre + "&#92;n Altura: "+ str(raiz.altura)+"&#92;n FE: "+ str(Fe)+"|<C1>\"];\n")
            if raiz.derecho != None:
                file.write(str(raiz.carne) + "->" + str(raiz.derecho.carne)+"\n")
            if raiz.izquierdo != None:
                file.write(str(raiz.carne) + "->" + str(raiz.izquierdo.carne) + "\n")

            self.CodigoInterno(raiz.derecho,file)


    def InOrden(self,nodo):
        if nodo != None:
            self.InOrden(nodo.izquierdo)
            print(nodo.carne)
            self.InOrden(nodo.derecho)

    def PostOrden(self,raiz):
        if raiz != None:
            self.PostOrden(raiz.izquierdo)
            self.PostOrden(raiz.derecho)
            print(raiz.carne)
    
    def PreOrden(self,raiz):
        if raiz != None:
            print(raiz.carne)
            self.PostOrden(raiz.izquierdo)
            self.PostOrden(raiz.derecho)

    def Graph_Transversal(self,lista,name):
        file=open('{}.dot'.format(name),"w")
        file.write("digraph inorden {\nrankdir = LR;\n")
        i=0
        for i in range(len(lista)):
            file.write(str(i)+"[shape=record, style=filled, fillcolor=seashell2,label=\"Carnet:"+str(lista[i])+"\"];\n")
            file.write(str(i)+"->"+str(i+1)+"\n")

        file.write(str(i+1)+"[shape=record, style=filled, fillcolor=seashell2,label=\"Fin\"];\n")
        file.write("}\n")
        file.close()
        os.system('dot -Tpng {}.dot -o {}.png'.format(name,name))
        os.system('{}.png'.format(name))
    
    def Graph_Inorden(self, lista, raiz):
        if raiz != None:
            carnet=str(raiz.carne)
            name=raiz.nombre
            total='{}\\n{}'.format(carnet,name)
            self.Graph_Inorden(lista,raiz.izquierdo)
            lista.append(total)
            self.Graph_Inorden(lista,raiz.derecho)

    def Graph_PostOrden(self, lista, raiz):
        if raiz != None:
            carnet=str(raiz.carne)
            name=raiz.nombre
            total='{}\\n{}'.format(carnet,name)
            self.Graph_Inorden(lista,raiz.izquierdo)
            self.Graph_Inorden(lista,raiz.derecho)
            lista.append(total)
            

    def Graph_PreOrden(self, lista, raiz):
        if raiz != None:
            carnet=str(raiz.carne)
            name=raiz.nombre
            total='{}\\n{}'.format(carnet,name)
            lista.append(total)
            self.Graph_Inorden(lista,raiz.izquierdo)
            self.Graph_Inorden(lista,raiz.derecho)





if __name__=="__main__":
    arbol=ArbolAVL()
    lista=[]
    arbol.insertartodo(201403525,"Nery")
    arbol.insertartodo(201212963, "Andres")
    arbol.insertartodo(201005874, "Estudiante1")
    arbol.insertartodo(201313526, "Alan")
    arbol.insertartodo(201403819, "Anne")
    arbol.insertartodo(201403624, "Fernando")
    arbol.insertartodo(201602255, "Estudiante2")
    arbol.InOrden(arbol.raiz)
    arbol.GraficarAVL()
    arbol.Graph_Inorden(lista,arbol.raiz)
    arbol.Graph_Transversal(lista,'INORDEN')
