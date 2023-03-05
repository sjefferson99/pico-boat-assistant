import logging as logging
from machine import I2C, Pin
from pba_i2c import pba_i2c_hub
import config as config
import sys
sys.path.append("/lights")
from lights import pba_lights
sys.path.append("/relays")
from relays import pba_relays
from networking import wireless
from webserver import website
import os
import json
from uasyncio import Loop

class pba_hub:
    """
    Pico Boatman hub device, polls I2C responder modules to control or
    return information as sensors.
    """
    def __init__(self, local_modules: list) -> None:
        # Init logging
        self.log = logging.getLogger('hub')
        self.log.info("Init I2C Hub")
        # Set version for use in communication protocol compatibility
        self.version = str("0.1.0")
        # Configure module information
        self.local_modules = local_modules
        self.registered_modules = config.registered_modules
        
        # Init I2C
        self.i2c1 = self.init_i2c_interface()
        self.pba_i2c = pba_i2c_hub(self.i2c1)

        # Detect if wireless module present and configure
        if self.detect_wireless():
            self.log.info("Wireless module detected, configuring")
            self.wireless_enabled = True
            self.wifi = self.init_wireless()
            
            # Init web server
            self.log.info("Configuring core website")
            # Builds the basic website framework ready for modules
            self.picowebsite = self.create_website()
        else:
            self.wireless_enabled = False
        
        # Local and remote modules config
        self.log.info("Configuring available modules")
        modules = self.init_modules()
        print(modules)
        if len(modules) > 0:
            self.log.info("Detected and enabled the following modules (Module name : I2C Address)")
            for module in modules:
                self.log.info(module + " : " + str(modules[module]["address"]))
        else: 
            self.log.info("No modules enabled")

        # Build and run asyncio loop for website
        if self.is_wireless_enabled():
            self.launch_webserver()

    def init_i2c_interface(self) -> I2C:    
        """Init I2C as hub"""
        sda1 = Pin(config.sda1)
        scl1 = Pin(config.scl1)
        i2c1_freq = config.i2c1_freq
        return I2C(1, sda=sda1, scl=scl1, freq=i2c1_freq)

    def get_pba_i2c(self):
        return self.pba_i2c
    
    def init_wireless(self) -> wireless:
        """Init the wireless module"""
        self.log.info("Configuring wireless network")
        wifi = wireless()
        connected = False
        while connected == False:
            connected = wifi.start_wifi()
        return wifi
    
    def is_wireless_enabled(self) -> bool:
        """Boolean check if wireless is configured"""
        if self.wireless_enabled:
            return True
        else:
            return False
    
    def get_wireless(self) -> wireless:
        """Return the wireless interface configuration"""
        return self.wifi
    
    def create_website(self) -> website:
        """Create a base website object"""
        site = website()
        return site
    
    def get_website(self) -> website:
        """Return the current hub website configuration"""
        return self.picowebsite
    
    # No longer used, but keeping funciton for now
    def delete_file(self, filename) -> bool:
        """
        Delete the filename passed from the root of the filesystem.
        Return True if file existed, False if it did not and no action taken.
        """
        if filename in os.listdir():
            self.log.info("Removing file: " + filename)
            os.remove(filename)
            return True
        else:
            self.log.info("No file to delete: " + filename)
            return False

    def init_modules(self) -> dict:
        """
        Configures requested local modules and scans the I2C bus for modules
        that return matching module IDs and returns a list of all enabled
        modules with keys for moduleID and address
        """
        self.log.info("The following modules are registered on this hub:")
        self.log.info(self.registered_modules)
        self.enabled_modules = {}
        
        # Populate list of local modules
        for module in self.local_modules:
            if (module in self.registered_modules):
                self.log.info("Configuring local module: " + module)
                self.enabled_modules[module] = {"moduleID": config.registered_modules[module], "address" : "local"}
            
            else:
                self.log.info("Skipping unregistered module: " + module)
        
        # Scan for I2C modules and populate names, IDs and addresses
        self.log.info("Scanning I2C bus for modules")
        devices = self.i2c1.scan()
        if devices:
            self.log.info("I2C devices found")
            for device in devices:
                moduleID = self.pba_i2c.get_i2c_module_id(device)
                self.log.info("Address: " + str(device) + " : Module ID: " + str(moduleID))
                if moduleID in self.registered_modules.values():
                    self.enabled_modules[self.get_module_name(moduleID)] = {"moduleID": moduleID, "address" : device}
        else:
            self.log.info("No I2C devices found")
        
        # Module configuration - manually add your module lines here using the
        # template as a guide - current approach assumes the hub has all module
        # config information with compatible module firmware versions attached

        # TODO Thought: make the module responsible for HTML and execution.
        #  Hub queries for API definition and HTML and passes everything through
        #  to module over I2C

        self.log.info("Configuring enabled modules")

        # Configures lights module instance if enabled
        if "lights" in self.enabled_modules.keys():
            self.log.info("Lights enabled, configuring...")
            self.lights = pba_lights(self)

        # TODO pass hub as we do with lights module above
        if "relays" in self.enabled_modules.keys():
            self.log.info("Relays enabled, configuring...")
            # Configures relays module instance
            self.relays = pba_relays()
            #Configures relays module web pages and API if wireless available
            if self.wireless_enabled:
                self.log.info("Configuring relays website")
                self.relays.init_web(self.picowebsite)

        ## Template code for custom module config
        # if "<module_name>" in enabled_names:
        #     # Configures module instance  
        #     self.<module_name> = pba_<module_name>()
        #     #Configures module web pages and API if wireless available
        #     if self.wireless:
        #         self.<module_name>.init_web()

        return self.enabled_modules
    
    def get_module_name(self, moduleID: int) -> str:
        """
        Return module name from the module ID using the registered module list
        built on init
        """
        keys = [k for k, v in self.registered_modules.items() if v == moduleID]
        if keys:
            return keys[0]
        return "Invalid module ID"
    
    def get_enabled_modules(self) -> dict:
        return self.enabled_modules
    
    def detect_wireless(self) -> bool:
        """
        Detect if the Pico is a W model with wireless chip.
        Currently always returns True, needs deteciton logic
        """
        return True # TODO actually detect wireless
    
    def launch_webserver(self):
        self.log.info("Configuring program loop with webserver")
        self.loop = self.picowebsite.run()
        self.log.info("Starting hub program loop")
        self.loop.run_forever()
    
    def get_async_loop(self) -> Loop:
        return self.loop