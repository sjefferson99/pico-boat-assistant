import network
from time import sleep_ms
import config
from machine import Pin
import logging as logging

class wireless:
    """
    Sets up and manages wifi connection
    """    
    def __init__(self) -> None:
        self.log = logging.getLogger('wireless')
        self.log.info("Init wireless")
        self.test_result = False
        self.heartbeat_interval = config.heartbeat_interval
        self.heartbeat_url = config.heartbeat_url
        self.network_relay = config.network_relay
        self.reset_duration = config.reset_duration

        self.led = Pin("LED", Pin.OUT)

    def start_wifi(self) -> bool:
        self.log.info("Attempting wifi connection")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            self.log.info("waiting for connection...")
            self.led.toggle()
            sleep_ms(500)

        if self.wlan.status() != 3:
            error_wait = 100
            while error_wait > 0:
                self.led.toggle()
                sleep_ms(100)
                error_wait -= 1
            return False
                
        else:
            self.log.info("connected")
            status = self.wlan.ifconfig()
            self.log.info("ip = " + str(status[0]))
            return True
    
    def wireless_status(self) -> int:
        return self.wlan.status()