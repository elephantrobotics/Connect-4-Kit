from abc import abstractmethod
import numpy as np
from typing import *
import cv2


class Camera:
    def __init__(self, mtx=None, dist=None):
        self.mtx = mtx
        self.dist = dist

    @classmethod
    def draw_cross_aux_line(cls, bgr_data):
        height, width = bgr_data.shape[0], bgr_data.shape[1]
        cv2.line(bgr_data, (int(width / 2), 0), (int(width / 2), height), (0, 255, 0), 1)  # 画竖线
        cv2.line(bgr_data, (0, int(height / 2)), (width, int(height / 2)), (0, 255, 0), 1)  # 画横线
        return bgr_data

    @abstractmethod
    def raw_color_frame(self) -> Union[np.ndarray, None]:
        pass

    @abstractmethod
    def undistorted_color_frame(self) -> Union[np.ndarray, None]:
        pass

    @abstractmethod
    def undistortion(self):
        pass

    @abstractmethod
    def release(self):
        pass
