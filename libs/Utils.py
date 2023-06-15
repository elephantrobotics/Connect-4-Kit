from typing import *
import cv2
import numpy as np
from PySide6.QtGui import QPixmap, QImage
from typing import *


def numpy_to_pixmap(arr: np.ndarray, image_format) -> QPixmap:
    if image_format == QImage.Format.Format_Grayscale8:
        h, w = arr.shape
        image = QImage(arr.data, w, h, w, image_format)
    else:
        h, w, c = arr.shape
        image = QImage(arr.data, w, h, c * w, image_format)
    pixmap = QPixmap.fromImage(image)
    return pixmap


def crop_frame_by_aruco(frame, aruco_detector) -> Tuple[bool, np.ndarray]:
    """
    如果检测到二维码则切割,如果没有检测到二维码则返回原始帧

    Returns:
        bool: 是否检测到二维码
        np.ndarray: 返回帧
    """
    corners, ids, rejectedImgPoints = aruco_detector.detect_marker_corners(frame)
    if ids is None or 1 not in ids or 2 not in ids or len(ids) != 2:
        return False, frame

    p1 = np.array(np.squeeze(corners)[0][0]).astype(int)
    p2 = np.array(np.squeeze(corners)[1][0]).astype(int)

    croped_frame = crop_frame(frame, p1, p2)
    croped_frame = np.ascontiguousarray(croped_frame)
    return True, croped_frame


def crop_frame(frame: np.ndarray, p1, p2) -> np.ndarray:
    x1, y1 = p1
    x2, y2 = p2
    x1, x2 = (x1, x2) if x1 < x2 else (x2, x1)
    y1, y2 = (y1, y2) if y1 < y2 else (y2, y1)
    return frame[y1:y2, x1:x2]
