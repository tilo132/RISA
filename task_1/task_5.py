from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.BlobColor import BlobColor

rob = Robobo('localhost')
rob.connect()

SIZE_REACHED = 1000
SIZE_NEAR = 50
CENTER_MIN = 35
CENTER_MAX = 65

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
    last_side = 'left'

    rob.moveTiltTo(105, 10)

    while color_detected == False:
        rob.moveWheels(10,0)
        rob.wait(0.1)
        if rob.readColorBlob(target_color).size > 0:
            print('Object detected')
            color_detected = True

    rob.stopMotors()

    while color_reached == False:
        blob = rob.readColorBlob(target_color)
        print('Blob position: ', blob.posx)
        print('Blob distance: ', blob.size)

        if blob.size == 0:
            print('Object lost')
            if last_side == 'left':
                rob.moveWheelsByTime(-10, 10, 0.1)
            else:
                rob.moveWheelsByTime(10, -10, 0.1)
            rob.wait(0.1)
        elif blob.size >= SIZE_REACHED:
            color_reached = True
            print('Object reached')
        elif blob.posx < CENTER_MIN:
            print('Object on the left')
            last_side = 'left'
            rob.moveWheelsByTime(-10, 10, 0.1)
            rob.wait(0.1)
        elif blob.posx > CENTER_MAX:
            print('Object on the right')
            last_side = 'right'
            rob.moveWheelsByTime(10, -10, 0.1)
            rob.wait(0.1)
        else:
            print('Object in the middle')
            rob.moveWheelsByTime(10, 10, 0.5)
            rob.wait(0.1)

    rob.stopMotors()

rob.whenATapIsDetected(on_tap)

while True:
    rob.wait(1)