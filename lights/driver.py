import logging as logging

class lights_driver:

    def __init__(self) -> None:
        """
        Driver for executing various lights functions to be called
        by the API definitions or local code where no web server exists.
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('template')

        # TODO Determine if lights are local or I2C networked and get address
        # TODO Add local lights driver functions
        # TODO Add functions for passing lights commands over the I2C network
        # TODO Add functions for parsing lights commands from the I2C network

    def list_lights(self, i2caddress: int) -> dict:
        self.log.info("Listing lights at address: " + str(i2caddress))
        return {"result": "Some lights"}

    def demo(self, i2caddress: int) -> dict:
        """Demo of functionality for quick testing"""
        self.log.info("Performing light demo at address: " + str(i2caddress))
        return {"result" : "Demo running"}