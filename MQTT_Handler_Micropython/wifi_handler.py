import network, time

class WiFiHandler:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.sta_if = network.WLAN(network.STA_IF)

    def connect(self):
        if not self.sta_if.isconnected():
            print(f"🔌 Connecting to WiFi {self.ssid}...")
            self.sta_if.active(True)
            self.sta_if.connect(self.ssid, self.password)
            while not self.sta_if.isconnected():
                print(".", end="")
                time.sleep(0.2)
        print("✅ WiFi Connected:", self.sta_if.ifconfig())

    def is_connected(self):
        return self.sta_if.isconnected()
