from config import GPIO 
    
class Motor:
    def __init__(self, pinControl):
        self.pinControl = pinControl
        GPIO.setup(self.pinControl, GPIO.OUT)
        
    def stop(self):
        """ Default stop method to be overridden by subclasses. """
        pass