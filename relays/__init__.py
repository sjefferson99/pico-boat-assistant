import logging as logging
from webserver import website
from relays.webpages import relaysite
from relays.api import relayapi

class pba_relays:
    """
    Builds a relays module instance and provides a function for building
    webpages and API for control.
    Currently only works using the API for module driver control.
    """
    def __init__(self) -> None:
        # 
        self.log = logging.getLogger('relays')
        self.log.info("Init relays module")
        
    def init_web(self, coresite: website) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        self.log.info("Building relay API website elements")
        api = relayapi(coresite)
        self.log.info("Building relay content website elements")
        site = relaysite(coresite)