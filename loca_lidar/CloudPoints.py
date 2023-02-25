from typing import Tuple
from functools import cache, lru_cache
from itertools import combinations
from math import cos, radians
import numpy as np
from PointsDataStruct import DistPts

amalgame_sample_1 = (#TODO : convert to input from eCAL
    (1.57, 125.67),  #EN DEGREE POUR L'INSTANT
    (1.59, 237.94), 
    (1.68, 310.59), #CAREFUL : USE DEGREES ANGLE POSTIVE ONLY
    (1.62, 337.7),
    (1.57, 350.22)
)

#https://math.stackexchange.com/questions/1506706/how-to-calculate-the-distance-between-two-points-with-polar-coordinates
def get_squared_dist_polar(pt1, pt2):
    r1 = pt1[0]
    r2 = pt2[0]
    theta1 = pt1[1]
    theta2 = pt2[1]
    return r1**2 + r2**2 - 2 * r1 * r2 * cos(radians(theta2 - theta1))

#calculate and return the distances between all amalgames in format ((amalgame1, amalgame2, distance), ...)
@lru_cache(100)
def get_distances(amalgames: Tuple[Tuple[float, float], ]) -> Tuple[Tuple[int, int, float]]:
    distances = np.array((-1, -1, -1), dtype=DistPts)
    for point_combination in combinations(enumerate(amalgames), 2): 
        pt1_name = point_combination[0][0]
        pt1 = point_combination[0][1]
        pt2_name = point_combination[1][0]
        pt2 = point_combination[1][1]
        distances = np.append(distances, np.array((pt1_name, pt2_name, get_squared_dist_polar(pt1, pt2)), dtype=DistPts))
        #print(str(pt1_name) + " " +str(pt2_name)+ " " + str(get_squared_dist_polar(pt1, pt2)))

    distances = distances [1:] #Removes the None
    print(distances)
    return distances

def get_distances_from_pivot(pt_index: np.int64, pt_distances: np.ndarray):
    #return all sqred_distances from the pt given by pt_index 
    #returns format : ((pt_index, other point, squared_dist)) of type DistPts
    
    a = np.where(pt_distances['pt1'] == pt_index)
    b = np.where(pt_distances['pt2'] == pt_index)
    distances_of_pivot = np.take(pt_distances,  np.unique(np.append(a, b)))  #np.unique(...) -> np.ndarray which contains all index of distances that contain at least pt_index
    
    for i in range(len(distances_of_pivot)): #'sort' the array, so that the order is for each element always (pt_index, other_pt, dist) and not (other_pt, pt_index, dist)
        if distances_of_pivot[i][0] != pt_index:
            distances_of_pivot[i] = (distances_of_pivot[i][1], distances_of_pivot[i][0], distances_of_pivot[i][2])
    return distances_of_pivot

    
    

if __name__ == '__main__':
    get_distances(amalgame_sample_1)
    #print(get_distances_from_pivot(1, get_distances()))
