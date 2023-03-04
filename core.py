from machine import Pin, I2C
import logging as logging
from time import sleep_ms
import config as config
from hub import i2c_hub

class pico_boat_assistant:
    """
    Core class for the pico boat assistant.
    Loads the core elements of a PBA module:
    - Board LED
    - I2C communication

    Currently assumes unit will be set hub mode and then loads optional modules
    via the i2c hub class
    """
    def __init__(self) -> None:
        # Basic IO
        self.log = logging.getLogger('core')
        self.log.info("Init board LED")
        led = Pin("LED", Pin.OUT)
        self.flash_led(led)
        
        # I2C setup
        self.log.info("Init I2C")
        # Modules defined to be locally executed by this hub
        self.local_modules = config.local_modules
        if "hub" in self.local_modules:
            self.log.info("Node is a Hub module")
            self.local_modules.remove("hub")
            #Build hub object
            self.ihub = i2c_hub(self.local_modules)
        
        else:
            self.log.info("Responder I2C node")
            # TODO build responder init logic

    def flash_led(self, led: Pin, duration: int=100) -> None:
        led.on()
        sleep_ms(duration)
        led.off()