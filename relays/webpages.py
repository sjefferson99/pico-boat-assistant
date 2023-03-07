from webserver import website

class relaysite:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, coresite: website) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        # Relay page
        @coresite.app.route('/relays')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>Relay control</h1>                
                    <p>
                    There is not currently a web form feature available. Please refer to the <a href="/api/relays">API reference - /api/relays</a> for interacting with the REST API.
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)