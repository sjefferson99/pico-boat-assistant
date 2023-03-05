from lights.driver import lights_driver
from json import dumps
import hub

class lightapi:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, hub: hub.pba_hub) -> None:
        """
        Tinyweb server API definitions for lights to extend the webserver passed.
        """
        self.hub = hub
        coresite = hub.get_website()
        # light API page
        @coresite.app.route('/api/lights')
        async def api(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>Light control API definition</h1>                
                    <p>
                    Use the following endpoints to drive the pico lights with appropriate data:
                    <ul>
                    <li><a href="/api/lights/list">List lights and names</a> - GET /api/lights/list (Dummy data)</li>
                    <li><a href="/api/lights/demo">Run a light demo</a> - GET /api/lights/demo (Dummy data)</li>
                    <li><a href="/api/lights/address">Return lights module address (Type error if local)</a> - GET /api/lights/address</li>
                    <li><a href="/api/lights/islocal">Return if lights module is local</a> - GET /api/lights/islocal</li>
                    <li>Turn on a light - PUT /api/lights/on/{light id} (Dummy data)</li>
                    </ul>
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)

        coresite.app.add_resource(lightlist, '/api/lights/list', hub=self.hub)
        coresite.app.add_resource(lightdemo, '/api/lights/demo', hub=self.hub)
        coresite.app.add_resource(get_address, '/light/api/address', hub=self.hub)
        coresite.app.add_resource(is_local, '/api/lights/islocal', hub=self.hub)
        coresite.app.add_resource(on, '/api/lights/on/<lightid>', hub=self.hub)
        #coresite.app.add_resource(light, '/light/api/lights/<lightid>')

class lightlist():

    def get(self, data, hub):
        """Return list of all lights"""
        driver = lights_driver(hub)
        html = dumps(driver.list_lights())
        return html

class lightdemo():

    def get(self, data, hub):
        """Return list of all lights"""
        driver = lights_driver(hub)
        html = dumps(driver.demo())
        return html

class on():

    def put(self, data, lightid, hub):
        """Turns on a light"""
        print("Received API call - relayid {}".format(lightid))
        driver = lights_driver(hub)
        html = dumps(driver.light_on(lightid))
        return html


# Test info, shouldn't be needed and implemented in the driver
class get_address():

    def get(self, data, hub):
        """Return address of module"""
        driver = lights_driver(hub)
        html = dumps(driver.get_address())
        return html
    
class is_local():

    def get(self, data, hub):
        """Return address of module"""
        driver = lights_driver(hub)
        html = dumps(driver.is_local())
        return html

# class light():
#     def put(self, data, lightid):
#         """Switch light"""
#         value = data["value"]
#         type = data["type"]
#         print("Received API call - lightid {}, type: {}, value: {}".format(lightid, type, value))
#         hardware = light_board()
#         if type == "switch":
#             print("API call to switch")
#             hardware.light_switch(int(lightid), int(value))
#             # Return message AND set HTTP response code to "200"
#             return {'message': 'Switched'}, 200
#         elif type == "toggle":
#             print("API call to toggle")
#             hardware.light_toggle(int(lightid), 500, int(value))
#             # Return message AND set HTTP response code to "200"
#             return {'message': 'Toggled'}, 200
#         else:
#             print("Incorrect data provided to lights API")
#             # Return message AND set HTTP response code to "200"
#             return {'message': 'Error'}, 500
