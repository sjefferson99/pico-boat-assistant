from webserver import website
import hub

class lightsite:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, hub: hub.i2c_hub) -> None:
        """
        Tinyweb server definitions for the template board to extend the webserver passed.
        """
        # template page
        coresite = hub.get_website()
        @coresite.app.route('/light')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>Light control</h1>                
                    <p>
                    There is not currently a web form feature available. Please refer to the <a href="/light/api">API reference</a> for interacting with the rest API.
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)