# get front distance
# get rear distance

# if front distance > MINIMUM_GAP and rear distance > REAR_MINIMUM_GAP:
#    Reverse the car

# if front distance < MINIMUM_GAP and rear distance < REAR_MINIMUM_GAP:
#    Get the direction with most distance without considering the minimum gap
#    Move the car in that direction

#    if the distance is extremely low then check the rear distance
#       if rear distance > REAR_MINIMUM_GAP:
#          Reverse the car
#          Repeat the process

#      if rear distance < REAR_MINIMUM_GAP:
#          keep on checking the rear and the front distances while logging the data
#          if a suitable distance is found then
# move the car in that direction