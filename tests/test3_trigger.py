from pymycobot.mycobot import MyCobot
from interaction import select_com, select_robot_model
import time
import platform

robot_model = select_robot_model()
com = select_com()

system_info = platform.uname()
baud = 115200
if (
    robot_model == MyCobot
    and system_info.system == "Linux"
    and "arm" in system_info.machine
):
    baud = 1000000

robot = robot_model(com, baud)

robot.send_angles([0, 0, 0, 0, 0, 45], 50)
time.sleep(5)

for i in range(5):
    robot.move_round()
    time.sleep(1)
