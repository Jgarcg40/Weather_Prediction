import http.client
import json

# Configurar la conexión
conn = http.client.HTTPSConnection("opendata.aemet.es")

# Escribir aquí tu clave API de AEMET personal
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ5b25pODA2MEBnbWFpbC5jb20iLCJqdGkiOiI0ZGFiM2I5OC03OTNjLTQyZDYtYTRkYi0zM2E2Y2M5ZDk2MTUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY4OTcxODk0MiwidXNlcklkIjoiNGRhYjNiOTgtNzkzYy00MmQ2LWE0ZGItMzNhNmNjOWQ5NjE1Iiwicm9sZSI6IiJ9.7YKE8z7ceq4f36UuvsSP0Xr-VITZVDXGkQE1EitPofg"
headers = {
    'accept': "application/json",
    'api_key': api_key
}

# Realizar la solicitud GET
conn.request("GET", "/opendata/api/observacion/convencional/datos/estacion/2661", headers=headers)

# Obtener la respuesta
res = conn.getresponse()
data = res.read()

# Decodificar la respuesta JSON
json_data = json.loads(data)

# Obtener el enlace para los datos
datos_url = json_data['datos']

# Realizar una nueva solicitud GET para obtener los datos de la URL obtenida
conn.request("GET", datos_url)
res = conn.getresponse()
data = res.read()

try:
    # para evitar error de utf-8
    datos_aemet_list = json.loads(data.decode('utf-8'))
except UnicodeDecodeError:
    #  para evitar error de ISO-8859-1
    datos_aemet_list = json.loads(data.decode('ISO-8859-1'))


if isinstance(datos_aemet_list, list) and len(datos_aemet_list) > 0:
    # Almacenar los datos climatológicos (lista de diccionarios)
    datos_climatologicos = datos_aemet_list
else:
    print("Error: La respuesta no es una lista válida o está vacía.")

## Definir funciones para pasarlas al archivo principal (datos del día actual)

#funcion para traducir de 360 grados a 100 el viento ya que aemet proporciona estos datos de manera diferente
def translate_dir_to_0_to_100(dir1):
    dir_0_to_1 = dir1 / 360
    dir_0_to_100 = dir_0_to_1 * 100
    return dir_0_to_100
def tmed():
    return sum(float(dato['ta']) for dato in datos_climatologicos) / len(datos_climatologicos)

def prec():
    return float(datos_climatologicos[-1]['prec'])

def tmin():
    return min(float(dato['tamin']) for dato in datos_climatologicos)

def tmax():
    return max(float(dato['tamax']) for dato in datos_climatologicos)

def dir1():
    return float(datos_climatologicos[-1]['dv'])

def dir():
    return round(translate_dir_to_0_to_100(dir1()))

def velmedia():
    return sum(float(dato['vv']) for dato in datos_climatologicos) / len(datos_climatologicos)

def racha():
    return max(float(dato['vmax']) for dato in datos_climatologicos)

def sol():
    return float(datos_climatologicos[-1]['inso'])

def presMax():
    return max(float(dato['pres']) for dato in datos_climatologicos)

def presMin():
    return min(float(dato['pres']) for dato in datos_climatologicos)

'''
# Imprimir los resultados test
if 'datos_climatologicos' in globals():
    print("Datos obtenidos de AEMET:")
    print(f"Temperatura media (promedio de todas las horas): {tmed():.1f}")
    print(f"Precipitación (último valor): {prec():.1f}")
    print(f"Temperatura mínima: {tmin():.1f}")
    print(f"Temperatura máxima: {tmax():.1f}")
    print(f"Dirección del viento (último valor): {dir():.1f}")
    print(f"Velocidad media del viento (último valor): {velmedia():.1f}")
    print(f"Racha máxima de viento: {racha():.1f}")
    print(f"Horas de sol (último valor): {sol():.1f}")
    print(f"Presión máxima: {presMax():.1f}")
    print(f"Presión mínima: {presMin():.1f}")
else:
    print("Error: No se pudieron obtener los datos climáticos.")
'''

