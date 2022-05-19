# qr_arm_control
<p align="center">
  <img src="https://github.com/QuantumRoboticsURC/qr_arm_control/blob/main/Inteface.gif" alt="animated" width="90%" height="90%"/>
</p>

## Clone your repo into your catkin workspace
```
cd ~/catkin_ws/src
git clone https://github.com/QuantumRoboticsURC/qr_arm_control.git
cd ~/catkin_ws/
catkin_make
```
## General steps:
Change photo variable from qr_arm_control/scripts/arm_interface.py to your real path:
```
photo = ImageTk.PhotoImage(Image.open("/home/jossian/catkin_ws/src/qr_arm_control/scripts/qr_arm.png"))
```

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
