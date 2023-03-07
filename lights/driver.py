import logging as logging
import hub
from pba_i2c import pba_i2c_hub
from machine import I2C
from time import sleep_ms
import json

class lights_driver:
    def __init__(self, hub: hub.pba_hub) -> None:
        """
        Driver for executing various lights functions to be called
        by the API definitions or local code where no web server exists.
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('lights_driver')
        self.log.info("Loading lights driver")

        self.hub = hub

        self.enabled_modules = self.hub.get_enabled_modules()

        self.address = self.enabled_modules["lights"]["address"]
        if self.address == "local":
            self.log.info("Lights module is local")
            self.local = True
        else:
            self.log.info("Lights module is at I2C address: " + str(self.address))
            self.local = False

        self.i2c_hub_interface = hub.get_i2c_interface()

        self.pba_i2c_lights = pba_i2c_hub_lights(self.i2c_hub_interface)

    def is_local(self) -> bool:
        return self.local            
    
    def get_address(self) -> int:
        return self.address
    
    ##############################
    # Abstracted light functions #
    ##############################
    def set_light(self, lightid: int, brightness: int) -> str:
        self.log.info("Setting light brightness value: " + str(lightid) + " : " + str(brightness))
        if self.is_local():
            result = self.set_local_light(lightid, brightness)
        else:
            result = self.set_remote_light(lightid, brightness, self.get_address())
        return "Attempted to turn light on: " + str(lightid) + " : " + result
    
    def set_group(self, groupid: int, brightness: int) -> str:
        self.log.info("Setting group brightness value: " + str(groupid) + " : " + str(brightness))
        if self.is_local():
            result = self.set_local_light(groupid, brightness)
        else:
            result = self.set_remote_group(groupid, brightness, self.get_address())
        return "Attempted to turn light on: " + str(groupid) + " : " + result
    
    def remote_set_light_demo(self) -> str:
        self.pba_i2c_lights.remote_set_light_demo(self.get_address())
        return "Executed remote set light demo"

    def get_groups(self) -> dict:
        return self.pba_i2c_lights.get_groups(self.get_address())
    
    # TODO Add local lights hardware driver functions
    # Add functions for parsing lights commands from the I2C network
    ##########################
    # Local light functions  #
    ##########################
    def set_local_light(self, lightid: int, brightness: int) -> str:
        self.log.info("Turning on local light")
        return "Success"
    
    # TODO Add functions for passing lights commands over the I2C network
    ##########################
    # Remote light functions #
    ##########################
    def set_remote_light(self, lightid: int, brightness: int, address: int) -> str:
        self.log.info("Turning on remote light")
        result = self.pba_i2c_lights.set_light(address, False, lightid, brightness)
        return str(result)
    
    def set_remote_group(self, groupid: int, brightness: int, address: int) -> str:
        self.log.info("Turning on remote group")
        result = self.pba_i2c_lights.set_group(address, False, groupid, brightness, self.hub)
        return str(result)
    
class pba_i2c_hub_lights(pba_i2c_hub):
    def __init__(self, i2c: I2C) -> None:
        super().__init__(i2c)
        """
        Class for lights module specific extensions to the PBA I2C interface
        """
        ###########################
        # I2C Pico light controller
        ###########################
        #
        # Command protocol:
        #
        # 0b01GRIIII 0bDDDDDDDD (6 bytes of 0) - set light or light group duty cycle
        # G: 1 = Group, 0 = Individual light
        # R: 1 = Reset other lights to duty cyle of 0, 0 = update only this target
        # IIII = 4 bit Light or Group ID
        # DDDDDDDD = 0-255 Duty cycle value 0 = off, 255 = fully on
        #
        # 0b1xxxxxxx: Get/set config data
        # 0b10000001: Get module ID - Pico lights should return 0b00000010
        # 0b10000010: Get version
        # 0b10000011: Get group assignments
        
        self.log = logging.getLogger('pba_i2c_hub_lights')
        self.log.info("Instantiating lights specific i2c interface")
        self.version = str("0.2.0")
        self.moduleID = 0b00000010
        self.set_light_bits = 0b01000000
        self.group_bit = 0b00100000
        self.reset_bit = 0b00010000
        self.get_groups_byte = 0b10000011

    def set_light(self, address: int, reset: bool, id: int, duty: int) -> int:
        """
        address: address of target I2C lights controller module
        reset: true = set all other lights off and apply this light configuration only
        id: 4 bit (0-15) ID of the light to configure
        duty: 16 bit (0-255) duty for the light PWM fader, 0=off, 255=fully on
        Returns 0 on success or error code
        
        Error codes:
        -1: Command not recognised by pico_lights module
        -10: Light ID out of range
        -20: Duty value out of range
        """

        id = int(id) # This should not be needed and I have no idea why it is

        command_byte = self.set_light_bits

        if id >=0 and id <=15:
            command_byte += id
        else:
            return -10 #Light ID out of range

        if reset:
            command_byte += self.reset_bit
        
        data = []
        data.append(command_byte)

        if duty >=0 and duty <=255:
            data.append(duty)    
        else:
            return -20 #Duty out of range

        data.append(duty)
        self.send_data(data, address)        
        #Expect 1 byte status return
        returnData = self.i2c.readfrom(address, 1)
        return int.from_bytes(returnData, "big") * -1
    
    def remote_set_light_demo(self, address: int) -> None:
        l = 0
        while l <= 15:
            self.set_light(address, True, l, 255)
            sleep_ms(100)
            l +=1
        
        while l >= 0:
            self.set_light(address, True, l, 255)
            sleep_ms(100)
            l -=1
        
        self.set_light(address, True, 0, 0)

        l=0
        d=5
        while d <= 255:
            l=0
            while l <= 15:
                self.set_light(address, False, l, d)
                sleep_ms(50)
                l +=1
            d += 10
            if d > 100:
                d+= 40
        return
    
    def get_groups(self, address: int) -> dict:
        command_byte = self.get_groups_byte
        data = []
        data.append(command_byte)
        self.send_data(data, address)    
        #Expect 2 byte length data return
        returnData = self.i2c.readfrom(address, 2)
        length = int.from_bytes(returnData, "big")
        #Expects immediate send of the group config data in JSON, byte count
        #specified above
        returnData = self.i2c.readfrom(address, length)
        #Populate updated LED groups config data dict
        # TODO Fix why this shows as an error in pylance
        self.led_groups = json.loads(returnData.decode('utf-8'))
        return self.led_groups
    
    def set_group(self, address: int, reset: bool, id: int, duty: int, hub: hub.pba_hub) -> int:
        """
        address: address of target I2C lights controller module
        reset: true = set all other lights off and apply this group configuration only
        id: 4 bit (0-15) ID of the group to configure
        duty: 16 bit (0-255) duty for the light PWM fader, 0=off, 255=fully on
        hub: pba hub object for checking and updating hub group definitions
        Returns 0 on success or error code
        
        Error codes:
        -1: Command not recognised by pico_lights module
        -2: Pico_lights module group config out of sync
        -10: Group ID out of range
        -20: Duty value out of range
        -30: Group ID not in local config
        """

        data = []
        command_byte = self.set_light_bits + self.group_bit
        # Check valid light id
        if id >=0 and id <= 15:
            # Check group id is in known groups - update if not and check again
            if str(id) in hub.lights.list_groups()["config"]: #TODO fix received groups JSON so ints are not strings
                command_byte += id
            else:
                hub.lights.set_groups()
                if str(id) in hub.lights.list_groups()["config"]: #TODO fix received groups JSON so ints are not strings
                    command_byte += id
                else:
                    return -30 #Group ID not in local config 
        else:
            return -10 #Light ID out of range
        
        if reset:
            command_byte += self.reset_bit

        data.append(command_byte)

        if duty >=0 and id <=255:
            data.append(duty)    
        else:
            return -20 #Duty out of range
        
        self.send_data(data, address)        
        #Expect 1 byte status return
        returnData = self.i2c.readfrom(address, 1)
        return int.from_bytes(returnData, "big") * -1