import time
import random
from temperatura import Temperatura
from date import date, datetime
from manejo_de_archivo import establecer_archivo, leer_json, escribir_archivo

dicDatos = {}
temperatura = Temperatura()

def fechaActual():
    ahora = datetime.now()
    mes = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'junio', 7: 'Julio', 8: 'Agosto',
           9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

    dia_semana = {0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}

    fecha = f"{dia_semana[date.today().weekday()]} {str(date.today().day)} de {mes[date.today().month]} del {str( date.today().year)}{ahora.hour}:{ahora.minute}:{ahora.second} hs"
    return fecha

def registrar_temperatura():
	info_temperatura = temperatura.datos_sensor()
	info_temperatura['fecha'] = fechaActual()
	try:
		l = leer_json('dato-oficinas.json')
		dicDatos = l
	except FileNotFoundError:
		dicDatos = {}
	clave = 'oficina1'
	if clave in dicDatos.keys():
		while True:
			num = random.randint(2, 100)
			clave = clave[:-1]
			clave += str(num)
			if clave not in dicDatos.keys():
				dicDatos[clave] = info_temperatura
				ar = establecer_archivo('dato-oficinas.json')
				escribir_archivo(ar, dicDatos)
				ar.close()
				break
			else:
				continue
	else:
		dicDatos['oficina1'] = info_temperatura
		ar = establecer_archivo('dato-oficinas.json')
		escribir_archivo(ar, dicDatos)
		ar.close()
		
registrar_temperatura()