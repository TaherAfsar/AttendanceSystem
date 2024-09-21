import time
import socket
import paho.mqtt.client as mqtt
import json

# MQTT Settings
MQTT_BROKER = "your_mqtt_broker_ip"  # Replace with the IP address of the Mosquitto broker
MQTT_PORT = 1883
MQTT_TOPIC = "attendance/wifi"


EMPLOYEE_DETAILS = {
    "emp_id": "E001",  # Each laptop should have its unique emp_id and token
    "token": "123456"
}

def check_wifi_connection():
    try:
        # checking connection to wifi
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def send_mqtt_message(status):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    message = {
        "emp_id": EMPLOYEE_DETAILS["emp_id"],
        "token": EMPLOYEE_DETAILS["token"],
        "status": status  # login or logout
    }

    client.publish(MQTT_TOPIC, json.dumps(message))
    client.disconnect()

def main():
    was_connected = False
    
    while True:
        is_connected = check_wifi_connection()

        if is_connected and not was_connected:
            print("Connected to Wi-Fi. Sending login status.")
            send_mqtt_message("login")
            was_connected = True

        elif not is_connected and was_connected:
            print("Disconnected from Wi-Fi. Sending logout status.")
            send_mqtt_message("logout")
            was_connected = False

        time.sleep(5)

if __name__ == "__main__":
    main()
