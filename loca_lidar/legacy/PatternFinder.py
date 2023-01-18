def calculate_dist(x1,y1,x2,y2):
    return NotImplementedError("calculate dist")

class Distance:
    def __init__(self, pt1, pt2): 
        if pt1.name == None or pt2.name == None: 
            raise NotImplementedError("unexpected point without name for distance calculation")
        self.name = pt1.name + pt2.name
        #TODO : calculer la distance
        #self.squared_distance = pt1.squared_distance + pt2.squared_distance

    def __sort__(self):
        raise NotImplementedError("sorting unimplemented for distances")

class PatternFinder:
    def __init__(self, pts_list, error_margin): 
        self.pts_list = pts_list
        self.error_margin = error_margin

        #generate the distances squared list, sorted from lowest to highest for easier computation later
        self.distances = []
        for i, pt in enumerate(self.pts_list[:-1]):
            next_pt = self.pts_list[i+1]
            cur_dist = Distance(pt, next_pt)
            self.distances.append(cur_dist)
        self.distances.sort()

    def find_pattern(self, amalgame_list):
            #calculate all amalgame distances squared and find if any distance match the ones in self.distances
            for amalgame in amalgame_list:
                for other_amalgame in amalgame_list[1:]:
                    cur_dist = calculate_dist(amalgame.relative_center, other_amalgame.relative_center)
                    #perform a search to find possible matching distances (if nothing found, it's not a corners fixed known of the map)
                    #TODO : convert to binary search ?
                    for couple_fixed_pts in self.distances:  #couple de points
                        #if found a match
                        if cur_dist > couple_fixed_pts.squared_distance - self.error_margin and \
                        cur_dist < couple_fixed_pts.squared_distance + self.error_margin: 
                            known_fixed_pts = self._pivot_search(amalgame_list, amalgame, other_amalgame, couple_fixed_pts)
                            if len(known_fixed_pts) >= 2:
                                return known_fixed_pts
            return None #no pattern found

    def _pivot_search(self, amalgame_list, amalg1, amalg2, dist_object):
        #returns known fixed points {"A": [x, y], "B":[x,y]}
        #Choses à prendre en compte pour dev la fonction : les distances, l'ordre des points
        pass