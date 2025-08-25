from wifi_handler import WiFiHandler
from mqtt_robust import HiveMQHandler
from machine import Pin
import time


MQTT_CLIENT_ID = "esp32-demo"
MQTT_BROKER    = "f446739580a645d9b26dc12166f78ed8.s1.eu.hivemq.cloud"
MQTT_USER      = "Mahmoud"
MQTT_PASSWORD  = "123456789mM"
MQTT_TOPIC     = b"esp322"
PORT = 8883

# setup LED pin (GPIO17) as output
led = Pin(13, Pin.OUT)


# --- Main Program ---
# MQTT message callback
def message_callback(topic, msg):
    print(f"📩 Received on {topic.decode()}: {msg.decode()}")
    if msg.decode().lower() == "on":
        led.value(not led.value())
        print(f"💡 LED {led.value()}")

# WiFi
wifi = WiFiHandler("Wokwi-GUEST", "")
wifi.connect()

# Connect
mqtt_client = HiveMQHandler(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, PORT)
mqtt_client.connect()
mqtt_client.subscribe(MQTT_TOPIC, message_callback)

    
while True:
    try:

        # Publish temperature
        mqtt_client.publish(MQTT_TOPIC, "on")

        # Check for incoming messages
        mqtt_client.check_messages()

    except OSError as e:
        print("⚠ Sensor Error:", e)
        mqtt_client.connect()
        mqtt_client.subscribe(MQTT_TOPIC_SUB, message_callback)

    time.sleep(2)