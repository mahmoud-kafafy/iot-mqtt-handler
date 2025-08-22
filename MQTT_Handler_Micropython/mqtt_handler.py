"""
To view the data:

1. Go to http://www.hivemq.com/demos/websocket-client/
2. Click "Connect"
3. Under Subscriptions, click "Add New Topic Subscription"
4. In the Topic field, type "wokwi-weather" then click "Subscribe"

"""

from umqtt.simple import MQTTClient
import time

class MQTTHandler:
    def __init__(self, client_id, broker, user="", password="", keepalive=60):
        self.client = MQTTClient(client_id, broker, user=user, password=password, keepalive=keepalive)
    
    def connect(self):
        self.client.connect()
        print("✅ MQTT Connected")

    def publish(self, topic, message):
        self.client.publish(topic, str(message).encode())

    def subscribe(self, topic, callback):
        self.client.set_callback(callback)
        self.client.subscribe(topic)
        print("✅ Subscribed to", topic)

    def check_messages(self):
        #Check for new messages (non-blocking)
        self.client.check_msg()
