# LIDAR_LD06_python_loder
This code can use  Lidar's LD06 (LDS06) provided by LDROBOT from python. and It displays the acquired point cloud in real time in matplotlib.

# How to use 
## lidar_visualization_direct
1. Change SERIAL_PORT = '/dev/tty.usbserial-0001' in lidar_visualization_direct.py to your own port.

## eCAL_ld06_driver
1. Install eCAL
2. Change SERIAL_PORT = '/dev/tty.usbserial-0001'


# TODO:

1. read from serial & send data over eCAL
2. visualize data from eCAL, without directly connecting to serial
# About LD06(LDS06)
- Sales page https://www.inno-maker.com/product/lidar-ld06/
- Datasheet http://wiki.inno-maker.com/display/HOMEPAGE/LD06

# LICENSE
Please see [LICENSE](https://github.com/henjin0/LIDAR_LD06_python_loder/blob/main/LICENSE).
Forked by jonathanTIE from [henjin0](https://github.com/henjin0/LIDAR_LD06_python_loder)
+ using forks for understanding codes
