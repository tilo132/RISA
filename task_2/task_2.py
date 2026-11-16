from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.BlobColor import BlobColor
from robobopy.utils.IR import IR
import numpy as np

rob = Robobo('localhost')
rob.connect()


TARGET_COLOR=Color.RED
kp=0.2
ki=0.02
kd=0.1
integral=0
previous_error=0
goal=50
speed=7

def search_for_color(target_color):
    color_detected = False
    
    rob.moveTiltTo(105, 10)
    if rob.readColorBlob(target_color).size > 0 and rob.readColorBlob(target_color).posx > 10 and rob.readColorBlob(target_color).posx < 90:
                print('Object detected')
                color_detected = True
    while color_detected == False:
        rob.moveWheels(10,-10)
        rob.wait(0.1)
        if rob.readColorBlob(target_color).size > 0 and rob.readColorBlob(target_color).posx > 10 and rob.readColorBlob(target_color).posx < 90:
            print('Object detected')
            color_detected = True

    rob.stopMotors()
    return True
search_for_color(TARGET_COLOR)
while True:
    rob.wait(0.1)
    #search_for_color(TARGET_COLOR)
    
    blob = rob.readColorBlob(TARGET_COLOR)
    print('Blob position: ', blob.posx)
    
    error=blob.posx - 50 if rob.readColorBlob(TARGET_COLOR).size > 0 else 0
    integral += error
    integral = np.clip(integral, -100, 100)
    derivative = error - previous_error
    correction = round(kp*error + ki*integral + kd*derivative)
    correction = np.clip(correction, 0, speed) if correction > 0 else np.clip(correction, -speed, 0)
    right_speed = speed + correction
    left_speed = speed - correction
    right_speed = np.clip(right_speed, 0, speed) if right_speed > 0 else np.clip(right_speed, -speed, 0)
    left_speed = np.clip(left_speed, 0, speed) if left_speed > 0 else np.clip(left_speed, -speed, 0)
    print('Left speed: ', left_speed, ' | Right speed: ', right_speed)
    print('Error: ', error, ' | Integral: ', integral, ' | Derivative: ', derivative, ' | Correction: ', correction)
    previous_error = error
    rob.moveWheels(left_speed, right_speed)

    if blob.posy > 90:
        rob.stopMotors()
        print('Object reached')
        break    
    
    

