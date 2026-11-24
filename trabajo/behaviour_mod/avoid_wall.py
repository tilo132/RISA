#
# Comportamiento que si ve una pared cerca, se para
#

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from robobopy.utils.Sounds import Sounds
from behaviour_mod.behaviour import Behaviour
from robobopy.utils.BlobColor import BlobColor
TARGET_COLOR = BlobColor.BLUE

class AvoidWall(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.side_distance = 20 #Valor de IR para que se active
        self.break_distance = 8 #Valor de IR para que pare

    #Método que define cuándo se activa el comportamiento
    def take_control(self):
        if not self.supress:
            #case diagnoal to wall
            if self.robot.readIRSensor(IR.FrontLL)>100 or self.robot.readIRSensor(IR.FrontRR)>100:
                return True
            #case parallel to wall
            if self.robot.readIRSensor(IR.FrontLL)< self.break_distance or self.robot.readIRSensor(IR.FrontRR)< self.break_distance:
                return
            #case vertical to wall
            if self.robot.readIRSensor(IR.FrontLL) >= self.side_distance and self.robot.readIRSensor(IR.FrontRR) >= self.side_distance:
                return True

    #Método que define qué hace el comportamiento
    def action(self):
        print("----> control: Avoid Wall")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        speed = 7
        self.robot.stopMotors()
        if self.robot.readIRSensor(IR.FrontLL) >= self.robot.readIRSensor(IR.FrontRR):
            #print("Turning right",self.robot.readIRSensor(IR.FrontLL),self.robot.readIRSensor(IR.FrontRR))
            self.robot.moveWheels(-speed, speed)
        else:
            #print("Turning left",self.robot.readIRSensor(IR.FrontLL),self.robot.readIRSensor(IR.FrontRR))
            self.robot.moveWheels(speed, -speed)
        self.robot.wait(2)
        for bh in self.supress_list:
            bh.supress = False

         
