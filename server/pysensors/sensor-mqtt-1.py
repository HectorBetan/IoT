import json
import time
import random
from datetime import datetime
import paho.mqtt.publish as publish
update_interval = 300 
# Your ThingSpeak MQTT credentials
mqtt_broker = "mqtt3.thingspeak.com"
mqtt_port = 80
mqtt_username = "Mx0dCyouIho2AxwJAwQ9Czs"
mqtt_password = "D9TgoG1TpqezC0bwUlFmXMNM"
t_transport = "websockets"
def generate_random_variation(base_value, variation_range, max_deviation):
    deviation = random.uniform(-variation_range, variation_range)
    deviation = max(-max_deviation, min(max_deviation, deviation))
    new_value = base_value + round(deviation)
    return round(new_value)

def get_air_quality_data(data, temp_change):
    variation_range = 3
    p_values = data.copy()
    for i, x in enumerate(data):
        variation_range = 2
        num = generate_random_variation(x, variation_range, variation_range)
        p_values[i] = num
    return tuple(p_values), temp_change
def format_payload(payload):
    query_string = "&".join([f"{key}={value}" for key, value in payload.items() if key != "created_at"])
    return query_string
def updates_mqtt(topic, message, temp_change):
    now = datetime.utcnow()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    data, temp_change = get_air_quality_data(message, temp_change)

    payload = {'created_at': timestamp}
    print("created_at:", timestamp)
    p = {}
    for i in range(len(data)):
        payload[f'field{i+1}'] = data[i]

    payload_json = json.dumps(payload)
    pay = format_payload(json.loads(payload_json))  # Cargar cadena JSON como diccionario antes de formatear
    print(pay)

    publish.single(topic, pay, hostname=mqtt_broker, transport= t_transport, port=mqtt_port, client_id=mqtt_username, auth={'username': mqtt_username, 'password': mqtt_password, 'client_id': mqtt_password})
    return temp_change

if __name__ == "__main__":
    sensor_topic = "channels/2411529/publish"
    sensor_values = [123, 218, 315, 298, 20, 80]

    temp_change = False

    try:
        while True:
            temp_change = updates_mqtt(sensor_topic, sensor_values, temp_change)
            time.sleep(update_interval)
    except KeyboardInterrupt:
        print("Exiting...")
