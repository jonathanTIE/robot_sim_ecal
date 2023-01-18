import PointsDataStruct as pt
import numpy as np
from itertools import combinations
from functools import cache

def get_squared_dist_cartesian(pt1=(0,0), pt2= (0,0)): #x,y
    return (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2

known_points_in_mm = ( #(x,y) | Made from Eurobot2023_Rules_FR_FInale, Blue Side
    (-94, 50), #A (bottom left)     | (22+22+45+5) Bordure mur + Bordure Mur + Moitié + Moitié trou
    (2094, 1500), #B (middle right)
    (-94, 2950), #C (top left)
    (1000, 3100), #D (Center of Support de Balise | Top middle)
    (225, 3100) #E (Center of Experience | top middle left)
    ) 

@cache
def known_points():
    return tuple((x / 1000, y / 1000) for x,y in known_points_in_mm)

@cache
def known_distances():
    temp_known_distances = []
    for point_combination in combinations(enumerate(known_points()), 2): 
        #get all possible combination (unique permutation) of points : [((Index PT1, (x,y)), (Index Pt2, (x,y))), ...]
        index_pt1 = point_combination[0][0]
        pt1 = point_combination[0][1]
        index_pt2 = point_combination[1][0]
        pt2 = point_combination[1][1]
        squared_dist = get_squared_dist_cartesian(pt1, pt2) #calculate squared distance
        temp_known_distances.append((index_pt1, index_pt2, squared_dist))

    #list of all the distances possibles between the points A/0, B/1, C/2, D/3, E/4   False example : ((0, 1, 2.0), (0,2, 4.4232)
    return np.array(temp_known_distances, dtype = pt.DistPts)

if __name__ == '__main__':
    print (known_distances())
    print("distance square rooted : ")
    print([np.sqrt(pair[2]) for pair in known_distances()])