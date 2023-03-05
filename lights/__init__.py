import logging as logging
from lights.webpages import lightsite
from lights.api import lightapi
import hub

class pba_lights:
    """
    Builds a lights module instance and provides a function for building
    webpages and API for control.
    """
    def __init__(self, hub: hub.i2c_hub) -> None:
        """
        Creates a lights module class, for use by a hub (need to work out local module later).
        Pass the instantiating hub as "self".
        """
        self.log = logging.getLogger('lights')
        self.log.info("Init lights module")
        self.hub = hub

        if hub.is_wireless_enabled():
            self.init_web()

    def init_web(self) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        self.log.info("Building light API website elements")
        lightapi(self.hub)
        self.log.info("Building light content website elements")
        lightsite(self.hub)