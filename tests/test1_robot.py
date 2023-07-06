from pymycobot.mycobot import MyCobot
from interaction import select_com
from tester import Tester

com = select_com()

robot_name = "myCobot 280 - M5"
robot_model_name = "myCobot 280"
robot = MyCobot(com, 115200)

tester = Tester(robot, robot_name, robot_model_name)

tester.test_servo()
tester.test_firmware_version()
tester.test_servo_status()
tester.test_running_params()
tester.test_servo_params()

test_log = tester.get_test_log()
print(test_log)
