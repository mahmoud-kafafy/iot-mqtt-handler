from machine import Pin, I2C
import time, dht, ssd1306, network
from mqtt_handler import MQTTHandler
from wifi_handler import WiFiHandler

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "mqtt-dashboard.com"
MQTT_USER      = ""       # set if required
MQTT_PASSWORD  = ""       # set if required
MQTT_TOPIC     = b"wokwi-weatherr"
MQTT_TOPIC_SUB = b"wokwi-weatherr"

# DHT22 Sensor on GPIO15
sensor = dht.DHT22(Pin(15))

# OLED Display (I2C: SDA=21, SCL=22)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# MQTT message callback
def message_callback(topic, msg):
    print(f"📩 Received on {topic.decode()}: {msg.decode()}")
    oled.fill(0)
    oled.text("MQTT Msg:", 0, 0)
    oled.text(msg.decode(), 0, 20)
    oled.show()

# --- Main Program ---

# WiFi
wifi = WiFiHandler("Wokwi-GUEST", "")
wifi.connect()

mqtt_client = MQTTHandler(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_USER, MQTT_PASSWORD)
mqtt_client.connect()
mqtt_client.subscribe(MQTT_TOPIC_SUB, message_callback)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print("🌡 Temperature:", temp, "°C")
        print("💧 Humidity:", hum, "%")

        # Publish temperature
        mqtt_client.publish(MQTT_TOPIC, temp)

        # Check for incoming messages
        mqtt_client.check_messages()

    except OSError as e:
        print("⚠ Sensor Error:", e)
        oled.fill(0)
        oled.text("Sensor Error", 20, 30)
        oled.show()
        mqtt_client.connect()
        mqtt_client.subscribe(MQTT_TOPIC_SUB, message_callback)

    time.sleep(2)
