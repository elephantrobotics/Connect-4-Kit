# @author  : Zhu ZhenDong
# @time    : 2023-06-15 01-47-29
# @function:
# @version :

from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from layouts.app_page import AppSharedMem

from configs.config import *
from core.mouse_callbacks import *


class DummyCamera:
    def __init__(self, context: AppSharedMem) -> None:
        self.context = context

    def update(self):
        pass

    def release(self):
        pass

    def get_frame(self):
        if self.context.curr_frame is not None:
            return self.context.curr_frame.copy()
        else:
            return None


class ArmCamera:
    def __init__(self, cam_index: int, flip_h=False, flip_v=False):
        self.cap = cv2.VideoCapture(cam_index)
        self.width = None
        self.height = None
        self.flip_h = flip_h
        self.flip_v = flip_v
        self.mtx = np.array(
            [
                [518.10427579, 0.0, 354.7908927],  # 内参矩阵
                [0.0, 515.09741266, 225.00161552],
                [0.0, 0.0, 1.0],
            ]
        )  # 内参矩阵
        self.dist = np.array(
            [[0.10979575, -0.3677762, -0.00080076, 0.00158036, 0.32856219]]
        )  # 畸变系数

        self.current_frame = None

        self.new_mtx = None
        self.new_dist = None

    @staticmethod
    def add_cross_aux_line(bgr_data):
        height, width = bgr_data.shape[0], bgr_data.shape[1]
        cv2.line(
            bgr_data, (int(width / 2), 0), (int(width / 2), height), BGR_GREEN, 1
        )  # 画竖线
        cv2.line(
            bgr_data, (0, int(height / 2)), (width, int(height / 2)), BGR_GREEN, 1
        )  # 画横线
        return bgr_data

    def update(self):
        ret, frame = self.cap.read()  # 读取摄像头的一帧
        if ret and self.width is None and self.height is None:
            self.width = frame.shape[0]  # 获取帧的宽度
            self.height = frame.shape[1]  # 获取帧的高度

        if ret is not None:
            if self.flip_h:
                frame = cv2.flip(frame, 1)  # 水平翻转
            if self.flip_v:
                frame = cv2.flip(frame, 0)  # 垂直翻转
            calibed_frame = cv2.undistort(frame, self.mtx, self.dist, None)  # 校正图像
            self.current_frame = calibed_frame  # 更新当前帧

    def get_frame(self):
        if self.current_frame is not None:
            return self.current_frame.copy()  # 返回当前帧的副本
        else:
            return None

    def release(self):
        self.cap.release()
