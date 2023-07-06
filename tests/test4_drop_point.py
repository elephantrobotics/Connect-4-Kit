# @author  : Zhu ZhenDong
# @time    : 2023-07-06 10-45-08
# @function:
# @version :

import sys

sys.path.append("..")
print(sys.path)

import time
from core.ArmInterface import ArmInterface
from interaction import select_com

com = select_com()

robot = ArmInterface(com, 115200)

for pos in robot.chess_table:
    robot.mc.send_angles(pos, robot.ARM_SPEED)
    time.sleep(5)
    robot.mc.set_gservo_round()
    time.sleep(1)
