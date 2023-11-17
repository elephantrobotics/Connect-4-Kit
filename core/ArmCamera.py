# @author  : Zhu ZhenDong
# @time    : 2023-06-15 01-47-29
# @function:
# @version :

from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from layouts.app_page import Context

from configs.config import *
from core.mouse_callbacks import *


class DummyCamera:
    def __init__(self, context: Context) -> None:
        # Initialize the DummyCamera with a context of type AppSharedMem
        self.context = context

    def update(self):
        # This method is a placeholder and does nothing
        pass

    def release(self):
        # This method is a placeholder and does nothing
        pass

    def get_frame(self):
        # This method returns a copy of the current frame if it exists, otherwise it returns None
        if self.context.curr_frame is not None:
            return self.context.curr_frame.copy()
        else:
            return None


class ArmCamera:
    def __init__(self, cam_index: int, flip_h=False, flip_v=False):
        # Initialize the ArmCamera with a camera index and optional horizontal and vertical flip parameters
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.width = None
        self.height = None
        self.flip_h = flip_h
        self.flip_v = flip_v
        # Initialize the camera matrix and distortion coefficients
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
        # This method adds a crosshair to the given image data
        height, width = bgr_data.shape[0], bgr_data.shape[1]
        cv2.line(
            bgr_data, (int(width / 2), 0), (int(width / 2), height), BGR_GREEN, 1
        )  # Draw vertical line
        cv2.line(
            bgr_data, (0, int(height / 2)), (width, int(height / 2)), BGR_GREEN, 1
        )  # Draw horizontal line
        return bgr_data

    def update(self):
        # This method reads a frame from the camera, applies optional flips, undistorts the image, and updates the current frame
        ret, frame = self.cap.read()  # Read a frame from the camera
        if ret and self.width is None and self.height is None:
            self.width = frame.shape[0]  # Get the frame width
            self.height = frame.shape[1]  # Get the frame height

        if ret is not None:
            if self.flip_h:
                frame = cv2.flip(frame, 1)  # Flip horizontally
            if self.flip_v:
                frame = cv2.flip(frame, 0)  # Flip vertically
            calibed_frame = cv2.undistort(frame, self.mtx, self.dist, None)  # Correct the image
            self.current_frame = calibed_frame  # Update the current frame

    def get_frame(self):
        # This method returns a copy of the current frame if it exists, otherwise it returns None
        if self.current_frame is not None:
            return self.current_frame.copy()  # Return a copy of the current frame
        else:
            return None

    def release(self):
        # This method releases the camera
        self.cap.release()