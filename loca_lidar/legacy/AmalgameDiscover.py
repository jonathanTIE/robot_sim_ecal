import lidar_data_pb2 as lidar_data
from Point import Point
from Amalgame import Amalgame

#Class that manages the discovery phases of amalgames from raw lidar protobuf message
class AmalgameDiscover:
    def __init__(self, amalg_min_dist = 0.1, amalg_min_size = 0.08, amalg_max_size = 0.15, amalg_max_nb_pts = 50):
        """_summary_

        Args:
            amalg_min_dist (float, optional): In meters. Defaults to 0.1.
            amalg_min_size (float, optional): In meters. Defaults to 0.08.
            amalg_max_size (float, optional): In meters. Defaults to 0.15.
            amalg_max_nb_pts (int, optional): In number of pts. Defaults to 50.
        """
        self.list_pts = None
        self.amalg_min_dist = amalg_min_dist
        self.amalg_min_size = amalg_min_size
        self.amalg_max_size = amalg_max_size
        self.amalg_max_nb_pts = amalg_max_nb_pts

    def on_msg_update(self, msg : lidar_data.Lidar)-> list(): #returns list of amalgames
        for i in msg.nb_pts:
            self.list_pts = self._msg_to_pts(msg)
        return _detect_Amalgames

    def _msg_to_pts(self, msg : lidar_data.Lidar):
        list_points = []
        for index, distance in enumerate(msg.distances):
            new_point = Point()
            new_point.distance = distance
            print("angle increment not updated in proto")
            new_point.set_angle(msg.angle_increment, index)
            new_point.set_abs_pos_robot()
            list_points.append(new_point)
        return list_points

    
    def _detect_Amalgames(self):
        # First we'll need to get the first point of the list that is a break. This will allow us to work in a fully circular way
        start_position = self.find_first_break()
        position = start_position
        list_obj = []
        points_length = len(self.list_points)
        #print("Pt depart: ", start_position)

        # Goes through all the list of points starting from the first break
        while position < points_length + start_position:
            list_pt_ama = []
            #print("BFEAK ! at position ", position)
            c = True
            while c:
                if self.is_break(position):
                    #print("Not a break")
                    c = False
                if position > points_length + start_position:
                    # print("overshoot")
                    c = False
                list_pt_ama.append(
                    self.list_points[position % points_length])
                position += 1
            new_ama = Amalgame(list_pt_ama)
            #print("New amalgame", new_ama.size)
            if new_ama.relative_center.distance > Amalgames_min_dist and new_ama.size < Amalgame_max_size and len(list_pt_ama) < Amalgame_max_nb_pts and new_ama.size > Amalgame_min_size :
                #print("Amalgame is fair")
                list_obj.append(new_ama)
        return list_obj

    # Returns the first point in the list that is a break
    # If not break is found, will return position 0

    def find_first_break(self):
        for index, point in enumerate(self.list_points):
            if self.is_break(index):
                return index

        return 0

    # gets last point before a break, returns true if this point is the last one before a break
    def is_break(self, pos_first):
        # The break calculation hasd been simplified from a previous complex calculation.
        # Given the small angle between 2 points (less than 1 degree) we can assume that points
        # are aligned and thus calculate only the difference in distance between 2 points

        distance = abs(self.list_points[pos_first % self.points_length].distance -
                       self.list_points[(pos_first+1) % self.points_length].distance)

        if distance > self.amalg_min_dist:
            return True
        else:
            return False
