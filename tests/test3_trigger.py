from pymycobot.mycobot import MyCobot
from tests.utils import select_com, select_robot_model
import time
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

for i in range(5):
    robot.move_round()
    time.sleep(1)
