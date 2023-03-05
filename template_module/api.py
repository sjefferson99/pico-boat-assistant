from webserver import website
from template_module.driver import template_board
from json import dumps

class templateapi:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, coresite: website) -> None:
        """
        Tinyweb server API definitions for template to extend the webserver passed.
        """
        # Template API page
        @coresite.app.route('/api/template')
        async def api(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>template control API definition</h1>                
                    <p>
                    Use the following endpoints to drive the pico templates with appropriate data:
                    <ul>
                    <li>List templates and names - GET /api/template/list</li>
                    <li>Switch or toggle template - PUT /api/template/{template number (1-4)}</li>
                    </ul>
                    Data:
                    <ul>
                    <li>type="switch"/"toggle" (Switch=Switch to given value, toggle=Switch initial value and switch to opposite value after 500ms)</li>
                    <li>value="0"/"1" (0=Common connected to NC, 1=Common connected to NO)</li>
                    </ul>
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)

        coresite.app.add_resource(templatelist, '/api/template/list')
        coresite.app.add_resource(template, '/api/template/<templateid>')

class templatelist():

    def get(self, data):
        """Return list of all templates"""
        hardware = template_board()
        return dumps(hardware.list_templates())

class template():
    def put(self, data, templateid):
        """Switch template"""
        value = data["value"]
        type = data["type"]
        print("Received API call - templateid {}, type: {}, value: {}".format(templateid, type, value))
        hardware = template_board()
        if type == "switch":
            print("API call to switch")
            hardware.template_switch(int(templateid), int(value))
            # Return message AND set HTTP response code to "200"
            return {'message': 'Switched'}, 200
        elif type == "toggle":
            print("API call to toggle")
            hardware.template_toggle(int(templateid), 500, int(value))
            # Return message AND set HTTP response code to "200"
            return {'message': 'Toggled'}, 200
        else:
            print("Incorrect data provided to templates API")
            # Return message AND set HTTP response code to "200"
            return {'message': 'Error'}, 500
