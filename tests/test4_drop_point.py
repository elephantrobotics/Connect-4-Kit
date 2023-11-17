import sys
import os
from tkinter import NO

sys.path.append(os.getcwd())

import time
from interaction import select_com, select_robot_model
import platform
from pymycobot import MyCobot, MyArm
from core.ArmInterface import _MyCobot, _MyArm

robot_model = select_robot_model()
serial_port = select_com()

robot = None
if robot_model == MyCobot:
    robot = _MyCobot(serial_port)
elif robot_model == MyArm:
    robot = _MyArm(serial_port)

robot.mc.send_angles(robot.angle_table["recovery"], 50)
time.sleep(3)

for pos in robot.chess_table:
    robot.mc.send_angles(pos, robot.ARM_SPEED)
    time.sleep(5)
    # robot.mc.move_round()
    # time.sleep(1)
