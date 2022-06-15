#!/usr/bin/python3
import time
from enum import Enum
import sys, os, math

INTERFACE = "ECAL5"

from data_types import PositionOriented, Speed, StrMsg, PositionOrientedTimed
from navigation import Navigation
from actuators import Actuators
    #import messages_pb2 as m

from ecal_launch import ecal5Interface


class Robot:
    
    class Modules(Enum):
        NAV = 0
        #ODOM_REPORT = 1
        ACTUATORS = 1

    def __init__(self, robot_name="robot_sim", pos_init=(3000-140, 1140, math.radians(180))):
        self.actuators = Actuators()
        #self.com = IvyInterface(robot_name, self.actuators, bus)
        self.nav = Navigation(pos_init)
        self.modules_period = {}
        self.modules_update = {}
        self.modules_update_time = {}
        self.register_module(Robot.Modules.NAV, 0.05, self.nav.update)
        self.register_module(Robot.Modules.ACTUATORS, 1, self.update_actuators)

        self.com = ecal5Interface(robot_name)
        self.com.start()
        self.com.register_msg_callback('cmd_vel', Speed, self.nav.set_speed)
        #self.com.register_msg_callback('position_cmd', PositionOriented, self.nav.set_pos_objective)
        #self.com.register_msg_callback('actuator_cmd', self.actuators.handle_cmd, Actuators)

        self.com.update_data_continuous("odom", PositionOrientedTimed, self.get_odom_report, 0.1)

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        if self.com.running:
            self.com.stop()
    
    def register_module(self, module, period, update):
        self.modules_period[module] = period
        self.modules_update[module] = update
        self.modules_update_time[module] = time.time()
    
    def update(self):
        for module in Robot.Modules:
            now = time.time()
            dt = now - self.modules_update_time[module]
            if dt >= self.modules_period[module]:
                self.modules_update[module](dt)
                self.modules_update_time[module] = now


    def update_actuators(self, dt):
        self.actuators.update()
        for ac in self.actuators.actuators:
            if ac.val_changed == True:
                ac.val_changed=False
                #self.com.report_actuator(ac)

    def get_odom_report(self):
        x, y, theta = self.nav.pos
        vx, vy, vz = self.nav.speed
        return PositionOrientedTimed(x,y,theta, vx, vz, time.time())

    def get_transform_report(self):
        x, y, theta = self.nav.pos
        return PositionOriented(x,y,theta)
        
    def run(self):
        while self.com:#.running :
            self.update()
            self.com.process_com()
            time.sleep(0.01)
        #self.com.stop ()


def main(args=None):
    """
    entry points for ros
    """
    robot = Robot("robot_sim")
    robot.run()

if __name__ == '__main__':
    main()
    """
    if len(sys.argv) != 2:
        print("Using default name : robot_sim")
    with Robot(sys.argv[1]) as robot:
        robot.run()
    """