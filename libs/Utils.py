# Importing necessary libraries and modules
from typing import *
import cv2
import numpy as np
from PySide6.QtGui import QPixmap, QImage
from typing import *

# Function to convert numpy array to QPixmap
def numpy_to_pixmap(arr: np.ndarray, image_format) -> QPixmap:
    # If the image format is grayscale
    if image_format == QImage.Format.Format_Grayscale8:
        h, w = arr.shape
        image = QImage(arr.data, w, h, w, image_format)
    else:
        # If the image format is not grayscale
        h, w, c = arr.shape
        image = QImage(arr.data, w, h, c * w, image_format)
    # Convert QImage to QPixmap
    pixmap = QPixmap.fromImage(image)
    return pixmap

# Function to crop frame by aruco
def crop_frame_by_aruco(frame, aruco_detector) -> Tuple[bool, np.ndarray]:
    """
    如果检测到二维码则切割,如果没有检测到二维码则返回原始帧

    Returns:
        bool: 是否检测到二维码
        np.ndarray: 返回帧
    """
    # Detect marker corners
    corners, ids, rejectedImgPoints = aruco_detector.detect_marker_corners(frame)
    # If no aruco detected, return original frame
    if ids is None or 1 not in ids or 2 not in ids or len(ids) != 2:
        return False, frame

    # Get coordinates of corners
    p1 = np.array(np.squeeze(corners)[0][0]).astype(int)
    p2 = np.array(np.squeeze(corners)[1][0]).astype(int)

    # Crop the frame
    croped_frame = crop_frame(frame, p1, p2)
    croped_frame = np.ascontiguousarray(croped_frame)
    return True, croped_frame

# Function to crop frame
def crop_frame(frame: np.ndarray, p1, p2) -> np.ndarray:
    # Get coordinates
    x1, y1 = p1
    x2, y2 = p2
    # Sort coordinates
    x1, x2 = (x1, x2) if x1 < x2 else (x2, x1)
    y1, y2 = (y1, y2) if y1 < y2 else (y2, y1)
    # Return cropped frame
    return frame[y1:y2, x1:x2]
