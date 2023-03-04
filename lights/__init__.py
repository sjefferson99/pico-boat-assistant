import logging as logging
from webserver import website
from lights.webpages import lightsite
from lights.api import lightapi

class pba_lights:
    """
    Builds a lights module instance and provides a function for building
    webpages and API for control.
    Currently only works using the API for module driver control.
    """
    def __init__(self) -> None:
        # TODO expose driver functions for local code execution
        self.log = logging.getLogger('lights')
        self.log.info("Init lights module")

    def init_web(self, coresite: website, i2caddress: int) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        self.log.info("Building light API website elements")
        api = lightapi(coresite, i2caddress)
        self.log.info("Building light content website elements")
        site = lightsite(coresite)