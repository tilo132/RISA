import sys
from robobopy.utils.Wheels import Wheels
from robobopy.utils.LED import LED
from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR
from robobopy.utils.Color import Color

import numpy as np

rob = Robobo("localhost")

rob.connect()
#TODO does this have to be 360 degrees, is this even necessary, is a check for collision necessary
rob.moveWheelsByTime(20, -20, 3)
distance_L=rob.readIRSensor(IR.BackL)
distance_R=rob.readIRSensor(IR.BackR)
distance_C=rob.readIRSensor(IR.BackC)
speed =4
rob.wait(0.1)
while(True):
    rob.wait(0.2)
    distance_L=rob.readIRSensor(IR.BackL)
    distance_R=rob.readIRSensor(IR.BackR)
    distance_C=rob.readIRSensor(IR.BackC)
    rob.playNote(distance_C*0.7, 0.2)
    print (f"Distancia L: {distance_L} Distancia R: {distance_R} Distancia C: {distance_C}")
    if np.abs(distance_L-distance_R)<=1:
        rob.moveWheels(-2*speed,-2*speed)
    elif distance_L>distance_R:
        rob.moveWheels(-2*speed,-1*speed)
    elif distance_L<distance_R:
        rob.moveWheels(-1*speed,-2*speed)
    
    if distance_C> 100:
        rob.moveWheels(0,0)
        rob.setLedColorTo(LED.All, Color.RED)

        rob.sayText("Aparcado")
        break
    if distance_C > 60:
        rob.setLedColorTo(LED.All, Color.RED)
        speed=1
        continue
    if distance_C > 53 :
        rob.setLedColorTo(LED.All, Color.ORANGE)
        speed=2
        continue
    rob.setLedColorTo(LED.All, Color.GREEN)
    
rob.stopMotors()
rob.disconnect()
