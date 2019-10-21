import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import csv
import time
import datetime
import hashlib
import json
import socket
import select
import sys
import threading
from Blockchain import NodoBlock, BlockChain
from ArbolAVL import NodoAVL,ArbolAVL
bloque=BlockChain()

index=0
clase=""
timestamp=""
cadenajson=""
salida=""
prevhash=""
Hash=""
codificar=hashlib.sha256()
flag_send=False
username=""
selectblock=0
inorden=""
postorden=""
preorden=""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:  #verifica cuando se ejecuta el programa con 3 argumentos
	print ("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port)) #inicia el cliente

def Menu_Principal(window):
    Titulo(window,'Main Menu')
    window.addstr(8,21, '1. Insert Block')
    window.addstr(9,21, '2. Select Block')
    window.addstr(10,21, '3. Reports')
    window.addstr(11,21, '4. Exit')
    window.timeout(-1)
def Menu_Reports(window):
    Titulo(window,'Reports')
    window.addstr(10,21, '1. BlockChain Report')
    window.addstr(11,21, '2. Tree Reports')
    window.addstr(12,21, '3. Exit')

def Select_Reports(window):
    window.clear()
    Menu_Reports(window)
    keystroke = -1
    while(keystroke==-1):
        keystroke = window.getch()
        if(keystroke==49): #1
            bloque.GraficarBloque()
            keystroke=-1
        elif(keystroke==50):
            select_Report_Tree(window)
            TeclaESC(window)
            Menu_Reports(window)
            keystroke=-1
        elif(keystroke==51):
            Menu_Principal(window)
        else:
            keystroke=-1
    window.refresh()

def select_Report_Tree(window):
    window.clear()
    Sub_Menu_Tree(window)
    keystroke = -1
    while(keystroke==-1):
        keystroke = window.getch()
        if(keystroke==49): #1 avl
            bloc=bloque.Buscar(selectblock)
            if bloc != None:
                bloc.arbol.GraficarAVL()
            else:
                print("Vacio")
            TeclaESC(window)
            Sub_Menu_Tree(window)
            keystroke=-1
        elif(keystroke==50):#2 preorden
            bloc=bloque.Buscar(selectblock)
            if bloc != None:
                lista=[]
                global preorden
                bloc.arbol.Graph_PreOrden(lista,bloc.arbol.raiz)
                bloc.arbol.Graph_Transversal(lista,'PREORDEN')
                Titulo(window,'PREORDEN')
                Show_PreOrden(window,bloc.arbol.raiz)
                window.addstr(5,4,"inicio ->"+preorden+"Fin")
                preorden=""
            else:
                print("Vacio")
            TeclaESC(window)
            Sub_Menu_Tree(window)
            keystroke=-1
        elif(keystroke==51):#3 postorden
            bloc=bloque.Buscar(selectblock)
            if bloc != None:
                lista=[]
                global postorden
                bloc.arbol.Graph_PostOrden(lista,bloc.arbol.raiz)
                bloc.arbol.Graph_Transversal(lista,'POSTORDEN')
                Titulo(window,'POSTORDEN')
                Show_PostOrden(window,bloc.arbol.raiz)
                window.addstr(5,4,"inicio ->"+postorden+"Fin")
                postorden=""
            else:
                print("Vacio")
            TeclaESC(window)
            Sub_Menu_Tree(window)
            keystroke=-1
        elif(keystroke==52):#4 inorden
            bloc=bloque.Buscar(selectblock)
            if bloc != None:
                lista=[]
                global inorden
                window.clear()
                bloc.arbol.Graph_Inorden(lista,bloc.arbol.raiz)
                bloc.arbol.Graph_Transversal(lista,'INORDEN')
                Titulo(window,'INORDEN')
                Show_Tree(window,bloc.arbol.raiz)
                window.addstr(5,4,"inicio ->"+inorden+"Fin")
                inorden=""
            else:
                print("Vacio")
            TeclaESC(window)
            Sub_Menu_Tree(window)
            keystroke=-1
        elif(keystroke==53):# exit
            Menu_Reports(window)
        else:
            keystroke=-1
    window.refresh()


def Sub_Menu_Tree(window):
    Titulo(window,'Tree Reports')
    window.addstr(10,21, '1. Tree Report')
    window.addstr(11,21, '2. PreOrden')
    window.addstr(12,21, '3. PostOrden')
    window.addstr(13,21, '4. Inorden')
    window.addstr(14,21, '5. Exit')

def Pedir_Dato(screen):
    curses.echo()
    curses.curs_set(True)
    screen.addstr(13, 5, "Ingrese el index")
    jugador = screen.getstr()
    curses.curs_set(False)
    screen.clear()
    return jugador


def Titulo(window,var):
    window.clear()
    window.border()
    centro = round((60-len(var))/2)
    window.addstr(0,centro,var)

def TeclaESC(window):
    tecla=window.getch()
    while tecla!=27:
        tecla = window.getch()

def Seleccion():
    curses.initscr()
    window = curses.newwin(20,60,0,0)
    window.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    Menu_Principal(window)
    keystroke = -1
    while keystroke == -1:
        keystroke = window.getch()
        if(keystroke==49):
            Titulo(window, ' Insert Block ')
            LeerArchivo(window)
            TeclaESC(window)
            Menu_Principal(window)
            keystroke = -1
        elif(keystroke==50):
            Titulo(window, ' Select Block ')
            Menu_Bloque(window)
            TeclaESC(window)
            Menu_Principal(window)
            keystroke = -1
        elif(keystroke==51):
            Titulo(window,' Reports')
            Select_Reports(window)
            TeclaESC(window)
            Menu_Principal(window)
            keystroke = -1
        elif(keystroke==52):
            pass
        else:
            keystroke=-1
    curses.endwin()

def LeerArchivo(window):
    global index
    global clase
    global cadenajson
    global timestamp
    global codificar
    global prevhash
    global Hash
    data = ""
    x=datetime.datetime.now()
    y=datetime.datetime.now()
    fecha=str(x.day)+"-"+str(x.month)+"-"+str(x.year)+"::"
    hora=str(y.hour)+":"+str(y.minute)+":"+str(y.second)
    ahora=datetime.datetime.now().strftime("%d-%m-%Y::%H:%M:%S")
    archivo=carga(window)
    pito=""
    timestamp=fecha+hora
    cod = hashlib.sha256()
    try:
        with open(archivo) as file:
            reader = csv.reader(file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    line_count += 1
                    clase=row[1]
                else:
                    cadenajson = row[1]
                    line_count +=  1
            while True:
                window.clear()
                window.border(0)
                Titulo(window,' Insert Block ')
                msg="Carga Con exito"
                centro = round((60-len(msg))/2)
                window.addstr(10,centro,msg)
                sel = window.getch()
                if bloque.primero == None:
                    index=0
                    prevhash="0000"
                    H = str.encode(str(index)+timestamp+clase+cadenajson+prevhash)
                    cod.update(H)
                    Hash=str(cod.hexdigest())
                    print("entro en lista vacia cuando carga")
                else:
                    index=(bloque.ultimo.INDEX)+1
                    prevhash=bloque.ultimo.HASH
                    H = str.encode(str(index)+timestamp+clase+cadenajson+prevhash)
                    cod.update(H)
                    Hash=str(cod.hexdigest())
                    print("entro en lista no vacia cuando carga")


                server.sendall(Convertir_JSON(index,timestamp,clase,cadenajson,prevhash,Hash).encode('utf-8'))
                if sel == 27:
                    break
    except:
        while True:
            window.clear()
            window.border(0)
            Titulo(window,' Insert Block ')
            texto2="Error al cargar el archivo"
            centro2 = round((60-len(texto2))/2)
            window.addstr(10,centro2,texto2)
            key2 = window.getch()
            if key2 is 27:
                break

def Convertir_JSON(inde,time,clase,data,prev,h):
    json="{\n"+"\"INDEX\": "+str(index)+",\n"+"\"TIMESTAMP\": "+"\""+time+"\""+",\n"+"\"CLASS\": "+"\""+clase+"\""+",\n"+"\"DATA\": "+data+",\n"+"\"PREVIOUSHASH\": "+"\""+prev+"\""+",\n"+"\"HASH\": "+"\""+h+"\""+"\n"+"}"
    return json


def Read_Json(data,index):
    for (inicio,datos) in data.items():
        if isinstance(datos, dict):
            Read_Json(datos,index)
        else:
            if datos != None:
                p=datos.split("-")
                nodo=bloque.Buscar(index)
                if nodo != None:
                    nodo.arbol.insertartodo(p[0],str(p[1]))
                else:
                    print("no existe el index del bloque")
            else:
                pass

def carga(window):
    window.clear()
    window.border(0)
    curses.echo()
    curses.curs_set(True)
    Titulo(window,' Insert Block ')
    msg="Ingresa El nombre del archivo csv"
    centro = round((60-len(msg))/2)
    window.addstr(10,centro,msg)
    texto=""
    window.addstr(12,15,texto)
    jugador = window.getstr()
    texto = "".join(map(chr, jugador))
    curses.noecho()
    curses.curs_set(False)
    window.clear()
    return texto

def Show_Tree(window,raiz):
    global inorden
    if raiz != None:
        Show_Tree(window,raiz.izquierdo)
        inorden=inorden+str(raiz.carne)+"-"+raiz.nombre+"->"
        #window.addstr(5, 4, inorden)
        Show_Tree(window,raiz.derecho)

def Show_PostOrden(window,raiz):
    global postorden
    if raiz != None:
        Show_PostOrden(window,raiz.izquierdo)
        Show_PostOrden(window,raiz.derecho)
        postorden=postorden+str(raiz.carne)+"-"+raiz.nombre+"->"

def Show_PreOrden(window,raiz):
    global preorden
    if raiz != None:
        preorden=preorden+str(raiz.carne)+"-"+raiz.nombre+"->"
        Show_PreOrden(window,raiz.izquierdo)
        Show_PreOrden(window,raiz.derecho)




def print_Bloque(window, index,time,clase,data,prev,Hash):
    window.clear()
    Titulo(window,' Select Block ')
    height, width = window.getmaxyx()
    ind=index
    t=time
    c=clase
    dat=data[:150]
    p=prev
    h=Hash
    window.addstr(2, 4, "INDEX: "+str(ind))
    window.addstr(3, 4, "TIMESTAMP:"+t)
    window.addstr(4, 4, "CLASS: " +c)
    window.addstr(5,4, "DATA: "+ dat)
    window.addstr(15, 4,"PREVIOUSHASH: " +p)
    window.addstr(18, 4, "HASH: " +h)
   
    
    window.refresh()

def Menu_Bloque(window):
    temp=bloque.primero
    temp2=bloque.ultimo
    global selectblock
    validar=True
    if temp != None:
        n = temp.INDEX
        t=temp.TIMESTAMP
        c=temp.CLASS
        d=temp.DATA
        p=temp.PREVIOUSHASH
        h=temp.HASH
        print_Bloque(window, n,t,c,str(d),p,h)
        while(validar):
            key = window.getch()
            if key == curses.KEY_RIGHT:
                if temp.siguiente != None:
                    temp = temp.siguiente
                    n = temp.INDEX
                    t=temp.TIMESTAMP
                    c=temp.CLASS
                    d=temp.DATA
                    p=temp.PREVIOUSHASH
                    h=temp.HASH
                else:
                   print_Bloque
            elif key == curses.KEY_LEFT:
                if temp.atras != None:
                    temp = temp.atras
                    n = temp.INDEX
                    t=temp.TIMESTAMP
                    c=temp.CLASS
                    d=temp.DATA
                    p=temp.PREVIOUSHASH
                    h=temp.HASH
                else:
                    pass
            elif key == 10:
                selectblock=n
                break
            elif key == 27:
                break
            print_Bloque(window, n,t,c,d,p,h)
    else:
        text="<- VACIO ->   "
        centro = round((60-len(text))/2)
        window.addstr(12, centro , text)

def Sha_256(ind,time,clas,dat,pre):
    code = hashlib.sha256('{}{}{}{}{}'.format(str(ind),str(time),str(clas),str(dat),str(pre)).encode())

    return str(code.hexdigest())


datos={}
flag=False

hilo1=threading.Thread(target=Seleccion)
hilo1.start()
while True:
    read_sockets = select.select([server], [], [], 1)[0]
    import msvcrt
    if msvcrt.kbhit(): read_sockets.append(sys.stdin)

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            #print (message.decode('utf-8'))
            if message.decode('utf-8').strip() == 'true':
                print ("esto es un true")
                flag=True
            else:
                if message.decode('utf-8').strip() == 'false':
                    print("es un false")
                    flag = False
                    datos={}
                    
                else:
                    try:
                        datos={}
                        JSON=message.decode('utf-8')
                        datos=json.loads(JSON)
                        if bloque.primero == None:
                            if datos["PREVIOUSHASH"] == '0000':
                                server.sendall('true'.encode('utf-8'))
                                sys.stdout.flush()
                            else:
                                print("no sirve")
                        else:
                            if datos['PREVIOUSHASH'] == bloque.ultimo.HASH:
                                print("se envia true al server")
                                server.sendall('true'.encode('utf-8'))
                            else:
                                print("se envia false al server")
                                server.sendall('false'.encode('utf-8'))
                            sys.stdout.flush()

                    except:
                        print("error: formato json con error")

    if flag and datos != None:
        cod = hashlib.sha256()
        print("entro en la condicion el inf de none")
        if cadenajson == "" and timestamp =="":
            bloque.Insertar(datos['INDEX'], datos["TIMESTAMP"], datos["CLASS"], json.dumps(datos['DATA'], indent=4), datos["PREVIOUSHASH"], datos["HASH"])
            codes=json.loads(json.dumps(datos['DATA']))
            Read_Json(codes,datos["INDEX"])
            flag=False
            print("inserta con el jason")
        else:
            if bloque.primero == None:
                index=0
                prevhash="0000"
                H = str.encode(str(index)+timestamp+clase+cadenajson+prevhash)
                cod.update(H)
                Hash=str(cod.hexdigest())
                bloque.Insertar(index,timestamp,clase,cadenajson,prevhash,Hash)
                codes=json.loads(cadenajson)
                Read_Json(codes,index)
                cadenajson=""
                timestamp=""
                Hash=""
                prevhash=""
                clase=""
                flag=False
                print("inserta con la lista vacia carga")
            else:
                index=(bloque.ultimo.INDEX)+1
                print("entro a este ")
                aux=bloque.primero
                prevhash=bloque.ultimo.HASH
                H = str.encode(str(index)+timestamp+clase+cadenajson+prevhash)
                cod.update(H)
                Hash=str(cod.hexdigest())
                bloque.Insertar(index,timestamp,clase,cadenajson,prevhash,Hash)
                codes=json.loads(cadenajson)
                Read_Json(codes,index)
                cadenajson=""
                timestamp=""
                Hash=""
                prevhash=""
                clase=""
                flag=False
                print("inserta con lista no vacia carga")
server.close()
