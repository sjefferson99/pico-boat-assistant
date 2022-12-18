from webserver import website
from lights.driver import lights_driver
from json import dumps

class lightapi:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, coresite: website, i2caddress: int) -> None:
        """
        Tinyweb server API definitions for lights to extend the webserver passed.
        """
        self.address = i2caddress
        # light API page
        @coresite.app.route('/light/api')
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
                    <li>List lights and names - GET /light/api/lights</li>
                    <li>Run a light demo - GET /light/api/demo</li>
                    </ul>
                    Data:
                    <ul>
                    </ul>
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)

        coresite.app.add_resource(lightlist, '/light/api/lights')
        coresite.app.add_resource(lightdemo, '/light/api/demo')
        #coresite.app.add_resource(light, '/light/api/lights/<lightid>')

class lightlist():

    def get(self, data):
        """Return list of all lights"""
        driver = lights_driver()
        return dumps(driver.list_lights(65)) # TODO get passed actual I2C address

class lightdemo():

    def get(self, data):
        """Return list of all lights"""
        driver = lights_driver()
        return dumps(driver.demo(65)) # TODO get passed actual I2C address

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
