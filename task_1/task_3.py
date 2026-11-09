import random
from robobopy.Robobo import Robobo
from robobopy.utils.Emotions import Emotions
from robobopy.utils.Sounds import Sounds
from robobopy.utils.IR import IR

rob = Robobo("localhost")
rob.connect()

speed = 15
emotions_list = [
    Emotions.HAPPY,
    Emotions.LAUGHING,
    Emotions.SURPRISED,
    Emotions.SAD,
    Emotions.ANGRY,
    Emotions.NORMAL,
    Emotions.SLEEPING,
    Emotions.TIRED,
    Emotions.AFRAID
]

def on_fling():
    angle = rob.readFlingAngle()
    if 45 <= angle < 135:
        if (rob.readIRSensor(IR.FrontC) > 90 or 
            rob.readIRSensor(IR.FrontLL) > 90 or 
            rob.readIRSensor(IR.FrontRR) > 90):
            
            rob.stopMotors()
            rob.sayText("No puedo, hay algo delante")
            print("obstacle detected")
        else:
            rob.moveWheelsByTime(speed, speed, 1)
            print("FrontC:", rob.readIRSensor(IR.FrontC))
            print("FrontLL:", rob.readIRSensor(IR.FrontLL))
            print("FrontRR:", rob.readIRSensor(IR.FrontRR))

    elif 225 <= angle < 315:
        rob.moveWheelsByTime(-speed, -speed, 1)
    elif 135 <= angle < 225:
        rob.moveWheelsByTime(speed, -speed, 1)
    else:
        rob.moveWheelsByTime(-speed, speed, 1)

def on_tap():
    tap = rob.readTapSensor()
    if tap.zone == 'eye':
        rob.stopMotors()
        rob.setEmotionTo(Emotions.ANGRY)
        rob.playSound(Sounds.ANGRY)
    elif tap.zone == 'mouth':
        battery = rob.readBatteryLevel('phone')
        rob.sayText(f"Bateria al {battery} por ciento")
    elif tap.zone == 'forehead':
        rob.setEmotionTo(random.choice(emotions_list))

rob.whenAFlingIsDetected(on_fling)
rob.whenATapIsDetected(on_tap)

while True:
    rob.wait(1)