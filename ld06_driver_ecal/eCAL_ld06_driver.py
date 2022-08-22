import serial
import ecal.core as ecal_core
from ecal.core.publisher import ProtoPublisher

import sys, os, time
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

#import proto.py.lidar_data_pb2 as lidar_data
import lidar_data_pb2 as lidar_data
from CalcLidarData import CalcLidarData

SERIAL_PORT = '/dev/tty.usbserial-0001'

ser = serial.Serial(port=SERIAL_PORT,
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

tmpString = ""
lines = list()
angles = list()
distances = list()

#init ecal publisher 
ecal_core.initialize(sys.argv, "eCAL_LD06_driver")

pub = ProtoPublisher("lidar_data", lidar_data.Lidar)
def publish_reading(angles, distances):
    #once the program finished to read a full circle reading from lidar, publlish it to eCAL with protobuf format
    lidar_msg = lidar_data.Lidar()
    lidar_msg.angles = angles 
    lidar_msg.distances = distances
    pub.send(lidar_msg, time.time())
    
if __name__ == '__main__':
    #read data continuously
    i = 0
    while True:
        loopFlag = True
        flag2c = False

        # collect 429 readings (complete circle)
        if(i % 40 == 39):
            publish_reading(angles, distances)
            angles.clear()
            distances.clear()
            i = 0
            

        while loopFlag:
            b = ser.read()
            tmpInt = int.from_bytes(b, 'big')
            
            if (tmpInt == 0x54): #if starting character
                tmpString +=  b.hex()+" "
                flag2c = True
                continue
            
            elif(tmpInt == 0x2c and flag2c): #reading datalength (constant -> 0x2c)
                tmpString += b.hex()

                if(not len(tmpString[0:-5].replace(' ','')) == 90 ): #?? On vérifie que la valeur fixe du datalength est correct?
                    tmpString = ""
                    loopFlag = False
                    flag2c = False
                    continue

                lidarData = CalcLidarData(tmpString[0:-5])
                angles.extend(lidarData.Angle_i)
                distances.extend(lidarData.Distance_i)
                    
                tmpString = ""
                loopFlag = False
            else:
                tmpString += b.hex()+" "
            
            flag2c = False
        
        i +=1

    ecal_core.finalize()
    ser.close()