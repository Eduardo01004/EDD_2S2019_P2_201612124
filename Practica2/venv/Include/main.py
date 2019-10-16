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
from Blockchain import NodoBlock, BlockChain
bloque=BlockChain()

index=0
clase=""
timestamp=""
cadenajson=""
salida=""
prevhash=""
Hash=""
codificar=hashlib.sha256()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:  #verifica cuando se ejecuta el programa con 3 argumentos
	print ("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port)) #inicia el cliente

def Menu_Principal(window):

    Titulo(window,'Main Menu')
    window.addstr(10,21, '1. Insert Block')
    window.addstr(11,21, '2. Select Block')
    window.addstr(12,21, '3. Reports')
    window.addstr(13,21, '4. Exit')
    window.timeout(-1)

def Titulo(window,var):
    window.clear()
    window.border()
    centro = round((60-len(var))/2)
    window.addstr(0,centro,var)

def TeclaESC(window):
    tecla=window.getch()
    while tecla!=27:
        tecla = window.getch()

def Seleccion(window,flag):
    keystroke = -1
    while(keystroke==-1):
        keystroke = window.getch()
        if(keystroke==49):
            global username
            Titulo(window, ' Insert Block ')
            LeerArchivo(window)
            TeclaESC(window)
            Menu_Principal(window)
            keystroke=-1
        elif(keystroke==50):
            Titulo(window, ' Select Block ')
            Menu_Bloque(window)
            TeclaESC(window)
            Menu_Principal(window)
            keystroke=-1
        elif(keystroke==51):
            Titulo(window,' Reports')
            TeclaESC(window)
            Menu_Principal(window)
            keystroke=-1
        elif(keystroke==52):
            flag=False
        else:
            keystroke=-1

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
    archivo=carga(window)
    pito=""
    timestamp=fecha+hora
    data=""
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
                    for x in range (1,len(row)):
                        pito=row[x]+","+"\n"
                        data=data+pito
                    line_count +=  1
                temp=len(data)
                cadenajson=data[:temp-2] 

            decoded=json.loads(cadenajson)
            
            Read_Json(decoded)
            if bloque.primero == None:
                index=0
                prevhash="0000"
                H = str.encode(str(index)+timestamp+clase+cadenajson+prevhash)
                cod.update(H)
                Hash=str(cod.hexdigest())
            else:
                index=index+1
                aux=bloque.primero
                prevhash=bloque.ultimo.HASH
                H = str.encode(str(index)+timestamp+clase+cadenajson+prevhash)
                cod.update(H)
                Hash=str(cod.hexdigest())

            
           # Send_Bloque(server,Convertir_JSON(str(index),timestamp,clase,cadenajson,prevhash,Hash))
                
           

            while True:
                window.clear()
                window.border(0)
                Titulo(window,' Insert Block ')
                msg="Carga Con exito"
                centro = round((60-len(msg))/2)
                window.addstr(10,centro,msg)
                sel = window.getch()
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

    
def Insert_Bloque(timestamp,clase,cadenajson):
    global index
    Hash = hashlib.sha256()
    if bloque.primero == None:
        index=0
        my_str_as_bytes1 = str.encode(str(index)+timestamp+clase+cadenajson+"0000")
        Hash.update(my_str_as_bytes1)
        bloque.Insertar(index,timestamp,clase,cadenajson,"0000",str(Hash.hexdigest()))     
    else:
        index=index+1
        aux=bloque.primero
        my_str_as_bytes = str.encode(str(index)+timestamp+clase+cadenajson+bloque.ultimo.HASH)
        Hash.update(my_str_as_bytes)
        bloque.Insertar(index,timestamp,clase,cadenajson,bloque.ultimo.HASH,str(Hash.hexdigest()))

def Read_Json(data):
    for (inicio,datos) in data.items():
        if isinstance(datos, dict):
            Read_Json(datos)
        else:
            if datos != None:
                p=datos.split("-")
                #print("carne: ",p[0])
                #print("nombre: ",p[1])
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

def print_Bloque(window, index,time,clase,data,prev,Hash):
    window.clear()
    Titulo(window,' Select Block ')
    height, width = window.getmaxyx()
    ind=index
    t=time
    c=clase
    dat=data
    p=prev
    h=Hash
    window.addstr(2, 4, "INDEX: "+str(ind))
    window.addstr(3, 4, "TIMESTAMP:"+t)
    window.addstr(4, 4, "CLASS: " +c)
    window.addstr(5,4, "DATA: "+ dat)
    window.addstr(20, 4,"PREVIOUSHASH: " +p)
    window.addstr(22, 4, "HASH: " +h)
   
    
    window.refresh()

def Menu_Bloque(window):
    temp=bloque.primero
    temp2=bloque.ultimo
    validar=True
    if temp != None:
        n = temp.INDEX
        t=temp.TIMESTAMP
        c=temp.CLASS
        d=temp.DATA
        p=temp.PREVIOUSHASH
        h=temp.HASH
        print_Bloque(window, n,t,c,d,p,h)
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

curses.initscr()
window = curses.newwin(25,60,0,0)
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.border(0)
flag=True
Menu_Principal(window)

while True:
    keystroke = window.getch()

    read_sockets = select.select([server], [], [], 1)[0]
    import msvcrt
    if msvcrt.kbhit(): read_sockets.append(sys.stdin)

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print (message.decode('utf-8'))
            if message.decode('utf-8') == 'true':
                print ("esto es un true")
                server.sendall('true'.encode('utf-8'))
            else:
                print("no entra al if")
    
    if(keystroke==49):
        Titulo(window, ' Insert Block ')
        LeerArchivo(window)
        TeclaESC(window)
        Menu_Principal(window)
    elif(keystroke==50):
        Titulo(window, ' Select Block ')
        Menu_Bloque(window)
        TeclaESC(window)
        Menu_Principal(window)
    elif(keystroke==51):
        Titulo(window,' Reports')
        TeclaESC(window)
        Menu_Principal(window)
    elif(keystroke==52):
        break
    else:
        pass
    
        


curses.endwin()
server.close()
