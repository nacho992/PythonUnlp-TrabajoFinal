import json


def establecer_archivo(nombre):
    try:
        archivo = open(nombre, 'x', encoding='utf-8')
        return archivo
    except FileExistsError:
        existe = open(nombre, 'w', encoding='utf-8')
        return existe

		
def leer_json(archivo):
    c = open(archivo, 'r')
    aux = json.load(c)
    return aux
	
	
def escribir_archivo(archivo, dato):
    json.dump(dato, archivo, indent=5, ensure_ascii=False)