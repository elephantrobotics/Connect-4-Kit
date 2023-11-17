# @author  : Zhu ZhenDong
# @time    : 2023-07-06 09-58-47
# @function:
# @version :

from serial.tools import list_ports
from pymycobot import MyCobot, MyArm


def get_available_serial_port():
    return list(list_ports.comports())


def select_com() -> str:
    print("Select a COM port (Enter the number):")

    while True:
        com_ports = get_available_serial_port()
        for i, port in enumerate(com_ports):
            print(f"({i}) - {port}")

        reply = input("Enter number of your select :")
        if str.isdigit(reply) and 0 <= int(reply) <= len(com_ports) - 1:
            device = com_ports[int(reply)].device
            return device

        print("Wrong number, try again.\n")


def select_robot_model():
    print("Select a robot model (Enter the number):")

    while True:
        print(f"(0) - MyCobot")
        print(f"(1) - MyArm")

        reply = input("Enter number of your select :")
        if reply == "0":
            return MyCobot
        elif reply == "1":
            return MyArm
        else:
            print("Wrong number, try again.\n")


if __name__ == "__main__":
    robot_model = select_robot_model()
    com_port = select_com()
    print()

    print(robot_model)
    print(com_port)
