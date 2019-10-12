import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import csv
import time
import datetime
import hashlib
import json
from Blockchain import NodoBlock, BlockChain
bloque=BlockChain()

index=0
clase=""

def Menu_Principal(window):

    Titulo(window,'Main Menu')
    window.addstr(7,21, '1. Insert Block')
    window.addstr(8,21, '2. Select Block')
    window.addstr(9,21, '3. Reports')
    window.addstr(10,21, '4. Exit')
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

def Seleccion(window):
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
            pass
        else:
            keystroke=-1

def LeerArchivo(window):
    global index
    global clase
    data = ""
    x=datetime.datetime.now()
    y=datetime.datetime.now()
    fecha=str(x.day)+"-"+str(x.month)+"-"+str(x.year)+"::"
    hora=str(y.hour)+":"+str(y.minute)+":"+str(y.second)
    archivo=carga(window)
    pito=""
    timestamp=fecha+hora
    Hash = hashlib.sha256()
    data=""
    p=bloque.primero
    #print(m.hexdigest())

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
                #print(cadenajson)
                
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
                
            #bloque.GraficarBloque()
            
            
            p="{\"value\":\"201403525-Nery\",\"left\":{\"value\":\"201212963-Andres\",\"left\":{\"value\":\"201005874-Estudiante1\",\"left\":null,\"right\":null},\"right\":{\"value\":\"201313526-Alan\",\"left\":null,\"right\":null}},\"right\":{\"value\":\"201403819-Anne\",\"left\":{\"value\":\"201403624-Fernando\",\"left\":null,\"right\":null},\"right\":{\"value\":\"201602255-Estudiante2\",\"left\":null,\"right\":null}}}"
            decoded=json.loads(cadenajson)
            Read_Json(decoded)
            while True:
                window.clear()
                window.border(0)
                Titulo(window,' Insert Block ')
                msg="Carga Con exito"
                centro = round((60-len(msg))/2)
                window.addstr(10,centro,msg)
                sel = window.getch()
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


def Read_Json(data):
    for (inicio,datos) in data.items():
        if isinstance(datos, dict):
            Read_Json(datos)
        else:
            if datos != None:
                print(datos)
                print("carne:",datos.split('-',1))
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
    window.addstr(13, 4,"PREVIOUSHASH: " +p)
    window.addstr(18, 4, "HASH: " +h)
   
    
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
                temp = temp.siguiente
                n = temp.INDEX
                t=temp.TIMESTAMP
                c=temp.CLASS
                d=temp.DATA
                p=temp.PREVIOUSHASH
                h=temp.HASH
            elif key == curses.KEY_LEFT:
                temp = temp.atras
                n = temp.INDEX
                t=temp.TIMESTAMP
                c=temp.CLASS
                d=temp.DATA
                p=temp.PREVIOUSHASH
                h=temp.HASH
            elif key == 10:
                break
            elif key == 27:
                break
            print_Bloque(window, n,t,c,d,p,h)
    else:
        print("vacio")


curses.initscr()
window = curses.newwin(23,60,0,0)
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.border(0)

Menu_Principal(window)
Seleccion(window)

curses.endwin()
