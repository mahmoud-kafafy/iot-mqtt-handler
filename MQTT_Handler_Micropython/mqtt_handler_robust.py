#https://console.hivemq.cloud/clusters/f446739580a645d9b26dc12166f78ed8/web-client
from umqtt.robust import MQTTClient
import time

class HiveMQHandler:
    def __init__(self, client_id, broker, user, password, port):
        self.client = MQTTClient(
            client_id=client_id,
            server=broker,
            port=port,
            user=user,
            password=password,
            ssl=True,
            ssl_params={"server_hostname": broker}  # required for HiveMQ Cloud SNI
        )
        self.broker = broker
        self.port = port

    def connect(self):
        try:
            self.client.connect()
            print("✅ Connected securely to HiveMQ Cloud")
        except Exception as e:
            print("❌ Connection failed:", e)
            raise

    def publish(self, topic, message):
        try:
            self.client.publish(topic, str(message).encode())
            print(f"📤 Published: {message} → {topic.decode() if isinstance(topic, bytes) else topic}")
        except Exception as e:
            print("⚠ Publish error:", e)

    def subscribe(self, topic, callback):
        try:
            self.client.set_callback(callback)
            self.client.subscribe(topic)
            print("✅ Subscribed to", topic.decode() if isinstance(topic, bytes) else topic)
        except Exception as e:
            print("⚠ Subscribe error:", e)

    def check_messages(self):
        try:
            self.client.check_msg()  # non-blocking
        except Exception as e:
            print("⚠ Check message error:", e)

    def reconnect(self):
        try:
            self.client.reconnect()
            print("🔄 Reconnected to HiveMQ Cloud")
        except Exception as e:
            print("❌ Reconnect failed:", e)
