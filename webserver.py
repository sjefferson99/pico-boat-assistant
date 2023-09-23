from tinyweb import webserver
import uasyncio

class website:
    """
    Creates a pico webserver ready for modules
    """    
    def __init__(self) -> None:
        self.app = webserver()

        # Index page
        @self.app.route('/')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            # TODO abstract to set of HTML pages for easier content editing
            html = """<!DOCTYPE html>
            <html>
                <head> <title>Pico-Boat-Assistant</title> </head>
                <body> <h1>Pico-Boat-Assistant: A Pico powered modular web driven control system for boats</h1>
                    <p>
                    Use the following URL suffixes to drive functions on this Pico:
                        <ul>
                        <li><a href="/lights">/lights</a> - Lights module control</li>
                        <li><a href="/relays">/relays</a> - Relays module control</li>
                        </ul>
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)

    def run(self): # -> uasyncio.Loop:
        loop = self.app.run(host='0.0.0.0', port=80, loop_forever=False)
        return loop