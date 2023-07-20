import time
from pymycobot import MyCobot
from typing import *
import logging
from core.logger import get_logger

logger = get_logger(__name__, filepath="logs/robot.log")


class ArmInterface:
    def __init__(self, port: str, baudrate: int):
        # Define arm speeds
        self.ARM_SPEED = 60
        self.ARM_SPEED_PRECISE = 10
        self.port = port
        # Define angle tables for different positions
        self.angle_table = {
            "recovery": [0, 0, 0, 0, 0, 45],
            "observe": [-53.78, 116.98, -117.86, -29.35, 52.38, 20.03],
        }

        # Define chess table for different positions
        self.chess_table = [None for _ in range(7)]
        self.chess_table[6] = [-16.69, -40.25, -73.21, 104.41, 18.19, 45.43]
        self.chess_table[5] = [-8.87, -34.27, -84.46, 110.21, 10.19, 46.23]  # 需要向前一点
        self.chess_table[4] = [1.58, -27.33, -95.09, 114.43, -0.26, 47.81]
        self.chess_table[3] = [14.23, -22.58, -102.48, 116.89, -12.74, 49.21]
        self.chess_table[2] = [26.89, -21.7, -103.79, 116.98, -25.57, 50.8]
        self.chess_table[1] = [38.49, -22.76, -102.39, 115.57, -36.12, 52.47]  # 向后
        self.chess_table[0] = [48.33, -25.13, -95.88, 111.79, -46.58, 54.22]  # 向后

        # Define retry count
        self.retry = 5

        # Initialize MyCobot instance
        self.mc = MyCobot(port, baudrate, timeout=0.5, debug=True)

        # counter mycobot module contaminating the root logger
        logging.getLogger().setLevel(logging.CRITICAL)
        self.mc.log.setLevel(logging.DEBUG)
        self.mc.log.propagate = False

        # Set up log to file
        mc_file_hdlr = logging.FileHandler("logs/robot.log")
        mc_file_hdlr.setFormatter(
            logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
        )
        self.mc.log.addHandler(mc_file_hdlr)

        self.mc.set_fresh_mode(0)

    # Method to turn on the pump
    def pump_on(self):
        # Open the solenoid valve
        time.sleep(0.05)
        self.mc.set_basic_output(5, 0)
        time.sleep(0.05)
        time.sleep(1)

    # Method to send angles with retry logic
    def send_angles(self, angle, speed):
        self.mc.send_angles(angle, speed)

    # Method to set basic output with retry logic
    def set_basic_output(self, val1, val2):
        self.mc.set_basic_output(val1, val2)

    # Method to send coordinates with retry logic
    def send_coord(self, arm_id, coord, speed):
        self.mc.send_coord(arm_id, coord, speed)

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
            logger.debug(f"Move to chess position {n}, angles {self.chess_table[n]}")
            self.send_angles(self.chess_table[n], self.ARM_SPEED)
            time.sleep(2)
        else:
            self.pump_off()
            raise Exception(
                f"Input error, expected chessboard input point must be between 0 and 6, got {n}"
            )

    # Method to move to the observation posture
    def observe_posture(self):
        logger.debug(f"Move to observe position {self.angle_table['observe']}")
        self.send_angles(self.angle_table["observe"], self.ARM_SPEED)
        time.sleep(2)

    # Method to move the arm
    def move(self, action: str):
        logger.debug(f"Action move: {action} Angles {self.angle_table[action]}")
        self.mc.send_angles(self.angle_table[action], self.ARM_SPEED)

    # Method to drop the chess piece
    def drop_piece(self):
        logger.debug(f"Dropping piece at {self.mc.get_angles()}")
        self.mc.set_gservo_round(12)
