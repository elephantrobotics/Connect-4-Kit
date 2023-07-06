# @author  : Zhu ZhenDong
# @time    : 2023-07-06 10-42-07
# @function:
# @version :

from pymycobot.mycobot import MyCobot
from interaction import select_com

com = select_com()

robot = MyCobot(com, 115200)

robot.set_gservo_round()
