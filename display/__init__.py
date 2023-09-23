import logging as logging
import hub
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
from machine import Pin
import utime as time

class pba_display:
    """
    Builds a display module instance.
    """
    def __init__(self, hub: hub.pba_hub) -> None:
        """
        Creates a display module class, for use by a hub and passes the instantiating hub as "self".
        Or initialises the remote display module
        """
        self.log = logging.getLogger('display')
        self.log.info("Init display module")
        self.hub = hub

        # Init display
        print("initialising display, LED and buttons")
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332, rotate=0)
        self.display.set_backlight(1.0)

        # Pico pens
        GREEN = self.display.create_pen(0, 255, 0)
        WHITE = self.display.create_pen(255, 255, 255)

        background_pen = GREEN
        text_pen = WHITE

        # Startup display
        self.display.set_pen(background_pen)                      # Set a green pen
        self.display.clear()                                 # Clear the display buffer
        self.display.set_pen(text_pen)                  # Set a white pen
        self.display.text("BoatMan", 10, 10, 240, scale = 4)         # Add some text
        self.display.text("Boat Manager", 10, 50, 240, scale = 2)    # Add some text
        self.display.update()                                # Update the display with our changes

        #Init buttons
        self.BUTTON_A = Pin(12, Pin.IN, Pin.PULL_UP)
        self.BUTTON_B = Pin(13, Pin.IN, Pin.PULL_UP)
        self.BUTTON_X = Pin(14, Pin.IN, Pin.PULL_UP)
        self.BUTTON_Y = Pin(15, Pin.IN, Pin.PULL_UP)