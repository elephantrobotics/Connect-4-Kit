import sys
import os
import cv2
import time

sys.path.append(os.getcwd())

from core.ArmCamera import ArmCamera
from core.Detection import ChessBoardDetector
from core.logger import get_logger
from core.ArmInterface import ArmInterface
from core.Board import Board

if __name__ == "__main__":
    camera = ArmCamera(0)
    arm = ArmInterface("COM6", 115200)
    mtx, dist = camera.mtx, camera.dist
    detector = ChessBoardDetector(mtx, dist)
    logger = get_logger(__name__)
    FPS = 60
    arm.recovery()
    arm.observe_posture()
    logger.info("INFO: Arm standing-by in observation position.")
    logger.info("INFO: Starting recognition")

    detector.watch_board.drop_piece(3, Board.P_RED)
    detector.stable_board.drop_piece(3, Board.P_RED)

    # 循环读取相机帧
    while True:
        camera.update()
        frame = camera.get_frame()
        if frame is None:
            time.sleep(1 / FPS)
            continue
        rectified_frame = detector.rectify_frame(frame)
        if rectified_frame is None:
            time.sleep(1 / FPS)
            continue

        # 检测棋盘
        if detector.detect(frame):
            logger.info("Grid stabilized.")
            # break
        else:
            logger.info("Grid unstable.")
            time.sleep(1 / FPS)
            continue

        if detector.stable_board.check_board_state_valid():
            x, y = detector.stable_board.last_drop_pos
            virtual_entry = detector.stable_board.last_drop_color
            actual_entry = detector.stable_board.grid[x][y]
            if actual_entry == virtual_entry:
                logger.info("check position success")
            else:
                logger.info("check position failed")

        
        rectified_frame = detector.visu_chessboard(rectified_frame)
        cv2.imshow("frame", rectified_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()

    # agent = self.state_machine.agent
    # n = agent.plan_move(board)
    # logger.info(f"INFO: Next move {n}")
