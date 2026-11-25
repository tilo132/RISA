from robobopy.Robobo import Robobo
from robobopy.utils.QRCode import QRCode





##QR CODE WILL NOT BE RECOGNIZED FROM FAR AWAY

# Use "localhost" for Robobo Sim, or the smartphone's Wi-Fi IP for the physical robot
ROBOBO_IP = "localhost"

rob = Robobo(ROBOBO_IP)
rob.connect()
rob.wait(1)
# Octave 3
c3 = 48
cs3 = db3 = 49
d3 = 50
ds3 = eb3 = 51
e3 = 52
f3 = 53
fs3 = gb3 = 54
g3 = 55
gs3 = ab3 = 56
a3 = 57
as3 = bb3 = 58
b3 = 59

# Octave 4 (Middle C = 60)
c4 = 60
cs4 = db4 = 61
d4 = 62
ds4 = eb4 = 63
e4 = 64
f4 = 65
fs4 = gb4 = 66
g4 = 67
gs4 = ab4 = 68
a4 = 69
as4 = bb4 = 70
b4 = 71

# Octave 5
c5 = 72
cs5 = db5 = 73
d5 = 74
ds5 = eb5 = 75
e5 = 76
f5 = 77
fs5 = gb5 = 78
g5 = 79
gs5 = ab5 = 80
a5 = 81
as5 = bb5 = 82
b5 = 83

# Octave 6
c6 = 84
cs6 = db6 = 85
d6 = 86
ds6 = eb6 = 87
e6 = 88
f6 = 89
fs6 = gb6 = 90
g6 = 91
gs6 = ab6 = 92
a6 = 93
as6 = bb6 = 94
b6 = 95

# Octave 7
c7 = 96

def anthem():
    half = 1.6667
    quarter = 0.8333
    eight = 0.417
    sixteenth = 0.208

    # Measure 1: Glo-ria,
    rob.playNote(f3, quarter, True)
    rob.playNote(c3, quarter, True)

    # Measure 2: Glo-ria: co-
    rob.playNote(a3, quarter, True)
    rob.playNote(f3, eight + sixteenth, True)
    rob.playNote(c4, sixteenth, True)

    # Measure 3: ro-na de la
    rob.playNote(bb3, eight + sixteenth, True)
    rob.playNote(a3, sixteenth, True)
    rob.playNote(g3, eight + sixteenth, True)
    rob.playNote(f3, sixteenth, True)

    # Measure 4: Pa-tria so-be-
    rob.playNote(f3, eight, True)
    rob.playNote(e3, eight, True)
    rob.playNote(d3, eight, True)
    rob.playNote(c3, eight, True)

    # Measure 5: ra-na
    rob.playNote(f3, quarter, True)
    rob.playNote(g3, quarter, True)

    # Measure 6: luz que es
    rob.playNote(a3, quarter + eight, True)
    rob.playNote(c4, eight, True)

    # Measure 7: o-ro en tu pen-
    rob.playNote(bb3, eight + sixteenth, True)
    rob.playNote(a3, sixteenth, True)
    rob.playNote(g3, eight + sixteenth, True)
    rob.playNote(f3, sixteenth, True)

    # Measure 8: dón. (repeat sign)
    rob.playNote(c4, half, True)

anthem()