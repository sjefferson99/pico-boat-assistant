from webserver import website

class templatesite:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, coresite: website) -> None:
        """
        Tinyweb server definitions for the template board to extend the webserver passed.
        """
        # template page
        @coresite.app.route('/template')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>template control</h1>                
                    <p>
                    There is not currently a web form feature available. Please refer to the <a href="/template/api">API reference</a> for interacting with the rest API.
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)