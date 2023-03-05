import logging as logging
import hub
from pba_i2c import pba_i2c_hub
from machine import I2C

class lights_driver:
    def __init__(self, hub: hub.pba_hub) -> None:
        """
        Driver for executing various lights functions to be called
        by the API definitions or local code where no web server exists.
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('lights_driver')
        self.log.info("Loading lights driver")

        self.hub = hub

        self.enabled_modules = self.hub.get_enabled_modules()

        self.address = self.enabled_modules["lights"]["address"]
        if self.address == "local":
            self.log.info("Lights module is local")
            self.local = True
        else:
            self.log.info("Lights module is at I2C address: " + str(self.address))
            self.local = False

        self.i2c_hub_interface = hub.get_i2c_interface()

    def is_local(self) -> bool:
        return self.local            
    
    def get_address(self) -> int:
        return self.address
    
    ##############################
    # Abstracted light functions #
    ##############################
    def light_on(self, lightid) -> str:
        self.log.info("Turning light on: " + lightid)
        if self.is_local():
            result = self.local_light_on(lightid)
        else:
            result = self.remote_light_on(lightid, self.get_address(), self.hub)
        return "Attempted to turn light on: " + lightid + " : " + result
    
    # TODO Add local lights hardware driver functions
    # Add functions for parsing lights commands from the I2C network
    ##########################
    # Local light functions  #
    ##########################
    def local_light_on(self, lightid) -> str:
        self.log.info("Turning on local light")
        return "Success"
    
    # TODO Add functions for passing lights commands over the I2C network
    ##########################
    # Remote light functions #
    ##########################
    def remote_light_on(self, lightid, address, hub: hub.pba_hub) -> str:
        self.log.info("Turning on remote light")
        pba_i2c_lights = pba_i2c_hub_lights(self.i2c_hub_interface)
        print("Testing subclass, should get 2")
        print(pba_i2c_lights.test_function())
        return "Success"
    
    # Dummy testing functions
    def list_lights(self) -> dict:
        self.log.info("Listing lights at address: " + str(self.address))
        return {"result": "Some lights"}

    def demo(self) -> dict:
        """Demo of functionality for quick testing"""
        self.log.info("Performing light demo at address: " + str(self.address))
        return {"result" : "Demo running"}

class pba_i2c_hub_lights(pba_i2c_hub):
    def __init__(self, i2c: I2C) -> None:
        super().__init__(i2c)
        """
        Class for lights module specific extensions to the PBA I2C interface
        """
        self.log = logging.getLogger('pba_i2c_hub_lights')
        self.log.info("Instantiating lights specific i2c interface")

    def test_function(self):
        return self.get_i2c_module_id(65)
