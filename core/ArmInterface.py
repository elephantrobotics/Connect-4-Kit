import time
from pymycobot import MyCobot
from typing import *


class ArmInterface:
    def __init__(self, port: str, baudrate: int):
        # Define arm speeds
        self.ARM_SPEED = 60
        self.ARM_SPEED_PRECISE = 10

        # Define angle tables for different positions
        self.angle_table = {
            "recovery": [0, 0, 0, 0, 0, 45],
            "observe": [-53.78, 116.98, -117.86, -29.35, 52.38, 20.03],
        }

        # Define chess table for different positions
        self.chess_table = [None for _ in range(7)]
        # ... (rest of the chess_table initialization)

        # Define retry count
        self.retry = 5

        # Initialize MyCobot instance
        self.mc = MyCobot(port, baudrate, timeout=0.5)
        self.mc.set_fresh_mode(0)

    # Method to set Z-axis coordinate
    def set_z_linear(self, val: int):
        self.mc.send_coord(3, val, self.ARM_SPEED_PRECISE)
        time.sleep(2)

    # Method to turn on the pump
    def pump_on(self):
        # Open the solenoid valve
        time.sleep(0.05)
        self.mc.set_basic_output(5, 0)
        time.sleep(0.05)
        time.sleep(1)

    # Method to send angles with retry logic
    def send_angles(self, angle, speed):
        for i in range(self.retry):
            try:
                self.mc.send_angles(angle, speed)
                break
            except Exception as e:
                print(f"ERR: {e}")
                print(f"ERR: Retry {i}")

    # Method to set basic output with retry logic
    def set_basic_output(self, val1, val2):
        for i in range(self.retry):
            try:
                self.mc.set_basic_output(val1, val2)
                break
            except Exception as e:
                print(f"ERR: {e}")
                print(f"ERR: Retry {i}")

    # Method to send coordinates with retry logic
    def send_coord(self, arm_id, coord, speed):
        for i in range(self.retry):
            try:
                self.mc.send_coord(arm_id, coord, speed)
                break
            except Exception as e:
                print(f"ERR: {e}")
                print(f"ERR: Retry {i}")

    # Method to turn off the pump
    def pump_off(self):
        # Close the solenoid valve
        time.sleep(0.05)
        self.set_basic_output(5, 1)
        time.sleep(0.1)
        # Start the exhaust valve
        self.set_basic_output(2, 0)
        time.sleep(1)
        self.set_basic_output(2, 1)
        time.sleep(0.05)
        time.sleep(1)

    # Method to return to the initial position
    def recovery(self):
        self.send_angles(self.angle_table["recovery"], self.ARM_SPEED)
        time.sleep(2)

    # Method to move to the top of the chess piece stack
    def hover_over_stack(self):
        self.send_angles(self.angle_table["stack-hover-1"], self.ARM_SPEED)
        time.sleep(3)

    # Method to move to the top of the chessboard
    def hover_over_chessboard_n(self, n: int):
        if n is not None and 0 <= n <= 6:
            self.send_angles(self.chess_table[n], self.ARM_SPEED)
            time.sleep(2)
        else:
            self.pump_off()
            raise Exception(f"Input error, expected chessboard input point must be between 0 and 6, got {n}")

    # Method to move to the observation posture
    def observe_posture(self):
        self.send_angles(self.angle_table["observe"], self.ARM_SPEED)
        time.sleep(2)

    # Method to move the arm
    def move(self, action: str):
        self.mc.send_angles(self.angle_table[action], self.ARM_SPEED)

    # Method to drop the chess piece
    def drop_piece(self):
        self.mc.set_gservo_round()
