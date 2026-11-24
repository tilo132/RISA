#
#  Ejemplo de uso de threads para el desarrollo de arquitecturas reactivas (subsumida)
#

from robobopy.Robobo import Robobo

from behaviour_mod.avoid_wall import AvoidWall
from behaviour_mod.find_ball import FindBall
from behaviour_mod.drive import Drive


import time

def main():
    rob = Robobo("localhost")
    rob.connect()
    rob.wait(1)

    try:
        # Diccionario que se pasará a los comportamientos
        # para que lo activen cuando se finalice la misión
        params = {"stop": False}

        # Creación de los comportamientos
        drive_behaviour = Drive(rob, [], params)

        find_ball_behaviour = FindBall(rob, [drive_behaviour], params)
        avoid_wall_behaviour = AvoidWall(rob, [find_ball_behaviour,drive_behaviour], params)

        threads = [find_ball_behaviour, avoid_wall_behaviour, drive_behaviour]

        find_ball_behaviour.start()
        avoid_wall_behaviour.start()
        drive_behaviour.start()

        while not params["stop"]:
            time.sleep(0.1)

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        params["stop"] = True
    finally:
        rob.stopMotors()
        rob.disconnect()

if __name__ == "__main__":
    main()
