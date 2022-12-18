from machine import Pin, I2C
import logging as logging
from time import sleep_ms
import config as config
from hub import i2c_hub

class pico_boat_assistant:
    """
    Core class for the pico boat assistant.
    Loads the common elements:
    I2C communication
    Allows modular plugging of optional elements.
    """
    def __init__(self) -> None:
        # Basic IO
        self.log = logging.getLogger('core')
        self.log.info("Init board LED")
        led = Pin("LED", Pin.OUT)
        self.flash_led(led)
        
        # I2C setup
        self.log.info("Init I2C")
        self.local_modules = config.local_modules
        if "hub" in self.local_modules:
            self.log.info("Node is a Hub module")
            self.local_modules.remove("hub")
            self.ihub = i2c_hub(self.local_modules)
        
        else:
            self.log.info("Responder I2C node")
            # TODO build responder init logic

    def flash_led(self, led: Pin, duration: int=100) -> None:
        led.on()
        sleep_ms(duration)
        led.off()