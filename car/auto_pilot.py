from classes import LidarSensor


class Auto_Pilot:
    def __int__(self):
        pass
    
    def find_direction(self):
        # Get the input from lida
        self.lidarSensor = LidarSensor()
        distance = self.lidarSensor.get_distance_to_obstacle()
        # if a distance is long enough

           
        
        # Move the car
        # else
        # trun the car and get the input from Lida
    
# Get all the input from
# LIDA
# Camera
# Then Move
# or Turn and Get the input again until it can move