from pymycobot.mycobot import MyCobot
from interaction import select_com
import time

com = select_com()

robot = MyCobot(com, 115200)
robot.send_angles([0, 0, 0, 0, 0, 45], 50)
time.sleep(5)

for i in range(5):
    robot.move_round()
    time.sleep(1)
