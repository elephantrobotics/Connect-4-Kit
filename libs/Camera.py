# Importing necessary libraries
from abc import abstractmethod
import numpy as np
from typing import *
import cv2

# Defining the Camera class
class Camera:
    # Initializer / Instance Attributes
    def __init__(self, mtx=None, dist=None):
        self.mtx = mtx  # Camera matrix
        self.dist = dist  # Distortion coefficients

    # Class method to draw cross auxiliary line on the image
    @classmethod
    def draw_cross_aux_line(cls, bgr_data):
        # Getting the height and width of the image
        height, width = bgr_data.shape[0], bgr_data.shape[1]
        # Drawing a vertical line in the middle of the image
        cv2.line(bgr_data, (int(width / 2), 0), (int(width / 2), height), (0, 255, 0), 1)
        # Drawing a horizontal line in the middle of the image
        cv2.line(bgr_data, (0, int(height / 2)), (width, int(height / 2)), (0, 255, 0), 1)
        return bgr_data

    # Abstract method to get raw color frame
    @abstractmethod
    def raw_color_frame(self) -> Union[np.ndarray, None]:
        pass

    # Abstract method to get undistorted color frame
    @abstractmethod
    def undistorted_color_frame(self) -> Union[np.ndarray, None]:
        pass

    # Abstract method for undistortion
    @abstractmethod
    def undistortion(self):
        pass

    # Abstract method to release the camera
    @abstractmethod
    def release(self):
        pass
