# @author  : Zhu ZhenDong
# @time    : 2023-07-06 10-45-08
# @function:
# @version :

import sys
import os

sys.path.append(os.getcwd())

import time
from core.ArmInterface import ArmInterface
from interaction import select_com

com = select_com()

robot = ArmInterface(com, 115200)
robot.send_angles([0, 0, 0, 0, 0, 45], 50)
time.sleep(3)

for pos in robot.chess_table:
    robot.mc.send_angles(pos, robot.ARM_SPEED)
    time.sleep(5)
    robot.mc.move_round()
    time.sleep(1)
