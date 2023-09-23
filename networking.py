import network
from time import sleep
import config
from machine import Pin
import logging as logging
import rp2
import ubinascii

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

        rp2.country("GB")

        self.led = Pin("LED", Pin.OUT)

    def start_wifi(self) -> bool:
        self.log.info("Attempting wifi connection")
    
        # Set WLAN as client
        self.wlan = network.WLAN(network.STA_IF)
        
        # Print MAC
        mac = ubinascii.hexlify(self.wlan.config('mac'),':').decode()
        self.log.info("MAC: " + mac)
        
        self.wlan.active(True)
        self.wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

        # 5 Second connection attempt with LED status
        max_wait = 10
        while max_wait > 0:
            if self.wireless_status() < 0 or self.wireless_status() >= 3:
                break
            max_wait -= 1
            self.log.info("waiting for connection...")
            self.led.toggle()
            sleep(0.5)

        # 10 second back off timer with LED status
        if self.wireless_status() != 3:
            self.log.info("Retrying connection in 10 seconds")
            error_wait = 100
            while error_wait > 0:
                self.led.toggle()
                sleep(0.100)
                error_wait -= 1
            return False
                
        else:
            self.log.info("connected")
            ifconfig = self.wlan.ifconfig()
            self.log.info("ip = " + str(ifconfig[0]))
            return True
    
    def wireless_status(self) -> int:
        # Reference: https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
        CYW43_LINK_DOWN = 0
        CYW43_LINK_JOIN = 1
        CYW43_LINK_NOIP = 2
        CYW43_LINK_UP = 3
        CYW43_LINK_FAIL = -1
        CYW43_LINK_NONET = -2
        CYW43_LINK_BADAUTH = -3

        self.status_names = {
        CYW43_LINK_DOWN: "Link is down",
        CYW43_LINK_JOIN: "Connected to wifi",
        CYW43_LINK_NOIP: "Connected to wifi, but no IP address",
        CYW43_LINK_UP: "Connect to wifi with an IP address",
        CYW43_LINK_FAIL: "Connection failed",
        CYW43_LINK_NONET: "No matching SSID found (could be out of range, or down)",
        CYW43_LINK_BADAUTH: "Authenticatation failure",
        }

        status = self.wlan.status()
        logging.info("WLAN status: " + str(status) + " - " + self.status_names[status])
        return status