# qr_arm_control
<p align="center">
  <img src="https://github.com/QuantumRoboticsURC/qr_arm_control/blob/main/InterfaceGIF.gif" alt="animated" width="90%" height="90%"/>
</p>

## Clone your repo into your catkin workspace
```
cd ~/catkin_ws/src
git clone https://github.com/QuantumRoboticsURC/qr_arm_control.git
cd ~/catkin_ws/
catkin_make
```
## General steps:

First you need to run roscore:
```
roscore
```

### Run Arm interface:
```
rosrun qr_arm_control arm_interface.py
```

### Run 2D simulation in matplotlib:
```
rosrun qr_arm_control arm_2d_simulation.py
```

### Roslaunch
```
roslaunch qr_arm_control arm_bringup.launch
```
