# Incomplete project
None of the below fully works as a unified solution as yet.

At present, the code will connect to a wifi network, build a core website and serve it on the IP allocated on port 80.
A local relay function will load and a remote pico-lights board running the latest pico-lights repo version will detect on the I2C bus

The relay website presents and responds to API calls as documented on the hoome page, the code assumes local operation and needs logic to abstract hardware from webserver over I2C

As yet the lights commands are not configured or presented on the hub website. Pulling these in from the other repos next.

# Pico-boat-assistant
A pico powered network of boat automation devices with the ultimate goal of proividing cheap, configurable options to automating your boat (or any space really), with integrations with [Signal-K](https://github.com/SignalK) (open source boat networking protocol) and [Home-Assistant](https://github.com/home-assistant) (awesome home automation server). Hence Pico-boat-assistant.

## Pico-boat-assistant core
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

## Pico-display - Not implemented yet
### Module details

## Pico-lights - Not fully implemented yet
### Module details
The Boatman pico lights module forms part of a wider Boatman ecosystem documented in the [Boatman project repository](https://github.com/sjefferson99/Boatman-project)

The hardware detailed below is built around the relatively new Raspberry Pi Pico microprocessor using the micropython firmware option.

The module leverages all of the 16 onboard PWM drivers, which should be fed into LED driver circuitry to address the current requirements of LED strips (See hardware section).

Control of the module is performed by a custom protocol on the I2C bus, using a community library to have the pico present as an I2C slave on the bus.
A pico hub module performs the role of I2C master and depending on the hub, will have a variety of ways to drive the lights module config (Serial UART, REST API, web page etc.)

### Wiring pinout
The module does not use any off the shelf Pico hats and is wired directly to the level shifters for the LED strips and connects to the hub module by 2 wire I2C as illustrated in the pinout diagram:
![Pico lights pinout diagram](/images/LED%20PICO%20Pinout.drawio.png)

### Pico firmware
This module release was developed against [Pico Micropython v1.18](https://micropython.org/resources/firmware/rp2-pico-20220117-v1.18.uf2).

See https://micropython.org/download/rp2-pico/ for more details.

### Configuration
As of this release, group configruation is hard coded and must be updated in firmware. Future releases are planned to allow configuration to be set remotely by the Boatman hub. The firmware should set var "groupConfigInSync == FALSE" on startup, to ensure an error is produced until the Boatman hub issues a group sync command to reduce the risk of unexpected group control behaviour.

### Hardware
- Raspberry Pi Pico: [Pi hut pico](https://thepihut.com/products/raspberry-pi-pico)
- MOSFET PWM Drivers: [Amazon Mosfet with connectors on PCB](https://www.amazon.co.uk/gp/product/B07QVZK39F/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
- 2x1Kohm resistors
- Push button reset switch (optional)

## Pico-Power - Not fully implemented yet
### Module details

Pico W based relay controller for web based control of DC and AC circuits onboard.

This code is built around the [Pimoroni Pico W firmware v1.19.9](https://github.com/pimoroni/pimoroni-pico/releases/download/v1.19.9/pimoroni-picow-v1.19.9-micropython.uf2)

### Hardware
- Uses Pico W board mounted on the [PiHut relay board](https://thepihut.com/products/raspberry-pi-pico-relay-board)

- Optional LiPo and charger shim allows the Pico to reset circuits it is powered by without shutting down, you will need to connect VSYS to VBUS to power the relays from the shim.
  - [Battery](https://thepihut.com/products/2000mah-3-7v-lipo-battery?variant=42143258050755)
  - [Charging shim](https://thepihut.com/products/lipo-shim-for-pico?variant=39809509785795)

### Usage
- Populate wifi SSID and password in the config.py file
- Set the startup relay states in the config.py file using the dictionary format example given.
- Determine pico IP from DHCP server (hostname appears to be "PYBD")
- Navigate to http://<pico IP>:80 for further instructions

### LED behaviour
#### Board power
The board has a power LED to show that the Pico AND the relay board have power i.e. 5v on VBUS as opposed to just VSYS.
#### Relay state
The relays each have an LED to show relay state on/off.
#### Pico LED
The Pico LED is normally off in proper operation.

When connecting to the wifi the LED will flash once per second. Should the conection fail, the LED will flash 5 times per second for the retry backoff period then loop back to connecting.

### Connectivity watchdog - Not implemented yet
Refer to the config file comments for options to enable polling a specified website at a given interval for a successful http response and take action to reset a specified relay and rerun the wifi connection on any failures.

## Adding a module
Dynamic importing of modules is currently beyond me. To create a new module perform the following steps.
- Copy the template_module folder and rename to your module name
- Adjust the class name in __init__.py to pba_<your_module_name>
- Add a sys path and import line to the top of hub.py similar to lights and relay
- Add an entry to the registered_modules list in config.py, increment the ID number to an unused value, use this ID in the module definition
- Copy the template code block in the hub.py section under comment "# configuration - manually add your module lines here", uncomment and adjust instances of <module_name> to init your module