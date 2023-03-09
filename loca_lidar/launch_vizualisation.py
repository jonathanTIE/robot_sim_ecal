import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import sys
import lidar_data_pb2 as lidar_data
import time

plt.style.use('ggplot')

display_lidar = True

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
lidar_scatter = ax.scatter(0, 0)
lidar_dist = np.array([0])
lidar_theta = np.array([0])

# on_lidar_scan
def on_lidar_scan(topic_name, msg, time):
    global lidar_dist, lidar_theta
    lidar_dist = np.array(msg.distances)
    lidar_theta = np.array(msg.angles)

rax = fig.add_axes([0.005, 0.1, 0.1, 0.1])
rax.get_xaxis().set_visible(False)
rax.get_yaxis().set_visible(False)


def switch_display_lidar(event): 
    global display_lidar
    display_lidar = not display_lidar

bnext = Button(rax, 'raw_lidar', color='y')
bnext.label.set_fontsize(8)
bnext.on_clicked(switch_display_lidar)
# position_filtered_scan

# Amalgames center

# calculated beacons positions

# real_position



if __name__ == "__main__":
    

    # Init ecal Communication
    ecal_core.initialize(sys.argv, "ecal_lidar_vizualisation")
    sub_lidar = ProtoSubscriber('lidar_data',lidar_data.Lidar)

    sub_lidar.set_callback(on_lidar_scan)
    # Init matplotlib plot

    lastax = None
    plt.show(block=False)
    while ecal_core.ok():
        if lastax != None: 
            ax.cla()
            
        if display_lidar:
            lastax = ax.scatter(lidar_theta, lidar_dist, color='y')
        plt.pause(0.1)
    ecal_core.finalize()

