#
# Comportamiento que busca un pilar de color y se aproxima a él
#

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.BlobColor import BlobColor



TARGET_COLOR = BlobColor.RED
KP = 0.2
KI = 0.02
KD = 0.1
GOAL = 50
SPEED = 7



class FindBall(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.integral = 0
        self.previous_error = 0

    #Método que define cuándo se activa el comportamiento
    def take_control(self):
        return not self.supress

    def _search_for_color(self, target_color):
        self.robot.moveTiltTo(105, 10, wait=True)
        blob = self.robot.readColorBlob(target_color)

        if blob.size > 0 and 10 < blob.posx < 90:
            print("Object detected")
            return True

        while not self.stopped() and not self.supress:
            self.robot.moveWheels(10, -10)
            self.robot.wait(0.1)
            blob = self.robot.readColorBlob(target_color)
            if blob.size > 0 and 10 < blob.posx < 90:
                print("Object detected")
                self.robot.stopMotors()
                return True

        self.robot.stopMotors()
        return False

    #Método que define qué hace el comportamiento
    def action(self):
        print("----> control: Find Ball")
        for bh in self.supress_list:
            bh.supress = True

        try:
            while not self.stopped() and not self.supress:
                if not self._search_for_color(TARGET_COLOR):
                    break

                self.robot.wait(0.1)
                blob = self.robot.readColorBlob(TARGET_COLOR)
                if blob.size == 0:
                    print("Object lost")
                    continue

                print("Blob position: ", blob.posx)

                error = blob.posx - GOAL
                self.integral += error
                self.integral = max(-100, min(100, self.integral))
                derivative = error - self.previous_error
                correction = round(
                    KP * error + KI * self.integral + KD * derivative
                )
                correction = max(-SPEED, min(SPEED, correction))

                right_speed = max(-SPEED, min(SPEED, SPEED + correction))
                left_speed = max(-SPEED, min(SPEED, SPEED - correction))
                print("Left speed: ", left_speed, " | Right speed: ", right_speed)
                print("Error: ", error, " | Integral: ", self.integral,
                      " | Derivative: ", derivative, " | Correction: ", correction)
                self.previous_error = error
                self.robot.moveWheels(left_speed, right_speed)

                if blob.posy > 90:
                    print("Object reached")
                    self.set_stop()
                    break
        finally:
            self.robot.stopMotors()
            for bh in self.supress_list:
                bh.supress = False

         
