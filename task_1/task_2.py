import sys
import numpy as np
from robobopy.Robobo import Robobo
from robobopy.utils.Wheels import Wheels
from robobopy.utils.LED import LED
from robobopy.utils.IR import IR
from robobopy.utils.Color import Color
from robobopy.utils.Emotions import Emotions

rob = Robobo("localhost")
rob.connect()
#TODO head tilt, is confusing what is asked because of translation,
#TODO dont know if it is the correct face expression
turn_speed = 2
move_speed = 8
obstacle_number = 0
rob.wait(0.1)
rob.moveTiltTo(80, speed=20, wait=True)


def normalize_angle(angle):
    return (angle + 180) % 360 - 180

def turn_to_angle(rob, goal_angle, kp=0.15, ki=0.005, tolerance=3.0, dt=0.1):
    integral = 0.0
    max_integral = 15.0
    min_speed = 2
    max_speed = 10

    while True:
        rob.wait(dt)
        current_yaw = -rob.readOrientationSensor().yaw
        error = normalize_angle(goal_angle - current_yaw)
        print(f"Current: {current_yaw:.1f} | Goal: {goal_angle:.1f} | Error: {error:.1f}")

        if abs(error) <= tolerance:
            break

        if (error > 0 and integral < 0) or (error < 0 and integral > 0):
            integral = 0.0

        integral += error * dt
        integral = max(-max_integral, min(max_integral, integral))

        control_output = (kp * error) + (ki * integral)

        speed = int(round(abs(control_output)))
        if speed < min_speed:
            speed = min_speed
        elif speed > max_speed:
            speed = max_speed

        if error > 0:
            rob.moveWheels(-speed, speed)
        else:
            rob.moveWheels(speed, -speed)

    rob.stopMotors()
    rob.wait(0.2)

def turn_left(rob):
    current_direction = -rob.readOrientationSensor().yaw
    goal = normalize_angle(current_direction + 90)
    turn_to_angle(rob, goal)

def turn_right(rob):
    current_direction = -rob.readOrientationSensor().yaw
    goal = normalize_angle(current_direction - 90)
    turn_to_angle(rob, goal)

while True:
    rob.wait(0.2)
    distance_L = rob.readIRSensor(IR.FrontL)
    distance_LL = rob.readIRSensor(IR.FrontLL)
    distance_R = rob.readIRSensor(IR.FrontR)
    distance_RR = rob.readIRSensor(IR.FrontRR)
    distance_C = rob.readIRSensor(IR.FrontC)

    print(f"L: {distance_L} | LL: {distance_LL} | R: {distance_R} | RR: {distance_RR} | C: {distance_C}")

    if distance_C > 89:
        obstacle_number += 1
        tilt = rob.readTiltPosition()
        rob.moveTiltTo(50, speed=20, wait=True)
        rob.setEmotionTo(Emotions.NORMAL)
        rob.sayText(f"obstacle number {obstacle_number}")


        rob.moveWheelsByTime(-move_speed, -move_speed, 3)
        rob.wait(1)
        rob.moveTiltTo(80, speed=20, wait=True)
        rob.wait(0.5)
        if obstacle_number == 4:
            rob.sayText("Patrulla terminada")
            rob.stopMotors()
            rob.disconnect()
            break

        if distance_LL <= distance_RR:
            turn_right(rob)
        else:
            turn_left(rob)

    rob.moveWheels(move_speed, move_speed)
    rob.setEmotionTo(Emotions.HAPPY)