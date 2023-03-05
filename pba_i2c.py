from machine import I2C
import logging as logging

class pba_i2c_hub:
    """
    Pico Boatman I2C hub device, polls I2C responder modules to control or
    return information as sensors.
    """
    def __init__(self, i2c: I2C) -> None:
        # Init logging
        self.log = logging.getLogger('pba_i2c')
        self.log.info("Init I2C Hub")
        self.i2c = i2c

    def send_data(self, data: list, address: int) -> None:
        """
        Send one byte of data over I2C, padding as needed to byte boundary.
        """
        # Pad data to protocol length
        while len(data) < 8:
            data.append(0)

        sendData = bytearray(data)
        self.i2c.writeto(address, sendData)

    def get_i2c_module_id(self, address: int) -> int:
        """
        Query I2C module for its one byte module ID and return, provide the i2c
        object to communicate via and the target address
        """
        command_byte = 0b10000001
        data = []
        data.append(command_byte)
        self.send_data(data, address)
        #Expect one byte status return
        returnData = self.i2c.readfrom(address, 1)
        returnData = int(returnData[0])
        return returnData