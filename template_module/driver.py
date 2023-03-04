import logging as logging

class template_board:

    def __init__(self) -> None:
        """
        Creates abstraction for template
        Extends base tinyweb server with template functionality
        Execute demo() for a board self test
        """
        self.log = logging.getLogger('template')

    def list_templates(self) -> None:
        pass

    def template_switch(self, relay: int, value: int=1) -> None:
        pass

    def template_toggle(self, relay: int, duration_ms: int = 1000, initial_value: int=1) -> None:
        pass
    
    def demo(self) -> None:
        """Demo of functionality for quick testing"""
        self.log.info("Performing template demo")