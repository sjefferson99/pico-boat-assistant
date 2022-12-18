import logging as logging
from webserver import website
from lights.webpages import lightsite
from lights.api import lightapi

class pba_lights:
    """
    
    """
    def __init__(self) -> None:
        # 
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