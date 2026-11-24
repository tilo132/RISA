from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from robobopy.utils.Sounds import Sounds
from behaviour_mod.behaviour import Behaviour
from robobopy.utils.BlobColor import BlobColor
TARGET_COLOR = BlobColor.BLUE

class Drive(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        

   
    def take_control(self):
        if not self.supress:
           return True

    #Método que define qué hace el comportamiento
    def action(self):
        print("----> control: Drive")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        print(self.robot.readIRSensor(IR.FrontLL),self.robot.readIRSensor(IR.FrontC),self.robot.readIRSensor(IR.FrontRR))
        speed =7
        self.robot.moveWheels(speed,speed)
        self.robot.wait(0.2)
       

        for bh in self.supress_list:
            bh.supress = False

         
