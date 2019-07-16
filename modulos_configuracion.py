import PySimpleGUI as sg
import random
from pattern.web import Wiktionary
from pattern.text.es import parse

dicPalabras = {'verbos': [], 'sustantivos': [], 'adjetivos': [], 'totalPalbras': [],
               'color_verbo': 'red', 'color_adjetivo': 'green', 'color_sustantivo': 'yellow',
               'max_pal': 0}


def reporte(mensaje, nombre):
    """
        recibe como parametro el nombre del archivo, se abre un contexto y solo escribie el mensaje en el arhivo
    """

    with open(nombre + '.txt', 'a+') as a:
        a.write(mensaje + '\n')


def ingresar_definicion(color_interface):
    """
        Se ingresa una definicion por teclado por el usuario
    """

    layout = [
        [sg.Text('Ingrese definicion:', size=(15, 1), background_color=color_interface, text_color='white'),
         sg.InputText(key='ms', background_color=color_interface, text_color='white'),
         sg.Button('Agregar', button_color=('white', 'orange'))]
    ]
    msj = '999'
    window = sg.Window('panel').Layout(layout)
    ok = True
    while ok:
        button, values = window.Read()
        if button is None:
            sg.Popup('Es obligatorio ingresar una definicion',
                     title='Error', text_color='red', background_color=color_interface)
            msj = ingresar_definicion(color_interface)
            break
        if button == 'Agregar':
            msj = values['ms']
            ok = False
        if msj == '':
            sg.Popup('Es obligatorio ingresar una definicion',
                     title='Error', text_color='red', background_color=color_interface)
            ok = True
    window.Close()
    return msj


def devuelve_definicion(unstring, clasificacion, color_interface):
    """
        Devuelve una definicion dada por wiktionary, en casa de que no haya se le pide al usuario que ingrese una
    """

    cat = Wiktionary(license=None, throttle=5.0, language='ES').search(unstring)
    definicion = ''
    encontre = False
    for elem in cat.sections:
        if clasificacion in elem.title.lower():
            encontre = True
        if encontre:
            definicion = elem.content.split('1')[1].split('.2')[0].split('*')[0]
            break
    if definicion == '':
        definicion = ingresar_definicion(color_interface)
    return definicion


def buscar_pattern(x):
    """
        clasifica el string recbido como paramentro(x) en pattern, analizando la palabra, devuleve su clasificacion
        sustantivo, adjetivo o verbo.
    """

    s = parse(x).split()
    for cada in s:
        for i in cada:
            if i[1] == 'VB':
                return 'VB'
            elif i[1] == 'NN':
                return 'NN'
            elif i[1] == 'JJ':
                return 'JJ'


def clasificar_pal(un_string, color_interface):
    """
        Se clasifica la palabra segun sea adjetivo, verbo o sustantivo mediante pattren.es y wiktionary
        y se agrega a sus correspondiente lista y se guarda la definicion dicha por wiktinary de la palabra,
        en caso de que no coincidan se generan reportes de las palabras que tienen conflictos entre los modulos.
        si coinside solo con Wiktionary, y no se obtiene un definicion, se pide que ingrese la definicion de la palabra
        , en los demas casos
        se tomara la definicion solo de Wiktionary y siempre se guararan en un archivo local.
    """

    pal = Wiktionary(license=None, throttle=5.0, language='ES').search(un_string)
    try:
        if un_string in dicPalabras['verbos'] or un_string in dicPalabras['adjetivos'] \
                or un_string in dicPalabras['sustantivos']:
            sg.Popup('la palabra ingresada ya existe', title='Error',
                     background_color=color_interface, text_color='red')
        else:
            secciones = []
            for section in pal.categories:
                secciones.append(section)
            if ('ES:Verbos' in secciones) and (buscar_pattern(un_string) == 'VB'):
                if un_string not in dicPalabras['verbos']:
                    dicPalabras['verbos'].append(un_string)
                    definicion = devuelve_definicion(un_string, 'verbo', color_interface)
                    reporte(definicion, 'ArchivoLocal')

            elif (buscar_pattern(un_string) != 'VB') and ('ES:Verbos' in secciones):  # si no coincide con pattern
                if un_string not in dicPalabras['verbos']:
                    dicPalabras['verbos'].append(un_string)
                    msj = f'la palabra {un_string} no se encuentra en pattern pero si en Wiktionary.\n'
                    reporte(msj, 'reporte')
                    definicion = devuelve_definicion(un_string, 'verbo', color_interface)
                    reporte(definicion, 'ArchivoLocal')

            elif 'ES:Verbos' not in secciones and buscar_pattern(un_string) == 'VB':  # si no coincide con wiktionary
                if un_string not in dicPalabras['verbos']:
                    dicPalabras['verbos'].append(un_string)
                    msj = ingresar_definicion(color_interface)
                    reporte(msj, 'ArchivoLocal')

            elif 'ES:Adjetivos' in secciones and buscar_pattern(un_string) == 'JJ':
                if un_string not in dicPalabras['adjetivos']:
                    dicPalabras['adjetivos'].append(un_string)
                    definicion = devuelve_definicion(un_string, 'adjetivo', color_interface)
                    reporte(definicion, 'ArchivoLocal')

            elif buscar_pattern(un_string) != 'JJ' and 'ES:Adjetivos' in secciones:
                if un_string not in dicPalabras['adjetivos']:
                    dicPalabras['adjetivos'].append(un_string)
                    msj = f'la palabra {un_string} no se encuentra en pattern pero si en Wiktionary.\n'
                    reporte(msj, 'reporte')
                    definicion = devuelve_definicion(un_string, 'adjetivo', color_interface)
                    reporte(definicion, 'ArchivoLocal')

            elif 'ES:Adjetivos' not in secciones and buscar_pattern(un_string) == 'JJ':
                if un_string not in dicPalabras['adjetivos']:
                    dicPalabras['adjetivos'].append(un_string)
                    msj = ingresar_definicion(color_interface)
                    reporte(msj, 'ArchivoLocal')

            elif 'ES:Sustantivos' in secciones and buscar_pattern(un_string) == 'NN':
                if un_string not in dicPalabras['sustantivos']:
                    dicPalabras['sustantivos'].append(un_string)
                    definicion = devuelve_definicion(un_string, 'sustantivo', color_interface)
                    reporte(definicion, 'ArchivoLocal')

            elif buscar_pattern(un_string) != 'NN' and 'ES:Sustantivos' in secciones:
                if un_string not in dicPalabras['sustantivos']:
                    dicPalabras['sustantivos'].append(un_string)
                    msj = f'la palabra {un_string} no se encuentra en pattern pero si en Wiktionary.\n'
                    reporte(msj, 'reporte')
                    definicion = devuelve_definicion(un_string, 'sustantivo', color_interface)
                    reporte(definicion, 'ArchivoLocal')

            elif 'ES:Sustantivos' not in secciones and buscar_pattern(un_string) == 'NN':
                if un_string not in dicPalabras['sustantivos']:
                    dicPalabras['sustantivos'].append(un_string)
                    msj = ingresar_definicion(color_interface)
                    reporte(msj, 'ArchivoLocal')
            else:
                msj = f'la palabra {un_string} no se encuentra en pattern y tampoco en Wiktionary.\n'
                sg.Popup(f'la palabra {un_string}, no existe en pattern y tampoco en Wiktionary',
                         background_color=color_interface, text_color='white', title='Error')
                reporte(msj, 'reporte')
    except AttributeError:
        sg.Popup('Ingrese una palabra valida', background_color=color_interface, text_color='white')


def eliminar_palabra(palabra, color_interface):
    """
        este modulo elimina una palabra que se recibe por parametro,
        e informa de que tipo de palabra fue la que se elimino
    """
    if palabra in dicPalabras['adjetivos']:
        dicPalabras['adjetivos'].remove(palabra)
        sg.Popup(' la palabra que se elimino es un adjetivo',
                 background_color=color_interface, text_color='white', title='Informe')
    elif palabra in dicPalabras['sustantivos']:
        dicPalabras['sustantivos'].remove(palabra)
        sg.Popup(' la palabra que se elimino es un sustantivo',
                 background_color=color_interface, text_color='white', title='Informe')
    elif palabra in dicPalabras['verbos']:
        dicPalabras['verbos'].remove(palabra)
        sg.Popup(' la palabra que se elimino es un verbo',
                 background_color=color_interface, text_color='white', title='Informe')
    else:
        sg.Popup(f'la palabra {palabra}, no existe',
                 background_color=color_interface, text_color='white', title='Error')


def agregar_palabra(un_string, opcion, fondo_interface):
    """
        esta funcion se encarga de clasificar una palabra que se recibe como parametro,
        para esto interactua con una funcion que evalua la palabra segun su tipo, y la almacena en una lista
        correspondiente a su tipo(verbo, adjetivo o sustantivo)
    """
    pal = un_string.lower()
    if pal.isalpha() and pal != '':
        resultado = ''
        if opcion == 0:
            clasificar_pal(pal, fondo_interface)
            dicPalabras['totalPalbras'] = dicPalabras['verbos'] + dicPalabras['adjetivos'] + dicPalabras['sustantivos']
            resultado = ', '.join(['{}'.format(o) for o in dicPalabras['totalPalbras']])
        elif opcion == 1:
            eliminar_palabra(pal, fondo_interface)
            dicPalabras['totalPalbras'] = dicPalabras['verbos'] + dicPalabras['adjetivos'] + dicPalabras['sustantivos']
            resultado = ', '.join(['{}'.format(o) for o in dicPalabras['totalPalbras']])
        return resultado
    else:
        sg.Popup(f'No se admiten numeros, ni espacios en blanco',
                 background_color=fondo_interface, text_color='white', title='Error')


def limitaciones(cant, tipo):
    """
    recibe una cantidad y un tipo de palabra, se limitan las palabras segun la cantidad recibida como parametro. Retorna una lista por si
    la cantidad que se elije, es incorrecta, es decir la lista correspondiente no tiene datos, entonces se salvan los datos. 
    """
    lista = []
    while True:
        if cant < len(dicPalabras[tipo]) and cant != 0:
            pal = random.choice(dicPalabras[tipo])
            dicPalabras[tipo].remove(pal)
            cant -= 1
            if cant == 0:
                break
        else:
            if cant == 0:
                lista = dicPalabras[tipo]
                dicPalabras[tipo] = dicPalabras[tipo][:cant]
                break
            else:
                if len(dicPalabras[tipo]) == 0:
                    break
                else:
                    break
    return lista


def get_lista_resultante(cant_v, cant_a, cant_s, rojo_v, verde_v, yellow_v,
                         rojo_s, verde_s, yellow_s, rojo_ad, verde_ad, yellow_ad,
                         color_interface, tipo_de_ayuda, sentido, mayuscula):
    """
        cant_v --> LIMITE DE VERBOS
        cant_a --> LIMITE DE ADJETIVOS
        cant_s --> LIMITE DE SUSTANTIVOS
        esta funcion asigna los colores, tipo de ayuda, orientacion de las palabras, si es mayuscula o minuscula.
        En caso de que el usuario no seleccione la informacion se asignarán valores por defecto, solo las cantidades son obligatorias
        retorna un diccionario con toda la informacion

    """
    sin_marcar1 = True
    sin_marcar2 = True
    sin_marcar3 = True
    sus = limitaciones(cant_s, 'sustantivos')
    ad = limitaciones(cant_a, 'adjetivos')
    ve = limitaciones(cant_v, 'verbos')
    if len(dicPalabras['verbos']) == 0 and len(dicPalabras['sustantivos']) == 0 and len(dicPalabras['adjetivos']) == 0:
        sg.Popup('No se pueden cargar datos vacios al tablero vuelva a intentar asignar las cantidades',
                 background_color=color_interface, text_color='white', title='Error')
        dicPalabras['verbos'] = ve
        dicPalabras['sustantivos'] = sus
        dicPalabras['adjetivos'] = ad
    else:
        dicPalabras['totalPalbras'] = dicPalabras['verbos'] + dicPalabras['adjetivos'] + dicPalabras['sustantivos']
        max_pal = max(dicPalabras['totalPalbras'], key=len)
        dicPalabras['ayuda'] = tipo_de_ayuda
        dicPalabras['sentido'] = sentido
        dicPalabras['mayusculas'] = mayuscula
        if rojo_v:
            dicPalabras['color_verbo'] = 'red'
            sin_marcar1 = False
        elif verde_v:
            dicPalabras['color_verbo'] = 'green'
            sin_marcar1 = False
        elif yellow_v:
            dicPalabras['color_verbo'] = 'yellow'
            sin_marcar1 = False

        if rojo_s:
            dicPalabras['color_sustantivo'] = 'red'
            sin_marcar2 = False
        elif verde_s:
            dicPalabras['color_sustantivo'] = 'green'
            sin_marcar2 = False
        elif yellow_s:
            dicPalabras['color_sustantivo'] = 'yellow'
            sin_marcar2 = False

        if rojo_ad:
            dicPalabras['color_adjetivo'] = 'red'
            sin_marcar3 = False
        elif verde_ad:
            dicPalabras['color_adjetivo'] = 'green'
            sin_marcar3 = False
        elif yellow_ad:
            dicPalabras['color_adjetivo'] = 'yellow'
            sin_marcar3 = False

        if sin_marcar1 and sin_marcar2 and sin_marcar3:
            sg.Popup(f'No ha seleccionado ni un color,'
                     f' por defecto se le asignaran colores de forma preterminada por la app',
                     background_color=color_interface, text_color='white', title='Aviso')
        dicPalabras['max_pal'] = len(max_pal)

        return dicPalabras
