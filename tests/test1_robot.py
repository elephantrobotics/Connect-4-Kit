from pymycobot import MyCobot, MyArm
from tests.utils import select_com, select_robot_model
import time
import platform
import os
import sys
sys.path.append(os.getcwd())

from core.utils import SystemIdentity

robot_model = select_robot_model()

if SystemIdentity.is_jetson_nano():
    com = "/dev/ttyTHS1"
else:
    com = select_com()

baud = 115200

# for raspi and jetson nano
if (
    robot_model == MyCobot
    and (SystemIdentity.is_jetson_nano() or SystemIdentity.is_raspi())
):
    baud = 1000000

robot = robot_model(com, baud)

# Test rotation range
twist = 30
# Arm move speed
speed = 50

if robot_model == MyCobot:
    zero_pos = [0, 0, 0, 0, 0, 0]
    joint_n = 6
elif robot_model == MyArm:
    zero_pos = [0] * 7
    joint_n = 7
    
robot.send_angles(zero_pos, speed)
time.sleep(5)

for i in range(1, joint_n + 1):
    robot.send_angle(i, twist, speed)
    time.sleep(3)
    robot.send_angle(i, -twist, speed)
    time.sleep(3)
    robot.send_angle(i, 0, speed)
    time.sleep(3)

robot.send_angles(zero_pos, speed)