import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

import numpy as np
import matplotlib.pyplot as plt
import sys
import lidar_data_pb2 as lidar_data
import time

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(projection='polar')
lidar_scatter = ax.scatter(0, 0)

# on_lidar_scan
def on_lidar_scan(topic_name, msg, time):
    global lidar_scatter
    dist = np.array(msg.distances)
    theta = np.deg2rad(np.array(msg.angles))
    # https://stackoverflow.com/questions/9867889/matplotlib-scatterplot-removal
    lidar_scatter.remove()
    lidar_scatter = ax.scatter(theta, dist)
    # line1.set_ydata(theta)
    # line1.set_xdata(dist)
    

# position_filtered_scan

# Amalgames center

# calculated beacons positions

# real_position



curScatter = None

def callback(topic_name, msg, time):
    global curScatter
    with plt.ion():
        if curScatter != None:
            curScatter.remove()
            curScatter = None
        curScatter = plt.scatter(msg.angles, msg.distances, c="pink", s=5)


def draw(): 
    pass

def start_plot():
    plt.ion()
    

if __name__ == "__main__":
    start_plot()
    

    # Init ecal Communication
    ecal_core.initialize(sys.argv, "ecal_lidar_vizualisation")
    sub_lidar = ProtoSubscriber('lidar_data',lidar_data.Lidar)

    sub_lidar.set_callback(on_lidar_scan)
    # Init matplotlib plot

    plt.show()
    while ecal_core.ok():
        plt.pause(0.05)
"""
plt.axes(projection = 'polar')
ax = plt.gca()
ax.set_ylim([0, 20])
plt.show()


  # Just don't exit



  
  # finalize eCAL API
ecal_core.finalize()
"""
"""
        if('line' in locals()):
            line.remove()
        line = ax.scatter(angles, distances, c="pink", s=5)

        ax.set_theta_offset(math.pi / 2)
        plt.pause(0.01)
        angles.clear()
        distances.clear()
"""

"""
r = 3
   
rads = np.arange(0, (2 * np.pi), 0.01)
   
# plotting the circle
for i in rads:
    plt.polar(i, r, 'g.')
   
# display the Polar plot
plt.show()
"""