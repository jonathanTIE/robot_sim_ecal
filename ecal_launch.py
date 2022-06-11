from robot_sim_enac.data_types import data_type, PositionOrientedTimed
from robot_sim_enac.interface import Interface
import sched
from time import time, sleep


import sys
import time

import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher, ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

  # Infinite loop (using ecal_core.ok() will enable us to gracefully shutdown
  # the process from another application)

def generate_pos_oriented_timed(data):
    msg = PositionOrientedTimed_pb()
    msg.x = data.x
    msg.y = data.y
    msg.theta = data.theta
    msg.vx = data.vx
    msg.vz = data.vz
    msg.stamp = data.stamp
    return msg


class ecal5Interface(Interface):
    def __init__(self, robot_name):
        ecal_core.initialize(sys.argv, f"robot_sim-{robot_name}")
        self.tasks = []
        self.schedulder =sched.scheduler(time, sleep)
        self.odom_pub = ProtoPublisher("odom")

        #TODO : publisher
    def start(self, *args):
        print("local debug started !")

    def process_com(self):
        self.schedulder.run(False)
        pass

    def stop(self):
        print("stoping sim !")
        ecal_core.finalize()


    def update_data_continuous(self, name : str, dataType: data_type, get_data_callback, rate : float):
        if type(get_data_callback()) == PositionOrientedTimed:
            pb_msg = generate_pos_oriented_timed(get_data_callback())
            self.odom_pub.send(pb_msg)
        else:
            print("error, unsupported topic for ecal (no publisher, add it to the init !)")
            print(get_data_callback())
        self.schedulder.enter(rate, 3, self.update_data_continuous, (name, dataType, get_data_callback, rate))

    def register_msg_callback(self, name: str, dataType:data_type, set_data_callback):
        sub = ProtoSubscriber(name, dataType)
        sub.set_callback(set_data_callback)