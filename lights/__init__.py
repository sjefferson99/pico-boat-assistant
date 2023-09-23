import logging as logging
from lights.webpages import lightsite
from lights.api import lightapi
import hub
from lights.driver import lights_driver
from time import time

class pba_lights:
    """
    Builds a lights module instance and provides a function for building
    webpages and API for control.
    """
    def __init__(self, hub) -> None: # TODO add pba_hub type after this module isnot called in pba_hub.init()
        """
        Creates a lights module class, for use by a hub (need to work out local module later).
        Pass the instantiating hub as "self".
        """
        self.log = logging.getLogger('lights')
        self.log.info("Init lights module")
        self.hub = hub

        if hub.is_wireless_enabled():
            self.init_web()
        
        self.driver = lights_driver(self.hub)
        self.groups = {}
        self.set_groups()
        self.log.info(self.groups)

    def init_web(self) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        self.log.info("Building light API website elements")
        lightapi(self.hub)
        self.log.info("Building light content website elements")
        lightsite(self.hub)

    def list_groups(self) -> dict:
        return self.groups
    
    def set_groups(self) -> None:
        self.groups["config"] = self.driver.get_groups()
        self.groups["timestamp"] = time()
        return