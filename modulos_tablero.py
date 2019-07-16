import random
import string


dic_palabra_coordenada = {}  # clave sera una palabra, como valor tiene una lista de coordenadas donde fue ubicada

caja = 32


def obtener_datos_arch(arch):
    a = open(arch, 'r')
    datos = a.read()
    a.close()
    return datos


def crear_matriz(nxn):
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


def completar_matriz(matriz, nxn):
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
            # clave sera una palabra, como valor tiene una lista de coordenadas donde fue ubicada
            dic_palabra_coordenada[palabra].append((pos, x))
            matriz[pos][x] = palabra[x - inicio]
        else:
            dic_palabra_coordenada[palabra].append((x, pos))
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
        pos_inicial = random.randint(0, nxn - 1)
        posicion = pos_inicial
        colocada = False
        while not colocada:
            valores_en_posicion = valores_posicion(matriz, nxn, esfila, posicion)
            for e in range(int(len(valores_en_posicion) / 2)):
                if int(valores_en_posicion[e * 2]) > len(palabras[i]):
                    margen = int(valores_en_posicion[e * 2]) - len(palabras[i])
                    matriz = colocar_palabra(matriz, palabras[i], esfila, posicion, margen)
                    colocada = True
                    break
            if not colocada:
                if posicion < nxn - 1:
                    posicion += 1
                else:
                    posicion = 0
    return matriz


def graficar_matrix(color, mt, nxn, d, m):
    """
       esta funcion arma el tablero, y en ella distribuimos todos los datos de nuestra matriz
       manejando un localizacion que sirve para centrar los datos los mejor posible en el tablero, dependiendo de lo
       que el user decida los datos se mostraran en mayusculas o su opuesto (M: es la condicion que determina esto)
    """
    dic_color = {}
    dic = {}
    for fila in range(nxn):
        for columna in range(nxn):
            localizacion = (fila * caja + 20, columna * caja + 19)
            dato = d.DrawRectangle((fila * caja + 5, columna * caja + 3),
                                   (fila * caja + caja + 5, columna * caja + caja + 3),
                                   line_color='white', fill_color=color)
            dic_color[(fila, columna)] = dato
            if m:
                dic[(fila, columna)] = mt[fila][columna].upper()
                d.DrawText(mt[fila][columna].upper(), localizacion, font='Courier 19', color='white')
            else:
                dic[(fila, columna)] = mt[fila][columna].lower()
                d.DrawText(mt[fila][columna].lower(), localizacion, font='Courier 19', color='white')
    return dic_color, dic


def determinar_ayuda(sg, layout, ayuda, color_interface):

    if ayuda[0] and ayuda[1]:
        layout.append([sg.Frame(
            background_color=color_interface,
            layout=[
                [sg.Multiline('', key='ayuda', background_color=color_interface, text_color='white'),
                 sg.Multiline('', key='def', background_color=color_interface, text_color='white')],
            ], title='Cantidad de palabras y/o Definiciones y palabras', title_color='lightgreen'
        )])
        layout.append([sg.ReadButton('Volver al menu', button_color=('white', 'orange'), key='Volver al menu'),
                      sg.Button('salir', button_color=('white', 'red')),
                      sg.Button('Verificar Palabra / Limpiar selección'),
                      sg.Button('terminar', button_color=('white', 'red'))])
        return layout

    elif ayuda[0] and ayuda[1] is False:
        layout.append([sg.Frame(
            background_color=color_interface,
            layout=[
                [sg.Multiline('', key='ayuda', background_color=color_interface, text_color='white')],
            ], title='Cantidad de palabras', title_color='lightgreen'
        )])
        layout.append([sg.ReadButton('Volver al menu', button_color=('white', 'orange'), key='Volver al menu'),
                       sg.Button('salir', button_color=('white', 'red')),
                       sg.Button('Verificar Palabra / Limpiar selección'),
                       sg.Button('terminar', button_color=('white', 'red'))])
        return layout

    elif ayuda[1] and ayuda[0] is False:
        layout.append([sg.Frame(
            background_color=color_interface,
            layout=[
                [sg.Multiline('', key='def', background_color=color_interface, text_color='white')],
            ], title='definiciones', title_color='lightgreen'
        )])
        layout.append([sg.ReadButton('Volver al menu', button_color=('white', 'orange'), key='Volver al menu'),
                       sg.Button('salir', button_color=('white', 'red')),
                       sg.Button('Verificar Palabra / Limpiar selección'),
                       sg.Button('terminar', button_color=('white', 'red'))])
        return layout

    else:
        layout.append([sg.Frame(
            background_color=color_interface,
            layout=[
                [sg.Text('Sustantivos :', background_color=color_interface, text_color='white'),
                 sg.Text('', key='cantS', background_color=color_interface, text_color='white'),
                 sg.Text('Adjetivos :', background_color=color_interface, text_color='white'),
                 sg.Text('', key='cantA', background_color=color_interface, text_color='white'),
                 sg.Text('Verbos :', background_color=color_interface, text_color='white'),
                 sg.Text('', key='cantV', background_color=color_interface, text_color='white')],
            ], title='Cantidad de palabras a buscar ', title_color='lightgreen'
        )])
        layout.append([sg.ReadButton('Volver al menu', button_color=('white', 'orange'), key='Volver al menu'),
                       sg.Button('salir', button_color=('white', 'red')),
                       sg.Button('Verificar Palabra / Limpiar selección'),
                       sg.Button('terminar', button_color=('white', 'red'))])
        return layout


def ordenacion_horizontal(tupla):
    """
        ordena segundo elemento de la tupla de mayor a menor
    """
    return tupla[1], - tupla[0]


def ordenacion_vertical(tupla):
    """
        ordena primer elemento de la tupla de mayor a menor
    """
    return tupla[0], - tupla[1]


def armo_palabra(diccionario, coordenadas_marcadas, sentido):
    """
        deveulve una palabra segun las letras que haya en las coordenadas recibidas como parametro (todos_los_clik).
    """
    un_string = ''
    coordenadas_marcadas.sort()  # se ordena para luego poder comparar si son iguales
    if sentido:
        datos = sorted(coordenadas_marcadas, key=ordenacion_horizontal)
    else:
        datos = sorted(coordenadas_marcadas, key=ordenacion_vertical)
    for i in datos:
        un_string = un_string + diccionario[i]
    if un_string.lower() in dic_palabra_coordenada.keys():
        if dic_palabra_coordenada[un_string.lower()] == coordenadas_marcadas:
            # si la palabra se encuentra en sus coordenadas correspondientes
            return un_string.lower()
    else:
        un_string = ''
        return un_string.lower()


def definir_color(sg, un_string, verbos, adjetivos, sustantivos, lista_palabras, color_verbo, color_adjetivo,
                  color_sustantivo):
    """ recibe una palabra a buscar en el diccionario, la busca y nos retorno un valor(color) del diccionaro """
    color = 'red'
    encontre = False
    opcion = 0
    try:
        if un_string in lista_palabras:
            if un_string in verbos:
                color = color_verbo
                encontre = True
                opcion = 1
                verbos.remove(un_string)
            elif un_string in adjetivos:
                color = color_adjetivo
                encontre = True
                opcion = 2
                adjetivos.remove(un_string)
            elif un_string in sustantivos:
                color = color_sustantivo
                encontre = True
                opcion = 3
                sustantivos.remove(un_string)
            else:
                sg.Popup('La palabra no existe')
    except IndexError:
        color = 'dimgrey'
    return encontre, color, opcion


def ventana_terminar(sg, color, lista_verbo, lista_sustantivo, lista_adjetivo):
    """
         esta funcion se encarga de mostrarle la cantidad de palabras que le falto al usuario
         por encontrar, adicionalmente tambien mostrandole la palbras que no encontro
         retornado la opcion de volver al menu o finalizar
    """
    ventana = [
        [sg.Text('FIN DEL JUEGO', size=(30, 1), justification='center', font=('Helvetica', 25),
                 text_color='lightgreen', background_color=color)],
        [sg.Text(f'palabras por encontrar:', size=(30, 1), justification='center',
                 font=('Helvetica', 25), text_color='red', background_color=color)],
        [sg.Text(f"Verbos: {lista_verbo}", size=(30, 1),
                 text_color='orange', font=('Helvetica', 15), background_color=color)],
        [sg.Text(f"Sustantivos: {lista_sustantivo}", size=(30, 1),
                 text_color='orange', font=('Helvetica', 15), background_color=color)],
        [sg.Text(f"adjetivos: {lista_adjetivo}", size=(30, 1),
                 text_color='orange', font=('Helvetica', 15), background_color=color)],
        [sg.Radio('Volver al menu', "R", key='v', background_color=color, text_color='white'),
         sg.Radio('Salir del juego', "R", key='S', background_color=color, text_color='white'), sg.Button('OK')]

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
