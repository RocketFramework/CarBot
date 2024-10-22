import importlib
import sys
import os
# Add the root path to sys.path so packages can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from car import full_self_driving

# full_self_driving.run()
# # Define the modules you want to import and use
modules = ['telemetry.client']
# #modules = ['car.classes.lida_sensor']
# # Iterate through each module
for module_name in modules:
    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Optionally call a function or class from each module
    # Assuming each module has a 'run' function for example
    if hasattr(module, 'start_client'):
        module.start_client()