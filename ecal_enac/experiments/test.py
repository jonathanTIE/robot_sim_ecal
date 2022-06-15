import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import time

import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher, ProtoPublisher
import proto.py.position_pb2 as position
#import ...proto.cmd_speed_pb2 as position
ecal_core.initialize(sys.argv, "enac - teleop speed cmd")

cmd_speed_pub = ProtoPublisher("cmd_vel", position.cmd_speed)

while ecal_core.ok():
    cmd_speed_input = input("entrez z pour avancer")
    cmd = position.cmd_speed()
    if cmd_speed_input == "z":
        cmd.x = 1.0
    elif False:
        cmd.x = 0.0
    cmd_speed_pub.send(cmd)
    print("Sending: {}".format(cmd))

  # finalize eCAL API
ecal_core.finalize()




"""
    

    import sys
import time

import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher

if __name__ == "__main__":
  # initialize eCAL API. The name of our Process will be "Python Hello World Publisher"
  ecal_core.initialize(sys.argv, "Python Hello World Publisher")

  # Create a String Publisher that publishes on the topic "hello_world_python_topic"
  pub = StringPublisher("hello_world_python_topic")
  
  # Create a counter, so something changes in our message
  counter = 0
  
  # Infinite loop (using ecal_core.ok() will enable us to gracefully shutdown
  # the process from another application)
  while ecal_core.ok():
    # Create a message with a counter an publish it to the topic
    current_message = "Hello World {:6d}".format(counter)
    print("Sending: {}".format(current_message))
    pub.send(current_message)
    
    # Sleep 500 ms
    time.sleep(0.5)
    
    counter = counter + 1
  
  # finalize eCAL API
  ecal_core.finalize()



  SUBSCRIBER

  import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

# Callback for receiving messages
def callback(topic_name, msg, time):
  print("Received: {}".format(msg))

if __name__ == "__main__":
  # Initialize eCAL
  ecal_core.initialize(sys.argv, "Python Hello World Publisher")

  # Create a subscriber that listenes on the "hello_world_python_topic"
  sub = StringSubscriber("hello_world_python_topic")

  # Set the Callback
  sub.set_callback(callback)
  
  # Just don't exit
  while ecal_core.ok():
    time.sleep(0.5)
  
  # finalize eCAL API
  ecal_core.finalize()
"""