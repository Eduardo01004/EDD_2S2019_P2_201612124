import os

class Nodo:
    def __init__(self,carne):
        self.carne=carne
        self.siguiente=None

class Recorrido:
    def __init__(self):
        self.primero=None
        self.ultimo=None
    
    def Buscar(self, carne):
        aux = self.primero
        while aux != None:
            if aux.carne == carne:
                return aux
        return None

    def Inorden(self,carne):
        nuevo=Nodo(carne)
        if self.primero == None:
            self.primero = nuevo
            self.primero.siguiente=None
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.siguiente = None
            self.ultimo = nuevo
        

    def GraficarInorden(self):
        file = open("RecorridoInorden.dot", "w")
        file.write("digraph inorden {\nrankdir = LR;\n")
        aux = self.primero
        if aux != None:
            while aux != None:
                aux2=aux.siguiente
                point = str(hash(aux))
                file.write(point+"[shape=record, style=filled, fillcolor=seashell2,label=\"Imagen:"+str(aux.carne)+"\"];\n")
                if aux2 != None:
                    point2 = str(hash(aux2))
                    file.write(point+"->"+point2+"\n")
                aux=aux.siguiente
            file.write("}\n")
            file.close()
            os.system("dot -Tpng RecorridoInorden.dot -o RecorridoInorden.png")
            os.system(" RecorridoInorden.png")
    

    def Postorden(self,carne):
        nuevo=Nodo(carne)
        if self.primero == None:
            self.primero = nuevo
            self.primero.siguiente=None
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.siguiente = None
            self.ultimo = nuevo
        

    def GraficarPostorden(self):
        file = open("RecorridoPostorden.dot", "w")
        file.write("digraph PostOrden {\nrankdir = LR;\n")
        aux = self.primero
        if aux != None:
            while aux != None:
                aux2=aux.siguiente
                point = str(hash(aux))
                file.write(point+"[shape=record, style=filled, fillcolor=seashell2,label=\"Imagen:"+str(aux.carne)+"\"];\n")
                if aux2 != None:
                    point2 = str(hash(aux2))
                    file.write(point+"->"+point2+"\n")
                aux=aux.siguiente
            file.write("}\n")
            file.close()
            os.system("dot -Tpng RecorridoPostorden.dot -o RecorridoPostordenpng")
            os.system(" RecorridoPostorden.png")

    def Preorden(self,carne):
        nuevo=Nodo(carne)
        if self.primero == None:
            self.primero = nuevo
            self.primero.siguiente=None
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.siguiente = None
            self.ultimo = nuevo
        

    def GraficarPreorden(self):
        file = open("RecorridoPreorden.dot", "w")
        file.write("digraph RecorridoPreorden {\nrankdir = LR;\n")
        aux = self.primero
        if aux != None:
            while aux != None:
                aux2=aux.siguiente
                point = str(hash(aux))
                file.write(point+"[shape=record, style=filled, fillcolor=seashell2,label=\"Imagen:"+str(aux.carne)+"\"];\n")
                if aux2 != None:
                    point2 = str(hash(aux2))
                    file.write(point+"->"+point2+"\n")
                aux=aux.siguiente
            file.write("}\n")
            file.close()
            os.system("dot -Tpng RecorridoPreorden.dot -o RecorridoPreorden.png")
            os.system(" RecorridoPreorden.png")


    

