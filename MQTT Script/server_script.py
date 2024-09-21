import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime

# MQTT Settings
MQTT_BROKER = "your_mqtt_broker_ip"
MQTT_PORT = 1883
MQTT_TOPIC = "attendance/wifi"

# Django API endpoint for marking attendance
DJANGO_API_URL = "http://127.0.0.1:8000/mark-attendance/"

# Function to mark attendance via Django API
def mark_attendance(emp_id, token, status):
    data = {
        "emp_id": emp_id,
        "token": token,
        "status": status,
        "loginTime": datetime.now().isoformat(),
        "logoutTime": datetime.now().isoformat() if status == 'logout' else None
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(DJANGO_API_URL, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print(f"Attendance updated for {emp_id}")
    else:
        print(f"Failed to update attendance for {emp_id}: {response.content}")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing to the attendance topic
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        # Decode the incoming message
        message = msg.payload.decode('utf-8')
        data = json.loads(message)

        emp_id = data.get('emp_id')
        token = data.get('token')
        status = data.get('status')  # login or logout

        # Mark attendance in the Django backend
        mark_attendance(emp_id, token, status)

    except Exception as e:
        print(f"Error processing message: {e}")

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Blocking loop to process network traffic, dispatch callbacks and handle reconnecting.
client.loop_forever()
