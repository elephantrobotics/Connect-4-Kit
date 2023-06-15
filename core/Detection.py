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
    检测识别类
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
        # 图像网格
        self.bgr_data_grid = [[None for j in range(6)] for i in range(7)]
        # 逻辑网格-稳定
        self.stable_board = Board()
        self.stable_grid = self.stable_board.grid
        # 逻辑网格-观望(状态可能不稳定)
        self.watch_board = Board()
        self.watch_grid = self.watch_board.grid

        # 上一次观望网格改变的时间
        self.grid_change_timestamp = time.time()

        # 观望网格已改变
        # 生产者-消费者模型变量
        self.__watch_grid_changed_flag = False

        # 稳定网格是否更新
        # 生产者-消费者模型变量
        self.__stable_grid_changed_flag = False

        # 网格稳定时间阈值
        self.stable_thresh = 1

        # 相机内参
        self.mtx = mtx
        self.dist = dist

    def is_grid_changed(self):
        """
        暴露给外部的接口, 消费更新标志以后将标志置False
        :return:
        """
        if self.__stable_grid_changed_flag:
            self.__stable_grid_changed_flag = False
            return True
        else:
            return False

    def detect_board_corners(self, bgr_data):
        """
        识别棋盘角落的二维码
        :param bgr_data: bgr格式视频帧
        :return: 按空间顺序排列的四个角点坐标
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

        # debug
        if DEBUG:
            debug_img = bgr_data.copy()
            for i in range(rvec.shape[0]):
                # 绘制轴
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
                # 在标记周围画一个正方形
                cv2.aruco.drawDetectedMarkers(debug_img, corners)
            cv2.imshow("debug1", debug_img)

        # 给识别到的二维码角点按照 左上 右上 左下 右下排序
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

    def rectify_frame(self, bgr_data):
        """
        修正相机视图
        :param bgr_data:
        :return: 返回已经被修正的BGR帧
        """
        corners = self.detect_board_corners(bgr_data)
        if corners is None:
            return None

        # 坐标顺序 [x,y]
        pts1: np.ndarray = np.float32(corners)

        # 对坐标点进行微调
        pts1[0] = pts1[0][0] - 13, pts1[0][1] + 13
        pts1[1] = pts1[1][0] + 13, pts1[1][1] + 13
        pts1[2] = pts1[2][0] - 10, pts1[2][1] - 10
        pts1[3] = pts1[3][0] + 10, pts1[3][1] - 10

        pts2: np.ndarray = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        res = cv2.warpPerspective(bgr_data, M, (bgr_data.shape[1], bgr_data.shape[0]))
        if DEBUG:
            debug_img = bgr_data
            for x, y in pts1:
                cv2.circle(debug_img, (int(x), int(y)), 3, BGR_RED, -1)
            for x, y in pts2:
                cv2.circle(debug_img, (int(x), int(y)), 3, BGR_GREEN, -1)
            cv2.imshow("Rectify debug", debug_img)
        return res

    def verify_cell(self, bgr_data):
        """
        判断某一个格子的内容
        :param bgr_data:
        :return: red 或 yellow 或 empty
        """
        # 匹配面积要大于这个值才算
        factor_thresh = 0.1

        hsv_data = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)

        # 红色在HSV色环里面占两头位置，因此要拼接一下
        redA_match = cv2.inRange(hsv_data, *self.HSV_DIST["redA"])
        redB_match = cv2.inRange(hsv_data, *self.HSV_DIST["redB"])
        red_match = cv2.bitwise_or(redA_match, redB_match)

        # 计算红色匹配面积占总面积的比值
        red_factor = np.count_nonzero(red_match) / (
            red_match.shape[0] * red_match.shape[1]
        )
        if red_factor > factor_thresh:
            return Board.P_RED

        # 同红色
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
        外部调用的主方法,只有在稳定状态才会返回True，其他情况都是False
        :param bgr_data:
        :return: bool
        """

        # 根据二维码信息校正图像
        rect_frame = self.rectify_frame(bgr_data)
        if rect_frame is None:
            return False

        # 切割图像到图像网格
        height, width = rect_frame.shape[:2]
        height_interval = int(height / 6)
        width_interval = int(width / 7)

        for i in range(7):
            for j in range(6):
                w1, w2 = (width_interval * i, width_interval * (i + 1))
                h1, h2 = (height_interval * j, height_interval * (j + 1))
                cell = rect_frame[h1:h2, w1:w2]
                self.bgr_data_grid[i][j] = cell

        # 检测图像网格，更新逻辑网格(不稳定网格)
        is_grid_changed = False
        for i in range(7):
            for j in range(6):
                new_val = self.verify_cell(self.bgr_data_grid[i][j])
                if new_val != self.watch_grid[i][j]:
                    is_grid_changed = True
                self.watch_grid[i][j] = self.verify_cell(self.bgr_data_grid[i][j])

        # 如果检测到观望网格更新，记录一下这个时间
        if is_grid_changed:
            self.__watch_grid_changed_flag = True
            self.grid_change_timestamp = time.time()

        # 是否距离上一次网格更新的时间已经超过稳定阈值
        if time.time() - self.grid_change_timestamp > self.stable_thresh:
            # 观望网格标记是否为真
            if self.__watch_grid_changed_flag:
                self.update_stable_grid()
                self.__stable_grid_changed_flag = True

            # 已经是稳定状态
            self.__watch_grid_changed_flag = False
            return True

        self.debug_display_chess(rect_frame)
        return False

    def debug_display_chess_console(self):
        """
        用文字形式输出
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

    def debug_display_chess(self, rect_bgr):
        """
        修改rect_bgr,把文字打在上面显示
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
        cv2.imshow("Debug detect", debug_img)

    def get_grid_status(self):
        """
        外部获取稳定网格的接口
        :return:
        """
        return self.stable_grid

    @classmethod
    def debug_grid_view(cls, bgr_data):
        """
        网格视图，debug用途
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
