import core
import logging

"""
Instantiates Pico Boat Assistant class, this class autoloads and detects
modules and starts a TinyWeb server running on asyncio
"""

log = logging.getLogger('main')
log.info("Creating core class")

pba = core.pico_boat_assistant()