import PySimpleGUI as sg
import random
import string

dic_palabra_coordenada = {}  # clave sera una palabra, como valor tiene una lista de coordenadas donde fue ubicada
caja = 15
dic = {}   # letra en la coordenada
dicColor = {}  
colorTablero = 'dimgrey'


def limpiar_vacias(dic_palabras):
    '''
    esta funcion evita que se agregen listas vacias al diccionario en caso de leventar un slider contador sin palabras ingreseadas 
    '''

    if len(dic_palabras['palVer']) > 1 and len(dic_palabras['palAd']) > 1 and len(dic_palabras['palSus']) > 1:
        for i in range(len(dic_palabras['palVer']) - 1):
            dic_palabras['palVer'].remove([])
            dic_palabras['palAd'].remove([])
            dic_palabras['palSus'].remove([])
    



def obtener_datosArch(arch):

    a = open(arch, 'r')
    datos = a.read()
    a.close()
    return datos


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
    """
        retorna un lista con informacion de una fila/columna especifica de la matriz
        esfila --> indica si es columna o fila
        pos --> indica que fila/columna
    """
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
    """
        coloca la palabra dentro de la matriz, en una coordenada especificada
    """
    dic_palabra_coordenada[palabra] = []
    for x in range(inicio, inicio + len(palabra)):
        if esfila:
            dic_palabra_coordenada[palabra].append((pos,x))  #clave sera una palabra, como valor tiene una lista de coordenadas donde fue ubicada
            matriz[pos][x] = palabra[x - inicio]
        else:
            dic_palabra_coordenada[palabra].append((x,pos))
            matriz[x][pos] = palabra[x - inicio]
    return matriz


def procesar_palabras(matriz, nxn, palabras, esfila):
    """
        esta funcion se encarga de encontrar y distribuir las palabras de manera random por toda la matriz
        manejando un margen para su posicion, el sentido de la palabra( si es horizontal o vertical)
        dependiendo de lo que el usuario desea(param esfila),
        y finamente llamando a una funcion que se encargara de colocar la palabra, finalmente se retornara la matriz
        con los datos ya ubicado en sus respectivas posiciones
    """
    for i in range(len(palabras)):
        pos_inicial = random.randint(0, nxn-1) 
        posicion = pos_inicial
        colocada = False
        while not colocada:
            valores_en_posicion = valores_posicion(matriz, nxn, esfila, posicion)
            aux1 = int(len(valores_en_posicion)/2)
            for e in range(aux1):
                if int(valores_en_posicion[e * 2]) > len(palabras[i]):
                    margen = int(valores_en_posicion[e * 2]) - len(palabras[i])
                    matriz = colocar_palabra(matriz, palabras[i], esfila, posicion, margen)
                    colocada = True
            if not colocada:
                if posicion < nxn-1:
                    posicion += 1
                else:
                    posicion = 0
    return matriz


def ordenacion_horizontal(tupla):
    """
        ordena segundo elemento de la tupla de mayor a menor
    """
    return tupla[1], -tupla[0]


def ordenacion_vertical(tupla):
    """
        ordena primer elemento de la tupla de mayor a menor
    """
    return tupla[0], - tupla[1]


def armo_palabra(dic, todos_los_clik, sentido):
    """
        deveulve una palabra segun las letras que haya en las coordenadas recibidas como parametro (todos_los_clik).
    """
    un_string = ''
    todos_los_clik.sort() #  se ordena para luego poder comparar si son iguales
    if sentido:
        datos = sorted(todos_los_clik, key=ordenacion_horizontal)
    else:
        datos = sorted(todos_los_clik, key=ordenacion_vertical)
    for i in datos:
        un_string = un_string + dic[i]
    if un_string.lower() in dic_palabra_coordenada.keys():
        if dic_palabra_coordenada[un_string.lower()] == todos_los_clik: #  si la palabra se encuentra en sus coordenadas correspondientes
            return un_string.lower()
    else:
        un_string = ''
        return un_string.lower()


def definir_color(un_string, dic, lnue):
    """ recibe una palabra a buscar en el diccionario, la busca y nos retorno un valor(color) del diccionaro """
    color = 'red'
    encontre = False
    try:
        if un_string in lnue:
            if un_string in dic['palVer'][0]:
                color = dic['verbo']
                encontre = True
                dic['palVer'][0].remove(un_string)
            elif un_string in dic['palAd'][0]:
                color = dic['adjetivo']
                encontre = True
                dic['palAd'][0].remove(un_string)
            elif un_string in dic['palSus'][0]:
                color = dic['sustantivo']
                encontre = True
                dic['palSus'][0].remove(un_string)
            else:
                sg.Popup('La palabra no existe')
    except IndexError:
        color = 'dimgrey'
    return encontre, color

        
def graficar_matrix(mt, nxn, d, M):
    """
       esta funcion arma el tablero, y en ella distribuimos todos los datos de nuestra matriz
       manejando un localizacion que sirve para centrar los datos los mejor posible en el tablero, dependiendo de lo
       que el user decida los datos se mostraran en mayusculas o su opuesto (M: es la condicion que determina esto)
    """
    for fila in range(nxn):
        for columna in range(nxn):
            localizacion = (fila * caja + 11, columna * caja + 12)
            dato = d.DrawRectangle((fila * caja + 5, columna * caja + 3), (fila * caja + caja + 5, columna * caja + caja + 3), line_color='white', fill_color=colorTablero)
            dicColor[(fila, columna)] = dato
            if M:
                dic[(fila, columna)] = mt[fila][columna].upper()
                d.DrawText(mt[fila][columna].upper(), localizacion , font='Courier 22', color='white')
            else:
                dic[(fila, columna)] = mt[fila][columna].lower()
                d.DrawText(mt[fila][columna].lower(), localizacion , font='Courier 22', color='white')


def ventana_terminar(cantidad_pal, lnue):
    """
         esta funcion se encarga de mostrarle la cantidad de palabras que le falto al usuario
         por encontrar, adicionalmente tambien mostrandole la palbras que no encontro
         retornado la opcion de volver al menu o finalizar
    """
    ventana = [
        [sg.Text('FIN DEL JUEGO', size=(30, 1), justification='center', font=('Helvetica', 25), text_color='lightgreen')],
        [sg.Text(f'Cantidad de palabras por encontrar : {cantidad_pal}', size=(30, 1), justification='center', font=('Helvetica', 25), text_color='red')],
        [sg.Text(f"Verbos: {lnue['palVer'][0]}", size=(30, 1), text_color='orange', font=('Helvetica', 15))],
        [sg.Text(f"Sustantivos: {lnue['palSus'][0]}", size=(30, 1), text_color='orange', font=('Helvetica', 15))],
        [sg.Text(f"adjetivos: {lnue['palAd'][0]}", size=(30, 1), text_color='orange', font=('Helvetica', 15))],
        [sg.Radio('Volver al menu', "R", key='v'), sg.Radio('Salir del juego', "R", key='S'), sg.Button('OK')]

    ]
    window = sg.Window('Continuar?').Layout(ventana)
    c = 'no'
    while True:
        button, values = window.Read()
        if button is None:
            break
        if button is 'OK':
            if values['v'] is True:
                c = 'jugar'
                window.Close()
                break
            else:
                window.Close()
                break
    return c


def tablero(lnue, long_maxPal, dic_palabras, M, ok, TipoAyuda):
    """
       en esta funcion se encarga de armar la interface del tablero, e interactuar con todos lo modulos
       iniciando con la creacion de nuestra matriz, para esto se toma la longitud de la palabra mas grande + 4
       para darle mas espacion y mejor distribucion a las palabras(param lnue), siguiendo con el procesamiento de estas misma,
       depues completando la matriz con letras random, y finalmente graficandola, depues de eso, en esta funcion,
       tambien maneja toda la interaccion del jugador con el tablero mapiando los click e evaluando la palabras,
       el tipo de ayuda que este recibe(param tipoAyuda), el sentido en el que se le van a mostrar la palabras(param ok)
    """
    sg.ChangeLookAndFeel('Dark')
    layout = [
            [sg.Text('sopa de letras', text_color='red')],
            [sg.Graph((430, 430), (0, 180), (180, 0), key='_dibujar_', change_submits=True, drag_submits=False)],
            [sg.Frame(
                            layout=[
                                        [sg.Text('Cantidad de palabras restantes :'), sg.Text('', key='cantPal')],
                                        [sg.Text('Sustantivos :'), sg.Text('', key='cantS'),
                                        sg.Text('Adjetivos :'),sg.Text('', key='cantA'),
                                        sg.Text('Verbos :'),sg.Text('', key='cantV')],
                                        [sg.Multiline('', key='ayuda'), sg.Multiline('', key='def')],
                                     ], title='Cantidad de palabras y/o Definiciones y palabras', title_color='lightgreen'
                        )],
            [sg.ReadButton('Volver al menu', button_color=('white', 'orange'), key='Volver al menu'), sg.Button('salir', button_color=('white', 'red')), sg.Button('Verificar Palabra / Limpiar selección'), sg.Button('terminar', button_color=('white', 'red'))],
         ]

    window = sg.Window('panel').Layout(layout).Finalize()
    g = window.FindElement('_dibujar_')
    window.FindElement('Volver al menu').Update(disabled=True)
    window.FindElement('salir').Update(disabled=True)

    limpiar_vacias(dic_palabras) #  en caso de que se ingrese una lista vacia al diccionario

    #-----------------------------------------------------------------------------------#

    nxn = long_maxPal + 4  # longuitud de la palabra mas larga
    matriz = crearMatriz(nxn)
    matriz = procesar_palabras(matriz, nxn, lnue, ok)
    dato = completarMatriz(matriz, nxn)
    graficar_matrix(dato, nxn, g, M)
    cantidad_pal = len(lnue)
    palabrasBuscadas = '\n'.join(['{}'.format(p) for p in lnue])
    window.FindElement('cantPal').Update(cantidad_pal)
    defPal = obtener_datosArch('ArchivoLocal.txt')  # SE OBTIENEN LAS DEFINICIONES GUARDADAS EN UN ARCHIVO LOCAL
    todos_los_clik = []  # todas las cooredenadas donde se hizo click en el tablero
    coordenadas_encontradas = []

    # --------SE EVALUAN LAS CONDICIONES DE AYUDA------- #
    if TipoAyuda[0] and TipoAyuda[1]:
        window.FindElement('def').Update(defPal)
        window.FindElement('ayuda').Update(palabrasBuscadas)
        window.FindElement('cantS').Update(str(len(dic_palabras['palSus'][0])))
        window.FindElement('cantV').Update(len(dic_palabras['palVer'][0]))
        window.FindElement('cantA').Update(str(len(dic_palabras['palAd'][0])))
    elif TipoAyuda[0]:
        window.FindElement('ayuda').Update(palabrasBuscadas)
        window.FindElement('cantS').Update(str(len(dic_palabras['palSus'][0])))
        window.FindElement('cantV').Update(len(dic_palabras['palVer'][0]))
        window.FindElement('cantA').Update(str(len(dic_palabras['palAd'][0])))
    elif TipoAyuda[1]:
        window.FindElement('ayuda').Update(defPal)
        window.FindElement('cantS').Update(str(len(dic_palabras['palSus'][0])))
        window.FindElement('cantV').Update(len(dic_palabras['palVer'][0]))
        window.FindElement('cantA').Update(str(len(dic_palabras['palAd'][0])))
    else:
        window.FindElement('cantPal').Update(str(len(lnue)))
        window.FindElement('cantS').Update(str(len(dic_palabras['palSus'][0])))
        window.FindElement('cantV').Update(len(dic_palabras['palVer'][0]))
        window.FindElement('cantA').Update(str(len(dic_palabras['palAd'][0])))
    # -----------------FIN EVALUACION------------------#

    while True:
        button, values = window.Read()
        if button is None:
            break
        puntero = values['_dibujar_']
        if button is '_dibujar_':
            if puntero == (None, None):
                continue
            coorX = puntero[0] // caja
            coorY = puntero[1] // caja
            click = (coorX, coorY)
            # ------------marcar y desmarcar letras------------#
            if click in dic.keys():  # si esta en el margen de nuestra matriz creada
                if click in coordenadas_encontradas:
                    print()
                elif click not in todos_los_clik:
                    g.TKCanvas.itemconfig(dicColor[click], fill="blue")
                    todos_los_clik.append(click)  # coordenadas seleccionadas
                else:
                    g.TKCanvas.itemconfig(dicColor[click], fill=colorTablero)
                    todos_los_clik.remove(click)
        if button is 'Verificar Palabra / Limpiar selección':
            # se arma la palabra segun las letras que haya en las coordenadas
            palC = armo_palabra(dic, todos_los_clik, ok)
            encontre, color = definir_color(palC, dic_palabras, lnue)
            #  -------si la seleccion coincide con alguna palabra--------#
            if encontre:
                cantidad_pal -= 1
                window.FindElement('cantPal').Update(cantidad_pal)
                sg.Popup(f'Has Encontrado la palabra {palC}', text_color='orange', title='BIEN')
                for i in todos_los_clik:
                    g.Update(g.TKCanvas.itemconfig(dicColor[i], fill=color))  # concatenar + 1 a dicolor para pintar solo letra
                    coordenadas_encontradas.append(i)
                lnue.remove(palC)  # se van eliminando las palabras encontradas
                window.FindElement('ayuda').Update(lnue)
                todos_los_clik.clear()
                palC = ''
            else:
                # -------Se limpia_todo lo que haya sido seleccionado--------#
                sg.Popup(f'la palabra {palC} no existe', text_color='lightgreen', title='ERROR', font='Curier')
                for i in todos_los_clik:
                    g.Update(g.TKCanvas.itemconfig(dicColor[i], fill=colorTablero))
                todos_los_clik.clear()
                palC = ''
            # -----------------------------------------------------------#
            if cantidad_pal == 0:
                window.FindElement('Volver al menu').Update(disabled=False)
                window.FindElement('salir').Update(disabled=False)
                window.FindElement('terminar').Update(disabled=False)
                sg.Popup('¡¡Has encontrado todas las palabras!!', title='Crack!')
                # ------se limpian las listas---------#
                dic_palabras['palVer'].clear()
                dic_palabras['palSus'].clear()
                dic_palabras['palAd'].clear()
        c = ''
        if button is 'terminar':
            var = ventana_terminar(cantidad_pal, dic_palabras)
            if var is 'jugar':
                window.Close()
                return var
            elif var is 'no':
                window.Close()
                return c
        if button is 'Volver al menu':
            c = 'jugar'
            window.Close()
            return c
        if button is 'salir':
            break