from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.BlobColor import BlobColor

rob = Robobo('localhost')
rob.connect()

def on_tap():
    tap = rob.readTapSensor()
    if tap.zone == 'eye':
        rob.setLedColorTo(LED.All, Color.RED)
        search_for_color(BlobColor.RED)
    elif tap.zone == 'mouth':
        rob.setLedColorTo(LED.All, Color.GREEN)
        search_for_color(BlobColor.GREEN)
    elif tap.zone == 'forehead':
        rob.setLedColorTo(LED.All, Color.BLUE)
        search_for_color(BlobColor.BLUE)

def search_for_color(target_color):
    color_detected = False
    color_reached = False
    while color_detected == False:
        rob.moveWheels(10,0)
        rob.wait(0.1)
        if rob.readColorBlob(target_color).size > 0:
            print('Object detected')
            color_detected = True

    rob.stopMotors()

    while color_reached == False:
        print('Blob position: ', rob.readColorBlob(target_color).posx)
        print('Blob distance: ', rob.readColorBlob(target_color).posy)
        if 0 <= rob.readColorBlob(target_color).posx < 45 and rob.readColorBlob(target_color).posy < 100:
            print('Object on the left')
            rob.moveWheelsByTime(-10, 10, 0.1)
        elif 45 <= rob.readColorBlob(target_color).posx <= 55 and rob.readColorBlob(target_color).posy < 100:
            print('Object in the middle')
            rob.moveWheelsByTime(10, 10, 0.5) 
        elif 55 < rob.readColorBlob(target_color).posx <= 100 and rob.readColorBlob(target_color).posy < 100:
            print('Object on the right')
            rob.moveWheelsByTime(10, -10, 0.1)
        else:
            color_reached = True
            print('Object reached')
    
rob.whenATapIsDetected(on_tap)

while True:
    rob.wait(1)