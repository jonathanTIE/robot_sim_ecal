from enum import Enum
from Point import Point
import math

#Theoritical shape of the regrouped points | could be used to calculate more precisely the center of the amalgame using presumed shape
class Shape(Enum):
    CLOUD = 1
    #CIRCLE = 2

class Amalgame:
    """group of 2D points that should correspond to one single object (for example, a "beacon", a robot, ...)
    """
    def __init__(self, list_points, shape = Shape.CLOUD):
        self.shape = shape
        self.list_points = list_points
        self.relative_center = self._calculate_relative_center() #TODO : disjonction de cas selon le "shape"
        self.absolute_position = []
        self.size = self.get_size_amalgame()
        #print("TAILLE", self.size)

    @classmethod
        def from_cloud_points(cls, list_points): #[(x)]

    def _calculate_relative_center(self):
        new_p = Point()
        new_p.distance = 0

        for point in self.list_points:
            new_p.distance = new_p.distance + point.distance

        new_p.distance = new_p.distance / (len(self.list_points))
        new_p.angle = self.list_points[math.floor(
            len(self.list_points)/2)].angle
        new_p.set_abs_pos_robot()

        return new_p

    def get_size_amalgame(self):
        return math.sqrt(self.list_points[0].distance**2 + self.list_points[len(self.list_points)-1].distance**2 - 2*self.list_points[0].distance*self.list_points[len(self.list_points)-1].distance*math.cos(abs(self.list_points[0].angle-self.list_points[len(self.list_points)-1].angle)))