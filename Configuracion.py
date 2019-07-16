import PySimpleGUI as sg
from modulos_configuracion import agregar_palabra
from modulos_configuracion import get_lista_resultante
from sensores.manejo_de_archivo import leer_json
from tablero import juego


def mostrar_reporte(color, fuentestitulo, fuentetexto):
    """
        :param fuentestitulo: sera la fuente para el titulo del reporte
        :param fuentetexto:  sera la fuente para contenido del reporte
        :param color: es para definir color de fondo de la interface
        :return: nada esta funcion solo se encarga de mostrarle al docente la informacion
        de las palabras que no fueron admitidas por patterns/wiki, o wiki si, patterns no, o patterns si y wiki no
    """
    try:
        a = open('reporte.txt', 'r')
        lista = a.readlines()
        layout = [
            [sg.Text('PROBLEMAS!!', size=(20, 1), font=fuentestitulo, background_color=color, text_color='white')],
            [sg.Listbox(values=lista[:], size=(70, 10), font=fuentetexto, background_color=color, text_color='white')],
            [sg.Text('', background_color=color), sg.Button('Ok')],

        ]
        window = sg.Window('Panel').Layout(layout)

        button, values = window.Read()
        if button is 'Ok':
            window.Close()
        if button is None:
            window.Close()
    except FileNotFoundError:
        sg.Popup('No hay informe de errores para mostrar', background_color=color, text_color='white', title='Reporte')


def dato_para_color_interface():
    oficina = []
    dato = leer_json('sensores/dato-oficinas.json')
    try:
        for i in dato.keys():
            oficina.append(i)
        return oficina, dato
    except FileNotFoundError:
        dato = ''
        fin = ''
        return fin, dato


def color_interface_del_tablero(lista):
    cant = 0
    for i in lista:
        cant += i['temperatura']
    temperatura = cant / len(lista)
    if temperatura >= 2 and (temperatura <= 15):
        color = '#181832'
        return color
    elif temperatura >= 16 and (temperatura <= 21):
        color = '#34240B'
        return color
    else:
        color = '#C13700'
        return color


def config():
    """
        esta funcion provee todos los datos que se necesitan para la sopa de letras
        :rtype: se limpian las listas para evitar duplicados, cuando se decide volver al menu desde el juego
        :return un diccionario con toda la informacion listas de palabras, horientacion de las mismas,
        tamanio de la matriz, que este apartado tomamos como referencioa la longitud de la palabra mas grande,
        tipo de ayuda, se debe tener encuenta que si el docente no selecciona ni una de las ayudas, se asume que el
        user no contara con ayuda y en su lugar se mostrara la cantidad de palabras a encontrar

    """
    oficina, dato = dato_para_color_interface()
    diccionario = {'colorInterface': '#001920', 'fin': 0, 'info': {}}
    color = diccionario['colorInterface']
    sg.SetOptions(background_color=color)
    fuente = 'Helvetica'
    layout = [
        [sg.InputCombo(values=('Arial', 'Comic', 'Curier'), key='titulo', size=(10, 1)),
         sg.InputCombo(values='Helvetica, Verdana, Fixedsys', size=(10, 1), key='texto'),
         sg.Button('Mostrar reporte'), sg.InputCombo(values=oficina, size=(10, 1), key='oficinaa'),
         sg.ReadButton('color_interface', key='color_interface')
         ],
        [sg.Text('Configuracion del juego', size=(30, 1), background_color=color,
                 justification='center', font=(fuente, 25), text_color='lightgreen')],
        [sg.Frame(
         background_color=color,
            layout=[
                [sg.Text('Ingrese palabra', background_color=color,
                         text_color='white', font=(fuente, 12), size=(15, 1)), sg.InputText(key='pal'),
                 sg.Button('Agregar', button_color=('white', 'orange')),
                 sg.Button('Eliminar', button_color=('white', 'red'))
                 ],
                [sg.Multiline(key='dato', size=(70, 1), font='Courier 10', background_color=color, text_color='white')],
            ], title='AgregarPalabras', title_color='lightgreen'
         )],
        [sg.Frame(
         background_color=color,
         layout=[
             [sg.Frame(
              background_color=color,
              layout=[
                  [sg.Text('Verbo:      ', text_color='white', background_color=color, font=(fuente, 12)),
                   sg.Radio('Rojo', "c", background_color=color, text_color='red', key='roVe'),
                   sg.Radio('verde', "c", background_color=color, text_color='lightgreen', key='veVe'),
                   sg.Radio('Amarillo', "c", background_color=color, text_color='yellow', key='amVe')],
                  [sg.Text('Adjetivo:   ', text_color='white', background_color=color, font=(fuente, 12)),
                   sg.Radio('Rojo', "s", background_color=color, text_color='red', key='roAd'),
                   sg.Radio('verde', "s", background_color=color, text_color='lightgreen', key='veAd'),
                   sg.Radio('Amarillo', "s", background_color=color, text_color='yellow', key='amAd')],
                  [sg.Text('Sustantivo:', text_color='white', background_color=color, font=(fuente, 12)),
                   sg.Radio('Rojo', "ad", background_color=color, text_color='red', key='roSu'),
                   sg.Radio('verde', "ad", background_color=color, text_color='lightgreen', key='veSu'),
                   sg.Radio('Amarillo', "ad", background_color=color, text_color='yellow', key='amSu')]
                  ], title='configurar-colores', font=fuente, title_color='lightgreen'
              )],
             [sg.Frame(
              background_color=color,
              layout=[
                  [sg.Text('Opciones de Ayuda', font=(fuente, 12), background_color=color, text_color='white')],
                  [sg.Radio('Mostrar palabras', "A", key='ayuda', background_color=color, text_color='white'),
                   sg.Radio('Mostrar definiciones', "D", key='def', background_color=color, text_color='white')],
              ], title='Habiltar/Deshabilitar Ayuda', font=(fuente, 12), title_color='lightgreen'
              )],
             [sg.Frame(
              background_color=color,
              layout=[
                  [sg.Radio('Mayusculas', "l", key='M', background_color=color, text_color='white'),
                   sg.Radio('Minusculas', "l", key='Mn', background_color=color, text_color='white')],
                  [sg.Radio('Habilitar Palabras en Vertical', "h", key='h', background_color=color, text_color='white'),
                   sg.Radio('Habilitar Palabras en horizontal', "h", key='v',
                            background_color=color, text_color='white')],
              ], title='configurar-orden-sentido de las palabras', font=fuente, title_color='lightgreen'
              )],
             [sg.Text('Cantidad de verbos', text_color='white', font=(fuente, 12), background_color=color),
              sg.Slider(range=(0, 20), orientation='h', size=(34, 20),
                        default_value=0, key='X1', background_color=color)],
             [sg.Text('Cantidad de sustantivos', font=(fuente, 12), text_color='white', background_color=color),
              sg.Slider(range=(0, 20), orientation='h',
                        size=(34, 20), default_value=0, key='X2', background_color=color)],
             [sg.Text('Cantidad de adjetivos', font=(fuente, 12), text_color='white', background_color=color),
              sg.Slider(range=(0, 20), orientation='h',
                        size=(34, 20), default_value=0, key='X3', background_color=color)],
         ], title='Paso final', title_color='lightgreen'
         )],
        [sg.Button('Comenzar', button_color=('white', 'orange')),
         sg.Button('Cancelar', button_color=('white', 'orange'))],
    ]
    window = sg.Window('Configuracion').Layout(layout).Finalize()
    if oficina is '' and dato is '':
        # se desabilita el botton de cambiar el color de la interface
        # por sino se localiza el archivo json
        window.FindElement('color_interface').Update(disabled=True)

    ok = True
    while ok:
        button, values = window.Read()
        if button is None or button is 'Cancelar':
            break
        if button is 'color_interface':
            lista = dato[values['oficinaa']]
            color_user = color_interface_del_tablero(lista)
            diccionario['colorInterface'] = color_user
        if button is 'Agregar':
            palabra = agregar_palabra(values['pal'], 0, diccionario['colorInterface'])
            window.FindElement('dato').Update(palabra)
        if button is 'Eliminar':
            pal = agregar_palabra(values['pal'], 1, diccionario['colorInterface'])
            window.FindElement('dato').Update(pal)
        if button is 'Mostrar reporte':
            mostrar_reporte(color, values['titulo'], values['texto'])
        if button is 'Comenzar':
            cant_v = int(values['X1'])  # SON LOS VALORES DE LOS SLIDER QUE REFERENCIAN A LAS CANTIDADES
            cant_s = int(values['X2'])  # X ES LA CANTIDAD DE CADA TIPO DE PALABRA QUE EL DOCENTE QUIERE MOSTRAR
            cant_a = int(values['X3'])
            if cant_a != 0 or cant_s != 0 or cant_v != 0:
                diccionario['fin'] = 1
                tipo_ayudas = (values['ayuda'], values['def'])
                diccionario['info'] = get_lista_resultante(cant_v, cant_a, cant_s, values['roVe'],
                                                           values['veVe'], values['amVe'], values['roSu'],
                                                           values['veSu'], values['amSu'], values['roAd'],
                                                           values['veAd'],
                                                           values['amAd'], diccionario['colorInterface'],
                                                           tipo_ayudas, values['h'], values['M'])
                if diccionario['info'] is None:
                    continue
                else:
                    window.Close()
                    break
            else:
                sg.Popup('no se puede empezar sin asignar las cantidades',
                         background_color=diccionario['colorInterface'], text_color='white', title='Error')
    return diccionario['info'], diccionario['fin'], diccionario['colorInterface']


def main():
    ok = True
    while ok:
        info, fin, color_interface = config()
        if fin == 0:
            ok = False
        else:
            opcion = juego(color_interface, info['totalPalbras'], info['max_pal'],
                           info['mayusculas'], info['sentido'], info['ayuda'], info['verbos'],
                           info['adjetivos'], info['sustantivos'], info['color_verbo'], info['color_adjetivo'],
                           info['color_sustantivo'])
            if opcion != 'jugar':
                ok = False


main()
