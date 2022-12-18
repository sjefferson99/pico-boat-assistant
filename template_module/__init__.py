import logging as logging
from webserver import website
from webpages import templatesite
from api import templateapi

class pba_template:
    """
    
    """
    def __init__(self) -> None:
        # 
        self.log = logging.getLogger('template')
        self.log.info("Init template module")

    def init_web(self, coresite: website) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        self.log.info("Building template API website elements")
        api = templateapi(coresite)
        self.log.info("Building template content website elements")
        site = templatesite(coresite)