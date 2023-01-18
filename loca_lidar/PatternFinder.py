from math import isclose
from functools import cache
import numpy as np
import CloudPoints as CPts
import FixedPoints as FPts

class PatternFinder:
    def __init__(self, dist_pts_reference, error_margin): #DistPts, float
        self.dist_pts_reference = dist_pts_reference
        self.error_margin = error_margin
        self._generate_candidate_table_cache()
        self.table_pivot_dist = {pivot_index: CPts.get_distances_from_pivot(pivot_index) for pivot_index in range(self.dist_pts_reference.shape[0])}
        #example dictionnary {0: ((0, 1, 0.3242), (0, 2, 0.231)), ...}
        pass 

    def find_pattern(self, dist_pts_lidar):
        #return dict lidar_to_table association
        #calculate all amalgame distances squared and find if any distance match the ones in self.distances
        #perform a search to find possible matching distances (if nothing found, it's not a corners fixed known of the map)
        for detected_DistPts in dist_pts_lidar:
            #TODO : convert to binary search ?
            for candidate_table_point in self._get_candidates_table_point(detected_DistPts[2]):
                #Test candidate_table_point - finding at least another distance of candidate/Beacon :
                table_dists = self.table_pivot_dist[candidate_table_point]
                dists_from_pivot = CPts.get_distances_from_pivot(detected_DistPts[0], dist_pts_lidar)
                matching_dists = np.where(np.isclose(table_dists['squared_dist'], dists_from_pivot['squared_dist'], rtol=self.error_margin))
                #generate an array where the distance pivot_point/amalgame is close enough to pivot_table/other_beacon
                # 4. Deduce and return correspondance lidar_point_name -> table_point_name (or none if not found)
                pass
                """
                for couple_fixed_pts in self.distances:  #couple de points
                    #if found a match
                    if cur_dist > couple_fixed_pts.squared_distance - self.error_margin and \
                    cur_dist < couple_fixed_pts.squared_distance + self.error_margin: 
                        known_fixed_pts = self._pivot_search(amalgame_list, amalgame, other_amalgame, couple_fixed_pts)
                        if len(known_fixed_pts) >= 2:
                            return known_fixed_pts
                """
        return None #no pattern found


    @cache
    def _get_candidates_table_point(self, squared_dist)->tuple:
        #returns tuple of possible points in known_points from table reference for a certain squared_dist
        #Example : If distance is close to 2.5 m, it returns possible points (0, 1, 2)/(A,B,C)
        candidates = []
        for table_ref in self.dist_pts_reference:
            if isclose(table_ref[2], squared_dist, rel_tol=self.error_margin):
                if table_ref[0] not in candidates:
                    candidates.append(table_ref[0])
                if table_ref[1] not in candidates:
                    candidates.append(table_ref[1])
        return tuple(candidates)

    def _generate_candidate_table_cache(self):
        for squared_dist in self.dist_pts_reference['squared_dist']:
            self._get_candidates_table_point(squared_dist)

class Triangulate(): 
    def __init__(self, known_pts):
        known_pts = known_pts.copy()
        
    def triangulate(self, lidar_to_table, lidar_amalgames)-> tuple[float, float, float]:
        """returns average computed (x,y, angle) in meters, meters, radians

        Args:
            self (_type_): _description_
            lidar_to_table (dict {int:int}): _description_
            lidar_amalgames (np.ndarray of ndtype PolarPoints): _description_
        """
        computed_pose = [] #(x, y, angle)
        for lidar_index in lidar_to_table.keys():
            #calculate relative position of robot according to the current lidar/table_beacon association
            dist_lidar_cur_amalg = lidar_amalgames[lidar_index][0]
            angle_lidar_cur_amalg = lidar_amalgames[lidar_index][1]
            #TODO : Calculer position relative du robot par rapport à l'origine
            computed_pose.append(())

        #average those values
        mean_x = np.average([pose[0] for pose in computed_pose])
        mean_y = np.average([pose[1] for pose in computed_pose])
        mean_angle = np.average([pose[2] for pose in computed_pose])
        return (mean_x, mean_y, mean_angle)

if __name__ == "__main__":
    finder = PatternFinder(FPts.known_distances(), 0.02)
    finder.find_pattern(CPts.get_distances())