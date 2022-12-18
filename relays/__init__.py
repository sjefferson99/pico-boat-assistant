import logging as logging
from webserver import website
from relays.webpages import relaysite
from relays.api import relayapi

class pba_relays:
    """
    
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