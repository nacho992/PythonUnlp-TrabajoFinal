import PySimpleGUI as sg
import random
import string


caja = 15
dic = {}   #letra en la coordenada
dicColor = {} #coordenada
listaT = []
colorTablero = 'dimgrey'



def obtener_datosArch(arch):

    a = open(arch,'r')
    datos = a.read()
    a.close()
    return datos


def Lista_letras(palabras,lnue):
    """ lista todas las palabras que haya en el diccionario """
    for cadaLista in range(len(palabras['palVer'])):
        for i in palabras['palVer']:
            for pal in i:
                lnue.append(pal)
    for cadaLista in range(len(palabras['palSus'])):
        for i in palabras['palSus']:
            for pal in i:
                lnue.append(pal)
    for cadaLista in range(len(palabras['palAd'])):
        for i in palabras['palAd']:
            for pal in i:
                lnue.append(pal)



def crearMatriz(nxn):
    matriz = []

    '''
        retorna una matriz de nxn filas/columnas
        nota: el valor de nxn, es la longitud
        de la palabra mas grande, proporcionada por el docente
        en base a eso, se tomaran la dimensiones de la matriz
    '''
    for fila in range(nxn):
        matriz.append([])
        for columna in range(nxn):
            matriz[fila].append("")
    return matriz


def completarMatriz(matriz, nxn):
    """
        este modulo retorna la matriz de nxn
        con letras aleatorias
    """
    for fila in range(nxn):
        for columna in range(nxn):
            if matriz[fila][columna] is "":
                matriz[fila][columna] = random.choice(string.ascii_lowercase)
    return matriz


def valores_posicion(matriz, nxn, esfila, pos):
    '''
        retorna un lista con informacion de una fila/columna especifica de la matriz
        esfila --> indica si es columna o fila
        pos --> indica que fila/columna
    '''
    valores = []
    espacios = 0

    for i in range(nxn):
        if esfila:
            if matriz[pos][i] != "":
                valores.append(espacios)
                valores.append(matriz[pos][i])
            else:
                espacios += 1
        else:
            if matriz[i][pos] != "":
                valores.append(espacios)
                valores.append(matriz[i][pos])
                espacios = 0
            else:
                espacios += 1 
    if espacios == nxn:
        valores.append(espacios)
        valores.append("0")
    return valores


def colocar_palabra(matriz, palabra, esfila, pos, inicio):
    '''
        coloca la palabra dentro de la matriz, en una coordenada especificada
    '''
    for x in range(inicio, inicio + len(palabra)):
        if esfila:
            matriz[pos][x] = palabra[x - inicio]
        else:
            matriz[x][pos] = palabra[x - inicio]
    return matriz

def procesar_palabras(matriz, nxn, palabras, esfila):
    for i in range(len(palabras)):
        pos_inicial = random.randint(0, nxn-1) 
        posicion = pos_inicial
        colocada = False
        while not colocada:
            valores_en_posicion = valores_posicion(matriz, nxn, esfila, posicion)
            aux1 = int(len(valores_en_posicion)/2)
            for e in range(aux1):
                if int(valores_en_posicion[ e * 2]) > len(palabras[i]):
                    margen = int(valores_en_posicion[e * 2]) - len(palabras[i])
                    matriz = colocar_palabra(matriz, palabras[i], esfila, posicion, margen)
                    columna_final = margen + len(palabras[i])-1
                    colocada = True
            if not colocada:
                if posicion < nxn-1:
                    posicion += 1
                else:
                    posicion = 0
    return matriz


def evaluar_palabra(palabra_evaluar,lnue,M):
    """ Compara la palabra ingresada como parametro con cada elemento de de la lista """
    ok=True
    encontre = False
    i = 0
    if M:
        x = ''.join(['{}'.format(o) for o in palabra_evaluar])
        while ok and (i < len(lnue)):
            if lnue[i].upper() == x.upper():
                encontre = True
                ok = False
            i+=1
    else:
        x = ''.join(['{}'.format(o) for o in palabra_evaluar])
        while ok and (i < len(lnue)):
            if lnue[i].lower() == x.lower():
                encontre = True
                ok = False
            i+=1
    return encontre


def definir_color(un_string,dic):
    """ recibe una palabra a buscar en el diccionario, la busca y nos retorno un valor(color) del diccionaro """
    color = 'aaaa'
    if un_string in dic['palVer'][0]:
        color = dic['verbo']
    if un_string in dic['palAd'][0]:
        color = dic['adjetivo']
    if un_string in dic['palSus'][0]:
        color = dic['sustantivo']
    return color

        
def graficar_matrix(mt, nxn, d, M):
    for fila in range(nxn):
        for columna in range(nxn):
            localizacion = (fila * caja + 11, columna * caja + 12)
            dato = d.DrawRectangle((fila * caja + 5, columna * caja + 3), (fila* caja + caja + 5, columna * caja + caja + 3), line_color='white',fill_color=colorTablero)
            dicColor[(fila, columna)] = dato
            if M:
                dic[(fila, columna)] = mt[fila][columna].upper()
                d.DrawText(mt[fila][columna].upper(), localizacion , font='Courier 22', color='white')
            else:
                dic[(fila, columna)] = mt[fila][columna].lower()
                d.DrawText(mt[fila][columna].lower(), localizacion , font='Courier 22', color='white')

#ok = bool, SENTIDO DE LA DE LAS PALABRAS EN LA MATRIZ, VERTICAL HORIZONTAL
#M = bool, SI ES MAYUSCULA O MINUSCULA
def tablero(long_maxPal,dic_palabras,M,ok,TipoAyuda):
    sg.ChangeLookAndFeel('Dark')
    layout = [
            [sg.Text('tes de tablero'), sg.Text('', key='_salida_')],
            [sg.Graph((500, 500), (0, 170), (170, 0), key='_dibujar_', change_submits=True, drag_submits=False)],
            [sg.Frame(
                            layout = [
                                        [sg.Text('Cantidad de palabras restantes :'),sg.Text('',key= 'cantPal')],
                                        [sg.Multiline('',key='ayuda'),sg.Multiline('',key='def')],
                                     ], title = 'Cantidad de palabras y/o Definiciones y palabras', title_color = 'lightgreen'
                        )],
            [sg.Button('ver'), sg.Button('cancelar'),sg.Button('Verificar Palabra / Limpiar selección')],
         ]
    window =  sg.Window('panel').Layout(layout).Finalize()
    g = window.FindElement('_dibujar_')


    lnue = []
    Lista_letras(dic_palabras,lnue)     #recibe el diccionario, devuelve una lista(lnue) de todas las palabras seleccionadas
    nxn = long_maxPal + 1               #longuitud de la palabra mas larga
    matriz = crearMatriz(nxn)
    matriz = procesar_palabras(matriz, nxn, lnue, ok)
    dato = completarMatriz(matriz, nxn)
    graficar_matrix(dato, nxn, g, M)
    lista_click = []                    #esta lista contendra las letras que seran evaluadas con las palabras de la lista(lnue)
    todos_los_clik = []                 #todas las cooredenadas donde se hizo click en el tablero
    cantidad_pal = len(lnue)
    palabrasBuscadas = '\n'.join(['{}'.format(p) for p in lnue])
    window.FindElement('cantPal').Update(cantidad_pal)
    defPal = obtener_datosArch('ArchivoLocal.txt')  #SE OBTIENEN LAS DEFINICIONES GUARDADAS EN UN ARCHIVO LOCAL




    #--------SE EVALUAN LAS CONDICIONES DE AYUDA-------
    if TipoAyuda[0] and TipoAyuda[1]:
        window.FindElement('def').Update(defPal)
        window.FindElement('ayuda').Update(palabrasBuscadas)       
    elif  TipoAyuda[0]:
        window.FindElement('ayuda').Update(palabrasBuscadas)
    elif TipoAyuda[1]:
        window.FindElement('ayuda').Update(defPal)
    else:
        window.FindElement('cantPal').Update(str(len(lnue)))
    ##-----------------FIN EVALUACION------------------
    while True:
        button, values = window.Read()
        if button is None or button is 'cancelar':
            break
        puntero = values['_dibujar_']
        if button is '_dibujar_':
            if puntero == (None, None):
                continue
            try:
                coorY = puntero[0]//caja 
                coorX = puntero[1]//caja
                click = (coorY, coorX)
                if click in todos_los_clik:
                    g.Update(g.TKCanvas.itemconfig(dicColor[click], fill=colorTablero))
                    todos_los_clik.remove(click)
                    lista_click.remove(dic[click])
                else:
                    g.TKCanvas.itemconfig(dicColor[click], fill="blue")
                    todos_los_clik.append(click)  #coordenadas
                    lista_click.append(dic[click]) #letras
            except KeyError:
                None 
        if button is 'Verificar Palabra / Limpiar selección':
            encontre = evaluar_palabra(lista_click,lnue,M)
            if encontre:
                cantidad_pal -= 1
                window.FindElement('cantPal').Update(cantidad_pal)
                x = ''.join(['{}'.format(o) for o in lista_click])
                sg.Popup(f'Has Encontrado la palabra {x}')
                color = definir_color(x.lower(),dic_palabras)
                for i in todos_los_clik:
                    g.TKCanvas.itemconfig(dicColor[i]+1, fill= color)
            for i in todos_los_clik:
                g.Update(g.TKCanvas.itemconfig(dicColor[i], fill=colorTablero))
            todos_los_clik.clear()
            lista_click.clear()
            if cantidad_pal == 0:
                sg.Popup('¡¡Has encontrado todas las palabras!!')