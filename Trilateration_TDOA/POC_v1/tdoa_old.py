from dataclasses import dataclass
import numpy as np

SOUND_SPEED = 343.2 # m/s
HEIGHT_SPK = 0.5 # m, height of speaker above microphone

@dataclass
class Position:
    x: float
    y: float
    z: float

    def to_array(self):
        return np.array([self.x, self.y, self.z])
    
class Station():
    def __init__(self, pos:Position) -> None:
        self.pos = pos
    
    def get_toa(self, target:Position) -> float:
        distance = ((self.pos.x - target.x)**2 + (self.pos.y - target.y)**2 + (HEIGHT_SPK)**2)**0.5
        return distance / SOUND_SPEED
    
    def gen_ghost_station(self, station, dist: float): #-> (Station, float)
        #generate station at same z-height from microphone, in order to have at least 4 stations for tdoa calc
        new_station = Station(Position(station.pos.x, station.pos.y, 0.0))

        #calculate distance from new station to target using pythagoras
        new_dist = (dist**2 - HEIGHT_SPK**2)**0.5
        return (new_station, new_dist) 



#made with love from chat GPT except matrix
def trilateration_3d_tdoa(beacon_positions, tdoa):
    # beacon_positions: List of 3D positions of the beacons [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)]
    # tdoa: List of TDOA values between the beacons [tdoa_12, tdoa_13, tdoa_14]

    # Check if the number of beacons and TDOA values are valid
    num_beacons = len(beacon_positions)
    #if num_beacons < 4 or len(tdoa) < 3:
    #    raise ValueError("This trilateration algorithm requires >= four beacons and >= three TDOA values.")

    # Create an empty matrix to hold the equations
    A = np.zeros((num_beacons - 1, 4))

    # Create an empty vector to hold the known TDOA values
    b = np.zeros((num_beacons - 1, 1))

    # Iterate over the beacons (except the first one)
    # matrix from https://math.stackexchange.com/questions/1722021/trilateration-using-tdoa

    for i in range(1, num_beacons):
        delta_position = np.array([beacon_positions[0][0], beacon_positions[0][1], -0.5]) - np.array([beacon_positions[i][0], beacon_positions[i][1], -0.5])
        A[i - 1, :-1] = 2 * delta_position
        A[i - 1, -1] = 2 * SOUND_SPEED * tdoa[i - 1]

        b[i - 1] = np.sum(np.square(np.array([beacon_positions[0][0], beacon_positions[0][1], -0.5]))) \
            - np.sum(np.square(np.array([beacon_positions[i][0], beacon_positions[i][1], -0.5]))) \
            + np.square(SOUND_SPEED * tdoa[i - 1])
        
    # Solve the system of equations using least squares
    result, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    # Calculate the 3D position of the mobile object
    x = beacon_positions[0][0] + result[0][0]
    y = beacon_positions[0][1] + result[1][0]
    z = beacon_positions[0][2] + result[2][0]

    return x, y, z


if __name__ == "__main__":
    station1 = Station(Position(0, 0, HEIGHT_SPK))
    station2 = Station(Position(1.5, 2.0, HEIGHT_SPK))
    station3 = Station(Position(3.0, 0, HEIGHT_SPK))

    #fictive position : (0.5, 0.5)
    distance1 = 0.87
    distance2 = 1.87
    distance3 = 2.6

    toa1 = distance1 / SOUND_SPEED
    toa2 = distance2 / SOUND_SPEED
    toa3 = distance3 / SOUND_SPEED

    toa12 = toa2 - toa1
    toa13 = toa3 - toa1

    #"real" experiment : 
    tdoa12 = toa2 - toa1
    tdoa13 = toa3 - toa1

    print(tdoa12*SOUND_SPEED)
    #station4, distance4 = station1.gen_ghost_station(station1, distance1)
    #station5, distance5 = station2.gen_ghost_station(station2, distance2)
    #station6, distance6 = station3.gen_ghost_station(station3, distance3)



    tri = trilateration_3d_tdoa([
        station1.pos.to_array(), station2.pos.to_array(), station3.pos.to_array()],
        #station4.pos.to_array(), station5.pos.to_array(), station6.pos.to_array()], 
        [toa12, toa13])#, toa14, toa15, toa16])

    print(tri)

