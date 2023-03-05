import logging as logging
import config
import json

class lights_driver:

    def __init__(self) -> None:
        """
        Driver for executing various lights functions to be called
        by the API definitions or local code where no web server exists.
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('template')
        self.log.info("Loading lights driver")

        # Determine if lights are local or I2C networked and get address
        self.log.info("Loading enabled modules from file")
        with open(config.en_mod_file, "r") as en_mod_file:
            self.enabled_modules = json.load(en_mod_file)

        self.address = self.enabled_modules["lights"]["address"]
        if self.address == "local":
            self.log.info("Lights module is local")
        else:
            self.log.info("Lights module is at I2C address: " + str(self.address))

        # TODO Add local lights driver functions
        # TODO Add functions for passing lights commands over the I2C network
        # TODO Add functions for parsing lights commands from the I2C network

    def list_lights(self) -> dict:
        self.log.info("Listing lights at address: " + str(self.address))
        return {"result": "Some lights"}

    def demo(self) -> dict:
        """Demo of functionality for quick testing"""
        self.log.info("Performing light demo at address: " + str(self.address))
        return {"result" : "Demo running"}