from aemet import Aemet
import json
from datetime import datetime, timedelta

def generar_datos_aemet():

    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ5b25pODA2MEBnbWFpbC5jb20iLCJqdGkiOiI0ZGFiM2I5OC03OTNjLTQyZDYtYTRkYi0zM2E2Y2M5ZDk2MTUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY4OTcxODk0MiwidXNlcklkIjoiNGRhYjNiOTgtNzkzYy00MmQ2LWE0ZGItMzNhNmNjOWQ5NjE1Iiwicm9sZSI6IiJ9.7YKE8z7ceq4f36UuvsSP0Xr-VITZVDXGkQE1EitPofg" #Aqui debes introducir tu clave de la api de aemet personal
    aemet = Aemet(api_key)

    estacion = {
          'nombre': 'LEÓN Aeropuerto', #si se quiere usar otra ciudad buscar el indicativo de tu ciudad
         'indicativo': '2661'
    }

    # Fecha de inicio y fin en formato específico para aemet
    fecha_inicio_str = '2018-07-20T00:00:00UTC'
    fecha_fin_str = '2023-07-19T23:59:59UTC'

    # Convertir las fechas a objetos datetime
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M:%SUTC')
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M:%SUTC')
    n=0
    # Bucle para restar 5 años en cada iteración y asi poder recorrer todos los json
    while n<12:
        # Obtener los datos climatológicos diarios para la estación y el rango de fechas
        vcm = aemet.get_valores_climatologicos_diarios(fecha_inicio.strftime('%Y-%m-%dT%H:%M:%SUTC'), fecha_fin.strftime('%Y-%m-%dT%H:%M:%SUTC'),estacion['indicativo'])

        resultado = {
            'estacion': estacion,
            'valores_climatologicos': vcm
        }

        # Crear un nombre de archivo único para cada iteración
        nombre_archivo = f'Datos_AEMET-Leon_{fecha_inicio.year}-{fecha_fin.year}.json'

        # Guardar los datos en un archivo JSON con el nombre único
        with open(nombre_archivo, 'w') as archivo_json:
            json.dump(resultado, archivo_json, indent=2)


        fecha_inicio -= timedelta(days=5*365)
        fecha_fin -= timedelta(days=5*365)
        n=n+1

generar_datos_aemet()
