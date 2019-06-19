import PySimpleGUI as sg
from modulos import clasificar_pal
from modulos import getListaResultante
from modulos import mostrar_palabra
from modulos import eliminarPalabra
from juego import tablero
import sys



def config():
    diccionario = {}
    diccionario['fin'] = 0
    sg.ChangeLookAndFeel('Dark')
    fuente = 'Helvetica'
    layout = [
              [sg.Text('Configuracion del juego', size=(30, 1), justification='center', font=(fuente, 25), text_color='lightgreen')],
              [sg.Frame(
                  layout=[
                            [sg.Text('Ingrese palabra',font=(fuente,12), size=(15, 1)), sg.InputText(key='pal'), sg.Button('Agregar', button_color=('white', 'orange')), sg.Button('Eliminar', button_color=('white', 'red'))],
                            [sg.Multiline(key='dato', size=(70,1), font='Courier 10')],
                         ], title='AgregarPalabras', title_color='lightgreen'
              )],
              [sg.Frame(
                  layout=[
                            [sg.Frame(
                                layout = [
                                            [sg.Text('Verbo:      ',font=(fuente, 12)), sg.Radio('Rojo', "c", text_color='red', key='roVe'), sg.Radio('verde', "c", text_color='lightgreen', key='veVe'), sg.Radio('Amarillo', "c", text_color='yellow', key='amVe')],
                                            [sg.Text('Adjetivo:   ',font=(fuente,12)), sg.Radio('Rojo', "s", text_color='red', key='roAd'), sg.Radio('verde', "s", text_color='lightgreen', key='veAd'), sg.Radio('Amarillo', "s", text_color='yellow', key='amAd')],
                                            [sg.Text('Sustantivo:',font=(fuente,12)), sg.Radio('Rojo', "ad", text_color='red', key='roSu'), sg.Radio('verde', "ad", text_color='lightgreen', key='veSu'), sg.Radio('Amarillo', "ad", text_color='yellow', key='amSu')]
                                        ], title = 'configurar-colores',font=(fuente), title_color = 'lightgreen'
                            )],
                            [sg.Frame(
                                layout = [
                                            [sg.Text('Opciones de Ayuda',font=(fuente,12))],
                                            [sg.Radio('Mostrar palabras', "A", key='ayuda'),sg.Radio('Mostrar definiciones', "D", key='def')],
                                         ], title = 'Habiltar/Deshabilitar Ayuda',font=(fuente,12), title_color = 'lightgreen'
                            )],
                            [sg.Frame(
                                layout = [
                                            [sg.Radio('Mayusculas', "l", key='M'), sg.Radio('Minusculas', "l", key='Mn')],
                                            [sg.Radio('Habilitar Palabras en Vertical', "h", key='h'), sg.Radio('Habilitar Palabras en horizontal', "h", key='v')],
                                         ], title = 'configurar-orden-sentido de las palabras',font=(fuente), title_color = 'lightgreen'
                            )],
                            [sg.Text('Cantidad de verbos',font=(fuente,12)), sg.Slider(range=(0, 20), orientation='h', size=(34, 20), default_value=0, key='X1')],
                            [sg.Text('Cantidad de sustantivos',font=(fuente,12)), sg.Slider(range=(0, 20), orientation='h', size=(34, 20), default_value=0, key='X2')],
                            [sg.Text('Cantidad de adjetivos',font=(fuente,12)), sg.Slider(range=(0, 20), orientation='h', size=(34, 20), default_value=0, key='X3')],
                         ], title='Paso final', title_color='lightgreen'
              )],
              [sg.Button('Comenzar', button_color=('white', 'orange')),  sg.Button('Cancelar', button_color=('white', 'orange'))],
             ]
    window = sg.Window('panel').Layout(layout)
    ok = True
    while ok:
        try:
            button, values =  window.Read()
            if button is None or button is 'Cancelar':
                break
            if button is 'Agregar':
                palabra = mostrar_palabra(values['pal'])
                window.FindElement('dato').Update(palabra)
                clasificar_pal(values['pal'])
            if button is 'Eliminar':
                pal = eliminarPalabra(values['pal'])
                window.FindElement('dato').Update(pal)
            if button is 'Comenzar':
                cantV = int(values['X1'])  # SON LOS VALORES DE LOS SLIDER QUE REFERENCIAN A LAS CANTIDADES
                cantS = int(values['X2'])  # X DE CADA TIPO DE PALABRA QUE EL DOCENTE QUIERE MOSTRAR
                cantA = int(values['X3'])
                dic = getListaResultante(cantV, cantA, cantS, values['roVe'], values['veVe'], values['amVe'], values['roSu'], values['veSu'], values['amSu'], values['roAd'], values['veAd'], values['amAd'])
                TipoAyudas = (values['ayuda'],values['def'])
                diccionario['tam'] = dic['maxPal']
                diccionario['palabras'] = dic
                diccionario['ayudas'] = TipoAyudas
                diccionario['sentidos'] = values['h']
                diccionario['Mayusculas'] = values['M']
                diccionario['fin'] = 1
                window.Close()
                break
            if button is 'Cancelar':
                window.Close()
                break
        except ValueError:
            sg.Popup('Todos los campos son obligatorios.')
    return diccionario


def main():

    ok = True
    while ok:
        info = config()
        if info['fin'] == 0:
            sys.exit()
        else:
            opcion = tablero(info['tam'],info['palabras'],info['Mayusculas'],info['sentidos'],info['ayudas'])
            if opcion is 'jugar':
                continue
            else:
                break


main()
