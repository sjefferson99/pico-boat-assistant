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
                    <li><a href="/api/lights/getlights">List lights and names</a> - GET /api/lights/getlights</li>
                    <li><a href="/api/lights/demo">Run a light demo</a> - GET /api/lights/demo</li>
                    <li><a href="/api/lights/address">Return lights module address (Type error if local)</a> - GET /api/lights/address</li>
                    <li><a href="/api/lights/islocal">Return if lights module is local</a> - GET /api/lights/islocal</li>
                    <li>Turn on a light - PUT /api/lights/light/on/{light id}</li>
                    <li>Turn off a light - PUT /api/lights/light/off/{light id}</li>
                    <li>Set a light's brightness - PUT /api/lights/light/brightness/{light id} - put data: {"brightness" = 0-255}</li>
                    <li><a href="/api/lights/getgroups">Return JSON of group configuration from lights module</a> - GET /api/lights/getgroups</li>
                    <li><a href="/api/lights/listgroups">Return JSON of group configuration on hub</a> - GET /api/lights/listgroups</li>
                    <li>Turn on a group - PUT /api/lights/group/on/{group id}</li>
                    <li>Turn off a group - PUT /api/lights/group/off/{group id}</li>
                    <li>Set a group's brightness - PUT /api/lights/group/brightness/{group id} - put data: {"brightness" = 0-255}</li>
                    </ul>
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)

        coresite.app.add_resource(get_lights, '/api/lights/getlights', hub=self.hub)
        coresite.app.add_resource(lightdemo, '/api/lights/demo', hub=self.hub)
        coresite.app.add_resource(get_address, '/api/lights/address', hub=self.hub)
        coresite.app.add_resource(is_local, '/api/lights/islocal', hub=self.hub)
        coresite.app.add_resource(light_on, '/api/lights/light/on/<lightid>', hub=self.hub)
        coresite.app.add_resource(light_off, '/api/lights/light/off/<lightid>', hub=self.hub)
        coresite.app.add_resource(light_brightness, '/api/lights/light/brightness/<lightid>', hub=self.hub)
        coresite.app.add_resource(get_groups, '/api/lights/getgroups', hub=self.hub)
        coresite.app.add_resource(list_groups, '/api/lights/listgroups', hub=self.hub)
        coresite.app.add_resource(group_on, '/api/lights/group/on/<lightid>', hub=self.hub)
        coresite.app.add_resource(group_off, '/api/lights/group/off/<lightid>', hub=self.hub)
        coresite.app.add_resource(group_brightness, '/api/lights/group/brightness/<groupid>', hub=self.hub)

class get_lights():  # TODO create driver function to return this data

    def get(self, data, hub):
        """Returns a list of lights and their names"""
        driver = lights_driver(hub)
        html = "Feature not yet implemented"
        return html

class lightdemo(): # TODO make this aware of local or remote module

    def get(self, data, hub):
        """Runs a remote light set demo"""
        driver = lights_driver(hub)
        html = dumps(driver.remote_set_light_demo())
        return html

class light_on():

    def put(self, data, lightid, hub):
        """Turns on a light"""
        print("Received API call - turn on lightid {}".format(lightid))
        driver = lights_driver(hub)
        html = dumps(driver.set_light(int(lightid), 255))
        return html

class light_off():

    def put(self, data, lightid, hub):
        """Turns off a light"""
        print("Received API call - turn off lightid {}".format(lightid))
        driver = lights_driver(hub)
        html = dumps(driver.set_light(int(lightid), 0))
        return html
    
class light_brightness():

    def put(self, data, lightid, hub):
        """Sets a light brightness"""
        brightness = int(data["brightness"])
        print("Received API call set brightness - lightid {} - brightness {}".format(lightid, brightness))
        driver = lights_driver(hub)
        html = dumps(driver.set_light(int(lightid), brightness))
        return html
    
class get_groups():

    def get(self, data, hub):
        """Gets the group config from the remote lights module"""
        print("Received API call - get groups")
        driver = lights_driver(hub)
        html = dumps(driver.get_groups())
        return html
    
class list_groups():

    def get(self, data, hub):
        """Gets the group config stored in the hub"""
        print("Received API call - list groups")
        lights = hub.get_lights()
        html = dumps(lights.list_groups())
        return html

class group_on():

    def put(self, data, groupid, hub):
        """Turns on a group"""
        print("Received API call - turn on groupid {}".format(groupid))
        driver = lights_driver(hub)
        html = dumps(driver.set_group(int(groupid), 255))
        return html

class group_off():

    def put(self, data, groupid, hub):
        """Turns off a group"""
        print("Received API call - turn off groupid {}".format(groupid))
        driver = lights_driver(hub)
        html = dumps(driver.set_group(int(groupid), 0))
        return html

class group_brightness():

    def put(self, data, groupid, hub):
        """Sets a group brightness"""
        brightness = int(data["brightness"])
        print("Received API call set group brightness - groupid {} - brightness {}".format(groupid, brightness))
        driver = lights_driver(hub)
        html = dumps(driver.set_group(int(groupid), brightness))
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