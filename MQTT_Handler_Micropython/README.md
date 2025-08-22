
# 📡 MQTTHandler & WiFiHandler for ESP32 (MicroPython)

Simple classes to connect your ESP32 to **WiFi** and an **MQTT broker**, publish sensor data, and receive messages.




---

## 🛠 Steps to Use

### 1️⃣ Import the handler files

Download `wifi_handler.py` and `mqtt_handler.py` from the repo and put them in the **same directory as your main**.
This allows you to use the WiFi and MQTT helper classes in your project.

```python
from wifi_handler import WiFiHandler
from mqtt_handler import MQTTHandler
```

---

### 2️⃣ Connect to WiFi

This step establishes your ESP32’s internet connection. Without it, MQTT won’t work.

```python
wifi = WiFiHandler("YourWiFiSSID", "YourWiFiPassword")
wifi.connect()
```

Output will show your ESP32 IP address:

```
✅ WiFi Connected: ('192.168.1.50', '255.255.255.0', '192.168.1.1', '8.8.8.8')
```

---

### 3️⃣ Define your MQTT parameters

Here you set the **client ID**, **broker address**, **username/password** (if required), and the topics you want to publish or subscribe to.

```python
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "mqtt-dashboard.com"
MQTT_USER      = ""       # set if required
MQTT_PASSWORD  = ""       # set if required
MQTT_TOPIC     = b"wokwi-weatherr"      # where you will publish
MQTT_TOPIC_SUB = b"wokwi-weatherr"      # where you will listen
```

---

### 4️⃣ Create and connect the MQTT client

This step initializes your MQTT client and connects it to the broker.

```python
mqtt_client = MQTTHandler(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_USER, MQTT_PASSWORD)
mqtt_client.connect()
```

---

### 5️⃣ Publish a message

Sends data to your chosen topic. You can publish **sensor readings** or any data you want and i change it to bytes in the class.

```python
mqtt_client.publish(MQTT_TOPIC, "Hello from ESP32")
```

---

### 6️⃣ Subscribe to a topic

This lets your ESP32 **listen** for incoming messages on a topic.
When a new message arrives, the callback function is triggered.

```python
def message_callback(topic, msg):
    print(f"📩 Received on {topic.decode()}: {msg.decode()}")

mqtt_client.subscribe(MQTT_TOPIC_SUB, message_callback)
```

---

### 7️⃣ Check for incoming messages (inside your loop)

Keeps checking for new messages from the broker.
You should place this in your main loop so messages are not missed.

```python
while True:
    mqtt_client.check_messages()
```

---

## ✅ Features

* Easy WiFi connection
* MQTT connect, publish, and subscribe
* Custom callback for received messages
* Non-blocking message checking

---

👉 See `main.py` for a **full working example** with WiFi + MQTT.

---

## 📊 Workflow Diagram

The following diagram shows how the WiFi and MQTT handlers work together:

![Workflow Diagram](Diagram/Diagram.png)

---

⚠️ **Important Notes:**
- This example uses a **simple MQTT connection** (non-TLS, port **1883**).  
  It works well with public brokers like `mqtt-dashboard.com` or `test.mosquitto.org`, but it does **not use encryption**.  
  For cloud brokers (like HiveMQ Cloud or AWS IoT), you must use **TLS/SSL (port 8883)**  — which requires extra setup.
- For better reliability (automatic reconnection if the broker disconnects) and also to use HIVEMQ Cloud service, you should use **`umqtt.robust`** instead of plain **`umqtt.simple`**.