#
# Comportamiento de máxima prioridad para la aproximación final al pilar
#

import os
import time

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.BlobColor import BlobColor

TARGET_COLOR = BlobColor.GREEN
KP = 0.2
KI = 0.02
KD = 0.1
SPEED = 7
PURSUIT_SIZE_THRESHOLD = 120


class GoalPursuit(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.integral = 0
        self.previous_error = 0
        self.goal = None
        self.goal_pursuit=False

    def take_control(self):
        if not self.supress:
            blob = self.robot.readColorBlob(TARGET_COLOR)
            if blob.size > PURSUIT_SIZE_THRESHOLD:
                self.goal_pursuit=True
                return self.goal_pursuit
        

    def action(self):
        print("----> control: Goal Pursuit (TOP PRIORITY)")
        # Suppress all lower-priority behaviours (FindGoal, AvoidObstacles, etc.)
        for bh in self.supress_list:
            bh.supress = True

        self.integral = 0
        self.previous_error = 0
        self.goal = None

        try:
            while not self.stopped() and not self.supress:
                self.robot.wait(0.1)
                blob = self.robot.readColorBlob(TARGET_COLOR)

                if blob.size == 0:
                    print("Goal lost during pursuit")
                    break

                angle = self.robot.readOrientationSensor().yaw

                # Lock the offset target (20 or 80) once upon entering pursuit
                if self.goal is None:
                    self.goal = 20 if angle >= 0 else 80

                error = blob.posx - self.goal
                print(f"Pursuit -> Size: {blob.size} | Goal: {self.goal} | Error: {error} | Yaw: {angle}")

                # Aligned with the offset edge -> execute final drive and terminate
                if abs(error) < 5:
                    for bh in self.supress_list:
                        bh.supress = True

                    print("Start final drive:", time.time())
                    self.robot.moveWheelsByTime(7, 7, 7, wait=True)
                    print("End final drive:", time.time())

                    self.robot.stopMotors()
                    print("Goal reached - stopping program")
                    self.robot.disconnect()
                    os._exit(0)

                # PID alignment toward self.goal (20 or 80)
                self.integral += error
                self.integral = max(-100, min(100, self.integral))
                derivative = error - self.previous_error
                correction = round(
                    KP * error + KI * self.integral + KD * derivative
                )
                correction = max(-SPEED, min(SPEED, correction))

                right_speed = max(-SPEED, min(SPEED, SPEED + correction))
                left_speed = max(-SPEED, min(SPEED, SPEED - correction))

                self.previous_error = error
                self.robot.moveWheels(left_speed, right_speed)

        finally:
            self.robot.stopMotors()
            for bh in self.supress_list:
                bh.supress = False