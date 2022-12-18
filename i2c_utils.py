from machine import I2C

def send_data(i2c: I2C, data: list, address: int) -> None:
    """
    Send one byte of data over I2C, padding as needed to byte boundary.
    """
    # Pad data to protocol length
    while len(data) < 8:
        data.append(0)

    sendData = bytearray(data)
    i2c.writeto(address, sendData)

def get_i2c_module_id(i2c: I2C, address: int) -> int:
    """
    Query I2C module for its one byte module ID and return, provide the i2c
    object to communicate via and the target address
    """
    command_byte = 0b10000001
    data = []
    data.append(command_byte)
    send_data(i2c, data, address)
    #Expect one byte status return
    returnData = i2c.readfrom(address, 1)
    returnData = int(returnData[0])
    return returnData