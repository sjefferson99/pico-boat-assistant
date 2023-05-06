# Getting started
Pico Boat Assistant is set of pico based modules that allow smart boat management of power, lights and anything else that can be controlled by Pico GPIO.

The basic architecture is a Pico W device acting as a wireless hub with a basic web server for control and API access to the functions for devices on the network. The hub module communicates with other devices via I2C to allow considerable expandability where more GPIO is needed that one pico can provide.

## What currently works
At present the power and lights modules have a basic functionality and the power module must be the wireless hub device with the lights module connected over I2C.

You can see hardware and pinout information to connect everything up for each module:

 - [Pico Hub](modules/hub.md)
 - [Pico Power](modules/power.md)
 - [Pico Lights](modules/lights.md)

 You will need to upload the code in this repository to the hub/power device, and for now, the lights module will need to be loaded from the [Pico Lights](https://github.com/sjefferson99/Boatman-pico-lights) repo.

 Finally ensure config.py on the hub device is set up appropriately according to the comments.