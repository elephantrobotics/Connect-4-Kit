from pymycobot import MyCobot
from interaction import select_com
import time

com = select_com()

robot_name = "myCobot 280 - M5"
robot_model_name = "myCobot 280"
robot = MyCobot(com, 115200)

# Test rotation range
twist = 30
# Arm move speed
speed = 50
# Arm joint number
joint_n = 6

zero_pos = [0, 0, 0, 0, 0, 0]
robot.send_angles(zero_pos, speed)
time.sleep(5)

for i in range(1, joint_n + 1):
    robot.send_angle(i, twist, speed)
    time.sleep(3)
    robot.send_angle(i, -twist, speed)
    time.sleep(3)
    robot.send_angle(i, 0, speed)
    time.sleep(3)
