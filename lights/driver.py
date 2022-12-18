import logging as logging

class lights_driver:

    def __init__(self) -> None:
        """
        Creates abstraction for template
        Extends base tinyweb server with template functionality
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('template')

    def list_lights(self, i2caddress: int) -> dict:
        self.log.info("Listing lights at address: " + str(i2caddress))
        return {"result": "Some lights"}

    def demo(self, i2caddress: int) -> dict:
        """Demo of functionality for quick testing"""
        self.log.info("Performing light demo at address: " + str(i2caddress))
        return {"result" : "Demo running"}