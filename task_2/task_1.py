import sys
import numpy as np
from robobopy.Robobo import Robobo
from robobopy.utils.Wheels import Wheels
from robobopy.utils.LED import LED
from robobopy.utils.IR import IR
from robobopy.utils.Color import Color
from robobopy.utils.Emotions import Emotions

rob = Robobo("localhost")
rob.connect()
#K_p=1 -> much overshoot
#K_p=0.1 -> slow
K_p=0.3 # good balance between fast and accurate

#to keep value in same range of -180 to 180 degrees like sensor readings
def normalize_angle(angle):
    return (angle + 180) % 360 - 180

def turn_degrees(degrees):
    print("Tap detected, turning ",degrees," degrees")
    #minus for compliant convention from task description
    current_direction = -rob.readOrientationSensor().yaw
    goal=normalize_angle(current_direction + degrees)
    error=normalize_angle(goal-current_direction)
    # correction loop with treshold of 2 degrees
    while(abs(error)>2):
        current_direction = -rob.readOrientationSensor().yaw
        error=normalize_angle(goal-current_direction)
        speed=round(K_p*error)
        # clip speed to avoid too slow or too fast movement
        # at 1 it stops moving
        speed = np.clip(speed,2,10) if speed > 0 else np.clip(speed,-10,-2)
        print("Current: ",current_direction," | Goal: ",goal," | Error: ",error," | Speed: ",speed)

        rob.moveWheels(-speed,speed)
        rob.wait(0.2)
    rob.stopMotors()
    print("Turn completed. Current direction: ",-rob.readOrientationSensor().yaw)


'''game loop with callback function for tap detection'''    
rob.whenATapIsDetected(lambda: turn_degrees(-90))
print("Waiting for tap to turn 90 degrees to left")
while True:
    
    rob.wait(0.5)

    
