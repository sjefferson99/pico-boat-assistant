import logging as logging
import json
import i2c_utils
import hub

class lights_driver:
    def __init__(self, hub: hub.i2c_hub) -> None:
        """
        Driver for executing various lights functions to be called
        by the API definitions or local code where no web server exists.
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('template')
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
            result = self.remote_light_on(lightid, self.get_address())
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
    def remote_light_on(self, lightid, address) -> str:
        self.log.info("Turning on remote light")
        return "Success"
    
    # Dummy testing functions
    def list_lights(self) -> dict:
        self.log.info("Listing lights at address: " + str(self.address))
        return {"result": "Some lights"}

    def demo(self) -> dict:
        """Demo of functionality for quick testing"""
        self.log.info("Performing light demo at address: " + str(self.address))
        return {"result" : "Demo running"}