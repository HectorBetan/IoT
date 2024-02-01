import json
import time
import requests
import random
from datetime import datetime

last_connection_time = time.time()   # Track the last connection time
last_update_time = time.time()        # Track the last update time
update_interval = 5                 # Update once every 1 minute

# URL del servicio local
local_url = "http://localhost:5001/post_data"
previous_values = [175, 245, 305, 405, 16, 74]

def httpRequest(data):
    # Función para enviar la solicitud POST al servicio local
    headers = {"Content-Type": "application/json"}
    # Realizar la solicitud al servicio local
    try:
        response = requests.post(local_url, json=data, headers=headers)
        print(response)  # Un código de respuesta 200 indica que la solicitud fue exitosa
    except Exception as e:
        print(e)  # Imprimir el código de error
    global last_update_time
    last_update_time = time.time()  # Actualizar el tiempo de conexión

def generate_random_variation(base_value, variation_range, max_deviation):
    deviation = random.uniform(-variation_range, variation_range)
    deviation = max(-max_deviation, min(max_deviation, deviation))
    new_value = base_value + round(deviation)
    return round(new_value)

def getAirQualityData(data):
    global temp_change
    global previous_values
    variation_range = 3
    pValues = previous_values.copy()
    for i, x in enumerate(data): 
        variation_range = 2
        num = generate_random_variation(x, variation_range, variation_range)
        pValues[i] = num
    previous_values = pValues
    return tuple(pValues)

def updatesJson():
    # Función para actualizar el buffer de mensajes cada 15 segundos con datos.
    # Y luego llamar a la función httpRequest cada 2 minutos.

    global last_update_time
    message = {}
    now = datetime.utcnow()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    message['sensor_id'] = '0001'
    message['created_at'] = timestamp
    print("created_at: " + timestamp)
    print(previous_values)
    pm10, pm2, so2, no2, co, o3 = getAirQualityData(previous_values)
    message['field1'] = pm10
    message['field2'] = pm2
    message['field3'] = so2
    message['field4'] = no2
    message['field5'] = co
    message['field6'] = o3
    print(message)
    httpRequest(message)

if __name__ == "__main__":
    while True:
        # Si ha transcurrido el intervalo de actualización, actualiza el buffer de mensajes con datos
        if time.time() - last_update_time >= update_interval:
            last_update_time = time.time()
            updatesJson()
            