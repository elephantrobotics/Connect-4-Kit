from pymycobot import MyCobot, MyArm
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
