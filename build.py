import importlib
import sys
import os

# Add the root path to sys.path so packages can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define the modules you want to import and use
modules = ['car.classes.motor', 'car.classes.stepper_motor']

# Iterate through each module
for module_name in modules:
    # Import the module dynamically
    module = importlib.import_module(module_name)
    
    # Optionally call a function or class from each module
    # Assuming each module has a 'run' function for example
    if hasattr(module, 'run'):
        module.run()