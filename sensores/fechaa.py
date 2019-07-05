from datetime import date,datetime

def fechaActual():
    ahora = datetime.now()
    mes = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'junio', 7: 'Julio', 8: 'Agosto',
           9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

    dia_semana = {0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}

    fecha = f"{dia_semana[date.today().weekday()]} {str(date.today().day)} de {mes[date.today().month]} del {str( date.today().year)}"
    hora = f"{ahora.hour}:{ahora.minute}:{ahora.second} hs"
    return fecha,hora
