'''
Mockups of hardware specific modules
'''

import sys
import os
import asyncio
import errno
import socket
import time
import binascii

# Deifne classes and functions to be mocked in testing
# machine module
class Pin:
    OUT = 0
    
    def __init__(self, id: str, mode: int = 0) -> None:
        pass
    
    def on(self):
        return 0
    
    def off(self):
        return 0
    
    def toggle(self):
        pass
    
class I2C:
    def __init__(self, id: int, sda, scl, freq: int):
        pass

    def scan(self):
        pass

# network module
class WLAN():
    def __init__(self, interface) -> None:
        pass

    def config(self, item: str) -> bytes:
        return bytes(0)
    
    def active(self, mode: bool):
        pass

    def connect(self, ssid: str, password: str):
        pass

    def status(self):
        return 3
    
    def ifconfig(self):
        config = ["192.168.1.100"]
        return config

# rp2 module
def rp2_country(id: str):
    return 0

# build mocked modules for testing using functions and classes above
machine = type(sys)('machine')
machine.Pin = Pin
machine.I2C = I2C

network = type(sys)('network')
network.WLAN = WLAN
network.STA_IF = 0

rp2 = type(sys)('rp2')
rp2.country = rp2_country

# Insert mocked modules into testing environment
sys.modules['machine'] = machine
sys.modules['uasyncio'] = asyncio
sys.modules['uos'] = os
sys.modules['uerrno'] = errno
sys.modules['usocket'] = socket
sys.modules['utime'] = time
sys.modules['network'] = network
sys.modules['rp2'] = rp2
sys.modules['ubinascii'] = binascii