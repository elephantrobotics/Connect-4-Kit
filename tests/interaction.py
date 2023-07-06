# @author  : Zhu ZhenDong
# @time    : 2023-07-06 09-58-47
# @function:
# @version :

from serial.tools import list_ports


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


if __name__ == "__main__":
    print(select_com())
