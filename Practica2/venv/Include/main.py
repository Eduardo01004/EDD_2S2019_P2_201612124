import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import csv
import time
import datetime
import hashlib

index=0

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
    index=index+1
    archivo=carga(window)
    pito=""
    x=datetime.datetime.now()
    y=datetime.datetime.now()
    fecha=str(x.day)+"-"+str(x.month)+"-"+str(x.year)+"-"+"::"
    hora=str(y.hour)+":"+str(y.minute)+":"+str(y.second)
    timestamp=fecha+hora
    #print(timestamp)
    m = hashlib.sha256()
    m.update(b"Nobody inspects")
    #print(m.hexdigest())

    try:
        with open(archivo) as file:
            reader = csv.reader(file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    line_count += 1
                else:
                    for x in range (1,len(row)):
                        pito=row[x]+","
                        temp=len(pito)
                        cadenajson=pito[:temp-1]
                        #print(cadenajson)
                    line_count +=  1

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



curses.initscr()
window = curses.newwin(20,60,0,0)
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.border(0)

Menu_Principal(window)
Seleccion(window)

curses.endwin()
