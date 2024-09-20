from config import GPIO 
    
class Motor:
    def __init__(self, pinControl):
        self.pinControl = pinControl
        GPIO.setup(self.pinControl, GPIO.OUT)
        self.delay = 0.01
        
    def stop(self):
        """ Default stop method to be overridden by subclasses. """
        pass
    
    @property    
    def delay(self, delay=0.01):
        self.delay = delay