from typing import Tuple
from functools import cache, lru_cache
from itertools import combinations

from math import cos, radians
import numpy as np
from PointsDataStruct import PolarPts, DistPts, AmalgamePolar, AmalgameCartesian, \
    PolarPts_t, AmalgamePolar_t
import loca_lidar.config as config

amalgame_sample_1 = (#TODO : convert to input from eCAL
    (1.57, 125.67),  #EN DEGREE POUR L'INSTANT
    (1.59, 237.94), 
    (1.68, 310.59), #CAREFUL : USE DEGREES ANGLE POSTIVE ONLY
    (1.62, 337.7),
    (1.57, 350.22)
)

# function to remove incoherent points from lidar scan (to pre-filter them)
def basic_filter_pts(pts: PolarPts_t) -> PolarPts_t:
    # pt should be at least within 5 cm & 3 meters distance from lidar to be in the table
    mask = (pts['distance'] < 3.0) & (pts['distance'] > 0.05)
    return pts[mask]

def position_filter_pts(pts: PolarPts_t, lidar_x, lidar_y, lidar_theta) -> PolarPts_t:
    # TODO 1. Add additionnal check with the last known lidar position on the table
    return pts

def obstacle_in_cone(pts: PolarPts_t, angle: float) -> str:
    angle_to_check = []

    # avoiding checking negative index in pts 
    if angle >= 0 and angle <= config.cone_angle / 2:
        angle_to_check = [[0, angle], [angle - config.cone_angle + 360, 360]]
    elif angle > config.cone_angle / 2 and angle < 360 - config.cone_angle / 2:
        angle_to_check = [[angle-60, angle], [angle, angle + 60]]
    elif angle >= 360 - config.cone_angle / 2 and angle <= 360:
        angle_to_check = [[angle, 360], [0, angle + config.cone_angle - 360]]
    else: 
        raise ValueError("angle value given to obstacle_in_cone is not between 0 & 360")

    #checking corresponding angle within the range given above
    obstacles = np.where(
        ( #check valid angle
            (pts['angle'] > angle_to_check[0][0] and pts['angle'] < angle_to_check[0][1]) or
            (pts['angle'] > angle_to_check[1][0] and pts['angle'] < angle_to_check[1][1])
        ) and #check distance
        pts['distance'] < config.cone_warning_dist
    )

    # check the minimal distance from the detected obstacle in cone
    if np.argmin(obstacles) < config.cone_stop_dist:
        return "STOP"
    elif obstacles.size == 0:
        return "OK"
    else:
        return "WARNING"

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

def amalgames_from_cloud(pts: PolarPts_t) -> AmalgamePolar_t:
    """
        pts : in polar coordinates,  np.ndarray[PolarPoints]
    """
    amalgames = np.zeros((20, ), dtype=AmalgamePolar) # Hypothesis that we won't detect more than 20 valid amalgames per scan
    amalg_i, amalg_pt_count = 0, 0

    #TODO : optimize below using numpy
    for i, pt in enumerate(pts):
        #initialize first cur_pt
        if amalg_pt_count == 0: 
            amalgames[amalg_i]['list_pts'][amalg_pt_count] = pt
            amalg_pt_count += 1
            continue

        # check if point could be part of the same amalgame as pt, and add it if so
        cur_pt = amalgames[amalg_i]['list_pts'][amalg_pt_count -1] #last added point in the amalgame
        if get_squared_dist_polar(cur_pt, pt) <= config.amalgame_squared_dist_max:
            amalgames[amalg_i]['list_pts'][amalg_pt_count] = pt
            amalg_pt_count += 1
        
        # if next point is not part of the amalgame currently being discovered, finish it
        if get_squared_dist_polar(cur_pt, pt) > config.amalgame_squared_dist_max \
            or i == pts[1:].size: # this condition makes sure to finish the last amalgame if reaching the end of the pts list
            last_i = np.max(np.nonzero(amalgames[amalg_i]['list_pts']['distance']))
            # Calculate amalgame relative center 
            avg_pts_dist = amalgames[amalg_i]['list_pts']['distance'][:last_i+1].mean()
            avg_pts_angle = amalgames[amalg_i]['list_pts']['angle'][:last_i+1].mean()
            amalgames[amalg_i]['center_polar']['distance'] = avg_pts_dist
            amalgames[amalg_i]['center_polar']['angle'] = avg_pts_angle

            # Calculate amalgame size :
            first_pt, last_pt = amalgames[amalg_i]['list_pts'][0], amalgames[amalg_i]['list_pts'][last_i]
            amalgames[amalg_i]['size'] = np.sqrt(get_squared_dist_polar(first_pt, last_pt))

            #if amalgame is valid ("coherent size" ex :  not a wall, not a referee, ...)
            if amalgames[amalg_i]['size'] > 0.08 and amalgames[amalg_i]['size'] < 0.15:
                amalg_i += 1  
            # if cur_amalgame is invalid, we reset it to use it
            else: 
                amalgames[amalg_i] = np.empty((1, ))
            amalg_pt_count = 0
    return amalgames


if __name__ == '__main__':
    get_distances(amalgame_sample_1)
    
    #print(get_distances_from_pivot(1, get_distances()))
