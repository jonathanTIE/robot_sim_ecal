import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

import loca_lidar.CloudPoints as cp
import PointsDataStruct as lid_struct

"""TODO
    - pour la gestion des déplacements sur la carte:
    - la stratégie(module nav) demande: qqun à cet endroit là?
    - le lidar répond: {"oui"; "non"}
"""

last_known_moving_angle = 0 #angle in degrees from where the robot is moving 
last_known_lidar = (0, 0, 0) #x, y, theta (meters, degrees)

def on_moving_angle(topic_name, proto_msg, time):
    last_known_moving_angle = proto_msg.msg

def on_lidar_scan(topic_name, proto_msg, time):
    # Obstacle avoidance
    lidar_scan = proto_msg.msg #TODO : convert to lid_struct.PolarPts_t
    basic_filtered_scan = cp.basic_filter_pts(lidar_scan)
    obstacle_consigne = cp.obstacle_in_cone(basic_filtered_scan, last_known_moving_angle)
    #TODO : publish the obstacle_consigne

    # advanced filtering
    x,y,theta = last_known_lidar[0], last_known_lidar[1], last_known_lidar[2]
    pos_filtered_scan = cp.position_filter_pts(basic_filtered_scan, x, y, theta)
    # TODO : position filter is unimplemented | it returns everything
    amalgames = cp.amalgames_from_cloud(pos_filtered_scan)
   
if __name__ == "__main__":
    ecal_core.initialize(sys.argv, "loca_lidar_ecal_interface")

    sub_angle = ProtoSubscriber("robot_moving_angle", hello_world_pb2.HelloWorld)
    sub_lidar = ProtoSubscriber("lidar_scan", hello_world_pb2.HelloWorld)

    sub_angle.set_callback(on_moving_angle)
    sub_lidar.set_callback(on_lidar_scan)

    while ecal_core.ok():
        time.sleep(0.5)

    ecal_core.finalize()
