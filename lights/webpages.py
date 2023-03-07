from webserver import website
import hub

class lightsite:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, hub: hub.pba_hub) -> None:
        """
        Tinyweb server definitions for the template board to extend the webserver passed.
        """
        # template page
        coresite = hub.get_website()
        @coresite.app.route('/lights')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>Light control</h1>                
                    <p>
                    There is not currently a web form feature available. Please refer to the <a href="/api/lights">API reference - /api/lights</a> for interacting with the REST API.
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)