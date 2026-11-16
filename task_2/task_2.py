from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.BlobColor import BlobColor
from robobopy.utils.IR import IR
import numpy as np

rob = Robobo('localhost')
rob.connect()


TARGET_COLOR=Color.RED
kp=1
ki=1
kd=1
integral=0
previous_error=0
goal=50
speed=5

def search_for_color(target_color):
    color_detected = False
    

    rob.moveTiltTo(105, 10)
    if rob.readColorBlob(target_color).size > 0:
                print('Object detected')
                color_detected = True
    while color_detected == False:
        rob.moveWheels(speed,-speed)
        rob.wait(0.1)
        if rob.readColorBlob(target_color).size > 0:
            print('Object detected')
            color_detected = True

    rob.stopMotors()
    return True
while True:
    rob.wait(0.1)
    search_for_color(TARGET_COLOR)
    blob = rob.readColorBlob(TARGET_COLOR)
    print('Blob position: ', blob.posx)
    error=blob.posx - 50
    integral += error
    derivative = error - previous_error
    correction = round(kp*error + ki*integral + kd*derivative)
    correction = np.clip(correction, 0, speed) if correction > 0 else np.clip(correction, -speed, 0)
    right_speed = speed - correction
    left_speed = speed + correction
    right_speed = np.clip(right_speed, 0, speed) if right_speed > 0 else np.clip(right_speed, -speed, 0)
    left_speed = np.clip(left_speed, 0, speed) if left_speed > 0 else np.clip(left_speed, -speed, 0)
    print('Left speed: ', left_speed, ' | Right speed: ', right_speed)
    rob.moveWheels(left_speed, right_speed)
    
    
    

