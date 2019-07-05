import PySimpleGUI as sg
from modulos import clasificar_pal
from modulos import getListaResultante
from modulos import mostrar_palabra, limpiarL
from modulos import eliminarPalabra
from juego import tablero
from sensores.manejo_de_archivo import leer_json
import sys


def cambiar_color(dic_json,clave):
    """
    devuelve un color segun la temperatura registrada
    """
    try :
        color = 'Dark'
        if dic_json[clave]["temperatura"] < 10:
            color = 'BlueMono'
        elif dic_json[clave]["temperatura"] in range(11,21):
            color = 'GreenMono'
        elif dic_json[clave]["temperatura"] in range(21,31):
            color = 'Kayak'
        return color
    except FileNotFoundError:
        sg.Popup('no se encuentra el archvio json')



def mostrar_reporte(fuentesTitulo, fuenteTexto):
    """
        :param fuentesTitulo: sera la fuente para el titulo del reporte
        :param fuenteTexto:  sera la fuente para contenido del reporte
        :return: nada esta funcion solo se encarga de mostrarle al docente la informacion
        de las palabras que no fueron admitidas por patterns/wiki, o wiki si, patterns no, o patterns si y wiki no
    """
    try:
        a = open('reporte.txt', 'r')
        lista = a.readlines()
        layout = [
            [sg.Text('PROBLEMAS!!', size=(20, 1), font=fuentesTitulo)],
            [sg.Listbox(values=lista[:], size=(70, 10), font=fuenteTexto)],
            [sg.Text(''), sg.ReadButton('Ok')],

        ]
        window = sg.Window('panel').Layout(layout)

        button, values = window.Read()
        if button is 'Ok':
            window.Close()
        if button is None:
            window.Close()
    except FileNotFoundError:
        sg.Popup('No hay informe de errores para mostrar')


def config():
    """
        Los colores configurados para el tipo de palabra podran ser diferentes o iguales.
        esta funcion provee todos los datos que se necesitan para la sopa de letras
        :returns un diccionario con toda la informacion listas de palabras, horientacion de las mismas,
        tamanio de la matriz, que este apartado tomamos como referencioa la longitud de la palabra mas grande,
        tipo de ayuda, se debe tener encuenta que si el docente no selecciona ni una de las ayudas, se asume que el
        user no contara con ayuda y en su lugar se mostrara la cantidad de palabras a encontrar

    """
    diccionario = {}
    diccionario['fin'] = 0
    color_interfaz = 'Dark'
    sg.ChangeLookAndFeel(color_interfaz)
    fuente = 'Helvetica'
    datos = leer_json('sensores\dato-oficinas.json')
    claves = list(datos.keys())
    layout = [[sg.InputCombo(values=('Arial', 'Comic', 'Curier'), key='titulo', size=(10, 1)), sg.InputCombo(values=('Helvetica, Verdana, Fixedsys'), size=(10, 1), key='texto'), sg.Button('Mostrar reporte'), sg.Button('Cambiar color para Tablero'),sg.Listbox(values=(claves),key='claves')],
              [sg.Text('Configuracion del juego', size=(30, 1), justification='center', font=(fuente, 25), text_color='lightgreen')],
              [sg.Frame(
                  layout=[
                            [sg.Text('Ingrese palabra', font=(fuente,12), size=(15, 1)), sg.InputText(key='pal'), sg.Button('Agregar', button_color=('white', 'orange')), sg.Button('Eliminar', button_color=('white', 'red'))],
                            [sg.Multiline(key='dato', size=(70,1), font='Courier 10')],
                         ], title='AgregarPalabras', title_color='lightgreen'
              )],
              [sg.Frame(
                  layout=[
                            [sg.Frame(
                                layout=[
                                            [sg.Text('Verbo:      ', font=(fuente, 12)), sg.Radio('Rojo', "c", text_color='red', key='roVe'), sg.Radio('verde', "c", text_color='lightgreen', key='veVe'), sg.Radio('Amarillo', "c", text_color='yellow', key='amVe')],
                                            [sg.Text('Adjetivo:   ', font=(fuente, 12)), sg.Radio('Rojo', "s", text_color='red', key='roAd'), sg.Radio('verde', "s", text_color='lightgreen', key='veAd'), sg.Radio('Amarillo', "s", text_color='yellow', key='amAd')],
                                            [sg.Text('Sustantivo:', font=(fuente, 12)), sg.Radio('Rojo', "ad", text_color='red', key='roSu'), sg.Radio('verde', "ad", text_color='lightgreen', key='veSu'), sg.Radio('Amarillo', "ad", text_color='yellow', key='amSu')]
                                        ], title='configurar-colores', font=(fuente), title_color='lightgreen'
                            )],
                            [sg.Frame(
                                layout=[
                                            [sg.Text('Opciones de Ayuda', font=(fuente, 12))],
                                            [sg.Radio('Mostrar palabras', "A", key='ayuda'), sg.Radio('Mostrar definiciones', "D", key='def')],
                                         ], title='Habiltar/Deshabilitar Ayuda', font=(fuente, 12), title_color='lightgreen'
                            )],
                            [sg.Frame(
                                layout=[
                                            [sg.Radio('Mayusculas', "l", key='M'), sg.Radio('Minusculas', "l", key='Mn')],
                                            [sg.Radio('Habilitar Palabras en Vertical', "h", key='h'), sg.Radio('Habilitar Palabras en horizontal', "h", key='v')],
                                         ], title='configurar-orden-sentido de las palabras', font=(fuente), title_color='lightgreen'
                            )],
                            [sg.Text('Cantidad de verbos', font=(fuente,12)), sg.Slider(range=(0, 20), orientation='h', size=(34, 20), default_value=0, key='X1')],
                            [sg.Text('Cantidad de sustantivos', font=(fuente,12)), sg.Slider(range=(0, 20), orientation='h', size=(34, 20), default_value=0, key='X2')],
                            [sg.Text('Cantidad de adjetivos', font=(fuente,12)), sg.Slider(range=(0, 20), orientation='h', size=(34, 20), default_value=0, key='X3')],
                         ], title='Paso final', title_color='lightgreen'
              )],
              [sg.Button('Comenzar', button_color=('white', 'orange')),  sg.Button('Cancelar', button_color=('white', 'orange'))],
    ]
    window = sg.Window('panel').Layout(layout)
    ok = True
    while ok:
        try:
            button, values = window.Read()
            if button is None or button is 'Cancelar':
                break
            if button is 'Agregar':
                palabra = mostrar_palabra(values['pal'])
                window.FindElement('dato').Update(palabra)
                clasificar_pal(values['pal'])
            if button is 'Eliminar':
                try:
                    pal = eliminarPalabra(values['pal'])
                    window.FindElement('dato').Update(pal)
                except UnboundLocalError:
                    sg.PopupError('se debe ingresar una palabra valida')
                    continue
            if button is 'Comenzar':
                cantV = int(values['X1'])  # SON LOS VALORES DE LOS SLIDER QUE REFERENCIAN A LAS CANTIDADES
                cantS = int(values['X2'])  # X DE CADA TIPO DE PALABRA QUE EL DOCENTE QUIERE MOSTRAR
                cantA = int(values['X3'])
                if cantA != 0 or cantS != 0 or cantV != 0:
                    dic, lisR = getListaResultante(cantV, cantA, cantS, values['roVe'], values['veVe'], values['amVe'], values['roSu'], values['veSu'], values['amSu'], values['roAd'], values['veAd'], values['amAd'])
                    TipoAyudas = (values['ayuda'], values['def'])
                    diccionario['listaPal'] = lisR
                    diccionario['tam'] = dic['maxPal']
                    diccionario['palabras'] = dic
                    diccionario['ayudas'] = TipoAyudas
                    diccionario['sentidos'] = values['h']
                    diccionario['Mayusculas'] = values['M']
                    diccionario['fin'] = 1
                    limpiarL()
                    window.Close()
                    break
                else:
                    sg.Popup('Como minimo debe ingresar una palabra')
            if button is 'Cancelar':
                window.Close()
                break
            if button is 'Mostrar reporte':
                mostrar_reporte(values['titulo'], values['texto'])
        except ValueError:
            sg.Popup('Todos los campos son obligatorios.')
        if button is 'Cambiar color para Tablero'and values['claves']:
            color_interfaz = cambiar_color(datos,values['claves'][0])
            sg.ChangeLookAndFeel(color_interfaz)
    return diccionario, color_interfaz


def main():
    """
        :return: nada esta funcion solo se encarga de interactuar con los modulos, dependiendo de su resultado
        se continura con el bucle o se finalizara el mismo si es lo que se desea
    """
    ok = True
    while ok:
        info,color_interfaz = config()
        if info['fin'] == 0:
            sys.exit()
        else:
            opcion = tablero(color_interfaz,info['listaPal'],info['tam'], info['palabras'], info['Mayusculas'], info['sentidos'], info['ayudas'])
            if opcion is 'jugar':
                info['palabras']['palVer'].clear()
                info['palabras']['palSus'].clear()
                info['palabras']['palAd'].clear()
                ok = True
            else:
                break
main()