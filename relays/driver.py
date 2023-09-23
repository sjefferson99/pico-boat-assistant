from utime import sleep
from machine import Pin

class relay_board:
    """
    Creates driver abstraction for the pi hut 4 opto relay board for Pico W.
    Maps relays to GP18-21.
    To be called by the API definitions or local code where no web server
    exists.
    Execute demo() for a board self test
    """

    def __init__(self) -> None:
        self.pin_mapping = {1: 18, 2: 19, 3: 20, 4: 21}
        self.relays = {}
        self.states = {0: "off", 1: "on"}
        #Build pin objects
        x = 1
        p = 18
        while x <= 4:
            self.relays[x] = Pin(p, Pin.OUT)
            x += 1
            p += 1
    
        # TODO Determine if relays are local or I2C networked and get address
        # TODO Add functions for passing relays commands over the I2C network
        # TODO Add functions for parsing relays commands from the I2C network
        
    def relay_toggle(self, relay: int, duration_seconds: float = 1, initial_value: int=1) -> None:
        """For specified relay, connects common to intiial value terminal for specified duration in ms then toggles to the opposite terminal
        Initial value:
        1: Common connected to NO
        0: Common connected to NC
        """
        print("Toggling relay: " + str(relay) + " to value: " + str(initial_value) + " for duration: " + str(duration_seconds))
        self.relays[relay].value(initial_value)
        sleep(duration_seconds)
        self.relays[relay].toggle()

    def relay_switch(self, relay: int, value: int=1) -> None:
        """For specified relay, connects common to value terminal
        Value:
        1: Common connected to NO
        0: Common connected to NC
        """
        print("Switching relay: " + str(relay) + " to value: " + str(value))
        self.relays[relay].value(value)

    def list_relays(self) -> list:
        x = 1
        relaylist = []
        while x <= 4:
            relaylist.append([x, "Relay " + str(x)]) #Generate some names for illustrative purposes
            x += 1
        return relaylist

    def demo(self) -> None:
        """Cycles quickly through toggling each relay"""
        print("Executing relay demo")
        x = 1
        while x <= 4:
            self.relay_switch(x, 1)
            sleep(0.2)
            x += 1
        x = 1
        while x <= 4:
            self.relay_switch(x, 0)
            sleep(0.2)
            x += 1
        x = 1
        while x <= 4:
            self.relay_toggle(x, 100, 1)
            sleep(0.2)
            x += 1