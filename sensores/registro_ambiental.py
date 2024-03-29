import time
import random
from temperatura import Temperatura
from manejo_de_archivo import establecer_archivo, leer_json, escribir_archivo

dicDatos = {}
temperatura = Temperatura()


def registrar_temperatura():
	info_temperatura = temperatura.datos_sensor()
	info_temperatura.update({"fecha": time.asctime(time.localtime(time.time()))})
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