import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

import numpy as np
import matplotlib.pyplot as plt
import sys
import lidar_data_pb2 as lidar_data
import time

curScatter = None

def callback(topic_name, msg, time):
    global curScatter
    with plt.ion():
        if curScatter != None:
            curScatter.remove()
            curScatter = None
        curScatter = plt.scatter(msg.angles, msg.distances, c="pink", s=5)

ecal_core.initialize(sys.argv, "ecal_lidar_vizualisation")
sub = ProtoSubscriber('lidar_data',lidar_data.Lidar)

sub.set_callback(callback)

plt.axes(projection = 'polar')
ax = plt.gca()
ax.set_ylim([0, 20])
plt.show()


  # Just don't exit
while ecal_core.ok():
    plt.pause(0.1)


  
  # finalize eCAL API
ecal_core.finalize()

"""
        if('line' in locals()):
            line.remove()
        line = ax.scatter(angles, distances, c="pink", s=5)

        ax.set_theta_offset(math.pi / 2)
        plt.pause(0.01)
        angles.clear()
        distances.clear()
"""

 
r = 3
   
rads = np.arange(0, (2 * np.pi), 0.01)
   
# plotting the circle
for i in rads:
    plt.polar(i, r, 'g.')
   
# display the Polar plot
plt.show()