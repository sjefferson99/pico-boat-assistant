# Development documentation and guidelines

## Architecture
```mermaid
```

## Adding a module
Dynamic importing of modules is currently beyond me. To create a new module perform the following steps.
- Copy the template_module folder and rename to your module name
- Adjust the class name in __init__.py to pba_<your_module_name>
- Add a sys path and import line to the top of hub.py similar to lights and relay
- Add an entry to the registered_modules list in config.py, increment the ID number to an unused value, use this ID in the module definition
- Copy the template code block in the hub.py section under comment "# configuration - manually add your module lines here", uncomment and adjust instances of <module_name> to init your module
- Build a whole load of code in the module template folder similar to the lights and relay module essentially replace the word "template" for your module and update/extend webpage and API definitions and build out a hardware abstraction - This only supports local modules at present