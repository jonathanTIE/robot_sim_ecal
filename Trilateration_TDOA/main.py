from dataclasses import dataclass
import numpy as np
from random import random

SOUND_SPEED = 343.2 # m/s

@dataclass
class Position:
    x: float
    y: float
    z: float

    def to_array(self):
        return np.array([self.x, self.y, self.z])
    
class Station():
    def __init__(self, pos:Position, noise=0.0) -> None:
        self.pos = pos
        self.noise = 0.0
    
    def get_toa(self, target:Position) -> float:
        distance = ((self.pos.x - target.x)**2 + (self.pos.y - target.y)**2 + (self.pos.z - target.z)**2)**0.5
        return distance / SOUND_SPEED
        #TODO implement noise

#made with love from chat GPT except matrix
def trilateration_3d_tdoa(beacon_positions, tdoa):
    # beacon_positions: List of 3D positions of the beacons [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)]
    # tdoa: List of TDOA values between the beacons [tdoa_12, tdoa_13, tdoa_14]

    # Check if the number of beacons and TDOA values are valid
    num_beacons = len(beacon_positions)
    if num_beacons < 4 or len(tdoa) < 3:
        raise ValueError("This trilateration algorithm requires exactly four beacons and three TDOA values.")

    # Create an empty matrix to hold the equations
    A = np.zeros((num_beacons - 1, 4))

    # Create an empty vector to hold the known TDOA values
    b = np.zeros((num_beacons - 1, 1))

    # Iterate over the beacons (except the first one)
    # matrix from https://math.stackexchange.com/questions/1722021/trilateration-using-tdoa

    for i in range(1, num_beacons):
        delta_position = np.array(beacon_positions[0]) - np.array(beacon_positions[i])
        A[i - 1, :-1] = 2 * delta_position
        A[i -1, -1] = 2 * SOUND_SPEED * tdoa[i - 1]

        b[i - 1] = np.sum(np.square(np.array(beacon_positions[0]))) \
            - np.sum(np.square(np.array(beacon_positions[i]))) \
            + np.square(SOUND_SPEED * tdoa[i - 1])
        
    # Solve the system of equations using least squares
    result, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    # Calculate the 3D position of the mobile object
    x = beacon_positions[0][0] + result[0][0]
    y = beacon_positions[0][1] + result[1][0]
    z = beacon_positions[0][2] + result[2][0]

    return x, y, z

station1 = Station(Position(0, 0, 0.5))
station2 = Station(Position(1.5, 2.0, 0.5))
station3 = Station(Position(3.0, 0, 0.5))
station4 = Station(Position(0.0, 0.0, 0))
station5 = Station(Position(1.5, 2.0, 0.0))
station6 = Station(Position(3.0, 0.0, 0.0))

#fictive position : (0.63, 1.34)
distance1 = 0.87
distance2 = 1.87
distance3 = 2.6
distance4 = 0.71
distance5 = 1.8
distance6 = 2.55

toa1 = distance1 / SOUND_SPEED
toa2 = distance2 / SOUND_SPEED
toa3 = distance3 / SOUND_SPEED
toa4 = distance4 / SOUND_SPEED
toa5 = distance5 / SOUND_SPEED
toa6 = distance6 / SOUND_SPEED

toa12 = toa2 - toa1
toa13 = toa3 - toa1
toa14 = toa4 - toa1
toa15 = toa5 - toa1
toa16 = toa6 - toa1

tri = trilateration_3d_tdoa([
    station1.pos.to_array(), station2.pos.to_array(), station3.pos.to_array(), 
    station4.pos.to_array(), station5.pos.to_array(), station6.pos.to_array()], 
    [toa12, toa13, toa14, toa15, toa16])

print(tri)

