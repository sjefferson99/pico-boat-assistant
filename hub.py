import logging as logging
from machine import I2C, Pin
import i2c_utils
import config as config
import sys
sys.path.append("/lights")
from lights import pba_lights
sys.path.append("/relays")
from relays import pba_relays
from networking import wireless
from webserver import website

class i2c_hub:
    """
    Pico Boatman I2C hub device, polls responder modules to control or return
    information.
    """
    def __init__(self, local_modules: list) -> None:
        self.log = logging.getLogger('hub')
        self.log.info("Init I2C Hub")
        self.version = str("0.1.0")
        self.local_modules = local_modules
        self.wireless = self.detect_wireless()
        self.registered_modules = config.registered_modules
        
        # Init I2C
        sda1 = Pin(config.sda1)
        scl1 = Pin(config.scl1)
        i2c1_freq = config.i2c1_freq
        self.i2c1 = I2C(1, sda=sda1, scl=scl1, freq=i2c1_freq)

        if self.wireless:
            # Init wireless
            self.log.info("Wireless detected, configuring network")
            self.wifi = wireless()
            connected = False
            while connected == False:
                connected = self.wifi.start_wifi()
            
            # Init web server
            self.log.info("Configuring core website")
            self.picoserver = website()
        
        # Local and remote modules config
        self.log.info("Configuring available modules")
        modules = self.init_modules()
        if len(modules) > 0:
            self.log.info("Detected and enabled the following modules (Module name : I2C Address)")
            for module in modules:
                self.log.info(str(module.key()) + " : " + str(module["address"]))
        else: 
            self.log.info("No modules enabled")

        # Build asyncio loop for website
        if self.wireless:
            self.log.info("Configuring program loop with webserver")
            self.loop = self.picoserver.run()
            self.log.info("Starting hub program loop")
            self.loop.run_forever()

    def init_modules(self) -> dict:
        """
        Configures requested local modules and scans the I2C bus for modules
        that return matching module IDs and returns a list of all enabled
        modules with keys for moduleID and address
        """
        self.log.info("The following modules are registered on this hub:")
        self.log.info(self.registered_modules)
        self.enabled_modules = {}
        
        # Configure local modules
        for module in self.local_modules:
            # If module name via registered module lookup is in supported modules - configure module
            if (module in self.registered_modules):
                self.log.info("Configuring local module: " + module)
                self.enabled_modules[module] = {"moduleID": config.registered_modules[module], "address" : "local"}
            
            else:
                self.log.info("Skipping unregistered module: " + module)
        
        # Scan for I2C modules
        self.log.info("Scanning I2C bus for modules")
        devices = self.i2c1.scan()
        if devices:
            self.log.info("I2C devices found")
            for device in devices:
                moduleID = i2c_utils.get_i2c_module_id(self.i2c1, device)
                self.log.info("Address: " + str(device) + " : Module ID: " + str(moduleID))
                if moduleID in self.registered_modules.values():
                    self.enabled_modules[self.get_module_name(moduleID)] = {"moduleID": moduleID, "address" : device}
        else:
            self.log.info("No I2C devices found")
        
        # configuration - manually add your module lines here
        self.log.info("Configuring enabled modules")

        if "lights" in self.enabled_modules.keys():
            self.log.info("Lights enabled, configuring...")
            self.lights = pba_lights()
            if self.wireless:
                self.log.info("Configuring lights website")
                self.lights.init_web(self.picoserver, self.enabled_modules["lights"]["address"])

        if "relays" in self.enabled_modules.keys():
            self.log.info("Relays enabled, configuring...")
            self.relays = pba_relays()
            if self.wireless:
                self.log.info("Configuring relays website")
                self.relays.init_web(self.picoserver)

        ## Template code for custom module config
        # if "<module_name>" in enabled_names:
        #     self.<module_name> = pba_<module_name>()
        #     if self.wireless:
        #         self.<module_name>.init_web()

        return self.enabled_modules
    
    def get_module_name(self, moduleID: int) -> str:
        keys = [k for k, v in self.registered_modules.items() if v == moduleID]
        if keys:
            return keys[0]
        return "Invalid module ID"
    
    def detect_wireless(self) -> bool:
        return True # TODO actually detect wireless