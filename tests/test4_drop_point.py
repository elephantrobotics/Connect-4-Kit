import sys
import os
from tkinter import NO
import time

sys.path.append(os.getcwd())

from core.utils import SystemIdentity
from tests.utils import select_com, select_robot_model
from pymycobot import MyCobot, MyArm
from core.ArmInterface import _MyCobot, _MyArm

robot_model = select_robot_model()
if SystemIdentity.is_jetson_nano():
    com = "/dev/ttyTHS1"
else:
    com = select_com()

robot = None
if robot_model == MyCobot:
    robot = _MyCobot(com)
elif robot_model == MyArm:
    robot = _MyArm(com)

robot.mc.send_angles(robot.angle_table["recovery"], 50)
time.sleep(3)

for pos in robot.chess_table:
    robot.mc.send_angles(pos, robot.ARM_SPEED)
    time.sleep(5)
    robot.mc.move_round()
    time.sleep(1)

robot.mc.send_angles(robot.angle_table["recovery"], 50)
time.sleep(3)