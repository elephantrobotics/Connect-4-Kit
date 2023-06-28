# @author  : Zhu ZhenDong
# @time    : 2023-06-15 02-03-11
# @function:
# @version :


import time

import cv2
import numpy as np
from core.Board import Board
from configs.config import *


class ChessBoardDetector:
    """
    Class for detecting and recognizing
    """

    HSV_DIST = {
        "redA": (np.array([0, 120, 50]), np.array([3, 255, 255])),
        "redB": (np.array([176, 120, 50]), np.array([179, 255, 255])),
        "yellow": (np.array([15, 100, 150]), np.array([26, 255, 255])),
    }

    default_hough_params = {
        "method": cv2.HOUGH_GRADIENT_ALT,
        "dp": 1.5,
        "minDist": 20,
        "param2": 0.6,
        "minRadius": 15,
        "maxRadius": 40,
    }

    def __init__(self, mtx, dist):
        # Image grid
        self.bgr_data_grid = [[None for j in range(6)] for i in range(7)]
        # Logical grid - stable
        self.stable_board = Board()
        self.stable_grid = self.stable_board.grid
        # Logical grid - watch (status may be unstable)
        self.watch_board = Board()
        self.watch_grid = self.watch_board.grid

        # Last time the watch grid changed
        self.grid_change_timestamp = time.time()

        # Watch grid has changed
        # Producer-consumer model variable
        self.__watch_grid_changed_flag = False

        # Whether the stable grid is updated
        # Producer-consumer model variable
        self.__stable_grid_changed_flag = False

        # Grid stability time threshold
        self.stable_thresh = 1

        # Camera internal parameters
        self.mtx = mtx
        self.dist = dist

    def is_grid_changed(self):
        """
        Interface exposed to the outside, set the update flag to False after consuming
        :return:
        """
        if self.__stable_grid_changed_flag:
            self.__stable_grid_changed_flag = False
            return True
        else:
            return False

    def detect_board_corners(self, bgr_data):
        """
        Recognize the QR code in the corner of the chessboard
        :param bgr_data: bgr format video frame
        :return: Four corner coordinates arranged in spatial order
        """
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)

        corners, ids, rejectedCandidates = detector.detectMarkers(bgr_data)
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, 0.05, self.mtx, self.dist
        )

        if rvec is None or len(corners) != 4:
            return None

        # Sort the recognized QR code corners as top left, top right, bottom left, bottom right
        corners = np.mean(corners, axis=2)
        corners = (np.ceil(corners)).astype(int)
        corners = corners.reshape((4, 2))
        cx, cy = (np.mean(corners[:, 0]), np.mean(corners[:, 1]))
        res: list = [None for _ in range(4)]
        for x, y in corners:
            if x < cx and y < cy:
                res[0] = (x, y)
            elif x > cx and y < cy:
                res[1] = (x, y)
            elif x < cx and y > cy:
                res[2] = (x, y)
            else:
                res[3] = (x, y)
        res = np.array(res)

        ## debug code
        if DEBUG:
            debug_img = bgr_data.copy()
            for p in res:
                cv2.circle(debug_img, p, 3, BGR_GREEN, -1)
            cv2.imshow("aruco", debug_img)

        return res

    def visu_aruco_detect(self, bgr_data, rvec, tvec, corners):
        debug_img = bgr_data.copy()
        for i in range(rvec.shape[0]):
            # Draw axis
            cv2.drawFrameAxes(
                debug_img,
                self.mtx,
                self.dist,
                rvec[
                    i,
                    :,
                    :,
                ],
                tvec[
                    i,
                    :,
                    :,
                ],
                0.03,
            )
            # Draw a square around the marker
            cv2.aruco.drawDetectedMarkers(debug_img, corners)
        return debug_img

    def rectify_frame(self, bgr_data):
        """
        Correct the camera view
        :param bgr_data:
        :return: Returns the corrected BGR frame
        """
        frame = bgr_data.copy()
        corners = self.detect_board_corners(frame)
        if corners is None:
            return None

        # Coordinate order [x,y]
        pts1: np.ndarray = np.float32(corners)

        # Fine-tune the coordinates
        pts1[0] = pts1[0][0] - 13, pts1[0][1] + 13
        pts1[1] = pts1[1][0] + 13, pts1[1][1] + 13
        pts1[2] = pts1[2][0] - 10, pts1[2][1] - 10
        pts1[3] = pts1[3][0] + 10, pts1[3][1] - 10

        pts2: np.ndarray = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        res = cv2.warpPerspective(frame, M, (frame.shape[1], frame.shape[0]))
        if DEBUG:
            debug_img = frame
            for x, y in pts1:
                cv2.circle(debug_img, (int(x), int(y)), 3, BGR_RED, -1)
            for x, y in pts2:
                cv2.circle(debug_img, (int(x), int(y)), 3, BGR_GREEN, -1)
            cv2.imshow("Rectify debug", debug_img)
        return res

    def verify_cell(self, bgr_data):
        """
        Determine the content of a cell
        :param bgr_data:
        :return: red or yellow or empty
        """
        # The matching area must be larger than this value
        factor_thresh = 0.1

        hsv_data = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)

        # Red occupies two ends in the HSV color ring, so it needs to be spliced
        redA_match = cv2.inRange(hsv_data, *self.HSV_DIST["redA"])
        redB_match = cv2.inRange(hsv_data, *self.HSV_DIST["redB"])
        red_match = cv2.bitwise_or(redA_match, redB_match)

        # Calculate the ratio of the red matching area to the total area
        red_factor = np.count_nonzero(red_match) / (
            red_match.shape[0] * red_match.shape[1]
        )
        if red_factor > factor_thresh:
            return Board.P_RED

        # Same as red
        yellow_match = cv2.inRange(hsv_data, *self.HSV_DIST["yellow"])
        yellow_match = np.count_nonzero(yellow_match) / (
            yellow_match.shape[0] * yellow_match.shape[1]
        )
        if yellow_match > factor_thresh:
            return Board.P_YELLOW

        return Board.P_EMPTY

    def update_stable_grid(self):
        for x in range(self.stable_board.width):
            for y in range(self.stable_board.height):
                self.stable_grid[x][y] = self.watch_grid[x][y]

    def detect(self, bgr_data):
        """
        The main method called externally, only returns True in a stable state, otherwise it is False
        :param bgr_data:
        :return: bool
        """

        # Correct the image based on QR code information
        rect_frame = self.rectify_frame(bgr_data)
        if rect_frame is None:
            return False

        # Cut the image to the image grid
        height, width = rect_frame.shape[:2]
        height_interval = int(height / 6)
        width_interval = int(width / 7)

        for i in range(7):
            for j in range(6):
                w1, w2 = (width_interval * i, width_interval * (i + 1))
                h1, h2 = (height_interval * j, height_interval * (j + 1))
                cell = rect_frame[h1:h2, w1:w2]
                self.bgr_data_grid[i][j] = cell

        # Detect the image grid and update the logical grid (unstable grid)
        is_grid_changed = False
        for i in range(7):
            for j in range(6):
                new_val = self.verify_cell(self.bgr_data_grid[i][j])
                if new_val != self.watch_grid[i][j]:
                    is_grid_changed = True
                self.watch_grid[i][j] = self.verify_cell(self.bgr_data_grid[i][j])

        # If the watch grid update is detected, record this time
        if is_grid_changed:
            self.__watch_grid_changed_flag = True
            self.grid_change_timestamp = time.time()

        # Has the time since the last grid update exceeded the stability threshold?
        if time.time() - self.grid_change_timestamp > self.stable_thresh:
            # Is the watch grid flag true?
            if self.__watch_grid_changed_flag:
                self.update_stable_grid()
                self.__stable_grid_changed_flag = True

            # Already in a stable state
            self.__watch_grid_changed_flag = False
            return True

        self.visu_chessboard(rect_frame)
        return False

    def debug_display_chess_console(self):
        """
        Output in text form
        :return:
        """
        for y in range(6):
            for x in range(7):
                cell = self.stable_grid[x][y]
                if cell == Board.P_RED:
                    print(Board.DISPLAY_R, end="")
                elif cell == Board.P_YELLOW:
                    print(Board.DISPLAY_Y, end="")
                else:
                    print(Board.DISPLAY_EMPTY, end="")
            print()
        print()

    def visu_chessboard(self, rect_bgr):
        """
        Modify rect_bgr, print the text on it for display
        :param rect_bgr:
        :return:
        """
        if self.watch_grid[0][0] is None:
            return

        height, width = rect_bgr.shape[:2]
        height_interval = int(height / 6)
        width_interval = int(width / 7)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 2
        offset = 20
        debug_img = rect_bgr.copy()
        for y in range(6):
            for x in range(7):
                cell = self.watch_grid[x][y]
                if cell == Board.P_RED:
                    cv2.putText(
                        debug_img,
                        Board.DISPLAY_R,
                        (x * width_interval + offset, (y + 1) * height_interval),
                        font,
                        font_size,
                        BGR_GREEN,
                        1,
                        cv2.LINE_AA,
                    )
                elif cell == Board.P_YELLOW:
                    cv2.putText(
                        debug_img,
                        Board.DISPLAY_Y,
                        (x * width_interval + offset, (y + 1) * height_interval),
                        font,
                        font_size,
                        BGR_GREEN,
                        1,
                        cv2.LINE_AA,
                    )
                else:
                    cv2.putText(
                        debug_img,
                        Board.DISPLAY_EMPTY,
                        (x * width_interval + offset, (y + 1) * height_interval),
                        font,
                        font_size,
                        BGR_GREEN,
                        1,
                        cv2.LINE_AA,
                    )

        return debug_img

    def get_grid_status(self):
        """
        External interface to get stable grid
        :return:
        """
        return self.stable_grid

    @classmethod
    def debug_grid_view(cls, bgr_data):
        """
        Grid view, for debug purposes
        :param bgr_data:
        :return:
        """
        height, width = bgr_data.shape[:2]
        height_interval = int(height / 6)
        width_interval = int(width / 7)

        for i in range(7 + 1):
            pt1 = (width_interval * i, 0)
            pt2 = (width_interval * i, height)
            cv2.line(bgr_data, pt1, pt2, BGR_GREEN, 2)

        for i in range(7 + 1):
            pt1 = (0, height_interval * i)
            pt2 = (width, height_interval * i)
            cv2.line(bgr_data, pt1, pt2, BGR_GREEN, 2)
