from class_config import GPIO 
    
class Motor:
    def __init__(self, pinControl):
        self.pinControl = pinControl
        GPIO.setup(self.pinControl, GPIO.OUT)
        self.delay = 0.01
        
    def stop(self):
        """ Default stop method to be overridden by subclasses. """
        pass
    
    @property    
    def Delay(self, delay=0.01)->float:
        self.delay = delay
        
    @property    
    def Delay(self)->float:
        return self.delay
    
if __name__ == "__main__":
    pass