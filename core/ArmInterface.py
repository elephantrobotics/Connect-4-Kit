import time
from pymycobot import MyCobot
from typing import *


class ArmInterface:
    def __init__(self, port: str, baudrate: int):
        self.ARM_SPEED = 60
        self.ARM_SPEED_PRECISE = 10

        self.angle_table = {
            "recovery": [0, 0, 0, 0, 0, 45],
            "observe": [-53.78, 116.98, -117.86, -29.35, 52.38, 20.03],
        }

        self.chess_table = [None for _ in range(7)]
        self.chess_table[6] = [-23.37, -42.89, -64.33, 107.05, 29.35, 46.66]
        self.chess_table[5] = [-11.77, -30.84, -85.78, 118.21, 17.84, 46.75]  # 需要向前一点
        self.chess_table[4] = [2.1, -20.83, -101.86, 118.65, -1.49, 46.49]
        self.chess_table[3] = [21.09, -20.03, -110.65, 132.27, -23.64, 46.75]
        self.chess_table[2] = [29.97, -8.7, -110.65, 117.7, -29.7, 52.55]
        self.chess_table[1] = [43.15, -6.67, -108.19, 101.25, -45.52, 61.17]  # 向后
        self.chess_table[0] = [54.75, -17.66, -99.93, 113.29, -57.39, 53.26]  # 向后

        # 重试次数
        self.retry = 5
        self.mc = MyCobot(port, baudrate, timeout=0.5)
        self.mc.set_fresh_mode(0)
        # self.pump_off()

    # 设置Z轴坐标
    def set_z_linear(self, val: int):
        self.mc.send_coord(3, val, self.ARM_SPEED_PRECISE)
        time.sleep(2)

    # 开启吸泵
    def pump_on(self):
        # 打开电磁阀
        time.sleep(0.05)
        self.mc.set_basic_output(5, 0)
        time.sleep(0.05)
        time.sleep(1)

    # 已经证明该方法对于解决丢指令的情况无效，但是还是先保留wrapper
    def send_angles(self, angle, speed):
        for i in range(self.retry):
            try:
                self.mc.send_angles(angle, speed)
                break
            except Exception as e:
                print(f"ERR: {e}")
                print(f"ERR: Retry {i}")

    def set_basic_output(self, val1, val2):
        for i in range(self.retry):
            try:
                self.mc.set_basic_output(val1, val2)
                break
            except Exception as e:
                print(f"ERR: {e}")
                print(f"ERR: Retry {i}")

    def send_coord(self, arm_id, coord, speed):
        for i in range(self.retry):
            try:
                self.mc.send_coord(arm_id, coord, speed)
                break
            except Exception as e:
                print(f"ERR: {e}")
                print(f"ERR: Retry {i}")

    # 停止吸泵
    def pump_off(self):
        # 关闭电磁阀
        time.sleep(0.05)
        self.set_basic_output(5, 1)
        time.sleep(0.1)
        # 泄气阀门开始工作
        self.set_basic_output(2, 0)
        time.sleep(1)
        self.set_basic_output(2, 1)
        time.sleep(0.05)
        time.sleep(1)

    # 返回到初始位置
    def recovery(self):
        self.send_angles(self.angle_table["recovery"], self.ARM_SPEED)
        time.sleep(2)

    # 移动到棋子堆上方
    def hover_over_stack(self):
        self.send_angles(self.angle_table["stack-hover-1"], self.ARM_SPEED)
        time.sleep(3)

    # 移动到棋盘格上方
    def hover_over_chessboard_n(self, n: int):
        if n is not None and 0 <= n <= 6:
            self.send_angles(self.chess_table[n], self.ARM_SPEED)
            time.sleep(2)
        else:
            self.pump_off()
            raise Exception(f"输入错误,预期棋盘输入点必须在0到6之间,实际得到{n}")

    # 移动到观察姿态
    def observe_posture(self):
        self.send_angles(self.angle_table["observe"], self.ARM_SPEED)
        time.sleep(2)

    def move(self, action: str):
        self.mc.send_angles(self.angle_table[action], self.ARM_SPEED)

    def drop_piece(self):
        self.mc.set_gservo_round()
