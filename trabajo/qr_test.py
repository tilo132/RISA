from robobopy.Robobo import Robobo
from robobopy.utils.QRCode import QRCode





##QR CODE WILL NOT BE RECOGNIZED FROM FAR AWAY

# Use "localhost" for Robobo Sim, or the smartphone's Wi-Fi IP for the physical robot
ROBOBO_IP = "localhost"

rob = Robobo(ROBOBO_IP)
rob.connect()
rob.wait(1)

# Tilt the smartphone slightly downward to see QR codes on the floor/table
rob.moveTiltTo(100, 50)

# Start camera and QR code tracking
rob.wait(0.5)
rob.startQrTracking()

print("Scanning for QR codes...")

try:
    while True:
        rob.wait(0.2)

        # Read the most recently detected QR code
        qr = rob.readQR()
        print(qr)
        # If qr.id is not empty, a QR code is currently visible
        if qr and qr.id != "":
            print(f"Found QR ID: {qr.id}")
            print(f"Center (x, y): ({qr.x}, {qr.y}) | Distance: {qr.distance}")
            print(f"Corners: {qr.p1}, {qr.p2}, {qr.p3}, {qr.p4}")

            rob.stopMotors()
            rob.sayText(f"Found QR code {qr.id}")
            rob.wait(2)
        else:
            # Rotate slowly to scan the environment
            # rob.moveWheels(4, -4)
            pass

except KeyboardInterrupt:
    rob.stopMotors()

finally:
    rob.stopQrTracking()
    rob.stopCamera()
    rob.disconnect()