from pattern.web import Wiktionary
import PySimpleGUI as sg
from pattern.text.es import parse, split

lista_verbos = []
lista_adjetivos = []
lista_sustantivos = []
lista_palabras = []

dicGeneral = {}
# -------------------
l_palAbuscar_verbo = []
l_palAbuscar_sus = []
l_palAbuscar_ad = []


def mostrar_palabra (pal):
    '''
        agrego la palabra una lista general,
        para asi poder formatear su salida en la ventana,
        y tener un control de todas las palabras que se ingresaron, si
        el docente, decide eliminar un palabra lo pueda hacer sin problemas
        ademas, de eliminarse en la lista general, se verificara en las listas correspondientes
        a esa palabras, si existe se eliminan tambien, sino sale un cartel de alerta
    '''
    lista_palabras.append(pal)
    resultado = ', '.join(['{}'.format(o) for o in lista_palabras])
    return resultado


def eliminarPalabra(palabra):
    '''
        este modulo elimina una palabra que se recibe por parametro,
        e informa de que tipo de palabra fue la que se elimino
    '''
    if palabra in lista_palabras:
        lista_palabras.remove(palabra)
        pal = ', '.join(['{}'.format(o) for o in lista_palabras])
    if palabra in lista_adjetivos:
        lista_adjetivos.remove(palabra)
        sg.Popup(' la palabra que se elimino es un adjetivo')
    elif palabra in lista_sustantivos:
        lista_sustantivos.remove(palabra)
        sg.Popup('la palabra que se elimino es un sustantivo')
    elif palabra in lista_verbos:
        lista_verbos.remove(palabra)
        sg.Popup('la palabra que se elimino es un verbo')
    else:
        sg.PopupError('la palabra ingresada no existe!')
    return pal


def getListaResultante(lv, la, ls, rV, vV, aV, rSus, vSus, aSus, rAd, vAd, aAd):
    '''
        lv --> LIMITE DE VERBOS
        la --> LIMITE DE ADJETIVOS
        ls --> LIMITE DE SUSTANTIVOS
        retorna la lista resultante con las palabras
        segun la cantidad a la que el docente lo haya limitado
        es decir ej:
        si selecciona 3 verbos, 2 sustantivos, 1 adjetivo

    '''
    l_palAbuscar_verbo.append(lista_verbos[ : lv])
    l_palAbuscar_ad.append(lista_adjetivos[ : la])
    l_palAbuscar_sus.append(lista_sustantivos[ : ls])
    lisR =  lista_verbos[ : lv] + lista_adjetivos[ : la] + lista_sustantivos[ : ls]
    maxPal = max(lisR, key=len)
    dic = {}
    if rV:
        dic['verbo'] = 'red'
        dic['palVer'] = l_palAbuscar_verbo
    elif vV:
        dic['verbo'] = 'green'
        dic['palVer'] = l_palAbuscar_verbo
    elif aV:
        dic['verbo'] = 'yellow'
        dic['palVer'] = l_palAbuscar_verbo

    if rSus:
        dic['sustantivo'] = 'red'
        dic['palSus'] = l_palAbuscar_sus
    elif vSus:
        dic['sustantivo'] = 'green'
        dic['palSus'] = l_palAbuscar_sus
    elif aSus:
        dic['sustantivo'] = 'yellow'
        dic['palSus'] = l_palAbuscar_sus
        
    if rAd:
        dic['adjetivo'] = 'red'
        dic['palAd'] = l_palAbuscar_ad
    elif vAd:
        dic['adjetivo'] = 'green'
        dic['palAd'] = l_palAbuscar_ad
    elif aAd:
        dic['adjetivo'] = 'yellow'
        dic['palAd'] = l_palAbuscar_ad
    dic['maxPal']=len(maxPal)
    return dic



def buscar_pattern(x):

    '''
    clasifica el string recbido como paramentro(x) en pattern, analizando la palabra, devuleve su clasificacion
    sustantivo, adjetivo o verbo.
    '''

    s = parse(x).split()
    for cada in s:
            for i in cada:
                if i[1] == 'VB':
                    return 'VB'
                elif i[1] == 'NN':
                    return 'NN'
                elif i[1] == 'JJ':
                    return 'JJ'



def reporte (mensaje,nombre):

    '''
    recibe como parametro el nombre del archivo, se abre un contexto y solo escribie el mensaje en el arhivo
    '''

    with open(nombre + '.txt','a+') as a:
        a.write(mensaje+'\n')



def ingresar_definicion ():

    '''
    Se ingresa una definicion por teclado por el usuario
    '''

    layout = [[sg.Text('Ingrese definicion:', size=(15, 1)), sg.InputText(key='ms'), sg.Button('Agregar', button_color=('white', 'orange')),sg.Button('Cancelar', button_color=('white', 'orange'))]
    ]
    window = sg.Window('panel').Layout(layout)
    ok=True
    while ok:
        button, values =  window.Read()
        if button == 'Agregar':
            msj = values['ms']
            ok = False
        if button is None or button is 'Cancelar':
            break
            msj = ''
    window.Close()
    try:
        return msj
    except UnboundLocalError:
        None




def devuelve_definicion(unstring, clasificacion):

    '''
    Devuelve una definicion dada por wiktionary, en casa de que no haya se le pide al usuario que ingrese una
    '''

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
        definicion = ingresar_definicion()
    return definicion



def clasificar_pal(Un_string):
    '''

    #Se clasifica la palabra segun sea adjetivo, verbo o sustantivo mediante pattren.es y wiktionary
    y se agrega a sus correspondiente lista y se guarda la definicion dicha por wiktinary de la palabra,
    en caso de que no coincidan se generan reportes de las palabras que tienen conflictos entre los modulos.
    #si coinside solo con Wiktionary, se pide que ingrese la definicion de la palabra, en los demas casos
    se tomara la definicion solo de Wiktionary y siempre se guararan en un archivo local.
    '''


    pal = Wiktionary(license=None, throttle=5.0, language='ES').search(Un_string)
    try:
        secciones=[]
        ok = False
        for section in pal.categories:
            secciones.append(section)
        if ('ES:Verbos' in secciones) and (buscar_pattern(Un_string) == 'VB'):
            if Un_string not in lista_verbos:
                lista_verbos.append(Un_string)
                definicion = devuelve_definicion(Un_string,'verbo')
                reporte(definicion,'ArchivoLocal')
                ok = True
        elif (buscar_pattern(Un_string) != 'VB') and ('ES:Verbos' in secciones):   #si no coincide con pattern
            if Un_string not in lista_verbos:
                lista_verbos.append(Un_string)
                msj = f'la palabra {Un_string} no se encuentra en pattern pero si en Wiktionary.\n'
                reporte(msj,'reporte')
                definicion = devuelve_definicion(Un_string,'verbo')
                reporte(definicion,'ArchivoLocal')
                ok = True
        elif 'ES:Verbos' not in secciones and buscar_pattern(Un_string) == 'VB':   #si coincide con wiktionary
            if Un_string not in lista_verbos:
                lista_verbos.append(Un_string)
                msj = ingresar_definicion()
                reporte(msj,'ArchivoLocal')
                ok = True



        if 'ES:Adjetivos' in secciones and buscar_pattern(Un_string) == 'JJ':
            if Un_string not in lista_adjetivos:
                lista_adjetivos.append(Un_string)
                definicion = devuelve_definicion(Un_string,'sustantivos')
                reporte(definicion,'ArchivoLocal')
                ok = True
        elif buscar_pattern(Un_string) != 'JJ' and 'ES:Adjetivos' in secciones:
            if Un_string not in lista_adjetivos:
                lista_adjetivos.append(Un_string)
                msj = f'la palabra {Un_string} no se encuentra en pattern pero si en Wiktionary.\n'
                reporte(msj,'reporte')
                definicion = devuelve_definicion(Un_string,'sustantivos')
                reporte(definicion,'ArchivoLocal')
                ok = True
        elif 'ES:Adjetivos' not in secciones and buscar_pattern(Un_string) == 'JJ':
            if Un_string not in lista_adjetivos:
                lista_adjetivos.append(Un_string)
                msj = ingresar_definicion()
                reporte(msj,'ArchivoLocal')
                ok = True

        if 'ES:Sustantivos' in secciones and buscar_pattern(Un_string) == 'NN':
            if Un_string not in lista_sustantivos:
                lista_sustantivos.append(Un_string)
                definicion = devuelve_definicion(Un_string,'adjetivo')
                reporte(definicion,'ArchivoLocal')
                ok = True
        elif buscar_pattern(Un_string) != 'NN' and 'ES:Sustantivos' in secciones:
            if Un_string not in lista_sustantivos:
                lista_sustantivos.append(Un_string)
                msj = f'la palabra {Un_string} no se encuentra en pattern pero si en Wiktionary.\n'
                reporte(msj,'reporte')
                definicion = devuelve_definicion(Un_string,'adjetivo')
                reporte(definicion,'ArchivoLocal')
                ok = True
        elif 'ES:Sustantivos' not in secciones and buscar_pattern(Un_string) == 'NN':
            if Un_string not in lista_sustantivos:
                lista_sustantivos.append(Un_string)
                msj = ingresar_definicion()
                reporte(msj,'ArchivoLocal')
                ok = True

        elif not ok:
            msj = f'la palabra {Un_string} no se encuentra en pattern y tampoco en Wiktionary.\n'
            reporte(msj, 'reporte')
    except AttributeError:
        sg.Popup('Ingrese una palabra valida')
