import json
import time
import requests
import random
from datetime import datetime
last_connection_time = time.time() # Track the last connection time
last_update_time = time.time()     # Track the last update time
posting_interval = 1200             # Post data once every 5 minutes
update_interval = 300            # Update once every 1 minute

write_api_key = "5C3H53361USNNBOM" # Replace YOUR-CHANNEL-write_api_key with your channel write API key
channel_ID = "2411527"              # Replace YOUR-channel_ID with your channel ID
url = "https://api.thingspeak.com/channels/" + channel_ID + "/bulk_update.json" # ThingSpeak server settings
message_buffer = []

previous_values = [145, 232, 297, 398, 21, 67]
temp_change = False
def httpRequest():
    # Function to send the POST request to ThingSpeak channel for bulk update.
        global message_buffer
        print(message_buffer)
        bulk_data = json.dumps({'write_api_key':write_api_key,'updates':message_buffer}) # Format the json data buffer
        request_headers = {"Content-Type":"application/json","Content-Length":str(len(bulk_data))}
    # Make the request to ThingSpeak
        try:
            response = requests.post(url, headers=request_headers, data=bulk_data)
            print(response)  # A 202 indicates that the server has accepted the request
        except Exception as e:
            print(e)  # Print the error code"""

        message_buffer = []# Liberar la memoria asignada al buffer

        global last_connection_time
        last_connection_time = time.time()  # Update the connection time
        global temp_change
        temp_change = True
def generate_random_variation(base_value, variation_range, max_deviation):
    deviation = random.uniform(-variation_range, variation_range)
    deviation = max(-max_deviation, min(max_deviation, deviation))
    new_value = base_value + round(deviation)
    return round(new_value)
def getAirQualityData(data):
    global temp_change
    global previous_values
    variation_range = 3
    pValues = previous_values.copy()  # Inicializar como una copia
    for i, x in enumerate(data): 
        variation_range = 2
        num = generate_random_variation(x, variation_range, variation_range)
        pValues[i] = num
    previous_values = pValues
    return tuple(pValues)
def updatesJson():
    # Function to update the message buffer every 15 seconds with data. 
    # And then call the httpRequest function every 2 minutes. 
    # This examples uses the relative timestamp as it uses the "delta_t" parameter.
    # If your device has a real-time clock, you can also provide the absolute timestamp 
    # using the "created_at" parameter.

        global last_update_time
        message = {}
        now = datetime.utcnow()  # Obtenemos la fecha y hora actual en UTC
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')  # Formateamos la fecha y hora en ISO 8601
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
        global message_buffer
        message_buffer.append(message)

    # If posting interval time has crossed 2 minutes update the ThingSpeak channel with your data
        if time.time() - last_connection_time >= posting_interval:
            httpRequest()
if __name__ == "__main__":  # To ensure that this is run directly and does not run when imported
        while True:
                # If update interval time has crossed 15 seconds update the message buffer with data
            if time.time() - last_update_time >= update_interval:
                last_update_time = time.time()
                updatesJson()