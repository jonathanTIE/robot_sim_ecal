from data_types import data_type, PositionOrientedTimed, PositionOriented, Speed
from interface import Interface
import sched
from time import time, sleep


import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import proto.py.robot_state_pb2 as robot_state

import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher, ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

  # Infinite loop (using ecal_core.ok() will enable us to gracefully shutdown
  # the process from another application)

def generate_pos_oriented_timed(data):
    msg = robot_state.Odom()
    msg.position.x = data.x
    msg.position.y = data.y
    msg.position.theta = data.theta
    msg.speed.vx = data.vx
    msg.speed.vtheta = data.vz
    msg.timestamp = data.stamp
    return msg

def generate_pos_oriented(data):
    msg = robot_state.Position()
    msg.x = data.x
    msg.y = data.y
    msg.theta = data.theta
    return msg

def parse_ecal_speed(msg):
    return Speed(msg.vx, msg.vtheta)

class ecal5Interface(Interface):
    def __init__(self, robot_name):
        ecal_core.initialize(sys.argv, f"robot_sim-{robot_name}")
        self.tasks = []
        self.scheduler = sched.scheduler(time, sleep)
        self.odom_pub = ProtoPublisher("odom", robot_state.Odom)

        #TODO : publisher
    def start(self, *args):
        print("ecal started !")

    def process_com(self):
        self.scheduler.run(False)
        pass

    def stop(self):
        print("stoping sim !")
        ecal_core.finalize()


    def update_data_continuous(self, name : str, dataType: data_type, get_data_callback, rate : float):
        if type(get_data_callback()) == PositionOrientedTimed:
            pb_msg = generate_pos_oriented_timed(get_data_callback())
            self.odom_pub.send(pb_msg)
        #elif type(get_data_callback()) == PositionOriented:
        #    pb_msg = generate_pos_oriented(get_data_callback())
        else:
            print("error, unsupported topic for ecal (no publisher, add it to the init !)")
            print(get_data_callback())
        self.scheduler.enter(rate, 9, self.update_data_continuous, (name, dataType, get_data_callback, rate))

    def register_msg_callback(self, name: str, dataType:data_type, set_data_callback):
        proto_type = None
        if type(dataType) == type(Speed):
            proto_type = robot_state.Speed
            sub = ProtoSubscriber(name, proto_type)
            sub.set_callback(lambda topic, msg, stamp: set_data_callback(parse_ecal_speed(msg)))
        if proto_type == None:
            raise NotImplementedError("unsuported data_type -> protobuf !")
