from AmalgameDiscover import AmalgameDiscover
from PatternFinder import PatternFinder
from Point import Point

#TODO : différencier les configurations gauche ou droite
A = Point('A')
B = Point('B')
C = Point('C')
E = Point('E')
P = Point('P')
amalgame_discover = AmalgameDiscover()
pattern_finder = PatternFinder([A, B, C, E, P], 0.02) #in meters margin
if __name__ == "__main__":
    #on receiving msg :
    amalg_list = amalgame_discover.on_msg_update(msg)
    relative_fixed_pts = pattern.find_pattern(amalg_list) #fixed points known with their coordinates in relative lidar/robot space
    #TODO : passer d'un repère relatif à un repère "absolu" en triangulant
    