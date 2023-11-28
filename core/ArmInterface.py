import time
from pymycobot import MyCobot, MyArm
from typing import *
import logging
from core.logger import get_logger
import platform
from core.utils import SystemIdentity, Platform

logger = get_logger(__name__, filepath="logs/robot.log")


class ArmInterface:
    def __init__(self):
        # Define arm speeds
        self.ARM_SPEED = 60
        self.ARM_SPEED_PRECISE = 10

        self.init_angle_constants()

        # Define retry count
        self.retry = 5

    def set_robot_log(self):
        # counter mycobot module contaminating the root logger
        # logging.getLogger().setLevel(logging.CRITICAL)
        self.mc.log.setLevel(logging.DEBUG)
        self.mc.log.propagate = False

        # Set up log to file
        mc_file_hdlr = logging.FileHandler("logs/robot.log")
        mc_file_hdlr.setFormatter(
            logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
        )
        self.mc.log.addHandler(mc_file_hdlr)

        self.mc.set_fresh_mode(0)

    # Method to send angles with retry logic
    def send_angles(self, angle, speed):
        self.mc.send_angles(angle, speed)

    # Method to set basic output with retry logic
    def set_basic_output(self, val1, val2):
        self.mc.set_basic_output(val1, val2)

    # Method to send coordinates with retry logic
    def send_coord(self, arm_id, coord, speed):
        self.mc.send_coord(arm_id, coord, speed)

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
            coords = self.chess_table[n]
            logger.debug(f"Move to chess position {n}, angles {coords}")
            self.send_angles(coords, self.ARM_SPEED)
            time.sleep(3)
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
        self.mc.move_round()
        time.sleep(3)

    def init_angle_constants(self):
        raise NotImplementedError()


class _MyCobot(ArmInterface):
    def __init__(self, port: str):
        super().__init__()

        system_info = platform.uname()
        baud = None
                
        # raspberry pi and jetson nano
        if system_info.system == "Linux" and "arm" in system_info.machine:
            baud = 1000000
        else:
            baud = 115200

        self.mc = MyCobot(port, baud)
        if len(self.mc.get_angles()) != 6:
            raise Exception("Robot connect failed.")
        self.set_robot_log()

    def init_angle_constants(self):
        
        if SystemIdentity.curr_board_model() == Platform.JETSON_NANO:
            logger.info("Using Mycobot 280 - Jetson nano presets.")
        
        # Define angle tables for different positions
        self.angle_table = {
            "recovery": [0, 0, 0, 0, 0, 45],
            "observe": [-53.78, 116.98, -117.86, -29.35, 52.38, 20.03],
        }

        # Define chess table for different positions
        self.chess_table = [None for _ in range(7)]
        self.chess_table[6] = [-23.11, -49.92, -58.35, 96.85, 29.0, 45.08]
        self.chess_table[5] = [-13.97, -39.37, -77.6, 105.82, 19.86, 46.05]
        self.chess_table[4] = [-2.46, -32.25, -91.31, 115.4, 2.81, 48.33]
        self.chess_table[3] = [12.3, -29, -104.41, 126.65, -12.91, 49.21]
        self.chess_table[2] = [20.74, -29.79, -100.63, 127.35, -17.31, 50.44]
        self.chess_table[1] = [33.57, -23.9, -103.88, 116.63, -29.09, 56.86]
        self.chess_table[0] = [45.96, -26.45, -98.87, 111.79, -45.08, 59.76]


class _MyArm(ArmInterface):
    def __init__(self, port: str):
        super().__init__()
        self.mc = MyArm(port, 115200)
        if len(self.mc.get_angles()) != 7:
            raise Exception("Robot connect failed.")
        self.set_robot_log()

    def init_angle_constants(self):
        # Define angle tables for different positions
        self.angle_table = {
            "recovery": [0, 0, 0, 0, 0, -90, 0],
            "observe": [7, -77, 30, -86, 0, -109, 30],
        }

        # Define chess table for different positions
        self.chess_table = [None for _ in range(7)]
        self.chess_table[6] = [-47.28, 23.2, -0.52, -79.8, -79.8, 48.16, 73.91]
        self.chess_table[5] = [-39.46, 13.09, -0.52, -92.72, -73.47, 41.39, 67.76]
        self.chess_table[4] = [-29.35, 4.74, -0.43, -102.12, -64.86, 32.51, 60.11]
        self.chess_table[3] = [-14.32, -1.4, -0.35, -108.8, -44.29, 20.39, 41.66]
        self.chess_table[2] = [-2.1, -3.42, -0.52, -110.83, -8.96, 14.76, 8.61]
        self.chess_table[1] = [9.75, -2.54, -0.61, -109.95, 32.6, 17.49, -31.11]
        self.chess_table[0] = [25.57, 2.54, -0.35, -104.58, 60.82, 29.26, -57.04]
