## Pico-lights
### Module details
The Boatman pico lights module forms part of a wider Boatman ecosystem documented in the [Boatman project repository](https://github.com/sjefferson99/Boatman-project)
This is now being refactored into the Pico Boat Assistant project (this repo), but so far the PBA project only supports remote control of a lights module that is running firmware from the original [Pico Lights repo](https://github.com/sjefferson99/Boatman-pico-lights)

The hardware detailed below is built around the Raspberry Pi Pico microprocessor using the micropython firmware option.

The module leverages all of the 16 onboard PWM drivers, which should be fed into LED driver circuitry to address the current requirements of LED strips (See hardware section).

Control of the module is performed by a custom protocol on the I2C bus, using a community library to have the pico present as an I2C slave on the bus.
A pico hub module performs the role of I2C master which is controlled via API on a small web server hosted on the wireless network of the hub module.

### Wiring pinout
The module does not use any off the shelf Pico hats and is wired directly to the level shifters for the LED strips and connects to the hub module by 2 wire I2C as illustrated in the pinout diagram:
![Pico lights pinout diagram](../images/LED%20PICO%20Pinout.drawio.png)

### Pico firmware
This module release was developed against [Pico Micropython v1.18](https://micropython.org/resources/firmware/rp2-pico-20220117-v1.18.uf2).

See https://micropython.org/download/rp2-pico/ for more details.

### Configuration
As of this release, group configuration is hard coded and must be updated in firmware. Future releases are planned to allow configuration to be set remotely by the PBA hub. The firmware should set var "groupConfigInSync == FALSE" on startup, to ensure an error is produced until the Boatman hub issues a group sync command to reduce the risk of unexpected group control behaviour.

### Hardware
- Raspberry Pi Pico: [Pi hut pico](https://thepihut.com/products/raspberry-pi-pico)
- MOSFET PWM Drivers: [Amazon Mosfet with connectors on PCB](https://www.amazon.co.uk/gp/product/B07QVZK39F/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
- 2x1Kohm resistors
- Push button reset switch (optional)