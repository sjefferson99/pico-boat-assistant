## Pico-boat-assistant hub
### I2C
#### I2C Overview
The module presents as an I2C slave by default at address 0x41 defined in var "RESPONDER_ADDRESS".

The I2C frequency should be 100000 defined in var "I2C_FREQUENCY"

The master I2C device is expected to issue a command at the target address and then wait for the expected data length to be returned by the lights module for that command.

Each hub module has a pico lights library that is built around this premise and the following data structures. The variables module_id = 0b00000010 and version = str("x.y") can be interrogated by two of these commands in order to confirm that the library code will reliably work with this version of the boatman module.

Review pico_lights.py of a matching version in a Boatman hub module repository for an example implementation against this protocol.

#### I2C command protocol
Commands and data should be sent as a byte array.

The commands are constructed as a 1 byte command with supplementary data bytes as defined below where required. The pico module will read 8 bytes into the read buffer, so pad remaining data bytes with 0 to ensure no unexpected results.

##### 0b00xxxxxx: Reserved
##### 0b01xxxxxx: Get/set light values
0b01GRIIII 0bDDDDDDDD - set light or light group duty cycle
<br>
G: 1 = Group, 0 = Individual light
<br>
R: 1 = Reset other lights to duty cyle of 0, 0 = update only this target
<br>
IIII = 4 bit Light or Group ID
<br>
DDDDDDDD = 0-255 Duty cycle value 0 = off, 255 = fully on

##### 0b1xxxxxxx: Get/set config data
0b10000001: Get module ID - Pico lights should return 0b00000010
<br>
0b10000010: Get version
<br>
0b10000011: Get group assignments

#### I2C command expected data return
- 0b01xxxxxx: Get/set light values - 1 byte
  - 0: Success
  - 1: Received reserved command
  - 2: Group config out of sync (only on group set command, issue a group sync command)
  - 3: Unrecognised get/set config command
  - 10: Group ID out of range (only on group set command)
  - 20: Duty value out of range
  - 30: Group ID not in local config
- 0b10000001: Get module ID - 1 byte - 0b00000010
- 0b10000010: Get version - 1 byte big endian defining payload length - immediate send of version string, decode as ansi string e.g. "0.2.0"
- 0b10000011: Get group assignments - 2 bytes big endian defining payload length - immediate send of JSON of that length that can be fed into python json.loads(). This is a python dictionary for use in set light group command.