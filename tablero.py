import PySimpleGUI as sg
from modulos_tablero import procesar_palabras, completar_matriz, crear_matriz, graficar_matrix
from modulos_tablero import determinar_ayuda, armo_palabra, definir_color, obtener_datos_arch, ventana_terminar
caja = 32


def asignar_datos(window, tipo_ayuda, lista_palabras, definiciones, tamanio_verbos, tamanio_adjetivos,
                  tamanio_sustantivos):
    if tipo_ayuda[0] and tipo_ayuda[1]:
        window.FindElement('ayuda').Update(lista_palabras)
        window.FindElement('def').Update(definiciones)
    elif tipo_ayuda[0]:
        window.FindElement('ayuda').Update(lista_palabras)
    elif tipo_ayuda[1]:
        window.FindElement('def').Update(definiciones)
    else:
        window.FindElement('cantS').Update(tamanio_sustantivos)
        window.FindElement('cantV').Update(tamanio_verbos)
        window.FindElement('cantA').Update(tamanio_adjetivos)


def juego(color_interface, lista_palabras, longitud, mayusculas, sentido, tipo_ayuda, lista_verbos, lista_adjetivos,
          lista_sustantivos, color_verbo, color_adjetivo, color_sustantivo):
    """
       en esta funcion se encarga de armar la interface del tablero, e interactuar con todos lo modulos
       iniciando con la creacion de nuestra matriz, para esto se toma la longitud de la palabra mas grande + 4
       para darle mas espacion y mejor distribucion a las palabras(param lnue),
        siguiendo con el procesamiento de estas misma,
       depues completando la matriz con letras random, y finalmente graficandola, depues de eso, en esta funcion,
       tambien maneja toda la interaccion del jugador con el tablero mapiando los click e evaluando la palabras,
       el tipo de ayuda que este recibe(param tipoAyuda), el sentido en el que se le van a mostrar la palabras(param ok)
    """
    sg.SetOptions(background_color=color_interface)
    layout = [
        [sg.Text('sopa de letras', text_color='white', background_color=color_interface)],
        [sg.Graph((430, 430), (0, 450), (450, 0), key='_dibujar_',
                  change_submits=True, drag_submits=False, background_color=color_interface)],
    ]
    ventana = determinar_ayuda(sg, layout, tipo_ayuda, color_interface)
    window = sg.Window('panel').Layout(ventana).Finalize()
    g = window.FindElement('_dibujar_')
    window.FindElement('Volver al menu').Update(disabled=True)
    window.FindElement('salir').Update(disabled=True)
    if longitud >= 8:
        nxn = longitud + 2  # longuitud de la palabra mas larga
    else:
        nxn = longitud + 4  # longuitud de la palabra mas larga
    matriz = crear_matriz(nxn)
    matriz = procesar_palabras(matriz, nxn, lista_palabras, sentido)
    dato = completar_matriz(matriz, nxn)
    dic_color, dic = graficar_matrix(color_interface, dato, nxn, g, mayusculas)
    coordenadas_marcadas = []  # es para todas las cooredenadas donde se hizo click en el tablero
    coordenadas_encontradas = []
    tamanio_verbos = len(lista_verbos)
    tamanio_adjetivos = len(lista_adjetivos)
    tamanio_sustantivos = len(lista_sustantivos)
    def_pal = obtener_datos_arch('ArchivoLocal.txt')  # SE OBTIENEN LAS DEFINICIONES GUARDADAS EN UN ARCHIVO LOCAL
    asignar_datos(window, tipo_ayuda, lista_palabras, def_pal, tamanio_verbos,
                  tamanio_adjetivos, tamanio_sustantivos)
    while True:
        button, values = window.Read()
        if button is None or button is 'salir':
            break
        puntero = values['_dibujar_']
        if button is '_dibujar_':
            if puntero == (None, None):
                continue
            coor_x = puntero[0] // caja
            coor_y = puntero[1] // caja
            click = (coor_x, coor_y)
            # ------------marcar y desmarcar letras------------#
            if click in dic.keys():
                if click in coordenadas_encontradas:
                    continue
                elif click not in coordenadas_marcadas:
                    g.TKCanvas.itemconfig(dic_color[click], fill="blue")
                    coordenadas_marcadas.append(click)  # coordenadas seleccionadas
                else:
                    g.TKCanvas.itemconfig(dic_color[click], fill=color_interface)
                    coordenadas_marcadas.remove(click)
        if button == 'Verificar Palabra / Limpiar selección':
            un_strin = armo_palabra(dic, coordenadas_marcadas, sentido)
            encontre, color_palabra, opcion = definir_color(sg, un_strin, lista_verbos, lista_adjetivos,
                                                            lista_sustantivos, lista_palabras,
                                                            color_verbo, color_adjetivo, color_sustantivo)
            if encontre:
                sg.Popup(f'Has Encontrado la palabra {un_strin}', text_color='orange', title='BIEN',
                         background_color=color_interface)
                for i in coordenadas_marcadas:
                    g.Update(g.TKCanvas.itemconfig(dic_color[i], fill=color_palabra))
                    coordenadas_encontradas.append(i)
                lista_palabras.remove(un_strin)  # se van eliminando las palabras encontradas

                if tipo_ayuda[0]:
                    window.FindElement('ayuda').Update(lista_palabras)
                    if len(lista_palabras) == 0:
                        sg.Popup('¡¡Has encontrado todas las palabras!!', title='Crack!',
                                 background_color=color_interface, text_color='white')
                        window.FindElement('Volver al menu').Update(disabled=False)
                        window.FindElement('salir').Update(disabled=False)
                        window.FindElement('terminar').Update(disabled=True)

                elif tipo_ayuda[0] and tipo_ayuda[1]:
                    window.FindElement('ayuda').Update(lista_palabras)
                    if len(lista_palabras) == 0:
                        sg.Popup('¡¡Has encontrado todas las palabras!!', title='Crack!',
                                 background_color=color_interface, text_color='white')
                        window.FindElement('Volver al menu').Update(disabled=False)
                        window.FindElement('salir').Update(disabled=False)
                        window.FindElement('terminar').Update(disabled=True)

                elif tipo_ayuda[1]:
                    if len(lista_palabras) == 0:
                        sg.Popup('¡¡Has encontrado todas las palabras!!', title='Crack!',
                                 background_color=color_interface, text_color='white')
                        window.FindElement('Volver al menu').Update(disabled=False)
                        window.FindElement('salir').Update(disabled=False)
                        window.FindElement('terminar').Update(disabled=True)

                else:
                    if opcion == 1:
                        tamanio_verbos -= 1
                        window.FindElement('cantV').Update(tamanio_verbos)
                    elif opcion == 2:
                        tamanio_adjetivos -= 1
                        window.FindElement('cantA').Update(tamanio_adjetivos)
                    else:
                        tamanio_sustantivos -= 1
                        window.FindElement('cantS').Update(tamanio_sustantivos)
                un_strin = ''
                coordenadas_marcadas.clear()
            else:
                # -------Se limpia_todo lo que haya sido seleccionado--------#
                sg.Popup(f'la palabra no existe', text_color='lightgreen',
                         title='ERROR', font='Curier', background_color=color_interface)
                for i in coordenadas_marcadas:
                    g.Update(g.TKCanvas.itemconfig(dic_color[i], fill=color_interface))
                coordenadas_marcadas.clear()
                un_strin = ''
            if tamanio_verbos == 0 and tamanio_adjetivos == 0 and tamanio_sustantivos == 0:
                window.FindElement('Volver al menu').Update(disabled=False)
                window.FindElement('salir').Update(disabled=False)
                window.FindElement('terminar').Update(disabled=True)
                sg.Popup('¡¡Has encontrado todas las palabras!!', title='Crack!',
                         background_color=color_interface, text_color='white')
        c = ''
        if button is 'terminar':
            var = ventana_terminar(sg, color_interface, lista_verbos, lista_sustantivos, lista_adjetivos)
            lista_adjetivos.clear()
            lista_sustantivos.clear()
            lista_verbos.clear()
            if var is 'jugar':
                window.Close()
                return var
            else:
                window.Close()
                return c
        if button == 'Volver al menu':
            c = 'jugar'
            window.Close()
            return c
    window.Close()
