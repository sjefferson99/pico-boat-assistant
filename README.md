# Pico-boat-assistant

A pico powered network of boat automation devices with the ultimate goal of proividing cheap, configurable options to automating your boat (or any space really), with integrations with [Signal-K](https://github.com/SignalK) (open source boat networking protocol) and [Home-Assistant](https://github.com/home-assistant) (awesome home automation server). Hence Pico-boat-assistant.

This diagram outlines the elements built so far, planed development and the wider ecosystem in which this solution could sit:

![PBA network diagram](docs/images/Pico%20Boat%20Assistant%20network.drawio.png)

Please see the [getting started](docs/getting-started.md) documentation for more information.

## Pre release version
There is now enough implemented that all functions will work from pico-lights and pico-power, assuming that the hub module is directly connected to the relays and the lights module is connected over I2C.

At present, the code will connect to a wifi network, build a core website and serve it on the IP allocated by DHCP on port 80.
The module will assume it is a Pico W with a relay board attached and load a local relay control module. If connected via I2C, a pico running the latest firmware in pico-lights will be detected and all pico-lights functions are available over the API via I2C.

The index page provides links to the lights and relays pages and APIs.

## Components
### PBA wireless hub
A Pico W device acts as an I2C hub for all other PBA devices and hosts a basic web server and API over wireless. It can also load a module to directly control power (lights to follow in future dev).

### PBA power
Module (currently only works on the hub device) to control relays via GPIO.

### PBA lights
Module (currently only works connecting to the hub device over I2C) to provide PWM dimmable control over 16 LED strips via step up transistors.